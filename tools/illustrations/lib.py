"""Tiny flat-design SVG toolkit for the original cartoon pictures (our own artwork, released as CC0).
Everything draws in a 1600 x 1200 viewBox; scenes are rendered to PNG by render.py."""
from __future__ import annotations

import math
import random

W, H = 1600, 1200


def svg(body: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f"<defs>{defs}</defs>{body}</svg>")


def grad(gid: str, stops: list[tuple[float, str]], x1=0, y1=0, x2=0, y2=1) -> str:
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def radial(gid: str, stops: list[tuple[float, str]]) -> str:
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<radialGradient id="{gid}">{s}</radialGradient>'


def circle(cx, cy, r, fill, extra="") -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {extra}/>'


def ellipse(cx, cy, rx, ry, fill, extra="") -> str:
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'


def rect(x, y, w, h, fill, rx=0, extra="") -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'


def poly(points, fill, extra="") -> str:
    return f'<polygon points="{" ".join(f"{x},{y}" for x, y in points)}" fill="{fill}" {extra}/>'


def path(d, fill="none", stroke="none", sw=0, extra="") -> str:
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def g(content: str, x=0, y=0, s=1.0, rot=0, flip=False) -> str:
    sx = -s if flip else s
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({sx},{s})">{content}</g>'


def eye(x, y, r=14, look=(0, 0)) -> str:
    return (circle(x, y, r, "#fff") + circle(x + look[0], y + look[1], r * 0.55, "#2b2233") +
            circle(x + look[0] + r * 0.2, y + look[1] - r * 0.2, r * 0.2, "#fff"))


def cheeks(x1, x2, y, r=14, color="#ff9aa2") -> str:
    return circle(x1, y, r, color, 'opacity="0.55"') + circle(x2, y, r, color, 'opacity="0.55"')


def smile(x, y, w=26, color="#2b2233", sw=5) -> str:
    return path(f"M{x - w},{y} Q{x},{y + w * 0.9} {x + w},{y}", stroke=color, sw=sw)


def star(cx, cy, r, fill, rot=0) -> str:
    pts = []
    for i in range(10):
        a = math.radians(-90 + rot + i * 36)
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((round(cx + rr * math.cos(a), 1), round(cy + rr * math.sin(a), 1)))
    return poly(pts, fill)


def cloud(x, y, s=1.0, color="#ffffff") -> str:
    body = (circle(0, 0, 55, color) + circle(60, -25, 70, color) + circle(135, 0, 55, color) +
            rect(-5, 0, 150, 55, color, 27) + circle(60, 25, 45, color))
    return g(body, x, y, s)


def sun(x, y, r=90, face=True) -> str:
    rays = "".join(path(f"M{x + (r + 20) * math.cos(a):.0f},{y + (r + 20) * math.sin(a):.0f} L{x + (r + 55) * math.cos(a):.0f},"
                        f"{y + (r + 55) * math.sin(a):.0f}", stroke="#ffc83d", sw=16)
                   for a in [i * math.pi / 6 for i in range(12)])
    out = rays + circle(x, y, r, "#ffd84d")
    if face:
        out += eye(x - 30, y - 8, 11) + eye(x + 30, y - 8, 11) + smile(x, y + 22, 24) + cheeks(x - 52, x + 52, y + 22, 12)
    return out


def hill(cx, base, w, h, fill) -> str:
    return path(f"M{cx - w / 2},{base} Q{cx},{base - h * 2} {cx + w / 2},{base} Z", fill)


def tree(x, y, s=1.0, leaf="#4caf50", trunk="#8d5a3b") -> str:
    body = rect(-14, -10, 28, 110, trunk, 8) + circle(0, -50, 70, leaf) + circle(-45, -10, 48, leaf) + circle(45, -10, 48, leaf)
    return g(body, x, y, s)


def pine(x, y, s=1.0, color="#2e7d5b", snow=False) -> str:
    body = rect(-12, 60, 24, 50, "#7a4e32", 4)
    for i, (w, yy) in enumerate([(110, 40), (90, -10), (70, -55)]):
        body += poly([(-w, yy + 40), (w, yy + 40), (0, yy - 55)], color)
        if snow:
            body += poly([(-w * 0.45, yy - 14), (w * 0.45, yy - 14), (0, yy - 55)], "#fff")
    return g(body, x, y, s)


def flower(x, y, s=1.0, petal="#ff6f91", center="#ffd84d", stem=True) -> str:
    body = (rect(-4, 0, 8, 70, "#4aa564", 4) if stem else "")
    for i in range(6):
        a = i * 60
        body += g(ellipse(0, -22, 12, 22, petal), 0, 0, 1, a)
    body += circle(0, 0, 14, center)
    return g(body, x, y, s)


def house(x, y, s=1.0, wall="#ffb74d", roof="#e5533d", door="#6b4aa3") -> str:
    body = (rect(-90, -80, 180, 140, wall, 8) + poly([(-110, -75), (0, -170), (110, -75)], roof) +
            rect(-24, 0, 48, 60, door, 10) + rect(-70, -45, 40, 40, "#bfe9ff", 6) + rect(30, -45, 40, 40, "#bfe9ff", 6) +
            circle(14, 32, 4, "#ffd84d"))
    return g(body, x, y, s)


def bubble(x, y, r) -> str:
    return circle(x, y, r, "#ffffff", 'opacity="0.35"') + circle(x - r * 0.3, y - r * 0.3, r * 0.22, "#ffffff", 'opacity="0.7"')


def fish(x, y, s=1.0, body="#ff8a3d", fin="#ffc83d", flip=False) -> str:
    f = (path("M-70,0 L-125,-45 L-125,45 Z", fin) + ellipse(0, 0, 80, 48, body) +
         path("M-10,-44 Q20,-90 50,-40 Z", fin) + path("M0,40 Q20,75 40,38 Z", fin) +
         ellipse(10, 12, 60, 28, "#ffffff", 'opacity="0.25"') + eye(40, -10, 11, (3, 0)) + smile(58, 14, 12, "#2b2233", 4) +
         path("M-20,-30 Q-30,0 -20,30", stroke="#ffffff", sw=8, extra='opacity="0.45"'))
    return g(f, x, y, s, flip=flip)


