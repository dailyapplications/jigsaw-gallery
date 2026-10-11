"""Gate for every change to docs/: licence allowlist, provenance, files present, sizes sane."""
from __future__ import annotations

import re
from pathlib import Path

from . import store
from .images import MAX_FULL_BYTES, PIECE_PRESETS
from .models import ALLOWED_LICENSES, LATEST_ANONYMOUS_WORK_YEAR, LATEST_CREATOR_DEATH_YEAR

REQUIRED = ("id", "title", "file", "thumb", "w", "h", "creator", "source", "sourceUrl", "license",
            "licenseUrl", "proof", "retrieved", "addedAt", "publishAt", "status")
STATUSES = {"active", "retired"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MIN_PER_CATEGORY = 10


def validate_puzzle(docs: Path, cat_id: str, x: dict) -> list[str]:
    where = f"{cat_id}/{x.get('id', '?')}"
    errs = [f"{where}: missing {k}" for k in REQUIRED if x.get(k) in (None, "", {})]
    if errs:
        return errs
    if x["license"] not in ALLOWED_LICENSES:
        errs.append(f"{where}: licence {x['license']!r} is not allowed")
    elif x["licenseUrl"] != ALLOWED_LICENSES[x["license"]]:
        errs.append(f"{where}: licenceUrl does not match licence")
    if x["status"] not in STATUSES:
        errs.append(f"{where}: bad status {x['status']!r}")
    for k in ("retrieved", "addedAt", "publishAt"):
        if not DATE.match(str(x[k])):
            errs.append(f"{where}: {k} is not YYYY-MM-DD")
    if not x["sourceUrl"].startswith("https://"):
        errs.append(f"{where}: sourceUrl must be https")
    if "en" not in x["title"]:
        errs.append(f"{where}: title needs an English entry")
    if x.get("difficulty") not in (1, 2, 3):
        errs.append(f"{where}: difficulty must be 1, 2 or 3")
    if x.get("maxPieces") not in PIECE_PRESETS:
        errs.append(f"{where}: maxPieces must be a piece preset")
    year, death = x.get("year"), x.get("deathYear")
    if x["license"] != "NASA" and x["source"] not in ("commons", "original"):
        if death is not None and death > LATEST_CREATOR_DEATH_YEAR:
            errs.append(f"{where}: creator died {death}, work may still be protected")
        if death is None and (year is None or year > LATEST_ANONYMOUS_WORK_YEAR):
            errs.append(f"{where}: no creator death year and work not clearly old")
    for rel, limit in ((x["file"], MAX_FULL_BYTES), (x["thumb"], 120_000)):
        f = docs / rel
        if not f.exists():
            errs.append(f"{where}: missing file {rel}")
        elif f.stat().st_size > limit:
            errs.append(f"{where}: {rel} is {f.stat().st_size} bytes (limit {limit})")
    return errs


def validate_tree(docs: Path, require_launch_size: bool = False) -> list[str]:
    errs: list[str] = []
    seen: set[str] = set()
    for cid in store.category_ids(docs):
        cat = store.load_category(docs, cid)
        if cat.get("id") != cid:
            errs.append(f"{cid}: category id does not match folder")
        if "en" not in cat.get("title", {}):
            errs.append(f"{cid}: title needs an English entry")
        live = 0
        for x in cat["puzzles"]:
            errs += validate_puzzle(docs, cid, x)
            if x.get("id") in seen:
                errs.append(f"{cid}/{x.get('id')}: duplicate puzzle id")
            seen.add(x.get("id"))
            live += x.get("status") == "active"
        if require_launch_size and live < MIN_PER_CATEGORY:
            errs.append(f"{cid}: only {live} active puzzles (need {MIN_PER_CATEGORY})")
    # every image file must be referenced, so deleted entries do not leave orphans behind
    referenced = {x["file"] for c in store.category_ids(docs) for x in store.load_category(docs, c)["puzzles"] if "file" in x}
    referenced |= {x["thumb"] for c in store.category_ids(docs) for x in store.load_category(docs, c)["puzzles"] if "thumb" in x}
    for f in (docs / "categories").rglob("*.webp") if (docs / "categories").exists() else []:
        if str(f.relative_to(docs)) not in referenced:
            errs.append(f"orphan file {f.relative_to(docs)}")
    return errs
