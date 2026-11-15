"""Pass 2 repaint of the anime face + hair strand textures (PIL, 2x supersampled).
Same layout language as pass 1 (symmetric, clean vector style), with:
 (a) warmer + darker skin so it stops clipping to white under sun+sky,
 (b) eyes ~35% larger, mouth + blush raised (shorter perceived chin).
Saves over the source PNGs in assets/characters/quaternius/ (kept as .kra-free
source: the deterministic repaint script lives at tools/studio/repaint_face_pass2.py
-- rerun it to reproduce these exact PNGs).
"""
import math
from PIL import Image, ImageDraw, ImageFilter

S = 2  # supersample
W, H = 1024 * S, 1024 * S
FACE = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/Warrior_Face_Anime.png"
HAIR = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/Hair_Strands.png"

# ---------------------------------------------------------------- face
img = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(img)

# Skin base: warm tan, slightly darker than pass 1 (#B98A63 -> #A87C54), with a
# very subtle vertical light falloff (forehead a touch lighter, chin darker).
SKIN_TOP = (178, 132, 90)
SKIN_BOT = (158, 110, 72)
for y in range(H):
    t = y / H
    c = tuple(int(SKIN_TOP[i] + (SKIN_BOT[i] - SKIN_TOP[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)
# soft centre light on the forehead/cheeks
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([W * 0.28, H * 0.05, W * 0.72, H * 0.62], fill=(14, 9, 4))
glow = glow.filter(ImageFilter.GaussianBlur(180 * S))
from PIL import ImageChops
img = ImageChops.add(img, glow)

d = ImageDraw.Draw(img)
DARK = (32, 20, 12)      # lash / brow
AMBER_D = (122, 74, 22)  # iris outer
AMBER_M = (181, 119, 36) # iris mid
AMBER_L = (217, 154, 53) # iris inner
PUPIL = (20, 10, 4)

def eye(cx, cy):
    """One big anime eye, centre (cx, cy) in supersampled px."""
    ew, eh = 150 * S, 88 * S
    x0, y0 = cx - ew // 2, cy - eh // 2
    x1, y1 = cx + ew // 2, cy + eh // 2
    # sclera
    d.ellipse([x0, y0, x1, y1], fill=(245, 239, 230))
    # iris (amber, radial: concentric ellipses)
    ir = 82 * S // 2
    icx, icy = cx, cy + 4 * S
    d.ellipse([icx - ir, icy - ir, icx + ir, icy + ir], fill=AMBER_D)
    ir2 = int(ir * 0.78)
    d.ellipse([icx - ir2, icy - ir2, icx + ir2, icy + ir2], fill=AMBER_M)
    ir3 = int(ir * 0.52)
    d.ellipse([icx - ir3, icy - ir3, icx + ir3, icy + ir3], fill=AMBER_L)
    # pupil
    pr = 34 * S // 2
    d.ellipse([icx - pr, icy - pr, icx + pr, icy + pr], fill=PUPIL)
    # upper lash: thick dark band across the top of the eye
    d.pieslice([x0 - 4 * S, y0 - 16 * S, x1 + 4 * S, y0 + 46 * S], 180, 360, fill=DARK)
    # clip lash to eye shape: redraw sclera slivers at the corners
    d.ellipse([x0, y0, x1, y1], outline=(245, 239, 230), width=2 * S)
    # outer wing flick
    d.polygon([(x1 - 8 * S, y0 + 6 * S), (x1 + 26 * S, y0 - 6 * S), (x1 + 6 * S, y0 + 18 * S)], fill=DARK)
    # highlights
    d.ellipse([icx - 26 * S, icy - 28 * S, icx - 2 * S, icy - 4 * S], fill=(255, 255, 255))
    d.ellipse([icx + 8 * S, icy + 10 * S, icx + 22 * S, icy + 24 * S], fill=(255, 255, 255))
    # lower lash line
    d.arc([x0 + 6 * S, y0 + 14 * S, x1 - 6 * S, y1 + 10 * S], 15, 165, fill=(107, 74, 47), width=3 * S)
    # upper crease
    d.arc([x0 - 2 * S, y0 - 34 * S, x1 + 2 * S, y0 + 30 * S], 200, 340, fill=(138, 90, 52), width=3 * S)

def brow(cx, cy):
    # arched brow, thicker than pass 1
    d.arc([cx - 62 * S, cy - 26 * S, cx + 62 * S, cy + 26 * S], 205, 335, fill=DARK, width=11 * S)

for cx in (292 * S, 732 * S):
    eye(cx, 430 * S)
    brow(cx, 238 * S)

# blush (soft, raised from y590 -> y565) + nose tick + mouth (raised 830 -> 795)
blush = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(blush)
for cx in (290 * S, 734 * S):
    bd.ellipse([cx - 58 * S, 565 * S - 32 * S, cx + 58 * S, 565 * S + 32 * S], fill=(217, 106, 85, 110))
blush = blush.filter(ImageFilter.GaussianBlur(16 * S))
img = Image.alpha_composite(img.convert("RGBA"), blush).convert("RGB")
d = ImageDraw.Draw(img)
d.arc([512 * S - 8 * S, 566 * S, 512 * S + 8 * S, 582 * S], 20, 160, fill=(138, 90, 58), width=3 * S)
# smile
d.arc([512 * S - 42 * S, 762 * S, 512 * S + 42 * S, 828 * S], 15, 165, fill=(122, 46, 34), width=5 * S)
# lower lip hint
d.arc([512 * S - 22 * S, 806 * S, 512 * S + 22 * S, 824 * S], 20, 160, fill=(201, 138, 106), width=4 * S)
# chin/neck shadow strip at the very bottom (as pass 1)
d.rectangle([0, 985 * S, W, H], fill=(107, 66, 38))

img = img.resize((1024, 1024), Image.LANCZOS)
img.save(FACE)
print("saved", FACE, img.size)

# ---------------------------------------------------------------- hair strands
# 256x512, transparent bg, 8 bold strands: roots at image top (v=1), tapered
# tips at image bottom (v=0). Hard alpha (scissor-friendly).
SW, SH = 256 * S, 512 * S
him = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
hd = ImageDraw.Draw(him)
STRAND_D = (51, 32, 15, 255)
STRAND_M = (122, 82, 48, 255)
STRAND_L = (168, 123, 79, 255)
for i in range(8):
    cx = int((i + 0.5) * SW / 8)
    wob = 10 * S * math.sin(i * 1.7)
    w_top = 24 * S
    w_bot = 8 * S
    pts = []
    steps = 24
    for s in range(steps + 1):
        t = s / steps
        y = t * SH
        w = w_top + (w_bot - w_top) * t
        x = cx + wob * math.sin(t * 3.1 + i)
        pts.append((x - w / 2, y))
    for s in range(steps, -1, -1):
        t = s / steps
        y = t * SH
        w = w_top + (w_bot - w_top) * t
        x = cx + wob * math.sin(t * 3.1 + i)
        pts.append((x + w / 2, y))
    hd.polygon(pts, fill=STRAND_D)
    # lighter centre stripe (tapers with the strand)
    stripe = []
    for s in range(steps + 1):
        t = s / steps
        y = t * SH
        w = (w_top * 0.42 + (w_bot * 0.42 - w_top * 0.42) * t)
        x = cx + wob * math.sin(t * 3.1 + i)
        stripe.append((x - w / 2, y))
    for s in range(steps, -1, -1):
        t = s / steps
        y = t * SH
        w = (w_top * 0.42 + (w_bot * 0.42 - w_top * 0.42) * t)
        x = cx + wob * math.sin(t * 3.1 + i)
        stripe.append((x + w / 2, y))
    hd.polygon(stripe, fill=STRAND_M)
    # thin highlight near the root half
    hl = []
    for s in range(0, steps // 2 + 1):
        t = s / steps
        y = t * SH
        w = 5 * S
        x = cx + wob * math.sin(t * 3.1 + i) - w_top * 0.18
        hl.append((x - w / 2, y))
    for s in range(steps // 2, -1, -1):
        t = s / steps
        y = t * SH
        w = 5 * S
        x = cx + wob * math.sin(t * 3.1 + i) - w_top * 0.18
        hl.append((x + w / 2, y))
    hd.polygon(hl, fill=STRAND_L)

him = him.resize((256, 512), Image.LANCZOS)
# re-harden alpha for the scissor threshold (0.5): anything < 128 -> 0, else 255
r, g, b, a = him.split()
a = a.point(lambda v: 255 if v >= 128 else 0)
him = Image.merge("RGBA", (r, g, b, a))
him.save(HAIR)
print("saved", HAIR, him.size)
