"""daily.json: which puzzle is the "daily puzzle" for each date, generated days ahead so offline apps know it."""
from __future__ import annotations

import hashlib
from datetime import date, timedelta
from pathlib import Path

from . import store

HORIZON_DAYS = 30
KEEP_PAST_DAYS = 14
DAILY_MAX_WIDTH_RATIO = 1.8  # keep the daily puzzle a comfortable shape on phones


def eligible(docs: Path, today: str) -> list[dict]:
    out = []
    for cid in store.category_ids(docs):
        for x in store.active(store.load_category(docs, cid), today):
            if x["w"] / x["h"] <= DAILY_MAX_WIDTH_RATIO and x.get("difficulty", 2) <= 2 and x.get("maxPieces", 0) >= 300:
                out.append({"category": cid, "id": x["id"], "addedAt": x["addedAt"]})
    return sorted(out, key=lambda e: (e["addedAt"], _shuffle_key(e["id"])))


def _shuffle_key(puzzle_id: str) -> str:
    """A stable pseudo-random order, so the daily puzzle does not walk through one category after another."""
    return hashlib.sha256(puzzle_id.encode()).hexdigest()


def build_daily(docs: Path, today: date) -> dict:
    """Fills missing dates up to the horizon, never rewriting dates already published.
    Picks the least recently used puzzle so the cycle only repeats after everything was shown."""
    path = docs / "daily.json"
    current = store.read_json(path, {"days": {}})["days"]
    pool = eligible(docs, today.isoformat())
    if not pool:
        return {"days": current}
    last_used = {}
    for d, e in sorted(current.items()):
        last_used[e["id"]] = d
    days = {d: e for d, e in current.items() if d >= (today - timedelta(days=KEEP_PAST_DAYS)).isoformat()}
    for i in range(HORIZON_DAYS + 1):
        d = (today + timedelta(days=i)).isoformat()
        if d in days:
            continue
        # a retired puzzle can no longer be chosen because `pool` only holds active ones
        pick = min(pool, key=lambda e: (last_used.get(e["id"], ""), e["addedAt"], _shuffle_key(e["id"])))
        days[d] = {"category": pick["category"], "id": pick["id"]}
        last_used[pick["id"]] = d
    result = {"days": dict(sorted(days.items()))}
    store.write_json(path, result)
    return result
