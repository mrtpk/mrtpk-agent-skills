# Project structure

## Layout

```
.
├── pyproject.toml          # the only place for metadata, dependencies and tool settings
├── uv.lock                 # exact dependency versions; commit it
├── .python-version         # Python version for uv
├── .github/workflows/ci.yml # lint -> test -> wheel test and docker image
├── .pre-commit-config.yaml # hooks call `uv run`, so they use the locked tool versions
├── .flake8                 # only for plain flake8 runs; mirrors [tool.ruff]
├── Dockerfile              # stages: builder, dev (compose), runtime (default, non-root)
├── compose.yaml            # local development in the dev stage; `prod` profile for the image
├── .env.example            # copy to .env: UID/GID and MY_PROJECT_* overrides
├── docs/                   # setup.md (setup and workflows), structure.md (these rules)
├── scripts/                # developer scripts, when needed; not in the installed package
├── src/
│   └── my_project/         # the ONE import package
│       ├── __init__.py     # __version__ from package metadata
│       ├── __main__.py     # python -m my_project
│       ├── py.typed        # tells type checkers the package has types
│       ├── cli.py          # entry point: parse args, configure logging, call core
│       ├── config.py       # settings: packaged defaults + environment variables
│       ├── logging_setup.py
│       ├── resources/      # data files that ship in the wheel
│       └── core/           # domain logic; no CLI, environment or global state
└── tests/
    ├── conftest.py         # shared fixtures
    ├── unit/               # mirrors src/my_project/
    └── integration/        # runs the package as a process (marker: integration)
```

## Rules

### Packaging
1. Use one top-level import package under `src/`. Put sub-tools in sub-packages
   (`my_project/<tool>/`). Never add a second top-level package.
2. Do not put `__init__.py` in `src/`. Never write `import src...`.
3. Keep metadata, dependencies and tool settings in `pyproject.toml` only. Do not add
   `requirements.txt`, `setup.py`, `setup.cfg`, `mypy.ini` or a `VERSION` file.
4. Set the version only in `pyproject.toml`. Read it with `importlib.metadata`.
5. Put runtime dependencies in `[project.dependencies]`. Put optional features in
   `[project.optional-dependencies]`. Put dev tools in `[dependency-groups]`.
   Change dependencies only with `uv add` and `uv remove`.

### Data and paths
6. Put data that the code needs in `src/my_project/resources/`. Read it with
   `importlib.resources`. Never build paths from `__file__` or `Path(...).parents[n]`.
7. Never write into the package directory. Write output to the directory in the settings
   (`MY_PROJECT_OUTPUT_DIR`).
8. Keep large data, generated results and datasets out of the repository. Load them from a
   path that the user configures.

### Code
9. Keep `cli.py` thin. Put logic in `core/` (or other sub-packages) as functions that take
   arguments and return values.
10. Read environment variables only in `config.py`. Pass settings down as arguments.
11. Configure logging only in the entry point. Modules call `logging.getLogger(__name__)`.
12. Do not keep two versions of the same module (`x.py` and `x_refactor.py`). Git keeps history.
13. Put a separate application (own Dockerfile, own dependencies) in its own repository.

### Tests
14. Put all tests in `tests/`. Never put tests in `src/`.
15. Mirror the package: `src/my_project/core/greeting.py` -> `tests/unit/core/test_greeting.py`.
16. Every test folder has `__init__.py`, so test files with the same name do not collide.
17. Never change `sys.path` or `PYTHONPATH` in tests. Tests import the installed package.
18. Mark slow or external tests with a marker. Register every marker in `pyproject.toml`.

### Tooling
19. Use uv for environments, dependencies, builds and tool runs. Do not use pip, venv or conda.
20. Ship the application as a Docker image built from `Dockerfile`. The image installs from
    `uv.lock` with `--no-dev --no-editable` and runs as a non-root user.
    Develop locally with `docker compose` (the `dev` stage) or with `uv` on the host.

### Quality gates
21. `ruff format`, `ruff check`, `mypy` (strict) and `pytest` must pass before a merge.
22. CI builds the wheel, installs it outside the checkout, and runs the tests against it.
23. CI builds the Docker image and runs it before a merge.
