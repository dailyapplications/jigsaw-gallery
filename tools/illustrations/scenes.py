"""Kid-friendly cartoon scenes, drawn from the building blocks in lib.py. Each returns an SVG string."""
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


def balloon_festival() -> str:
    defs = L.grad("bf", [(0, "#5ab8ff"), (0.65, "#bfe6ff"), (1, "#ffe9c7")])
    b = L.rect(0, 0, 1600, 1200, "url(#bf)") + L.sun(1380, 200, 85) + L.cloud(170, 180, 1.3) + L.cloud(1000, 120, 0.9) + L.cloud(620, 330, 1.1)
    b += L.hill(300, 1000, 1200, 150, "#9fdc7a") + L.hill(1250, 1020, 1100, 170, "#7ccf6a") + L.grass(980, "#62c25f", 70)
    for x, y, sc in [(280, 470, 1.5), (760, 360, 2.0), (1240, 520, 1.3), (1480, 300, 0.8), (520, 700, 0.9), (1010, 740, 0.8)]:
        b += L.hot_air_balloon(x, y, sc)
    b += L.kite(120, 760, 1.0, "#ff5a5f", "#ffd84d", -10) + L.bird(660, 190, 0.8) + L.bird(900, 260, 0.6, "#ff7aa8") + L.bird(1100, 160, 0.5)
    for fx, fy, c in [(100, 1120, "#ff6f91"), (330, 1150, "#ffd84d"), (600, 1110, "#ffffff"), (900, 1140, "#ff9f1c"), (1200, 1120, "#8e5fd1"), (1480, 1150, "#ff6f91")]:
        b += L.flower(fx, fy, 1.3, c)
    return L.svg(b, defs)


def birthday_party() -> str:
    defs = L.grad("bp", [(0, "#ffe9f5"), (1, "#fff6d6")])
    b = L.rect(0, 0, 1600, 1200, "url(#bp)") + L.rect(0, 860, 1600, 340, "#ffd9ea")
    flags = ["#ff5a5f", "#ffd84d", "#4ab3ff", "#7ddc6c", "#8e5fd1", "#ff9f1c"]
    b += L.path("M0,60 Q400,260 800,100 Q1200,-40 1600,150", stroke="#8d6e63", sw=6)
    for i in range(16):
        x = 50 + i * 98
        y = 60 + 140 * (0.5 - 0.5 * __import__("math").cos(i / 15 * 3.1416)) * (1 if i < 8 else 0.4) + (i > 7) * 20
        b += L.poly([(x - 28, y), (x + 28, y), (x, y + 70)], flags[i % 6])
    for x, y, c in [(180, 330, "#ff5a5f"), (330, 250, "#ffd84d"), (1270, 280, "#8e5fd1"), (1430, 380, "#4ab3ff"), (800, 360, "#7ddc6c"), (950, 250, "#ff9ecb")]:
        b += L.balloon(x, y, 1.3, c)
    b += L.rect(300, 830, 1000, 40, "#fff8e8", 14) + L.rect(340, 870, 30, 240, "#c98f5b", 6) + L.rect(1230, 870, 30, 240, "#c98f5b", 6)
    b += L.cupcake(450, 800, 1.6) + L.cupcake(1130, 800, 1.6, "#fff1b8", "#ff9ecb") + L.lollipop(640, 650, 1.1) + L.lollipop(980, 650, 1.1, "#6ec6ff", "#ffffff", "#ff9ecb")
    cake = L.rect(-110, -70, 220, 80, "#ff9ecb", 18) + L.rect(-80, -140, 160, 74, "#fff1b8", 16) + L.rect(-110, 0, 220, 14, "#ffffff", 6)
    cake += "".join(L.circle(x, -80, 11, c) for x, c in [(-90, "#6ec6ff"), (-45, "#ffd84d"), (0, "#7ddc6c"), (45, "#ff5a5f"), (90, "#8e5fd1")])
    cake += L.rect(-5, -190, 10, 52, "#6ec6ff", 4) + L.path("M0,-196 q-14,-22 0,-40 q14,18 0,40 Z", "#ff9f1c")
    b += L.g(cake, 800, 830, 1.5)
    b += L.bear(190, 1020, 1.3, "#a56a3f") + L.rabbit(1440, 1030, 1.3) + L.dog(520, 1100, 1.0) + L.cat(1080, 1110, 1.0)
    for x, y in [(120, 700), (1500, 700), (700, 560), (1220, 560)]:
        b += L.star(x, y, 24, "#ffd84d")
    return L.svg(b, defs)


