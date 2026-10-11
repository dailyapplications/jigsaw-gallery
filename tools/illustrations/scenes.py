"""Twelve kid-friendly cartoon scenes, drawn from the building blocks in lib.py. Each returns an SVG string."""
from __future__ import annotations

import random

from .lib import *  # noqa: F401,F403
from . import lib as L


def happy_farm() -> str:
    defs = L.grad("sky", [(0, "#8fd3ff"), (1, "#e4f6ff")])
    b = L.rect(0, 0, 1600, 1200, "url(#sky)") + L.sun(1380, 190, 85) + L.cloud(200, 170, 1.4) + L.cloud(760, 260, 1.0) + L.cloud(1080, 120, 0.8)
    b += L.hill(300, 760, 1100, 160, "#9bdc7a") + L.hill(1250, 780, 1000, 190, "#7ccf6a") + L.barn(1180, 640, 1.5)
    b += L.grass(800, "#6fcf6a") + L.path("M0,1000 Q800,900 1600,1020 L1600,1200 L0,1200 Z", "#59bb5a")
    b += L.fence(60, 700, 9) + L.tree(560, 640, 1.3) + L.cow(420, 900, 1.5) + L.pig(900, 960, 1.3, True) + L.chicken(1300, 1020, 1.2, True) + L.chicken(1480, 1060, 0.9)
    for fx, fy, c in [(120, 1040, "#ff6f91"), (260, 1100, "#ffd84d"), (640, 1080, "#ff9f1c"), (1100, 1120, "#ffffff"), (700, 1020, "#8e5fd1"), (1020, 880, "#ff6f91")]:
        b += L.flower(fx, fy, 1.0, c)
    b += L.bird(1000, 250, 0.7) + L.bird(1120, 330, 0.5, "#ff7aa8")
    return L.svg(b, defs)


def under_the_sea() -> str:
    defs = L.grad("sea", [(0, "#38b6ff"), (0.6, "#1479d8"), (1, "#0b3d91")])
    rnd = random.Random(3)
    b = L.rect(0, 0, 1600, 1200, "url(#sea)")
    for i in range(7):
        b += L.path(f"M{200 * i - 80},0 L{200 * i + 100},0 L{200 * i - 40},620 Z", "#ffffff", extra='opacity="0.07"')
    b += L.path("M0,1050 Q300,950 600,1040 Q900,1120 1200,1010 Q1450,940 1600,1030 L1600,1200 L0,1200 Z", "#f1d58a")
    b += L.seaweed(120, 1080, 320) + L.seaweed(180, 1090, 240, "#37b57a") + L.seaweed(1400, 1070, 340) + L.seaweed(1470, 1090, 260, "#37b57a")
    b += L.coral(330, 1090, 1.5) + L.coral(1250, 1080, 1.3, "#ffa94d") + L.coral(980, 1110, 1.0, "#c06bd6")
    b += L.whale(760, 300, 1.1) + L.fish(250, 520, 1.1, "#ff8a3d") + L.fish(1250, 560, 1.0, "#ffd84d", "#ff8a3d", True) + L.fish(420, 760, 0.8, "#7ddc6c", "#2fa36b") + L.fish(1050, 800, 0.9, "#ff6f91", "#ffb3c4", True)
    b += L.octopus(700, 900, 1.2) + L.crab(1160, 1060, 0.9) + L.starfish(520, 1090, 0.9) + L.starfish(860, 1110, 0.6, "#ffb347")
    for _ in range(22):
        b += L.bubble(rnd.randrange(80, 1520), rnd.randrange(80, 1000), rnd.choice([10, 14, 18, 26]))
    return L.svg(b, defs)


