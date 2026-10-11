from datetime import date

from conftest import add
from tools.gallery import schedule, store


def _set(docs, key, value):
    cat = store.load_category(docs, "art")
    for x in cat["puzzles"]:
        x[key] = value
    store.write_json(store.category_path(docs, "art"), cat)


def _gallery(docs, n=3):
    for i in range(n):
        add(docs, str(i), color=(i * 40, 10, 10))
    _set(docs, "difficulty", 2)   # flat test pictures are rated hard; medium suits every weekday


def test_fills_today_plus_horizon_days(docs):
    _gallery(docs)
    days = schedule.build_daily(docs, date(2026, 6, 1))["days"]
    assert len(days) == schedule.HORIZON_DAYS + 1 and "2026-06-01" in days


def test_every_puzzle_is_shown_before_any_repeats(docs):
    _gallery(docs, 3)
    days = schedule.build_daily(docs, date(2026, 6, 1))["days"]
    first_three = [days[d]["id"] for d in sorted(days)[:3]]
    assert sorted(first_three) == ["met-0", "met-1", "met-2"]


def test_existing_days_are_never_rewritten(docs):
    _gallery(docs)
    first = schedule.build_daily(docs, date(2026, 6, 1))["days"]
    add(docs, "9", color=(99, 99, 99))
    _set(docs, "difficulty", 2)
    again = schedule.build_daily(docs, date(2026, 6, 2))["days"]
    assert all(again[d] == first[d] for d in first if d in again)


def test_retired_puzzle_is_not_scheduled_for_new_days(docs):
    _gallery(docs)
    schedule.build_daily(docs, date(2026, 6, 1))
    store.retire(docs, "art", "met-0")
    later = schedule.build_daily(docs, date(2026, 8, 1))["days"]
    assert all(e["id"] != "met-0" for d, e in later.items() if d >= "2026-08-01")


def test_very_wide_images_are_not_used_as_daily_puzzle(docs):
    add(docs, "wide", w=3600, h=1900)   # ratio 1.89 > 1.8
    assert schedule.build_daily(docs, date(2026, 6, 1))["days"] == {}


def test_low_resolution_pictures_are_never_the_daily_puzzle(docs):
    _gallery(docs, 1)
    cat = store.load_category(docs, "art")
    cat["puzzles"][0]["maxPieces"] = 150
    store.write_json(store.category_path(docs, "art"), cat)
    assert schedule.build_daily(docs, date(2026, 6, 1))["days"] == {}


def _mixed(docs):
    for i, level in enumerate((1, 2, 3)):
        add(docs, str(i), color=(i * 40, 10, 10))
    cat = store.load_category(docs, "art")
    for x, level in zip(cat["puzzles"], (1, 2, 3)):
        x["difficulty"] = level
    store.write_json(store.category_path(docs, "art"), cat)


def test_difficulty_follows_the_weekday(docs):
    _mixed(docs)
    days = schedule.build_daily(docs, date(2026, 6, 1))["days"]   # a Monday
    assert days["2026-06-01"]["id"] == "met-0"    # Monday: easy
    assert days["2026-06-03"]["id"] == "met-1"    # Wednesday: medium
    assert days["2026-06-06"]["id"] == "met-2"    # Saturday: hard


def test_missing_difficulty_falls_back_to_the_nearest_one(docs):
    _mixed(docs)
    cat = store.load_category(docs, "art")
    cat["puzzles"][2]["difficulty"] = 1     # no hard picture left
    store.write_json(store.category_path(docs, "art"), cat)
    days = schedule.build_daily(docs, date(2026, 6, 1))["days"]
    assert days["2026-06-06"]["id"] == "met-1"   # Saturday gets the nearest level (medium), not nothing


def test_empty_gallery_produces_empty_schedule(docs):
    assert schedule.build_daily(docs, date(2026, 6, 1))["days"] == {}
