from conftest import candidate
from tools.gallery.models import licence_problem


def test_cc0_painting_with_old_creator_is_accepted():
    assert licence_problem(candidate()) is None


def test_nasa_item_is_accepted_without_death_year():
    assert licence_problem(candidate(license="NASA", creator="NASA/JPL", death_year=None, year=2011)) is None


def test_cc_by_is_refused():
    assert "not allowed" in licence_problem(candidate(license="CC-BY"))


def test_missing_creator_is_refused():
    assert licence_problem(candidate(creator="  ")) == "creator missing"


def test_missing_proof_is_refused():
    assert licence_problem(candidate(proof={})) == "no licence proof recorded"


def test_creator_who_died_recently_is_refused():
    assert "died 1973" in licence_problem(candidate(death_year=1973))


def test_creator_who_died_in_1955_is_accepted_but_1956_is_refused():
    assert licence_problem(candidate(death_year=1955)) is None
    assert licence_problem(candidate(death_year=1956)) is not None


def test_unknown_creator_needs_an_old_work():
    assert licence_problem(candidate(creator="Unknown artist", death_year=None, year=1850)) is None
    assert licence_problem(candidate(creator="Unknown artist", death_year=None, year=1950)) is not None
    assert licence_problem(candidate(creator="Unknown artist", death_year=None, year=None)) is not None
