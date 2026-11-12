"""Turn a Markdown study report into one HTML page.

Usage:
    uv run --with markdown python build_report_page.py REPORT.md OUT.html --header header.json [--kept-column NAME]

header.json gives the page header. Take every number from the report:
    {
      "title": "Short page title",
      "eyebrow": "Model · dataset · scope",
      "lede": "Two or three sentences: what the study did and what it found.",
      "figures": [{"value": "12.4 -> 15.1", "label": "what the number measures"}],
      "footer": "Sources: ..."
    }
All fields are optional except "title". Text is HTML-escaped.

The report needs numbered H2 sections ("## 1. Verdict", "## 2. ..."). The contents rail
comes from the H2 headings. Section 1 becomes the verdict box.
With --kept-column, the cells "yes" and "no" in that table column become "kept" and
"not kept" labels. Other columns are not changed.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

import markdown

CSS = """
/* Layout: lab report. Sticky contents rail on wide screens, one reading column, wide tables scroll in place. */
:root {
  --bg: #f6f7f9; --panel: #ffffff; --ink: #1b1f27; --muted: #5b6372; --rule: #d9dde4;
  --accent: #2a4bb0; --accent-soft: #e6ebf8; --ok: #1d7a4d; --ok-soft: #e1f2e8; --no: #a0412d; --no-soft: #f7e5e0;
  --code-bg: #eceef3;
  --f-display: "Archivo", "Helvetica Neue", Arial, sans-serif;
  --f-body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #12151b; --panel: #1a1e26; --ink: #e4e7ee; --muted: #9aa3b4; --rule: #2d333f;
  --accent: #8fa8ff; --accent-soft: #232c45; --ok: #6fd3a0; --ok-soft: #173326; --no: #f0957f; --no-soft: #3a211b;
  --code-bg: #232833; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #12151b; --panel: #1a1e26; --ink: #e4e7ee; --muted: #9aa3b4; --rule: #2d333f;
  --accent: #8fa8ff; --accent-soft: #232c45; --ok: #6fd3a0; --ok-soft: #173326; --no: #f0957f; --no-soft: #3a211b;
  --code-bg: #232833; color-scheme: dark; }
body { background: var(--bg); color: var(--ink); font-family: var(--f-body); font-size: 17px; line-height: 1.6;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 0 64px; }
a { color: var(--accent); }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
header { max-width: 1180px; margin: 0 auto; padding-block: 48px 28px; border-bottom: 1px solid var(--rule); }
.eyebrow { font-family: var(--f-mono); font-size: 12.5px; letter-spacing: .06em; text-transform: uppercase;
  color: var(--muted); }
h1 { font-family: var(--f-display); font-weight: 800; font-size: clamp(30px, 5vw, 46px); line-height: 1.1;
  margin: 10px 0 12px; text-wrap: balance; letter-spacing: -.01em; }
.lede { max-width: 68ch; color: var(--muted); font-size: 18px; margin: 0; }
.figs { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin-top: 28px; }
.fig { background: var(--panel); border: 1px solid var(--rule); border-radius: 6px; padding: 14px 16px;
  display: flex; flex-direction: column; gap: 4px; }
.fig b { font-family: var(--f-mono); font-size: 22px; font-weight: 600; font-variant-numeric: tabular-nums; }
.fig span { font-size: 14px; color: var(--muted); line-height: 1.35; }
.wrap { max-width: 1180px; margin: 0 auto; display: grid; grid-template-columns: 230px minmax(0, 1fr); gap: 48px;
  padding-top: 32px; }
nav { position: sticky; top: calc(env(safe-area-inset-top, 0px) + 20px); align-self: start; font-size: 14.5px; }
nav ol { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px; }
nav a { color: var(--muted); text-decoration: none; }
nav a:hover { color: var(--accent); }
main { min-width: 0; max-width: 820px; }
h2 { font-family: var(--f-display); font-weight: 700; font-size: 26px; margin: 52px 0 14px; padding-top: 14px;
  border-top: 2px solid var(--ink); text-wrap: balance; scroll-margin-top: 16px; }
h3 { font-family: var(--f-display); font-weight: 500; font-size: 19px; margin: 32px 0 8px; color: var(--ink); }
main > p, main li, section p, section li { max-width: 70ch; }
ul, ol { padding-left: 1.3em; }
li { margin: 4px 0; }
code { font-family: var(--f-mono); font-size: .84em; background: var(--code-bg); padding: 1px 5px; border-radius: 3px;
  overflow-wrap: anywhere; }
pre { background: var(--code-bg); padding: 12px 14px; border-radius: 6px; overflow-x: auto; }
pre code { background: none; padding: 0; }
.tw { overflow-x: auto; margin: 16px 0 20px; border: 1px solid var(--rule); border-radius: 6px;
  background: var(--panel); }
table { border-collapse: collapse; width: 100%; font-size: 14.5px; line-height: 1.4; }
th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--rule); vertical-align: top;
  font-variant-numeric: tabular-nums; }
th { font-family: var(--f-display); font-weight: 500; font-size: 13px; letter-spacing: .03em; text-transform: uppercase;
  color: var(--muted); background: var(--bg); white-space: nowrap; }
tr:last-child td { border-bottom: 0; }
td strong { color: var(--accent); }
.pill { display: inline-block; font-family: var(--f-mono); font-size: 12px; padding: 1px 8px; border-radius: 999px;
  white-space: nowrap; }
