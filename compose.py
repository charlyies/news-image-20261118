#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Wednesday 18 November 2026.

Pure Pillow drawing: no network, no randomness, no timestamps. Running
``python3 compose.py`` twice produces a byte-identical entry.png.
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/noto/"
SANS_BOLD = FONT_DIR + "NotoSans-Bold.ttf"
SANS_REG = FONT_DIR + "NotoSans-Regular.ttf"
SERIF_BOLD = FONT_DIR + "NotoSerif-Bold.ttf"
SERIF_REG = FONT_DIR + "NotoSerif-Regular.ttf"
SERIF_ITALIC = FONT_DIR + "NotoSerif-Italic.ttf"

PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 32, 44)
RED_DARK = (140, 22, 32)
GREY = (96, 92, 84)
RULE = (60, 56, 48)

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill, spacing=0):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + spacing


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def flame_tongue(layer, cx, base_y, width, height, lean):
    """One layered teardrop flame: red outer, orange middle, yellow core."""
    d = ImageDraw.Draw(layer)

    def tongue(w, h, colour):
        pts = []
        steps = 14
        for i in range(steps + 1):
            t = i / steps  # 0 at base, 1 at tip
            wob = math.sin(t * 5.1 + lean) * 0.16 * w
            half = (w / 2) * math.sin(math.pi * min(1.0, t * 1.15)) ** 0.7
            half = max(half, 0.5)
            x = cx + lean * t * 14 + wob
            pts.append((x - half, base_y - t * h))
        for i in range(steps, -1, -1):
            t = i / steps
            wob = math.sin(t * 4.3 + lean + 1.7) * 0.16 * w
            half = (w / 2) * math.sin(math.pi * min(1.0, t * 1.15)) ** 0.7
            half = max(half, 0.5)
            x = cx + lean * t * 14 + wob
            pts.append((x + half, base_y - t * h))
        d.polygon(pts, fill=colour)

    tongue(width, height, (226, 44, 22, 235))
    tongue(width * 0.66, height * 0.72, (244, 124, 26, 240))
    tongue(width * 0.38, height * 0.48, (252, 210, 74, 245))


def smoke_puff(layer, x, y, r, colour):
    d = ImageDraw.Draw(layer)
    d.ellipse((x - r, y - r, x + r, y + r), fill=colour)


