"""Write the brand tokens and the voice files from brand-kit/ into the skills, or check them.

Usage (from the repo root):
    python3 brand-kit/tools/sync_brand.py           # write every region and copy
    python3 brand-kit/tools/sync_brand.py --check   # exit 1 when a region, a copy or a literal drifts

brand-kit/tokens.json is the one source. A skill holds a synced copy of what it needs, so that each skill
folder stays installable alone. Two kinds of target:

- Region: the lines between a "BEGIN brand-kit:<name>" line and an "END brand-kit:<name>" line. The
  marker lines use the comment syntax of the file. The script rewrites only the lines between them.
- Copy: a whole file (a voice file), with one generated header line.

--check also scans every text file of the consumer skills for colour literals (#rgb, #rrggbb) outside
the regions. Each literal must be a current token value, or be listed in brand-kit/allowlist.json
(colours that are not brand, for example syntax highlighting). A literal that was a token value before
a change fails the check, so no stale copy stays hidden.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from pathlib import Path
from typing import Callable

KIT = Path(__file__).resolve().parent.parent
ROOT = KIT.parent
SKILLS = ROOT / "skills"
TOKENS = json.loads((KIT / "tokens.json").read_text(encoding="utf-8"))
ALLOW: dict[str, dict[str, str]] = json.loads((KIT / "allowlist.json").read_text(encoding="utf-8"))

HEX = re.compile(r"(?<!&)#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-zA-Z_-])")
TEXT_SUFFIXES = {".py", ".css", ".html", ".md", ".json", ".js", ".svg", ".yaml", ".yml", ".markdown", ".txt"}
SCAN_SKILLS = [
    "svg-figures",
    "codebase-explainer",
    "code-to-md-writeup",
    "report-to-page",
    "design-plan-presentation",
    "code-to-kaizen-blog",
]

Renderer = Callable[[], list[str]]


# ---------------------------------------------------------------- token access

def page(theme: str, name: str) -> str:
    return str(TOKENS["page"][theme][name])


def status(theme: str, name: str) -> str:
    return str(TOKENS["status"][theme][name])


def font(name: str) -> str:
    return str(TOKENS["fonts"][name])


def favicon_data_uri() -> str:
    data = (KIT / TOKENS["favicon"]["file"]).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def css_vars(pairs: list[tuple[str, str]], indent: str = "  ") -> list[str]:
    return [f"{indent}--{name}: {value};" for name, value in pairs]


def wrap(lines: list[str], width: int = 110) -> list[str]:
    """Break long CSS lines after a comma, for CSS inside a Python string (flake8 limit 120)."""
    out: list[str] = []
    for line in lines:
        while len(line) > width and ", " in line[:width]:
            cut = line[:width].rindex(", ") + 1
            out.append(line[:cut])
            line = "    " + line[cut:].lstrip()
        out.append(line)
    return out


# ---------------------------------------------------------------- renderers

def svglib_tokens() -> list[str]:
    fig = TOKENS["figure"]
    out = [f'{k} = "{v}"' for k, v in fig["neutrals"].items()]
    out.append("")
    for k, v in fig["roles"].items():
        if not k.startswith("_"):
            out.append(f"{k} = (" + ", ".join(f'"{c}"' for c in v) + ")")
    out.append(f'TEAL_STRONG_TINT = "{fig["TEAL_STRONG_TINT"]}"')
    out.append("")
    out.append("SERIES = [" + ", ".join(f'"{c}"' for c in fig["series"]) + "]")
    out.append(f'SANS = "{font("figure_sans")}"')
    out.append(f'MONO = "{font("figure_mono")}"')
    return out


def site_page(theme: str) -> Renderer:
    def render() -> list[str]:
        pairs: list[tuple[str, str]] = []
        if theme == "light":
            pairs += [("sans", font("page_sans")), ("mono", font("page_mono"))]
        pairs += list(TOKENS["page"][theme].items())
        return css_vars(pairs)
    return render


def viz_series(key: str) -> Renderer:
    def render() -> list[str]:
        cols = TOKENS["figure"][key]
        first = " ".join(f"--viz-c{i + 1}: {c};" for i, c in enumerate(cols[:4]))
        second = " ".join(f"--viz-c{i + 5}: {c};" for i, c in enumerate(cols[4:]))
        return ["  " + first, "  " + second]
    return render


def explainer_build_consts() -> list[str]:
    return [
        f'BRAND_INTER_CSS_URL = "{font("inter_css_url")}"  # noqa: E501',
        f'BRAND_MARK_FILL = "{page("light", "link")}"',
        f'BRAND_MARK_FONT = "{font("figure_mono")}"',
    ]


def preview_page_css() -> list[str]:
    """md2html.py and render_review.py: one :root rule with the page tokens they use."""
    names = ["ink", "ink-strong", "mute", "line", "border", "bg", "sidebar-bg", "link",
             "code-bg", "inline-code-bg"]
    lines = [":root{", "--sans:" + font("page_sans") + ";", "--mono:" + font("page_mono") + ";"]
    lines += [f"--{n}:{page('light', n)};" for n in names]
    return wrap(lines + ["}"])


REPORT_MAP = [
    ("bg", "sidebar-bg"), ("panel", "surface"), ("ink", "ink"), ("muted", "mute"), ("rule", "border"),
    ("accent", "link"), ("accent-soft", "blue-tint"), ("code-bg", "code-bg"),
]


def report_tokens(theme: str, indent: str) -> Renderer:
    def render() -> list[str]:
        pairs = [(name, page(theme, tok)) for name, tok in REPORT_MAP]
        pairs += [("ok", status(theme, "kept")), ("ok-soft", status(theme, "kept-tint")),
                  ("no", status(theme, "not-kept")), ("no-soft", status(theme, "not-kept-tint"))]
        if theme == "light":
            pairs += [("f-display", font("page_sans")), ("f-body", font("page_sans")),
                      ("f-mono", font("page_mono"))]
        return wrap(css_vars(pairs, indent))
    return render


def report_py_consts() -> list[str]:
    return [
        f'BRAND_INTER_CSS_URL = "{font("inter_css_url")}"  # noqa: E501',
        f'BRAND_FAVICON = "{favicon_data_uri()}"  # noqa: E501',
    ]


def presentation_tokens(theme: str) -> Renderer:
    def render() -> list[str]:
        fig = TOKENS["figure"]["roles"]
        pairs = [("bg", page(theme, "bg")), ("panel", page(theme, "panel-bg")), ("ink", page(theme, "ink")),
                 ("mute", page(theme, "mute")), ("line", page(theme, "line"))]
        if theme == "light":
            pairs += [("accent", fig["VIOLET"][0]), ("accent-ink", page("light", "white")),
                      ("c1", fig["BLUE"][0]), ("c1-t", fig["BLUE"][1]),
                      ("c2", fig["AMBER"][0]), ("c2-t", fig["AMBER"][1]),
                      ("c3", fig["EMERALD"][0]), ("c3-t", fig["EMERALD"][1]),
                      ("sans", font("page_sans")), ("mono", font("page_mono"))]
        else:
            pairs += [("accent", page("dark", "violet")), ("accent-ink", page("dark", "bg")),
                      ("c1", page("dark", "blue")), ("c1-t", page("dark", "blue-tint")),
                      ("c2", page("dark", "amber")), ("c2-t", page("dark", "amber-tint")),
                      ("c3", page("dark", "emerald")), ("c3-t", page("dark", "emerald-tint"))]
        return css_vars(pairs)
    return render


def presentation_head() -> list[str]:
    url = font("inter_css_url").replace("&", "&amp;")
    return [
        f'<link rel="icon" type="image/png" href="{favicon_data_uri()}">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        f'<link rel="stylesheet" href="{url}">',
    ]


# ---------------------------------------------------------------- targets

REGIONS: list[tuple[str, str, Renderer]] = [
    ("svg-figures/tools/svglib.py", "figure-tokens", svglib_tokens),
    ("codebase-explainer/templates/assets/site.css", "page-light", site_page("light")),
    ("codebase-explainer/templates/assets/site.css", "page-dark", site_page("dark")),
    ("codebase-explainer/templates/assets/viz/viz.css", "series-light", viz_series("series")),
    ("codebase-explainer/templates/assets/viz/viz.css", "series-dark", viz_series("series_dark")),
    ("codebase-explainer/templates/build.py", "explainer-consts", explainer_build_consts),
    ("code-to-md-writeup/scripts/md2html.py", "preview-css", preview_page_css),
    ("code-to-kaizen-blog/scripts/render_review.py", "preview-css", preview_page_css),
    ("report-to-page/build_report_page.py", "report-light", report_tokens("light", "  ")),
    ("report-to-page/build_report_page.py", "report-dark-media", report_tokens("dark", "  ")),
    ("report-to-page/build_report_page.py", "report-dark-toggle", report_tokens("dark", "  ")),
    ("report-to-page/build_report_page.py", "report-consts", report_py_consts),
    ("design-plan-presentation/templates/presentation.html", "head", presentation_head),
    ("design-plan-presentation/templates/presentation.html", "page-light", presentation_tokens("light")),
    ("design-plan-presentation/templates/presentation.html", "page-dark", presentation_tokens("dark")),
]

TECH = "voice/tech-docs.md"
BLOG = "voice/blog.md"
COPIES: list[tuple[str, str]] = [
    ("svg-figures/references/voice.md", TECH),
    ("codebase-explainer/references/voice.md", TECH),
    ("code-to-md-writeup/references/voice.md", TECH),
    ("report-to-page/references/voice.md", TECH),
    ("design-plan-presentation/references/voice.md", TECH),
    ("code-to-kaizen-blog/references/voice.md", BLOG),
]


# ---------------------------------------------------------------- engine

def region_span(lines: list[str], name: str, path: str) -> tuple[int, int]:
    begin_re = re.compile(rf"BEGIN brand-kit:{re.escape(name)}(?![\w-])")
    end_re = re.compile(rf"END brand-kit:{re.escape(name)}(?![\w-])")
    begin = [i for i, s in enumerate(lines) if begin_re.search(s)]
    end = [i for i, s in enumerate(lines) if end_re.search(s)]
    if len(begin) != 1 or len(end) != 1 or end[0] < begin[0]:
        raise SystemExit(f"error: {path}: need exactly one BEGIN and one END marker for brand-kit:{name}")
    return begin[0], end[0]


def sync_regions(write: bool) -> list[str]:
    problems: list[str] = []
    by_file: dict[str, list[tuple[str, Renderer]]] = {}
    for rel, name, render in REGIONS:
        by_file.setdefault(rel, []).append((name, render))
    for rel, items in by_file.items():
        path = SKILLS / rel
        raw = path.read_bytes().decode("utf-8")
        newline = "\r\n" if "\r\n" in raw else "\n"
        lines = raw.split(newline)
        for name, render in items:
            b, e = region_span(lines, name, rel)
            want = render()
            if lines[b + 1:e] != want:
                problems.append(f"{rel}: region brand-kit:{name} differs from tokens.json")
                lines[b + 1:e] = want
        new = newline.join(lines)
        if write and new != raw:
            path.write_bytes(new.encode("utf-8"))
    return problems


def copy_text(src: str) -> str:
    body = (KIT / src).read_text(encoding="utf-8")
    header = (f"<!-- Synced from brand-kit/{src} by brand-kit/tools/sync_brand.py. "
              "Do not edit here; edit the brand-kit file and run the sync. -->\n")
    return header + body


def sync_copies(write: bool) -> list[str]:
    problems: list[str] = []
    for rel, src in COPIES:
        path = SKILLS / rel
        want = copy_text(src)
        have = path.read_text(encoding="utf-8") if path.exists() else None
        if have != want:
            problems.append(f"{rel}: copy differs from brand-kit/{src}")
            if write:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(want, encoding="utf-8")
    return problems


def norm(hex_value: str) -> str:
    h = hex_value.lower()
    return "#" + "".join(c * 2 for c in h[1:]) if len(h) == 4 else h


def token_values() -> set[str]:
    found: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
        elif isinstance(node, str):
            found.update(norm(m) for m in HEX.findall(node))
    walk(TOKENS)
    return found


def region_lines(lines: list[str]) -> set[int]:
    inside: set[int] = set()
    open_at: int | None = None
    for i, s in enumerate(lines):
        if "BEGIN brand-kit:" in s:
            open_at = i
        elif "END brand-kit:" in s and open_at is not None:
            inside.update(range(open_at, i + 1))
            open_at = None
    return inside


def scan_literals() -> list[str]:
    problems: list[str] = []
    known = token_values()
    for skill in SCAN_SKILLS:
        for path in sorted((SKILLS / skill).rglob("*")):
            if not path.is_file() or path.suffix not in TEXT_SUFFIXES or "__pycache__" in path.parts:
                continue
            rel = path.relative_to(SKILLS).as_posix()
            allowed = {norm(h) for h in ALLOW.get(rel, {}) if h.startswith("#")}
            lines = path.read_text(encoding="utf-8").splitlines()
            skip = region_lines(lines)
            for i, line in enumerate(lines):
                if i in skip:
                    continue
                for m in HEX.findall(line):
                    if norm(m) not in known and norm(m) not in allowed:
                        problems.append(f"{rel}:{i + 1}: colour {m} is not a token value and not in allowlist.json")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report drift; change no file")
    args = ap.parse_args()
    write = not args.check
    problems = sync_regions(write) + sync_copies(write)
    literal_problems = scan_literals()
    if write:
        for p in problems:
            print(f"updated: {p}")
        for p in literal_problems:
            print(p)
        print(f"{len(problems)} target(s) updated, {len(literal_problems)} literal problem(s)")
        return 1 if literal_problems else 0
    for p in problems + literal_problems:
        print(p)
    print(f"{len(problems) + len(literal_problems)} problem(s)")
    return 1 if problems or literal_problems else 0


if __name__ == "__main__":
    sys.exit(main())
