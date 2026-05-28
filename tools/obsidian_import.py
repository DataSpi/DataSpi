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
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

# Hardcoded paths (edit these once to match your machine)
OBSIDIAN_VAULT = Path(r"C:\Users\LAP14354\OneDrive - VNG Corporation\Documents\Kiem - LEGO\Zettelkasten")
REPO_ROOT = Path(__file__).resolve().parents[1]
BLOGS_DIR = REPO_ROOT / "_blogs"
MEDIA_DIR = REPO_ROOT / "assets" / "media"

# Matches: ![[file.png]] or ![[file.png|400]] or ![[folder/file.png|alt text]]
OBSIDIAN_EMBED_RE = re.compile(r"!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((https?://[^\s)]+)\)")
ADMONITION_RE = re.compile(r"```ad-([a-zA-Z0-9_-]+)\n(.*?)\n```", re.DOTALL)
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import Obsidian markdown and convert image embeds.",
    )
    parser.add_argument(
        "input_filename",
        help="Markdown filename inside Obsidian vault (example: note.md)",
    )
    return parser.parse_args()


def resolve_markdown_source(input_filename: str) -> Path:
    source = OBSIDIAN_VAULT / input_filename
    if source.exists() and source.is_file():
        return source

    matches = list(OBSIDIAN_VAULT.rglob(input_filename))
    matches = [p for p in matches if p.is_file()]

    if not matches:
        raise FileNotFoundError(
            f"Cannot find markdown file '{input_filename}' in vault: {OBSIDIAN_VAULT}"
        )

    if len(matches) > 1:
        preview = "\n".join(f"- {m}" for m in matches[:5])
        raise FileExistsError(
            "Found multiple files with the same name. Please pass a more specific path\n"
            f"within the vault. Example matches:\n{preview}"
        )

    return matches[0]


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
    return f"../assets/media/{encoded}"


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

    def replacer(match: re.Match[str]) -> str:
        nonlocal converted_count

        alt_text = (match.group(1) or "").strip()
        url = match.group(2).strip()
        video_id = extract_youtube_video_id(url)

        if not video_id:
            return match.group(0)

        converted_count += 1
        safe_alt = alt_text or f"YouTube video {video_id}"
        watch_url = f"https://www.youtube.com/watch?v={video_id}"
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        return f"[![{safe_alt}]({thumbnail_url})]({watch_url})"

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
    updated, copied_images, missing_images = convert_embeds_and_copy_images(content, source_md)
    updated, youtube_previews = convert_youtube_image_links(updated)
    updated, converted_admonitions = convert_obsidian_admonitions(updated)
    target_md.write_text(updated, encoding="utf-8")

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

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
