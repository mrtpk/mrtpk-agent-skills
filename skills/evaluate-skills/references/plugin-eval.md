# `claude plugin eval`: format, flags and traps

Verified with Claude Code CLI 2.1.323 on 2026-11-13. "Unverified" marks what we did not test.
Run `claude --version` first. When it is newer, do one smoke run before you rely on the traps below.

## Run

```bash
claude plugin eval ./skills/<skill> --trust-plugin --no-publish \
  --runs 3 -j 4 --scaffold --allow-tools Edit Write \
  --judge-model sonnet --max-cost-usd 5 \
  --output-dir <scratch>/<skill> --report <scratch>/<skill>.html
```

- The target can be a bare skill folder. A `plugin.json` is not necessary.
- Default: two arms, with the skill and without it. The report shows the difference (Δ). `--ablation none` runs
  one arm only.
- Results go to `<skill>/evals/results/` unless `--output-dir` is set. Add `evals/results/` to `.gitignore`.
- `--case <glob>` runs only some cases. `--runs` overrides the case value.
- The run cost printed is the equivalent API price.

## Case layout

```
evals/<case>/
  case.yaml       schema_version "1.1", name, expected_outcome, context.scaffold_script (optional)
  setup.sh        fixture script; runs in the workspace only with --scaffold
  prompt.md       front matter + the user prompt (body)
  graders/*.md    one grader per file
```

`prompt.md` front-matter keys (all others are errors): `runs`, `model`, `max_turns`, `timeout_seconds`,
`allowed_tools`, `disallowed_tools`, `append_system_prompt`, `env`, `artifact_publish`, `growthbook_overrides`.
`env` accepts only `EVAL_*` keys. Unverified: `context.add_dirs`, `context.history_file`.

## Graders

| type | front matter | notes |
|---|---|---|
| `llm` | `weight`, optional `focus: trace` | the body is the criterion; 3 judge votes |
| `tool_used` | `tool`, `input_match` (regex on the input JSON), `min`, `max` | `min: 0` + `max: 0` = never used |
| `file_exists` | `path` (glob) | files that the agent made |
| `regex`, `tool_order`, `baseline` | see the CLI messages | unverified in this repo |

A `tool_used: Skill` grader is unscored in the two-arm mode. Use it as an indicator that the skill loaded:
`input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<name>"'`.

## Traps (each one cost runs)

- **It ignores `evals/trigger_evals.json`.** Use `scripts/trigger_eval.py` for level 3.
- **Bash cases are refused** when a credential folder of the machine has a symbolic link inside it, for example
  `~/.docker/contexts` made by Docker Desktop on WSL. `DOCKER_CONFIG` does not help. Without a fix, give the
  agent no Bash, and write graders that do not need a run.
- **Effort level:** set `CLAUDE_CODE_EFFORT_LEVEL=low` in the shell (not in `env`). Its effect is unverified.
- **The Haiku judge gives false FAILs.** Use `--judge-model sonnet`. Read the evidence of each failed grader
  before you blame the skill.
- **Fixtures:** make them with `setup.sh` and `--scaffold`. Do not put the answer in a file name or a comment.
- **Context:** a prompt that refers to earlier work needs that work in the prompt or in the fixture. Each run
  starts a new session.
- **Folders outside the workspace:** a skill that says "write to a temporary folder" can write to `/tmp`, and the
  sandbox denies it. The skill must name a folder inside the workspace.
- **Kept temp folders:** a failed run keeps `/tmp/claude-eval-*` with mode 000 parts. Run
  `chmod -R u+rwx <dir>` before you delete it.
- **Slash-command skills** (`disable-model-invocation: true`): a prompt that starts with `/<name>` loads them, but
  the arm without the skill gets an unknown command. Use `--ablation none` and report no Δ.