def draw_lead_scene():
    """Night over the Gulf: burning tanker, intact tanker, jets, drones."""
    sw, sh = 972, 314
    scene = Image.new("RGB", (sw, sh), (8, 15, 40))
    horizon = 196
    # --- sky gradient: deep navy down to a burning orange horizon ---
    stops = [(0.0, (7, 13, 38)), (0.45, (34, 24, 58)),
             (0.78, (122, 48, 44)), (1.0, (228, 108, 34))]
    for y in range(horizon + 1):
        t = y / horizon
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                f = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
                col = lerp(c0, c1, f)
                break
        else:
            col = stops[-1][1]
        ImageDraw.Draw(scene).line([(0, y), (sw, y)], fill=col)
    # --- sea ---
    sea = ImageDraw.Draw(scene)
    for y in range(horizon, sh):
        f = (y - horizon) / (sh - horizon)
        sea.line([(0, y), (sw, y)], fill=lerp((16, 34, 66), (6, 12, 30), f))
    # warm glow band on the water under the horizon
    glow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i, (r, a) in enumerate([(150, 46), (110, 70), (70, 96), (36, 130)]):
        gd.ellipse((300 - r, horizon - 26 - i * 2, 300 + r,
                    horizon + 34 + i * 3), fill=(238, 122, 36, a))
    scene = Image.alpha_composite(scene.convert("RGBA"), glow)
    d = ImageDraw.Draw(scene)

    # --- stars (fixed positions) ---
    stars = [(40, 26, 2), (96, 58, 1), (150, 20, 2), (210, 44, 1),
             (268, 16, 2), (330, 52, 1), (392, 24, 2), (448, 66, 1),
             (512, 18, 2), (566, 46, 1), (624, 22, 2), (688, 56, 1),
             (742, 18, 2), (806, 48, 1), (862, 24, 2), (920, 54, 1),
             (60, 96, 1), (180, 84, 2), (300, 100, 1), (430, 88, 1),
             (560, 96, 2), (660, 84, 1), (780, 100, 2), (900, 88, 1),
             (120, 130, 1), (250, 142, 1), (480, 128, 2), (700, 138, 1),
             (840, 128, 1), (940, 140, 2)]
    for x, y, r in stars:
        d.ellipse((x - r, y - r, x + r, y + r), fill=(235, 238, 255))

    # --- layered clouds, dark above, fire-lit near the horizon ---
    clouds = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    cd = ImageDraw.Draw(clouds)
    for (cx, cy, rx, ry, col) in [
            (180, 70, 150, 16, (30, 34, 66, 110)),
            (330, 78, 120, 13, (30, 34, 66, 100)),
            (620, 60, 170, 15, (28, 30, 60, 110)),
            (830, 74, 130, 13, (28, 30, 60, 100)),
            (120, 150, 140, 12, (52, 38, 62, 120)),
            (480, 158, 160, 12, (62, 40, 56, 120)),
            (820, 150, 150, 12, (52, 38, 62, 120)),
            (260, 178, 170, 10, (150, 74, 40, 130)),
            (640, 182, 180, 10, (170, 84, 38, 130)),
            (920, 180, 120, 9, (150, 74, 40, 120))]:
        cd.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=col)
    scene = Image.alpha_composite(scene, clouds)
    d = ImageDraw.Draw(scene)

    # --- missile trails arcing up from the sea ---
    def arc(x0, y0, x1, y1, lift, colour):
        pts = []
        for i in range(21):
            t = i / 20
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t - lift * 4 * t * (1 - t)
            pts.append((x, y))
        d.line(pts, fill=colour, width=3)
        d.ellipse((x1 - 4, y1 - 4, x1 + 4, y1 + 4), fill=(255, 240, 190))
        d.ellipse((x1 - 8, y1 - 8, x1 + 8, y1 + 8),
                  outline=(255, 190, 90), width=1)

    arc(120, horizon - 6, 268, 96, 60, (255, 214, 130))
    arc(880, horizon - 4, 760, 70, 52, (255, 214, 130))

    # --- fighter jets with pale contrails ---
    def jet(x, y, s, flip):
        pts = [(x, y), (x - 26 * s * flip, y + 5 * s),
               (x - 20 * s * flip, y + 2 * s), (x - 30 * s * flip, y - 6 * s),
               (x - 8 * s * flip, y - 3 * s), (x + 4 * s * flip, y - 9 * s),
               (x + 2 * s * flip, y - 2 * s)]
        d.polygon(pts, fill=(24, 26, 34))
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 220, 160))

    contrail = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    cd = ImageDraw.Draw(contrail)
    cd.line([(706, 66), (560, 40)], fill=(235, 238, 250, 150), width=2)
    cd.line([(706, 70), (566, 52)], fill=(235, 238, 250, 110), width=2)
    cd.line([(842, 108), (730, 88)], fill=(235, 238, 250, 140), width=2)
    scene = Image.alpha_composite(scene, contrail)
    d = ImageDraw.Draw(scene)
    jet(712, 66, 1.0, 1)
    jet(848, 108, 0.85, 1)

    # --- small drone silhouettes ---
    for (x, y, s) in [(330, 92, 1.0), (402, 62, 0.8), (540, 118, 0.9)]:
        d.rectangle((x - 7 * s, y - 2, x + 7 * s, y + 2), fill=(20, 20, 26))
        d.line([(x - 9 * s, y - 5), (x + 9 * s, y - 5)], fill=(200, 200, 210), width=1)
        d.ellipse((x - 1, y - 4, x + 1, y - 2), fill=(255, 120, 90))

    # --- firelight reflected on the water ---
    refl = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    rd = ImageDraw.Draw(refl)
    for (x, w, a) in [(252, 6, 80), (282, 8, 95), (314, 5, 70),
                      (346, 7, 85), (230, 4, 60), (370, 4, 60)]:
        rd.polygon([(x - w, horizon + 4), (x + w, horizon + 4),
                    (x + w * 0.55, sh - 6), (x - w * 0.55, sh - 6)],
                   fill=(238, 122, 36, a))
    scene = Image.alpha_composite(scene, refl)
    d = ImageDraw.Draw(scene)

    # --- burning tanker (left), hull, containers, lit superstructure ---
    hull_y = horizon + 16
    d.polygon([(96, hull_y), (470, hull_y), (452, hull_y + 30),
               (120, hull_y + 30)], fill=(14, 15, 20))
    d.polygon([(452, hull_y), (470, hull_y), (452, hull_y + 30)],
              fill=(26, 22, 20))
    d.rectangle((96, hull_y - 4, 470, hull_y), fill=(58, 26, 22))
    # deck containers, some scorched
    conts = [(120, 26, (52, 66, 88)), (150, 26, (74, 58, 52)),
             (180, 22, (48, 58, 44)), (210, 26, (88, 62, 44)),
             (240, 22, (58, 58, 66)), (380, 26, (52, 66, 88)),
             (410, 22, (74, 58, 52)), (436, 24, (48, 58, 44))]
    for (x, h, col) in conts:
        d.rectangle((x, hull_y - h, x + 26, hull_y - 4), fill=col)
        d.rectangle((x, hull_y - h, x + 26, hull_y - 4),
                    outline=(20, 20, 24), width=1)
    # superstructure with lit windows
    d.rectangle((288, hull_y - 52, 352, hull_y - 4), fill=(214, 208, 192))
    d.rectangle((288, hull_y - 52, 352, hull_y - 46), fill=(150, 40, 30))
    for wy in (hull_y - 40, hull_y - 28, hull_y - 16):
        for wx in (296, 312, 328, 344):
            d.rectangle((wx, wy, wx + 6, wy + 5), fill=(255, 206, 92))
    # funnel
    d.rectangle((358, hull_y - 44, 372, hull_y - 4), fill=(178, 32, 44))
    d.rectangle((358, hull_y - 44, 372, hull_y - 38), fill=(30, 30, 34))

    # flames above the deck, between the containers
    flames = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    for (cx, w, h, lean) in [(196, 52, 96, 0.4), (232, 64, 122, -0.3),
                             (268, 56, 104, 0.5), (308, 44, 84, -0.5),
                             (392, 48, 88, 0.3)]:
        flame_tongue(flames, cx, hull_y - 4, w, h, lean)
    # flying embers
    ed = ImageDraw.Draw(flames)
    embers = [(180, 96, 3), (210, 72, 2), (246, 60, 3), (282, 78, 2),
              (318, 64, 3), (352, 88, 2), (392, 76, 2), (226, 44, 2),
              (300, 40, 2), (410, 92, 2)]
    for (x, y, r) in embers:
        ed.ellipse((x - r, y - r, x + r, y + r), fill=(255, 190, 60, 240))
        ed.ellipse((x - r - 2, y - r - 2, x + r + 2, y + r + 2),
                   outline=(255, 120, 40, 160), width=1)
    scene = Image.alpha_composite(scene, flames)
    d = ImageDraw.Draw(scene)
    # three-shade smoke plume drifting up and right with the wind
    smoke = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    plume = [(238, 76, 13, (96, 94, 100, 70)),
             (256, 66, 16, (82, 80, 86, 75)),
             (274, 56, 18, (110, 108, 114, 70)),
             (292, 48, 15, (82, 80, 86, 80)),
             (310, 40, 19, (110, 108, 114, 70)),
             (330, 34, 16, (82, 80, 86, 75)),
             (350, 28, 18, (110, 108, 114, 65)),
             (372, 24, 15, (82, 80, 86, 70)),
             (394, 20, 17, (110, 108, 114, 65)),
             (416, 18, 14, (82, 80, 86, 70)),
             (438, 18, 15, (110, 108, 114, 60)),
             (460, 20, 12, (82, 80, 86, 65)),
             (300, 62, 12, (96, 94, 100, 60)),
             (340, 48, 12, (96, 94, 100, 55))]
    for (x, y, r, col) in plume:
        smoke_puff(smoke, x, y, r, col)
    scene = Image.alpha_composite(scene, smoke)
    d = ImageDraw.Draw(scene)

    # --- intact tanker (right), lit superstructure, red mast light ---
    hx = 640
    hy = horizon + 22
    d.polygon([(hx, hy), (930, hy), (912, hy + 26), (hx + 18, hy + 26)],
              fill=(18, 19, 26))
    d.rectangle((hx, hy - 3, 930, hy), fill=(70, 32, 26))
    for (x, h, col) in [(hx + 20, 20, (52, 66, 88)), (hx + 48, 18, (74, 58, 52)),
                        (hx + 76, 22, (48, 58, 44)), (hx + 104, 18, (88, 62, 44)),
                        (hx + 132, 20, (58, 58, 66))]:
        d.rectangle((x, hy - h, x + 24, hy - 3), fill=col)
    d.rectangle((hx + 168, hy - 46, hx + 222, hy - 3), fill=(206, 200, 184))
    for wy in (hy - 36, hy - 25, hy - 14):
        for wx in (hx + 176, hx + 190, hx + 204):
            d.rectangle((wx, wy, wx + 6, wy + 5), fill=(255, 206, 92))
    d.rectangle((hx + 228, hy - 38, hx + 240, hy - 3), fill=(178, 32, 44))
    d.ellipse((hx + 232, hy - 48, hx + 238, hy - 42), fill=(255, 60, 50))
    # faint wake behind the intact tanker
    for i in range(5):
        d.line([(hx - 10 - i * 14, hy + 8 + i * 4),
                (hx + 60, hy + 8 + i * 4)], fill=(70, 100, 140), width=1)

    # thin dark frame around the scene
    d.rectangle((0, 0, sw - 1, sh - 1), outline=(20, 20, 24), width=2)
    return scene


