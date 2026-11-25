"""Rename the template placeholders to a new project name.

Usage (run one time, from the repository root):

    uv run python scripts/rename_project.py acme-tool

This replaces, in every text file:
    my-project -> acme-tool   (distribution and CLI name)
    my_project -> acme_tool   (import package name)
    MY_PROJECT -> ACME_TOOL   (environment variable prefix)
    My Project -> Acme Tool   (human-readable title)
It then renames `src/my_project` and runs `uv lock`.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
SELF = Path(__file__).resolve()

# Build the placeholders from parts, so that this file never matches its own search.
_WORDS = ("my", "project")
OLD_DIST = "-".join(_WORDS)
OLD_PKG = "_".join(_WORDS)
OLD_ENV = OLD_PKG.upper()
OLD_TITLE = " ".join(w.capitalize() for w in _WORDS)

SKIP_DIRS = {
    ".git",
    ".venv",
    ".uv-cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "dist",
}
SKIP_FILES = {"uv.lock"}
NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$")


def iter_text_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if not path.is_file() or path.name in SKIP_FILES or path.resolve() == SELF:
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # binary file
        result.append(path)
    return result


def rename(new_name: str, root: Path) -> list[Path]:
    words = re.split(r"[-_]", new_name)
    replacements = [
        (OLD_DIST, "-".join(words)),
        (OLD_PKG, "_".join(words)),
        (OLD_ENV, "_".join(words).upper()),
        (OLD_TITLE, " ".join(w.capitalize() for w in words)),
    ]
    changed: list[Path] = []
    for path in iter_text_files(root):
        text = path.read_text(encoding="utf-8")
        new_text = text
        for old, new in replacements:
            new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append(path)

    old_pkg_dir = root / "src" / OLD_PKG
    new_pkg_dir = root / "src" / "_".join(words)
    if old_pkg_dir.is_dir():
        if new_pkg_dir.exists():
            raise SystemExit(f"error: {new_pkg_dir} already exists")
        old_pkg_dir.rename(new_pkg_dir)
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("name", help="New project name, for example 'acme-tool'.")
    parser.add_argument("--no-lock", action="store_true", help="Do not run 'uv lock'.")
    args = parser.parse_args(argv)

    if not NAME_RE.match(args.name):
        parser.error("name must be lowercase letters and digits, separated by '-' or '_'")
    if not (ROOT / "src" / OLD_PKG).is_dir():
        parser.error(f"run from the repository root; src/{OLD_PKG} was not found")

    changed = rename(args.name, ROOT)
    print(f"Updated {len(changed)} files.")

    if not args.no_lock:
        if shutil.which("uv") is None:
            print("warning: uv not found; run 'uv lock' yourself", file=sys.stderr)
        else:
            subprocess.run(["uv", "lock"], cwd=ROOT, check=True)
    print("Done. Delete scripts/rename_project.py when you no longer need it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
