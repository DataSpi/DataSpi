---
layout: page
title: Blog
permalink: /blog/
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