def thumb_bridge():
    """Kerch Bridge: dusk sky, a broken span, the fallen road in the strait."""
    w, h = 170, 164
    img = Image.new("RGB", (w, h), (44, 40, 66))
    d = ImageDraw.Draw(img)
    for y in range(110):
        d.line([(0, y), (w, y)], fill=lerp((52, 44, 84), (214, 120, 52), y / 110))
    for y in range(110, h):
        d.line([(0, y), (w, y)], fill=lerp((30, 52, 84), (16, 26, 48), (y - 110) / 54))
    d.ellipse((132, 18, 158, 44), fill=(250, 196, 110))
    # bridge deck with a gap in the middle
    d.rectangle((0, 78, 62, 86), fill=(30, 30, 36))
    d.rectangle((108, 78, w, 86), fill=(30, 30, 36))
    d.line([(0, 78), (62, 78)], fill=(120, 120, 130), width=1)
    d.line([(108, 78), (w, 78)], fill=(120, 120, 130), width=1)
    # pylons and cables
    for px in (30, 140):
        d.rectangle((px - 2, 40, px + 2, 110), fill=(24, 24, 30))
        d.line([(px, 40), (px - 26, 78)], fill=(150, 150, 160), width=1)
        d.line([(px, 40), (px + 26, 78)], fill=(150, 150, 160), width=1)
    # fallen road section sliding into the water
    d.polygon([(64, 80), (102, 80), (92, 118), (70, 110)], fill=(40, 38, 44))
    d.polygon([(64, 80), (102, 80), (100, 86), (64, 86)], fill=(90, 88, 96))
    # blast glow and a thin smoke wisp at the break
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse((62, 58, 110, 96), fill=(250, 150, 50, 150))
    od.ellipse((74, 44, 98, 66), fill=(90, 88, 96, 140))
    od.ellipse((84, 30, 106, 50), fill=(120, 118, 124, 120))
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    d = ImageDraw.Draw(img)
    for x in (20, 60, 100, 140):
        d.line([(x, 118), (x + 24, 118)], fill=(120, 150, 190), width=1)
    d.rectangle((0, 0, w - 1, h - 1), outline=(20, 20, 24), width=2)
    return img


