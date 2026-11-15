"""PROJECT ETERNIA — anime hero PASS 2 (Character dept).
Re-styles Warrior_Anime.glb in place: imports the pass-1 GLB, applies the five
pass-2 fixes, saves Warrior_Anime.blend next to it and re-exports the GLB.

 (b) chin: lift jaw verts (face plate + head mesh) with a smooth falloff.
 (d) cape: flare the hem (0.95 -> 1.47 m raw) + bow it off the back.
 (e) hair: rebuild HairCards as 6 wide bold cards (2 fringe, 2 side, 2 back)
     + keep the 8 ponytail quads; puff the hair cap on the head mesh +6%.
 (a) texture repaint is done by tools/studio/repaint_face_pass2.py (run first);
     this script relinks the materials to the repainted disk PNGs.
 (a/c) shader cap + fill light are Godot-side (anime_face.gdshader, scene).

Run: blender --background --python tools/studio/hero_pass2.py
Idempotent-ish: it always starts from the COMMITTED Warrior_Anime.glb, so
re-running after a `git checkout` of the GLB reproduces pass 2 from pass 1.
"""
import bpy
import math
from mathutils import Vector

PROJ = "/home/hatch/workspace/project-eternia"
GLB = PROJ + "/assets/characters/quaternius/Warrior_Anime.glb"
BLEND = PROJ + "/assets/characters/quaternius/Warrior_Anime.blend"
FACE_PNG = PROJ + "/assets/characters/quaternius/Warrior_Face_Anime.png"
HAIR_PNG = PROJ + "/assets/characters/quaternius/Hair_Strands.png"
BODY_PNG = PROJ + "/assets/characters/quaternius/Warrior_Texture.png"
SWORD_PNG = PROJ + "/assets/characters/quaternius/Warrior_Sword_Texture.png"


def sstep(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)

arm = bpy.data.objects["CharacterArmature"]
body = bpy.data.objects["Warrior_Body"]
head = bpy.data.objects["Face"]
cape = bpy.data.objects["Cape"]
hair = bpy.data.objects["HairCards"]

# --- reset pose to rest so the export bakes a clean bind pose
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
bpy.ops.pose.select_all(action="SELECT")
bpy.ops.pose.transforms_clear()
bpy.ops.object.mode_set(mode="OBJECT")
if arm.animation_data:
    arm.animation_data.action = None
bpy.context.scene.frame_set(1)

# --- remove the pass-1 cloth-sim leftover (hidden 2 m icosphere at origin)
if "Icosphere" in bpy.data.objects:
    ico = bpy.data.objects["Icosphere"]
    bpy.data.objects.remove(ico, do_unlink=True)
    print("PASS2: removed stray Icosphere")

# --- (b) shorten the chin: lift jaw verts, smooth falloff, keep registration
# Face plate (Warrior_Body, Face_Anime material) + neck column.
me = body.data
face_mat_idx = [i for i, m in enumerate(me.materials) if m and m.name == "Face_Anime"]
face_polys = set()
for p in me.polygons:
    if p.material_index in face_mat_idx:
        face_polys.update(p.vertices)
moved = 0
for v in me.vertices:
    co = v.co
    if co.z < 2.02 or co.z > 2.40 or abs(co.x) > 0.32:
        continue
    if v.index not in face_polys and not (-0.35 < co.y < 0.35):
        continue
    w = 1.0 - sstep(2.08, 2.35, co.z)  # 1 at chin, 0 at brow line
    if w > 0:
        v.co.z += 0.07 * w
        if co.z < 2.30:  # widen the jaw a touch so the face reads less narrow
            v.co.x *= 1.0 + 0.03 * w
        moved += 1
print(f"PASS2: chin lift on Warrior_Body moved {moved} verts")
# Head mesh ("Face" object): same lift so the two stay registered.
me = head.data
moved = 0
for v in me.vertices:
    co = v.co
    if co.z < 2.08 or co.z > 2.42 or abs(co.x) > 0.34:
        continue
    w = 1.0 - sstep(2.12, 2.42, co.z)
    if w > 0:
        v.co.z += 0.06 * w
        if co.z < 2.30:
            v.co.x *= 1.0 + 0.03 * w
        moved += 1
print(f"PASS2: chin lift on head mesh moved {moved} verts")

# --- (e) hair-cap volume: puff the crown/back of the head mesh +6%
me = head.data
moved = 0
for v in me.vertices:
    co = v.co
    if co.z <= 2.55 or co.y <= -0.10:
        continue
    sz = sstep(2.55, 2.75, co.z)
    sy = sstep(-0.10, 0.15, co.y)
    f = 1.0 + 0.06 * sz * sy
    if f > 1.0:
        v.co.x *= f
        v.co.y = 0.10 + (co.y - 0.10) * f
        moved += 1
