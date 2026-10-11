"""The Met Open Access (CC0). Licence proof: `isPublicDomain` true on the object record."""
from __future__ import annotations

import re
import time

from ..http import get_json
from ..models import Candidate

BASE = "https://collectionapi.metmuseum.org/public/collection"
WANTED = ("Paintings", "Prints", "Drawings", "Photographs", "Illustrations", "Posters")


def _year(text: str) -> int | None:
    m = re.search(r"(1[0-9]{3}|[2-9][0-9]{2})", text or "")
    return int(m.group(1)) if m else None


def _int(text: str) -> int | None:
    try:
        return int(text)
    except (TypeError, ValueError):
        return None


def candidate(obj: dict) -> Candidate | None:
    if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
        return None
    kind = obj.get("classification") or ""
    if not any(w in kind for w in WANTED):
        return None
    return Candidate(
        source="met", source_id=str(obj["objectID"]), title=obj.get("title") or "Untitled",
        creator=(obj.get("artistDisplayName") or "").strip() or "Unknown artist",
        year=_int(obj.get("objectEndDate")) or _year(obj.get("objectDate")),
        death_year=_int(obj.get("artistEndDate")) if obj.get("artistDisplayName") else None,
        license="CC0", source_url=obj.get("objectURL") or "",
        image_url=obj["primaryImage"], preview_url=obj.get("primaryImageSmall") or obj["primaryImage"],
        proof={"isPublicDomain": True, "api": f"{BASE}/v1/objects/{obj['objectID']}"}, kind=kind,
    )


def search(query: str, limit: int = 20) -> list[Candidate]:
    ids = get_json(f"{BASE}/v1.1/search", {"q": query, "hasImages": "true", "isPublicDomain": "true",
                                           "limit": limit * 3, "offset": 0}).get("objectIDs") or []
    out: list[Candidate] = []
    for oid in ids:
        if len(out) >= limit:
            break
        time.sleep(0.15)  # be gentle: the Met rate-limits bursts
        try:
            c = candidate(get_json(f"{BASE}/v1/objects/{oid}"))
        except RuntimeError:
            continue
        if c:
            out.append(c)
    return out
