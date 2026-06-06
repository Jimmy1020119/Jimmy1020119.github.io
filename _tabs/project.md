---
title: Project
icon: fas fa-diagram-project
order: 4
---

{% assign posts = site.categories["Project"] %}
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
