---
layout: page
title: Blog
permalink: /blog/
---

Xin chào tất cả mọi người, mình là Spyno. Chào mừng mọi người đến với góc nhỏ mình xây lên để chia sẻ một vài điều thú vị đến mọi người. 

Thực ra mình là một người đã tập viết lâu năm, từng xuất hiện trên nhiều nền tảng khác nhau. Gần đây thì mình chủ yếu viết trên [Spyno Substack](https://spyno.substack.com/) và vẫn sẽ tiếp tục viết trên này về các chủ đề chung trong cuộc sống, chia sẻ cá nhân, quan điểm của mình về một điều gì đó.  Kênh này sẽ được duy trì song song cùng với substack, với mục đích chia sẻ các bài viết chuyên sâu trong mảng dữ liệu, công nghệ, và hành trình đi làm của mình. 

Một vài lời giới thiệu ngắn thế thôi, mọi người hãy đón đọc những bài viết của mình nhé. 

---

{% assign sorted_blogs = site.blogs | sort: 'date' | reverse %}

{% if sorted_blogs.size > 0 %}
<ul class="blog-list">
  {% for post in sorted_blogs %}
  <li class="blog-list-item">
    <h2 class="blog-list-title">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h2>
    <p class="blog-list-meta">{{ post.date | date: "%b %d, %Y" }}</p>
    {% if post.excerpt %}
    <p class="blog-list-excerpt">{{ post.excerpt | strip_html | truncate: 180 }}</p>
    {% endif %}
  </li>
  {% endfor %}
</ul>
{% else %}
<p>Chua co bai viet nao. Ban co the tao bai dau tien trong thu muc <strong>_blogs</strong>.</p>
{% endif %}
