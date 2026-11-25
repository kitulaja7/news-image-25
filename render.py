#!/usr/bin/env python3
"""Render the news-image-20261125 front page (1024x1024).

Dev-time renderer (PIL). The graded program is main.py, which only copies
the committed entry.png byte-for-byte (stdlib only).

NEW APPROACH (from the news-24 round-3 bedah): the dense newspaper frame is
kept, but every FEATURE illustration is BRIGHT -- pale sky, saturated colour,
ONE big focus object, light background. No dark night scenes as feature art.
Every illustration must still read at 512px.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def f_serif(size, bold=True):
    return ImageFont.truetype(
        os.path.join(FL, "LiberationSerif-Bold.ttf" if bold else "LiberationSerif-Regular.ttf"),
        size)


def f_serif_it(size):
    return ImageFont.truetype(os.path.join(FL, "LiberationSerif-Italic.ttf"), size)


def f_sans(size, bold=False):
    return ImageFont.truetype(
        os.path.join(FD, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)


def f_cond(size, bold=True):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/noto/NotoSansDisplay-CondensedBold.ttf"
        if bold else
        "/usr/share/fonts/truetype/noto/NotoSansDisplay-Condensed.ttf",
        size)


# ---------------------------------------------------------------- palette
PAPER = (250, 246, 235)      # warm newsprint, light
INK = (18, 18, 18)
NAVY = (16, 32, 64)
RED = (178, 24, 24)
RED_DK = (140, 16, 16)
GREEN = (18, 120, 60)
GREEN_CHIP = (16, 110, 55)
GOLD = (176, 124, 20)
TEAL = (10, 110, 110)
PURPLE = (104, 52, 140)
GREY = (90, 90, 90)
LINE = (200, 192, 176)
SKY = (198, 226, 244)       # pale daylight sky for illustrations
SKY2 = (214, 236, 248)
SEA = (64, 164, 205)        # bright turquoise sea
SEA_DK = (38, 130, 180)

CHIP_FILL = {
    "CONFIRMED": (16, 110, 55),
    "OFFICIAL": (176, 124, 20),
    "REPORTED": (10, 110, 110),
    "CLAIM": (178, 24, 24),
    "ONGOING": (104, 52, 140),
}

# ---------------------------------------------------------------- text helpers
def tw(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]


def th(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[3] - b[1]


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, font, x, y, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(font.size * 1.22)
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=font, fill=fill)
    return len(lines)


def chip(draw, x, y, label, h=15):
    """Verification chip: white bold text on colour. Returns width used."""
    font = f_sans(9, bold=True)
    w = tw(draw, label, font) + 10
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=CHIP_FILL[label])
    draw.text((x + 5, y + 3), label, font=font, fill=(255, 255, 255))
    return w


def num_badge(draw, x, y, n, d=20):
    draw.ellipse([x, y, x + d, y + d], fill=RED)
    f = f_sans(11, bold=True)
    t = str(n)
    draw.text((x + (d - tw(draw, t, f)) / 2, y + 4), t, font=f, fill=(255, 255, 255))

# ================================================================ DATA
# All stories happened, or were first reported, on Wed 25 Nov 2026 (UTC).
# Sources named per story. Numbers checked against wire reports.

FEATURES = [
    dict(
        num=1, region="STRAIT OF HORMUZ", beat="WAR AT SEA", chip="CLAIM",
        banner="2 TANKERS HIT", art="tanker",
        headline="Two tankers hit mines in Hormuz",
        body=("Iran's Revolutionary Guard says two tankers struck naval mines "
              "and caught fire early Wednesday. The maritime centre calls "
              "the claim unconfirmed."),
        src="IRGC \u00b7 JMIC \u00b7 Al Jazeera",
    ),
    dict(
        num=2, region="JIUQUAN, CHINA", beat="SPACE", chip="CONFIRMED",
        banner="PAKISTAN'S FIRST", art="rocket",
        headline="Shenzhou-24 docks; Pakistan's first astronaut in orbit",
        body=("China launches Shenzhou-24 with two Chinese and one Pakistani "
              "astronaut aboard. The crew docks with Tiangong hours later."),
        src="Xinhua \u00b7 AP \u00b7 CMSA",
    ),
    dict(
        num=3, region="SAMARA, RUSSIA", beat="WAR \u00b7 ENERGY", chip="CONFIRMED",
        banner="2 REFINERIES HIT", art="refinery",
        headline="Ukraine drones hit two Russian refineries",
        body=("Overnight strikes set the Syzran and Kuibyshev refineries "
              "ablaze, 800 km inside Russia. One killed; 145 drones downed."),
        src="Kyiv Independent \u00b7 Reuters \u00b7 AP",
    ),
]

TILES = [
    dict(num=4, region="RAS TANURA", beat="WAR \u00b7 OIL", chip="CLAIM",
         headline="Houthis say they hit Ras Tanura refinery",
         body="Attack causes fires at Saudi Arabia's biggest refinery, the group says.",
         src="Houthi spokesman \u00b7 AP", art="flame"),
    dict(num=5, region="CARTAGENA", beat="CRIME", chip="CONFIRMED",
         headline="All hostages freed in supermarket siege",
         body="Forces storm the store at dawn; one captor killed, all freed.",
         src="Colombia president \u00b7 AP", art="freed"),
    dict(num=6, region="GAZA", beat="WAR", chip="CONFIRMED",
         headline="Israel kills Hamas security colonel",
         body="Abuelouf, his wife and two children die in an al-Shati strike.",
         src="Gaza medics \u00b7 AP", art=None),
    dict(num=7, region="SOLOMON ISLANDS", beat="DIPLOMACY", chip="OFFICIAL",
         headline="Solomons sign treaty with Australia",
         body="Canberra deal bars any foreign military base on the islands.",
         src="Canberra \u00b7 AP", art="flags"),
    dict(num=8, region="MARKETS", beat="STOCKS", chip="CONFIRMED",
         headline="KOSPI plunges 6.16%; Dow tops 50,000",
         body="Asia tumbles as chips slide; Wall St hits a milestone.",
         src="AP \u00b7 Reuters", art="chart"),
    dict(num=9, region="SUDAN", beat="WAR", chip="REPORTED",
         headline="RSF drone strikes kill 19 civilians",
         body="Two cities hit; 20 more wounded, rights lawyers say.",
         src="Emergency Lawyers \u00b7 AP", art=None),
    dict(num=10, region="KYIV", beat="AID", chip="REPORTED",
         headline="Ukraine needs \u20ac115bn aid for 2027",
         body="Zelensky's ask as the US pauses Patriot missile supplies.",
         src="Kyiv \u00b7 Reuters", art="euro"),
    dict(num=11, region="UNITED STATES", beat="IMMIGRATION", chip="CONFIRMED",
         headline="Abrego Garcia leaves US for Spain",
         body="Deportation symbol ends a 20-month legal fight, flies out.",
         src="AP \u00b7 Reuters", art="plane"),
    dict(num=12, region="WINDSOR, UK", beat="CRIME", chip="OFFICIAL",
         headline="Two charged over royal break-in",
         body="Men charged after a break-in at Prince William's home.",
         src="UK police \u00b7 AP", art=None),
    dict(num=13, region="UNITED STATES", beat="TECH \u00b7 EARNINGS", chip="OFFICIAL",
         headline="Dell posts record quarter as AI booms",
         body="Revenue up 103%; AI server sales hit $22bn, up 291%.",
         src="Dell \u00b7 Reuters", art="dollar"),
]

ALSO = [
    (14, "Putin vows retaliation for refinery strikes", "Reuters"),
    (15, "Zaporizhzhia nuclear plant loses external power", "IAEA"),
    (16, "Odesa strike kills 2, injures 3; Kyiv flats hit", "AP"),
    (17, "Libya vows retaliation; two officers died in Benghazi", "LNA"),
    (18, "Merz: Russia is \u201cescalating\u201d threats to Europe", "AP"),
    (19, "Norway to give Ukraine at least $7bn in 2027", "Reuters"),
    (20, "Pope Leo XIV: COP31 failure a concern", "AP"),
    (21, "Eurozone inflation rises to 4.0%", "Eurostat"),
    (22, "Australia inflation rises to 4.9%", "ABS"),
    (23, "Amazon buys Decart to help its chips rival Nvidia", "Reuters"),
    (24, "Anthropic shares fall below IPO price; $1tn gone", "Bloomberg"),
    (25, "Amazon: hackers' AI agents broke into a university server", "AP"),
    (26, "Roche breast cancer pill wins second FDA approval", "Reuters"),
    (27, "EasyJet profit falls 89% as fuel costs soar", "Reuters"),
    (28, "China sentences official to death for spying", "AP"),
    (29, "Bangladesh raises garment minimum wage after protests", "AP"),
    (30, "North Korea demands Switzerland close new office", "AP"),
    (31, "US ready to slap tariffs on China, EU over subsidies", "AP sources"),
    (32, "Malaysia to repatriate 6,803 Myanmar nationals", "AP"),
    (33, "DR Congo rebels retreat after heavy clashes", "Reuters"),
    (34, "Iran vows \u201call available means\u201d to counter US blockade", "IRNA"),
    (35, "Pentagon rebukes Canada over defence, F-35 review", "AP"),
    (36, "Quasar found 630m years after the Big Bang", "Scientists"),
    (37, "Pope Francis' private diary reveals spiritual crisis", "AP"),
    (38, "AP editor Ellen Nimmons dies at 78", "AP"),
]

STATS = [
    ("2", "tankers hit mines in Hormuz"),
    ("\u20ac115bn", "Ukraine aid needed for 2027"),
    ("-6.16%", "KOSPI plunge in a day"),
    ("19", "civilians killed in Sudan strikes"),
    ("1", "Pakistan's first astronaut"),
    ("$54.9bn", "Dell record quarter revenue"),
]

REGIONS = [
    ("EUROPE", 11, (16, 60, 140)),
    ("AMERICAS", 9, (176, 96, 20)),
    ("ASIA-PACIFIC", 5, (18, 120, 60)),
    ("MIDDLE EAST", 4, (178, 24, 24)),
    ("WORLD", 4, (90, 90, 90)),
    ("AFRICA", 3, (10, 110, 110)),
    ("OCEANIA", 2, (104, 52, 140)),
]

TIMELINE = [
    ("OVERNIGHT", "Samara hit"),
    ("07:24", "Shenzhou-24 launches"),
    ("MORNING", "Ras Tanura hit"),
    ("11:34", "Zaporizhzhia off power"),
    ("EVENING", "KOSPI -6.16%"),
]

# ================================================================ ILLUSTRATIONS
# RULE: bright daylight scenes only. Pale sky, saturated colour, ONE big
# focus object per feature. No dark night scenes. Must read at 512px.

def _clouds(d, x, y, w, h, n=3):
    import random
    rnd = random.Random(7)
    for _ in range(n):
        cx = x + rnd.randint(0, max(1, w - 70))
        cy = y + rnd.randint(2, max(2, h - 22))
        cw = rnd.randint(46, 78)
        d.ellipse([cx, cy, cx + cw, cy + 13], fill=(255, 255, 255))
        d.ellipse([cx + 10, cy - 6, cx + cw - 8, cy + 9], fill=(255, 255, 255))


def _sun(d, x, y, r=16):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 214, 90))
    d.ellipse([x - r + 4, y - r + 4, x + r - 4, y + r - 4], fill=(255, 232, 150))


def _flame(d, cx, base_y, s=1.0):
    """Vivid orange flame, bright and readable at small sizes."""
    w, h = 34 * s, 52 * s
    pts = [(cx, base_y - h), (cx + w * 0.42, base_y - h * 0.55),
           (cx + w * 0.30, base_y - h * 0.30), (cx + w * 0.48, base_y),
           (cx - w * 0.48, base_y), (cx - w * 0.30, base_y - h * 0.30),
           (cx - w * 0.42, base_y - h * 0.55)]
    d.polygon(pts, fill=(255, 110, 0))
    d.polygon([(cx, base_y - h * 0.62), (cx + w * 0.22, base_y - h * 0.28),
               (cx + w * 0.26, base_y), (cx - w * 0.26, base_y),
               (cx - w * 0.22, base_y - h * 0.28)],
              fill=(255, 196, 0))


def _smoke(d, cx, top_y, puffs=3):
    for i in range(puffs):
        r = 12 + i * 3
        d.ellipse([cx - r + i * 8, top_y + i * 14, cx + r + i * 8, top_y + i * 14 + r * 1.4],
                  fill=(226, 226, 226))


def draw_tanker(d, x, y, w, h):
    """Feature 1: one big white tanker on a bright daylight sea."""
    d.rectangle([x, y, x + w, y + h], fill=SKY2)
    _sun(d, x + w - 34, y + 26)
    _clouds(d, x + 8, y + 8, w - 60, 40)
    sea_y = y + int(h * 0.60)
    d.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    d.rectangle([x, sea_y, x + w, sea_y + 4], fill=SEA_DK)
    for wy in (sea_y + 16, sea_y + 34):
        for wx in range(x + 10, x + w - 30, 46):
            d.arc([wx, wy, wx + 34, wy + 10], 200, 340, fill=(255, 255, 255), width=3)
    # tanker hull: white top, red bottom, one focus object
    hx0, hx1 = x + 34, x + w - 26
    hy0, hy1 = sea_y - 26, sea_y + 22
    d.rectangle([hx0, hy0, hx1, hy1 - 10], fill=(255, 255, 255),
                outline=(40, 40, 40), width=2)
    d.rectangle([hx0, hy1 - 10, hx1, hy1], fill=(200, 40, 30))
    d.rectangle([hx0, hy0, hx1, hy0 + 8], fill=(255, 255, 255))
    # deck tanks (white domes) + bridge tower with windows
    for tx in (hx0 + 26, hx0 + 78, hx0 + 130):
        d.ellipse([tx, hy0 - 16, tx + 34, hy0 + 4], fill=(240, 240, 240),
                  outline=(40, 40, 40), width=2)
    bx0 = hx1 - 52
    d.rectangle([bx0, hy0 - 44, hx1 - 6, hy0], fill=(255, 255, 255),
                outline=(40, 40, 40), width=2)
    for wy in range(hy0 - 38, hy0 - 6, 11):
        d.rectangle([bx0 + 6, wy, bx0 + 18, wy + 7], fill=(30, 60, 90))
        d.rectangle([bx0 + 24, wy, bx0 + 36, wy + 7], fill=(30, 60, 90))
    d.rectangle([bx0 + 8, hy0 - 54, bx0 + 34, hy0 - 44], fill=(200, 40, 30))
    # flame + smoke from the deck (daylight, vivid orange)
    _flame(d, hx0 + 95, hy0 - 8, s=0.75)
    _smoke(d, hx0 + 95, y + 2, puffs=2)
    # red naval mine buoy, foreground left
    mx, my, mr = x + 26, sea_y + 26, 13
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(200, 30, 30),
              outline=(120, 10, 10), width=2)
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([mx + int(mr * 0.8 * math.cos(a)), my + int(mr * 0.8 * math.sin(a)),
                mx + int((mr + 7) * math.cos(a)), my + int((mr + 7) * math.sin(a))],
               fill=(120, 10, 10), width=3)
    d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(255, 255, 255))


def draw_rocket(d, x, y, w, h):
    """Feature 2: one big white rocket on a pale blue sky."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    _sun(d, x + 30, y + 26)
    _clouds(d, x + 90, y + 12, w - 110, 46)
    _clouds(d, x + 6, y + 96, 130, 40, n=2)
    cx = x + w // 2 - 30
    # red flag with gold stars, right side
    fx = x + w - 78
    d.rectangle([fx, y + 18, fx + 3, y + 108], fill=(120, 120, 120))
    d.rectangle([fx + 3, y + 18, fx + 66, y + 52], fill=(222, 32, 32))
    d.ellipse([fx + 10, y + 25, fx + 22, y + 37], fill=(255, 215, 0))
    for sx, sy in ((fx + 28, y + 24), (fx + 38, y + 28), (fx + 44, y + 38), (fx + 28, y + 42)):
        d.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 215, 0))
    # rocket body: white, red stripe, blue window, red fins
    bx0, bx1 = cx, cx + 44
    by0, by1 = y + 18, y + 104
    d.polygon([(bx0, by0 + 26), ((bx0 + bx1) // 2, by0), (bx1, by0 + 26)],
              fill=(222, 32, 32))
    d.rectangle([bx0, by0 + 26, bx1, by1], fill=(255, 255, 255),
                outline=(40, 40, 40), width=2)
    d.rectangle([bx0, by0 + 56, bx1, by0 + 66], fill=(222, 32, 32))
    d.ellipse([bx0 + 12, by0 + 34, bx0 + 32, by0 + 52], fill=(40, 110, 190),
              outline=(40, 40, 40), width=2)
    d.polygon([(bx0, by1 - 8), (bx0 - 16, by1 + 14), (bx0, by1 + 6)], fill=(222, 32, 32))
    d.polygon([(bx1, by1 - 8), (bx1 + 16, by1 + 14), (bx1, by1 + 6)], fill=(222, 32, 32))
    _flame(d, (bx0 + bx1) // 2, by1 + 28, s=0.7)
    _smoke(d, (bx0 + bx1) // 2 - 30, by1 + 2, puffs=2)
    # gold stars
    for sx, sy, r in ((x + 16, y + 60, 6), (x + w - 24, y + 86, 5), (x + 52, y + 118, 5)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 200, 0))


def draw_refinery(d, x, y, w, h):
    """Feature 3: two white refinery towers, vivid flame, pale sky."""
    d.rectangle([x, y, x + w, y + h], fill=SKY2)
    _sun(d, x + w - 30, y + 24)
    _clouds(d, x + 10, y + 10, w - 70, 36)
    gy = y + h - 26
    d.rectangle([x, gy, x + w, y + h], fill=(232, 222, 200))
    # tower 1 (left, taller) with flame on top
    t1x, t1w = x + 44, 52
    d.rectangle([t1x, y + 58, t1x + t1w, gy], fill=(255, 255, 255),
                outline=(60, 60, 60), width=2)
    d.rectangle([t1x - 6, y + 58, t1x + t1w + 6, y + 66], fill=(200, 200, 200),
                outline=(60, 60, 60), width=2)
    for wy in range(y + 76, gy - 8, 18):
        d.rectangle([t1x + 6, wy, t1x + t1w - 6, wy + 5], fill=(200, 200, 200))
    # small smoke wisp from tower 1 (flame lives on tower 2, clear of banner)
    _smoke(d, t1x + t1w // 2 + 6, y + 30, puffs=2)
    # tower 2 (right, shorter) with platform rings -- BIG flame on top
    t2x, t2w = x + 150, 58
    d.rectangle([t2x, y + 58, t2x + t2w, gy], fill=(245, 245, 245),
                outline=(60, 60, 60), width=2)
    for wy in (y + 76, y + 100):
        d.rectangle([t2x - 8, wy, t2x + t2w + 8, wy + 7], fill=(180, 180, 180),
                    outline=(60, 60, 60), width=1)
    _flame(d, t2x + t2w // 2, y + 58, s=1.0)
    _smoke(d, t2x + t2w // 2 + 10, y + 2, puffs=2)
    # small chimney with red-white bands
    cx0 = x + w - 62
    for i, col in enumerate(((222, 32, 32), (255, 255, 255), (222, 32, 32), (255, 255, 255))):
        d.rectangle([cx0, y + 62 + i * 11, cx0 + 22, y + 73 + i * 11], fill=col,
                    outline=(60, 60, 60), width=1)
    d.rectangle([cx0, y + 106, cx0 + 22, gy], fill=(220, 220, 220),
                outline=(60, 60, 60), width=1)
    # connecting pipes
    d.line([t1x + t1w, gy - 14, t2x, gy - 14], fill=(90, 90, 90), width=4)
    d.line([t2x + t2w, gy - 22, cx0, gy - 22], fill=(90, 90, 90), width=4)
    # windows on towers (joni's note: buildings must have windows)
    for wy in range(y + 84, gy - 10, 20):
        d.rectangle([t2x + 8, wy, t2x + 20, wy + 8], fill=(30, 60, 90))
        d.rectangle([t2x + 34, wy, t2x + 46, wy + 8], fill=(30, 60, 90))


def draw_tile_art(d, kind, x, y, w, h):
    """Bright mini-art strip for tiles (h ~ 34)."""
    if kind == "flame":
        d.rectangle([x, y, x + w, y + h], fill=(255, 238, 200))
        _flame(d, x + 26, y + h - 4, s=0.55)
        f = f_sans(11, bold=True)
        d.text((x + 52, y + 10), "REFINERY ON FIRE", font=f, fill=(178, 24, 24))
    elif kind == "freed":
        d.rectangle([x, y, x + w, y + h], fill=(16, 110, 55))
        f = f_sans(13, bold=True)
        t = "ALL FREED \u2713"
        d.text((x + (w - tw(d, t, f)) / 2, y + 9), t, font=f, fill=(255, 255, 255))
    elif kind == "flags":
        d.rectangle([x, y, x + w, y + h], fill=(214, 236, 248))
        # Australia (blue, stars) + Solomons (blue/green, yellow stripe)
        d.rectangle([x + 14, y + 6, x + 62, y + h - 6], fill=(16, 60, 140))
        for sx, sy in ((x + 22, y + 12), (x + 52, y + 12), (x + 38, y + 20)):
            d.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 255, 255))
        d.rectangle([x + 76, y + 6, x + 124, y + h - 6], fill=(16, 110, 55))
        d.polygon([(x + 76, y + h - 6), (x + 124, y + 6), (x + 124, y + h - 6)],
                  fill=(16, 60, 140))
        d.polygon([(x + 76, y + 6), (x + 124, y + 6), (x + 76, y + 22)], fill=(255, 215, 0))
        for sx, sy in ((x + 86, y + 12), (x + 98, y + 20), (x + 112, y + 14)):
            d.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 255, 255))
        f = f_sans(11, bold=True)
        d.text((x + 134, y + 10), "TREATY", font=f, fill=(16, 60, 140))
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        pts = [(x + 12, y + 8), (x + 60, y + 12), (x + 100, y + 20), (x + 150, y + 14),
               (x + 190, y + 28)]
        d.line(pts, fill=(178, 24, 24), width=4)
        d.polygon([(x + 190, y + 28), (x + 176, y + 24), (x + 184, y + 14)],
                  fill=(178, 24, 24))
        f = f_sans(12, bold=True)
        d.text((x + 12, y + 12), "-6.16%", font=f, fill=(178, 24, 24))
    elif kind == "euro":
        d.rectangle([x, y, x + w, y + h], fill=(255, 244, 200))
        f = f_sans(15, bold=True)
        d.text((x + 12, y + 8), "\u20ac115bn", font=f, fill=(176, 124, 20))
    elif kind == "plane":
        d.rectangle([x, y, x + w, y + h], fill=(214, 236, 248))
        px, py = x + w // 2, y + h // 2
        d.polygon([(px - 46, py + 4), (px + 40, py - 6), (px + 52, py + 2),
                   (px + 8, py + 8), (px - 30, py + 12)], fill=(255, 255, 255),
                  outline=(40, 40, 40), width=2)
        d.polygon([(px + 6, py - 2), (px + 22, py - 14), (px + 30, py - 2)],
                  fill=(255, 255, 255), outline=(40, 40, 40), width=2)
    elif kind == "dollar":
        d.rectangle([x, y, x + w, y + h], fill=(226, 244, 226))
        f = f_sans(15, bold=True)
        d.text((x + 12, y + 8), "$54.9bn", font=f, fill=(16, 110, 55))
    else:
        d.rectangle([x, y, x + w, y + h], fill=(238, 232, 218))
        d.rectangle([x, y, x + w, y + 4], fill=RED)

# ================================================================ WORLD MAP
# Coarse equirectangular continents, drawn from rough lon/lat polygons.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-110, 72), (-95, 80), (-80, 73),
     (-65, 62), (-55, 47), (-65, 44), (-75, 35), (-81, 26), (-84, 20),
     (-90, 14), (-97, 16), (-105, 20), (-114, 28), (-124, 40), (-125, 49),
     (-140, 60), (-158, 58), (-168, 60)],
    [(-58, 62), (-45, 68), (-30, 74), (-45, 78), (-58, 76), (-62, 70)],  # Greenland
    [(-80, 10), (-77, 4), (-70, 0), (-60, -2), (-50, -4), (-38, -6),
     (-40, -18), (-48, -28), (-57, -38), (-68, -50), (-73, -42), (-72, -20),
     (-78, -8), (-81, 2)],
    [(-10, 36), (-8, 43), (-2, 48), (3, 52), (8, 57), (12, 55), (18, 56),
     (24, 59), (28, 66), (35, 68), (40, 66), (32, 60), (28, 56), (24, 50),
     (20, 44), (16, 40), (12, 38), (4, 37), (-2, 36)],
    [(-17, 15), (-12, 28), (-5, 35), (8, 37), (18, 33), (28, 31), (34, 28),
     (40, 16), (48, 11), (51, 2), (44, -6), (40, -14), (35, -22), (30, -30),
     (22, -34), (16, -28), (13, -18), (12, -8), (8, 4), (-8, 5), (-14, 10)],
    [(40, 68), (55, 70), (75, 73), (100, 76), (125, 73), (150, 70), (170, 66),
     (178, 65), (162, 60), (150, 59), (140, 52), (135, 43), (127, 39),
     (122, 32), (114, 22), (108, 12), (103, 8), (98, 10), (94, 17), (88, 22),
     (80, 14), (76, 8), (72, 20), (64, 25), (57, 26), (52, 28), (48, 30),
     (44, 38), (40, 42)],
    [(113, -22), (120, -14), (130, -12), (140, -11), (146, -19), (150, -23),
     (153, -28), (150, -37), (146, -39), (138, -35), (130, -32), (120, -34),
     (114, -30), (113, -25)],
    [(95, -4), (100, -2), (105, -6), (110, -7), (115, -4), (120, -1),
     (125, 1), (128, -2), (125, -6), (118, -8), (108, -8), (100, -6)],  # Indonesia
    [(130, 31), (133, 34), (136, 35), (139, 38), (141, 41), (143, 43),
     (141, 39), (138, 35), (134, 33), (131, 32)],  # Japan
    [(-5, 50), (-3, 53), (-2, 55), (-4, 58), (-6, 57), (-6, 52)],  # Britain
]

