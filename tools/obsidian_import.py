#!/usr/bin/env python3
"""Import an Obsidian markdown file into this blog repo.

What it does:
- Reads a .md file from a hardcoded Obsidian vault.
- Copies the markdown file content into _blogs/.
- Finds Obsidian image embeds like: ![[Pasted image 20260528172841.png]]
- Copies embedded image files into assets/media/.
- Rewrites embed syntax to standard markdown image links for VS Code/Jekyll.
- Converts markdown image links that point to YouTube into clickable thumbnail previews.
- Converts Obsidian admonition blocks (```ad-...```) into styled HTML callouts.

Hướng dẫn sử dụng: Activate conda env rồi run câu sau: 

python tools/obsidian_import.py "Bài 1 - Từ Bản Vẽ Tên Lửa Đến Phép Toán Tập Hợp - Bình Minh Của Dữ Liệu Giao Dịch"  
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.error import URLError
from urllib.parse import parse_qs, quote, urlparse
from urllib.request import urlopen

# Hardcoded paths (edit these once to match your machine)
# OBSIDIAN_VAULT = Path(r"C:\Users\LAP14354\OneDrive - VNG Corporation\Documents\Kiem - LEGO\Zettelkasten")
OBSIDIAN_VAULT = Path(r"/Users/spinokiem/Library/CloudStorage/OneDrive-VNGGroupJSC/Documents/Kiem - LEGO/Zettelkasten")
REPO_ROOT = Path(__file__).resolve().parents[1]
BLOGS_DIR = REPO_ROOT / "_blogs"
MEDIA_DIR = REPO_ROOT / "assets" / "media"

# Matches: ![[file.png]] or ![[file.png|400]] or ![[folder/file.png|alt text]]
OBSIDIAN_EMBED_RE = re.compile(r"!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((https?://[^\s)]+)\)")
ADMONITION_RE = re.compile(r"```ad-([a-zA-Z0-9_-]+)\n(.*?)\n```", re.DOTALL)
HTML_CALLOUT_RE = re.compile(
    r'<div class="obs-callout obs-callout-([a-zA-Z0-9_-]+)"(?:\s+markdown="1")?>\s*\n'
    r'<div class="obs-callout-title">([^<]+)</div>\s*\n'
    r"(.*?)\n</div>",
    re.DOTALL,
)
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}
OBSIDIAN_META_LINE_RE = re.compile(
    r"^(Status:\s*.*|Tag:\s*.*|Tags:\s*.*|Linking Notes:\s*.*)$",
    re.IGNORECASE,
)
OBSIDIAN_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import Obsidian markdown and convert image embeds.",
    )
    parser.add_argument(
        "input_filename",
        help="Markdown filename inside Obsidian vault (example: note.md)",
    )
    return parser.parse_args()


def remove_existing_front_matter(content: str) -> str:
    stripped = content.lstrip()
    if not stripped.startswith("---\n"):
        return content

    lines = stripped.splitlines()
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return content

    remaining = "\n".join(lines[end_idx + 1 :])
    return remaining.lstrip("\n")


def strip_obsidian_header_lines(content: str) -> str:
    lines = content.splitlines()
    idx = 0

    while idx < len(lines):
        current = lines[idx].strip()
        if not current:
            idx += 1
            continue

        if OBSIDIAN_DATETIME_RE.match(current) or OBSIDIAN_META_LINE_RE.match(current):
            idx += 1
            continue
        break

    return "\n".join(lines[idx:]).lstrip("\n")


def infer_excerpt(content: str) -> str:
    for line in content.splitlines():
        text = line.strip()
        if not text:
            continue
        if text.startswith("#"):
            continue
        if text.startswith("```"):
            continue
        if text.startswith("<") and text.endswith(">"):
            continue
        if text.startswith(("- ", "* ", ">")):
            continue

        text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
        text = re.sub(r"!\[[^\]]*\]\([^\)]+\)", "", text).strip()
        if not text:
            continue

        sentence_match = re.search(r"(.+?[.!?])(?:\s|$)", text)
        sentence = sentence_match.group(1).strip() if sentence_match else text
        return sentence.replace('"', '\\"')

    return ""


def build_front_matter(title: str, excerpt: str) -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        "layout: page\n"
        f'title: "{title}"\n'
        f"date: {today}\n"
        f'excerpt: "{excerpt}"\n'
        "toc: true\n"
        "---\n\n"
    )


def resolve_markdown_source(input_filename: str) -> Path:
    raw_input = input_filename.strip()
    candidate_inputs = [raw_input]

    # Allow users to pass filenames without the markdown extension.
    if Path(raw_input).suffix == "":
        candidate_inputs.append(f"{raw_input}.md")

    for candidate_name in candidate_inputs:
        source = OBSIDIAN_VAULT / candidate_name
        if source.exists() and source.is_file():
            return source

    matches: list[Path] = []
    for candidate_name in candidate_inputs:
        matches.extend(p for p in OBSIDIAN_VAULT.rglob(candidate_name) if p.is_file())

    # Deduplicate while preserving order.
    unique_matches: list[Path] = []
    seen: set[Path] = set()
    for match in matches:
        if match in seen:
            continue
        seen.add(match)
        unique_matches.append(match)

    if not unique_matches:
        raise FileNotFoundError(
            f"Cannot find markdown file '{input_filename}' in vault: {OBSIDIAN_VAULT}"
        )

    if len(unique_matches) > 1:
        preview = "\n".join(f"- {m}" for m in unique_matches[:5])
        raise FileExistsError(
            "Found multiple files with the same name. Please pass a more specific path\n"
            f"within the vault. Example matches:\n{preview}"
        )

    return unique_matches[0]


def find_image_in_vault(source_md: Path, embedded_name: str) -> Path | None:
    candidate = (source_md.parent / embedded_name).resolve()
    if candidate.exists() and candidate.is_file():
        return candidate

    candidate = (OBSIDIAN_VAULT / embedded_name).resolve()
    if candidate.exists() and candidate.is_file():
        return candidate

    filename_only = Path(embedded_name).name
    matches = [p for p in OBSIDIAN_VAULT.rglob(filename_only) if p.is_file()]
    if not matches:
        return None

    return matches[0]


def to_markdown_path_for_blog(image_filename: str) -> str:
    encoded = quote(image_filename)
    return f"{{{{ '/assets/media/{encoded}' | relative_url }}}}"


def extract_youtube_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()

    if "youtube.com" in host:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
            return video_id

        path_parts = [part for part in parsed.path.split("/") if part]
        if len(path_parts) >= 2 and path_parts[0] in {"embed", "shorts"}:
            return path_parts[1]

    if "youtu.be" in host:
        path_parts = [part for part in parsed.path.split("/") if part]
        if path_parts:
            return path_parts[0]

    return None


def convert_youtube_image_links(content: str) -> tuple[str, int]:
    converted_count = 0
    title_cache: dict[str, str] = {}

    def fetch_youtube_title(video_id: str) -> str | None:
        if video_id in title_cache:
            return title_cache[video_id]

        watch_url = f"https://www.youtube.com/watch?v={video_id}"
        oembed_url = (
            "https://www.youtube.com/oembed"
            f"?url={quote(watch_url, safe=':/?=&')}&format=json"
        )

        try:
            with urlopen(oembed_url, timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
                title = (payload.get("title") or "").strip()
                if title:
                    title_cache[video_id] = title
                    return title
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            pass

        title_cache[video_id] = ""
        return None

    def replacer(match: re.Match[str]) -> str:
        nonlocal converted_count

        alt_text = (match.group(1) or "").strip()
        url = match.group(2).strip()
        video_id = extract_youtube_video_id(url)

        if not video_id:
            return match.group(0)

        converted_count += 1
        resolved_title = fetch_youtube_title(video_id)
        safe_alt = resolved_title or alt_text or f"YouTube video {video_id}"
        watch_url = f"https://www.youtube.com/watch?v={video_id}"
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        safe_title_attr = safe_alt.replace('"', "&quot;")
        return (
            '<div class="yt-embed">\n'
            f'  <iframe src="{embed_url}" title="{safe_title_attr}" '
            'loading="lazy" allow="accelerometer; autoplay; clipboard-write; '
            'encrypted-media; gyroscope; picture-in-picture; web-share" '
            'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n'
            f'  <p class="yt-embed-caption"><a href="{watch_url}" target="_blank" rel="noopener">{safe_alt}</a></p>\n'
            '</div>'
        )

    updated = MARKDOWN_IMAGE_RE.sub(replacer, content)
    return updated, converted_count


def normalize_callout_label(callout_type: str) -> str:
    words = [w for w in re.split(r"[-_]", callout_type.strip()) if w]
    if not words:
        return "Callout"
    return " ".join(word.capitalize() for word in words)


def convert_obsidian_admonitions(content: str) -> tuple[str, int]:
    converted_count = 0

    def replacer(match: re.Match[str]) -> str:
        nonlocal converted_count

        raw_type = (match.group(1) or "note").strip().lower()
        body = (match.group(2) or "").strip("\n")
        label = normalize_callout_label(raw_type)

        converted_count += 1
        return (
            f'<div class="obs-callout obs-callout-{raw_type}" markdown="1">\n'
            f'<div class="obs-callout-title">{label}</div>\n\n'
            f"{body}\n"
            f"</div>"
        )

    updated = ADMONITION_RE.sub(replacer, content)
    return updated, converted_count


def convert_html_callouts(content: str) -> tuple[str, int]:
    # Keep already-converted HTML callouts intact.
    return content, 0


def convert_markdown_callout_blockquotes(content: str) -> tuple[str, int]:
    lines = content.splitlines()
    output: list[str] = []
    converted_count = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        if not line.startswith(">"):
            output.append(line)
            i += 1
            continue

        start = i
        while i < len(lines) and lines[i].startswith(">"):
            i += 1

        block = lines[start:i]
        stripped = [re.sub(r"^>\s?", "", b) for b in block]

        first_non_empty = 0
        while first_non_empty < len(stripped) and not stripped[first_non_empty].strip():
            first_non_empty += 1

        if first_non_empty >= len(stripped):
            output.extend(block)
            continue

        marker = stripped[first_non_empty].strip()
        marker_match = re.fullmatch(r"\*\*([^*]+)\*\*", marker)
        if not marker_match:
            output.extend(block)
            continue

        label = marker_match.group(1).strip()
        if not label:
            output.extend(block)
            continue

        callout_type = re.sub(r"[^a-z0-9_-]+", "-", label.lower()).strip("-") or "note"
        body_lines = stripped[first_non_empty + 1 :]
        body = "\n".join(body_lines).strip("\n")

        output.append(f'<div class="obs-callout obs-callout-{callout_type}" markdown="1">')
        output.append(f'<div class="obs-callout-title">{label}</div>')
        output.append("")
        if body:
            output.extend(body.splitlines())
        output.append("</div>")

        converted_count += 1

    return "\n".join(output), converted_count


def convert_embeds_and_copy_images(content: str, source_md: Path) -> tuple[str, list[str], list[str]]:
    copied: list[str] = []
    missing: list[str] = []

    def replacer(match: re.Match[str]) -> str:
        embedded_raw = match.group(1).strip()
        width_or_alias = (match.group(2) or "").strip()

        embedded_path = Path(embedded_raw)
        if embedded_path.suffix.lower() not in IMAGE_EXTENSIONS:
            return match.group(0)

        src_image = find_image_in_vault(source_md, embedded_raw)
        if src_image is None:
            missing.append(embedded_raw)
            return match.group(0)

        MEDIA_DIR.mkdir(parents=True, exist_ok=True)
        target_image = MEDIA_DIR / src_image.name

        if not target_image.exists() or src_image.stat().st_mtime > target_image.stat().st_mtime:
            shutil.copy2(src_image, target_image)
            copied.append(src_image.name)

        alt_text = width_or_alias or src_image.stem
        markdown_path = to_markdown_path_for_blog(src_image.name)
        return f"![{alt_text}]({markdown_path})"

    updated = OBSIDIAN_EMBED_RE.sub(replacer, content)
    return updated, copied, missing


def main() -> int:
    args = parse_args()

    try:
        source_md = resolve_markdown_source(args.input_filename)
    except (FileNotFoundError, FileExistsError) as exc:
        print(f"ERROR: {exc}")
        return 1

    BLOGS_DIR.mkdir(parents=True, exist_ok=True)
    target_md = BLOGS_DIR / source_md.name

    content = source_md.read_text(encoding="utf-8")
    content = remove_existing_front_matter(content)
    content = strip_obsidian_header_lines(content)

    updated, copied_images, missing_images = convert_embeds_and_copy_images(content, source_md)
    updated, youtube_previews = convert_youtube_image_links(updated)
    updated, converted_md_callouts = convert_markdown_callout_blockquotes(updated)
    updated, converted_html_callouts = convert_html_callouts(updated)
    updated, converted_admonitions = convert_obsidian_admonitions(updated)

    title = source_md.stem
    excerpt = infer_excerpt(updated)
    front_matter = build_front_matter(title=title, excerpt=excerpt)
    target_md.write_text(front_matter + updated.lstrip("\n"), encoding="utf-8")

    print(f"Imported markdown: {source_md} -> {target_md}")
    if copied_images:
        print("Copied images:")
        for name in sorted(set(copied_images)):
            print(f"- {name}")

    if missing_images:
        print("Missing images (kept original embed syntax):")
        for name in sorted(set(missing_images)):
            print(f"- {name}")

    if youtube_previews:
        print(f"Converted YouTube previews: {youtube_previews}")

    if converted_admonitions:
        print(f"Converted admonition blocks: {converted_admonitions}")

    if converted_html_callouts:
        print(f"Converted HTML callouts: {converted_html_callouts}")

    if converted_md_callouts:
        print(f"Converted markdown callouts: {converted_md_callouts}")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
