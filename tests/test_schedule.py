from datetime import date

from conftest import add
from tools.gallery import schedule, store


def _gallery(docs, n=3):
    for i in range(n):
        add(docs, str(i), color=(i * 40, 10, 10))


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


def test_empty_gallery_produces_empty_schedule(docs):
    assert schedule.build_daily(docs, date(2026, 6, 1))["days"] == {}
