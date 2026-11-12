---
name: lint
description: Runs flake8 and mypy in the workspace Python environment (uv or conda), reports the issues, and fixes them. Starts only with the /lint command.
disable-model-invocation: true
---

# Lint

Run the checks in the workspace environment.

## Environment

Find the environment manager. Check in this order:

1. `uv.lock`, or `pyproject.toml` with `.venv`: uv.
2. `environment.yml`, or a conda environment that the user named: conda.
3. Neither: uv.

When you cannot tell, ask the user.

## Scope

- Check only the project's own code. Use the flake8 and mypy configuration of the project (`setup.cfg`, `tox.ini`, `.flake8`, `pyproject.toml`, `mypy.ini`) when it exists.
- Exclude vendored, generated and third-party code (for example `.venv`, `vendor/`, `third_party/`, `build/`, generated protobuf files).
  - flake8: add the folders with `--extend-exclude` (it adds to the project setting).
  - mypy: a command-line `--exclude` replaces the `exclude` setting of the project config. When the config has an `exclude` setting, do not pass `--exclude`; add the folders to the config only when the user agrees. When the config has no `exclude` setting, pass one `--exclude` regex for all folders, for example `--exclude '(\.venv|vendor|third_party|build)/'`.
- When the user names files or folders, check only those.

## Checks

uv:

- When `pyproject.toml` exists, run `uv sync`.
- Run `uv run --with flake8 flake8 . --extend-exclude .venv`. Report each style violation.
- Run `uv run --with mypy mypy .`, with `--exclude` only as the Scope section says. Report each type error.

conda:

- When flake8 or mypy is absent, run `conda install -n <env> flake8 mypy`.
- Run `conda run -n <env> flake8 . --extend-exclude .venv`. Report each style violation.
- Run `conda run -n <env> mypy .`, with `--exclude` only as the Scope section says. Report each type error.

## Communication style

Apply these rules to all text that this skill produces (the issue report and the final reply). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- In reviews: be honest and brutal. State the verdict and the defects first.
- Text that this skill makes for other readers (pages, documents, reports, figures) follows the tone rules of this skill, for example neutral words for gaps.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## Fixes

Fix every reported issue in the project's own code. Run both commands again.

- Stop after 3 rounds of fixes. Report the issues that remain.
- When the first run reports more than 50 issues, or a fix needs a change of behavior, a new dependency or a change of the lint configuration, report the issues and ask the user before you fix them.
- Do not hide issues with `# noqa` or `# type: ignore` unless the user agrees. Say which ones you added.
