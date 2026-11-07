---
description: Run flake8 and mypy after every commit in a Python repository
alwaysApply: true
---

# Lint and type check after commit

Apply this rule only when the repository has Python files.

After each commit, run flake8 and mypy in the workspace environment (see the virtual-env rule).

uv:

- `uv run --with flake8 flake8 . --extend-exclude .venv`
- `uv run --with mypy mypy . --exclude '\.venv'`

conda:

- `conda run -n <env> flake8 . --extend-exclude .venv`
- `conda run -n <env> mypy . --exclude '\.venv'`
- When flake8 or mypy is absent, install it with `conda install -n <env> flake8 mypy`.

When a command reports issues, fix the issues. Then make a new commit with the fixes. Do not amend a commit that is pushed.
