# Figures

## Toolkit

The skill has the figure toolkit in `tools/`. Copy it into the blog repo (for example `tools/diagrams/`) when the repo has no figure tools.

- `svglib.py`: the drawing library (`Diagram`, `header`, `panel`, `box`, `arrow`, `legend`, `footnotes`). It is the same library as in the `codebase-explainer` skill.
- `figkit.py`: `row()` (up to 3 boxes with arrows), `table()`, `code()` (`\t` columns).
- `build_figures.py`: runs each `<post>/diagrams/*.py`, writes the SVG and a 2x PNG to `<post>/resources/`.

Build the figures of one post:

```
uv run --with cairosvg python <tools>/build_figures.py <post folder> [--lib <folder with svglib.py and figkit.py>]
```

`--lib` defaults to the folder of `build_figures.py`. Install the Inter font, so that the PNG matches the SVG.

## Rules

- One Python script per figure. No Mermaid. No hand-written SVG.
- Canvas width 1100. No text smaller than 11. Mono 12-13 for numbers and identifiers.
- At most 3 panels, at most 3 boxes side by side. Split a bigger figure.
- Each panel title is a question. Its subtitle is the answer.
- Header subtitle starts with the series name and the part: "<Series> · part 4 · <scope>".
- One colour has one meaning. 3-5 accents. All colours are in the legend. Gray for the rest.
- Arrows do not cross boxes or labels. Dashed arrows for secondary paths.
- Real values from the part's script. The figure script docstring names the script and the section.
- A footnote says what the figure simplifies.
- In the post: alt text describes each panel; the next line is "*Figure: ...*".

## Check every PNG

Read each PNG with the Read tool after each build. Look for:

- text that overlaps a box, an arrow or other text
- text that is clipped at a box edge or at the canvas edge
- columns that collapsed (the PNG renderer collapses runs of spaces; use `figkit.code()` with `\t`, or draw separate text)
- arrows that cross a box or a label

Add as many figures as the ideas need. 4-6 figures per part is a good range.
