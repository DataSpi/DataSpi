---
layout: page
title: Blog
permalink: /blog/
---

Chào mọi người đến với góc nhỏ chia sẻ của Spyno về Data Engineering. Ở đây, mình sẽ viết về những trải nghiệm, kiến thức, và dự án liên quan đến lĩnh vực dữ liệu cũng như hành trình học tập và phát triển bản thân của mình. Mục tiêu của blog là tạo ra một nơi để chia sẻ và học hỏi cùng nhau trong cộng đồng Data Engineering.

Thực ra mình là một người viết đã lâu năm, mình có vài trang blog cá nhân về nhiều chủ đề khác nhau trong cuộc sống. Hiện tại thì mình chủ yếu chỉ còn viết trên Substack, các bạn có thể theo dõi mình tại đây: [Spyno Substack](https://spyno.substack.com/). Blog này sẽ là nơi mình tập trung chia sẻ về Data Engineering, và mình sẽ cố gắng cập nhật thường xuyên những bài viết mới nhất về chủ đề này. Mình cũng rất mong nhận được sự ủng hộ và góp ý từ các bạn để blog ngày càng hoàn thiện hơn.



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
