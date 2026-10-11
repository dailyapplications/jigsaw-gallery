"""NASA Image and Video Library. NASA-created media is not copyrighted; we only accept items
credited to a NASA centre (no third-party credit), and never use NASA logos or imply endorsement."""
from __future__ import annotations

from ..http import get_json
from ..models import Candidate

API = "https://images-api.nasa.gov"
CENTRES = {"JPL", "GSFC", "JSC", "MSFC", "KSC", "ARC", "GRC", "LARC", "AFRC", "HQ", "SSC", "STScI"}


def candidate(item: dict) -> Candidate | None:
    data = (item.get("data") or [{}])[0]
    links = item.get("links") or []
    if data.get("media_type") != "image" or not links:
        return None
    if data.get("secondary_creator") or data.get("center") not in CENTRES:
        return None
    nasa_id = data["nasa_id"]
    # "~orig" is the full-size file; asset listings confirm the exact name at import time.
    return Candidate(
        source="nasa", source_id=nasa_id, title=data.get("title") or nasa_id,
        creator=f"NASA/{data['center']}", year=int((data.get("date_created") or "0")[:4]) or None,
        death_year=None, license="NASA", source_url=f"https://images.nasa.gov/details/{nasa_id}",
        image_url=f"https://images-assets.nasa.gov/image/{nasa_id}/{nasa_id}~orig.jpg",
        preview_url=links[0]["href"],
        proof={"center": data["center"], "no_secondary_creator": True, "api": f"{API}/asset/{nasa_id}"},
        kind="NASA image",
    )


def search(query: str, limit: int = 20) -> list[Candidate]:
    data = get_json(f"{API}/search", {"q": query, "media_type": "image"})
    items = data.get("collection", {}).get("items", [])
    out = [c for it in items if (c := candidate(it))]
    return out[:limit]
