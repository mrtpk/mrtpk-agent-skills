# Template record

`template/` is the template that `scripts/new_project.sh` copies. This copy is now the source.

- Copied from: `project-strcuture/python_project_structure`, on 2026-11-13.
- uv: 0.13.7 (pin in `pyproject.toml` `[build-system]`, `.github/workflows/ci.yml` (`UV_VERSION`) and `Dockerfile`).
- Python: 3.12.

## Differences from the copied source

1. `pyproject.toml`: `[tool.mypy] files = ["src", "tests"]`. The source also had `"scripts"`.
   The script deletes `scripts/rename_project.py`, so mypy would fail on a missing path.
2. `README.md`: the section "Use this template for a new project" is replaced by "Documentation".
3. `docs/setup.md`: section 2 "Create a new project from the template" is replaced by
   "First-time setup of a clone".
4. `docs/setup.md`: the `--mount` troubleshooting row no longer refers to "the template".
5. `docs/structure.md`: the `scripts/` line says "when needed".

## Placeholders

`scripts/rename_project.py` replaces these strings in all text files and renames `src/my_project`:
`my-project`, `my_project`, `MY_PROJECT`, `My Project`.
Use only these forms for names in the template. Another form will not be renamed.

## After a change

```bash
bash scripts/new_project.sh acme-tool "$(mktemp -d)/acme-tool"
```

All steps must pass. Then check that no placeholder remains in the new project.
