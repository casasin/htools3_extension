---
layout: default
title: Glyph
---

Tools to visualize and edit the current glyph.

<ul>
  {% for item in site.data.menu %}
    {% for subitem in item.submenu %}
      {% if subitem.title == 'glyph' %}
        {% for subsubitem in subitem.submenu %}
          <li><a href='{{ subsubitem.title | slugify }}'>{{ subsubitem.title }}</a></li>
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endfor %}
</ul>
