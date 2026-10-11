"""Renders the cartoon scenes to PNG (2048 px wide) with cairosvg: `python -m tools.illustrations.render [outdir]`."""
from __future__ import annotations

import sys
from pathlib import Path

import cairosvg

from .scenes import SCENES


def render_all(out: Path, width: int = 2048) -> dict[str, Path]:
    out.mkdir(parents=True, exist_ok=True)
    files = {}
    for name, fn in SCENES.items():
        target = out / (name.lower().replace(" ", "-") + ".png")
        cairosvg.svg2png(bytestring=fn().encode(), write_to=str(target), output_width=width)
        files[name] = target
    return files


if __name__ == "__main__":
    for n, f in render_all(Path(sys.argv[1] if len(sys.argv) > 1 else "work/illustrations")).items():
        print(n, f)
