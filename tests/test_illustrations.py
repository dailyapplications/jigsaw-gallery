import io
import xml.dom.minidom

import cairosvg
from PIL import Image

from tools.illustrations.scenes import SCENES


def render(name):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=SCENES[name]().encode(), output_width=400))).convert("RGB")


def test_every_scene_is_valid_svg_of_the_expected_size():
    assert len(SCENES) >= 10
    for name, scene in SCENES.items():
        doc = xml.dom.minidom.parseString(scene())
        root = doc.documentElement
        assert root.getAttribute("viewBox") == "0 0 1600 1200", name


def test_scenes_are_not_blank_and_use_many_colours():
    for name in SCENES:
        img = render(name)
        colours = len({img.getpixel((x, y)) for x in range(0, 400, 7) for y in range(0, 300, 7)})
        assert colours > 25, f"{name} looks flat"


def test_scenes_differ_from_each_other():
    thumbs = {name: render(name).resize((16, 12)).tobytes() for name in SCENES}
    assert len(set(thumbs.values())) == len(SCENES)


def test_scene_is_deterministic():
    assert SCENES["Under the sea"]() == SCENES["Under the sea"]()