def space_adventure() -> str:
    defs = L.grad("sp", [(0, "#12123a"), (1, "#3b1f6b")]) + L.radial("glow", [(0, "#ffe9a8"), (1, "#ffe9a800")])
    rnd = random.Random(7)
    b = L.rect(0, 0, 1600, 1200, "url(#sp)") + L.sparkle_field(rnd, 90)
    for _ in range(8):
        b += L.star(rnd.randrange(60, 1540), rnd.randrange(60, 700), rnd.choice([14, 18, 24]), "#fff4a8", rnd.randrange(0, 72))
    b += L.planet(250, 300, 140, "#ff8a5b", "#ffd2b0", "#d9562b") + L.planet(1330, 250, 100, "#4ab3ff", None, "#1d6fb8") + L.planet(1200, 820, 170, "#b66bd6", "#f0c8ff", "#8a3fb0")
    b += L.circle(560, 920, 130, "#e9e4f2") + L.circle(520, 890, 26, "#cfc8de") + L.circle(610, 960, 36, "#cfc8de") + L.circle(560, 1000, 18, "#cfc8de") + L.circle(640, 880, 16, "#cfc8de")
    b += L.rocket(800, 520, 1.5, 20) + L.path("M690,720 Q640,820 690,900", "#ffb347", extra='opacity="0.7"') + L.path("M730,740 Q700,860 740,940", "#ff7a3d", extra='opacity="0.6"')
    b += L.alien(1060, 520, 1.1) + L.alien(300, 780, 0.9, "#ff9ecb") + L.path("M1450,100 L1300,170", stroke="#ffffff", sw=8, extra='opacity="0.7"')
    return L.svg(b, defs)


def jungle_friends() -> str:
    defs = L.grad("jg", [(0, "#c8f0b5"), (1, "#7ccf6a")])
    b = L.rect(0, 0, 1600, 1200, "url(#jg)") + L.sun(200, 170, 70, False)
    for x, y, s, c in [(120, 700, 1.7, "#2fa36b"), (480, 640, 1.3, "#3fbf6b"), (1100, 660, 1.5, "#2fa36b"), (1480, 720, 1.8, "#3fbf6b")]:
        b += L.tree(x, y, s, c)
    for i in range(7):
        b += L.path(f"M{i * 240},0 Q{i * 240 + 40},120 {i * 240 + 10},260", stroke="#2a8a54", sw=22)
        b += L.ellipse(i * 240 + 12, 270, 32, 60, "#37b57a")
    b += L.grass(900, "#4fb35a", 80) + L.giraffe(520, 970, 1.5) + L.lion(1030, 890, 1.5) + L.monkey(1420, 560, 1.3) + L.parrot(210, 520, 1.3) + L.parrot(1260, 330, 0.9, "#ffd84d", "#4ab3ff")
    b += L.path("M1000,200 Q1200,330 1500,170", stroke="#7a4e32", sw=16)
    for fx, fy, c in [(100, 1100, "#ff6f91"), (1500, 1130, "#ffd84d"), (800, 1120, "#ff9f1c"), (300, 1150, "#ffffff")]:
        b += L.flower(fx, fy, 1.2, c)
    return L.svg(b, defs)


def candy_land() -> str:
    defs = L.grad("cl", [(0, "#ffe3f1"), (1, "#c9f0ff")])
    b = L.rect(0, 0, 1600, 1200, "url(#cl)") + L.rainbow(800, 760, 640, 44) + L.cloud(150, 200, 1.4) + L.cloud(1250, 170, 1.2)
    b += L.path("M0,900 Q400,800 800,880 Q1200,960 1600,860 L1600,1200 L0,1200 Z", "#ffc9de") + L.path("M0,1000 Q500,930 900,1010 Q1300,1070 1600,990 L1600,1200 L0,1200 Z", "#ffb0cf")
    b += L.lollipop(260, 520, 1.6) + L.lollipop(1340, 500, 1.5, "#6ec6ff", "#ffffff", "#ff9ecb") + L.cupcake(600, 940, 1.5) + L.cupcake(1080, 960, 1.4, "#fff1b8", "#ff9ecb")
    b += L.icecream(820, 880, 1.4) + L.candy(160, 960, 1.2) + L.candy(1450, 940, 1.2, "#6ec6ff") + L.candy(1280, 1100, 1.0, "#7ddc6c")
    for x, y in [(430, 1100), (700, 1120), (1000, 1110), (370, 820), (1210, 810)]:
        b += L.circle(x, y, 22, "#ffffff") + L.circle(x, y, 10, "#ff6f91")
    return L.svg(b, defs)


