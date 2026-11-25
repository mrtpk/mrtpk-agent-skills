---
name: new-python-project
description: Create a new Python project from the bundled template (uv, src layout, ruff, strict mypy, pytest, pre-commit, Docker, Docker Compose, GitHub Actions). Use this when the user asks to create, start, scaffold, bootstrap or set up a new Python project, package, CLI, library or service, even when they give only a name. Do not use it to change the layout of an existing project, to add a module or command to an existing project, to write a single standalone script, or for a project in another language.
---

# Create a new Python project

This skill makes a new project from the template in `assets/template/`.
A script does the fixed steps. You make the decisions and edit the metadata.

Never scaffold a project from memory. A project from memory has a flat layout,
`requirements.txt`, no lock file, no Docker and no CI. Then the user must fix
it by hand. Always use the script.

## Step 1: Collect the inputs

Get these values. Ask only for the values that the user did not give.

| Input | Rule | Default |
|---|---|---|
| Name | Lowercase letters and digits, separated by `-` or `_`. Not `my-project`. | none: ask |
| Destination | A new or empty directory, not inside a git repository. | `./<name>` |
| Description | One sentence for `pyproject.toml` and `README.md`. | none: ask |
| Authors | Name and e-mail address. | `git config user.name` and `user.email` |

Show the user the names that the script derives from the name. For `acme-tool`:

| Use | Value |
|---|---|
| Distribution, CLI command, image name | `acme-tool` |
| Import package, folder | `acme_tool`, `src/acme_tool` |
| Environment variable prefix | `ACME_TOOL_` |

On WSL, a destination on `/mnt/c/...` works, but it is slow.
Tell the user, and recommend a path on the Linux file system, such as `~/code/<name>`.

When `git config user.name` or `user.email` is empty, ask for the authors.
Do not keep the placeholders `Your Name` and `you@example.com`.

## Step 2: Run the script

Call the script with `bash` and its absolute path. Do not depend on the execute bit or on the current directory.

```bash
bash <this skill directory>/scripts/new_project.sh <name> <destination> \
  --description "<one sentence>" --author "<Name> <<email>>"
```

Always pass `--description` and `--author` when you have the values.

The script does these steps, in this sequence, and stops at the first failure:

1. Checks the name, the destination, the options, `uv` and `git`.
2. Copies the template and runs `git init -b main`.
3. Renames the placeholders, runs `uv lock` and deletes the rename script.
4. Writes the description and the author into `pyproject.toml` and `README.md`.
5. Runs `uv sync`, `pytest`, `ruff format --check`, `ruff check` and `mypy`.
6. Installs pre-commit and runs all hooks.

It does not commit.

When the script fails, it prints the failed step and the directory to delete.
Report the step and the error to the user. Do not repair the project by hand.
Do not create the missing files yourself.
The usual causes are no network access for `uv`, and an old `uv` version (the template needs 0.13 or later).

## Step 3: Set the metadata (only when you did not pass it)

The script prints a "Not set" line for each value that it did not get. Only then, in the new project:

1. In `pyproject.toml`, replace `description` or `authors`.
2. In `README.md`, replace the line under the title with the description.
3. Run `uv run pytest -q` and `uv run pre-commit run --all-files`.

## Step 4: Optional tasks, only when the user asks

- **Remove the example.** Delete `src/<pkg>/core/greeting.py` and `tests/unit/core/test_greeting.py`.
  Remove the `greet` command from `cli.py`, its tests in `tests/unit/test_cli.py`, and
  `tests/integration/test_installed_package.py`. Keep `--version` working.
  Then run the tests, `ruff` and `mypy` again.
- **Check the container.** Run `docker compose build` and `docker compose run --rm app pytest`.
  BuildKit is not necessary.
- **First commit.** Run `git add -A` and `git commit -m "Initial project from template"`.
  Commit only when the user agrees.
- **Remote.** Add the remote and push only when the user gives the URL and asks for the push.

## Step 5: Report

Tell the user:

- the path of the project and the derived names,
- the checks that passed, and the checks that you did not run (for example Docker),
- whether you made a commit,
- the next commands: `cd <path>`, `uv run <name> --help`, and `docs/setup.md` for the full workflow.

## Rules for the generated project

The project's `docs/structure.md` has the full rules. Do not break these rules when you change the project:

- Keep one top-level import package under `src/`. Do not add `src/__init__.py`.
- Keep all configuration in `pyproject.toml`. Do not add `requirements.txt`, `setup.py`, `setup.cfg`, `mypy.ini` or `VERSION`.
- Change dependencies with `uv add` and `uv remove` only.
- Load package data with `importlib.resources`. Do not build paths from `__file__`.
- Do not add `RUN --mount` to the `Dockerfile`. Some hosts have no buildx, and then the build fails.
- Before `docker compose --profile prod run`, run `mkdir -p output`. Otherwise Docker creates `output` as root on Linux.

## Maintain the template

`assets/TEMPLATE.md` records the template source and the differences from that source.
To change the template, edit `assets/template/`. Then run the script into a temporary directory, and check that all steps pass.

## Communication style

Apply these rules to all text that this skill produces (replies and the files that you write in the new project). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- Text that this skill makes for other readers (pages, documents, reports, figures) follows the tone rules of this skill, for example neutral words for gaps.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.
