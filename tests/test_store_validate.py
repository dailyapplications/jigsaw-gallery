import json

from conftest import add
from tools.gallery import store, validate


def test_add_registers_entry_and_writes_both_files(docs):
    e = add(docs)
    assert (docs / e["file"]).exists() and (docs / e["thumb"]).exists()
    assert store.load_category(docs, "art")["puzzles"][0]["id"] == "met-1"
    assert validate.validate_tree(docs) == []


def test_adding_the_same_source_id_twice_is_ignored(docs):
    add(docs)
    add(docs)
    assert len(store.load_category(docs, "art")["puzzles"]) == 1


def test_retired_and_future_puzzles_are_not_active(docs):
    add(docs, "1")
    add(docs, "2")
    add(docs, "3")
    cat = store.load_category(docs, "art")
    cat["puzzles"][2]["publishAt"] = "2099-01-01"
    store.write_json(store.category_path(docs, "art"), cat)
    assert store.retire(docs, "art", "met-2") is True
    assert store.retire(docs, "art", "met-2") is False   # already retired
    assert store.retire(docs, "art", "nope") is False
    live = store.active(store.load_category(docs, "art"), "2026-06-01")
    assert [x["id"] for x in live] == ["met-1"]


def test_catalog_version_only_changes_when_content_changes(docs):
    add(docs)
    v1 = store.build_catalog(docs, "2026-06-01")["version"]
    assert store.build_catalog(docs, "2026-06-01")["version"] == v1
    add(docs, "2", color=(10, 200, 30))
    assert store.build_catalog(docs, "2026-06-01")["version"] >= v1
    c = store.build_catalog(docs, "2026-06-01")["categories"][0]
    assert c["count"] == 2 and c["cover"].endswith(".webp")


def test_catalog_order_follows_the_seed_order(docs):
    store.new_category(docs, "b", {"en": "B"})
    ids = [c["id"] for c in store.build_catalog(docs, "2026-06-01", order=["b", "art"])["categories"]]
    assert ids == ["b", "art"]


def test_validator_flags_disallowed_licence(docs):
    e = add(docs)
    cat = store.load_category(docs, "art")
    cat["puzzles"][0]["license"] = "CC-BY"
    store.write_json(store.category_path(docs, "art"), cat)
    assert any("not allowed" in x for x in validate.validate_tree(docs))


def test_validator_flags_missing_provenance_and_missing_file(docs):
    e = add(docs)
    (docs / e["file"]).unlink()
    cat = store.load_category(docs, "art")
    cat["puzzles"][0]["proof"] = {}
    store.write_json(store.category_path(docs, "art"), cat)
    errs = validate.validate_tree(docs)
    assert any("missing proof" in x for x in errs) and not any("missing file" in x for x in errs)  # stops at first problem
    cat["puzzles"][0]["proof"] = {"x": 1}
    store.write_json(store.category_path(docs, "art"), cat)
    assert any("missing file" in x for x in validate.validate_tree(docs))


def test_validator_flags_recent_creator_and_orphans_and_duplicates(docs):
    add(docs, "1")
    add(docs, "2", color=(5, 5, 5))
    cat = store.load_category(docs, "art")
    cat["puzzles"][0]["deathYear"] = 1990
    cat["puzzles"][1]["id"] = cat["puzzles"][0]["id"]
    store.write_json(store.category_path(docs, "art"), cat)
    (docs / "categories/art/img/stray.webp").write_bytes(b"x")
    errs = " | ".join(validate.validate_tree(docs))
    assert "died 1990" in errs and "duplicate puzzle id" in errs and "orphan file" in errs


def test_launch_size_rule_needs_ten_active_puzzles(docs):
    add(docs)
    assert any("need 10" in x for x in validate.validate_tree(docs, require_launch_size=True))
    assert not any("need 10" in x for x in validate.validate_tree(docs))


def test_retired_entries_stay_in_the_file_for_provenance(docs):
    add(docs)
    store.retire(docs, "art", "met-1")
    assert json.loads(store.category_path(docs, "art").read_text())["puzzles"][0]["status"] == "retired"


def test_category_rev_changes_when_the_category_file_changes(docs):
    add(docs)
    before = store.build_catalog(docs, "2026-06-01")["categories"][0]["rev"]
    store.retire(docs, "art", "met-1")
    after = store.build_catalog(docs, "2026-06-01")["categories"][0]["rev"]
    assert before != after and len(after) == 10


def test_seed_categories_have_titles_in_all_launch_languages():
    import json
    from pathlib import Path
    languages = {"en", "es", "pt-BR", "fr", "de", "it", "ru", "tr", "id", "ar", "ja", "ko", "hi"}
    seed = json.loads((Path(__file__).resolve().parents[1] / "seed" / "categories.json").read_text(encoding="utf-8"))
    assert len(seed) >= 15
    for c in seed:
        assert set(c["title"]) == languages, c["id"]
        assert all(t.strip() for t in c["title"].values())