def parrot_paradise() -> str:
    defs = L.grad("pp", [(0, "#8fe3ff"), (1, "#e9ffd9")])
    b = L.rect(0, 0, 1600, 1200, "url(#pp)") + L.sun(1380, 170, 80) + L.cloud(200, 190, 1.2)
    b += L.hill(400, 980, 1400, 160, "#59bb5a") + L.hill(1300, 1000, 1000, 150, "#3fa653")
    b += L.palm(160, 900, 2.0) + L.palm(1460, 920, 2.0)
    b += L.path("M0,330 Q800,260 1600,360", stroke="#8d5a3b", sw=20)
    for x, y, bc, wc, s in [(300, 430, "#e5533d", "#2f8de4", 1.5), (620, 410, "#ffd84d", "#2f8de4", 1.4), (940, 440, "#4ab3ff", "#ff5a5f", 1.5), (1250, 420, "#7ddc6c", "#ffd84d", 1.4)]:
        b += L.parrot(x, y, s, bc, wc)
    b += L.monkey(800, 830, 1.4) + L.butterfly(430, 700, 1.4, "#ff6f91", "#ffd84d", -10) + L.butterfly(1180, 690, 1.3, "#4ab3ff", "#8e5fd1", 15)
    for fx, fy, s, c in [(260, 1090, 2.0, "#ff5a8a"), (520, 1110, 1.7, "#ffd84d"), (1050, 1100, 2.0, "#ff9f1c"), (1330, 1110, 1.8, "#8e5fd1"), (1500, 1120, 1.5, "#ff5a8a")]:
        b += L.flower(fx, fy, s, c)
    return L.svg(b, defs)


def magic_garden() -> str:
    defs = L.grad("mg", [(0, "#c8ecff"), (1, "#f4ffd8")])
    b = L.rect(0, 0, 1600, 1200, "url(#mg)") + L.rainbow(800, 700, 620, 40) + L.sun(1400, 160, 75) + L.cloud(160, 200, 1.4) + L.cloud(900, 120, 0.9)
    b += L.hill(500, 920, 1500, 140, "#9fdc7a") + L.rect(0, 960, 1600, 240, "#62c25f")
    big = [(150, 1100, 3.0, "#ff6f91"), (420, 1130, 2.4, "#ffd84d"), (700, 1100, 3.2, "#8e5fd1"), (1000, 1130, 2.6, "#ff9f1c"), (1280, 1100, 3.0, "#4ab3ff"), (1500, 1130, 2.3, "#ff6f91")]
    for fx, fy, sc, c in big:
        b += L.flower(fx, fy, sc, c)
    b += L.mushroom(560, 1010, 1.4) + L.mushroom(1120, 1030, 1.2, "#8e5fd1")
    b += L.butterfly(300, 560, 1.7, "#ff6f91", "#ffd84d", -10) + L.butterfly(1150, 520, 1.5, "#4ab3ff", "#8e5fd1", 15) + L.butterfly(760, 380, 1.2, "#ffd84d", "#ff9f1c", 5)
    b += L.bee(520, 740, 1.3) + L.bee(980, 700, 1.2) + L.ladybug(860, 1010, 1.2) + L.snail(380, 1120, 1.0)
    return L.svg(b, defs)


