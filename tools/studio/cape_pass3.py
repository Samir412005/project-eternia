"""PROJECT ETERNIA — Character dept, CAPE + FRINGE FIX (pass 3).

Fixes the two defects the parent read in shots 10/11 (2026-11-15):
  1. CAPE: flat salmon-pink 1.47 m rectangle (a board, not cloth).
     Rebuild the Cape mesh: hem 1.47 -> 1.02 m, 5 pleat folds across the
     cloth (depth variation grows toward the hem), drape bow off the back,
     sides wrap around the torso, wavy hem edge. UVs kept (v=0 top -> 1 hem)
     so the sway shader still weights the hem. Weights stay Torso 1.0
     (exactly as the old cape). Colour is NOT fixed here — it lives in
     assets/materials/cape_sway.gdshader (deep-red uniform + lower top band).
  2. FRINGE: crown strands stick up like sticks (fringe top row z=2.93 and
     back top row z=2.96 poke above the skull top z~2.94 as separate
     alpha-scissored strips). Lay the cards DOWN onto the head: the fringe
     gets a 6th crown row that lies flat on the dome (z=2.945, y=-0.15) and
     the row below bends back over the crown; the back cards' top row drops
     from 2.96 to 2.90, hugging the back of the dome. Forehead coverage
     (rows z<=2.77) is untouched. Side cards + ponytail copied verbatim.

Works from the EXTERNAL .blend (~/workspace/blender-sources/... — NEVER
inside the project tree: a .blend in-tree hangs `godot --import` forever).
Saves the .blend back there and re-exports the GLB with the pass-2
export settings. A .bak-pass2 copy is made first (once).

Run: ~/workspace/tools/blender-4.5/blender --background --python tools/studio/cape_pass3.py
"""
import bpy
import math
import os
import shutil
from mathutils import Vector

BLEND = "/home/hatch/workspace/blender-sources/project-eternia/hero/Warrior_Anime.blend"
BAK = BLEND + ".bak-pass2"
GLB = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/Warrior_Anime.glb"