def rainbow_sky() -> str:
    defs = L.grad("rs", [(0, "#6ec6ff"), (1, "#d8f1ff")])
    b = L.rect(0, 0, 1600, 1200, "url(#rs)") + L.sun(1400, 160, 80) + L.rainbow(800, 820, 700, 46) + L.cloud(80, 700, 1.7) + L.cloud(1250, 740, 1.6) + L.cloud(560, 160, 1.0)
    b += L.hill(400, 1100, 1300, 120, "#8fdc7a") + L.hill(1200, 1120, 1100, 150, "#6fcf6a") + L.grass(1050, "#5cc460", 60)
    b += L.balloon(300, 460, 1.3, "#ff5a5f") + L.balloon(520, 360, 1.0, "#ffd84d") + L.balloon(1110, 400, 1.2, "#8e5fd1") + L.balloon(1300, 520, 1.0, "#4ab3ff")
    b += L.kite(900, 250, 1.1) + L.bird(640, 560, 0.7) + L.bird(760, 620, 0.5, "#ff7aa8") + L.butterfly(980, 880, 1.2) + L.butterfly(260, 930, 0.9, "#8e5fd1", "#6ec6ff", -20)
    for fx, fy, c in [(150, 1130, "#ff6f91"), (420, 1150, "#ffd84d"), (700, 1120, "#ffffff"), (1000, 1140, "#ff9f1c"), (1300, 1120, "#8e5fd1"), (1500, 1150, "#ff6f91")]:
        b += L.flower(fx, fy, 1.3, c)
    return L.svg(b, defs)


def dino_valley() -> str:
    defs = L.grad("dv", [(0, "#ffd9a0"), (1, "#fff4d6")]) + L.radial("lava", [(0, "#ffb347"), (1, "#e5533d")])
    b = L.rect(0, 0, 1600, 1200, "url(#dv)") + L.sun(1380, 170, 80, False)
    b += L.path("M900,650 L1050,300 L1150,300 L1300,650 Z", "#8d6e63") + L.path("M1040,300 Q1100,230 1160,300 Z", "#e5533d") + L.circle(1090, 230, 28, "#ff9f1c", 'opacity="0.8"') + L.circle(1060, 170, 22, "#bdbdbd", 'opacity="0.6"') + L.circle(1110, 110, 30, "#bdbdbd", 'opacity="0.45"')
    b += L.hill(300, 760, 1100, 150, "#a8d86a") + L.hill(1300, 800, 900, 130, "#8fcb5a") + L.grass(850, "#78c45a", 70)
    b += L.palm(150, 760, 1.5) + L.palm(1500, 800, 1.4) + L.dino(520, 900, 1.5, "#4fb84d", False, True) + L.dino(1020, 1010, 1.4, "#ff8a5b") + L.dino(1380, 1090, 0.9, "#6ec6ff", True)
    for ex, ey, c in [(260, 1100, "#fff3d6"), (340, 1130, "#e8f5d0"), (760, 1120, "#fff3d6")]:
        b += L.ellipse(ex, ey, 34, 44, c) + L.circle(ex - 10, ey - 10, 7, "#8fcb5a") + L.circle(ex + 12, ey + 8, 6, "#8fcb5a")
    b += L.butterfly(700, 500, 0.9, "#8e5fd1", "#6ec6ff") + L.bird(300, 260, 0.9, "#ff7aa8")
    return L.svg(b, defs)


def little_town() -> str:
    defs = L.grad("lt", [(0, "#8fd3ff"), (1, "#e9f7ff")])
    b = L.rect(0, 0, 1600, 1200, "url(#lt)") + L.sun(240, 170, 80) + L.cloud(700, 150, 1.2) + L.cloud(1200, 240, 1.0) + L.hot_air_balloon(1050, 460, 1.0)
    b += L.hill(400, 820, 1200, 150, "#a8dd7a") + L.hill(1300, 850, 1000, 130, "#8fd06a")
    for x, y, w, r, d in [(200, 780, "#ffb74d", "#e5533d", "#6b4aa3"), (520, 790, "#8fd3ff", "#6b4aa3", "#e5533d"), (860, 780, "#ffd84d", "#2f8de4", "#e5533d"), (1180, 790, "#ff9ecb", "#8e5fd1", "#2fa36b"), (1480, 780, "#c8f0b5", "#e5533d", "#6b4aa3")]:
        b += L.house(x, y, 1.4, w, r, d)
    b += L.rect(0, 900, 1600, 300, "#6d7a8a") + L.rect(0, 1030, 1600, 12, "#ffd84d") + L.rect(0, 890, 1600, 24, "#b9c3cf")
    b += L.car(420, 1000, 1.2, "#e5533d") + L.car(1100, 1110, 1.2, "#2f8de4") + L.tree(60, 860, 0.8) + L.tree(1560, 860, 0.8)
    b += L.bird(600, 330, 0.6) + L.bird(720, 380, 0.45, "#ff7aa8")
    for x in (330, 760, 1260):
        b += L.flower(x, 910, 0.8, "#ff6f91")
    return L.svg(b, defs)


