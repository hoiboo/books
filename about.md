---
layout: page
title: About
permalink: /about/
---

{%- for page in site.pages -%}
    <p> {{ page.path }} | {{ page.url }} </p>
{%- endfor -%}

<hr/>

{%- for book in site.reads -%}
    {%- if book.path contains "index.md" -%}
        <p> {{ book.path }} | {{ book.url }} </p>
    {%- endif -%}
{%- endfor -%}

<hr/>

{%- assign book_home = site.reads | where: "path", "_reads/index.md" | first -%}
<p> {{ book_home.path }} | {{ book_home.url }} </p>

<h2>categories </h2>
{%- for book in site.reads -%}
    {%- if book.category == "book" -%}
        <p> {{ book.path }}  | {{ book.title }} | {{ book.url }} </p>
    {%- endif -%}
{%- endfor -%}