def starfish(x, y, s=1.0, color="#ff7a6b") -> str:
    return g(star(0, 0, 60, color) + eye(-14, -4, 7) + eye(14, -4, 7) + smile(0, 14, 10, "#2b2233", 3), x, y, s)


def seaweed(x, y, h=260, color="#2fa36b") -> str:
    d = f"M{x},{y} " + " ".join(f"Q{x + (40 if i % 2 else -40)},{y - h * (i + 0.5) / 4} {x},{y - h * (i + 1) / 4}" for i in range(4))
    return path(d, stroke=color, sw=22)


def coral(x, y, s=1.0, color="#ff6b8b") -> str:
    b = path("M0,0 L0,-120 M0,-60 L-45,-110 M0,-80 L45,-130 M-45,-110 L-45,-150 M45,-130 L45,-170", stroke=color, sw=22)
    return g(b + circle(0, -125, 16, color) + circle(-45, -155, 14, color) + circle(45, -175, 14, color), x, y, s)


def rocket(x, y, s=1.0, rot=0) -> str:
    b = (path("M-30,60 Q-60,110 -20,125 L0,90 L20,125 Q60,110 30,60 Z", "#ff9f1c") +
         path("M-45,20 L-95,85 L-45,70 Z", "#e5533d") + path("M45,20 L95,85 L45,70 Z", "#e5533d") +
         path("M0,-130 Q70,-60 45,70 L-45,70 Q-70,-60 0,-130 Z", "#f4f4fb") +
         path("M0,-130 Q40,-95 52,-50 L-52,-50 Q-40,-95 0,-130 Z", "#e5533d") +
         circle(0, -10, 28, "#6ec6ff") + circle(0, -10, 20, "#bfe9ff") + rect(-45, 40, 90, 16, "#e5533d"))
    return g(b, x, y, s, rot)


def planet(x, y, r, color, ring=None, stripe=None) -> str:
    out = ""
    if ring:
        out += g(ellipse(0, 0, r * 1.8, r * 0.45, "none", f'stroke="{ring}" stroke-width="{r * 0.18}"'), x, y, 1, -18)
    out += circle(x, y, r, color)
    if stripe:
        out += path(f"M{x - r * 0.9},{y - r * 0.2} Q{x},{y + r * 0.15} {x + r * 0.9},{y - r * 0.2}", stroke=stripe, sw=r * 0.16, extra='opacity="0.55"')
        out += path(f"M{x - r * 0.7},{y + r * 0.35} Q{x},{y + r * 0.6} {x + r * 0.7},{y + r * 0.35}", stroke=stripe, sw=r * 0.12, extra='opacity="0.45"')
    if ring:
        out += g(path(f"M{-r * 1.8},0 A{r * 1.8},{r * 0.45} 0 0 0 {r * 1.8},0", stroke=ring, sw=r * 0.18), x, y, 1, -18)
    return out


def alien(x, y, s=1.0, color="#7ddc6c") -> str:
    b = (path("M-40,50 Q-70,10 -45,-45 Q0,-100 45,-45 Q70,10 40,50 Q0,75 -40,50 Z", color) +
         path("M-20,-70 L-35,-120", stroke=color, sw=8) + circle(-37, -125, 12, "#ffd84d") +
         path("M20,-70 L35,-120", stroke=color, sw=8) + circle(37, -125, 12, "#ffd84d") +
         eye(-18, -20, 18) + eye(18, -20, 18) + smile(0, 18, 18, "#2b2233", 4) + cheeks(-36, 36, 12, 9))
    return g(b, x, y, s)


# ---- animals --------------------------------------------------------------------------------------------------

def cow(x, y, s=1.0, flip=False) -> str:
    b = (rect(-80, 40, 22, 70, "#f5f5f5", 8) + rect(-30, 40, 22, 70, "#f5f5f5", 8) + rect(30, 40, 22, 70, "#f5f5f5", 8) +
         rect(80, 40, 22, 70, "#f5f5f5", 8) + path("M-130,-10 Q-150,0 -145,50", stroke="#2b2233", sw=8) +
         ellipse(0, 0, 135, 78, "#fafafa") + ellipse(-45, -15, 38, 30, "#3a3140") + ellipse(40, 25, 34, 26, "#3a3140") +
         ellipse(90, -10, 22, 18, "#3a3140") + rect(95, -60, 85, 80, "#fafafa", 36) + ellipse(160, 28, 36, 28, "#ffb3b3") +
         circle(150, 28, 5, "#7a5b5b") + circle(170, 28, 5, "#7a5b5b") + eye(138, -22, 11) + path("M105,-65 Q95,-100 120,-90", stroke="#e8d4a8", sw=10) +
         path("M170,-65 Q185,-100 160,-90", stroke="#e8d4a8", sw=10) + ellipse(100, -48, 24, 12, "#f1c8c0", 'transform="rotate(-25 100 -48)"'))
    return g(b, x, y, s, flip=flip)


def pig(x, y, s=1.0, flip=False) -> str:
    b = (rect(-60, 40, 22, 55, "#f4a5b8", 8) + rect(50, 40, 22, 55, "#f4a5b8", 8) + ellipse(0, 0, 100, 70, "#ffbfd0") +
         circle(105, -5, 52, "#ffbfd0") + path("M80,-45 L95,-85 L115,-48 Z", "#f4a5b8") + ellipse(140, 8, 24, 18, "#ff9fb5") +
         circle(133, 8, 4, "#a65a6e") + circle(147, 8, 4, "#a65a6e") + eye(108, -18, 9) + path("M-100,-5 q-30,-15 -10,-35 q15,-10 5,10", stroke="#f4a5b8", sw=8))
    return g(b, x, y, s, flip=flip)


def chicken(x, y, s=1.0, flip=False) -> str:
    b = (path("M-20,45 L-20,85 M20,45 L20,85", stroke="#ff9f1c", sw=8) + path("M-40,85 L-20,85 L-5,85 M0,85 L20,85 L35,85", stroke="#ff9f1c", sw=8) +
         ellipse(0, 0, 60, 50, "#ffffff") + path("M-50,-10 Q-85,-40 -70,0 Q-80,25 -45,25", "#ffffff") + circle(30, -50, 30, "#ffffff") +
         path("M10,-75 Q20,-100 30,-80 Q40,-102 48,-76 Z", "#e5533d") + poly([(55, -52), (85, -42), (55, -34)], "#ffb300") +
         path("M45,-26 Q55,-5 40,0", "#e5533d") + eye(38, -56, 7) + ellipse(-5, 5, 34, 24, "#f1f1f1"))
    return g(b, x, y, s, flip=flip)