def pirate_bay() -> str:
    defs = L.grad("pb", [(0, "#ffd9a0"), (1, "#ffefd2")]) + L.grad("pbsea", [(0, "#4fc3ff"), (1, "#1479d8")])
    b = L.rect(0, 0, 1600, 1200, "url(#pb)") + L.sun(1300, 220, 90) + L.cloud(200, 190, 1.3) + L.cloud(780, 120, 0.9)
    b += L.rect(0, 560, 1600, 640, "url(#pbsea)")
    for y, c in [(640, "#6ad0ff"), (760, "#37aef5"), (900, "#1d8de6")]:
        b += L.path(f"M0,{y} " + " ".join(f"q40,-34 80,0" for _ in range(20)), stroke=c, sw=10, extra='opacity="0.6"')
    b += L.pirate_ship(560, 560, 1.7) + L.path("M960,1000 Q1160,820 1380,940 Q1500,1010 1600,990 L1600,1200 L960,1200 Z", "#f1d58a") + L.palm(1250, 960, 1.5) + L.palm(1460, 1010, 1.1) + L.treasure(1120, 1050, 1.1)
    b += L.crab(1050, 1120, 0.6) + L.fish(200, 1000, 0.9, "#ff8a3d") + L.fish(420, 900, 0.7, "#ffd84d", "#ff8a3d", True) + L.bird(1000, 300, 0.8, "#fafafa") + L.bird(900, 380, 0.6, "#fafafa")
    b += L.star(150, 760, 28, "#ff6f91") + L.starfish(780, 1130, 0.8)
    return L.svg(b, defs)


def forest_friends() -> str:
    defs = L.grad("ff", [(0, "#ffe6b3"), (1, "#c8f0b5")])
    b = L.rect(0, 0, 1600, 1200, "url(#ff)") + L.sun(1380, 150, 70, False) + L.cloud(260, 150, 1.0)
    for x, y, s in [(100, 780, 1.8), (400, 760, 1.5), (1180, 760, 1.6), (1500, 790, 1.9)]:
        b += L.tree(x, y, s, "#4fb35a")
    b += L.hill(800, 1000, 1700, 170, "#78c45a") + L.grass(980, "#5cb35a", 80)
    b += L.bear(620, 800, 1.5) + L.fox(1010, 860, 1.5) + L.owl(1330, 480, 1.4) + L.rabbit(320, 900, 1.4) + L.snail(1100, 1130, 0.9)
    for mx, my, c in [(180, 1090, "#e5533d"), (480, 1120, "#ffb300"), (860, 1130, "#e5533d"), (1450, 1100, "#8e5fd1")]:
        b += L.mushroom(mx, my, 1.0, c)
    b += L.butterfly(800, 560, 1.0) + L.bee(540, 480, 1.1) + L.bee(960, 300, 0.9)
    for fx, fy, c in [(700, 1110, "#ff6f91"), (1250, 1140, "#ffd84d"), (60, 1130, "#ffffff")]:
        b += L.flower(fx, fy, 1.1, c)
    return L.svg(b, defs)


