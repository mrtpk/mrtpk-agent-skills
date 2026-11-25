#!/usr/bin/env bash
# Create a new Python project from the bundled template.
#
# Usage: bash new_project.sh <name> <dest> [--description TEXT] [--author "Name <email>"]
#   <name>         lowercase letters and digits, separated by '-' or '_' (example: acme-tool)
#   <dest>         directory to create; it must not exist, or it must be empty
#   --description  one sentence for pyproject.toml and the README (optional)
#   --author       the author for pyproject.toml, as "Name <email>" (optional)
#
# Steps: copy template, git init, rename placeholders, metadata, uv sync, tests, lint, mypy, pre-commit.
# It does not commit. On failure, it prints the failed step and the directory to delete.
set -euo pipefail

STEP="argument check"
DEST_CREATED=""

fail() {
    echo "ERROR: step '$STEP' failed." >&2
    if [[ -n "$DEST_CREATED" ]]; then
        echo "Delete '$DEST_CREATED' before you run this script again." >&2
    fi
}
trap fail ERR

die() {
    echo "ERROR: $*" >&2
    trap - ERR
    exit 2
}

USAGE='usage: bash new_project.sh <name> <dest> [--description TEXT] [--author "Name <email>"]'
DESCRIPTION=""
AUTHOR=""
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --description)
            [[ $# -ge 2 && -n "$2" ]] || die "--description needs a value"
            [[ -z "$DESCRIPTION" ]] || die "--description is given two times"
            DESCRIPTION="$2"
            shift 2
            ;;
        --author)
            [[ $# -ge 2 && -n "$2" ]] || die "--author needs a value"
            [[ -z "$AUTHOR" ]] || die "--author is given two times"
            AUTHOR="$2"
            shift 2
            ;;
        --*) die "unknown option '$1'; $USAGE" ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done
[[ ${#POSITIONAL[@]} -eq 2 ]] || die "$USAGE"
NAME="${POSITIONAL[0]}"
DEST="${POSITIONAL[1]}"
[[ ! "$DESCRIPTION" =~ [[:cntrl:]] ]] || die "--description must be one line with no control characters"
if [[ -n "$AUTHOR" ]]; then
    [[ ! "$AUTHOR" =~ [[:cntrl:]] ]] || die "--author must have no control characters"
    [[ "$AUTHOR" =~ ^[^\<\>]*[^\<\>[:space:]][[:space:]]*\<[^\<\>[:space:]]+@[^\<\>[:space:]]+\>$ ]] \
        || die "--author must have the form 'Name <email>'"
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="$SKILL_DIR/assets/template"

[[ "$NAME" =~ ^[a-z][a-z0-9]*([-_][a-z0-9]+)*$ ]] \
    || die "invalid name '$NAME': use lowercase letters and digits, separated by '-' or '_'"
case "$NAME" in
    my-project | my_project) die "'$NAME' is the template placeholder; choose another name" ;;
esac
[[ -f "$TEMPLATE/pyproject.toml" ]] || die "template not found at $TEMPLATE"
command -v uv >/dev/null || die "uv is not installed; see https://docs.astral.sh/uv/"
command -v git >/dev/null || die "git is not installed"

if [[ -e "$DEST" ]]; then
    [[ -d "$DEST" ]] || die "'$DEST' exists and is not a directory"
    [[ -z "$(ls -A "$DEST")" ]] || die "'$DEST' is not empty"
fi
PARENT="$(cd "$(dirname "$DEST")" 2>/dev/null && pwd)" || die "parent directory of '$DEST' does not exist"
if git -C "$PARENT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    die "'$DEST' is inside the git repository $(git -C "$PARENT" rev-parse --show-toplevel)"
fi

case "$PARENT" in
    /mnt/?/* | /mnt/?)
        echo "WARNING: '$DEST' is on a Windows drive. Builds are slow there. Prefer the Linux file system." >&2
        export UV_LINK_MODE="${UV_LINK_MODE:-copy}"
        ;;
esac

STEP="copy template"
mkdir -p "$DEST"
DEST="$(cd "$DEST" && pwd)"
DEST_CREATED="$DEST"
cp -a "$TEMPLATE/." "$DEST/"
cd "$DEST"

STEP="git init"
git init -q -b main

STEP="rename placeholders"
uv run --no-project python scripts/rename_project.py "$NAME"
rm -f scripts/rename_project.py
rmdir scripts 2>/dev/null || true

if [[ -n "$DESCRIPTION$AUTHOR" ]]; then
    STEP="metadata"
    NPP_DESCRIPTION="$DESCRIPTION" NPP_AUTHOR="$AUTHOR" uv run --no-project python - <<'PY'
import json
import os
import re
import sys
from pathlib import Path

desc = os.environ["NPP_DESCRIPTION"]
author = os.environ["NPP_AUTHOR"]


def toml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def replace_one(pattern: str, line: str, text: str, what: str) -> str:
    new, n = re.subn(pattern, lambda m: line, text, flags=re.M)
    if n != 1:
        sys.exit(f"metadata: expected 1 {what}, found {n}")
    return new


p = Path("pyproject.toml")
t = p.read_text(encoding="utf-8")
if desc:
    t = replace_one(r"^description = .*$", "description = " + toml_str(desc), t, "description key in pyproject.toml")
if author:
    m = re.fullmatch(r"\s*(.*?)\s*<([^<>\s]+@[^<>\s]+)>\s*", author)
    assert m is not None
    line = f"authors = [{{ name = {toml_str(m.group(1))}, email = {toml_str(m.group(2))} }}]"
    t = replace_one(r"^authors = .*$", line, t, "authors key in pyproject.toml")
p.write_text(t, encoding="utf-8")

if desc:
    r = Path("README.md")
    lines = r.read_text(encoding="utf-8").split("\n")
    if len(lines) < 3 or not lines[0].startswith("# ") or lines[1] != "" or not lines[2].startswith("Short description of "):
        sys.exit("metadata: README.md does not start with the title, a blank line and the description placeholder")
    lines[2] = desc
    r.write_text("\n".join(lines), encoding="utf-8")
PY
fi

STEP="uv sync"
uv sync

STEP="tests"
uv run pytest -q

STEP="ruff"
uv run ruff format --check .
uv run ruff check .

STEP="mypy"
uv run mypy

STEP="pre-commit"
git add -A
uv run pre-commit install
if ! uv run pre-commit run --all-files; then
    # A hook can fix files and return 1. Stage the fixes and run again; fail only on the second run.
    git add -A
    uv run pre-commit run --all-files
fi
git add -A

trap - ERR
PKG="${NAME//-/_}"
cat <<MSG

Created $DEST
  distribution and CLI : ${NAME//_/-}
  import package       : $PKG (src/$PKG)
  env variable prefix  : ${PKG^^}_
Passed: uv sync, pytest, ruff, mypy, pre-commit. Nothing is committed yet.
MSG
[[ -n "$DESCRIPTION" ]] || echo "Not set: description (pyproject.toml and README.md still have the placeholder)."
[[ -n "$AUTHOR" ]] || echo "Not set: authors (pyproject.toml still has 'Your Name <you@example.com>')."
