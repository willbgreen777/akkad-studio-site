#!/usr/bin/env python3
"""Builds social/og-1200x630.png — the link preview 40 prospects will see
before they see anything else. Run: python3 make-og-image.py"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG, TXT, ACC, DIM = (10, 10, 11), (242, 242, 239), (53, 196, 107), (120, 120, 128)

def font(size, weight="Heavy"):
    for p in (f"/System/Library/Fonts/Avenir Next.ttc",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/Library/Fonts/Arial Bold.ttf"):
        try:
            f = ImageFont.truetype(p, size)
            return f
        except Exception:
            continue
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# warm glow behind the headline, drawn as concentric translucent ellipses
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
for i in range(70, 0, -1):
    a = i / 70.0
    r = int(560 * a)
    col = (int(10 + 26 * (1 - a)), int(10 + 19 * (1 - a)), int(11 + 12 * (1 - a)))
    gd.ellipse([W // 2 - r, -160 - r // 3, W // 2 + r, 380 + r // 3], fill=col)
img = Image.blend(img, glow, 0.85)
d = ImageDraw.Draw(img)

# the delta mark
cx, cy, s = 92, 74, 34
d.polygon([(cx, cy - s), (cx + s * 1.05, cy + s * 0.78), (cx - s * 1.05, cy + s * 0.78)],
          outline=ACC, width=7)
d.polygon([(cx, cy + s * 0.02), (cx + s * 0.42, cy + s * 0.68), (cx - s * 0.42, cy + s * 0.68)],
          fill=ACC)
d.text((146, 50), "Akkad Studio", font=font(38), fill=TXT)

# headline
lines = [("Type your business", TXT),
         ("name. Watch your", TXT),
         ("website build itself.", ACC)]
y = 196
f = font(76)
for t, c in lines:
    d.text((72, y), t, font=f, fill=c)
    y += 92

# footer rule + line
d.line([(72, 520), (W - 72, 520)], fill=(34, 34, 40), width=2)
left_f, right_f = font(27), font(30)
left_t  = "Northwest Arkansas  ·  $500  ·  pay only if you like it"
right_t = "akkadstudio.com"
rx = W - 72 - d.textlength(right_t, font=right_f)
# guarantee clearance; shrink the left line if it would ever collide
while 72 + d.textlength(left_t, font=left_f) > rx - 40 and left_f.size > 18:
    left_f = font(left_f.size - 1)
d.text((72, 549), left_t, font=left_f, fill=DIM)
d.text((rx, 546), right_t, font=right_f, fill=ACC)

img.save("social/og-1200x630.png")
print("wrote social/og-1200x630.png")