def reef_party() -> str:
    defs = L.grad("rp", [(0, "#4fd0ff"), (0.6, "#1e88e5"), (1, "#0d47a1")])
    rnd = random.Random(5)
    b = L.rect(0, 0, 1600, 1200, "url(#rp)")
    for i in range(6):
        b += L.path(f"M{260 * i - 60},0 L{260 * i + 120},0 L{260 * i - 20},700 Z", "#ffffff", extra='opacity="0.07"')
    b += L.path("M0,1040 Q300,960 620,1030 Q940,1100 1240,1010 Q1450,960 1600,1020 L1600,1200 L0,1200 Z", "#f6dc95")
    for x, y, sc, c in [(150, 1080, 1.6, "#ff6b8b"), (420, 1100, 1.3, "#ffa94d"), (760, 1120, 1.5, "#c06bd6"), (1120, 1090, 1.6, "#ff6b8b"), (1400, 1100, 1.4, "#4dd0a0")]:
        b += L.coral(x, y, sc, c)
    b += L.seaweed(60, 1090, 300) + L.seaweed(1540, 1090, 320, "#37b57a")
    for x, y, sc, bc, fc, fl in [(300, 360, 1.3, "#ff8a3d", "#ffc83d", False), (700, 250, 1.0, "#ffd84d", "#ff6f91", True), (1150, 380, 1.4, "#ff5a8a", "#ffd84d", True),
                                 (520, 620, 1.1, "#7ddc6c", "#2f8de4", False), (950, 640, 1.2, "#b66bd6", "#ffd84d", False), (1400, 640, 1.0, "#ff8a3d", "#ffffff", True), (160, 640, 0.9, "#4ab3ff", "#ffd84d", False)]:
        b += L.fish(x, y, sc, bc, fc, fl)
    b += L.whale(1200, 180, 0.9) + L.octopus(820, 900, 1.3, "#b66bd6") + L.crab(260, 1000, 1.3) + L.starfish(1000, 1060, 1.1) + L.starfish(560, 1090, 0.8, "#ffc83d")
    for _ in range(18):
        b += L.bubble(rnd.randint(40, 1560), rnd.randint(80, 900), rnd.randint(10, 34))
    return L.svg(b, defs)


def busy_road() -> str:
    defs = L.grad("br", [(0, "#8fd3ff"), (1, "#e4f6ff")])
    b = L.rect(0, 0, 1600, 1200, "url(#br)") + L.sun(1400, 170, 80) + L.cloud(220, 170, 1.3) + L.cloud(900, 120, 0.9)
    b += L.hill(300, 640, 1100, 120, "#9bdc7a") + L.hill(1300, 650, 900, 110, "#7ccf6a")
    for x, y, sc, w, r in [(150, 520, 1.0, "#ffb74d", "#e5533d"), (420, 540, 1.1, "#ff8fb1", "#6b4aa3"), (710, 520, 1.0, "#6ec6ff", "#ff9f1c"), (1000, 540, 1.1, "#7ddc6c", "#e5533d"), (1280, 520, 1.0, "#ffd84d", "#4ab3ff"), (1500, 540, 0.9, "#c9a0ff", "#ff5a8a")]:
        b += L.house(x, y, sc, w, r)
    b += L.tree(300, 590, 0.8) + L.tree(860, 600, 0.8) + L.tree(1400, 600, 0.8)
    b += L.rect(0, 700, 1600, 90, "#7ccf6a") + L.rect(0, 780, 1600, 420, "#6b6f85") + L.rect(0, 770, 1600, 14, "#c9ccd8")
    for x in range(40, 1600, 220):
        b += L.rect(x, 970, 120, 18, "#ffe27a", 8) + L.rect(x + 40, 1130, 120, 18, "#ffe27a", 8)
    for x, y, sc, c, fl in [(260, 900, 1.5, "#e5533d", False), (780, 880, 1.4, "#4ab3ff", False), (1250, 920, 1.5, "#ffd84d", False), (480, 1090, 1.5, "#7ddc6c", True), (1020, 1080, 1.4, "#ff8fb1", True), (1440, 1090, 1.5, "#8e5fd1", True)]:
        b += L.car(x, y, sc, c) if not fl else L.g(L.car(0, 0, 1, c), x, y, sc, 0, True)
    b += L.balloon(120, 330, 1.0, "#ff5a5f") + L.balloon(1500, 320, 1.0, "#8e5fd1") + L.bird(760, 260, 0.7)
    return L.svg(b, defs)


