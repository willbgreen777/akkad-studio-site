#!/usr/bin/env python3
"""
Generates the Akkad Studio social images — Facebook/Instagram profile picture and
Facebook cover — in the site's navy/gold brand, using the delta mark from favicon.svg.

Run:  python3 make-social-images.py
Output: social/ folder next to this script.

Sizes are chosen so nothing important gets cropped:
  profile 1080x1080  — Facebook and Instagram both crop this to a circle, so the mark
                       is centred with generous padding
  cover   1640x856   — Facebook's recommended Page cover. It crops HARD on mobile
                       (down to roughly the middle 640px wide), so every word sits
                       inside a safe centre band.
"""
from PIL import Image, ImageDraw, ImageFont
import pathlib, math

OUT = pathlib.Path(__file__).parent / "social"
OUT.mkdir(exist_ok=True)

NAVY   = (10, 22, 38)
NAVY2  = (15, 32, 56)
GOLD   = (201, 162, 39)
GOLDLT = (227, 199, 102)
INK    = (232, 237, 244)
MUTED  = (159, 176, 196)

def font(size, bold=False):
    """Georgia is the site's face; fall back through what macOS actually ships."""
    for path in ([
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf" if bold else
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf" if bold else
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

def sans(size):
    for path in ["/System/Library/Fonts/Supplemental/Futura.ttc",
                 "/System/Library/Fonts/HelveticaNeue.ttc",
                 "/System/Library/Fonts/Helvetica.ttc"]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

def delta(d, cx, cy, size, stroke_w=None):
    """The Akkad mark: an open triangle with a solid triangle inside it."""
    sw = stroke_w or max(3, int(size * 0.09))
    h  = size
    w  = size * 1.12
    outer = [(cx, cy - h/2), (cx + w/2, cy + h/2), (cx - w/2, cy + h/2)]
    d.polygon(outer, outline=GOLD, width=sw)
    ih = h * 0.36
    iw = w * 0.34
    inner_cy = cy + h*0.18
    d.polygon([(cx, inner_cy - ih/2), (cx + iw/2, inner_cy + ih/2), (cx - iw/2, inner_cy + ih/2)], fill=GOLD)

def streaks(d, W, H, n=7):
    """The gold 'speed lines' from the website background, angled the same way."""
    for i in range(n):
        y = int(H * (i + 0.5) / n)
        length = int(W * 0.55)
        x0 = int(-W * 0.1 + (i * W * 0.16) % W)
        for t in range(length):
            frac = t / length
            alpha = math.sin(frac * math.pi)          # fade in and out
            if alpha <= 0.02:
                continue
            xx = x0 + t
            yy = y - int(t * 0.25)                     # -14deg-ish
            if 0 <= xx < W and 0 <= yy < H:
                base = d.im.getpixel((xx, yy)) if hasattr(d, "im") else NAVY
                d.point((xx, yy), fill=(
                    int(base[0] + (GOLD[0]-base[0]) * alpha * 0.22),
                    int(base[1] + (GOLD[1]-base[1]) * alpha * 0.22),
                    int(base[2] + (GOLD[2]-base[2]) * alpha * 0.22)))

# ── PROFILE — 1080x1080, cropped to a circle by both platforms ──────────────
S = 1080
img = Image.new("RGB", (S, S), NAVY)
d = ImageDraw.Draw(img)
# subtle radial lift so the circle doesn't read as flat black
for r in range(S//2, 0, -6):
    a = 1 - (r / (S/2))
    c = tuple(int(NAVY[i] + (NAVY2[i]-NAVY[i]) * a * 0.9) for i in range(3))
    d.ellipse([S/2-r, S/2-r, S/2+r, S/2+r], fill=c)
d.ellipse([46, 46, S-46, S-46], outline=GOLD, width=6)
delta(d, S/2, S/2 - 40, 380, stroke_w=34)
f = sans(74)
t = "AKKAD"
w = d.textbbox((0,0), t, font=f)[2]
d.text(((S-w)/2, S/2 + 190), t, font=f, fill=INK)
f2 = sans(38)
t2 = "S T U D I O"
w2 = d.textbbox((0,0), t2, font=f2)[2]
d.text(((S-w2)/2, S/2 + 285), t2, font=f2, fill=GOLD)
img.save(OUT / "profile-1080.png")

# ── COVER — 1640x856, mobile crops to roughly the middle 640px ──────────────
W, H = 1640, 856
img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
for y in range(H):                                  # vertical navy gradient
    a = y / H
    c = tuple(int(NAVY[i] + (NAVY2[i]-NAVY[i]) * a) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)
streaks(d, W, H)

cx = W/2
delta(d, cx, 232, 150, stroke_w=13)

f = font(78, bold=True)
line1 = "Websites for small businesses"
w1 = d.textbbox((0,0), line1, font=f)[2]
d.text((cx - w1/2, 340), line1, font=f, fill=INK)

f = font(78, bold=True)
line2 = "in Northwest Arkansas"
w2 = d.textbbox((0,0), line2, font=f)[2]
d.text((cx - w2/2, 432), line2, font=f, fill=GOLDLT)

f = sans(40)
line3 = "From $500  ·  akkadstudio.com"
w3 = d.textbbox((0,0), line3, font=f)[2]
d.text((cx - w3/2, 566), line3, font=f, fill=MUTED)

d.line([(cx-190, 646), (cx+190, 646)], fill=GOLD, width=3)

f = sans(31)
line4 = "Springdale  ·  Fayetteville  ·  Rogers  ·  Bentonville"
w4 = d.textbbox((0,0), line4, font=f)[2]
d.text((cx - w4/2, 690), line4, font=f, fill=MUTED)

img.save(OUT / "cover-1640x856.png")

# ── A square post image for the first Page post ─────────────────────────────
S = 1080
img = Image.new("RGB", (S, S), NAVY)
d = ImageDraw.Draw(img)
for y in range(S):
    a = y / S
    c = tuple(int(NAVY[i] + (NAVY2[i]-NAVY[i]) * a) for i in range(3))
    d.line([(0, y), (S, y)], fill=c)
streaks(d, S, S, n=5)
delta(d, S/2, 210, 130, stroke_w=12)
f = font(66, bold=True)
for i, ln in enumerate(["On Facebook,", "but nowhere", "on Google?"]):
    w = d.textbbox((0,0), ln, font=f)[2]
    d.text(((S-w)/2, 330 + i*88), ln, font=f, fill=INK if i < 2 else GOLDLT)
f = sans(36)
ln = "Sites from $500"
w = d.textbbox((0,0), ln, font=f)[2]
d.text(((S-w)/2, 650), ln, font=f, fill=MUTED)
f = sans(32)
ln = "akkadstudio.com"
w = d.textbbox((0,0), ln, font=f)[2]
d.text(((S-w)/2, 720), ln, font=f, fill=GOLD)
img.save(OUT / "post-1-1080.png")

for p in sorted(OUT.glob("*.png")):
    im = Image.open(p)
    print(f"  {p.name:<24} {im.size[0]}x{im.size[1]}  {p.stat().st_size//1024} KB")