def giraffe(x, y, s=1.0, flip=False) -> str:
    spots = "".join(ellipse(px, py, 14, 11, "#b87333") for px, py in [(-30, -20), (10, 10), (-60, 20), (40, -25), (65, 15), (-10, -45)])
    neck = "".join(ellipse(px, py, 11, 9, "#b87333") for px, py in [(105, -90), (118, -150), (102, -200), (120, -250)])
    b = (rect(-70, 40, 20, 100, "#ffcf5d", 8) + rect(-30, 40, 20, 100, "#ffcf5d", 8) + rect(30, 40, 20, 100, "#ffcf5d", 8) +
         rect(70, 40, 20, 100, "#ffcf5d", 8) + ellipse(0, 0, 105, 62, "#ffcf5d") + spots +
         path("M70,-30 L135,-300 L185,-290 L130,10 Z", "#ffcf5d") + neck + ellipse(170, -315, 52, 36, "#ffcf5d") + ellipse(198, -305, 30, 22, "#ffe29a") +
         path("M150,-345 L146,-385", stroke="#b87333", sw=7) + circle(146, -388, 8, "#b87333") + path("M175,-345 L182,-385", stroke="#b87333", sw=7) +
         circle(182, -388, 8, "#b87333") + eye(172, -322, 9) + path("M-100,-10 Q-125,10 -112,50", stroke="#b87333", sw=8))
    return g(b, x, y, s, flip=flip)


def lion(x, y, s=1.0) -> str:
    mane = "".join(circle(70 * math.cos(math.radians(a)), 70 * math.sin(math.radians(a)), 42, "#e0842b") for a in range(0, 360, 30))
    b = (mane + circle(0, 0, 75, "#ffc04d") + circle(-60, -55, 20, "#ffc04d") + circle(60, -55, 20, "#ffc04d") + ellipse(0, 25, 35, 26, "#ffe6b3") +
         path("M-10,10 L10,10 L0,22 Z", "#6b3f2a") + eye(-28, -12, 11) + eye(28, -12, 11) + path("M0,22 Q-14,42 -26,32 M0,22 Q14,42 26,32", stroke="#6b3f2a", sw=4) +
         cheeks(-48, 48, 14, 10))
    return g(b, x, y, s)


def monkey(x, y, s=1.0) -> str:
    b = (path("M60,60 Q130,60 120,-10 Q115,-45 90,-35", stroke="#8d5a3b", sw=14) + ellipse(0, 40, 62, 72, "#a8693e") + ellipse(0, 55, 38, 46, "#f1d2a7") +
         circle(0, -50, 52, "#a8693e") + circle(-58, -52, 24, "#a8693e") + circle(58, -52, 24, "#a8693e") + circle(-58, -52, 13, "#f1d2a7") + circle(58, -52, 13, "#f1d2a7") +
         ellipse(0, -36, 36, 32, "#f1d2a7") + eye(-16, -52, 9) + eye(16, -52, 9) + smile(0, -30, 14, "#6b3f2a", 4) + circle(-5, -40, 3, "#6b3f2a") + circle(5, -40, 3, "#6b3f2a"))
    return g(b, x, y, s)


def parrot(x, y, s=1.0, body="#e5533d", wing="#2f8de4") -> str:
    b = (path("M-10,80 L-30,140 L0,120 L30,140 L10,80 Z", "#ffd84d") + ellipse(0, 20, 52, 75, body) + path("M-45,0 Q-100,40 -55,95 Q-20,70 -25,10 Z", wing) +
         circle(0, -70, 44, body) + ellipse(-12, -78, 24, 24, "#ffffff") + eye(-12, -78, 10) + path("M28,-80 Q75,-70 60,-40 Q50,-55 28,-52 Z", "#ffb300") +
         path("M-5,-120 Q10,-150 25,-118", stroke=body, sw=12))
    return g(b, x, y, s)


def owl(x, y, s=1.0, body="#8d6e63") -> str:
    b = (poly([(-45, -85), (-28, -125), (-8, -90)], body) + poly([(45, -85), (28, -125), (8, -90)], body) + ellipse(0, 0, 70, 95, body) +
         ellipse(0, 25, 46, 62, "#d7b899") + "".join(path(f"M{ax - 12},{ay} q12,12 24,0", stroke="#b89574", sw=4) for ax, ay in [(-14, 15), (14, 15), (0, 35), (-18, 45), (18, 45)]) +
         circle(-28, -35, 28, "#fff3d6") + circle(28, -35, 28, "#fff3d6") + circle(-28, -35, 14, "#2b2233") + circle(28, -35, 14, "#2b2233") +
         circle(-24, -40, 5, "#fff") + circle(32, -40, 5, "#fff") + poly([(-9, -18), (9, -18), (0, 2)], "#ffb300") +
         path("M-70,-5 Q-100,40 -60,70 Q-50,30 -55,0 Z", "#6d4c41") + path("M70,-5 Q100,40 60,70 Q50,30 55,0 Z", "#6d4c41") + path("M-30,85 L-30,105 M30,85 L30,105", stroke="#ffb300", sw=8))
    return g(b, x, y, s)


def bear(x, y, s=1.0, body="#a56a3f") -> str:
    b = (ellipse(0, 70, 70, 80, body) + ellipse(0, 85, 44, 52, "#e8c8a0") + circle(-72, -60, 26, body) + circle(72, -60, 26, body) + circle(-72, -60, 14, "#e8c8a0") +
         circle(72, -60, 14, "#e8c8a0") + circle(0, -25, 66, body) + ellipse(0, -5, 34, 26, "#e8c8a0") + ellipse(0, -14, 11, 8, "#3a2a22") + eye(-28, -38, 9) + eye(28, -38, 9) +
         path("M0,-8 L0,6 M-14,12 Q0,22 14,12", stroke="#3a2a22", sw=4) + cheeks(-44, 44, -8, 10) +
         ellipse(-62, 70, 18, 30, body, 'transform="rotate(25 -62 70)"') + ellipse(62, 70, 18, 30, body, 'transform="rotate(-25 62 70)"'))
    return g(b, x, y, s)