def sstep(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


if not os.path.exists(BAK):
    shutil.copy2(BLEND, BAK)
    print("PASS3: backed up .blend to", BAK)
else:
    print("PASS3: backup already exists, keeping", BAK)

bpy.ops.wm.open_mainfile(filepath=BLEND)

arm = bpy.data.objects["CharacterArmature"]
body = bpy.data.objects["Warrior_Body"]
head = bpy.data.objects["Face"]
cape = bpy.data.objects["Cape"]
hair = bpy.data.objects["HairCards"]

# --- reset pose to rest so the export bakes a clean bind pose (as pass 2)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
bpy.ops.pose.select_all(action="SELECT")
bpy.ops.pose.transforms_clear()
bpy.ops.object.mode_set(mode="OBJECT")
if arm.animation_data:
    arm.animation_data.action = None
bpy.context.scene.frame_set(1)

# ================================================================ CAPE
old_me = cape.data
cape_mat = old_me.materials[0] if len(old_me.materials) else None
print("PASS3: old cape verts=%d polys=%d mat=%s" % (
    len(old_me.vertices), len(old_me.polygons),
    cape_mat.name if cape_mat else None))

NCOLS, NROWS = 17, 13
verts, uvs, faces = [], [], []


def cape_point(col, row):
    """col 0..16 left->right, row 0..12 top->bottom. Returns (x, y, z)."""
    u = col / (NCOLS - 1)          # 0..1 across
    s = u * 2.0 - 1.0              # -1..1 across
    t = row / (NROWS - 1)          # 0 top .. 1 hem
    halfw = 0.31 + 0.20 * (t ** 1.1)   # top +-0.31, hem +-0.51 (was +-0.735)
    x = s * halfw
    z = 2.44 - t * 1.46             # shoulders 2.44 -> hem 0.98
    # drape: bows off the back, more toward the hem
    y = 0.30 + 0.10 * t
    # wrap: sides curl forward around the torso (strongest at shoulders)
    y -= 0.10 * (1.0 - 0.6 * t) * (s * s)
    # pleats: 5 folds across the cloth, amplitude grows toward the hem
    fold_amp = 0.012 + 0.038 * t
    y += fold_amp * math.sin(s * math.pi * 2.5)
    # wavy hem edge
    if row == NROWS - 1:
        z -= 0.015 * (0.5 + 0.5 * math.sin(s * math.pi * 2.5))
    return (x, y, z)


for r in range(NROWS):
    for c in range(NCOLS):
        verts.append(cape_point(c, r))
        uvs.append((c / (NCOLS - 1), r / (NROWS - 1)))  # v=0 top, 1 hem
for r in range(NROWS - 1):
    for c in range(NCOLS - 1):
        a = r * NCOLS + c
        b = a + 1
        cc = a + NCOLS
        dd = cc + 1
        faces.append((a, b, dd, cc))  # winding -> +Y (outward, off the back)

new_me = bpy.data.meshes.new("Cape")
new_me.from_pydata(verts, [], faces)
new_me.update()
uv_layer = new_me.uv_layers.new(name="UVMap")
for loop in new_me.loops:
    uv_layer.data[loop.index].uv = uvs[loop.vertex_index]
if cape_mat:
    new_me.materials.append(cape_mat)

new_cape = bpy.data.objects.new("Cape", new_me)
bpy.context.scene.collection.objects.link(new_cape)
new_cape.parent = arm
mod = new_cape.modifiers.new(name="Armature", type="ARMATURE")
mod.object = arm
mod.use_vertex_groups = True
vg = new_cape.vertex_groups.new(name="Torso")  # old cape: Torso 1.0 on all verts
vg.add(list(range(len(verts))), 1.0, "REPLACE")

xs = [v[0] for v in verts]
ys = [v[1] for v in verts]
zs = [v[2] for v in verts]
print("PASS3: new cape verts=%d quads=%d x=[%.2f,%.2f] y=[%.2f,%.2f] z=[%.2f,%.2f]" % (
    len(verts), len(faces), min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))

bpy.data.objects.remove(cape, do_unlink=True)
bpy.data.meshes.remove(old_me)
new_cape.name = "Cape"
new_me.name = "Cape"

# ================================================================ HAIR
# Current layout (built by pass 2): 6 cards x 12 quads = 72 quads, then 16
# ponytail tris. Verts: fringe L 0-19, fringe R 20-39, side L 40-59,
# side R 60-79, back L 80-99, back R 100-119, ponytail 120-167.
old_hme = hair.data
old_uv = old_hme.uv_layers.active.data

# per-vertex UV (each hair vert has exactly one UV in this construction)
vert_uv = {}
for loop in old_hme.loops:
    vert_uv.setdefault(loop.vertex_index, tuple(old_uv[loop.index].uv))

hair_mat = old_hme.materials[0]
print("PASS3: old hair verts=%d polys=%d" % (len(old_hme.vertices), len(old_hme.polygons)))

hverts, huvs, hfaces = [], [], []


def add_card(grid, uv_rect, flip=False):
    """grid: rows top->bottom, each a list of (x,y,z). uv_rect=(u0,v_top,u1,v_bot)."""
    base = len(hverts)
    nrows, ncols = len(grid), len(grid[0])
    for r, row in enumerate(grid):
        for c, p in enumerate(row):
            hverts.append(p)
            u = uv_rect[0] + (uv_rect[2] - uv_rect[0]) * (c / (ncols - 1))
            v = uv_rect[1] + (uv_rect[3] - uv_rect[1]) * (r / (nrows - 1))
            huvs.append((u, v))
    for r in range(nrows - 1):
        for c in range(ncols - 1):
            a = base + r * ncols + c
            b = base + r * ncols + c + 1
            cc = base + (r + 1) * ncols + c
            dd = base + (r + 1) * ncols + c + 1
            hfaces.append((a, cc, dd, b) if flip else (a, b, dd, cc))


def copy_card(first_vert, nverts, first_poly, npolys):
    """Copy a card verbatim (verts + UVs + quad faces) from the old mesh."""
    remap = {}
    for i in range(nverts):
        remap[first_vert + i] = len(hverts)
        hverts.append(tuple(old_hme.vertices[first_vert + i].co))
        huvs.append(vert_uv[first_vert + i])
    for p in range(first_poly, first_poly + npolys):
        poly = old_hme.polygons[p]
        hfaces.append(tuple(remap[vi] for vi in poly.vertices))


def fringe_grid(x0, x1):
    """6 rows now: the top row LIES FLAT on the dome (z=2.945, y=-0.15)
    and row 2 bends back over the crown. Bottom 4 rows = pass 2 (forehead
    coverage untouched). Outer top corners drop to follow the dome curve."""
    cols = [x0 + (x1 - x0) * i / 3 for i in range(4)]
    # (z, y) top -> bottom
    zrows = [2.945, 2.895, 2.845, 2.770, 2.690, 2.610]
    yrows = [-0.150, -0.240, -0.300, -0.320, -0.330, -0.335]
    rows = []
    for ri, (z, y) in enumerate(zip(zrows, yrows)):
        row = []
        for x in cols:
            edge = (abs(x) / 0.33) ** 2
            if ri == 0:      # crown row: outer corners drop with the dome
                zz = z - 0.03 * edge
            elif ri == 1:
                zz = z - 0.01 * edge
            elif ri == 5:    # fringe tips: outer tips end shorter (pass 2)
                zz = z + 0.04 * edge
            else:
                zz = z
            row.append((x, y + 0.04 * edge, zz))
        rows.append(row)
    return rows


# fringe: 2 wide cards, facing forward (-Y) -> flip winding (as pass 2)
add_card(fringe_grid(-0.33, 0.0), (0.02, 1.0, 0.52, 0.0), flip=True)
add_card(fringe_grid(0.0, 0.33), (0.48, 1.0, 0.98, 0.0), flip=True)

# side locks: verbatim (polys 24-47, verts 40-79)
copy_card(40, 40, 24, 24)


def back_grid(x0, x1):
    """Top row drops 2.96 -> 2.90 to hug the back of the dome; rest = pass 2."""
    cols = [x0 + (x1 - x0) * i / 3 for i in range(4)]
    rows = []
    for z, y in [(2.90, 0.37), (2.79, 0.375), (2.62, 0.40), (2.45, 0.425), (2.28, 0.45)]:
        row = []
        for x in cols:
            edge = (abs(x) / 0.29) ** 2
            row.append((x, y - 0.03 * edge, z))
        rows.append(row)
    return rows


# back hair: 2 wide cards facing backward (+Y)
add_card(back_grid(-0.29, 0.0), (0.0, 1.0, 0.5, 0.0))
add_card(back_grid(0.0, 0.29), (0.5, 1.0, 1.0, 0.0))

# ponytail tris: verbatim (polys 72-87, verts 120-167)
remap = {}
for i in range(120, 168):
    remap[i] = len(hverts)
    hverts.append(tuple(old_hme.vertices[i].co))
    huvs.append(vert_uv[i])
for p in range(72, 88):
    poly = old_hme.polygons[p]
    hfaces.append(tuple(remap[vi] for vi in poly.vertices))

new_hme = bpy.data.meshes.new("HairCards")
new_hme.from_pydata(hverts, [], hfaces)
new_hme.update()
uv_layer = new_hme.uv_layers.new(name="UVMap")
for loop in new_hme.loops:
    uv_layer.data[loop.index].uv = huvs[loop.vertex_index]
new_hme.materials.append(hair_mat)

new_hair = bpy.data.objects.new("HairCards", new_hme)
bpy.context.scene.collection.objects.link(new_hair)
new_hair.parent = arm
mod = new_hair.modifiers.new(name="Armature", type="ARMATURE")
mod.object = arm
mod.use_vertex_groups = True
vg = new_hair.vertex_groups.new(name="Head")
vg.add(list(range(len(hverts))), 1.0, "REPLACE")

top_z = max(v[2] for v in hverts if v[1] < 0.42)
print("PASS3: new hair verts=%d faces=%d top_z(non-ponytail)=%.3f (was 2.960)" % (
    len(hverts), len(hfaces), top_z))

bpy.data.objects.remove(hair, do_unlink=True)
bpy.data.meshes.remove(old_hme)
new_hair.name = "HairCards"
new_hme.name = "HairCards"

# hair cards render double-sided (kept from pass 2)
bpy.data.materials["HairCards"].use_backface_culling = False

# --- save .blend source (EXTERNAL path only), then export GLB
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("PASS3: saved", BLEND)

bpy.ops.export_scene.gltf(
    filepath=GLB,
    export_format="GLB",
    export_animations=True,
    export_skins=True,
    export_apply=False,
    export_yup=True,
    export_materials="EXPORT",
)
print("PASS3: exported", GLB)
