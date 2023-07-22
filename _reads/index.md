---
layout: page
title : Books
---

{%- for book in site.reads -%}
    {%- if book.category == "book" -%}
    <li><a href="{{ book.url }}">{{ book.title }}</a></li>
    {%- endif -%}
{%- endfor -%}