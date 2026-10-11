"""Wikimedia Commons, restricted to files their uploader dedicated to the public domain with CC0 (category
"CC-Zero") that are the uploader's "Own work". Everything else on Commons (CC-BY, CC-BY-SA, PD-self of unclear origin ...)
is ignored on purpose. Licence proof: LicenseShortName == "CC0" in the file's machine-readable metadata."""
from __future__ import annotations

import html
import re

from ..http import get_json
from ..models import Candidate

API = "https://commons.wikimedia.org/w/api.php"
FULL_WIDTH = 1920  # Commons only renders standard thumbnail widths (500, 960, 1280, 1920 ...)

# Words that point at identifiable people, brands or protected artwork: such files are skipped before review.
BLOCKED = re.compile(
    r"\b(person|people|man|men|woman|women|girl|girls|boy|boys|child|children|kid|kids|baby|portrait|selfie|face|faces|"
    r"wedding|crowd|tourist|tourists|model|nude|bikini|logo|logos|brand|advertisement|billboard|mural|graffiti|"
    r"statue|sculpture|car|cars|truck|bus|license plate|screenshot|diagram|map|flag|poster|painting|drawing)\b", re.I)


def _plain(text: str | None) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", text or "")).strip()


def candidate(page: dict) -> Candidate | None:
    info = (page.get("imageinfo") or [None])[0]
    if not info:
        return None
    meta = info.get("extmetadata") or {}

    def val(key: str) -> str:
        return _plain((meta.get(key) or {}).get("value"))

    if val("LicenseShortName") != "CC0" or "own work" not in val("Credit").lower():
        return None
    vector = info.get("mime") == "image/svg+xml"  # rendered by Commons at FULL_WIDTH, so the nominal size does not matter
    if not vector and max(info.get("width", 0), info.get("height", 0)) < 1200:
        return None
    title = re.sub(r"^File:|\.[A-Za-z]+$", "", page["title"])
    text = " ".join([title, val("ImageDescription"), " ".join(c["title"] for c in page.get("categories", []))])
    if BLOCKED.search(text):
        return None
    thumb = info.get("thumburl") or info["url"]
    preview = re.sub(r"/\d+px-", "/500px-", thumb)
    return Candidate(
        source="commons", source_id=str(page["pageid"]), title=title[:90], creator=val("Artist")[:60] or "Unknown",
        year=None, death_year=None, license="CC0", source_url=info.get("descriptionurl") or "",
        image_url=thumb, preview_url=preview,
        proof={"LicenseShortName": "CC0", "LicenseUrl": val("LicenseUrl"), "own_work": True,
               "api": f"{API}?action=query&pageids={page['pageid']}&prop=imageinfo&iiprop=extmetadata&format=json"},
        kind="photo",
    )


def search(query: str, limit: int = 20) -> list[Candidate]:
    """`query` may start with "svg:" to search drawings (cartoons, illustrations) instead of photos."""
    filetype = "bitmap"
    if query.startswith("svg:"):
        query, filetype = query[4:].strip(), "drawing"
    data = get_json(API, {
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrlimit": min(50, limit * 4),
        "gsrsearch": f'{query} incategory:"CC-Zero" filetype:{filetype}', "prop": "imageinfo|categories",
        "iiprop": "url|size|mime|extmetadata", "iiurlwidth": FULL_WIDTH, "cllimit": "max",
    })
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))
    out = [c for p in pages if (c := candidate(p))]
    return out[:limit]
