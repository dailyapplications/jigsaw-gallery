"""Reads and writes the served tree under docs/ (catalog.json, categories/<id>/category.json, daily.json)."""
from __future__ import annotations

import hashlib
import json
import time
from datetime import date
from pathlib import Path

from .images import Processed
from .models import ALLOWED_LICENSES, SCHEMA_VERSION, Candidate

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")


def read_json(path: Path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def category_path(docs: Path, cat_id: str) -> Path:
    return docs / "categories" / cat_id / "category.json"


def load_category(docs: Path, cat_id: str) -> dict:
    cat = read_json(category_path(docs, cat_id))
    if cat is None:
        raise SystemExit(f"unknown category {cat_id!r}; create it with `new-category` first")
    return cat


def new_category(docs: Path, cat_id: str, titles: dict[str, str]) -> None:
    if category_path(docs, cat_id).exists():
        return
    write_json(category_path(docs, cat_id), {"id": cat_id, "title": titles, "puzzles": []})


def puzzle_entry(c: Candidate, p: Processed, cat_id: str, today: str, publish_at: str | None = None,
                 titles: dict[str, str] | None = None) -> dict:
    return {
        "id": f"{c.source}-{c.source_id}",
        "title": {"en": c.title[:90], **(titles or {})},
        "file": f"categories/{cat_id}/img/{p.name}.webp",
        "thumb": f"categories/{cat_id}/thumb/{p.name}.webp",
        "w": p.width, "h": p.height, "avgColor": p.avg_color,
        "difficulty": p.difficulty, "lookAlike": p.look_alike, "maxPieces": p.max_pieces,
        "creator": c.creator, "year": c.year, "deathYear": c.death_year,
        "source": c.source, "sourceUrl": c.source_url,
        "license": c.license, "licenseUrl": ALLOWED_LICENSES[c.license],
        "proof": c.proof, "retrieved": today,
        "addedAt": today, "publishAt": publish_at or today, "status": "active", "tags": [],
    }


def add_puzzle(docs: Path, cat_id: str, entry: dict, p: Processed) -> bool:
    """Write the image files and register the entry. Returns False if the id already exists."""
    cat = load_category(docs, cat_id)
    if any(x["id"] == entry["id"] for x in cat["puzzles"]):
        return False
    for rel, blob in ((entry["file"], p.full), (entry["thumb"], p.thumb)):
        target = docs / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
    cat["puzzles"].append(entry)
    write_json(category_path(docs, cat_id), cat)
    return True


def retire(docs: Path, cat_id: str, puzzle_id: str) -> bool:
    cat = load_category(docs, cat_id)
    for x in cat["puzzles"]:
        if x["id"] == puzzle_id and x["status"] != "retired":
            x["status"] = "retired"
            write_json(category_path(docs, cat_id), cat)
            return True
    return False


def active(cat: dict, today: str) -> list[dict]:
    return [x for x in cat["puzzles"] if x["status"] == "active" and x["publishAt"] <= today]


def category_ids(docs: Path) -> list[str]:
    cats = docs / "categories"
    return sorted(p.name for p in cats.iterdir() if (p / "category.json").exists()) if cats.exists() else []


def build_catalog(docs: Path, today: str, order: list[str] | None = None) -> dict:
    """Rewrites catalog.json from the category files. Empty categories are listed with count 0 (the app hides them)."""
    ids = category_ids(docs)
    if order:
        ids = [i for i in order if i in ids] + [i for i in ids if i not in order]
    cats = []
    for i, cid in enumerate(ids):
        cat = load_category(docs, cid)
        live = active(cat, today)
        rev = hashlib.sha256(category_path(docs, cid).read_bytes()).hexdigest()[:10]  # apps refetch a category only when this changes
        cats.append({"id": cid, "title": cat["title"], "order": i, "count": len(live), "rev": rev,
                     "cover": live[0]["thumb"] if live else None,
                     "path": f"categories/{cid}/category.json"})
    prev = read_json(docs / "catalog.json", {})
    # `version` only changes when content changes, so apps can skip identical downloads.
    body = {"schemaVersion": SCHEMA_VERSION, "minAppVersion": 1, "categories": cats}
    same = {k: prev.get(k) for k in body} == body
    catalog = {**body, "version": prev.get("version", 1) if same else int(time.time())}
    write_json(docs / "catalog.json", catalog)
    return catalog


def today_str() -> str:
    return date.today().isoformat()
