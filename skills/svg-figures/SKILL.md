---
name: svg-figures
description: Draw static technical figures (architecture boxes and arrows, data flows, step sequences, comparison tables, annotated code cards) as one Python script per figure in one house style, then build an SVG and a 2x PNG and check each PNG for overlap and clipping. Use this skill when the user wants a figure file for a Markdown document, a design note, a write-up, a README or a report, asks to "draw a diagram as SVG/PNG", or asks for figures "in the house style". Do not use it for charts of data series (line, bar, scatter: use a plotting library), for diagrams inside an HTML explainer site (codebase-explainer copies `svglib.py` from this skill but has its own diagram style guide), for slides (design-plan-presentation), or for Mermaid diagrams.
---

# SVG figures

This skill draws figures with `tools/svglib.py`. Each figure is one Python script. A build step writes the SVG and a PNG at 2x scale. You then read each PNG and fix the defects.

## Files in this skill

| Path | Read it when |
|---|---|
| `references/style.md` | before you draw the first figure; it has all the style rules |
| `templates/figure.py` | copy it for each new figure |
| `tools/svglib.py` | the drawing library; read the API table below first, read the code only for details |
| `tools/figkit.py` | layout helpers: `row()`, `table()`, `code()` |
| `tools/build_figures.py` | builds all figures of one folder |

## Folder layout

```
<document folder>/
  diagrams/<name>.py        one script per figure (files that start with "_" are helpers; the build skips them)
  resources/<name>.svg      written by the build
  resources/<name>.png      written by the build (2x)
```

When one folder holds figures of many parts or sections, name the scripts `NN_figK_<name>.py` (part number, figure number, short name). This prevents name collisions.

When the target repo must rebuild the figures without this skill, copy `tools/` into the repo (for example `tools/diagrams/`) and pass `--lib` to that folder. Other skills do this: `code-to-kaizen-blog`, `code-to-md-writeup` and `codebase-explainer` depend on this skill and copy its tools. This skill is the only owner of the toolkit; do not keep edited copies in other skills.

**Existing copy (drift check).** When the target folder already has a copy, compare each copied file with
the file in this skill: `diff -q <copy> <skill>/tools/<file>`. When a file differs, do not overwrite it.
Tell the user which files differ, and ask: keep the copy, or replace it. A copy can have local edits.

## Build

```
PYTHONDONTWRITEBYTECODE=1 uv run --with cairosvg python <skill>/tools/build_figures.py <document folder> [--lib <folder with svglib.py and figkit.py>]
```

- Add `--with <package>` for each package that a figure script imports (for example numpy).
- `--lib` defaults to the folder of `build_figures.py`.
- Install the Inter font. The PNG renderer uses only installed fonts. For each font stack, the build uses the first installed font, or the generic `monospace` / `sans-serif` font (also when `fc-list` is absent). The SVG keeps the full stack. The build prints `WARN fonts` when no sans font of the stack is installed; text widths then differ from the layout estimates.
- When the repo has its own `build_figures.py`, use it. Read its usage first.
- A `WARN` line means that content passes the canvas edge. Fix it.

## Workflow

1. Decide the idea of the figure in one sentence. One figure explains one idea.
2. Copy `templates/figure.py` to `diagrams/<name>.py`. Fill the docstring: what the figure explains, and the source of each value (a script and its section, or a file:line).
3. Draw with the API below. Follow `references/style.md`.
4. Build.
5. Read each PNG with the Read tool. Do the checks below. Fix and build again until the PNG is clean.
6. Put the figure in the document: Markdown image with alt text that describes each panel, then a caption line `*Figure: ...*`.

## Check every PNG

- Text overlaps a box, an arrow or other text.
- Text is clipped at a box edge or at the canvas edge.
- Columns collapsed. The PNG renderer collapses runs of spaces. Use `figkit.code()` with `\t`, or draw separate text.
- An arrow crosses a box or a label.
- A colour is not in the legend, or one colour has two meanings.
- A value in the figure does not match its source.

## API (svglib.Diagram)

Colours are role tuples `(strong, tint, pale)`: `BLUE`, `AMBER`, `VIOLET`, `TEAL`, `EMERALD`, `PINK`, `NEUTRAL`. Plain hex is also accepted. Neutrals: `INK`, `MUTE`, `GRAY_MID`, `LINE`, `BORDER`, `PANEL_BG`, `WHITE`. `SERIES` is a list of 8 categorical colours.

| Method | Draws |
|---|---|
| `Diagram(width=1100)` | a new canvas |
| `header(title, subtitle, params=None, scope=None)` | title at y 42, subtitle 68, mono parameter line 88, scope 106 |
| `panel(y, h, num, title, sub)` | a numbered section card across the canvas; title is a question, sub is the answer |
| `box(x, y, w, h, title, lines, col, align="middle")` | tinted box, bold title, mono detail lines (15 px pitch) |
| `step_card(x, y, w, h, num, title, col, tag, rows)` | card with accent bar, badge, tag pill, key/value mono rows |
| `lane(x, y, w, h, col, name, details)` | dashed lane with a solid header band |
| `arrow(x1, y1, x2, y2, col, dash=None)` / `path_arrow(d, col)` | straight or path arrow with a marker |
| `arrow_label(x, y, s, col)` | label for an arrow |
| `pill(x, y, w, label, col)` / `pill_auto(x, y, label, col)` | small tag; `pill_auto` returns its width |
| `chip(x, y, w, label, col)` | result chip, mono bold |
| `badge(cx, cy, n, col)` | numbered circle |
| `callout(x, y, w, lead, body, col)` | dashed note with a bold lead-in |
| `legend(x, y, items)` | `items = [(col, label), ...]`; returns the x after the last label |
| `footnotes(x, y, lines)` | muted notes; returns the y after the last line |
| `aside(x, y, lines)` | italic muted aside |
| `text`, `rect`, `line`, `circle` | low level |
| `save(height)` | writes the SVG to `sys.argv[1]`; warns on stderr when content passes an edge |

`figkit`: `row(d, y, boxes, arrow_col)` draws up to 3 boxes `(title, [lines], col)` at x 60/410/760 (width 290) with arrows. `table(d, y, rows, cols, color_fn)` draws a header row and mono body rows; returns the y after the table. `code(d, x, y, w, lines, tabs=(0, 160, 260))` draws a code card; `\t` starts a new column; returns the height.

## Communication style

Apply these rules to all text that this skill produces (figure titles, panel questions, labels, footnotes, alt text and captions). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- Text that this skill makes for other readers (pages, documents, reports, figures) follows the tone rules of this skill, for example neutral words for gaps.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## Hard rules

- One Python script per figure. No hand-written SVG. No Mermaid.
- Every value in a figure comes from a named source in the script docstring. Do not type a measured value from memory.
- Read every PNG after every build.