def thumb_summit():
    """Shenzhen skyline at sunrise with three flags on poles."""
    w, h = 170, 164
    img = Image.new("RGB", (w, h), (214, 228, 240))
    d = ImageDraw.Draw(img)
    for y in range(120):
        d.line([(0, y), (w, y)], fill=lerp((168, 196, 226), (250, 214, 170), y / 120))
    d.ellipse((18, 16, 52, 50), fill=(248, 190, 90))
    d.ellipse((18, 16, 52, 50), outline=(240, 160, 60), width=2)
    # skyline, one tall tapered tower in the middle
    towers = [(0, 78, 22, 120), (24, 62, 18, 120), (44, 88, 20, 120),
              (66, 52, 26, 120), (94, 70, 20, 120), (116, 58, 24, 120),
              (142, 84, 28, 120)]
    for (x, top, tw, bot) in towers:
        d.rectangle((x, top, x + tw, bot), fill=(52, 62, 84))
    d.polygon([(72, 52), (86, 30), (92, 52)], fill=(40, 48, 70))
    d.rectangle((84, 22, 88, 32), fill=(40, 48, 70))
    for (x, y) in [(8, 92), (30, 76), (50, 100), (72, 66), (100, 84),
                   (122, 72), (150, 96), (76, 40)]:
        d.rectangle((x, y, x + 4, y + 5), fill=(255, 214, 120))
    d.rectangle((0, 120, w, h), fill=(74, 96, 66))
    d.rectangle((0, 120, w, 126), fill=(52, 70, 50))
    # three flags on poles in front of the skyline
    for (x, col1, col2) in [(28, (200, 30, 30), None),
                            (84, (240, 240, 240), (30, 60, 160)),
                            (140, (200, 30, 30), (255, 220, 80))]:
        d.rectangle((x, 96, x + 2, 126), fill=(40, 40, 44))
        d.polygon([(x + 2, 96), (x + 20, 100), (x + 2, 106)], fill=col1)
        if col2 is not None:
            d.polygon([(x + 2, 100), (x + 20, 100), (x + 2, 106)], fill=col2)
    d.rectangle((0, 0, w - 1, h - 1), outline=(20, 20, 24), width=2)
    return img


