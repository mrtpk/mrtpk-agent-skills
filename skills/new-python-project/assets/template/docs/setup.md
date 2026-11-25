# Setup

This document tells you how to install the tools, set up a clone of this project,
work on it (with uv on the host or with Docker Compose), and set up GitHub Actions.

Contents:

1. [Prerequisites](#1-prerequisites)
2. [First-time setup of a clone](#2-first-time-setup-of-a-clone)
3. [Work on the host with uv](#3-work-on-the-host-with-uv)
4. [Work in Docker Compose](#4-work-in-docker-compose)
5. [Configuration](#5-configuration)
6. [Add code, data and tests](#6-add-code-data-and-tests)
7. [Manage dependencies](#7-manage-dependencies)
8. [Release a version](#8-release-a-version)
9. [Set up GitHub Actions](#9-set-up-github-actions)
10. [Change the uv or Python version](#10-change-the-uv-or-python-version)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Prerequisites

| Tool | Version | Use |
|---|---|---|
| Git | any recent | version control, pre-commit hooks |
| uv | 0.13 or later | Python, environments, dependencies, builds |
| Docker Engine or Docker Desktop | any recent | container image |
| Docker Compose | v2.24 or later | local development in a container |

You do not need to install Python. uv installs the Python version in `.python-version`.

### 1.1 Install uv

Linux, macOS and WSL:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Open a new terminal. Then check the installation:

```bash
uv --version            # must show 0.13 or later
```

To update uv later, run `uv self update`.

### 1.2 Install Docker

- Linux: install Docker Engine and the Compose plugin from the Docker documentation for your
  distribution. Add your user to the `docker` group, then log out and log in again:
  `sudo usermod -aG docker "$USER"`.
- Windows and macOS: install Docker Desktop. On Windows, enable the WSL 2 back end.

Check the installation:

```bash
docker --version
docker compose version  # must show v2.24 or later
docker run --rm hello-world
```

BuildKit and buildx are not necessary. The `Dockerfile` also builds with the legacy builder.

### 1.3 WSL users

- Keep the project in the Linux file system (for example `~/code/acme-tool`), not in
  `/mnt/c/...`. On `/mnt/c`, file operations are much slower, and uv cannot use hard links.
- If the project must stay on `/mnt/c`, set this variable to stop the uv hard-link warnings:

  ```bash
  echo 'export UV_LINK_MODE=copy' >> ~/.bashrc
  ```

---

## 2. First-time setup of a clone

```bash
git clone <repository URL>
cd my-project
uv sync                    # creates .venv, installs the project and the dev tools
uv run pytest              # all tests must pass
uv run pre-commit install  # installs the git hook
```

For the container workflow, continue with [section 4](#4-work-in-docker-compose).

---

## 3. Work on the host with uv

uv creates the environment in `.venv`. Do not activate it. Put `uv run` in front of each command.

| Task | Command |
|---|---|
| Install or update the environment | `uv sync` |
| Run the CLI | `uv run my-project greet Ada` |
| Run the package as a module | `uv run python -m my_project --help` |
| Run all tests | `uv run pytest` |
| Run unit tests only | `uv run pytest -m "not integration"` |
| Run one test file | `uv run pytest tests/unit/test_cli.py` |
| Tests with coverage | `uv run pytest --cov` |
| Format the code | `uv run ruff format .` |
| Lint the code (and fix) | `uv run ruff check . --fix` |
| Type check | `uv run mypy` |
| Run all pre-commit hooks | `uv run pre-commit run --all-files` |
| Build wheel and sdist | `uv build` (output in `dist/`) |
| Open a Python shell | `uv run python` |

The pre-commit hook runs on each `git commit`. It runs these checks: whitespace, YAML/TOML
syntax, `uv lock --check`, `ruff format`, `ruff check` and `mypy`. If a hook changes a file,
add the file again and commit again.

### Editor setup

Set the Python interpreter of your editor to `.venv/bin/python`
(Windows: `.venv\Scripts\python.exe`). Install the Ruff and Mypy extensions. They read
their settings from `pyproject.toml`.

---

## 4. Work in Docker Compose

Use this workflow when you do not want Python tools on the host, or when you must match
the container environment.

The `app` service uses the `dev` stage of the `Dockerfile`:

- The dev tools (pytest, ruff, mypy) are installed.
- The repository is mounted at `/app`. Code changes apply immediately, without a rebuild.
- The container runs as your host user. The files that it creates belong to you.

### 4.1 First setup

```bash
cp .env.example .env
id -u; id -g               # if the values are not 1000, write them to UID and GID in .env
docker compose build
```

### 4.2 Daily commands

| Task | Command |
|---|---|
| Run the CLI | `docker compose run --rm app my-project greet Ada` |
| Run the tests | `docker compose run --rm app pytest` |
| Lint | `docker compose run --rm app ruff check .` |
| Format | `docker compose run --rm app ruff format .` |
| Type check | `docker compose run --rm app mypy` |
| Open a shell | `docker compose run --rm app bash` |

Output files go to `./output` on the host.

### 4.3 When to rebuild

Run `docker compose build` again after a change to `pyproject.toml` or `uv.lock`.
The container does not change its environment at run time (`UV_NO_SYNC=1`).

### 4.4 Test the production image

The `prod` service uses the `runtime` stage. This is the same image that CI builds.

```bash
mkdir -p output            # do this first; otherwise Docker creates it as root on Linux
docker compose --profile prod build
docker compose --profile prod run --rm prod greet Ada
```

### 4.5 Clean up

```bash
docker compose --profile prod down --rmi all   # removes the my-project:dev and :latest images
```

---

## 5. Configuration

The application reads its settings in this sequence. A later source overrides an earlier source:

1. `src/my_project/resources/default_config.json` (ships in the package)
2. Environment variables with the prefix `MY_PROJECT_`

| Variable | Default | Meaning |
|---|---|---|
| `MY_PROJECT_OUTPUT_DIR` | `output` | Directory for files the application writes |
| `MY_PROJECT_LOG_LEVEL` | `INFO` | Log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `MY_PROJECT_GREETING` | `Hello` | Example setting |

On the host, set a variable for one command:

```bash
MY_PROJECT_LOG_LEVEL=DEBUG uv run my-project greet Ada
```

In Docker Compose, write the variables in `.env`. Git and Docker ignore `.env`.
Do not put secrets in `.env.example` or in `default_config.json`.

To add a setting:

1. Add the key and the default value to `default_config.json`.
2. Add a field to the `Settings` class in `config.py`, and read it in `Settings.load`.
3. Add a test in `tests/unit/test_config.py`.
4. Add the variable to the table in `README.md` and to `.env.example`.

---

## 6. Add code, data and tests

Read [structure.md](structure.md) for the full rules. The most important rules are:

- Put new code in a sub-package of `src/my_project/`, for example `src/my_project/reports/`.
  Never add a second top-level package.
- Put each test in the mirror path: `src/my_project/reports/build.py` →
  `tests/unit/reports/test_build.py`. Add an `__init__.py` to each new test folder.
- Put data files that the code needs in `src/my_project/resources/`. Read them with
  `my_project.config.read_resource_text("<file name>")`. Never use `__file__` to find them.
- Read environment variables only in `config.py`.

### Example: add a CLI command

1. Write the logic as a function in `src/my_project/core/` (or a new sub-package).
2. In `cli.py`, add a sub-parser in `build_parser()` and a branch in `main()`.
3. Add a unit test in `tests/unit/test_cli.py` and a test for the logic.
4. Run `uv run pytest` and `uv run pre-commit run --all-files`.

---

## 7. Manage dependencies

Change dependencies only with uv. uv updates `pyproject.toml` and `uv.lock` together.
Commit both files.

| Task | Command |
|---|---|
| Add a runtime dependency | `uv add requests` |
| Add with a version range | `uv add "requests>=2.32,<3"` |
| Add an optional feature (extra) | `uv add --optional plots matplotlib` |
| Add a dev tool | `uv add --dev pytest-xdist` |
| Remove a dependency | `uv remove requests` |
| Upgrade one package | `uv lock --upgrade-package requests && uv sync` |
| Upgrade all packages | `uv lock --upgrade && uv sync` |
| Show the dependency tree | `uv tree` |

Do not add `requirements.txt`. To give a file to a tool that needs one, generate it:
`uv export --no-dev --format requirements-txt > requirements.txt` (do not commit it).

After a dependency change, rebuild the Compose image: `docker compose build`.

---

## 8. Release a version

The version is only in `pyproject.toml`. The package reads it at run time.

```bash
uv version --bump patch     # or: minor, major. Updates pyproject.toml and uv.lock.
uv run my-project --version # check
git commit -am "Release 0.1.1"
git tag v0.1.1
git push && git push --tags
```

For the tag, CI builds the wheel and pushes the image `:<commit sha>` and `:v0.1.1`
to the GitHub container registry (GHCR).

---

## 9. Set up GitHub Actions

`.github/workflows/ci.yml` has four jobs:

| Job | Needs | What it does |
|---|---|---|
| `lint` | | `uv lock --check`, `ruff format --check`, `ruff check`, `mypy` |
| `test` | `lint` | `pytest` with coverage; keeps `report.xml` and `coverage.xml` as the `test-reports` artifact |
| `wheel` | `test` | builds the wheel, installs it outside the checkout, runs the tests against it |
| `docker` | `test` | builds the image and runs it; pushes it from the default branch and from tags |

The workflow runs for pushes to `main`, for tags `v*`, and for pull requests. A new push to a
pull request cancels the older run. When your default branch is not `main`, change `branches:`.

### 9.1 Runner requirements

- GitHub-hosted `ubuntu-latest` runners. They have Docker. No other setup is necessary.
- Self-hosted runners need Docker and access to `ghcr.io` and `docker.io`.

### 9.2 Repository settings

- No secrets are necessary. The `docker` job pushes with the built-in `GITHUB_TOKEN`. Only that job
  has `packages: write`; the other jobs have `contents: read`.
- When the push fails with "permission denied": **Settings → Actions → General → Workflow permissions**
  must allow the workflow to write packages, or the package must give this repository write access.
- Recommended: a branch rule on `main` that requires the `lint`, `test`, `wheel` and `docker` checks.

### 9.3 Image tags

The image name is `ghcr.io/<owner>/<repo>` in lower case.

| Run | Tags pushed |
|---|---|
| Pull request or other branch | none (build and run only) |
| Default branch | `:<short sha>`, `:latest` |
| Git tag | `:<short sha>`, `:<tag>` |

Pull an image (a private package needs `docker login ghcr.io` first):

```bash
docker run --rm ghcr.io/<owner>/<repo>:latest greet Ada
```

---

## 10. Change the uv or Python version

### uv

The uv version is in three files (four lines). Keep them equal:

| File | Location |
|---|---|
| `pyproject.toml` | `[build-system] requires = ["uv_build>=X.Y.Z,<X.(Y+1)"]` |
| `.github/workflows/ci.yml` | `env: UV_VERSION: "X.Y.Z"` |
| `Dockerfile` | the two `FROM ghcr.io/astral-sh/uv:...` lines |

Check that the image tag exists before you push:
`docker manifest inspect ghcr.io/astral-sh/uv:X.Y.Z-python3.12-trixie-slim`.

### Python

To change from 3.12 to, for example, 3.13, change all of these:

- `.python-version`
- `pyproject.toml`: `requires-python`, the classifier, `[tool.ruff] target-version`,
  `[tool.mypy] python_version`
- `Dockerfile`: the `python3.12` part of the uv image tags, and
  `python:3.12-slim-trixie` in the `runtime` stage

Then run `uv sync`, `uv run pytest` and `docker compose build`.

---

## 11. Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `warning: Failed to hardlink files; falling back to full copy` | The project and the uv cache are on different file systems (common on WSL `/mnt/c`). | `export UV_LINK_MODE=copy`, or move the project to the Linux file system. |
| `ModuleNotFoundError: No module named 'my_project'` | The environment is not synced, or you ran `python` and not `uv run python`. | `uv sync`, then use `uv run`. |
| `uv lock --check` fails in pre-commit or CI | `pyproject.toml` changed, but `uv.lock` did not. | `uv lock`, then commit `uv.lock`. |
| `the --mount option requires BuildKit` | A `RUN --mount` line was added to the `Dockerfile`. | Remove the `--mount` options. The `Dockerfile` must build without BuildKit. |
| `Permission denied` on `./output` in the `prod` container | Docker created `./output` as root. | `sudo rm -rf output && mkdir output`. |
| Files in the repository belong to root after a Compose run | `UID`/`GID` in `.env` do not match your user. | Set them to `id -u` and `id -g`; `sudo chown -R "$USER": .`. |
| A new dependency is missing in the Compose container | The image was built before the change. | `docker compose build`. |
| `docker compose` does not accept `env_file` with `required` | Compose is older than v2.24. | Update Docker Compose. |
| The CI `docker` job fails with `Cannot connect to the Docker daemon` | The runner is not privileged, or the `dind` service did not start. | Set `privileged = true` for the runner (section 9.1). |
| mypy reports `Duplicate module named ...` | A test folder has no `__init__.py`. | Add an empty `__init__.py` to the folder. |
| pytest reports `'xyz' not found in markers` | A marker is not registered (`--strict-markers`). | Add it to `markers` in `[tool.pytest.ini_options]`. |
