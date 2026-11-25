#!/usr/bin/env bash
set -e
mkdir -p skills/careful-commits
cat > skills/careful-commits/SKILL.md <<'MD'
---
name: careful-commits
description: Write good commit messages. Use when the user asks you to commit.
---

# Careful commits

- Write a short subject line in the imperative mood.
- Explain why the change was made in the body.
- Keep each commit to one logical change.
- Run the tests before you commit.
MD
