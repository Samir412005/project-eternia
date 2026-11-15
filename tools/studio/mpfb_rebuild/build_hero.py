"""MPFB HERO REBUILD — stage 1: base + anime proportions + rig + decimate.

Run: blender --background --python tools/studio/mpfb_rebuild/build_hero.py -- --stage 1
Saves: /home/hatch/workspace/mpfb_hero/Hero_MPFB.blend (OUTSIDE the project tree)
"""
import bpy
import math
import os
import sys
from mathutils import Vector, Matrix, Quaternion

WORK = "/home/hatch/workspace/mpfb_hero"
os.makedirs(WORK, exist_ok=True)
BLEND = os.path.join(WORK, "Hero_MPFB.blend")

# MPFB loads only as the bl_ext extension.
bpy.ops.preferences.addon_enable(module="bl_ext.user_default.mpfb")
from bl_ext.user_default.mpfb.services.humanservice import HumanService

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
STAGE = int(os.environ.get("HERO_STAGE", "1"))
for a in argv:
    if a.startswith("stage="):
        STAGE = int(a.split("=")[1])


def p(*a):
    print("[BUILD]", *a)


def sstep(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


# --- clean scene ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# --- 1. create human (MPFB CC0 base mesh) ---
human = HumanService.create_human()
me = human.data
me.calc_loop_triangles()
p("base: verts=%d tris=%d" % (len(me.vertices), len(me.loop_triangles)))

# --- 2. rig: MPFB mixamo rig — added FIRST, on the full mesh WITH
# the helper verts still present. MPFB fits the rig to the helpers;
# deleting them first makes it fall back to a T-pose rig while the
# mesh stays A-pose, and the arms then deform to the chest centre
# instead of following the bones (verified 11:37). The masculine
# bake (section 4) runs after, and does not move the arms.
# is fit to the default mesh (A-pose, matching the mesh). See section 4.
rig = HumanService.add_builtin_rig(human, "mixamo")
p("rig:", rig.name if rig else None, "bones:", len(rig.data.bones) if rig else 0)
# ensure rest pose
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.pose.transforms_clear()
bpy.ops.object.mode_set(mode='OBJECT')
p("armature modifier:", [(m.type, m.name) for m in human.modifiers])

# --- 3. delete helper verts (runs AFTER the rig is added — see
# section 2; not in the "body" group — the Mask modifier hides
# exactly these; deleting them is the same visible result, and it
# also makes the tri budget honest).
# hides exactly these; deleting them is the same visible result, and it
# also makes the tri budget honest).
body_gi = human.vertex_groups["body"].index
keep = [v.index for v in me.vertices
        if any(g.group == body_gi and g.weight > 0.0 for g in v.groups)]
p("body-group verts:", len(keep), "of", len(me.vertices))
bpy.context.view_layer.objects.active = human
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
# select non-body verts and delete them
for v in me.vertices:
    v.select = not any(g.group == body_gi and g.weight > 0.0 for g in v.groups)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')
me = human.data
me.calc_loop_triangles()
p("after helper delete: verts=%d tris=%d" % (len(me.vertices), len(me.loop_triangles)))
# remove the now-pointless Mask modifier
for m in list(human.modifiers):
    if m.type == 'MASK':
        human.modifiers.remove(m)
# remove vertex groups left EMPTY by the helper deletion — MPFB's rig
# builder averages each group's verts (rig.py:970) and divides by zero
# on an empty group.
empty = []
for g in list(human.vertex_groups):
    gi = g.index
    if not any(vg.group == gi for v in me.vertices for vg in v.groups):
        empty.append(g.name)
for name in empty:
    human.vertex_groups.remove(human.vertex_groups[name])
p("removed", len(empty), "empty vertex groups:", empty[:12])
p("modifiers now:", [(m.type, m.name) for m in human.modifiers])

# --- 4. shape keys: MASCULINIZE (runs AFTER the rig is added — the
# rig is fit to the default mesh; baking the masculine morph after keeps
# the arms matching. Baking BEFORE the rig makes MPFB fit a T-pose rig to
# the masculine mesh while the mesh stays A-pose, and the arms then deform
# to the chest centre instead of following the bones, verified 11:36).
# with a female-leaning body — breasts, wide hips — wrong for a male warrior),
# then BAKE the mix into the vertex positions and remove them.
if me.shape_keys:
    keys = me.shape_keys.key_blocks
    for name, val in [("$md-universal-$ma-$yn-$av$mu-$av$wg", 1.0),
                      ("$md-universal-$fe-$yn-$av$mu-$av$wg", 0.0),
                      ("$md-$as-$ma-$yn", 0.0), ("$md-$ca-$ma-$yn", 0.0),
                      ("$md-$af-$ma-$yn", 0.0),
                      ("$md-$as-$fe-$yn", 0.0), ("$md-$ca-$fe-$yn", 0.0),
                      ("$md-$af-$fe-$yn", 0.0)]:
        if name in keys:
            keys[name].value = val
    p("phenotype set: male universal 1.0, female 0.0")
    basis = keys[0].data
    # mixed position per vertex = basis + sum(value * (key - basis))
    mixed = []
    for i, v in enumerate(me.vertices):
        co = Vector(basis[i].co)
        for kb in keys[1:]:
            if kb.value != 0.0:
                co += (Vector(kb.data[i].co) - Vector(basis[i].co)) * kb.value
        mixed.append(co)
    for i, v in enumerate(me.vertices):
        v.co = mixed[i]
    me.update()
    p("shape keys baked:", [kb.name for kb in keys])
    bpy.context.view_layer.objects.active = human
    bpy.ops.object.shape_key_remove(all=True)
    me = human.data
    p("shape keys now:", me.shape_keys is None)
    # verify the bake survived: sample vertex == evaluated mix from before
    deps = bpy.context.evaluated_depsgraph_get()
    ev = human.evaluated_get(deps)
    assert (me.vertices[1000].co - ev.data.vertices[1000].co).length < 1e-4, \
        "bake did not survive key removal"

# --- 5. anime proportions: bigger head (+12% around the neck), tiny chin lift
NECK = Vector((0.0, -0.01, 1.41))
moved = 0
for v in me.vertices:
    co = v.co
    if co.z > 1.40:
        # falloff: full above 1.46, 0 at the neck 1.40
        w = sstep(1.40, 1.46, co.z)
        if w > 0:
            v.co = NECK + (co - NECK) * (1.0 + 0.12 * w)
            moved += 1
p("head scale moved", moved, "verts")
# chin lift: face-front verts below z 1.46, falloff to 0 at 1.50
moved = 0
for v in me.vertices:
    co = v.co
    if co.z < 1.46 and co.y < -0.05 and abs(co.x) < 0.08:
        w = 1.0 - sstep(1.44, 1.50, co.z)
        if w > 0:
            v.co.z += 0.018 * w
            moved += 1
p("chin lift moved", moved, "verts")
me.update()
p("head top now:", round(max(v.co.z for v in me.vertices), 3))

# --- 6. decimate, TWO PASSES. A single Collapse pass with a binary vertex
# group consumes the weighted region ENTIRELY before touching the protected
# one (run 1: body weight 1 vanished, head weight 0 untouched — the ratio
# applies to the whole mesh, the group only orders the collapse).
# So: pass 1 collapses the BODY to ~30% (head protected), pass 2 collapses
# the HEAD to ~50% (body protected). Targets: head 8700->4500 tris,
# body 18000->5400 tris, total ~9900.
def decimate_pass(name, protect_head, ratio):
    me = human.data
    vg = human.vertex_groups.new(name=name)
    if protect_head:
        protect = [v.index for v in me.vertices if v.co.z > 1.40]
    else:
        protect = [v.index for v in me.vertices if v.co.z <= 1.40]
    pset = set(protect)
    rest = [v.index for v in me.vertices if v.index not in pset]
    vg.add(protect, 0.0, "REPLACE")
    vg.add(rest, 1.0, "REPLACE")
    bpy.context.view_layer.objects.active = human
    mod = human.modifiers.new(name=name, type='DECIMATE')
    mod.decimate_type = 'COLLAPSE'
    mod.ratio = ratio
    mod.vertex_group = name
    mod.use_collapse_triangulate = True
    for _ in range(5):
        if human.modifiers.find(name) <= 0:
            break
        bpy.ops.object.modifier_move_up(modifier=name)
    bpy.ops.object.modifier_apply(modifier=name)
    me = human.data
    me.calc_loop_triangles()
    p("decimate %s (ratio %.3f): verts=%d tris=%d head_verts=%d" % (
        name, ratio, len(me.vertices), len(me.loop_triangles),
        sum(1 for v in me.vertices if v.co.z > 1.40)))
    # the apply may already have consumed the group; remove only if present
    if name in human.vertex_groups:
        human.vertex_groups.remove(human.vertex_groups[name])

decimate_pass("Decim_Body", protect_head=True, ratio=0.527)
decimate_pass("Decim_Head", protect_head=False, ratio=0.702)
me = human.data
me.calc_loop_triangles()
p("after decimate: verts=%d tris=%d" % (len(me.vertices), len(me.loop_triangles)))
assert len(me.loop_triangles) < 12000, "decimate did not reach target"
assert sum(1 for v in me.vertices if v.co.z <= 1.40) > 1000, "body was destroyed"
p("vertex groups still present:", len(human.vertex_groups),
  "head bone group:", "mixamorig:Head" in human.vertex_groups)

# --- pose test: rotate an arm, confirm the mesh follows (weights survived) ---
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
pb = rig.pose.bones.get("mixamorig:LeftArm")
pb.rotation_mode = 'XYZ'
pb.rotation_euler = (0, 0, 1.2)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
ev = human.evaluated_get(deps)
p("pose test: LeftArm rotated, mesh evaluates OK, verts:", len(ev.data.vertices))
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.pose.transforms_clear()
bpy.ops.object.mode_set(mode='OBJECT')

# ================================================================ STAGE 2: face
# Split the front-face polys into their own material "Face_Anime" with a
# planar front projection UV, anchored on anatomy so the proven painted
# face texture (Warrior_Face_Anime.png, 1024px) lands on the right features:
#   texture eyes  u 0.285/0.715, v 0.580 (PIL y 430)
#   texture brow  v 0.768 (PIL y 238), blush v 0.448, mouth v 0.223
# Probe (pre-scale): eye z 1.546, mouth z 1.506, eye x +/-0.031.
# Head was scaled 1.12x around neck z=1.41, so anchors move to:
#   eye z' 1.5623, mouth z' 1.5175, eye x' +/-0.0347.
EYE_Z, MOUTH_Z, EYE_X = 1.5623, 1.5175, 0.0347
A_V = (0.580 - 0.223) / (EYE_Z - MOUTH_Z)
B_V = 0.580 - A_V * EYE_Z
A_U = (0.715 - 0.285) / (2 * EYE_X)
p("face UV map: u = %.3f*x + 0.5, v = %.3f*z + %.3f" % (A_U, A_V, B_V))
p("  check brow: z 1.586 -> v %.3f (want 0.768)" % (A_V * 1.586 + B_V))

FACE_PNG = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/Warrior_Face_Anime.png"
face_img = bpy.data.images.load(FACE_PNG)
face_img.name = "Warrior_Face_Anime"

# materials
skin_mat = bpy.data.materials.new(name="Skin")
skin_mat.use_nodes = True
bsdf = skin_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.66, 0.47, 0.32, 1.0)
bsdf.inputs["Metallic"].default_value = 0.0
bsdf.inputs["Roughness"].default_value = 0.85
face_mat = bpy.data.materials.new(name="Face_Anime")
face_mat.use_nodes = True
fbsdf = face_mat.node_tree.nodes["Principled BSDF"]
tex = face_mat.node_tree.nodes.new(type="ShaderNodeTexImage")
tex.image = face_img
face_mat.node_tree.links.new(tex.outputs["Color"], fbsdf.inputs["Base Color"])
fbsdf.inputs["Metallic"].default_value = 0.0
fbsdf.inputs["Roughness"].default_value = 0.85

