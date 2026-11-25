# Figures

## Toolkit

The figure toolkit is in the `svg-figures` skill. Load that skill before you draw the first figure. It has the API, the style rules and the PNG checks.

Find the `svg-figures` skill. Look first in the folder that contains this skill (`../svg-figures/`). Other places are only examples: `.claude/skills/`, `~/.claude/skills/`, `.cursor/skills/`. When it is absent, stop and tell the user to install `svg-figures` beside this skill.

Copy `svg-figures/tools/` into the blog repo (for example `tools/diagrams/`) when the repo has no figure tools. The blog repo can then rebuild the figures without the skill. Copy `svg-figures/templates/figure.py` for each new figure.

Build the figures of one post:

```
PYTHONDONTWRITEBYTECODE=1 uv run --with cairosvg --with numpy --with pillow python <blog repo>/tools/diagrams/build_figures.py <post folder>
```

Add `--with <package>` for every package that a figure script imports (figures that compute data from the post's script need numpy, and often pillow). Install the Inter font and a mono font, so that the PNG matches the SVG.

When the blog repo has its own `build_figures.py`, use it. It can have other arguments (for example no `--lib`); read its usage first.

## Rules

The blog repo `STYLE.md` (section "Figures") wins over this list. The colours come from `svg-figures` (`brand-kit`).


- One Python script per figure. No Mermaid. No hand-written SVG.
- Canvas width 1100. No text smaller than 11. Mono 12-13 for numbers and identifiers.
- At most 3 panels, at most 3 boxes side by side. Split a bigger figure.
- Each panel title is a question. Its subtitle is the answer.
- Header: the title says what the figure explains. The subtitle starts with the series name: "<Series> · part 4 · <scope>".
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