def safari_rainbow() -> str:
    defs = L.grad("sr", [(0, "#ffd9a0"), (1, "#fff4d6")])
    b = L.rect(0, 0, 1600, 1200, "url(#sr)") + L.rainbow(800, 780, 700, 44) + L.sun(1420, 160, 80) + L.cloud(150, 190, 1.3) + L.cloud(1050, 130, 0.9)
    b += L.hill(300, 960, 1300, 130, "#d9c36a") + L.hill(1300, 980, 1000, 150, "#c7b45a") + L.rect(0, 960, 1600, 240, "#bfa94f")
    b += L.tree(1480, 800, 1.5, "#4caf50") + L.tree(120, 820, 1.2, "#59bb5a")
    b += L.giraffe(480, 860, 1.4) + L.lion(900, 960, 1.3) + L.monkey(1280, 960, 1.2) + L.parrot(1050, 520, 1.0, "#e5533d", "#2f8de4") + L.parrot(1330, 600, 0.9, "#4ab3ff", "#ffd84d")
    b += L.butterfly(300, 600, 1.2, "#ff6f91", "#ffd84d", -10) + L.butterfly(1500, 540, 1.0, "#8e5fd1", "#6ec6ff", 15)
    for fx, fy, c in [(200, 1120, "#ff6f91"), (560, 1140, "#ffd84d"), (1000, 1130, "#ffffff"), (1250, 1140, "#ff9f1c"), (1500, 1120, "#8e5fd1")]:
        b += L.flower(fx, fy, 1.4, c)
    return L.svg(b, defs)


def fruit_orchard() -> str:
    defs = L.grad("fo", [(0, "#a8e0ff"), (1, "#f2ffd9")])
    rnd = random.Random(8)
    b = L.rect(0, 0, 1600, 1200, "url(#fo)") + L.sun(1420, 170, 80) + L.cloud(220, 180, 1.3) + L.cloud(860, 120, 0.9)
    b += L.hill(400, 900, 1500, 140, "#9fdc7a") + L.rect(0, 900, 1600, 300, "#6fcf6a")
    fruit = [("#ff3b4a", 0), ("#ffd84d", 1), ("#ff9f1c", 2), ("#b66bd6", 3), ("#ff3b4a", 4)]
    for ti, (x, y, sc) in enumerate([(260, 720, 2.0), (800, 700, 2.3), (1330, 720, 2.0)]):
        b += L.tree(x, y, sc, "#4caf50", "#8d5a3b")
        col = ["#ff3b4a", "#ff9f1c", "#ffd84d"][ti]
        for k in range(9):
            fx = x + (rnd.random() - 0.5) * 230 * sc * 0.75
            fy = y - 70 * sc + (rnd.random() - 0.4) * 180 * sc * 0.6
            b += L.circle(fx, fy, 15 * sc * 0.8, col) + L.circle(fx - 4, fy - 4, 4 * sc * 0.8, "#ffffff", 'opacity="0.6"')
    for x, y, c in [(120, 1050, "#ff3b4a"), (260, 1110, "#ffd84d"), (520, 1060, "#ff9f1c"), (700, 1120, "#b66bd6"), (1000, 1070, "#ff3b4a"), (1200, 1120, "#7ddc6c"), (1450, 1060, "#ff9f1c")]:
        b += L.circle(x, y, 38, c) + L.circle(x - 12, y - 12, 9, "#ffffff", 'opacity="0.55"') + L.rect(x - 3, y - 52, 6, 16, "#7a4e32", 3)
    b += L.rabbit(640, 960, 1.2) + L.bear(1100, 940, 1.2, "#a56a3f") + L.bee(480, 600, 1.2) + L.butterfly(1020, 560, 1.3, "#ff6f91", "#ffd84d", 10) + L.bird(160, 440, 0.8) + L.bird(1500, 480, 0.7, "#ff7aa8")
    return L.svg(b, defs)


def pets_party_scene() -> str:
    return L.pets_party()


def cozy_pets_scene() -> str:
    return L.cozy_pets()


SCENES = {
    "Happy farm": happy_farm, "Under the sea": under_the_sea, "Space adventure": space_adventure, "Jungle friends": jungle_friends,
    "Candy land": candy_land, "Rainbow sky": rainbow_sky, "Dino valley": dino_valley, "Little town": little_town,
    "Pirate bay": pirate_bay, "Pets party": pets_party_scene, "Cozy pets": cozy_pets_scene, "Forest friends": forest_friends, "Balloon festival": balloon_festival, "Birthday party": birthday_party, "Parrot paradise": parrot_paradise, "Magic garden": magic_garden, "Reef party": reef_party, "Busy road": busy_road, "Safari rainbow": safari_rainbow, "Fruit orchard": fruit_orchard, "Winter fun": winter_fun, "Insect garden": insect_garden,
}
