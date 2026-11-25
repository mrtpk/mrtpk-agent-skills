---
type: llm
weight: 1
---

The answer keeps the order trap: `check_version.py` must run after `make test`, because `make test` regenerates `_version.py`.