def rabbit(x, y, s=1.0, body="#f2eee8") -> str:
    b = (ellipse(-26, -135, 20, 60, body) + ellipse(-26, -135, 10, 44, "#ffc4cf") + ellipse(26, -135, 20, 60, body, 'transform="rotate(8 26 -135)"') +
         ellipse(26, -135, 10, 44, "#ffc4cf", 'transform="rotate(8 26 -135)"') + ellipse(0, 60, 62, 72, body) + circle(0, -35, 56, body) + eye(-20, -42, 8) + eye(20, -42, 8) +
         ellipse(0, -22, 8, 6, "#ff8ea1") + path("M0,-16 L0,-4 M-10,2 Q0,10 10,2", stroke="#9a7b7b", sw=3) + cheeks(-34, 34, -14, 9) + circle(-50, 110, 18, body) + circle(50, 110, 18, body))
    return g(b, x, y, s)


def fox(x, y, s=1.0) -> str:
    b = (path("M50,70 Q150,60 140,-20 Q110,0 90,30 Z", "#f28b2d") + path("M118,-6 Q140,-20 140,-20 Q132,15 100,40 Z", "#fff") + ellipse(0, 60, 58, 70, "#f28b2d") +
         ellipse(0, 78, 30, 48, "#fff3e0") + poly([(-62, -45), (-52, -105), (-14, -62)], "#f28b2d") + poly([(62, -45), (52, -105), (14, -62)], "#f28b2d") +
         poly([(-52, -62), (-48, -90), (-30, -66)], "#3a2a22") + poly([(52, -62), (48, -90), (30, -66)], "#3a2a22") +
         path("M-64,-30 Q0,-80 64,-30 Q56,30 0,52 Q-56,30 -64,-30 Z", "#f28b2d") + path("M-64,-30 Q-20,20 0,52 Q20,20 64,-30 Q40,10 0,18 Q-40,10 -64,-30 Z", "#fff3e0") +
         eye(-24, -22, 9) + eye(24, -22, 9) + ellipse(0, 28, 9, 7, "#3a2a22"))
    return g(b, x, y, s)


def penguin(x, y, s=1.0) -> str:
    b = (ellipse(-28, 112, 24, 11, "#ff9f1c") + ellipse(28, 112, 24, 11, "#ff9f1c") + ellipse(0, 25, 62, 90, "#2e3a59") + ellipse(0, 40, 44, 66, "#ffffff") +
         path("M-60,10 Q-100,50 -64,75 Q-50,45 -52,15 Z", "#2e3a59") + path("M60,10 Q100,50 64,75 Q50,45 52,15 Z", "#2e3a59") +
         eye(-18, -25, 11) + eye(18, -25, 11) + poly([(-12, -8), (12, -8), (0, 12)], "#ff9f1c") + cheeks(-34, 34, -8, 8))
    return g(b, x, y, s)


def snowman(x, y, s=1.0) -> str:
    b = (circle(0, 80, 80, "#ffffff") + circle(0, -20, 58, "#ffffff") + circle(0, -105, 42, "#ffffff") + rect(-40, -150, 80, 12, "#3f51b5", 4) +
         rect(-26, -190, 52, 44, "#3f51b5", 6) + eye(-14, -112, 6) + eye(14, -112, 6) + poly([(0, -100), (46, -92), (0, -86)], "#ff8a3d") +
         circle(0, -10, 7, "#2b2233") + circle(0, 20, 7, "#2b2233") + circle(0, 52, 7, "#2b2233") +
         path("M-50,-30 L-100,-70 M50,-30 L100,-70", stroke="#7a4e32", sw=8) + path("M-30,-72 Q0,-55 30,-72", stroke="#e5533d", sw=14))
    return g(b, x, y, s)


def dino(x, y, s=1.0, color="#6cc04a", flip=False, long_neck=False) -> str:
    plates = "".join(poly([(px, py), (px + 20, py - 36), (px + 40, py)], "#ffb300") for px, py in [(-60, -50), (-20, -62), (20, -62), (60, -50)])
    if long_neck:
        b = (path("M-120,30 Q-170,50 -190,100 Q-130,70 -90,60 Z", color) + ellipse(0, 20, 120, 70, color) + path("M60,0 Q110,-120 80,-220 L130,-230 Q150,-110 110,20 Z", color) +
             ellipse(120, -235, 44, 32, color) + eye(132, -245, 8) + cheeks(130, 130, -222, 8) + rect(-70, 60, 28, 80, color, 10) + rect(40, 60, 28, 80, color, 10) +
             ellipse(-10, 38, 70, 40, "#b8e3a0"))
    else:
        b = (path("M-110,20 Q-190,40 -170,-30 Q-140,10 -100,-20 Z", color) + ellipse(0, 25, 115, 78, color) + ellipse(0, 45, 80, 46, "#b8e3a0") + plates +
             rect(-55, 70, 30, 70, color, 10) + rect(35, 70, 30, 70, color, 10) + circle(105, -25, 52, color) + ellipse(138, -8, 38, 28, color) +
             eye(112, -42, 10) + path("M118,-6 Q135,6 156,-4", stroke="#2b2233", sw=4) + poly([(132, 0), (138, 14), (144, 0)], "#fff") + cheeks(110, 110, -14, 9))
    return g(b, x, y, s, flip=flip)


def butterfly(x, y, s=1.0, c1="#ff6f91", c2="#ffd84d", rot=0) -> str:
    b = (ellipse(-48, -28, 52, 40, c1, 'transform="rotate(-20 -48 -28)"') + ellipse(48, -28, 52, 40, c1, 'transform="rotate(20 48 -28)"') +
         ellipse(-36, 32, 36, 30, c2, 'transform="rotate(20 -36 32)"') + ellipse(36, 32, 36, 30, c2, 'transform="rotate(-20 36 32)"') +
         circle(-50, -30, 14, "#ffffff", 'opacity="0.7"') + circle(50, -30, 14, "#ffffff", 'opacity="0.7"') +
         ellipse(0, 0, 9, 52, "#4a3b52") + circle(0, -56, 11, "#4a3b52") + path("M-3,-64 Q-20,-100 -30,-96 M3,-64 Q20,-100 30,-96", stroke="#4a3b52", sw=4))
    return g(b, x, y, s, rot)


