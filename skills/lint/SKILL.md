---
name: lint
description: Runs flake8 and mypy in the workspace Python environment (uv or conda), reports the issues, and fixes them. Use this skill only when the user invokes /lint or asks to lint the workspace.
disable-model-invocation: true
---

# Lint

Run the checks in the workspace environment.

## Environment

Find the environment manager. Use the order in the virtual-env rule:

1. `uv.lock`, or `pyproject.toml` with `.venv`: uv.
2. `environment.yml`, or a conda environment that the user named: conda.
3. Neither: uv.

When you cannot tell, ask the user.

## Checks

uv:

- When `pyproject.toml` exists, run `uv sync`.
- Run `uv run --with flake8 flake8 . --extend-exclude .venv`. Report each style violation.
- Run `uv run --with mypy mypy . --exclude '\.venv'`. Report each type error.

conda:

- When flake8 or mypy is absent, run `conda install -n <env> flake8 mypy`.
- Run `conda run -n <env> flake8 . --extend-exclude .venv`. Report each style violation.
- Run `conda run -n <env> mypy . --exclude '\.venv'`. Report each type error.

## Fixes

Fix every reported issue. Run both commands again.

Repeat the fixes and both commands until both commands pass with no issues.
