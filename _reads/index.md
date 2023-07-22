---
layout: page
title : Books
---

{%- for book in site.reads -%}
    {%- if book.category == "book" -%}
    <li> <a class="page-link" href="{{ book.url | relative_url }}">{{ book.title | escape }}</a></li>
    {%- endif -%}
{%- endfor -%}