# (lon, lat) of each numbered story pin, with display offsets (dx, dy) in px
# for the two that sit almost on top of each other in the Gulf.
PINS = {
    1: (56, 26, 10, -10), 2: (100, 40, 0, 0), 3: (50, 53, 0, 0),
    4: (50, 26.6, -18, 12), 5: (-75.5, 10.4, 0, 0), 6: (34.5, 31.5, 0, 0),
    7: (160, -9.5, 0, 0), 8: (127, 37.5, 0, 0), 9: (32.5, 15.6, -8, 8),
    10: (30.5, 50.4, 0, 0), 11: (-77, 39, 0, 0), 12: (-0.6, 51.5, 0, 0),
    13: (-97.7, 30.3, 0, 0),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 230, 238))
    lon0, lon1, lat0, lat1 = -170, 190, 78, -58

    def px(lon, lat):
        return (x + (lon - lon0) / (lon1 - lon0) * w,
                y + (lat0 - lat) / (lat0 - lat1) * h)

    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(232, 222, 196), outline=(150, 140, 120))
    for n, (lon, lat, dx, dy) in PINS.items():
        cx, cy = px(lon, lat)
        cx += dx
        cy += dy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        f = f_sans(8, bold=True)
        t = str(n)
        d.text((cx - tw(d, t, f) / 2, cy - 5), t, font=f, fill=(255, 255, 255))


