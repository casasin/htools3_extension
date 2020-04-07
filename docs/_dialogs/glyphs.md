---
layout: default
title: Glyphs
---

<style>
.container {
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-content: flex-start;
  justify-content: flex-start;
}
.item {
  flex: 0 0 auto;
  min-width: 16em;
  margin-bottom: 1em;
}
.item h4 {
  margin: 0;
}
</style>

Tools to apply actions to the current glyph or to selected glyphs.

<div class='container'>

{% for item in site.data.menu %}
  {% for subitem in item.submenu %}
    {% if subitem.title == 'glyphs' %}
      {% for subsubitem in subitem.submenu %}

<div class='item'>
<h4>{{ subsubitem.title }}</h4>
<ul style='margin-bottom:0;'>
  {% for subsubsubitem in subsubitem.submenu %}
  <li>
    {% capture subsubsubitem_url %}{{ subitem.title }}/{{ subsubitem.title | slugify }}/{{ subsubsubitem.title | slugify }}{% endcapture %}
    <a href='{{ subsubsubitem_url | relative_url }}'>{{ subsubsubitem.title }}</a>
  </li>
  {% endfor %}
</ul>
</div>

      {% endfor %}
    {% endif %}
  {% endfor %}
{% endfor %}

</div>