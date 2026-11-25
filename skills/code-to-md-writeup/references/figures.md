# Figures

The figures use the `svg-figures` skill. Load that skill before you draw the first figure. Follow its `references/style.md`.

## Find the toolkit

1. Find the `svg-figures` skill. Look first in the folder that contains this skill (`../svg-figures/`). Other places are only examples: `.claude/skills/`, `~/.claude/skills/`, `.cursor/skills/`. When it is absent, stop and tell the user to install `svg-figures` beside this skill.
2. Do not draw figures with another method.
3. Copy `svg-figures/tools/` to `<writeup>/tools/`. The team can then rebuild the figures without the skill.
   When `<writeup>/tools/` already exists, do the drift check in `svg-figures/SKILL.md` first.

## Rules for the write-up

- One script per figure in `<writeup>/diagrams/`, named `NN_figK_<name>.py` (part number, figure number, short name).
- Build: `PYTHONDONTWRITEBYTECODE=1 uv run --with cairosvg --with numpy python <writeup>/tools/build_figures.py <writeup>`. Add `--with` for each package that a figure script imports.
- Header subtitle: `<write-up title>  ·  part NN  ·  <scope>`.
- Real values from the part's check script. The figure script docstring names the script and the section.
- Public mode: the docstrings cite the check scripts, not the original source files. Figure text follows the publishing-safety rules.
- Read every PNG after every build.
