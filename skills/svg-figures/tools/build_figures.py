"""Build the figures of one document folder: run each diagram script, then convert SVG to PNG.

Usage:
    uv run --with cairosvg python build_figures.py <folder> [--lib <folder>]

For each `<folder>/diagrams/<name>.py` (files that start with "_" are helpers and are skipped):
  1. run it to write `<folder>/resources/<name>.svg`
  2. convert the SVG to `<folder>/resources/<name>.png` at 2x scale

Add `--with <package>` for each package that a diagram script imports.
The diagram scripts import `svglib` and `figkit` from --lib (default: the folder of this file).

Fonts: cairosvg uses only the FIRST family of a font-family stack. An unknown first family (for example
`ui-monospace`) falls back to the default sans font, so mono text renders in sans. Before the PNG step, each
stack is replaced by its first installed family (from fc-list), or by its last, generic item (`monospace`,
`sans-serif`). The SVG file does not change.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import cairosvg

SCALE = 2
FONT_ATTR = re.compile(r'font-family="([^"]*)"')


def installed_families() -> set[str] | None:
    """Lower-case family names from fc-list, or None when fc-list is absent."""
    if not shutil.which("fc-list"):
        return None
    out = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout
    return {name.strip().lower() for name in re.split(r"[,\n]", out) if name.strip()}


class FontResolver:
    def __init__(self) -> None:
        self.installed = installed_families()
        self.cache: dict[str, str] = {}
        self.warned: set[str] = set()

    def resolve(self, stack: str) -> str:
        if stack not in self.cache:
            names = [n.strip().strip("'\"") for n in stack.split(",") if n.strip()]
            generic = names[-1] if names else stack
            pick = generic
            if self.installed is not None:
                pick = next((n for n in names[:-1] if n.lower() in self.installed), generic)
            if pick == generic and generic == "sans-serif" and stack not in self.warned:
                self.warned.add(stack)
                print(f"WARN fonts: no font of '{stack}' is installed; the PNG uses the default sans font")
            self.cache[stack] = pick
        return self.cache[stack]

    def rewrite(self, svg_text: str) -> str:
        return FONT_ATTR.sub(lambda m: f'font-family="{self.resolve(m.group(1))}"', svg_text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path)
    ap.add_argument("--lib", type=Path, default=Path(__file__).resolve().parent)
    a = ap.parse_args()
    folder = a.folder.resolve()
    scripts = sorted(p for p in (folder / "diagrams").glob("*.py") if not p.name.startswith("_"))
    if not scripts:
        print(f"no diagram scripts in {folder / 'diagrams'}")
        return 1
    out_dir = folder / "resources"
    out_dir.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(a.lib.resolve()), str(folder / "diagrams")]))
    fonts = FontResolver()
    failed = 0
    for script in scripts:
        svg = out_dir / f"{script.stem}.svg"
        png = out_dir / f"{script.stem}.png"
        proc = subprocess.run([sys.executable, str(script), str(svg)], capture_output=True, text=True, env=env)
        if proc.returncode != 0:
            failed += 1
            print(f"FAIL {script.name}\n{proc.stderr}")
            continue
        if proc.stderr.strip():
            print(f"WARN {script.name}: {proc.stderr.strip()}")
        svg_text = fonts.rewrite(svg.read_text(encoding="utf-8"))
        cairosvg.svg2png(bytestring=svg_text.encode("utf-8"), write_to=str(png), scale=SCALE)
        print(f"ok   {png.relative_to(folder)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
