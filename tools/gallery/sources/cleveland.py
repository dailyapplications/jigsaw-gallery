"""Cleveland Museum of Art Open Access. Licence proof: `share_license_status` == "CC0"."""
from __future__ import annotations

from ..http import get_json
from ..models import Candidate

API = "https://openaccess-api.clevelandart.org/api/artworks/"


def candidate(row: dict) -> Candidate | None:
    images = row.get("images") or {}
    big = (images.get("print") or images.get("full") or {}).get("url")
    web = (images.get("web") or {}).get("url")
    if row.get("share_license_status") != "CC0" or not big or not web:
        return None
    if (row.get("type") or "") not in ("Painting", "Print", "Drawing", "Photograph", "Illustrated Book"):
        return None
    artists = [c for c in row.get("creators") or [] if c.get("role", "artist") in ("artist", "")]
    creator = (artists[0].get("description") or "").split("(")[0].strip() if artists else ""
    death = artists[0].get("death_year") if artists else None
    return Candidate(
        source="cleveland", source_id=str(row["id"]), title=row.get("title") or "Untitled",
        creator=creator or "Unknown artist",
        year=_to_int(row.get("creation_date_latest")), death_year=_to_int(death),
        license="CC0", source_url=row.get("url") or f"https://clevelandart.org/art/{row.get('accession_number')}",
        image_url=big, preview_url=web,
        proof={"share_license_status": "CC0", "api": f"{API}{row['id']}"}, kind=row.get("type") or "",
    )


def _to_int(v) -> int | None:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def search(query: str, limit: int = 20) -> list[Candidate]:
    data = get_json(API, {"q": query, "has_image": 1, "cc0": 1, "limit": limit * 3})
    out = [c for row in data.get("data", []) if (c := candidate(row))]
    return out[:limit]
