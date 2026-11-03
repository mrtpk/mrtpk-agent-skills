---
description: Run flake8 and mypy after every commit to keep code clean
alwaysApply: true
---

# Lint & Type Check After Commit

After making a commit, always run `flake8` and `mypy` to ensure clean code.

- Run both inside the workspace virtual environment (see the virtual-env rule).
- Commands: `flake8 .` and `mypy .`
- If either reports issues, fix them and amend/add a follow-up commit before
  continuing.
