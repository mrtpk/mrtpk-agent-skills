# mrtpk-agent-skills

A collection of agent skills.

Agent instructions are in [AGENTS.md](AGENTS.md).

## Skills

- [`skills/codebase-explainer`](skills/codebase-explainer/SKILL.md) — plan and build a static HTML study
  site that teaches an open-source codebase, with cited claims, diagrams, guided tours and a fact-check pass.
  Requires: `svg-figures`.
- [`skills/code-to-kaizen-blog`](skills/code-to-kaizen-blog/SKILL.md) — read a codebase, keep an internal knowledge
  base with file:line citations, and write a technical blog series with check scripts, svglib figures and a fact-check pass.
  Requires: `svg-figures`, `code-to-md-writeup`.
- [`skills/code-to-md-writeup`](skills/code-to-md-writeup/SKILL.md) — read a codebase, keep an internal knowledge base
  with file:line citations, and write a Markdown technical write-up (internal or public) with check scripts, figures and a
  fact-check pass. Requires: `svg-figures`.
- [`skills/explore`](skills/explore/SKILL.md) — work as a partner on an unclear idea, and stop at a rough skeleton.
- [`skills/lint`](skills/lint/SKILL.md) — run flake8 and mypy in the workspace environment (uv or conda), then fix the reported issues.
- [`skills/design-plan-presentation`](skills/design-plan-presentation/SKILL.md) — build a click-to-reveal HTML
  presentation from a design document or plan, and serve it locally. Uses the style of `svg-figures` when it is installed.
- [`skills/extract-skills`](skills/extract-skills/SKILL.md) — find reusable knowledge in a conversation, and turn it into
  skills, memories, docs or scripts.
- [`skills/report-to-page`](skills/report-to-page/SKILL.md) — turn a Markdown study report into one HTML page, and publish
  it as an Artifact.
- [`skills/self-review`](skills/self-review/SKILL.md) — check your own work against evidence before you say that it is done.
- [`skills/svg-figures`](skills/svg-figures/SKILL.md) — draw technical figures as one Python script per figure, build SVG
  and PNG, and check each PNG.
- [`skills/unattended-run`](skills/unattended-run/SKILL.md) — run a long series of experiments while the user is away,
  with logs, findings and short status replies.

## Usage

Copy one skill folder into the agent skills directory. Also copy each skill that it requires (see "Requires" above).
The skills find each other as sibling folders. `svg-figures` is the only owner of the figure toolkit; other skills copy it into their projects.

Use `.cursor/skills/` or `.claude/skills/` in the project. Use the global skills directory for every project.

Or ask the agent to look at this repo and then install the skills.

The agent invokes the skill by the `name` in `SKILL.md`.

## Rules

These files apply on every turn. They are not skills.

- [`rules/plan-review.md`](rules/plan-review.md) — review each new plan with the model in `plan-review-model.txt`.
- [`rules/lint-after-commit.md`](rules/lint-after-commit.md) — run flake8 and mypy after each commit in a Python repo.
- [`rules/virtual-env.md`](rules/virtual-env.md) — use the workspace environment (uv or conda; uv by default); use tmux for long-running commands.

Copy a rule into the agent rules directory. Cursor uses `.cursor/rules/`. Claude Code uses `.claude/rules/` in the project, or `~/.claude/rules/` for every project.

For Claude Code, copy `AGENTS.md` to `~/.claude/CLAUDE.md` (every project) or to `CLAUDE.md` in the project.

Or ask the agent to look at this repo and then install the rules.