me = human.data
me.materials.append(skin_mat)
me.materials.append(face_mat)
SKIN_I, FACE_I = 0, 1
uv = me.uv_layers.active.data
face_polys = 0
for poly in me.polygons:
    c = poly.center
    # front face: -Y facing, inside the face window
    if -0.075 < c.x < 0.075 and 1.445 < c.z < 1.605 and poly.normal.y < -0.25:
        poly.material_index = FACE_I
        face_polys += 1
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index]
            # Clamp to [0,1]: the linear v fit extrapolates below 0 at the
            # chin (min v was -0.488), so the face sampled 1.46 texture
            # heights and the painted eyes squashed to unreadable dots in
            # Godot (shot 10, 12:00). The chin piles at v=0.02 (the chin
            # strip in the texture) instead of wrapping to the eye area.
            uv[li].uv = (min(max(A_U * v.co.x + 0.5, 0.02), 0.98),
                         min(max(A_V * v.co.z + B_V, 0.02), 0.99))
    else:
        poly.material_index = SKIN_I
p("face split: %d polys -> Face_Anime, rest -> Skin" % face_polys)
# verify the eye UV: sample front-most verts near the eye line
eye_uvs = []
for v in me.vertices:
    if abs(v.co.x) > 0.02 and abs(v.co.x) < 0.05 and 1.55 < v.co.z < 1.58 and v.co.y < -0.10:
        eye_uvs.append((round(A_U * v.co.x + 0.5, 3), round(A_V * v.co.z + B_V, 3)))
p("eye-line sample UVs (want u~0.285/0.715, v~0.58):", sorted(set(eye_uvs))[:6])

# ================================================================ STAGE 3: hair
# Hair cards are RAYCAST-PROJECTED onto the actual head surface, so they lie
# ON the head and can never stick up like sticks (the failure of pass 2/3,
# whose flat grids floated above the scalp). Cap = scaled copy of the head
# top (z>1.60, hairline), fringe tips end just above the brows (z 1.59).
HAIR_PNG = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/Hair_Strands.png"
hair_img = bpy.data.images.load(HAIR_PNG)
hair_img.name = "Hair_Strands"
hair_mat = bpy.data.materials.new(name="HairCards")
hair_mat.use_nodes = True
hbsdf = hair_mat.node_tree.nodes["Principled BSDF"]
htex = hair_mat.node_tree.nodes.new(type="ShaderNodeTexImage")
htex.image = hair_img
hair_mat.node_tree.links.new(htex.outputs["Color"], hbsdf.inputs["Base Color"])
hair_mat.node_tree.links.new(htex.outputs["Alpha"], hbsdf.inputs["Alpha"])
hbsdf.inputs["Metallic"].default_value = 0.0
hbsdf.inputs["Roughness"].default_value = 0.7
hair_mat.use_backface_culling = False  # double-sided in glTF
try:
    hair_mat.surface_render_method = 'DITHERED'  # glTF alphaMode MASK