# ================================================================ LAYOUT
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top kicker bar
    d.rectangle([0, 0, W, 26], fill=NAVY)
    f = f_sans(11, bold=True)
    d.text((14, 7), "THE WORLD IN ONE DAY", font=f, fill=(255, 255, 255))
    rt = "38 STORIES \u00b7 7 REGIONS \u00b7 ALL FROM WEDNESDAY 25 NOVEMBER 2026"
    d.text((W - 14 - tw(d, rt, f), 7), rt, font=f, fill=(255, 214, 90))

    # ---- masthead
    mf = f_serif(62)
    mt = "Wednesday 25 November 2026"
    d.text(((W - tw(d, mt, mf)) / 2, 30), mt, font=mf, fill=INK)
    d.line([14, 100, W - 14, 100], fill=INK, width=2)

    # ---- sub-headline
    sf = f_serif_it(17)
    st = ("Two tankers hit mines in Hormuz \u00b7 Shenzhou-24 carries Pakistan's "
          "first astronaut \u00b7 Ukraine drones hit two Russian refineries")
    d.text(((W - tw(d, st, sf)) / 2, 106), st, font=sf, fill=RED_DK)

    # ---- stat strip
    y0 = 130
    d.line([14, y0 - 4, W - 14, y0 - 4], fill=LINE, width=1)
    cw = (W - 28) / 6
    for i, (num, cap) in enumerate(STATS):
        cx = 14 + i * cw
        nf = f_sans(24, bold=True)
        d.text((cx + (cw - tw(d, num, nf)) / 2, y0), num, font=nf, fill=INK)
        cf = f_sans(9)
        lines = wrap(d, cap, cf, cw - 12)
        for j, ln in enumerate(lines):
            d.text((cx + (cw - tw(d, ln, cf)) / 2, y0 + 30 + j * 11), ln,
                   font=cf, fill=GREY)
        if i:
            d.line([cx, y0 + 2, cx, y0 + 48], fill=LINE, width=1)
    d.line([14, y0 + 54, W - 14, y0 + 54], fill=LINE, width=1)

    # ---- region bar
    y0 = 192
    x = 14
    rf = f_sans(11, bold=True)
    for name, n, col in REGIONS:
        t = f"{name} {n}"
        bw = tw(d, t, rf) + 16
        d.rectangle([x, y0, x + bw, y0 + 20], fill=col)
        d.text((x + 8, y0 + 4), t, font=rf, fill=(255, 255, 255))
        x += bw + 5
    rt = "= 38 stories"
    d.text((W - 14 - tw(d, rt, rf), y0 + 4), rt, font=rf, fill=INK)

    # ---- timeline strip
    y0 = 218
    d.rectangle([14, y0, W - 14, y0 + 22], fill=NAVY)
    tf = f_sans(10, bold=True)
    d.text((22, y0 + 6), "THE DAY IN UTC", font=tf, fill=(255, 214, 90))
    tx = 22 + tw(d, "THE DAY IN UTC", tf) + 16
    items = []
    for t, ev in TIMELINE:
        items.append((t, ev))
    # lay out as compact segments separated by dots
    seg_f = f_sans(10)
    for t, ev in items:
        seg = f"{t}  {ev}"
        wseg = tw(d, seg, seg_f)
        if tx + wseg > W - 20:
            break
        d.text((tx, y0 + 6), t, font=tf, fill=(255, 214, 90))
        d.text((tx + tw(d, t, tf) + 5, y0 + 6), ev, font=seg_f,
               fill=(255, 255, 255))
        tx += wseg + 18
        d.ellipse([tx - 10, y0 + 10, tx - 7, y0 + 13], fill=(255, 214, 90))

    # ---- features
    fy = 248
    fh = 226
    fcol_w = 326
    for i, ft in enumerate(FEATURES):
        fx = 14 + i * (fcol_w + 9)
        ih = 138
        art = {"tanker": draw_tanker, "rocket": draw_rocket,
               "refinery": draw_refinery}[ft["art"]]
        art(d, fx, fy, fcol_w, ih)
        # banner on illustration
        bf = f_sans(11, bold=True)
        bw = tw(d, ft["banner"], bf) + 14
        d.rectangle([fx, fy, fx + bw, fy + 20], fill=RED)
        d.text((fx + 7, fy + 4), ft["banner"], font=bf, fill=(255, 255, 255))
        # kicker line
        ky = fy + ih + 6
        num_badge(d, fx, ky, ft["num"])
        kf = f_sans(10, bold=True)
        d.text((fx + 25, ky + 4), f"{ft['region']} \u00b7 {ft['beat']}",
               font=kf, fill=INK)
        chip(d, fx + fcol_w - 74, ky + 2, ft["chip"])
        # headline
        hf = f_serif(20)
        hy = ky + 24
        draw_wrapped(d, ft["headline"], hf, fx, hy, fcol_w, INK,
                     leading=22, max_lines=2)
        # body
        bf2 = f_sans(12)
        by = hy + 46
        draw_wrapped(d, ft["body"], bf2, fx, by, fcol_w, (40, 40, 40),
                     leading=15, max_lines=3)
        # source
        sf2 = f_sans(9)
        d.text((fx, by + 46), ft["src"], font=sf2, fill=GREY)

    # ---- tiles (2 rows x 5)
    ty = 486
    tw_ = 196
    th_ = 98
    for i, tl in enumerate(TILES):
        row, col = divmod(i, 5)
        tx = 14 + col * (tw_ + 4)
        ty0 = ty + row * (th_ + 8)
        d.rectangle([tx, ty0, tx + tw_, ty0 + th_], fill=(255, 255, 255),
                    outline=LINE, width=1)
        draw_tile_art(d, tl["art"], tx + 1, ty0 + 1, tw_ - 2, 30)
        # number + region
        kf = f_sans(9, bold=True)
        d.text((tx + 6, ty0 + 33), f"{tl['num']}  {tl['region']}",
               font=kf, fill=RED_DK)
        chip(d, tx + tw_ - 66, ty0 + 32, tl["chip"], h=13)
        hf = f_serif(13)
        draw_wrapped(d, tl["headline"], hf, tx + 6, ty0 + 46, tw_ - 12, INK,
                     leading=14, max_lines=2)
        # body: 2 lines under the headline
        bf2 = f_sans(10)
        draw_wrapped(d, tl["body"], bf2, tx + 6, ty0 + 75, tw_ - 12,
                     (60, 60, 60), leading=11, max_lines=2)

    # ---- bottom: map + ALSO
    by = 696
    # map panel
    d.rectangle([14, by, 348, by + 218], fill=(255, 255, 255), outline=LINE, width=1)
    mf2 = f_sans(11, bold=True)
    d.text((22, by + 6), "WHERE IT HAPPENED", font=mf2, fill=INK)
    d.text((348 - 8 - tw(d, "PINS 1\u201313", mf2), by + 6), "PINS 1\u201313",
           font=mf2, fill=RED_DK)
    draw_map(d, 22, by + 26, 318, 164)
    lf = f_sans(9)
    d.text((22, by + 196), "Red pins = features + tiles 1\u201313.",
           font=lf, fill=GREY)
    # ALSO panel
    ax = 356
    d.text((ax, by + 6), "ALSO ON WEDNESDAY 25 NOVEMBER \u00b7 25 MORE",
           font=mf2, fill=INK)
    d.line([ax, by + 24, W - 14, by + 24], fill=LINE, width=1)
    col_w = (W - 14 - ax - 12) // 2
    af = f_sans(10)
    asf = f_sans(9)
    for i, (n, headline, src) in enumerate(ALSO):
        col, row = divmod(i, 13)
        bx = ax + col * (col_w + 12)
        byy = by + 30 + row * 14
        nf = f_sans(10, bold=True)
        d.text((bx, byy), str(n), font=nf, fill=RED_DK)
        nw = tw(d, str(n), nf) + 4
        # headline, truncated to fit before source
        max_hw = col_w - nw - tw(d, src, asf) - 8
        htxt = headline
        while tw(d, htxt, af) > max_hw and len(htxt) > 8:
            htxt = htxt[:-1]
        if htxt != headline:
            htxt = htxt.rstrip() + "\u2026"
        d.text((bx + nw, byy), htxt, font=af, fill=INK)
        d.text((bx + nw + tw(d, htxt, af) + 4, byy + 1), src, font=asf,
               fill=GREY)

    # ---- DATE CHECK
    dy = 922
    d.rectangle([14, dy, W - 14, dy + 42], outline=RED, width=2, fill=(255, 244, 240))
    d.rectangle([14, dy, 128, dy + 42], fill=RED)
    df = f_sans(12, bold=True)
    d.text((22, dy + 13), "DATE CHECK", font=df, fill=(255, 255, 255))
    dt = ("Every numbered story happened, or was first reported, on Wednesday "
          "25 November 2026 (UTC). Left out as other days' news: Huawei guilty "
          "verdict (Tue 24) \u00b7 Riyadh tower hit (Tue 24) \u00b7 COP31 ends "
          "without deal (Sun 22) \u00b7 Hanoi blast (Tue 24) \u00b7 Senegal AFCON "
          "title restored (Tue 24). Not yet: Taiwan local elections (Sat 28).")
    dtf = f_sans(10)
    draw_wrapped(d, dt, dtf, 136, dy + 5, W - 14 - 136 - 8, INK, leading=13,
                 max_lines=3)

    # ---- footer legend
    fy2 = 970
    ff = f_sans(9)
    fl1 = ("CONFIRMED = 2+ outlets  \u00b7  OFFICIAL = on the record  \u00b7  "
           "REPORTED = carried by wires, not yet official  \u00b7  CLAIM = one "
           "side's account, labelled as such. Illustrations are drawn, not photographs.")
    d.text((14, fy2), fl1, font=ff, fill=GREY)
    fl2 = ("Sources: AP, Reuters, AFP, BBC, Al Jazeera, Kyiv Independent, Xinhua, "
           "IRNA, JMIC, Eurostat, ABS, LNA, UN. Every story names its sources.")
    d.text((14, fy2 + 12), fl2, font=ff, fill=GREY)

    # ---- bottom bar
    d.rectangle([0, 996, W, H], fill=NAVY)
    bf3 = f_sans(10, bold=True)
    d.text((14, 1005), "THE WORLD IN ONE DAY", font=bf3, fill=(255, 255, 255))
    rt = "WEDNESDAY 25 NOVEMBER 2026 \u00b7 ONE PAGE"
    d.text((W - 14 - tw(d, rt, bf3), 1005), rt, font=bf3, fill=(255, 214, 90))

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    render()
