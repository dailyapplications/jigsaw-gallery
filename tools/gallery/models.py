"""Data shapes shared by the importer, validator and catalog builder."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict

SCHEMA_VERSION = 1
# The only licences the public gallery accepts (see README "Licence policy").
ALLOWED_LICENSES = {
    "CC0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "PD-old": "https://creativecommons.org/publicdomain/mark/1.0/",
    "NASA": "https://www.nasa.gov/nasa-brand-center/images-and-media/",
}
# Newest creator death year we accept: public domain almost everywhere (life + 70).
LATEST_CREATOR_DEATH_YEAR = 1955
# If the creator is unknown, the work itself must be at least this old.
LATEST_ANONYMOUS_WORK_YEAR = 1900


@dataclass
class Candidate:
    """One image offered by a source API, before download."""
    source: str            # commons | original | met | cleveland | smk | nasa
    source_id: str
    title: str
    creator: str
    year: int | None       # best guess of creation year
    death_year: int | None  # creator death year when known
    license: str           # key of ALLOWED_LICENSES
    source_url: str
    image_url: str         # full-size download
    preview_url: str       # small image for the contact sheet
    proof: dict = field(default_factory=dict)  # API fields that justify the licence
    kind: str = ""         # classification, used for filtering

    def to_json(self) -> dict:
        return asdict(self)


@dataclass
class Rejection:
    reason: str


def licence_problem(c: Candidate) -> str | None:
    """Return why a candidate must not enter the gallery, or None when it is safe."""
    if c.license not in ALLOWED_LICENSES:
        return f"licence {c.license!r} not allowed"
    if not c.creator.strip():
        return "creator missing"
    if not c.proof:
        return "no licence proof recorded"
    if c.license == "NASA":
        return None
    if c.source == "commons":  # explicit CC0 dedication by the uploader of their own work
        return None if c.license == "CC0" and c.proof.get("own_work") and c.proof.get("LicenseShortName") == "CC0" \
            else "commons file is not CC0 own work"
    if c.source == "original":  # artwork drawn for this project by tools/illustrations, released as CC0
        return None if c.license == "CC0" and c.proof.get("own_work") else "original artwork must be CC0 own work"
    if c.death_year is not None:
        return None if c.death_year <= LATEST_CREATOR_DEATH_YEAR else f"creator died {c.death_year}"
    if c.year is None or c.year > LATEST_ANONYMOUS_WORK_YEAR:
        return "unknown creator and work not clearly old"
    return None