print(f"PASS2: hair puff moved {moved} head verts")

# --- (d) cape: flare the hem wider than the shoulders + bow it off the back
me = cape.data
for v in me.vertices:
    co = v.co
    t = max(0.0, min(1.0, (2.44 - co.z) / 1.45))  # 0 top, 1 hem
    v.co.x *= 1.0 + 0.55 * t
    v.co.y += 0.13 * (t ** 1.5)
xs = [v.co.x for v in me.vertices]
ys = [v.co.y for v in me.vertices]
zs = [v.co.z for v in me.vertices]
print(f"PASS2: cape now x=[{min(xs):.2f},{max(xs):.2f}] y=[{min(ys):.2f},{max(ys):.2f}] z=[{min(zs):.2f},{max(zs):.2f}]")

# --- (e) rebuild HairCards: 6 wide bold cards + old ponytail quads
old_me = hair.data
old_uv = old_me.uv_layers.active.data
# Note: glTF stores triangles, so the old "quads" are 2 tris each.
pony_tris = []  # (3x co, 3x uv)
for poly in old_me.polygons:
    cx = sum(old_me.vertices[i].co.x for i in poly.vertices) / len(poly.vertices)
    cy = sum(old_me.vertices[i].co.y for i in poly.vertices) / len(poly.vertices)
    cz = sum(old_me.vertices[i].co.z for i in poly.vertices) / len(poly.vertices)
    if cy > 0.42:  # ponytail region: keep as-is
        cos = [tuple(old_me.vertices[i].co) for i in poly.vertices]
        uvs = [tuple(old_uv[li].uv) for li in poly.loop_indices]
        pony_tris.append((cos, uvs))
print(f"PASS2: kept {len(pony_tris)} ponytail tris")

hair_mat = old_me.materials[0]
arm_mod = None
for m in hair.modifiers:
    if m.type == "ARMATURE":
        arm_mod = m
        print(f"PASS2: old HairCards armature modifier object={m.object.name if m.object else None} use_vg={m.use_vertex_groups}")

verts, uvs, faces = [], [], []


def add_card(grid, uv_rect, flip=False):
    """grid: rows top->bottom, each a list of (x,y,z). uv_rect=(u0,v_top,u1,v_bot)."""
    base = len(verts)
    nrows, ncols = len(grid), len(grid[0])
    for r, row in enumerate(grid):
        for c, p in enumerate(row):
            verts.append(p)
            u = uv_rect[0] + (uv_rect[2] - uv_rect[0]) * (c / (ncols - 1))
            v = uv_rect[1] + (uv_rect[3] - uv_rect[1]) * (r / (nrows - 1))
            uvs.append((u, v))
    for r in range(nrows - 1):
        for c in range(ncols - 1):
            a = base + r * ncols + c
            b = base + r * ncols + c + 1
            cc = base + (r + 1) * ncols + c
            dd = base + (r + 1) * ncols + c + 1
            faces.append((a, cc, dd, b) if flip else (a, b, dd, cc))


def fringe_grid(x0, x1, mirror=False):
    cols = [x0 + (x1 - x0) * i / 3 for i in range(4)]
    rows = []
    zrows = [2.93, 2.85, 2.77, 2.69, 2.61]
    yrows = [-0.255, -0.275, -0.295, -0.315, -0.335]
    for ri, (z, y) in enumerate(zip(zrows, yrows)):
        row = []
        for x in cols:
            edge = (abs(x) / 0.33) ** 2
            zz = z + (0.04 * edge if ri == 4 else 0.0)  # outer tips end shorter
            row.append((x, y + 0.04 * edge, zz))
        rows.append(row)
    return rows


# fringe: 2 wide cards (was 8 thin strips), facing forward (-Y) -> flip winding
add_card(fringe_grid(-0.33, 0.0), (0.02, 1.0, 0.52, 0.0), flip=True)
add_card(fringe_grid(0.0, 0.33), (0.48, 1.0, 0.98, 0.0), flip=True)


def side_grid(side):
    rows = []
    for z in [2.74, 2.60, 2.46, 2.32, 2.18]:
        flare = 0.02 * (2.74 - z) / 0.56
        row = []
        for y in [-0.14, -0.02, 0.10, 0.20]:
            x = side * (0.36 + flare)
            row.append((x, y, z))
        rows.append(row)
    return rows


# side locks: left faces -X (cols front->back), right mirrored (cols back->front)
add_card(side_grid(-1), (0.05, 1.0, 0.55, 0.0))
add_card([list(reversed(row)) for row in side_grid(1)], (0.45, 1.0, 0.95, 0.0))


