"""CAPE + HERO FIX — Blender pass (cape radical rebuild + ponytail tuck +
sword shorten/re-aim + pants/boot ankle overlap + face image repoint).

DIAGNOSIS (probes 2026-11-15, read from the saved .blend + shots 10/11):
  * Cape reads flat NOT because the mesh lacks folds (old simmed cape HAD
    hem y-spread 0.337) but because (a) the toon shader bands by NDL only,
    so one flat band covered the whole cloth, and (b) the old cape was
    BURIED in the tunic through the torso (cape y 0.06-0.09 vs tunic back
    ~0.10) and its hem swung FORWARD through the legs (hem centre y -0.106).
  * The dark shape on the cape's upper centre is the TUNIC SPIKE, not the
    ponytail: the tunic's top ring was built from a body measurement that
    caught an arm vert, so its back bulges to y 0.214 at z ~1.39 and stabs
    straight through the cape — visible as a blue fin in the Blender back
    render (checks/cape_back.png). The ponytail ALSO weaves in and out of
    the cape (hair max y 0.132-0.147 vs cape 0.060-0.125), so it gets
    tucked too. Both causes are fixed, not just the symptom.
  * The dark grey shape lower on the cape is the LEG/BOOT swinging back
    THROUGH the cape in the Walk (boot max y 0.433, pants 0.316; cape hem
    max y 0.231).
  * The SWORD blade is 1.235 m long (build comment said 0.68 m — the 0.28
    scale was applied to a ~4.4 m FBX sword), so its tip goes 0.31 m UNDER
    the ground in the Walk. It points forward-down, not along the arm.

FIXES (this script, surgical — no full rebuild):
  1. CAPE rebuilt as modelled draped cloth: 25x29 grid, 9 pleats with real
     depth (amp 0.015 -> 0.085), shaped fold profile, wavy hem (z varies
     per fold), side wrap over the shoulders, outward bow that clears the
     measured tunic/body occluder + 0.035 AND the Walk leg swing, hem
     raised to the knee (z 0.55) so the swinging shin/boot pass UNDER it.
     Solidify 0.012 applied (real thickness). UVs kept: u across,
     v=0 top -> 1 hem (sway shader contract). Fold texture node added
     to Cape_Red (phase-matched to Hero_MPFB_Cape_Folds.png).
  2. PONYTAIL tucked UNDER the cape: the crossed y-plane card is deleted;
     the x-plane + back-hair rows below z 1.50 are moved to body-back +
     0.008, so no hair can poke through the cloth.
  3. SWORD: scaled 0.50 about the grip (blade 1.235 -> 0.62 m) and rotated
     about the grip so the blade follows the forearm direction in rest.
  4. PANTS bottom ring 0.16 -> 0.08; BOOT top 0.14 -> 0.20 (ankle overlap).
  5. Face image repointed at the MPFB copy (repainted, bigger/brighter
     eyes) and reloaded, so the GLB embeds the new face, not the old
     quaternius one. No Warrior_Anime file is touched.

Run: ~/workspace/tools/blender-4.5/blender --background --python \
        tools/studio/mpfb_rebuild/fix_cape_hero.py
Saves: /home/hatch/workspace/mpfb_hero/Hero_MPFB.blend (backup .bak-capefix)
Exports: assets/characters/mpfb/Hero_MPFB.glb
"""
import bpy
import math
import os
import shutil
import hashlib
from mathutils import Vector

BLEND = "/home/hatch/workspace/mpfb_hero/Hero_MPFB.blend"
BAK = BLEND + ".bak-capefix"
PROJ = "/home/hatch/workspace/project-eternia"
GLB_OUT = PROJ + "/assets/characters/mpfb/Hero_MPFB.glb"
FACE_PNG = PROJ + "/assets/characters/mpfb/Hero_MPFB_Warrior_Face_Anime.png"
FOLD_PNG = PROJ + "/assets/characters/mpfb/Hero_MPFB_Cape_Folds.png"

