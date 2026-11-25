"""Check that each skill has the communication rules of AGENTS.md.

Usage: python3 tools/check_style.py
Exit code 1 when a rule is missing from a skill, or when a skill has an extra rule.
The "In reviews" rule is optional.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPTIONAL_PREFIX = "- In reviews:"


def bullets(text: str) -> list[str]:
    return [line.rstrip() for line in text.splitlines() if line.startswith("- ")]


def section(text: str) -> str | None:
    m = re.search(r"^## Communication style\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def main() -> int:
    canon = bullets((ROOT / "AGENTS.md").read_text(encoding="utf-8"))
    required = [b for b in canon if not b.startswith(OPTIONAL_PREFIX)]
    errors = 0
    for skill in sorted((ROOT / "skills").rglob("SKILL.md")):
        body = section(skill.read_text(encoding="utf-8"))
        name = skill.parent.relative_to(ROOT / "skills").as_posix()
        if body is None:
            print(f"{name}: no '## Communication style' section")
            errors += 1
            continue
        have = bullets(body)
        for b in required:
            if b not in have:
                print(f"{name}: missing: {b[:70]}")
                errors += 1
        for b in have:
            if b not in canon:
                print(f"{name}: not in AGENTS.md: {b[:70]}")
                errors += 1
    print(f"{errors} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
