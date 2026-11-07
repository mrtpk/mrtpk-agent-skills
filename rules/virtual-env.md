---
description: Use the workspace Python environment (uv or conda), and tmux for long-running commands
alwaysApply: true
---

# Python environment and tmux

## Find the environment

Use the environment manager that the workspace already uses. Check in this order:

1. `uv.lock`, or `pyproject.toml` with a `.venv` folder: use **uv**.
2. `environment.yml`, or a conda environment that the user named: use **conda**.
3. Neither: use **uv**.

When you cannot tell, ask the user. Do not mix uv and conda in one workspace. Do not use `pip` or `python -m venv` directly.

## uv

- The project environment is `.venv` in the workspace root.
- When `pyproject.toml` exists, run `uv sync`.
- Run Python and Python tools with `uv run <command>`. Do not activate the environment.
- Add a dependency with `uv add <package>`. Add a development tool with `uv add --dev <package>`.
- Run a tool one time, without a project change, with `uv run --with <package> <command>` or `uvx <tool>`.
- When a Python version is missing, run `uv python install <version>`.

## conda

- Use the conda environment of the workspace. Run commands with `conda run -n <env> <command>`, or activate the environment in the tmux window.
- Install packages with `conda install -n <env> <package>`. Use `pip` inside the conda environment only for packages that conda does not have.
- When conda is not installed, do not install it. Use uv, or ask the user.

## tmux

- Run long-running commands (servers, training, watchers) in tmux, not in the plain shell.
- Send a command with `tmux send-keys -t <session> "<command>" Enter`. Read the result with `tmux capture-pane -p -t <session>`.
- When no tmux session exists, make one: `tmux new-session -d -s <name> -c <workspace root>`.
- Run short commands in the plain shell.