N_FOLDS = 9


def p(*a):
    print("[CAPEFIX]", *a)


def fold_shape(u):
    """Shaped fold profile, phase-matched to the PIL fold texture:
    sin(2*pi*9*u), ridges broadened (|g|**0.8). +1 = ridge (most outward)."""
    g = math.sin(2 * math.pi * N_FOLDS * u)
    return math.copysign(abs(g) ** 0.8, g)


if not os.path.exists(BAK):
    shutil.copy2(BLEND, BAK)
    p("backed up .blend to", BAK)
else:
    p("backup already exists, keeping", BAK)

bpy.ops.wm.open_mainfile(filepath=BLEND)
rig = bpy.data.objects['Human.rig']
human = bpy.data.objects['Human']
scene = bpy.context.scene

# --- reset pose ------------------------------------------------------------
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.pose.transforms_clear()
bpy.ops.object.mode_set(mode='OBJECT')
rig.animation_data.use_nla = False
rig.animation_data.action = bpy.data.actions['Idle_Weapon']
scene.frame_set(1)


def body_back_y(zc, half_x=0.10):
    """Max +Y of Human+Tunic+Belt verts near height zc (centre back line)."""
    ys = []
    for o in (human, bpy.data.objects['Tunic'], bpy.data.objects['Belt']):
        for v in o.data.vertices:
            if abs(v.co.z - zc) < 0.04 and abs(v.co.x) < half_x:
                ys.append(v.co.y)
    return max(ys) if ys else 0.05


def walk_leg_max_y(z_lo, z_hi):
    """Max +Y reached by Human+Pants+Boots verts in a z-band over Walk
    frames 1/8/15/22/30 (evaluated). The cape must stay behind this."""
    rig.animation_data.action = bpy.data.actions['Walk']
    if bpy.data.actions['Walk'].slots:
        rig.animation_data.action_slot = bpy.data.actions['Walk'].slots[0]
    worst = -9.0
    for f in (1, 8, 15, 22, 30):
        scene.frame_set(f)
        bpy.context.view_layer.update()
        deps = bpy.context.evaluated_depsgraph_get()
        for name in ('Human', 'Pants_L', 'Pants_R', 'Boot_L', 'Boot_R'):
            o = bpy.data.objects[name]
            ev = o.evaluated_get(deps)
            mw = ev.matrix_world
            for v in ev.data.vertices:
                w = mw @ v.co
                if z_lo <= w.z <= z_hi and w.y > worst:
                    worst = w.y
    rig.animation_data.action = bpy.data.actions['Idle_Weapon']
    scene.frame_set(1)
    return worst


# --- 0. FLATTEN THE TUNIC SPIKE (the real cause of the dark shape) -------
# The Blender back render (checks/cape_back.png) shows it plainly: a BLUE
# vertical fin stabbing through the cape's upper centre. Cause: the tunic's
# top ring was built from body_extent(1.46), which caught an arm/shoulder
# vert, so the ring is ~0.16 deep and its back bulges to y 0.214 at
# z ~1.39 — straight through the cape (y 0.06-0.09). It is NOT the
# ponytail (the brown hair above the cape is fine). Clamp the tunic's
# upper-back verts to the normal back line (y 0.09) BEFORE measuring the
# occluder, so the new cape is built against the fixed body.
tunic = bpy.data.objects['Tunic']
spike_before = max(v.co.y for v in tunic.data.vertices if 1.28 < v.co.z < 1.48)
clamped = 0
for v in tunic.data.vertices:
    if 1.28 < v.co.z < 1.48 and v.co.y > 0.09:
        v.co.y = 0.09
        clamped += 1
spike_after = max(v.co.y for v in tunic.data.vertices if 1.28 < v.co.z < 1.48)
p("tunic spike: max back y 1.28<z<1.48 was %.3f, clamped %d verts -> %.3f" % (
    spike_before, clamped, spike_after))