def ladybug(x, y, s=1.0) -> str:
    b = (circle(0, 0, 50, "#e5333d") + path("M0,-50 L0,50", stroke="#2b2233", sw=5) + circle(-22, -14, 9, "#2b2233") + circle(22, -14, 9, "#2b2233") + circle(-24, 20, 8, "#2b2233") +
         circle(24, 20, 8, "#2b2233") + path("M-30,-40 A50,50 0 0 1 30,-40 L22,-52 Q0,-62 -22,-52 Z", "#2b2233") + eye(-14, -48, 6) + eye(14, -48, 6))
    return g(b, x, y, s)


def bee(x, y, s=1.0) -> str:
    b = (ellipse(-18, -38, 24, 14, "#ffffff", 'opacity="0.8" transform="rotate(-30 -18 -38)"') + ellipse(18, -38, 24, 14, "#ffffff", 'opacity="0.8" transform="rotate(30 18 -38)"') +
         ellipse(0, 0, 44, 34, "#ffd84d") + rect(-14, -32, 10, 64, "#2b2233", 3) + rect(8, -30, 10, 60, "#2b2233", 3) + eye(26, -8, 7) + poly([(-44, 0), (-62, 0), (-44, -6)], "#2b2233"))
    return g(b, x, y, s)


def snail(x, y, s=1.0) -> str:
    b = (path("M-100,50 Q-100,20 -60,20 L90,20 Q110,20 112,-30 Q112,-70 130,-62 Q128,-35 128,10 Q140,50 100,50 Z", "#f1c27d") + circle(-5, -5, 66, "#8e5fd1") + circle(-5, -5, 46, "#b085e8") +
         circle(-5, -5, 26, "#8e5fd1") + path("M112,-30 L112,-90 M128,-30 L146,-84", stroke="#f1c27d", sw=7) + circle(112, -92, 8, "#2b2233") + circle(146, -86, 8, "#2b2233"))
    return g(b, x, y, s)


def crab(x, y, s=1.0) -> str:
    b = (path("M-70,-10 Q-120,-30 -100,-80 Q-70,-70 -66,-40", "#ff6b4a") + path("M70,-10 Q120,-30 100,-80 Q70,-70 66,-40", "#ff6b4a") +
         path("M-60,20 L-110,40 M-55,35 L-100,70 M60,20 L110,40 M55,35 L100,70", stroke="#ff6b4a", sw=12) + ellipse(0, 10, 78, 52, "#ff6b4a") +
         path("M-20,-30 L-20,-58 M20,-30 L20,-58", stroke="#ff6b4a", sw=8) + eye(-20, -62, 12) + eye(20, -62, 12) + smile(0, 18, 20, "#2b2233", 4))
    return g(b, x, y, s)


def octopus(x, y, s=1.0, color="#b66bd6") -> str:
    legs = "".join(path(f"M{lx},40 Q{lx + d},110 {lx + d * 2},95 Q{lx + d * 3},82 {lx + d * 2},140", stroke=color, sw=22) for lx, d in [(-40, -14), (-14, 6), (14, -6), (40, 14)])
    b = legs + path("M-70,40 Q-90,-70 0,-85 Q90,-70 70,40 Z", color) + eye(-24, -10, 15) + eye(24, -10, 15) + smile(0, 22, 18, "#2b2233", 4) + cheeks(-46, 46, 14, 9) + circle(-36, -50, 6, "#ffffff", 'opacity="0.6"')
    return g(b, x, y, s)


def whale(x, y, s=1.0) -> str:
    b = (path("M-150,10 Q-190,-40 -170,-70 Q-130,-60 -110,-20 Z", "#4a90e2") + path("M-190,-62 Q-210,-100 -180,-95 Q-165,-90 -170,-70 Z", "#4a90e2") +
         ellipse(0, 10, 160, 90, "#4a90e2") + path("M-130,50 Q0,110 150,40 Q80,90 -130,50 Z", "#bfe0ff") + eye(85, -18, 14, (3, 0)) + smile(120, 20, 22, "#2b2233", 5) +
         path("M20,-76 L20,-130 M20,-130 Q-10,-150 -20,-135 M20,-130 Q50,-150 60,-135", stroke="#9bd0ff", sw=10) + cheeks(100, 100, 24, 10))
    return g(b, x, y, s)


def pirate_ship(x, y, s=1.0) -> str:
    b = (path("M-150,20 L150,20 Q120,110 80,120 L-80,120 Q-120,110 -150,20 Z", "#8d5a3b") + rect(-150, 8, 300, 18, "#6b4228", 6) + rect(-8, -190, 16, 200, "#6b4228", 4) +
         path("M10,-180 Q120,-120 100,-20 L10,-20 Z", "#fafafa") + path("M-10,-170 Q-100,-120 -90,-30 L-10,-30 Z", "#f4f4fb") + path("M-8,-190 L-8,-240 L50,-222 L-8,-205 Z", "#e5333d") +
         "".join(circle(cx, 62, 11, "#ffd84d") for cx in (-90, -30, 30, 90)) + circle(10, -100, 22, "#2b2233") + path("M-6,-100 h32 M10,-116 v32", stroke="#fff", sw=5))
    return g(b, x, y, s)


def candy(x, y, s=1.0, c1="#ff4f79", c2="#ffffff") -> str:
    b = (poly([(-95, -34), (-50, -10), (-50, 10), (-95, 34)], c1) + poly([(95, -34), (50, -10), (50, 10), (95, 34)], c1) + circle(0, 0, 54, c1) +
         path("M-40,-36 Q-10,-20 -40,20", stroke=c2, sw=12) + path("M0,-52 Q30,-20 0,52", stroke=c2, sw=12) + path("M40,-36 Q70,-10 40,26", stroke=c2, sw=0))
    return g(b, x, y, s)


def lollipop(x, y, s=1.0, c1="#ff4f79", c2="#ffd84d", c3="#6ec6ff") -> str:
    b = rect(-6, 20, 12, 150, "#f4f4fb", 6) + circle(0, -30, 62, c1) + "".join(path(f"M0,-30 m{r * math.cos(a):.0f},{r * math.sin(a):.0f}", stroke=c2, sw=10) for r, a in [(0, 0)]) + \
        path("M0,-30 m-45,0 a45,45 0 1,1 90,0 a45,45 0 1,1 -90,0", stroke=c2, sw=12) + path("M0,-30 m-26,0 a26,26 0 1,1 52,0 a26,26 0 1,1 -52,0", stroke=c3, sw=12) + circle(0, -30, 8, c1)
    return g(b, x, y, s)


