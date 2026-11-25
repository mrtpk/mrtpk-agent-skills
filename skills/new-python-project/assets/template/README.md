# My Project

Short description of my-project.

## Requirements

- [uv](https://docs.astral.sh/uv/) 0.13 or later. uv installs the correct Python version.
- Docker. The application ships as a container image.

## Quick start

```bash
uv sync                          # create .venv, install the project and the dev tools
uv run my-project greet Ada      # run the CLI
uv run python -m my_project --help
```

## Development commands

| Task | Command |
|---|---|
| Run tests | `uv run pytest` |
| Tests with coverage | `uv run pytest --cov` |
| Unit tests only | `uv run pytest -m "not integration"` |
| Format | `uv run ruff format .` |
| Lint | `uv run ruff check .` |
| Type check | `uv run mypy` |
| Install git hooks | `uv run pre-commit install` |
| Add a runtime dependency | `uv add <package>` |
| Add a dev tool | `uv add --dev <package>` |
| Build wheel and sdist | `uv build` |

## Local development with Docker Compose

`compose.yaml` runs the `dev` stage of the `Dockerfile`: dev tools installed, repository
mounted at `/app`, code changes apply without a rebuild, files created as your host user.

```bash
cp .env.example .env                       # once; set UID/GID if they are not 1000
docker compose build                       # again after a change to pyproject.toml or uv.lock
docker compose run --rm app my-project greet Ada
docker compose run --rm app pytest
docker compose run --rm app ruff check .
docker compose run --rm app mypy
docker compose run --rm app bash
mkdir -p output && docker compose --profile prod run --rm prod greet Ada   # production image
```

## Docker image

```bash
docker build -t my-project .
docker run --rm my-project greet Ada
docker run --rm -v "$PWD/output:/data/output" my-project greet Ada   # keep output files
```

The image installs the project as a wheel from `uv.lock` (no dev tools) and runs as a
non-root user. CI builds the image on every run and pushes it to the GitHub container registry (GHCR)
from the default branch (`:<sha>`, `:latest`) and from tags (`:<sha>`, `:<tag>`).

## Configuration

Defaults are in `src/my_project/resources/default_config.json`.
Environment variables with the prefix `MY_PROJECT_` override them:

| Variable | Default | Meaning |
|---|---|---|
| `MY_PROJECT_OUTPUT_DIR` | `output` | Directory for files the application writes |
| `MY_PROJECT_LOG_LEVEL` | `INFO` | Log level |
| `MY_PROJECT_GREETING` | `Hello` | Example setting |

## Documentation

- [docs/setup.md](docs/setup.md): install the tools, set up a clone, daily workflows, CI.
- [docs/structure.md](docs/structure.md): layout rules for code, data and tests.
