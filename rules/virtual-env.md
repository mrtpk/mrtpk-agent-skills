---
description: Always use the workspace conda environment inside tmux
alwaysApply: true
---

# Virtual Environment & tmux

Always run Python commands (and anything that needs the environment) inside
tmux, using the conda environment for this workspace.

## tmux

- Run commands in tmux, not in a plain shell.
- Send commands with `tmux send-keys "<command>" Enter` and read
  results with `tmux capture-pane -p`.
- If no tmux session is running, create one:
  `tmux new-session -d`.

## Conda environment

- Use the conda environment that is already active in the tmux window.
- The tmux window is in the workspace root.
  Re-activate that environment when the prompt does not show it.
- Do not create a `.env` virtual environment. The conda environment is the one to use.

## Docker

- Docker works directly: run `docker ps`, `docker run`, `docker exec`, etc.
  without any wrapper (the session has the `docker` group active).
- If `docker` ever fails with a socket permission error again, it means the
  session/server predates `docker` group membership. Fix it by fully killing
  the remote server (`pkill -f '.cursor-server'`) and reconnecting so a
  fresh login re-runs `initgroups()`; do not rely on `sg docker -c` wrappers.