def cupcake(x, y, s=1.0, frosting="#ff9ecb", wrapper="#6ec6ff") -> str:
    b = (path("M-60,10 L-48,100 Q0,115 48,100 L60,10 Z", wrapper) + "".join(path(f"M{px},12 L{px * 0.82},104", stroke="#ffffff", sw=5, extra='opacity="0.5"') for px in (-30, 0, 30)) +
         circle(-30, 0, 40, frosting) + circle(30, 0, 40, frosting) + circle(0, -34, 44, frosting) + circle(0, -64, 28, frosting) + circle(0, -98, 14, "#e5333d") +
         "".join(rect(px, py, 18, 7, c, 3, f'transform="rotate({r} {px + 9} {py + 3})"') for px, py, c, r in [(-40, -30, "#ffd84d", 20), (14, -40, "#7ddc6c", -30), (-10, 0, "#ffffff", 50), (22, 8, "#6ec6ff", 10)]))
    return g(b, x, y, s)


def icecream(x, y, s=1.0, c1="#ffb3d1", c2="#fff1b8") -> str:
    b = (poly([(-45, 10), (45, 10), (0, 150)], "#e6b273") + path("M-30,40 L30,60 M-22,75 L22,95 M-14,110 L14,122", stroke="#c88f4f", sw=6) + circle(-28, -2, 38, c1) + circle(28, -2, 38, c1) +
         circle(0, -48, 42, c2) + circle(0, -88, 12, "#e5333d") + eye(-14, -42, 6) + eye(14, -42, 6) + smile(0, -26, 9, "#2b2233", 3))
    return g(b, x, y, s)


def rainbow(cx, cy, r, w=34) -> str:
    cols = ["#ff5a5f", "#ff9f1c", "#ffd84d", "#5fd068", "#4ab3ff", "#8e5fd1"]
    return "".join(path(f"M{cx - r + i * w},{cy} A{r - i * w},{r - i * w} 0 0 1 {cx + r - i * w},{cy}", stroke=c, sw=w + 2) for i, c in enumerate(cols))


def balloon(x, y, s=1.0, color="#ff5a5f") -> str:
    b = path("M0,0 Q-62,-30 -52,-95 Q-40,-150 0,-150 Q40,-150 52,-95 Q62,-30 0,0 Z", color) + poly([(-8, 6), (8, 6), (0, -4)], color) + \
        path("M0,6 Q-14,40 6,70 Q18,95 0,120", stroke="#7a6a7a", sw=3) + ellipse(-22, -100, 9, 22, "#ffffff", 'opacity="0.45" transform="rotate(20 -22 -100)"')
    return g(b, x, y, s)


def car(x, y, s=1.0, color="#e5533d") -> str:
    b = (path("M-130,40 L-120,0 Q-100,-20 -60,-22 L-30,-70 Q-20,-85 0,-85 L60,-85 Q80,-85 90,-70 L120,-22 Q150,-14 150,10 L150,40 Z", color) +
         path("M-24,-60 L-40,-22 L20,-22 L20,-70 Z", "#bfe9ff") + path("M34,-70 L34,-22 L100,-22 L76,-62 Z", "#bfe9ff") + circle(-70, 44, 32, "#2b2233") + circle(70, 44, 32, "#2b2233") +
         circle(-70, 44, 14, "#cfd8dc") + circle(70, 44, 14, "#cfd8dc") + circle(138, 8, 9, "#ffd84d"))
    return g(b, x, y, s)


def hot_air_balloon(x, y, s=1.0) -> str:
    b = (path("M0,0 Q-120,-30 -110,-130 Q-100,-230 0,-240 Q100,-230 110,-130 Q120,-30 0,0 Z", "#ff5a5f") + path("M-40,-4 Q-90,-80 -50,-232 L0,-240 Q-30,-120 -10,0 Z", "#ffd84d") +
         path("M40,-4 Q90,-80 50,-232 L0,-240 Q30,-120 10,0 Z", "#4ab3ff") + path("M-30,6 L-26,60 M30,6 L26,60", stroke="#7a5a3a", sw=4) + rect(-34, 60, 68, 44, "#a8693e", 8))
    return g(b, x, y, s)


def treasure(x, y, s=1.0) -> str:
    b = (rect(-75, -10, 150, 78, "#a8693e", 10) + path("M-75,-10 Q0,-90 75,-10 Z", "#8d5a3b") + rect(-75, 18, 150, 14, "#ffd84d") + rect(-14, 6, 28, 38, "#ffd84d", 6) + circle(0, 22, 6, "#6b4228") +
         circle(-40, -22, 14, "#ffd84d") + circle(-14, -30, 12, "#ffc83d") + circle(20, -26, 14, "#ffd84d") + circle(44, -18, 11, "#ffc83d") + star(-30, -56, 12, "#fff4a8", 10))
    return g(b, x, y, s)


def palm(x, y, s=1.0) -> str:
    leaves = "".join(path(f"M0,-170 Q{dx},{-210 + dy} {dx * 2},{-130 + dy * 2}", stroke="#2fa36b", sw=26) for dx, dy in [(-70, 0), (70, 0), (-110, 30), (110, 30), (0, -30)])
    b = path("M0,0 Q-30,-90 10,-170", stroke="#9a6b3f", sw=26) + leaves + circle(-10, -160, 14, "#7a4e32") + circle(16, -158, 14, "#7a4e32")
    return g(b, x, y, s)


def mushroom(x, y, s=1.0, cap="#e5533d") -> str:
    b = (path("M-22,0 L-26,-60 Q0,-72 26,-60 L22,0 Z", "#f6ead6") + path("M-70,-55 Q0,-140 70,-55 Z", cap) + circle(-30, -85, 9, "#ffffff") + circle(14, -100, 11, "#ffffff") + circle(40, -72, 8, "#ffffff"))
    return g(b, x, y, s)


def fence(x, y, n=8, gap=46, color="#f4e3c1") -> str:
    out = rect(x - 20, y + 25, gap * n + 20, 14, color, 5) + rect(x - 20, y + 62, gap * n + 20, 14, color, 5)
    for i in range(n):
        out += poly([(x + i * gap, y + 100), (x + i * gap + 30, y + 100), (x + i * gap + 30, y + 14), (x + i * gap + 15, y - 6), (x + i * gap, y + 14)], color)
    return out