def thumb_senate():
    """The U.S. Capitol dome with a bold 56-seat badge."""
    w, h = 170, 164
    img = Image.new("RGB", (w, h), (30, 52, 92))
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp((36, 62, 110), (18, 30, 64), y / h))
    for (x, y, r) in [(20, 24, 1), (60, 14, 2), (110, 28, 1), (150, 16, 2),
                      (140, 44, 1), (36, 52, 1)]:
        d.ellipse((x - r, y - r, x + r, y + r), fill=(230, 234, 250))
    # capitol dome, white against the blue night
    d.rectangle((52, 118, 118, 132), fill=(232, 230, 222))
    d.rectangle((44, 110, 126, 120), fill=(238, 236, 228))
    d.rectangle((38, 102, 132, 112), fill=(244, 242, 234))
    d.pieslice((52, 62, 118, 128), 180, 360, fill=(244, 242, 234))
    d.rectangle((82, 44, 88, 64), fill=(244, 242, 234))
    d.ellipse((80, 38, 90, 48), fill=(244, 242, 234))
    d.line([(85, 34), (85, 22)], fill=(244, 242, 234), width=2)
    d.polygon([(85, 22), (97, 26), (85, 30)], fill=(200, 40, 44))
    for x in (58, 72, 86, 100, 114):
        d.rectangle((x, 116, x + 4, 124), fill=(60, 70, 90))
    d.rectangle((0, 132, w, h), fill=(22, 34, 54))
    # badge with the seat count
    d.ellipse((104, 96, 164, 156), fill=(178, 32, 44))
    d.ellipse((104, 96, 164, 156), outline=(247, 242, 231), width=3)
    f56 = font(SANS_BOLD, 34)
    txt = "56"
    tw = d.textlength(txt, font=f56)
    d.text((134 - tw / 2, 106), txt, font=f56, fill=(255, 255, 255))
    fcap = font(SANS_BOLD, 11)
    cap = "SEATS"
    cw = d.textlength(cap, font=fcap)
    d.text((134 - cw / 2, 140), cap, font=fcap, fill=(255, 226, 200))
    d.rectangle((0, 0, w - 1, h - 1), outline=(20, 20, 24), width=2)
    return img