def winter_fun() -> str:
    defs = L.grad("wf", [(0, "#a8d8ff"), (1, "#eaf6ff")]) + L.grad("au", [(0, "#7ddc6c00"), (0.5, "#7ddc6caa"), (1, "#8e5fd100")])
    rnd = random.Random(11)
    b = L.rect(0, 0, 1600, 1200, "url(#wf)") + L.path("M0,260 Q400,80 800,220 Q1200,340 1600,140 L1600,380 Q1200,520 800,380 Q400,240 0,420 Z", "#7ddc9c", extra='opacity="0.35"')
    for _ in range(60):
        b += L.circle(rnd.randrange(0, 1600), rnd.randrange(0, 1000), rnd.choice([4, 6, 8]), "#ffffff", 'opacity="0.85"')
    b += L.path("M0,820 Q400,720 800,800 Q1200,880 1600,760 L1600,1200 L0,1200 Z", "#ffffff") + L.path("M0,960 Q500,880 900,960 Q1300,1030 1600,950 L1600,1200 L0,1200 Z", "#e6f3ff")
    b += L.pine(150, 650, 1.6, "#2e7d5b", True) + L.pine(1480, 640, 1.7, "#2e7d5b", True) + L.pine(360, 700, 1.1, "#3a8f66", True)
    b += L.snowman(800, 800, 1.5) + L.penguin(1160, 900, 1.3) + L.penguin(1280, 960, 0.9) + L.penguin(480, 940, 1.1)
    igloo = L.path("M-120,0 A120,110 0 0 1 120,0 Z", "#ffffff") + L.path("M-60,0 A60,60 0 0 1 60,0 Z", "#6aa7d8") + L.path("M-110,-30 L110,-30 M-80,-70 L80,-70", stroke="#cfe6f8", sw=6)
    b += L.g(igloo, 1340, 800, 1.2) + L.bear(240, 880, 1.2, "#f4f4fb") + L.star(80, 160, 20, "#fff4a8") + L.star(1520, 280, 16, "#fff4a8")
    return L.svg(b, defs)


def insect_garden() -> str:
    defs = L.grad("ig", [(0, "#b8e8ff"), (1, "#e9fbd6")])
    b = L.rect(0, 0, 1600, 1200, "url(#ig)") + L.sun(1380, 170, 80) + L.cloud(260, 200, 1.3) + L.cloud(800, 120, 0.9)
    b += L.hill(500, 900, 1400, 140, "#9fdc7a") + L.grass(900, "#78c85a", 70) + L.rect(0, 1000, 1600, 200, "#5cb35a")
    for fx, fy, s, c in [(120, 1100, 2.2, "#ff6f91"), (400, 1120, 1.8, "#ffd84d"), (700, 1100, 2.4, "#8e5fd1"), (1000, 1110, 2.0, "#ff9f1c"), (1300, 1100, 2.3, "#ff6f91"), (1520, 1120, 1.7, "#ffffff")]:
        b += L.flower(fx, fy, s, c)
    b += L.butterfly(300, 520, 1.6, "#ff6f91", "#ffd84d", -10) + L.butterfly(1150, 460, 1.4, "#4ab3ff", "#8e5fd1", 15) + L.butterfly(720, 300, 1.0, "#ffd84d", "#ff9f1c", 5)
    b += L.bee(560, 700, 1.4) + L.bee(1000, 680, 1.2) + L.ladybug(520, 960, 1.4) + L.ladybug(1260, 1000, 1.0) + L.snail(880, 1150, 1.0) + L.mushroom(160, 980, 1.2)
    b += L.path("M1380,980 q40,-60 80,0 q40,60 80,0", stroke="#7ddc6c", sw=30) + L.circle(1560, 984, 30, "#7ddc6c") + L.eye(1568, 974, 8)
    return L.svg(b, defs)


def pets_party_scene() -> str:
    return L.pets_party()


def cozy_pets_scene() -> str:
    return L.cozy_pets()


SCENES = {
    "Happy farm": happy_farm, "Under the sea": under_the_sea, "Space adventure": space_adventure, "Jungle friends": jungle_friends,
    "Candy land": candy_land, "Rainbow sky": rainbow_sky, "Dino valley": dino_valley, "Little town": little_town,
    "Pirate bay": pirate_bay, "Pets party": pets_party_scene, "Cozy pets": cozy_pets_scene, "Forest friends": forest_friends, "Winter fun": winter_fun, "Insect garden": insect_garden,
}
