"""Command line for curating the gallery.  Run:  .venv/bin/python -m tools.gallery.cli --help

Typical flow:  candidates -> (look at the contact sheet) -> pick -> build -> validate -> commit.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw

from . import images, store, validate
from .http import get_bytes
from .models import Candidate, licence_problem
from .schedule import build_daily
from .sources import SOURCES

WORK = store.ROOT / "work"
SEED = store.ROOT / "seed" / "categories.json"


def _candidates_file(cat: str) -> Path:
    return WORK / "candidates" / f"{cat}.json"


def cmd_new_category(a) -> None:
    store.new_category(store.DOCS, a.id, json.loads(a.titles) if a.titles else {"en": a.id.title()})


def cmd_seed_categories(a) -> None:
    for c in json.loads(SEED.read_text(encoding="utf-8")):
        store.new_category(store.DOCS, c["id"], c["title"])
        cat = store.load_category(store.DOCS, c["id"])
        if cat["title"] != c["title"]:  # titles are edited in seed/categories.json
            cat["title"] = c["title"]
            store.write_json(store.category_path(store.DOCS, c["id"]), cat)
    print("categories ready:", ", ".join(store.category_ids(store.DOCS)))


def contact_sheet(cands: list[Candidate], path: Path, cols: int = 5, cell: int = 300) -> None:
    rows = (len(cands) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 34)), "white")
    draw = ImageDraw.Draw(sheet)
    for i, c in enumerate(cands):
        x, y = (i % cols) * cell, (i // cols) * (cell + 34)
        try:
            im = Image.open(io.BytesIO(get_bytes(c.preview_url))).convert("RGB")
            im.thumbnail((cell - 8, cell - 8))
            sheet.paste(im, (x + 4, y + 4))
        except Exception:
            draw.text((x + 10, y + 100), "no preview", fill="red")
        draw.text((x + 6, y + cell), f"#{i}  {c.title[:36]}", fill="black")
        draw.text((x + 6, y + cell + 14), f"{c.creator[:24]} {c.year or ''} [{c.source}]", fill="gray")
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, quality=80)


def cmd_candidates(a) -> None:
    store.load_category(store.DOCS, a.category)
    have = {x["id"] for x in store.load_category(store.DOCS, a.category)["puzzles"]}
    found: dict[str, Candidate] = {}
    for q in a.query:
        for name in a.source.split(","):
            try:
                results = SOURCES[name].search(q, a.limit)
            except RuntimeError as e:
                print(f"  {name} {q!r}: {e}", file=sys.stderr)
                continue
            for c in results:
                key = f"{c.source}-{c.source_id}"
                if key in have or key in found:
                    continue
                if (why := licence_problem(c)):
                    print(f"  skip {key}: {why}")
                    continue
                found[key] = c
    cands = list(found.values())[: a.max]
    _candidates_file(a.category).parent.mkdir(parents=True, exist_ok=True)
    _candidates_file(a.category).write_text(json.dumps([c.to_json() for c in cands], indent=1), encoding="utf-8")
    sheet = WORK / "contact" / f"{a.category}.jpg"
    contact_sheet(cands, sheet)
    print(f"{len(cands)} candidates -> {sheet}")


def import_candidate(cat: str, c: Candidate, docs: Path, publish_at: str | None = None) -> str:
    if (why := licence_problem(c)):
        return f"refused: {why}"
    pid = f"{c.source}-{c.source_id}"
    for other in store.category_ids(docs):
        if any(x["id"] == pid for x in store.load_category(docs, other)["puzzles"]):
            return f"already in category {other}"
    try:
        p = images.process(get_bytes(c.image_url, timeout=180))
    except (images.Rejected, RuntimeError) as e:
        return f"rejected: {e}"
    entry = store.puzzle_entry(c, p, cat, store.today_str(), publish_at)
    return "added" if store.add_puzzle(docs, cat, entry, p) else "already present"


def cmd_pick(a) -> None:
    cands = [Candidate(**d) for d in json.loads(_candidates_file(a.category).read_text(encoding="utf-8"))]
    for i in (int(n) for n in a.numbers.split(",")):
        c = cands[i]
        print(f"#{i} {c.source}-{c.source_id} {c.title[:50]!r}: {import_candidate(a.category, c, store.DOCS)}")


# Cartoons have large flat areas that the photo-oriented rating calls hard; they are made for kids with few big
# pieces, so they are rated by hand: 1 easy, 2 medium.
CARTOON_DIFFICULTY = {"Happy farm": 1, "Candy land": 1, "Rainbow sky": 1, "Little town": 1, "Jungle friends": 1, "Forest friends": 1,
                      "Pets party": 1, "Cozy pets": 1, "Under the sea": 2, "Space adventure": 2, "Dino valley": 2, "Pirate bay": 2, "Winter fun": 2, "Insect garden": 2,
                      "Balloon festival": 1, "Birthday party": 2, "Parrot paradise": 2, "Magic garden": 1, "Reef party": 2, "Busy road": 1, "Safari rainbow": 1, "Fruit orchard": 2}


def cmd_import_illustrations(a) -> None:
    """Draws our own cartoon scenes (tools/illustrations) and adds them to the `kids` category."""
    import io
    import cairosvg
    from tools.illustrations.scenes import SCENES

    store.new_category(store.DOCS, "kids", {"en": "Cartoon fun"})
    for name, scene in SCENES.items():
        png = cairosvg.svg2png(bytestring=scene().encode(), output_width=2048)
        slug = name.lower().replace(" ", "-")
        c = Candidate(source="original", source_id=slug, title=name, creator="Daily Applications", year=2026, death_year=None,
                      license="CC0", source_url="https://github.com/dailyapplications/jigsaw-gallery/blob/master/tools/illustrations/scenes.py",
                      image_url="", preview_url="", proof={"own_work": True, "generator": "tools/illustrations"}, kind="illustration")
        if (why := licence_problem(c)):
            print(name, "refused:", why)
            continue
        p = images.process(png)
        p.difficulty = CARTOON_DIFFICULTY.get(name, 1)
        entry = store.puzzle_entry(c, p, "kids", store.today_str())
        print(name, "added" if store.add_puzzle(store.DOCS, "kids", entry, p) else "already present")


def cmd_rate(a) -> None:
    """Recomputes the difficulty of every picture from its stored image (after changing the thresholds)."""
    for cid in store.category_ids(store.DOCS):
        cat = store.load_category(store.DOCS, cid)
        for x in cat["puzzles"]:
            share = images.look_alike_share(Image.open(store.DOCS / x["file"]))
            x["lookAlike"] = round(share, 3)
            x["difficulty"] = CARTOON_DIFFICULTY.get(x["title"]["en"], 1) if x["source"] == "original" else images.difficulty_in(cid, share)
            x["maxPieces"] = images.max_pieces_for(x["w"], x["h"])
            if a.verbose:
                print(f"{cid:14} {x['id']:22} {share:.2f} -> {x['difficulty']}  {x['title']['en'][:40]}")
        store.write_json(store.category_path(store.DOCS, cid), cat)


BORDER_CATEGORIES = ("impressionism", "masterpieces", "ukiyoe", "colour")  # photographed paintings and prints, where a black mat is a scan artefact


def cmd_trim_borders(a) -> None:
    """Cuts the black scan border off pictures in paintings categories and re-writes the files (new content hash)."""
    import io
    for cid in BORDER_CATEGORIES:
        cat = store.load_category(store.DOCS, cid)
        for x in cat["puzzles"]:
            if x["source"] == "commons":  # photos can have genuinely dark edges (night, sunset foregrounds)
                continue
            img = Image.open(store.DOCS / x["file"]).convert("RGB")
            cut = images.trim_dark_border(img)
            if cut.size == img.size:
                continue
            buf = io.BytesIO()
            cut.save(buf, "PNG")
            p = images.process(buf.getvalue())
            old = [store.DOCS / x["file"], store.DOCS / x["thumb"]]
            x["file"], x["thumb"] = f"categories/{cid}/img/{p.name}.webp", f"categories/{cid}/thumb/{p.name}.webp"
            (store.DOCS / x["file"]).write_bytes(p.full)
            (store.DOCS / x["thumb"]).write_bytes(p.thumb)
            for f in old:
                f.unlink(missing_ok=True)
            x.update(w=p.width, h=p.height, avgColor=p.avg_color, lookAlike=p.look_alike, difficulty=images.difficulty_in(cid, p.look_alike), maxPieces=p.max_pieces)
            print(f"{cid:14} {x['id']:22} {img.size} -> {cut.size}  {x['title']['en'][:40]}")
        store.write_json(store.category_path(store.DOCS, cid), cat)


def cmd_retitle(a) -> None:
    """Re-applies the title cleanup to every picture (English title only; translations are kept)."""
    from .titles import clean_title
    for cid in store.category_ids(store.DOCS):
        cat = store.load_category(store.DOCS, cid)
        for x in cat["puzzles"]:
            x["title"]["en"] = clean_title(x["title"]["en"], x["id"])
        store.write_json(store.category_path(store.DOCS, cid), cat)


def cmd_retire(a) -> None:
    print("retired" if store.retire(store.DOCS, a.category, a.puzzle_id) else "nothing to retire")


def cmd_build(a) -> None:
    today = date.today()
    order = [c["id"] for c in json.loads(SEED.read_text(encoding="utf-8"))] if SEED.exists() else None
    cat = store.build_catalog(store.DOCS, today.isoformat(), order)
    daily = build_daily(store.DOCS, today)
    write_licenses()
    print(f"catalog v{cat['version']}: {len(cat['categories'])} categories, "
          f"{sum(c['count'] for c in cat['categories'])} puzzles, {len(daily['days'])} daily slots")


def write_licenses() -> None:
    lines = ["# Image licences and sources", "",
             "Generated by `build`. Every image is CC0 / public domain (or NASA-created) with the proof recorded in its",
             "`category.json` entry.", ""]
    for cid in store.category_ids(store.DOCS):
        cat = store.load_category(store.DOCS, cid)
        lines += [f"## {cat['title']['en']}", ""]
        for x in cat["puzzles"]:
            lines.append(f"- {x['title']['en']} — {x['creator']}, {x['license']}, [{x['source']}]({x['sourceUrl']})"
                         + (" (retired)" if x["status"] == "retired" else ""))
        lines.append("")
    (store.ROOT / "LICENSES.md").write_text("\n".join(lines), encoding="utf-8")


def cmd_validate(a) -> None:
    errs = validate.validate_tree(store.DOCS, require_launch_size=a.launch)
    for e in errs:
        print("ERROR", e)
    print("OK" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="gallery")
    sub = p.add_subparsers(required=True)
    s = sub.add_parser("new-category"); s.add_argument("id"); s.add_argument("--titles", help='JSON {"en": "..."}'); s.set_defaults(f=cmd_new_category)
    s = sub.add_parser("seed-categories"); s.set_defaults(f=cmd_seed_categories)
    s = sub.add_parser("candidates"); s.add_argument("category"); s.add_argument("--query", action="append", required=True)
    s.add_argument("--source", default="commons"); s.add_argument("--limit", type=int, default=12)
    s.add_argument("--max", type=int, default=30); s.set_defaults(f=cmd_candidates)
    s = sub.add_parser("pick"); s.add_argument("category"); s.add_argument("numbers"); s.set_defaults(f=cmd_pick)
    s = sub.add_parser("retire"); s.add_argument("category"); s.add_argument("puzzle_id"); s.set_defaults(f=cmd_retire)
    s = sub.add_parser("import-illustrations"); s.set_defaults(f=cmd_import_illustrations)
    s = sub.add_parser("retitle"); s.set_defaults(f=cmd_retitle)
    s = sub.add_parser("trim-borders"); s.set_defaults(f=cmd_trim_borders)
    s = sub.add_parser("rate"); s.add_argument("-v", "--verbose", action="store_true"); s.set_defaults(f=cmd_rate)
    s = sub.add_parser("build"); s.set_defaults(f=cmd_build)
    s = sub.add_parser("validate"); s.add_argument("--launch", action="store_true"); s.set_defaults(f=cmd_validate)
    a = p.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
