"""Build the figures of one document folder: run each diagram script, then convert SVG to PNG.

Usage:
    uv run --with cairosvg python build_figures.py <folder> [--lib <folder>]

For each `<folder>/diagrams/<name>.py` (files that start with "_" are helpers and are skipped):
  1. run it to write `<folder>/resources/<name>.svg`
  2. convert the SVG to `<folder>/resources/<name>.png` at 2x scale

Add `--with <package>` for each package that a diagram script imports.
The diagram scripts import `svglib` and `figkit` from --lib (default: the folder of this file).
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

import cairosvg

SCALE = 2


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
        cairosvg.svg2png(url=str(svg), write_to=str(png), scale=SCALE)
        print(f"ok   {png.relative_to(folder)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