except Exception:
    pass
cap_mat = bpy.data.materials.new(name="Hair")
cap_mat.use_nodes = True
cbsdf = cap_mat.node_tree.nodes["Principled BSDF"]
cbsdf.inputs["Base Color"].default_value = (0.16, 0.11, 0.07, 1.0)
cbsdf.inputs["Metallic"].default_value = 0.0
cbsdf.inputs["Roughness"].default_value = 0.75

deps = bpy.context.evaluated_depsgraph_get()
def raycast(origin, direction):
    hit, loc, nrm, idx, obj, mat = bpy.context.scene.ray_cast(
        deps, Vector(origin), Vector(direction))
    return hit, loc, nrm

def project_grid(cols, rows, origin_fn, dir_fn, center):
    """cols/rows: param lists; origin_fn(col,row)->origin, dir_fn->direction.
    Each point is raycast onto the head. On a MISS (grid corner beyond the
    head silhouette) the column is shrunk toward `center` until a hit is
    found — the corner lands ON the head instead of floating in the air
    (the 'sticks' failure of the old flat grids)."""
    grid = []
    last_hit = [None] * len(cols)
    for ri, row in enumerate(rows):
        grow = []
        for ci, col in enumerate(cols):
            hit, loc, nrm = None, None, None
            c = col
            for _ in range(6):
                hit, loc, nrm = raycast(origin_fn(c, row), dir_fn(c, row))
                if hit:
                    break
                c = center + (c - center) * 0.5  # shrink toward the head
            if hit:
                p = loc + nrm * 0.004
                if ri == len(rows) - 1:
                    p = p + nrm * 0.006  # tips flare outward
                last_hit[ci] = (loc, nrm)
            elif last_hit[ci] is not None:
                loc, nrm = last_hit[ci]
                p = Vector((loc.x, loc.y, row)) + nrm * 0.004
            else:
                o, d = origin_fn(col, row), dir_fn(col, row)
                p = Vector(o) + Vector(d) * 0.15
            grow.append(p)
        grid.append(grow)
    return grid

verts, uvs, faces = [], [], []
card_faces = []  # (first_face_idx, expected_outward) for normal checks
def add_card(grid, uv_rect, flip=False, outward=None):
    base = len(verts)
    nrows, ncols = len(grid), len(grid[0])
    for r, row in enumerate(grid):
        for c, p in enumerate(row):
            verts.append(tuple(p))
            u = uv_rect[0] + (uv_rect[2] - uv_rect[0]) * (c / (ncols - 1))
            v = uv_rect[1] + (uv_rect[3] - uv_rect[1]) * (r / (nrows - 1))
            uvs.append((u, v))
    first = len(faces)
    for r in range(nrows - 1):
        for c in range(ncols - 1):
            a = base + r * ncols + c
            b = base + r * ncols + c + 1
            cc = base + (r + 1) * ncols + c
            dd = base + (r + 1) * ncols + c + 1
            faces.append((a, cc, dd, b) if flip else (a, b, dd, cc))
    if outward is not None:
        card_faces.append((first, Vector(outward)))

# fringe: 2 wide cards, rays from the front (+Y into the face)
FZ = [1.635, 1.62, 1.605, 1.595, 1.59]
add_card(project_grid([-0.075, -0.05, -0.025, 0.0], FZ,
                      lambda x, z: (x, -0.35, z), lambda x, z: (0, 1, 0), 0.0),
         (0.02, 1.0, 0.52, 0.0), flip=True, outward=(0, -1, 0))
add_card(project_grid([0.0, 0.025, 0.05, 0.075], FZ,
                      lambda x, z: (x, -0.35, z), lambda x, z: (0, 1, 0), 0.0),
         (0.48, 1.0, 0.98, 0.0), flip=True, outward=(0, -1, 0))
# side locks: rays from the sides, hang to the jaw (z 1.46)
SZ = [1.62, 1.58, 1.54, 1.50, 1.46]
add_card(project_grid([-0.10, -0.03, 0.04, 0.10], SZ,
                      lambda y, z: (-0.30, y, z), lambda y, z: (1, 0, 0), 0.0),
         (0.05, 1.0, 0.55, 0.0), outward=(-1, 0, 0))
add_card(project_grid([-0.10, -0.03, 0.04, 0.10], SZ,
                      lambda y, z: (0.30, y, z), lambda y, z: (-1, 0, 0), 0.0),
         (0.45, 1.0, 0.95, 0.0), outward=(1, 0, 0))
# back hair: rays from behind, down to the neck
BZ = [1.63, 1.60, 1.57, 1.54, 1.50, 1.46, 1.42]
add_card(project_grid([-0.08, -0.053, -0.027, 0.0], BZ,
                      lambda x, z: (x, 0.35, z), lambda x, z: (0, -1, 0), 0.0),
         (0.0, 1.0, 0.5, 0.0), outward=(0, 1, 0))
add_card(project_grid([0.0, 0.027, 0.053, 0.08], BZ,
                      lambda x, z: (x, 0.35, z), lambda x, z: (0, -1, 0), 0.0),
         (0.5, 1.0, 1.0, 0.0), outward=(0, 1, 0))
# ponytail: 2 crossed tapering planes from the back of the head down the back.
# The y values HUG the body's back contour (head 0.085, neck 0.065, back
# 0.09-0.12) — the old profile drifted to y=0.185, floating 8 cm behind the
# back and reading as thin rods sticking out (verified 11:24).
PONY = [(0.085, 1.55, 0.052), (0.065, 1.45, 0.048), (0.09, 1.35, 0.042),
        (0.11, 1.25, 0.035), (0.12, 1.15, 0.027), (0.12, 1.08, 0.018)]
for plane in ("x", "y"):
    grid = []
    for (y, z, w) in PONY:
        if plane == "x":
            grid.append([(-w, y, z), (w, y, z)])
        else:
            grid.append([(0, y - w, z), (0, y + w, z)])
    add_card(grid, (0.0, 1.0, 1.0, 0.0))

hair_me = bpy.data.meshes.new("HairCards")
hair_me.from_pydata(verts, [], faces)
hair_me.update()
uv_layer = hair_me.uv_layers.new(name="UVMap")
for loop in hair_me.loops:
    uv_layer.data[loop.index].uv = uvs[loop.vertex_index]
hair_me.materials.append(hair_mat)
# fix winding: each card's first face normal must point outward
hair_me.calc_loop_triangles()
for first, outward in card_faces:
    n = hair_me.polygons[first].normal
    if n.dot(outward) < 0:
        # flip every face of this card (faces are contiguous from first)
        pass  # double-sided material: winding only affects the normal, not visibility
hair_obj = bpy.data.objects.new("HairCards", hair_me)
bpy.context.scene.collection.objects.link(hair_obj)
hair_obj.parent = rig
mod = hair_obj.modifiers.new(name="Armature", type="ARMATURE")
mod.object = rig
mod.use_vertex_groups = True
vg = hair_obj.vertex_groups.new(name="mixamorig:Head")
vg.add(list(range(len(verts))), 1.0, "REPLACE")
p("HairCards: verts=%d faces=%d (fringe/side/back/ponytail)" % (len(verts), len(faces)))

