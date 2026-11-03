---
name: lint
description: Runs flake8 and mypy in the workspace virtual environment, reports the issues, and fixes them. Use this skill only when the user invokes /lint or asks to lint the workspace.
disable-model-invocation: true
---

# Lint

Run the checks in the workspace virtual environment.

## Environment

Activate `.env`. Run `source .env/bin/activate`.

Create the environment when it is absent. Run `python -m venv .env`. Then activate `.env`.

## Checks

Run `flake8 .`. Report each style violation.

Run `mypy .`. Report each type error.

## Fixes

Fix every reported issue. Run `flake8 .` again. Run `mypy .` again.

Repeat the fixes and both commands until both commands pass with no issues.
