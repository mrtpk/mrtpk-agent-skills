# mrtpk-agent-skills

A collection of agent skills.

Agent instructions are in [AGENTS.md](AGENTS.md).

## Skills

- [`skills/codebase-explainer`](skills/codebase-explainer/SKILL.md) — plan and build a static HTML study
  site that teaches an open-source codebase, with cited claims, diagrams, guided tours and a fact-check pass.
- [`skills/explore`](skills/explore/SKILL.md) — work as a partner on an unclear idea, and stop at a rough skeleton.
- [`skills/lint`](skills/lint/SKILL.md) — run flake8 and mypy in the workspace environment (uv or conda), then fix the reported issues.

## Usage

Copy one skill folder into the agent skills directory.

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