assert spike_after <= 0.091, "tunic spike not flattened!"

# --- measure clearances ----------------------------------------------------
TOP_Z, HEM_Z = 1.50, 0.55
for zc in (1.50, 1.40, 1.20, 1.00, 0.80, 0.60, 0.55):
    p("occluder rest back y at z=%.2f: %.3f" % (zc, body_back_y(zc)))
leg_055_065 = walk_leg_max_y(0.50, 0.65)
leg_065_080 = walk_leg_max_y(0.65, 0.80)
p("walk leg max y z 0.50-0.65: %.3f ; z 0.65-0.80: %.3f" % (leg_055_065, leg_065_080))

# Cape centre-line base y(z): clear the rest occluder + 0.035, flare out
# toward the hem, and stay behind the Walk leg swing at the hem.
# The flare is ADAPTIVE: the hem fold valleys must clear the measured
# knee-band leg swing + 0.02, otherwise the legs poke through the cloth
# again (the shot-11 dark shape). Cap the flare at 0.30 (a bigger bell
# would read as a tent, not a cloak).
AMP_HEM = 0.015 + 0.070  # fold amp at the hem
# +0.08 margin (not 0.02): the rows just above the hem sit ~0.02-0.03
# lower than the hem valley, the Solidify inner shell sits 0.006 further
# in, and the assert checks all verts with z < 0.62.
_flare_need = (leg_055_065 + 0.08 + AMP_HEM) - (body_back_y(HEM_Z) + 0.035)
FLARE = max(0.12, min(0.30, _flare_need))
p("cape flare: %.3f (need %.3f for hem clearance)" % (FLARE, _flare_need))
assert _flare_need <= 0.30, "hem clearance needs an absurd flare!"


def base_y(zc):
    t = (TOP_Z - zc) / (TOP_Z - HEM_Z)
    y = body_back_y(zc) + 0.035 + FLARE * t * t
    return y


def cape_centre_y(zc):
    return base_y(zc)


# --- 1. REBUILD THE CAPE ---------------------------------------------------
old_cape = bpy.data.objects.get('Cape')
old_me = old_cape.data if old_cape else None
if old_cape:
    bpy.data.objects.remove(old_cape, do_unlink=True)
if old_me and old_me.users == 0:
    bpy.data.meshes.remove(old_me)

COLS, ROWS = 25, 29
TOP_W, HEM_W = 0.52, 1.15
cverts, cuvs, cfaces = [], [], []
for ri in range(ROWS):
    t = ri / (ROWS - 1)  # 0 top -> 1 hem
    z = TOP_Z + (HEM_Z - TOP_Z) * t
    w = TOP_W + (HEM_W - TOP_W) * t
    amp = 0.015 + 0.070 * t  # fold depth grows toward the hem
    for ci in range(COLS):
        u = ci / (COLS - 1)
        s = u * 2 - 1  # -1 .. 1 across
        x = s * w / 2
        f = fold_shape(u)
        y = base_y(z) + amp * f
        # side wrap: edges curl forward around the shoulders/torso.
        # Strong at the top, ZERO at the hem (wrapped hem corners would
        # swing into the legs).
        ae = abs(s)
        if ae > 0.8:
            y -= 0.12 * (1 - t) * (ae - 0.8) / 0.2
        # wavy hem: ridges hang lower, valleys higher
        zz = z + 0.03 * t * f
        cverts.append((x, y, zz))
        cuvs.append((u, t))  # v=0 top, 1 hem (sway shader contract)
for ri in range(ROWS - 1):
    for ci in range(COLS - 1):
        a = ri * COLS + ci
        b = a + 1
        c = a + COLS
        dd = c + 1
        cfaces.append((a, b, dd, c))
