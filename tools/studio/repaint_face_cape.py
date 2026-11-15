"""CAPE + HERO FIX — PIL pass (face eyes + cape fold texture).

1. FACE: surgical repaint of the MPFB copy ONLY
   (assets/characters/mpfb/Hero_MPFB_Warrior_Face_Anime.png).
   The quaternius original is NOT touched (Warrior_Anime files are off-limits);
   the .blend's face image is repointed at the MPFB copy by fix_cape_hero.py.
   Eyes 1.6x bigger, brighter amber iris, thinner upper lash (the pass-2 lash
   band covered ~40% of the iris and the eyes read as small dark slits).
   Layout/positions unchanged (eye centres 292/732, y 430) so the face UVs
   still land.
2. CAPE FOLD TEXTURE: 1024x1024 vertical fold stripes, 9 folds, phase-matched
   to the modelled cape in fix_cape_hero.py: brightness peaks where the mesh
   fold ridge is most outward, dips in the valleys. Deep red base
   (140,18,20) = the cape uniform colour.
Run: python3 tools/studio/repaint_face_cape.py
"""
import math
from PIL import Image, ImageDraw, ImageFilter

PROJ = "/home/hatch/workspace/project-eternia"
FACE = PROJ + "/assets/characters/mpfb/Hero_MPFB_Warrior_Face_Anime.png"
FOLD = PROJ + "/assets/characters/mpfb/Hero_MPFB_Cape_Folds.png"

# ---------------------------------------------------------------- face
# Original = the quaternius pass-2 file (identical md5 to the MPFB copy
# before this edit). Erase per-column: for each x in the eye box, linearly
# interpolate the skin between a clean sample above the eye (y=350) and one
# below it (y=505) — that reproduces the local vertical gradient + centre
# glow at the eye's own x. (Sampling at the nose bridge left a visible
# pale rectangle: the centre glow is lighter at x=512 than at the eyes.)
ORIG = PROJ + "/assets/characters/quaternius/Warrior_Face_Anime.png"
img = Image.open(ORIG).convert("RGB")
W, H = img.size
assert (W, H) == (1024, 1024), img.size
d = ImageDraw.Draw(img)

EYE_CY = 430
EYE_CENTRES = (292, 732)

# 1a. erase the old eyes with the locally interpolated skin gradient.
for cx in EYE_CENTRES:
    for x in range(cx - 140, cx + 141):
        top = img.getpixel((x, 350))
        bot = img.getpixel((x, 505))
        for y in range(EYE_CY - 85, EYE_CY + 86):
            t = (y - 350) / (505 - 350)
            c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
            img.putpixel((x, y), c)
d = ImageDraw.Draw(img)
print("face: old eyes erased (per-column gradient)")

DARK = (32, 20, 12)       # lash / brow
# PASS 2b (cape-fix iteration): the 240px eyes still read as dark blobs at
# the 1.55 m closeup — the dark outer iris ring + big pupil + thick lash
# mash into a dark almond at ~26 px on screen. Brighter, thinner dark
# ring, smaller pupil, bigger highlights, thinner lash, slightly bigger eye.
AMBER_D = (170, 110, 40)  # iris outer (thin ring only)
AMBER_M = (235, 165, 60)  # iris mid
AMBER_L = (250, 200, 90)  # iris inner (bright, covers most of the iris)
PUPIL = (20, 10, 4)

def eye(cx, cy):
    """One big bright anime eye, centre (cx, cy), 1024px coords."""
    ew, eh = 260, 140  # pass 2 was 240x130
    x0, y0 = cx - ew // 2, cy - eh // 2
    x1, y1 = cx + ew // 2, cy + eh // 2
    # sclera
    d.ellipse([x0, y0, x1, y1], fill=(250, 244, 235))
    # iris (bright amber, radial: concentric ellipses; the dark outer ring
    # is THIN now — most of the iris is the bright inner amber)
    ir = 72  # pass 2 was 65
    icx, icy = cx, cy + 6
    d.ellipse([icx - ir, icy - ir, icx + ir, icy + ir], fill=AMBER_D)
    ir2 = int(ir * 0.88)
    d.ellipse([icx - ir2, icy - ir2, icx + ir2, icy + ir2], fill=AMBER_M)
    ir3 = int(ir * 0.62)
    d.ellipse([icx - ir3, icy - ir3, icx + ir3, icy + ir3], fill=AMBER_L)
    # pupil (smaller: r 20, was 27 — the big black centre is what read dark)
    pr = 20
    d.ellipse([icx - pr, icy - pr, icx + pr, icy + pr], fill=PUPIL)
    # upper lash: THIN band (top 14 px only, was 26)
    d.pieslice([x0 - 4, y0 - 12, x1 + 4, y0 + 14], 180, 360, fill=DARK)
    # redraw sclera slivers at the corners so the lash follows the eye shape
    d.ellipse([x0, y0, x1, y1], outline=(250, 244, 235), width=2)
    # outer wing flick
    d.polygon([(x1 - 8, y0 + 6), (x1 + 34, y0 - 8), (x1 + 6, y0 + 20)], fill=DARK)
    # highlights: bigger (big 34x28, was 28x28; small 20x16, was 18x18)
    d.ellipse([icx - 36, icy - 40, icx - 2, icy - 12], fill=(255, 255, 255))
    d.ellipse([icx + 12, icy + 14, icx + 32, icy + 30], fill=(255, 255, 255))
    # lower lash line
    d.arc([x0 + 6, y0 + 14, x1 - 6, y1 + 10], 15, 165, fill=(107, 74, 47), width=3)
    # upper crease
    d.arc([x0 - 2, y0 - 34, x1 + 2, y0 + 30], 200, 340, fill=(138, 90, 52), width=3)

for cx in EYE_CENTRES:
    eye(cx, EYE_CY)
print("face: new eyes drawn (260x140, iris r=72, bright inner amber, pupil r=20, thin lash)")

img.save(FACE)
print("saved", FACE)

# ---------------------------------------------------------------- cape fold texture
# Phase-matched to fix_cape_hero.py: fold(u) = shaped sin(2*pi*9*u),
# shaped = sign(g)*|g|**0.8. Ridges (fold most outward) brighter.
N_FOLDS = 9
BASE = (140, 18, 20)  # = cape uniform (0.55, 0.07, 0.08) * 255
tex = Image.new("RGB", (1024, 1024), BASE)
px = tex.load()
for x in range(1024):
    u = x / 1023.0
    g = math.sin(2 * math.pi * N_FOLDS * u)
    shaped = math.copysign(abs(g) ** 0.8, g)
    # PASS 2b: the x1.30/x0.70 stripes read as a mechanical accordion
    # (pleated skirt, not draped cloth). Softer contrast (x1.18/x0.82)
    # + a slow 2-cycle amplitude modulation so the folds are not
    # identical — breaks the radiator read while keeping the stripe
    # PHASE matched to the modelled pleats.
    slow = 1.0 + 0.30 * math.sin(2 * math.pi * 2 * u + 0.7)
    for y in range(1024):
        v = y / 1023.0  # 0 top -> 1 hem
        f = (1.0 + 0.18 * shaped * slow) * (1.0 - 0.10 * v)
        px[x, y] = tuple(max(0, min(255, int(BASE[i] * f))) for i in range(3))
tex.save(FOLD)
print("saved", FOLD, "9 folds, ridge x1.18 / valley x0.82, hem x0.90, slow 2-cycle modulation")
