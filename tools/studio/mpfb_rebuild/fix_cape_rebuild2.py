"""CAPE + HERO FIX — pass 3: rebuild the cape against the FIXED occluder.

Pass 1 built the cape against the tunic's twisted back ridge (occluder
0.211 at z 1.20); pass 2 flattened the ridge to 0.09, which exposed that
the cape's fold valleys now dip 0.018 BELOW the flattened tunic back at
z 1.262 (the pass-1 occluder measurement at that height had missed the
ridge vert). Fix by rebuilding ONLY the cape (the cape-build block is
self-contained and idempotent: it deletes the old Cape object and builds
fresh from the current measurements). Hair / sword / pants / boots / face
from passes 1-2 are NOT touched here.
Base offset raised 0.035 -> 0.05 so the fold valleys keep ~0.03 clearance
over the tunic back even at the top rows.
"""
import bpy
import hashlib
import math
import os

BLEND = "/home/hatch/workspace/mpfb_hero/Hero_MPFB.blend"
PROJ = "/home/hatch/workspace/project-eternia"
GLB_OUT = PROJ + "/assets/characters/mpfb/Hero_MPFB.glb"
FOLD_PNG = PROJ + "/assets/characters/mpfb/Hero_MPFB_Cape_Folds.png"
N_FOLDS = 9


def p(*a):
    print("[CAPEFIX3]", *a)


def fold_shape(u):
    g = math.sin(2 * math.pi * N_FOLDS * u)
    return math.copysign(abs(g) ** 0.8, g)


bpy.ops.wm.open_mainfile(filepath=BLEND)
rig = bpy.data.objects['Human.rig']
human = bpy.data.objects['Human']
scene = bpy.context.scene
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.pose.transforms_clear()
bpy.ops.object.mode_set(mode='OBJECT')
rig.animation_data.use_nla = False
rig.animation_data.action = bpy.data.actions['Idle_Weapon']
scene.frame_set(1)


def body_back_y(zc, half_x=0.10):
    ys = []
    for o in (human, bpy.data.objects['Tunic'], bpy.data.objects['Belt']):
        for v in o.data.vertices:
            if abs(v.co.z - zc) < 0.04 and abs(v.co.x) < half_x:
                ys.append(v.co.y)
    return max(ys) if ys else 0.05


def walk_leg_max_y(z_lo, z_hi):
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


TOP_Z, HEM_Z = 1.50, 0.55
leg_055_065 = walk_leg_max_y(0.50, 0.65)
p("walk leg max y z 0.50-0.65: %.3f" % leg_055_065)
AMP_HEM = 0.015 + 0.070
_flare_need = (leg_055_065 + 0.08 + AMP_HEM) - (body_back_y(HEM_Z) + 0.05)
FLARE = max(0.12, min(0.30, _flare_need))
p("cape flare: %.3f (need %.3f)" % (FLARE, _flare_need))
assert _flare_need <= 0.30


def base_y(zc):
    t = (TOP_Z - zc) / (TOP_Z - HEM_Z)
    return body_back_y(zc) + 0.05 + FLARE * t * t


# --- rebuild the cape (same design as pass 1, fresh measurements) ---------
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
    t = ri / (ROWS - 1)
    z = TOP_Z + (HEM_Z - TOP_Z) * t
    w = TOP_W + (HEM_W - TOP_W) * t
    amp = 0.015 + 0.070 * t
    for ci in range(COLS):
        u = ci / (COLS - 1)
        s = u * 2 - 1
        x = s * w / 2
        f = fold_shape(u)
        y = base_y(z) + amp * f
        ae = abs(s)
        if ae > 0.8:
            y -= 0.12 * (1 - t) * (ae - 0.8) / 0.2
        zz = z + 0.03 * t * f
        cverts.append((x, y, zz))
        cuvs.append((u, t))
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
cape_me.calc_loop_triangles()
ny = sum(poly.normal.y for poly in cape_me.polygons) / len(cape_me.polygons)
if ny < 0:
    cape_me.flip_normals()
    p("cape winding flipped (mean normal.y was %.2f)" % ny)
