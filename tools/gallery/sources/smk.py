"""SMK, the National Gallery of Denmark (open API, no key). Licence proof: `public_domain` true and
`rights` is the Public Domain Mark; SMK publishes these images under CC0 terms."""
from __future__ import annotations

from ..http import get_json
from ..models import Candidate

API = "https://api.smk.dk/api/v1/art/search/"
KINDS = {"Maleri", "Tegning", "Grafik", "Fotografi", "Akvarel"}


def _year(iso: str | None) -> int | None:
    return int(iso[:4]) if iso and iso[:4].isdigit() else None


def candidate(row: dict) -> Candidate | None:
    if not row.get("public_domain") or not row.get("image_native") or not row.get("image_thumbnail"):
        return None
    if "publicdomain/mark" not in (row.get("rights") or "") and "zero" not in (row.get("rights") or ""):
        return None
    names = {n.get("name") for n in row.get("object_names") or []}
    if names and not names & KINDS:
        return None
    prod = (row.get("production") or [{}])[0]
    creator = " ".join(filter(None, [prod.get("creator_forename"), prod.get("creator_surname")])).strip()
    titles = row.get("titles") or [{}]
    title = next((t["title"] for t in titles if t.get("language") == "engelsk"), None) \
        or next((t["title"] for t in titles if "English" in t.get("title", "")), None) or titles[0].get("title") or "Untitled"
    dates = row.get("production_date") or [{}]
    return Candidate(
        source="smk", source_id=row["object_number"], title=title,
        creator=creator or "Unknown artist", year=_year(dates[0].get("end")),
        death_year=_year(prod.get("creator_date_of_death")), license="CC0",
        source_url=f"https://open.smk.dk/artwork/image/{row['object_number']}",
        image_url=row["image_native"], preview_url=row["image_thumbnail"],
        proof={"public_domain": True, "rights": row.get("rights"),
               "api": f"https://api.smk.dk/api/v1/art/?object_number={row['object_number']}"},
        kind=next(iter(names), ""),
    )


def search(query: str, limit: int = 20) -> list[Candidate]:
    data = get_json(API, {"keys": query, "offset": 0, "rows": limit * 3,
                          "filters": "[public_domain:true],[has_image:true]"})
    out = [c for row in data.get("items", []) if (c := candidate(row))]
    return out[:limit]
