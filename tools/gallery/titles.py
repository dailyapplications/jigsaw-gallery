"""Turns Commons / museum titles into short, readable English titles (file names often carry dates and camera numbers)."""
from __future__ import annotations

import re

MAX_LEN = 46
# hand-written titles where the automatic rule cannot help (non-Latin names, awkward wording)
OVERRIDES = {
    "commons-17253033": "Red tulips",
    "commons-156423155": "Golden maple leaves",
    "commons-14060928": "Tulip bouquet",
    "commons-169304169": "Rose garden",
    "commons-169349777": "Flower cake",
    "commons-152295751": "Strawberries at the market",
    "commons-129325051": "Colourful macarons",
    "commons-133118032": "Macaron box",
    "commons-29180497": "Juicy oranges",
    "commons-142172803": "Oranges at the market",
    "commons-165941792": "Red fox in the meadow",
    "commons-114034519": "Deer in Nara",
    "commons-114034541": "Young deer",
    "commons-178430232": "Bengal tiger",
    "commons-193842982": "Christmas tree",
    "commons-176373909": "Peacock showing off",
    "commons-179967516": "Common kingfisher",
    "commons-178834525": "Mountain peak with ice cliffs",
    "commons-162746622": "Sunrise at Mount Cook",
    "commons-162746608": "Alpenglow on Mount Cook",
    "nasa-bedin1": "A new galaxy neighbour",
    "met-37193": "Seaside village in winter",
    "met-56906": "Station Fujikawa",
    "cleveland-111656": "Poem by Kakinomoto no Hitomaro",
    "cleveland-152499": "Moon-viewing promontory",
    "cleveland-103244": "Sudden shower over the bridge",
    "cleveland-120225": "Fireworks at Ryōgoku",
    "cleveland-118800": "Rain below the mountain",
}

_DATE = re.compile(r"\b(19|20)\d\d([-./ ]\d{1,2}){0,2}\b")
_MONTH = re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b", re.I)
_CAMERA = re.compile(r"\b(IMG|DSC|DSCF|PXL|P\d{3})[_\- ]?\d+\b|\b\d{6,}\b")
_PAREN_NUM = re.compile(r"\(\s*[\d ]+\)")
_TRAIL_NUM = re.compile(r"[\s\-–,]+\d{1,3}$")
_NONLATIN = re.compile(r"[^\u0000-ɏ‐-‟… ]+")


def clean_title(raw: str, puzzle_id: str = "") -> str:
    if puzzle_id in OVERRIDES:
        return OVERRIDES[puzzle_id]
    t = _NONLATIN.sub(" ", raw)
    t = _PAREN_NUM.sub(" ", t)
    t = _CAMERA.sub(" ", t)
    t = _DATE.sub(" ", t)
    t = _MONTH.sub(" ", t)
    t = re.sub(r"\(\s*\)", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" -–,.;:")
    for _ in range(2):
        t = _TRAIL_NUM.sub("", t).strip(" -–,.;:")
    # keep the first two comma/dash separated parts: "Lighthouse, harbor, Ré island, Charente-Maritime, France" -> "Lighthouse, harbor"
    parts = [p.strip() for p in re.split(r",| - ", t) if p.strip()]
    if len(parts) > 2:
        t = ", ".join(parts[:2])
    if len(t) > MAX_LEN:
        t = t[:MAX_LEN].rsplit(" ", 1)[0].rstrip(" ,-–")
    return t[:1].upper() + t[1:] if t else raw[:MAX_LEN]
