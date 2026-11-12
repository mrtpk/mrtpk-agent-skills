"""Render Markdown notes (KB, outline) to standalone HTML files beside them.

Usage: uv run --with markdown python -I md2html.py <file.md> [<file.md> ...]
"""

import html
import pathlib
import sys

import markdown

CSS = """
body{font-family:Inter,Segoe UI,Helvetica,Arial,sans-serif;font-size:17px;line-height:1.65;color:#292929;
background:#fff;max-width:860px;margin:40px auto;padding:0 16px}
h1,h2,h3{color:#141414;line-height:1.3} h1{font-size:30px}
h2{font-size:23px;margin-top:2em;border-bottom:1px solid #e5e7eb;padding-bottom:4px} h3{font-size:19px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.88em;background:#f3f4f6;
padding:1px 4px;border-radius:4px}
pre{background:#f6f8fa;padding:12px 14px;border-radius:8px;overflow-x:auto} pre code{background:none;padding:0}
table{border-collapse:collapse;margin:1em 0;font-size:.92em;display:block;overflow-x:auto}
th,td{border:1px solid #e5e7eb;padding:6px 10px;vertical-align:top} th{background:#f9fafb}
blockquote{border-left:3px solid #d1d5db;margin:1em 0;padding:.2em 1em;color:#4b5563} a{color:#2563eb}
img{max-width:100%}
"""
HEAD = '<!doctype html><html lang="en"><head><meta charset="utf-8">' \
       '<meta name="viewport" content="width=device-width,initial-scale=1">'

for p in map(pathlib.Path, sys.argv[1:]):
    body = markdown.markdown(p.read_text(encoding="utf-8"), extensions=["tables", "fenced_code", "sane_lists", "toc"])
    title = html.escape(p.stem.replace("_", " "))
    out = p.with_suffix(".html")
    out.write_text(f"{HEAD}<title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>",
                   encoding="utf-8")
    print("wrote", out.name)
