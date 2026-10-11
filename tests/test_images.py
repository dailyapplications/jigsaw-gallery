import io

import pytest
from PIL import Image

from conftest import jpeg
from tools.gallery import images


def test_large_image_becomes_two_webp_files_within_limits():
    p = images.process(jpeg(4000, 3000))
    full = Image.open(io.BytesIO(p.full))
    assert full.format == "WEBP" and max(full.size) == images.FULL_LONG_EDGE
    assert (p.width, p.height) == full.size
    assert len(p.full) <= images.MAX_FULL_BYTES and len(p.thumb) < len(p.full)
    assert max(Image.open(io.BytesIO(p.thumb)).size) == images.THUMB_LONG_EDGE
    assert p.avg_color.startswith("#") and len(p.avg_color) == 7


def test_name_is_content_hash_so_identical_input_gives_identical_name():
    assert images.process(jpeg()).name == images.process(jpeg()).name
    assert images.process(jpeg()).name != images.process(jpeg(color=(1, 2, 3))).name


def test_small_image_is_rejected():
    with pytest.raises(images.Rejected, match="too small"):
        images.process(jpeg(1000, 800))


def test_max_pieces_follows_resolution():
    assert images.max_pieces_for(2048, 1365) == 1000
    assert images.max_pieces_for(1280, 1215) == 500
    assert images.max_pieces_for(1200, 1200) == 500
    assert images.max_pieces_for(300, 200) == 24   # never below the smallest preset


def test_process_reports_max_pieces():
    assert images.process(jpeg(4000, 3000)).max_pieces == 1000
    assert images.process(jpeg(1280, 1100)).max_pieces == 500


def test_panorama_and_tall_strip_are_rejected():
    with pytest.raises(images.Rejected, match="aspect"):
        images.process(jpeg(4000, 1000))
    with pytest.raises(images.Rejected, match="aspect"):
        images.process(jpeg(1000, 4000))


def test_garbage_bytes_are_rejected():
    with pytest.raises(images.Rejected, match="cannot decode"):
        images.process(b"not an image")


def test_image_that_is_not_downscaled_keeps_its_size():
    p = images.process(jpeg(1800, 1700))
    assert (p.width, p.height) == (1800, 1700)


def test_flat_picture_is_hard_and_varied_picture_is_easy():
    import random
    flat = Image.new("RGB", (800, 600), (120, 130, 140))
    assert images.look_alike_share(flat) == 1.0 and images.difficulty_of(1.0) == 3
    rnd = random.Random(1)
    varied = Image.new("RGB", (800, 600))
    for gy in range(12):
        for gx in range(12):  # every patch its own random colour
            varied.paste((rnd.randrange(256), rnd.randrange(256), rnd.randrange(256)), (gx * 66, gy * 50, gx * 66 + 66, gy * 50 + 50))
    assert images.look_alike_share(varied) < 0.1 and images.difficulty_of(images.look_alike_share(varied)) == 1


def test_difficulty_tiers_follow_thresholds():
    assert [images.difficulty_of(v) for v in (0.0, 0.39, 0.4, 0.59, 0.6, 1.0)] == [1, 1, 2, 2, 3, 3]
