import io
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.gallery import images, store  # noqa: E402
from tools.gallery.models import Candidate  # noqa: E402


def jpeg(w=2400, h=1600, color=(200, 120, 60)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (w, h), color).save(buf, "JPEG")
    return buf.getvalue()


def candidate(**kw) -> Candidate:
    base = dict(source="met", source_id="1", title="Water Lilies", creator="Claude Monet", year=1906,
                death_year=1926, license="CC0", source_url="https://example.org/1", image_url="https://example.org/1.jpg",
                preview_url="https://example.org/1s.jpg", proof={"isPublicDomain": True}, kind="Paintings")
    base.update(kw)
    return Candidate(**base)


@pytest.fixture
def docs(tmp_path):
    d = tmp_path / "docs"
    store.new_category(d, "art", {"en": "Art"})
    return d


def add(docs, source_id="1", cat="art", color=(200, 120, 60), w=2400, h=1600, **kw):
    c = candidate(source_id=source_id, **kw)
    p = images.process(jpeg(w, h, color))
    entry = store.puzzle_entry(c, p, cat, "2026-01-01")
    store.add_puzzle(docs, cat, entry, p)
    return entry