cape_me.update()
cape_obj = bpy.data.objects.new("Cape", cape_me)
bpy.context.scene.collection.objects.link(cape_obj)
sol = cape_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
sol.thickness = 0.012
sol.offset = 0.0
bpy.context.view_layer.objects.active = cape_obj
bpy.ops.object.modifier_apply(modifier="Solidify")
cape_me = cape_obj.data
cape_me.calc_loop_triangles()
plus = sum(1 for poly in cape_me.polygons if poly.normal.y > 0)
p("cape rebuilt: verts=%d faces=%d normals +Y=%d/%d" % (
    len(cape_me.vertices), len(cape_me.polygons), plus, len(cape_me.polygons)))
hem_ys = [v.co.y for v in cape_me.vertices if v.co.z < 0.62]
p("cape hem min y=%.3f (walk leg %.3f) clearance %.3f" % (
    min(hem_ys), leg_055_065, min(hem_ys) - leg_055_065))
assert min(hem_ys) > leg_055_065 + 0.02, "cape hem does not clear the Walk leg swing!"
mid_ys = [v.co.y for v in cape_me.vertices if 0.95 < v.co.z < 1.05]
p("cape mid y spread=%.3f hem y spread=%.3f" % (
    max(mid_ys) - min(mid_ys), max(hem_ys) - min(hem_ys)))
cape_mat = bpy.data.materials.get("Cape_Red")
fold_img = bpy.data.images.get("Hero_MPFB_Cape_Folds")
if fold_img is None:
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
cape_obj.parent = rig
mod = cape_obj.modifiers.new(name="Armature", type="ARMATURE")
mod.object = rig
mod.use_vertex_groups = True
vg = cape_obj.vertex_groups.new(name="mixamorig:Spine2")
vg.add(list(range(len(cape_me.vertices))), 1.0, "REPLACE")
pin = cape_obj.vertex_groups.new(name="Pin")
pin.add(list(range(COLS)), 1.0, "REPLACE")
p("cape skinned to Spine2, Pin top row kept")

# --- verify: centre-column clearance at every row --------------------------
worst, worst_zc = 9.0, None
for zc in [1.50 - 0.95 * t for t in [i / 28 for i in range(29)]]:
    row = [v.co.y for v in cape_me.vertices
           if abs(v.co.z - zc) < 0.03 and abs(v.co.x) < 0.12]
    if row:
        c = min(row) - body_back_y(zc)
        if c < worst:
            worst, worst_zc = c, zc
p("cape clearance verify: worst centre (cape min y - occluder) = %.3f at z=%.3f (must be > 0.01)" % (worst, worst_zc))
assert worst > 0.01

# --- verify hair tuck still holds (cape moved closer to the body) -----------
worst_hair = -9.0
for v in bpy.data.objects['HairCards'].data.vertices:
    if v.co.z > 1.50:
        continue
    cy = base_y(max(0.55, min(1.50, v.co.z)))
    worst_hair = max(worst_hair, v.co.y - cy)
p("hair tuck verify: worst (hair_y - cape_centre_y) = %.3f (must be < -0.01)" % worst_hair)
assert worst_hair < -0.01

bpy.ops.export_scene.gltf(filepath=GLB_OUT, export_format="GLB",
                          export_animations=True, export_skins=True,
                          export_apply=False, export_yup=True,
                          export_materials="EXPORT", export_force_sampling=True)
md5 = hashlib.md5(open(GLB_OUT, 'rb').read()).hexdigest()
p("exported %s (%d bytes) md5=%s" % (GLB_OUT, os.path.getsize(GLB_OUT), md5))
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
p("CAPEFIX3 DONE, saved", BLEND)