def thumb_ebola():
    """Spiky virus shapes over a rising case chart, with a medical cross."""
    w, h = 170, 164
    img = Image.new("RGB", (w, h), (244, 238, 226))
    d = ImageDraw.Draw(img)
    # pale chart grid
    for y in (40, 76, 112):
        d.line([(14, y), (156, y)], fill=(214, 206, 190), width=1)
    # rising red case line with an arrowhead
    pts = [(16, 128), (48, 112), (78, 96), (106, 66), (138, 34)]
    d.line(pts, fill=(178, 32, 44), width=4)
    for (x, y) in pts:
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(178, 32, 44))
    d.polygon([(138, 34), (124, 34), (138, 48)], fill=(178, 32, 44))

    def virus(cx, cy, r, col):
        for k in range(10):
            ang = k * math.pi / 5
            x0 = cx + int(math.cos(ang) * r)
            y0 = cy + int(math.sin(ang) * r)
            x1 = cx + int(math.cos(ang) * (r + 7))
            y1 = cy + int(math.sin(ang) * (r + 7))
            d.line([(x0, y0), (x1, y1)], fill=col, width=2)
            d.ellipse((x1 - 2, y1 - 2, x1 + 2, y1 + 2), fill=col)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        d.ellipse((cx - r + 4, cy - r + 4, cx - r + 10, cy - r + 10),
                  fill=(255, 120, 100))

    virus(40, 52, 15, (178, 32, 44))
    virus(118, 118, 12, (140, 22, 32))
    virus(150, 66, 9, (200, 70, 50))
    # medical cross badge, top left
    d.rectangle((8, 8, 34, 34), fill=(255, 255, 255),
                outline=(178, 32, 44), width=2)
    d.rectangle((18, 13, 24, 29), fill=(178, 32, 44))
    d.rectangle((13, 18, 29, 24), fill=(178, 32, 44))
    d.rectangle((0, 0, w - 1, h - 1), outline=(20, 20, 24), width=2)
    return img


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    cx = W // 2

    # --- masthead ---
    f_mast = font(SERIF_BOLD, 62)
    d.text((cx - d.textlength("THE WORLD TODAY", font=f_mast) / 2, 12),
           "THE WORLD TODAY", font=f_mast, fill=INK)
    d.line([(26, 90), (998, 90)], fill=RULE, width=2)
    d.line([(26, 94), (998, 94)], fill=RULE, width=1)

    # --- red date bar ---
    d.rectangle((26, 102, 998, 134), fill=RED)
    f_date = font(SANS_BOLD, 21)
    date_txt = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text((cx - d.textlength(date_txt, font=f_date) / 2, 108),
           date_txt, font=f_date, fill=(255, 255, 255))

    # --- lead scene ---
    img.paste(draw_lead_scene(), (26, 142))
    d = ImageDraw.Draw(img)

    # --- caption under the scene ---
    f_cap = font(SERIF_ITALIC, 16)
    cap = "A tanker burns in the Gulf of Oman after U.S. strikes on Iran."
    d.text((cx - d.textlength(cap, font=f_cap) / 2, 460),
           cap, font=f_cap, fill=GREY)

    # --- lead headline, two lines ---
    f_head = font(SANS_BOLD, 40)
    head_lines = wrap(d, "U.S. STRIKES IRAN AS GULF WAR ESCALATES", f_head, 960)
    y = 486
    for line in head_lines:
        d.text((cx - d.textlength(line, font=f_head) / 2, y),
               line, font=f_head, fill=INK)
        y += 44

    # --- lead deck, two lines ---
    f_deck = font(SERIF_REG, 22)
    deck = ("Jets hit a missile site on Qeshm Island and sink five tankers; "
            "Tehran answers with drones over Bahrain and Kuwait and "
            "missiles at a U.S. base in Jordan.")
    deck_lines = wrap(d, deck, f_deck, 940)
    y = 578
    for line in deck_lines:
        d.text((cx - d.textlength(line, font=f_deck) / 2, y),
               line, font=f_deck, fill=(40, 38, 34))
        y += 28

    d.line([(26, 646), (998, 646)], fill=RULE, width=1)

    # --- secondary grid, 2 x 2 ---
    stories = [
        ("UKRAINE", "KERCH BRIDGE HIT AGAIN",
         "Ukraine strikes the bridge for a second day; part of the road "
         "span falls into the strait.",
         thumb_bridge()),
        ("CHINA", "THREE LEADERS MEET IN SHENZHEN",
         "Xi hosts the APEC summit as Putin and Trump arrive for talks "
         "this week.",
         thumb_summit()),
        ("U.S. POLITICS", "DEMOCRATS TAKE 56 SENATE SEATS",
         "Mary Peltola wins Alaska's Senate race, unseating Dan Sullivan.",
         thumb_senate()),
        ("HEALTH", "EBOLA CASES DOUBLE IN CONGO",
         "The outbreak passes 11,000 cases and 5,400 deaths in three "
         "months, the U.N. says.",
         thumb_ebola()),
    ]
    f_kick = font(SANS_BOLD, 13)
    f_sub = font(SANS_BOLD, 20)
    f_sdeck = font(SERIF_REG, 16)
    cell_w = 474
    for i, (kicker, headline, sdeck, thumb) in enumerate(stories):
        col = i % 2
        row = i // 2
        x0 = 26 + col * (cell_w + 24)
        y0 = 656 + row * 164
        img.paste(thumb, (x0, y0))
        tx = x0 + 182
        tw = 292
        d.text((tx, y0 + 2), kicker, font=f_kick, fill=RED_DARK)
        y = y0 + 22
        for line in wrap(d, headline, f_sub, tw):
            d.text((tx, y), line, font=f_sub, fill=INK)
            y += 24
        y += 4
        for line in wrap(d, sdeck, f_sdeck, tw):
            d.text((tx, y), line, font=f_sdeck, fill=(52, 50, 46))
            y += 20

    # --- footer ---
    d.line([(26, 990), (998, 990)], fill=RULE, width=1)
    f_foot = font(SANS_REG, 13)
    foot = "THE WORLD TODAY  ·  WEDNESDAY 18 NOVEMBER 2026  ·  FIVE STORIES FROM ONE DAY AROUND THE WORLD"
    d.text((cx - d.textlength(foot, font=f_foot) / 2, 996),
           foot, font=f_foot, fill=GREY)

    img.save(OUT, format="PNG")


if __name__ == "__main__":
    build()