cape_me = bpy.data.meshes.new("Cape")
cape_me.from_pydata(cverts, [], cfaces)
cape_me.update()
uvl = cape_me.uv_layers.new(name="UVMap")
for loop in cape_me.loops:
    uvl.data[loop.index].uv = cuvs[loop.vertex_index]
# outward normals (+Y = back, toward the back camera); flip if wound inside-out
cape_me.calc_loop_triangles()
ny = sum(poly.normal.y for poly in cape_me.polygons) / len(cape_me.polygons)
if ny < 0:
    cape_me.flip_normals()
    p("cape winding flipped (mean normal.y was %.2f)" % ny)
cape_me.update()
# real thickness
cape_obj = bpy.data.objects.new("Cape", cape_me)
bpy.context.scene.collection.objects.link(cape_obj)
sol = cape_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
sol.thickness = 0.012
sol.offset = 0.0  # centred: 6 mm out, 6 mm in
bpy.context.view_layer.objects.active = cape_obj
bpy.ops.object.modifier_apply(modifier="Solidify")
cape_me = cape_obj.data
cape_me.calc_loop_triangles()
plus = sum(1 for poly in cape_me.polygons if poly.normal.y > 0)
p("cape rebuilt: verts=%d faces=%d normals +Y=%d/%d" % (
    len(cape_me.vertices), len(cape_me.polygons), plus, len(cape_me.polygons)))
# hem clearance check (rest pose): min y at the hem vs Walk leg swing
hem_ys = [v.co.y for v in cape_me.vertices if v.co.z < 0.62]
p("cape hem min y=%.3f (walk leg max y 0.50-0.65 was %.3f) clearance %.3f" % (
    min(hem_ys), leg_055_065, min(hem_ys) - leg_055_065))
assert min(hem_ys) > leg_055_065 + 0.02, "cape hem does not clear the Walk leg swing!"
# fold depth check
mid_ys = [v.co.y for v in cape_me.vertices if 0.95 < v.co.z < 1.05]
p("cape mid y spread=%.3f hem y spread=%.3f" % (
    max(mid_ys) - min(mid_ys), max(hem_ys) - min(hem_ys)))
# material: deep red + fold texture node (Blender renders + GLB carry it)
cape_mat = bpy.data.materials.get("Cape_Red")
if cape_mat is None:
    cape_mat = bpy.data.materials.new(name="Cape_Red")
    cape_mat.use_nodes = True
    bsdf = cape_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.55, 0.07, 0.08, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
fold_img = bpy.data.images.load(FOLD_PNG)
fold_img.name = "Hero_MPFB_Cape_Folds"
nt = cape_mat.node_tree
bsdf = nt.nodes["Principled BSDF"]
for n in list(nt.nodes):
    if n.type == 'TEX_IMAGE':
        nt.nodes.remove(n)
tex = nt.nodes.new(type="ShaderNodeTexImage")
tex.image = fold_img
nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
cape_me.materials.append(cape_mat)
# skin 100% to Spine2, keep the Pin group (top row) for compatibility
cape_obj.parent = rig
mod = cape_obj.modifiers.new(name="Armature", type="ARMATURE")
mod.object = rig
mod.use_vertex_groups = True
vg = cape_obj.vertex_groups.new(name="mixamorig:Spine2")
vg.add(list(range(len(cape_me.vertices))), 1.0, "REPLACE")
pin = cape_obj.vertex_groups.new(name="Pin")
pin.add(list(range(COLS)), 1.0, "REPLACE")
p("cape skinned to Spine2, Pin top row kept")

