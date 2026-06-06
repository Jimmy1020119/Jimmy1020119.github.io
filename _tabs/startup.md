---
title: Startup
icon: fas fa-rocket
order: 3
---

{% assign posts = site.categories["Startup"] %}
{% if posts and posts.size > 0 %}
<ul class="content">
  {% for post in posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <span style="color:var(--sp-text-muted);font-size:.8rem;"> — {{ post.date | date: "%Y-%m-%d" }}</span>
  </li>
  {% endfor %}
</ul>
{% else %}
<p>No posts yet.</p>
{% endif %}
