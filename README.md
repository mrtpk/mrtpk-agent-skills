# mrtpk-agent-skills

A collection of agent skills.

Agent instructions are in [AGENTS.md](AGENTS.md).

## Skills

- [`skills/codebase-explainer`](skills/codebase-explainer/SKILL.md) — plan and build a static HTML study
  site that teaches a codebase, with cited claims, diagrams, guided tours and a fact-check pass.
  Requires: `svg-figures`.
- [`skills/code-to-kaizen-blog`](skills/code-to-kaizen-blog/SKILL.md) — read a codebase, keep an internal knowledge
  base with file:line citations, and write a technical blog series with check scripts, svglib figures and a fact-check pass.
  Requires: `svg-figures`, `code-to-md-writeup`.
- [`skills/code-to-md-writeup`](skills/code-to-md-writeup/SKILL.md) — read a codebase, keep an internal knowledge base
  with file:line citations, and write a Markdown technical write-up (internal or public) with check scripts, figures and a
  fact-check pass. Requires: `svg-figures`.
- [`skills/evaluate-skills`](skills/evaluate-skills/SKILL.md) — decide with evidence whether skills are worth their
  context: review, tool tests, trigger evals and behaviour evals with and without the skill, then a score and a verdict.
- [`skills/explore`](skills/explore/SKILL.md) — work as a partner on an unclear idea, and stop at a rough skeleton.
- [`skills/design-plan-presentation`](skills/design-plan-presentation/SKILL.md) — build a click-to-reveal HTML
  presentation from a design document or plan, and serve it locally. Starts from `templates/presentation.html`. Uses
  the style of `svg-figures` when it is installed.
- [`skills/extract-skills`](skills/extract-skills/SKILL.md) — find reusable knowledge in a conversation, and turn it into
  skills, memories, docs or scripts.
- [`skills/new-python-project`](skills/new-python-project/SKILL.md) — create a new Python project from the bundled
  template: uv, src layout, ruff, strict mypy, pytest, pre-commit, Docker, Docker Compose and GitHub Actions.
- [`skills/report-to-page`](skills/report-to-page/SKILL.md) — turn a Markdown study report into one HTML page, and publish
  it as an Artifact when the Artifact tool is present. Without it, it writes a standalone HTML file.
- [`skills/svg-figures`](skills/svg-figures/SKILL.md) — draw technical figures as one Python script per figure, build SVG
  and PNG, and check each PNG.
- [`skills/unattended-run`](skills/unattended-run/SKILL.md) — run a long series of experiments while the user is away,
  with logs, findings and short status replies.

## Work skills

Skills for work-analysis tasks, in `skills/work/`. They need MCP servers for YouTrack and Outline. Set the base URLs
of your instances (`<YOUTRACK_URL>`, `<OUTLINE_URL>`) as each `reference.md` says.

- [`skills/work/youtrack-user-issue-report`](skills/work/youtrack-user-issue-report/SKILL.md) — list every YouTrack
  issue assigned to a person, with the real workflow state, as a Markdown report.
- [`skills/work/outline-wiki-author-report`](skills/work/outline-wiki-author-report/SKILL.md) — list every Outline
  wiki page that a person created, as a grouped Markdown report with dated links.
- [`skills/work/contributor-work-profile`](skills/work/contributor-work-profile/SKILL.md) — write a work summary of a
  person from their issues and wiki pages, with an optional impact evaluation and growth plan.
  Requires: `youtrack-user-issue-report`, `outline-wiki-author-report`.

## Usage

Copy one skill folder into the agent skills directory. Also copy each skill that it requires (see "Requires" above).
The skills find each other as sibling folders.

Use `.cursor/skills/` or `.claude/skills/` in the project. Use the global skills directory for every project.

Or ask the agent to look at this repo and then install the skills.

The agent invokes the skill by the `name` in `SKILL.md`.
`explore` starts only with its slash command (`/explore`). The agent does not start it by itself.

`svg-figures`, `report-to-page`, `code-to-md-writeup`, `codebase-explainer` and `code-to-kaizen-blog` run Python scripts
with [uv](https://docs.astral.sh/uv/). Install uv first. `new-python-project` needs uv 0.13 or later and git.

`svg-figures` is the only owner of the figure toolkit (`svglib.py`, `figkit.py`, `build_figures.py`). Other skills
copy it into their projects. Change the toolkit only in `svg-figures`.

`AGENTS.md` is the single source of the communication rules. Each skill has a copy in its "Communication style"
section, because a skill folder is copied alone. Skills that do no reviews leave out the "In reviews" line. After a
change to `AGENTS.md`, update each copy, then run `python3 tools/check_style.py`. It reports each missing or extra
rule, also in the nested `skills/work/*` skills.

Most skills have an `evals/` folder (not `code-to-kaizen-blog` and not the `work/*` skills). `trigger_evals.json`
lists requests that must start the skill and requests that must not. `explore` has none, because only its slash
command starts it. `evals/<case>/` (`case.yaml`, `prompt.md`, `graders/`) is one behaviour case for
`claude plugin eval`. The `evaluate-skills` skill explains both, and its `scripts/trigger_eval.py` runs the trigger evals.

## Rules

These files apply on every turn. They are not skills.

- [`rules/plan-review.md`](rules/plan-review.md) — review each new plan with the model in `plan-review-model.txt`.
- [`rules/lint-after-commit.md`](rules/lint-after-commit.md) — run flake8 and mypy after each commit in a Python repo.
- [`rules/virtual-env.md`](rules/virtual-env.md) — use the workspace environment (uv or conda; uv by default); use tmux for long-running commands.

Copy a rule into the agent rules directory. Cursor uses `.cursor/rules/`. Claude Code uses `.claude/rules/` in the project, or `~/.claude/rules/` for every project.

For Claude Code, copy `AGENTS.md` to `~/.claude/CLAUDE.md` (every project) or to `CLAUDE.md` in the project.

Or ask the agent to look at this repo and then install the rules.