def barn(x, y, s=1.0) -> str:
    b = (path("M-130,100 L-130,-30 L-90,-110 L90,-110 L130,-30 L130,100 Z", "#d6453d") + path("M-130,-30 L-90,-110 L90,-110 L130,-30 L112,-30 L80,-92 L-80,-92 L-112,-30 Z", "#f4f4fb") +
         rect(-50, 8, 100, 92, "#f4f4fb", 6) + path("M-50,8 L50,100 M50,8 L-50,100", stroke="#d6453d", sw=10) + rect(-50, 8, 100, 92, "none", 6, 'stroke="#d6453d" stroke-width="10"') +
         circle(0, -62, 22, "#fff3d6") + rect(-72, 112, 144, 14, "#7a4e32", 4))
    return g(b, x, y, s)


def bird(x, y, s=1.0, color="#3f9bf5") -> str:
    b = (ellipse(0, 0, 44, 32, color) + circle(34, -18, 24, color) + poly([(54, -22), (78, -14), (54, -8)], "#ffb300") + eye(40, -22, 6) + path("M-44,0 L-80,-16 L-80,20 Z", color) +
         path("M-10,-6 Q-30,-40 -2,-40 Q20,-30 14,-4 Z", "#2f78d4"))
    return g(b, x, y, s)


def kite(x, y, s=1.0, c1="#ff5a5f", c2="#ffd84d", rot=15) -> str:
    b = poly([(0, -80), (50, 0), (0, 90), (-50, 0)], c1) + poly([(0, -80), (50, 0), (0, 0)], c2) + path("M0,90 Q-20,130 10,170 Q30,200 0,240", stroke="#7a6a7a", sw=4) + \
        poly([(-8, 140), (8, 140), (0, 124)], c2) + poly([(-6, 190), (10, 190), (2, 176)], c1)
    return g(b, x, y, s, rot)


def grass(y: float, color: str = "#6fcf6a", h: float = 70) -> str:
    d = f"M0,{y} " + " ".join(f"Q{x + 25},{y - h} {x + 50},{y}" for x in range(0, W, 50)) + f" L{W},{H} L0,{H} Z"
    return path(d, color)


def sparkle_field(rnd: random.Random, n: int, colors=("#ffffff", "#fff4a8", "#bfe9ff")) -> str:
    out = ""
    for _ in range(n):
        x, y, r = rnd.randrange(20, W - 20), rnd.randrange(20, H - 20), rnd.choice([3, 4, 5, 7])
        out += circle(x, y, r, rnd.choice(colors), f'opacity="{rnd.choice([0.5, 0.8, 1])}"')
    return out


# ---- pets ---------------------------------------------------------------------------------------------------

def cat(x, y, s=1.0, body="#f2a65a", belly="#fff1dc", stripe="#d9822b", flip=False) -> str:
    b = (path("M60,80 Q150,70 140,-20 Q135,-60 105,-50", stroke=body, sw=26) + ellipse(0, 55, 70, 78, body) + ellipse(0, 75, 40, 52, belly) +
         "".join(path(f"M{sx},{sy} l{dx},0", stroke=stripe, sw=7) for sx, sy, dx in [(-62, 30, 22), (-64, 55, 24), (42, 30, 22), (44, 55, 24)]) +
         poly([(-62, -38), (-54, -100), (-16, -62)], body) + poly([(62, -38), (54, -100), (16, -62)], body) + poly([(-54, -62), (-50, -88), (-32, -66)], "#ffb3c1") +
         poly([(54, -62), (50, -88), (32, -66)], "#ffb3c1") + circle(0, -18, 66, body) + path("M-12,-80 l0,18 M0,-84 l0,22 M12,-80 l0,18", stroke=stripe, sw=6) +
         eye(-26, -26, 12) + eye(26, -26, 12) + poly([(-7, -6), (7, -6), (0, 4)], "#ff8ea1") + path("M0,4 L0,14 M-14,18 Q0,26 14,18", stroke="#7a5a52", sw=4) +
         path("M-60,-8 l-36,-6 M-60,4 l-38,6 M60,-8 l36,-6 M60,4 l38,6", stroke="#ffffff", sw=3) + cheeks(-44, 44, -2, 10))
    return g(b, x, y, s, flip=flip)


def dog(x, y, s=1.0, body="#c58b5a", ear="#7a4e32", flip=False) -> str:
    b = (path("M70,70 Q140,40 130,-20", stroke=body, sw=22) + ellipse(0, 55, 76, 74, body) + ellipse(0, 75, 42, 50, "#f6e3c9") + ellipse(-48, 110, 22, 16, body) + ellipse(48, 110, 22, 16, body) +
         circle(0, -22, 66, body) + path("M-58,-50 Q-100,-40 -88,10 Q-60,20 -50,-20 Z", ear) + path("M58,-50 Q100,-40 88,10 Q60,20 50,-20 Z", ear) +
         ellipse(0, 0, 38, 30, "#f6e3c9") + ellipse(0, -10, 14, 10, "#2b2233") + eye(-26, -36, 11) + eye(26, -36, 11) + path("M0,-2 L0,10 M-16,14 Q0,26 16,14", stroke="#2b2233", sw=4) +
         path("M-8,22 Q0,48 8,22 Z", "#ff8ea1") + cheeks(-46, 46, -6, 9))
    return g(b, x, y, s, flip=flip)


def hamster(x, y, s=1.0) -> str:
    b = (ellipse(0, 20, 70, 62, "#f6c98d") + ellipse(0, 36, 44, 40, "#fff1dc") + circle(-48, -34, 18, "#f6c98d") + circle(48, -34, 18, "#f6c98d") + circle(-48, -34, 9, "#ffb3c1") + circle(48, -34, 9, "#ffb3c1") +
         circle(0, -10, 58, "#f6c98d") + ellipse(-26, -5, 22, 18, "#ffe3c0") + ellipse(26, -5, 22, 18, "#ffe3c0") + eye(-20, -26, 8) + eye(20, -26, 8) + ellipse(0, -12, 7, 5, "#ff8ea1") +
         path("M0,-8 L0,2 M-8,6 Q0,12 8,6", stroke="#7a5a52", sw=3) + circle(-34, 80, 14, "#f6c98d") + circle(34, 80, 14, "#f6c98d"))
    return g(b, x, y, s)