def back_grid(x0, x1):
    cols = [x0 + (x1 - x0) * i / 3 for i in range(4)]
    rows = []
    for z, y in [(2.96, 0.35), (2.79, 0.375), (2.62, 0.40), (2.45, 0.425), (2.28, 0.45)]:
        row = []
        for x in cols:
            edge = (abs(x) / 0.29) ** 2
            row.append((x, y - 0.03 * edge, z))
        rows.append(row)
    return rows


# back hair: 2 wide cards facing backward (+Y)
add_card(back_grid(-0.29, 0.0), (0.0, 1.0, 0.5, 0.0))
add_card(back_grid(0.0, 0.29), (0.5, 1.0, 1.0, 0.0))

# ponytail tris appended as standalone tris (own verts, original UVs)
for cos, quvs in pony_tris:
    base = len(verts)
    for co, uv in zip(cos, quvs):
        verts.append(co)
        uvs.append(uv)
    faces.append((base, base + 1, base + 2))

new_me = bpy.data.meshes.new("HairCards")
new_me.from_pydata(verts, [], faces)
new_me.update()
uv_layer = new_me.uv_layers.new(name="UVMap")
for loop in new_me.loops:
    uv_layer.data[loop.index].uv = uvs[loop.vertex_index]
new_me.materials.append(hair_mat)

new_hair = bpy.data.objects.new("HairCards", new_me)
bpy.context.scene.collection.objects.link(new_hair)
new_hair.parent = arm
mod = new_hair.modifiers.new(name="Armature", type="ARMATURE")
mod.object = arm
mod.use_vertex_groups = True
vg = new_hair.vertex_groups.new(name="Head")
vg.add(list(range(len(verts))), 1.0, "REPLACE")
print(f"PASS2: new HairCards verts={len(verts)} faces={len(faces)} (6 bold cards + {len(pony_tris)} ponytail tris)")

# check card normals (fringe should face -Y, back +Y, sides -/+X)
new_me.calc_loop_triangles()
for i, poly in enumerate(new_me.polygons):
    if i in (0, 16, 32, 48, 64, 80):
        print(f"PASS2: card face {i} normal={tuple(round(c, 2) for c in poly.normal)}")

bpy.data.objects.remove(hair, do_unlink=True)
bpy.data.meshes.remove(old_me)  # free the "HairCards" mesh name for the new mesh
new_hair.name = "HairCards"
new_me.name = "HairCards"

# --- relink material images to the repainted disk PNGs (drop packed copies)
def relink(mat_name, disk_path, new_name):
    mat = bpy.data.materials[mat_name]
    old_imgs = set()
    for node in mat.node_tree.nodes:
        if node.type == "TEX_IMAGE" and node.image is not None:
            old_imgs.add(node.image)
    new_img = bpy.data.images.load(disk_path)
    for node in mat.node_tree.nodes:
        if node.type == "TEX_IMAGE":
            node.image = new_img
    for img in old_imgs:  # drop the packed copies first, so the clean name is free
        if img.users == 0:
            bpy.data.images.remove(img)
    new_img.name = new_name
    new_img.filepath = "//" + new_name + ".png"
    print(f"PASS2: relinked {mat_name} -> {disk_path}")


relink("Face_Anime", FACE_PNG, "Warrior_Face_Anime")
relink("HairCards", HAIR_PNG, "Hair_Strands")
relink("Warrior_Texture", BODY_PNG, "Warrior_Texture")
relink("Warrior_Sword_Texture", SWORD_PNG, "Warrior_Sword_Texture")

# hair cards render double-sided so the back/side locks read from every angle
bpy.data.materials["HairCards"].use_backface_culling = False

# --- save .blend source, then export GLB
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("PASS2: saved", BLEND)

bpy.ops.export_scene.gltf(
    filepath=GLB,
    export_format="GLB",
    export_animations=True,
    export_skins=True,
    export_apply=False,
    export_yup=True,
    export_materials="EXPORT",
)
print("PASS2: exported", GLB)

# --- verify stats
total_tris = 0
for o in bpy.data.objects:
    if o.type == "MESH":
        o.data.calc_loop_triangles()
        total_tris += len(o.data.loop_triangles)
        print(f"PASS2: mesh {o.name} verts={len(o.data.vertices)} tris={len(o.data.loop_triangles)}")
print("PASS2: TOTAL TRIS =", total_tris)
print("PASS2: actions =", sorted(a.name for a in bpy.data.actions))
print("PASS2: objects =", sorted(o.name for o in bpy.data.objects))