.pill.ok { background: var(--ok-soft); color: var(--ok); }
.pill.no { background: var(--no-soft); color: var(--no); }
.verdict { background: var(--accent-soft); border-radius: 8px; padding: 4px 22px 14px; }
.verdict h2 { border-top: 0; margin-top: 12px; }
.verdict .tw { background: var(--panel); }
footer { max-width: 1180px; margin: 56px auto 0; padding-top: 16px; border-top: 1px solid var(--rule);
  color: var(--muted); font-size: 14px; }
@media (max-width: 860px) {
  .wrap { grid-template-columns: minmax(0, 1fr); gap: 8px; }
  nav { position: static; border: 1px solid var(--rule); border-radius: 6px; padding: 12px 16px;
    background: var(--panel); }
  nav ol { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 16px; }
  h2 { font-size: 22px; }
  .verdict { padding: 2px 14px 10px; }
}
@media (max-width: 420px) { nav ol { grid-template-columns: 1fr; } body { font-size: 16px; } }
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800'
         '&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap">')

YES = re.compile(r"^(yes|\*\*yes\*\*|<strong>yes</strong>)$", re.I)
NO = re.compile(r"^(no|\*\*no\*\*|<strong>no</strong>)$", re.I)


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def label_kept_column(table: str, column: str) -> str:
    """Replace yes/no cells with labels, only in the column whose header is `column`."""
    heads = [strip_tags(h).lower() for h in re.findall(r"<th[^>]*>(.*?)</th>", table, flags=re.S)]
    if column.lower() not in heads:
        return table
    idx = heads.index(column.lower())

    def row(m: re.Match) -> str:
        cells = re.split(r"(<td[^>]*>.*?</td>)", m.group(0), flags=re.S)
        n = -1
        for i, part in enumerate(cells):
            if not part.startswith("<td"):
                continue
            n += 1
            if n != idx:
                continue
            inner = re.sub(r"^<td[^>]*>|</td>$", "", part).strip()
            if YES.match(inner):
                cells[i] = '<td><span class="pill ok">kept</span></td>'
            elif NO.match(inner):
                cells[i] = '<td><span class="pill no">not kept</span></td>'
        return "".join(cells)

    return re.sub(r"<tr>.*?</tr>", row, table, flags=re.S)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--header", type=Path, required=True, help="JSON file with title, eyebrow, lede, figures, footer")
    ap.add_argument("--kept-column", help="table column whose yes/no cells become kept/not kept labels")
    ap.add_argument("--standalone", action="store_true",
                    help="write a full HTML document (doctype, html, head, body) for use without the Artifact tool")
    a = ap.parse_args()

    head = json.loads(a.header.read_text(encoding="utf-8"))
    if not head.get("title"):
        print("error: header.json needs a non-empty 'title'", file=sys.stderr)
        return 2

    md = a.report.read_text(encoding="utf-8")
    md = re.sub(r"\A\s*# .*\n", "", md, count=1)  # drop the H1; the page has its own header
    md = re.sub(r"^  - ", "    - ", md, flags=re.M)
    body = markdown.markdown(md, extensions=["tables", "sane_lists", "fenced_code"])

    toc: list[tuple[str, str]] = []

    def h2(m: re.Match) -> str:
        text = strip_tags(m.group(1))
        num = re.match(r"(\d+)\.", text)
        plain = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        slug = f"s{num.group(1)}" if num else (plain or f"h{len(toc) + 1}")
        toc.append((slug, text or f"Section {len(toc) + 1}"))
        return f'<h2 id="{slug}">{m.group(1)}</h2>'

    body = re.sub(r"<h2>(.*?)</h2>", h2, body)
    if not toc:
        print("error: the report has no H2 sections ('## 1. Verdict', ...)", file=sys.stderr)
        return 2
    if a.kept_column:
        body = re.sub(r"<table>.*?</table>", lambda m: label_kept_column(m.group(0), a.kept_column), body, flags=re.S)
    body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    body = re.sub(r'(<h2 id="s1">.*?)(?=<h2 |\Z)', r'<section class="verdict">\1</section>', body, count=1, flags=re.S)

    e = html.escape
    toc_html = "\n".join(f'<li><a href="#{s}">{e(t)}</a></li>' for s, t in toc)
    figs = "".join(f'<div class="fig"><b>{e(str(f.get("value", "")))}</b>'
                   f'<span>{e(str(f.get("label", "")))}</span></div>'
                   for f in head.get("figures", []))
    eyebrow = f'<div class="eyebrow">{e(head["eyebrow"])}</div>' if head.get("eyebrow") else ""
    lede = f'<p class="lede">{e(head["lede"])}</p>' if head.get("lede") else ""
    figs_html = f'<div class="figs">{figs}</div>' if figs else ""
    footer = f"<footer>{e(head['footer'])}</footer>" if head.get("footer") else ""

    page = f"""<title>{e(head["title"])}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<style>{CSS}</style>

<header>
  {eyebrow}
  <h1>{e(head["title"])}</h1>
  {lede}
  {figs_html}
</header>

<div class="wrap">
  <nav aria-label="Contents"><ol>
{toc_html}
  </ol></nav>
  <main>
{body}
  </main>
</div>
{footer}
"""
    if a.standalone:
        head_part, _, body_part = page.partition("</style>")
        page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                f"{head_part}</style>\n</head>\n<body>{body_part}</body>\n</html>\n")
    a.out.write_text(page, encoding="utf-8")
    print(f"{len(page)} bytes; {len(toc)} sections")
    return 0


if __name__ == "__main__":
    sys.exit(main())