def fishbowl(x, y, s=1.0) -> str:
    b = (circle(0, 0, 100, "#bfe9ff", 'opacity="0.55"') + path("M-70,30 Q0,60 70,30 L60,70 Q0,95 -60,70 Z", "#f1d58a") + circle(-70, 40, 8, "#ffffff", 'opacity="0.7"') +
         fish(0, -5, 0.5, "#ff8a3d") + path("M-48,70 Q-62,40 -48,10 M-34,70 Q-24,46 -34,24", stroke="#2fa36b", sw=9) + bubble(30, -40, 8) + bubble(44, -64, 5) + path("M-72,-60 Q-90,-30 -84,0", stroke="#ffffff", sw=8, extra='opacity="0.7"') +
         rect(-80, -104, 160, 14, "#9fd0ee", 6))
    return g(b, x, y, s)


def yarn(x, y, s=1.0, color="#ff6f91") -> str:
    b = circle(0, 0, 44, color) + "".join(path(f"M-40,{o} Q0,{o + 22} 40,{o}", stroke="#ffffff", sw=4, extra='opacity="0.5"') for o in (-18, 0, 18)) + path("M30,36 Q90,70 140,50", stroke=color, sw=8)
    return g(b, x, y, s)


def bone(x, y, s=1.0) -> str:
    b = rect(-50, -12, 100, 24, "#f6ead0", 8) + circle(-52, -14, 16, "#f6ead0") + circle(-52, 14, 16, "#f6ead0") + circle(52, -14, 16, "#f6ead0") + circle(52, 14, 16, "#f6ead0")
    return g(b, x, y, s)


def doghouse(x, y, s=1.0) -> str:
    b = (rect(-100, -50, 200, 150, "#e5533d", 8) + poly([(-125, -45), (0, -150), (125, -45)], "#8d5a3b") + path("M-45,100 L-45,10 Q0,-40 45,10 L45,100 Z", "#4a2f22") +
         rect(-30, -90, 60, 22, "#fff3d6", 6) + path("M-100,-10 h200 M-100,30 h200 M-100,70 h200", stroke="#c2402f", sw=5))
    return g(b, x, y, s)


def pets_party() -> str:
    defs = grad("pp", [(0, "#ffe3f1"), (1, "#fff6d6")])
    b = rect(0, 0, 1600, 1200, "url(#pp)")
    for i in range(14):
        b += circle(60 + i * 120, 60 + (i % 3) * 18, 12, ["#ff6f91", "#ffd84d", "#6ec6ff", "#7ddc6c"][i % 4])
    b += path("M0,70 Q400,170 800,70 Q1200,-20 1600,70", stroke="#ff9ecb", sw=6)
    b += poly([(150, 130), (200, 130), (175, 200)], "#ff6f91") + poly([(300, 150), (350, 150), (325, 220)], "#ffd84d") + poly([(1250, 150), (1300, 150), (1275, 220)], "#6ec6ff") + poly([(1400, 125), (1450, 125), (1425, 195)], "#7ddc6c")
    b += rect(0, 880, 1600, 320, "#f4c27a") + rect(0, 870, 1600, 24, "#e0a85a") + balloon(220, 520, 1.3, "#ff5a5f") + balloon(1380, 500, 1.3, "#4ab3ff") + balloon(340, 600, 1.0, "#ffd84d") + balloon(1260, 560, 1.0, "#8e5fd1")
    b += doghouse(1320, 790, 1.2) + dog(560, 800, 1.7) + cat(1010, 850, 1.6, flip=True) + hamster(780, 1010, 1.4) + fishbowl(200, 800, 1.2) + yarn(1000, 1130, 1.2) + bone(360, 1130, 1.2) + bone(1450, 1100, 1.0)
    b += cupcake(640, 1100, 0.7) + star(80, 330, 24, "#ffd84d") + star(1520, 330, 20, "#ff6f91") + butterfly(820, 380, 1.2) + bird(1100, 330, 0.8)
    return svg(b, defs)


def cozy_pets() -> str:
    defs = grad("cz", [(0, "#cfe8ff"), (1, "#eaf6ff")]) + grad("fl", [(0, "#c8905a"), (1, "#a8693e")])
    b = rect(0, 0, 1600, 1200, "url(#cz)") + rect(0, 760, 1600, 440, "url(#fl)")
    for i in range(10):
        b += path(f"M{i * 180},760 L{i * 180 - 60},1200", stroke="#9a5f33", sw=4, extra='opacity="0.5"')
    b += rect(150, 160, 380, 300, "#ffffff", 14) + rect(168, 178, 344, 264, "#9fd8ff", 6) + path("M340,178 V442 M168,310 H512", stroke="#ffffff", sw=12) + cloud(230, 260, 0.6) + sun(430, 250, 38, False)
    b += rect(1050, 150, 400, 200, "#fff3d6", 10) + circle(1130, 250, 46, "#ffb3c1") + circle(1250, 250, 46, "#bfe9ff") + circle(1370, 250, 46, "#c8f0b5") + rect(1030, 350, 440, 16, "#8d5a3b", 6)
    b += ellipse(800, 1000, 480, 120, "#e5533d") + ellipse(800, 985, 440, 96, "#ff7a6b") + cat(660, 880, 1.8) + dog(1010, 900, 1.7, flip=True)
    b += hamster(380, 1050, 1.3) + fishbowl(1380, 650, 1.1) + yarn(240, 1130, 1.3, "#6ec6ff") + bone(1420, 1100, 1.2) + L_plant(1480, 740) + star(800, 540, 28, "#ffd84d") + butterfly(820, 420, 1.3, "#ff9ecb", "#ffd84d")
    return svg(b, defs)


def L_plant(x, y) -> str:
    return (path("M-50,0 L-38,90 Q0,100 38,90 L50,0 Z", "#e5833d").replace('d="', f'transform="translate({x},{y})" d="') +
            g("".join(path(f"M0,0 Q{dx},-70 {dx * 1.6},-{h}", stroke="#2fa36b", sw=18) for dx, h in [(-50, 100), (0, 130), (50, 100)]), x, y, 1))