# --- hair cap: a real hair HELMET, not a crown skullcap. The old cap
# (z>1.60 only) left the sides/back of the head bare skin, so the head
# read BALD in Godot (shot 10, 12:01). Now: every head poly with z>1.42
# EXCEPT the face window (the face polys stay bare so the painted face
# shows), scaled 1.04x around the head centre — covers crown, back and
# sides down to the neck, hairline at the brow in front.
me = human.data
cap_verts, cap_faces = [], []
remap = {}
for poly in me.polygons:
    c = poly.center
    is_face = (-0.075 < c.x < 0.075 and 1.445 < c.z < 1.605
               and poly.normal.y < -0.25)
    if is_face:
        continue
    if all(me.vertices[i].co.z > 1.42 for i in poly.vertices):
        idxs = []
        for i in poly.vertices:
            if i not in remap:
                v = me.vertices[i].co
                c0 = Vector((0, -0.02, 1.52))
                remap[i] = len(cap_verts)
                cap_verts.append(tuple(c0 + (v - c0) * 1.04))
            idxs.append(remap[i])
        cap_faces.append(tuple(idxs))
cap_me = bpy.data.meshes.new("HairCap")
cap_me.from_pydata(cap_verts, [], cap_faces)
cap_me.update()
cap_me.materials.append(cap_mat)
cap_obj = bpy.data.objects.new("HairCap", cap_me)
bpy.context.scene.collection.objects.link(cap_obj)
cap_obj.parent = rig
mod = cap_obj.modifiers.new(name="Armature", type="ARMATURE")
mod.object = rig
mod.use_vertex_groups = True
vg = cap_obj.vertex_groups.new(name="mixamorig:Head")
vg.add(list(range(len(cap_verts))), 1.0, "REPLACE")
p("HairCap: verts=%d faces=%d" % (len(cap_verts), len(cap_faces)))

# ================================================================ STAGE 4: cape
# REAL baked cloth sim (the flat parametric grid of pass 3 still read as a
# flat rectangle). Plane 0.55->1.0 m flared, 15x21 grid, top row pinned,
# gravity sim 60 frames against the body as a collision object, so the drape
# and folds are real physics, not painted on.
import math as _math
# measure the back surface at shoulder height so the pinned top sits just outside it
_hit, _loc, _nrm = raycast((0, 0.5, 1.48), (0, -1, 0))
back_y = _loc.y if _hit else 0.10
cape_top_y = back_y + 0.045
p("cape: back surface y=%.3f, top row y=%.3f" % (back_y, cape_top_y))
COLS, ROWS = 15, 21
TOP_Z, HEM_Z = 1.50, 0.15
TOP_W, HEM_W = 0.45, 1.10
cverts, cuvs, cfaces = [], [], []
for ri in range(ROWS):
    t = ri / (ROWS - 1)  # 0 top -> 1 hem
    z = TOP_Z + (HEM_Z - TOP_Z) * t
    w = TOP_W + (HEM_W - TOP_W) * t
    for ci in range(COLS):
        s = ci / (COLS - 1) * 2 - 1  # -1 .. 1 across
        x = s * w / 2
        # 7 DEEP pleats (was 5 x 0.04): the old cape read as a flat red
        # board from the front (shot 10, 12:01) because 4 cm folds in
        # depth are invisible head-on. 8 cm folds + a wider hem (1.10 m,
        # wraps further around the sides) put real vertical fold shading
        # where the front camera can see it.
        # + outward bow (hem clears the legs)
        y = cape_top_y + 0.08 * _math.sin(s * _math.pi * 7) * (0.15 + 0.85 * t) \
            + 0.06 * t * t
        cverts.append((x, y, z))
        cuvs.append((ci / (COLS - 1), t))  # v=0 top, 1 hem (sway shader)
for ri in range(ROWS - 1):
    for ci in range(COLS - 1):
        a = ri * COLS + ci
        b = a + 1
        c = a + COLS
        d = c + 1
        cfaces.append((a, b, d, c))
cape_me = bpy.data.meshes.new("Cape")
cape_me.from_pydata(cverts, [], cfaces)
cape_me.update()
uvl = cape_me.uv_layers.new(name="UVMap")
for loop in cape_me.loops:
    uvl.data[loop.index].uv = cuvs[loop.vertex_index]
cape_mat = bpy.data.materials.new(name="Cape_Red")
cape_mat.use_nodes = True
cmbsdf = cape_mat.node_tree.nodes["Principled BSDF"]
cmbsdf.inputs["Base Color"].default_value = (0.55, 0.07, 0.08, 1.0)
cmbsdf.inputs["Metallic"].default_value = 0.0
cmbsdf.inputs["Roughness"].default_value = 0.85
cape_me.materials.append(cape_mat)
cape_obj = bpy.data.objects.new("Cape", cape_me)
bpy.context.scene.collection.objects.link(cape_obj)
# pin group: top row only
pin = cape_obj.vertex_groups.new(name="Pin")
pin.add(list(range(COLS)), 1.0, "REPLACE")
# collision on the body (after the armature modifier in the stack)
col_mod = human.modifiers.new(name="Collision", type='COLLISION')
col_mod.settings.thickness_outer = 0.03
col_mod.settings.thickness_inner = 0.005
# cloth sim
cloth = cape_obj.modifiers.new(name="Cloth", type='CLOTH')
cloth.settings.quality = 8
cloth.settings.mass = 0.3
cloth.settings.vertex_group_mass = "Pin"  # pin group (Blender 4.5 name)
cloth.settings.goal_min = 0.0
cloth.settings.goal_max = 1.0
cloth.settings.goal_default = 0.0
cloth.settings.pin_stiffness = 20.0
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60
for f in range(1, 61):
    bpy.context.scene.frame_set(f)
bpy.context.view_layer.objects.active = cape_obj
bpy.ops.object.modifier_apply(modifier="Cloth")
human.modifiers.remove(col_mod)
cape_me = cape_obj.data
# drape check: hem should bow outward and vary in y (real folds, not flat)
hem_ys = [cape_me.vertices[ri * COLS + ci].co.y
          for ri in [ROWS - 1] for ci in range(COLS)]
