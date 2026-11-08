"""Build the figures of one post: run each diagram script, then convert SVG to PNG.

Usage:
    uv run --with cairosvg python build_figures.py <post folder> [--lib <folder>]

For each `<post>/diagrams/<name>.py` (files that start with "_" are helpers and are skipped):
  1. run it to write `<post>/resources/<name>.svg`
  2. convert the SVG to `<post>/resources/<name>.png` at 2x scale

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
    ap.add_argument("post", type=Path)
    ap.add_argument("--lib", type=Path, default=Path(__file__).resolve().parent)
    a = ap.parse_args()
    post = a.post.resolve()
    scripts = sorted(p for p in (post / "diagrams").glob("*.py") if not p.name.startswith("_"))
    if not scripts:
        print(f"no diagram scripts in {post / 'diagrams'}")
        return 1
    out_dir = post / "resources"
    out_dir.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(a.lib.resolve()), str(post / "diagrams")]))
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
        print(f"ok   {png.relative_to(post)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