# --- 2. TUCK THE HAIR UNDER THE CAPE ---------------------------------------
# HairCards layout (from build_hero.py add_card order): fringe 0-39,
# side locks 40-79, back hair 80-135 (2 cards x 28 verts, 7 rows x 4 cols,
# rows z = 1.63..1.42), ponytail 136-159 (x-plane 136-147, y-plane 148-159).
# The y-plane card is DELETED (it is what stuck out beyond the cloth);
# back-hair rows with z <= 1.50 and ponytail rows with z <= 1.50 are moved
# to body-back + 0.008, i.e. between the body and the cape, hidden.
hair = bpy.data.objects['HairCards']
hme = hair.data
BACK_ROWS_Z = [1.63, 1.60, 1.57, 1.54, 1.50, 1.46, 1.42]
PONY_ROWS_Z = [1.55, 1.45, 1.35, 1.25, 1.15, 1.08]
tucked = 0
for vi, v in enumerate(hme.vertices):
    z = v.co.z
    tuck = None
    if 80 <= vi < 136:  # back hair
        card_row = (vi - 80) % 28 // 4
        rz = BACK_ROWS_Z[card_row]
        if rz <= 1.50:
            tuck = body_back_y(rz) + 0.008
    elif 136 <= vi < 148:  # ponytail x-plane (rows of 2)
        rz = PONY_ROWS_Z[(vi - 136) // 2]
        if rz <= 1.50:
            tuck = body_back_y(rz) + 0.008
    if tuck is not None:
        v.co.y = tuck
        tucked += 1
p("hair tucked: %d verts moved under the cape" % tucked)
# delete the ponytail y-plane card: verts 148-159 + its faces (last 5 quads)
keep_verts = [i for i in range(len(hme.vertices)) if i < 148]
# faces: ponytail planes are the last 10 faces (5 per plane); y-plane = last 5
faces = [tuple(f.vertices) for f in hme.polygons]
faces = faces[:-5]
uv_layer = hme.uv_layers.active.data
loop_uv = {}
for li, loop in enumerate(hme.loops):
    loop_uv.setdefault(loop.vertex_index, []).append(tuple(uv_layer[li].uv))
new_verts = [tuple(hme.vertices[i].co) for i in keep_verts]
new_me = bpy.data.meshes.new("HairCards")
new_me.from_pydata(new_verts, [], faces)
new_me.update()
new_uvl = new_me.uv_layers.new(name="UVMap")
# assign UVs: for each loop, take the first stored UV of that vertex
for loop in new_me.loops:
    new_uvl.data[loop.index].uv = loop_uv[loop.vertex_index][0]
new_me.materials.append(hme.materials[0])
hair.data = new_me
bpy.data.meshes.remove(hme)
# re-add the Head vertex group (rebuild drops it)
vg = hair.vertex_groups.new(name="mixamorig:Head")
vg.add(list(range(len(new_me.vertices))), 1.0, "REPLACE")
p("ponytail y-plane deleted: hair verts=%d faces=%d" % (
    len(new_me.vertices), len(new_me.polygons)))
assert len(new_me.vertices) == 148 and len(new_me.polygons) == 89, \
    "hair rebuild counts wrong!"

# --- 3. SWORD: shorten 1.235 -> 0.62 m + aim along the forearm -------------
sword = bpy.data.objects['Warrior_Sword']
hand = rig.data.bones['mixamorig:RightHand'].head_local
sverts = [v.co.copy() for v in sword.data.vertices]
grip = min(sverts, key=lambda co: (co - hand).length)
gi = min(range(len(sverts)), key=lambda i: (sverts[i] - hand).length)
tip = max(sverts, key=lambda co: (co - grip).length)
blade_len = (tip - grip).length
p("sword before: blade_len=%.3f grip=%s" % (blade_len, tuple(round(c, 2) for c in grip)))
fa = rig.data.bones['mixamorig:RightForeArm']
target_dir = (fa.tail_local - fa.head_local).normalized()
cur_dir = (tip - grip).normalized()
rot = cur_dir.rotation_difference(target_dir)
scale = 0.62 / blade_len
for v in sword.data.vertices:
    v.co = grip + (rot @ (v.co - grip)) * scale
sverts = [v.co.copy() for v in sword.data.vertices]
tip2 = max(sverts, key=lambda co: (co - grip).length)
p("sword after: blade_len=%.3f tip=%s (target dir %s)" % (
    (tip2 - grip).length, tuple(round(c, 2) for c in tip2),
    tuple(round(c, 2) for c in target_dir)))
assert abs((tip2 - grip).length - 0.62) < 0.01, "sword rescale failed!"

# --- 4. PANTS + BOOTS: close the ankle gap ----------------------------------
for side in ("L", "R"):
    pants = bpy.data.objects['Pants_' + side]
    bottom = [v for v in pants.data.vertices if v.co.z < 0.17]
    assert len(bottom) == 12, "Pants_%s bottom ring: %d verts (want 12)" % (side, len(bottom))
    for v in bottom:
        v.co.z = 0.08
    boot = bpy.data.objects['Boot_' + side]
    top = [v for v in boot.data.vertices if v.co.z > 0.13]
    assert len(top) == 4, "Boot_%s top face: %d verts (want 4)" % (side, len(top))
    for v in top:
        v.co.z = 0.20
    p("Pants_%s bottom -> z 0.08, Boot_%s top -> z 0.20 (overlap 0.12)" % (side, side))

# --- 5. FACE IMAGE: repoint at the repainted MPFB copy -----------------------
face_img = bpy.data.images.get('Warrior_Face_Anime')
assert face_img is not None, "face image missing from .blend!"
face_img.filepath = FACE_PNG
face_img.reload()
p("face image repointed: %s size=%s" % (face_img.filepath, tuple(face_img.size)))
assert tuple(face_img.size) == (1024, 1024)

# --- verify in the Walk ------------------------------------------------------
rig.animation_data.action = bpy.data.actions['Walk']
if bpy.data.actions['Walk'].slots:
    rig.animation_data.action_slot = bpy.data.actions['Walk'].slots[0]
sword = bpy.data.objects['Warrior_Sword']
ti = max(range(len(sword.data.vertices)),
         key=lambda i: (sword.data.vertices[i].co - grip).length)
worst_tip = 9.0
for f in (1, 8, 15, 22, 30):
    scene.frame_set(f)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    ev = sword.evaluated_get(deps)
    tip_w = ev.matrix_world @ ev.data.vertices[ti].co
    worst_tip = min(worst_tip, tip_w.z)
    p("walk verify f=%d sword tip_z=%.3f" % (f, tip_w.z))
assert worst_tip > 0.10, "sword tip still near/below ground: %.3f" % worst_tip
p("sword tip clears ground in Walk (worst tip_z=%.3f)" % worst_tip)
# hair tuck verify: no hair vert outside the cape surface at the same z
cape = bpy.data.objects['Cape']
worst_hair = -9.0
for v in bpy.data.objects['HairCards'].data.vertices:
    if v.co.z > 1.50:
        continue
    cy = cape_centre_y(max(0.55, min(1.50, v.co.z)))
    worst_hair = max(worst_hair, v.co.y - cy)
p("hair tuck verify: worst (hair_y - cape_centre_y) below z 1.50 = %.3f (must be < -0.01)" % worst_hair)
assert worst_hair < -0.01, "hair still pokes through the cape!"
rig.animation_data.action = bpy.data.actions['Idle_Weapon']
scene.frame_set(1)

# --- export + save -----------------------------------------------------------
bpy.ops.export_scene.gltf(filepath=GLB_OUT, export_format="GLB",
                          export_animations=True, export_skins=True,
                          export_apply=False, export_yup=True,
                          export_materials="EXPORT", export_force_sampling=True)
md5 = hashlib.md5(open(GLB_OUT, 'rb').read()).hexdigest()
p("exported %s (%d bytes) md5=%s" % (GLB_OUT, os.path.getsize(GLB_OUT), md5))
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
p("CAPEFIX DONE, saved", BLEND)