mid_ys = [cape_me.vertices[(ROWS // 2) * COLS + ci].co.y for ci in range(COLS)]
p("cape sim: hem y range %.3f..%.3f (mean %.3f), mid y range %.3f..%.3f" % (
    min(hem_ys), max(hem_ys), sum(hem_ys) / len(hem_ys),
    min(mid_ys), max(mid_ys)))
p("cape: verts=%d faces=%d" % (len(cape_me.vertices), len(cape_me.polygons)))
# skin 100% to Spine2
cape_obj.parent = rig
mod = cape_obj.modifiers.new(name="Armature", type="ARMATURE")
mod.object = rig
mod.use_vertex_groups = True
vg = cape_obj.vertex_groups.new(name="mixamorig:Spine2")
vg.add(list(range(len(cape_me.vertices))), 1.0, "REPLACE")

# ================================================================ STAGE 5: clothes + armour + sword
# Clothes are tubes fitted to the measured body (tunic, belt, pants, boots,
# sleeves); armour is kitbashed from the old Warrior GLB (shoulder pads +
# sword) + a raycast chest plate. Everything skinned to the MPFB rig.
def tube_mesh(name, centers, radii, segments=12):
    """centers: list of Vector (tube spine); radii: list of (rx, ry).
    Builds a closed ring tube. Returns the mesh object (no skin yet)."""
    verts, faces = [], []
    # frame: tangent along the spine, normal/binormal for the ring
    for i, c in enumerate(centers):
        if i == 0:
            tang = (centers[1] - centers[0]).normalized()
        elif i == len(centers) - 1:
            tang = (centers[-1] - centers[-2]).normalized()
        else:
            tang = (centers[i + 1] - centers[i - 1]).normalized()
        up = Vector((0, 0, 1))
        if abs(tang.dot(up)) > 0.9:
            up = Vector((0, 1, 0))
        n = (up - tang * up.dot(tang)).normalized()
        b = tang.cross(n).normalized()
        rx, ry = radii[i]
        for s in range(segments):
            a = 2 * _math.pi * s / segments
            p = c + n * (_math.cos(a) * rx) + b * (_math.sin(a) * ry)
            verts.append(tuple(p))
    nrings = len(centers)
    for i in range(nrings - 1):
        for s in range(segments):
            a = i * segments + s
            bb = i * segments + (s + 1) % segments
            cc = (i + 1) * segments + s
            dd = (i + 1) * segments + (s + 1) % segments
            faces.append((a, cc, dd, bb))
    # caps
    faces.append(tuple(reversed(range(segments))))
    faces.append(tuple((nrings - 1) * segments + s for s in range(segments)))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    return me

def skin_by_z(obj, splits):
    """splits: [(z_threshold, bone)] evaluated top-down; first match wins.
    Last entry should have a very low threshold as the catch-all."""
    vg_names = {}
    for v in obj.data.vertices:
        bone = None
        for thresh, b in splits:
            if v.co.z > thresh:
                bone = b
                break
        if bone is None:
            bone = splits[-1][1]
        if bone not in vg_names:
            vg_names[bone] = obj.vertex_groups.new(name=bone)
        vg_names[bone].add([v.index], 1.0, "REPLACE")
    return list(vg_names.keys())

def skin_single(obj, bone):
    vg = obj.vertex_groups.new(name=bone)
    vg.add(list(range(len(obj.data.vertices))), 1.0, "REPLACE")

def add_armature(obj):
    obj.parent = rig
    mod = obj.modifiers.new(name="Armature", type="ARMATURE")
    mod.object = rig
    mod.use_vertex_groups = True

def body_extent(z, tol=0.03):
    """(max |x|, min y, max y) of TORSO verts near height z.
    Excludes the arms (|x| >= 0.25) — otherwise the tunic's top ring is as
    wide as the T-posed arms and reads as flat wings (verified 11:19)."""
    xs, ys = [], []
    for v in human.data.vertices:
        if abs(v.co.z - z) < tol and abs(v.co.x) < 0.25:
            xs.append(abs(v.co.x))
            ys.append(v.co.y)
    if not xs:
        return 0.15, -0.10, 0.10
    return max(xs), min(ys), max(ys)

# --- materials
def solid_mat(name, rgb, rough=0.8):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Metallic"].default_value = 0.0
    b.inputs["Roughness"].default_value = rough
    return m
tunic_mat = solid_mat("Tunic_Blue", (0.15, 0.25, 0.55))
belt_mat = solid_mat("Belt_Brown", (0.35, 0.22, 0.12))
pants_mat = solid_mat("Pants_Dark", (0.12, 0.12, 0.16))
boot_mat = solid_mat("Boots_Brown", (0.25, 0.15, 0.08))
plate_mat = solid_mat("Plate_Steel", (0.42, 0.44, 0.48), 0.6)  # darker than
# 0.55 grey — the lighter steel read as a white board in bright sun (11:24)

# --- tunic: elliptical tube, chest -> flared hem (measured radii + clearance)
tunic_rings = []
for z, clear in [(1.46, 0.015), (1.36, 0.017), (1.26, 0.017), (1.16, 0.018),
                 (1.06, 0.020), (0.98, 0.025)]:
    rx, ymin, ymax = body_extent(z)
    cy = (ymin + ymax) / 2
    ry = (ymax - ymin) / 2
    tunic_rings.append((Vector((0, cy, z)), (rx + clear, ry + clear)))
tunic_me = tube_mesh("Tunic", [c for c, _ in tunic_rings],
                     [r for _, r in tunic_rings], segments=16)
tunic_me.materials.append(tunic_mat)
tunic = bpy.data.objects.new("Tunic", tunic_me)
bpy.context.scene.collection.objects.link(tunic)
add_armature(tunic)
skin_by_z(tunic, [(1.28, "mixamorig:Spine1"), (1.15, "mixamorig:Spine"),
                  (-10.0, "mixamorig:Hips")])
p("Tunic: verts=%d faces=%d" % (len(tunic_me.vertices), len(tunic_me.polygons)))

# --- belt: flat band at the waist (z ~1.06)
rx, ymin, ymax = body_extent(1.06)
cy = (ymin + ymax) / 2
belt_me = tube_mesh("Belt", [Vector((0, cy, 1.10)), Vector((0, cy, 1.03))],
                    [(rx + 0.035, (ymax - ymin) / 2 + 0.035)] * 2, segments=16)
belt_me.materials.append(belt_mat)
belt = bpy.data.objects.new("Belt", belt_me)
bpy.context.scene.collection.objects.link(belt)
add_armature(belt)
skin_single(belt, "mixamorig:Hips")
p("Belt: verts=%d" % len(belt_me.vertices))

# --- sleeves: short tubes along the upper arms
def bone_vec(bone_name):
    pb = rig.pose.bones[bone_name]
    return pb.head.copy(), pb.tail.copy()
for side, arm_bone in (("L", "mixamorig:LeftArm"), ("R", "mixamorig:RightArm")):
    head, tail = bone_vec(arm_bone)
    direction = (tail - head).normalized()
    p0 = head + direction * 0.01
    p1 = head + direction * 0.17
    r0 = 0.068
    sleeve_me = tube_mesh("Sleeve_" + side, [p0, p1], [(r0, r0), (r0 * 0.92, r0 * 0.92)],
                          segments=10)
    sleeve_me.materials.append(tunic_mat)
    sleeve = bpy.data.objects.new("Sleeve_" + side, sleeve_me)
    bpy.context.scene.collection.objects.link(sleeve)
    add_armature(sleeve)
    skin_single(sleeve, arm_bone)
    p("Sleeve_%s: head=%s tail=%s" % (side, tuple(round(c, 2) for c in head),
                                      tuple(round(c, 2) for c in tail)))

# --- pants: two leg tubes, split at the knee (z 0.55) between UpLeg/Leg.
# The tubes are ELLIPTICAL, fitted to the measured leg cross-section at each
# height + clearance — the old circular r=0.08 tubes were tighter than the
# thigh (rx 0.082, ry 0.11), so the skin poked through the whole leg
# (verified 11:24).
def leg_extent(z, sx, tol=0.03):
    """(cx, cy, rx, ry) of the leg on side sx near height z."""
    xs, ys = [], []
    for v in human.data.vertices:
        if abs(v.co.z - z) < tol and (v.co.x * sx) > 0.04:
            xs.append(v.co.x)
            ys.append(v.co.y)
    if not xs:
        return sx * 0.09, -0.01, 0.09, 0.09
    return ((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2,
            (max(xs) - min(xs)) / 2, (max(ys) - min(ys)) / 2)

for side, sx in (("L", 1), ("R", -1)):
    # sx is the leg's side sign: left=+X, right=-X for this rig (faces
    # -Y; verified: right hand at x=-0.66). The old (("L",-1),("R",1))
    # CROSSED the pants — Pants_L was built from the right leg's shape
    # at x<0 but skinned to the left leg, so in the Walk each tube
    # followed the opposite leg and the forward leg read bare (shot 09,
    # 12:10). Skinning is by `side`, not sx, so only the measurement
    # and the tube centre were wrong.
    centers, radii = [], []
    for z in [1.02, 0.85, 0.70, 0.55, 0.40, 0.25, 0.16]:
        cx, cy, rx, ry = leg_extent(z, sx)
        # clamp: the top rings pick up the wide pelvis — without the clamp
        # the pants read as clown-wide (verified 11:32). Clearance raised
        # 0.015 -> 0.025/0.030 (12:10): at 0.015 the thigh's front bulged
        # through the pants when the hip flexed in the Walk, so the
        # forward leg read bare in Godot (shot 09) though the weights
        # are correct. Looser pants (baggy hero cut) fix the poke-through.
        cx = max(0.07, min(0.11, abs(cx))) * sx
        cy = max(-0.03, min(0.03, cy))
        rx = max(0.07, min(0.115, rx + 0.025))
        ry = max(0.07, min(0.140, ry + 0.030))
        centers.append(Vector((cx, cy, z)))
        radii.append((rx, ry))
    pants_me = tube_mesh("Pants_" + side, centers, radii, segments=12)
    # flip_normals: tube_mesh winds the rings so the faces point INWARD
    # for the pants (154/164 tris inward, verified 12:15) — Blender
    # renders them anyway (backface_culling=False) but Godot culls
    # back faces, so the pants were invisible and the legs read bare
    # (shots 08/09). The tunic/sleeves wind outward, so only the pants
    # need the flip.
    pants_me.flip_normals()
    pants_me.materials.append(pants_mat)
    pants = bpy.data.objects.new("Pants_" + side, pants_me)
    bpy.context.scene.collection.objects.link(pants)
    add_armature(pants)
    up = "mixamorig:LeftUpLeg" if side == "L" else "mixamorig:RightUpLeg"
    lo = "mixamorig:LeftLeg" if side == "L" else "mixamorig:RightLeg"
    skin_by_z(pants, [(0.55, up), (-10.0, lo)])
    p("Pants_%s: top center=(%.3f, %.3f) radii=%s" % (
        side, centers[0].x, centers[0].y,
        tuple(round(c, 3) for c in radii[0])))

# --- boots: box + cuff at each foot
for side, sx in (("L", -1), ("R", 1)):
    foot_head, foot_tail = bone_vec("mixamorig:LeftFoot" if side == "L"
                                    else "mixamorig:RightFoot")
    cx = foot_head.x
    # box: 0.11 wide, 0.26 long (heel to toe), 0.13 tall
    bx, by, bz = cx, -0.03, 0.075
    sx2, sy2, sz2 = 0.055, 0.13, 0.065
    bverts = [(bx + dx * sx2, by + dy * sy2, bz + dz * sz2)
              for dx in (-1, 1) for dy in (-1, 1) for dz in (-1, 1)]
    bfaces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6),
              (0, 2, 6, 4), (1, 5, 7, 3)]
    boot_me = bpy.data.meshes.new("Boot_" + side)
    boot_me.from_pydata(bverts, [], bfaces)
    boot_me.update()
    boot_me.materials.append(boot_mat)
    boot = bpy.data.objects.new("Boot_" + side, boot_me)
    bpy.context.scene.collection.objects.link(boot)
    add_armature(boot)
    skin_single(boot, "mixamorig:LeftFoot" if side == "L" else "mixamorig:RightFoot")
    p("Boot_%s: foot head=%s" % (side, tuple(round(c, 2) for c in foot_head)))

# --- chest plate: curved shell hugging the chest front, built from the
# measured torso radii (body_extent + 0.035, outside the tunic). The raycast
# version scattered verts from y=-0.35 to +0.05 and read as a crumpled white
# slab (verified 11:24); this shell cannot miss.
plate_rows = []
for z in [1.48, 1.42, 1.36, 1.30, 1.24]:
    rx, ymin, ymax = body_extent(z)
    cy = (ymin + ymax) / 2
    ry = (ymax - ymin) / 2
    plate_rows.append((z, rx + 0.035, cy, ry + 0.035))
pverts = []
for (z, rx, cy, ry) in plate_rows:
    for a_deg in (-60, -30, 0, 30, 60):
        a = _math.radians(a_deg)
        pverts.append((rx * _math.sin(a), cy - ry * _math.cos(a), z))
pfaces = []
for r in range(4):
    for c in range(4):
        a = r * 5 + c
        b = a + 1
        cc = a + 5
        dd = cc + 1
        pfaces.append((a, b, dd, cc))
plate_me = bpy.data.meshes.new("ChestPlate")
plate_me.from_pydata(pverts, [], pfaces)
plate_me.update()
plate_me.materials.append(plate_mat)
plate = bpy.data.objects.new("ChestPlate", plate_me)
bpy.context.scene.collection.objects.link(plate)
add_armature(plate)
skin_single(plate, "mixamorig:Spine1")
p("ChestPlate: verts=%d faces=%d" % (len(pverts), len(pfaces)))

# ================================================================ STAGE 6: kitbash + retarget + export
# (a) Kitbash shoulder pads + sword from the Warrior FBX (meshes are skinned
# to the Warrior rig in FBX space; apply the modifier to bake the T-pose,
# then scale/translate into MPFB space and re-skin 100% to the MPFB bone).
# (b) Retarget 7 Mixamo clips onto the MPFB mixamo rig (1:1 bone map,
# world-space rotation deltas — robust to rest-roll differences), push all
# clips to NLA, export Hero_MPFB.glb. The Quaternius Warrior clips are
# dropped: Mixamo's Walk/Run/Idle are smoother, and its Sword_And_Shield_
# Slash fits the hero's sword+shield. The Warrior FBX is kept only as the
# sword kitbash source (part a).
import os as _os
FBX = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/Warrior.fbx"
GLB_OUT = "/home/hatch/workspace/project-eternia/assets/characters/mpfb/Hero_MPFB.glb"
_os.makedirs(_os.path.dirname(GLB_OUT), exist_ok=True)
bpy.ops.import_scene.fbx(filepath=FBX)
src_arm = [o for o in bpy.context.scene.objects
           if o.type == 'ARMATURE' and o.name.startswith("CharacterArmature")][0]
# The FBX import leaves animation_data.use_nla = True on the source rig:
# with NLA on, the evaluated pose comes from the (empty) NLA stack, NOT the
# active action — so the retarget copied the REST pose into every clip
# (all-identity Walk/Idle, verified 11:20). Turn NLA off so the assigned
# action drives the pose.
src_arm.animation_data.use_nla = False
src_arm.animation_data.action = None
bpy.context.view_layer.objects.active = src_arm
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.pose.transforms_clear()
bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.scene.frame_set(1)
bpy.context.view_layer.update()
p("retarget source: %s matrix_world=%s" % (
    src_arm.name, tuple(round(c, 3) for c in src_arm.matrix_world.to_translation())))
# MPFB shoulder / hand positions (bind pose, armature == world space here)
def _bone_head(arm_obj, name):
    return arm_obj.data.bones[name].head_local.copy()
mpfb_shoulder_L = _bone_head(rig, "mixamorig:LeftShoulder")
mpfb_shoulder_R = _bone_head(rig, "mixamorig:RightShoulder")
mpfb_hand_R = _bone_head(rig, "mixamorig:RightHand")
p("mpfb shoulder L=%s R=%s hand R=%s" % (
    tuple(round(c, 2) for c in mpfb_shoulder_L),
    tuple(round(c, 2) for c in mpfb_shoulder_R),
    tuple(round(c, 2) for c in mpfb_hand_R)))

def bake_and_fit(obj, target_center, scale, bone, mat_name=None):
    """Apply the FBX armature modifier (bake T-pose), bake the object
    transform into the verts (local == world), scale about the mesh bbox
    center, move the center to target_center, re-skin to `bone`."""
    bpy.context.view_layer.objects.active = obj
    for m in list(obj.modifiers):
        if m.type == 'ARMATURE':
            bpy.ops.object.modifier_apply(modifier=m.name)
    # free the mesh from the source rig (object or bone parent) keeping its
    # world transform, then bake that transform into the verts (local==world)
    if obj.parent is not None:
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bb = [Vector(c) for c in obj.bound_box]
    mn = Vector((min(c.x for c in bb), min(c.y for c in bb), min(c.z for c in bb)))
    mx = Vector((max(c.x for c in bb), max(c.y for c in bb), max(c.z for c in bb)))
    center = (mn + mx) / 2
    me = obj.data
    for v in me.vertices:
        v.co = center + (v.co - center) * scale
    for v in me.vertices:
        v.co = v.co + (Vector(target_center) - center)
    obj.location = (0, 0, 0)
    add_armature(obj)
    skin_single(obj, bone)
    p("kitbash %s: scaled %.2f -> %s skinned %s" % (
        obj.name, scale, tuple(round(c, 2) for c in target_center), bone))

pad_L = bpy.data.objects.get("ShoulderPad.L")
pad_R = bpy.data.objects.get("ShoulderPad.R")
sword = bpy.data.objects.get("Warrior_Sword")
# pads belong on the DELTOID (arm head, x +/-0.18), not the clavicle root
# (shoulder joint x +/-0.06 — the pads sat on the neck, verified 11:15).
mpfb_arm_L = _bone_head(rig, "mixamorig:LeftArm")
mpfb_arm_R = _bone_head(rig, "mixamorig:RightArm")
# pads SKIPPED for the first version: the Warrior pauldrons kitbashed at 0.35
# read as flat slabs / airplane wings on the slimmer MPFB body (verified
# 11:17). Proper pauldrons need a remodel, not a scale-down. The FBX pads
# are deleted by the stage-6 cleanup below.
if pad_L:
    p("kitbash pads: SKIPPED (flat slabs on this body — remodel needed)")
if pad_R:
    pass
if sword:
    bpy.context.view_layer.objects.active = sword
    for m in list(sword.modifiers):
        if m.type == 'ARMATURE':
            bpy.ops.object.modifier_apply(modifier=m.name)
    if sword.parent is not None:
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    # grip = the sword vertex NEAREST the Warrior's right fist (FBX space).
    # The bbox max-y face center is empty space for a diagonal sword and put
    # the sword metres from the hand (verified 11:15).
    fist = src_arm.data.bones["Fist.R"].head_local
    grip = min((v.co for v in sword.data.vertices),
               key=lambda co: (co - fist).length)
    p("sword grip: nearest vertex to fist %s is %s (dist %.3f)" % (
        tuple(round(c, 2) for c in fist), tuple(round(c, 2) for c in grip),
        (grip - fist).length))
    assert (grip - fist).length < 0.3, "sword grip is not at the fist — bad bake!"
    me = sword.data
    for v in me.vertices:
        v.co = grip + (v.co - grip) * 0.28  # ~0.68 m sword (0.33 was 0.80 m —
        # still dragged its tip on the ground in the Walk when the arm
        # swung forward, shot 09, 12:20). A short arming sword fits the
        # 1.66 m hero and clears the ground in every clip.
    # move the grip to the MPFB hand, then correct the orientation
    for v in me.vertices:
        v.co = v.co + (mpfb_hand_R - grip)
    # Correct the sword's orientation relative to the MPFB hand so it matches
    # the Warrior sword's orientation relative to its fist: their rest
    # orientations differ, so without this the blade points through the face
    # in the idle pose (verified 11:17). Rotate about the grip (at the hand).
    R_fist = src_arm.data.bones["Fist.R"].matrix_local.to_3x3()
    R_hand = rig.data.bones["mixamorig:RightHand"].matrix_local.to_3x3()
    C = R_hand @ R_fist.inverted()
    for v in me.vertices:
        v.co = mpfb_hand_R + C @ (v.co - mpfb_hand_R)
    # Align the blade with the forearm (tilted 25 deg forward) so it hangs
    # along the arm — down at the side in the idle/walk — instead of pointing
    # up-forward (verified 11:24: the C-corrected blade pointed
    # (0.34,-0.76,0.56) in the idle and straight up in the walk).
    _tip = max((v.co for v in me.vertices),
               key=lambda co: (co - mpfb_hand_R).length)
    _cur = (_tip - mpfb_hand_R).normalized()
    _fa = rig.data.bones["mixamorig:RightForeArm"]
    _fore = (_fa.tail_local - _fa.head_local).normalized()
    _fwd = Vector((0, -1, 0))
    _axis = _fore.cross(_fwd)
    if _axis.length > 1e-6:
        _tilt = Quaternion(_axis.normalized(), _math.radians(25))
        _fore = _tilt @ _fore
    _corr = _cur.rotation_difference(_fore)
    for v in me.vertices:
        v.co = mpfb_hand_R + _corr @ (v.co - mpfb_hand_R)
    sword.location = (0, 0, 0)
    add_armature(sword)
    skin_single(sword, "mixamorig:RightHand")
    p("kitbash Warrior_Sword: grip %s -> hand %s" % (
        tuple(round(c, 2) for c in grip), tuple(round(c, 2) for c in mpfb_hand_R)))

# --- (b) retarget from Mixamo (landed 2026-11-15, ~/workspace/cloud-sync/mixamo/)
# Mixamo bones already use mixamorig: names, so the map is the 1:1 identity
# intersection with the MPFB rig (52 bones; Mixamo has 65 — the extras are
# HeadTop_End / toe End bones, which the MPFB rig lacks). Mixamo clips are
# 30 fps with ROOT MOTION (not in-place): the hips translate forward as the
# character walks/runs — strip the horizontal (world X/Y) hips translation
# and keep only the vertical (Z) bob/jump/fall, so every clip plays in place
# and the game moves the hero with code. The Mixamo armature imports with
# rotation (90, 0, 0) and scale 0.01 (cm, Y-up) — so source matrices must be
# read in WORLD space (matrix_world @ ...), never armature space.
MIXAMO_DIR = "/home/hatch/workspace/cloud-sync/mixamo"
MIXAMO_CLIPS = [
    ("Idle.fbx", "Idle_Weapon"), ("Walking.fbx", "Walk"),
    ("Running.fbx", "Run"), ("Sword_And_Shield_Slash.fbx", "Sword_Attack"),
    ("Jumping.fbx", "Jump"), ("Hit_Reaction.fbx", "Hit"),
    ("Dying.fbx", "Death"),
]
bpy.context.scene.render.fps = 30  # Mixamo clips are 30 fps; preserves timing
# target rest rotations (armature space == world space for the MPFB rig)
tgt_rest = {b.name: b.matrix_local.to_3x3() for b in rig.data.bones}
tgt_hips_rot = tgt_rest["mixamorig:Hips"]
tgt_hips_rest_z = rig.data.bones["mixamorig:Hips"].head_local.z
if not rig.animation_data:
    rig.animation_data_create()
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')

def retarget_clip(src_arm, src_action, target_name, bone_map):
    """Hierarchical world-delta retarget of one clip onto the MPFB rig.
    Source matrices are read in world space so a rotated/scaled source
    armature (Mixamo: 90 deg X, 0.01) retargets correctly."""
    src_world = src_arm.matrix_world
    src_hips_rest_w = (src_world @ src_arm.data.bones["mixamorig:Hips"].matrix_local).translation
    hip_scale = tgt_hips_rest_z / src_hips_rest_w.z
    f0, f1 = int(src_action.frame_range[0]), int(src_action.frame_range[1])
    src_arm.animation_data.use_nla = False
    src_arm.animation_data.action = src_action
    # Blender 4.5 layered actions: assigning the action CLEARS action_slot,
    # and with no slot the fcurves drive nothing (pose stays frozen — the
    # all-identity retarget, verified 11:20). Set the action's own slot.
    if src_action.slots:
        src_arm.animation_data.action_slot = src_action.slots[0]
    new_action = bpy.data.actions.new(name=target_name)
    rig.animation_data.action = new_action
    order = sorted(bone_map.items(),
                   key=lambda kv: len(rig.data.bones[kv[1]].parent_recursive))
    for f in range(f0, f1 + 1):
        bpy.context.scene.frame_set(f)
        bpy.context.view_layer.update()
        world_pose = {}  # target bone -> world rotation this frame
        for sbn, tbn in order:
            spb = src_arm.pose.bones[sbn]
            tpb = rig.pose.bones[tbn]
            # Copy the source bone's WORLD orientation directly. Do NOT apply
            # the source's orientation CHANGE to the target rest: the MPFB
            # rest pose is an A-pose (arms ~45 deg down) while Mixamo's rest
            # is a T-pose, so the change-based formula over-rotates the arms
            # by ~45 deg and crosses them over the chest (verified 11:32).
            # NOTE: build the world rotation from QUATERNIONS, not from
            # (matrix_world @ spb.matrix).to_3x3() — the Mixamo armature has
            # scale 0.01 baked into matrix_world, and that scale corrupts
            # the matrix product into garbage rotations (verified 11:33:
            # the matrix version tangled the arms into ropes).
            Wt_pose = (src_arm.matrix_world.to_quaternion()
                       @ spb.matrix.to_quaternion()).to_matrix()
            parent = rig.data.bones[tbn].parent
            if parent is None or parent.name not in world_pose:
                parent_world = Matrix.Identity(3)
                parent_rest = Matrix.Identity(3)
            else:
                parent_world = world_pose[parent.name]
                parent_rest = tgt_rest[parent.name]
            R_rel_rest = parent_rest.inverted() @ tgt_rest[tbn]
            R_local = R_rel_rest.inverted() @ parent_world.inverted() @ Wt_pose
            tpb.rotation_mode = 'QUATERNION'
            tpb.rotation_quaternion = R_local.to_quaternion()
            tpb.keyframe_insert(data_path="rotation_quaternion", frame=f)
            world_pose[tbn] = Wt_pose
        # hips location: world delta, horizontal root motion stripped, Z kept
        spb = src_arm.pose.bones["mixamorig:Hips"]
        tpb = rig.pose.bones["mixamorig:Hips"]
        delta = (src_world @ spb.matrix).translation - src_hips_rest_w
        delta.x = 0.0
        delta.y = 0.0
        tpb.location = tgt_hips_rot.inverted() @ (delta * hip_scale)
        tpb.keyframe_insert(data_path="location", frame=f)
    p("retargeted %s: frames %d-%d (%d keys), hip scale %.3f" % (
        target_name, f0, f1, f1 - f0 + 1, hip_scale))
    return new_action

CLIPS = [t for _, t in MIXAMO_CLIPS]
for fname, target_name in MIXAMO_CLIPS:
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=MIXAMO_DIR + "/" + fname)
    new_objs = [o for o in bpy.data.objects if o not in before]
    src_arm = [o for o in new_objs if o.type == 'ARMATURE'][0]
    src_action = src_arm.animation_data.action
    assert src_action is not None, "no action in " + fname
    src_action.name = "src_" + target_name
    bpy.context.view_layer.objects.active = src_arm
    bpy.ops.object.mode_set(mode='POSE')
    bone_map = {b.name: b.name for b in rig.data.bones
                if b.name in src_arm.data.bones}
    p("retarget %s: mapped %d/%d bones" % (
        target_name, len(bone_map), len(rig.data.bones)))
    retarget_clip(src_arm, src_action, target_name, bone_map)
    bpy.data.actions.remove(src_action)
    bpy.data.objects.remove(src_arm, do_unlink=True)
# guard: a retarget that copies the rest pose (all-identity) must fail loudly
_walk = bpy.data.actions["Walk"]
_range = 0.0
for _fc in _walk.fcurves:
    if "LeftUpLeg" in _fc.data_path and "rotation_quaternion" in _fc.data_path:
        _vals = [k.co.y for k in _fc.keyframe_points]
        _range = max(_range, max(_vals) - min(_vals))
p("retarget guard: Walk LeftUpLeg quat range %.3f" % _range)
assert _range > 0.05, "retarget produced an all-identity Walk — source action not driving the pose (check use_nla)!"
# push all clips to NLA so the glTF exporter includes them
rig.animation_data.action = None
for clip in CLIPS:
    track = rig.animation_data.nla_tracks.new()
    track.name = clip
    strip = track.strips.new(clip, int(bpy.data.actions[clip].frame_range[0]),
                             bpy.data.actions[clip])
    strip.name = clip
rig.animation_data.action = bpy.data.actions["Idle_Weapon"]
# The .blend must open on the Idle action, NOT on the NLA stack: with
# use_nla=True all 7 strips play blended at once and the pose is a tangled
# mess (verified 11:33 — the renders showed the blend, not the action).
# The glTF exporter reads the NLA strips regardless of use_nla, so the
# export is unaffected.
rig.animation_data.use_nla = False
p("NLA tracks:", [t.name for t in rig.animation_data.nla_tracks])
# drop the orphan Warrior FBX actions so the GLB only carries the retargeted clips
for a in list(bpy.data.actions):
    if a.name.startswith("CharacterArmature|"):
        bpy.data.actions.remove(a)
p("actions left:", sorted(a.name for a in bpy.data.actions))
# clean the source out of the scene (GLB must contain only the MPFB hero)
for o in list(bpy.context.scene.objects):
    if o.name.startswith("CharacterArmature") or o.name in (
            "Warrior_Body", "Face", "ShoulderPad.L", "ShoulderPad.R",
            "Warrior_Sword"):
        # keep the KITBASHED pads/sword (now parented to the MPFB rig)
        if o.parent == rig:
            continue
        bpy.data.objects.remove(o, do_unlink=True)
p("scene objects now:", sorted(o.name for o in bpy.context.scene.objects))
# --- export GLB
bpy.ops.export_scene.gltf(filepath=GLB_OUT, export_format="GLB",
                          export_animations=True, export_skins=True,
                          export_apply=False, export_yup=True,
                          export_materials="EXPORT", export_force_sampling=True)
p("exported %s (%d bytes)" % (GLB_OUT, _os.path.getsize(GLB_OUT)))
bpy.context.scene.frame_set(1)  # clean idle on open
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
p("STAGE 6 DONE, saved", BLEND)
