from tools.gallery.titles import MAX_LEN, clean_title


def test_dates_camera_numbers_and_trailing_counters_are_removed():
    assert clean_title("Neuschwanstein Castle 2024-02") == "Neuschwanstein Castle"
    assert clean_title("Windmills along Zaan 2024-11-29") == "Windmills along Zaan"
    assert clean_title("Sunrise IMG20251118113500 field") == "Sunrise field"
    assert clean_title("Belle Tout Lighthouse, June 2020 01") == "Belle Tout Lighthouse"
    assert clean_title("Christmas tree (22622)") == "Christmas tree"
    assert clean_title("20190121 Nara deer-2") == "Nara deer"


def test_non_latin_text_is_dropped_and_long_titles_are_shortened():
    assert clean_title("Autumn leaves Все краски осени Листья клена 21") == "Autumn leaves"
    long = "A male Indian Peafowl trying to attract female peafowl to mate in the early morning light"
    assert len(clean_title(long)) <= MAX_LEN and not clean_title(long).endswith(" ")


def test_only_the_first_two_parts_of_a_place_title_are_kept():
    assert clean_title("Lighthouse, harbor Saint-Martin-de-Ré, Ré island, Charente-Maritime, France") == "Lighthouse, harbor Saint-Martin-de-Ré"


def test_hand_written_overrides_win_and_empty_titles_fall_back():
    assert clean_title("צבעונים", "commons-17253033") == "Red tulips"
    assert clean_title("12345678") == "12345678"


def test_normal_titles_are_left_alone():
    assert clean_title("Happy farm") == "Happy farm"
    assert clean_title("Allegory of the Catholic Faith") == "Allegory of the Catholic Faith"


def test_apply_titles_adds_translations_only_to_matching_titles(docs, tmp_path, monkeypatch):
    import json
    from tests.conftest import add
    from tools.gallery import cli, store
    add(docs, "1", title="Happy farm")
    add(docs, "2", title="Something else")
    table = tmp_path / "t.json"
    table.write_text(json.dumps({"Happy farm": {"de": "Fröhlicher Bauernhof", "fr": "Ferme joyeuse"}}), encoding="utf-8")
    monkeypatch.setattr(cli, "TITLE_TRANSLATIONS", table)
    monkeypatch.setattr(store, "DOCS", docs)
    cli.cmd_apply_titles(None)
    puzzles = {x["id"]: x["title"] for x in store.load_category(docs, "art")["puzzles"]}
    assert puzzles["met-1"]["de"] == "Fröhlicher Bauernhof" and puzzles["met-1"]["en"] == "Happy farm"
    assert puzzles["met-2"] == {"en": "Something else"}            # no entry in the table: untouched


def test_apply_titles_is_repeatable_and_keeps_the_english_title(docs, tmp_path, monkeypatch):
    import json
    from tests.conftest import add
    from tools.gallery import cli, store
    add(docs, "1", title="Happy farm")
    table = tmp_path / "t.json"
    table.write_text(json.dumps({"Happy farm": {"de": "Bauernhof"}}), encoding="utf-8")
    monkeypatch.setattr(cli, "TITLE_TRANSLATIONS", table)
    monkeypatch.setattr(store, "DOCS", docs)
    cli.cmd_apply_titles(None)
    first = store.read_json(store.category_path(docs, "art"))
    cli.cmd_apply_titles(None)
    assert store.read_json(store.category_path(docs, "art")) == first
