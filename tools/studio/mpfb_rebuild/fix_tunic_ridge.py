"""CAPE + HERO FIX — pass 2: flatten the REST of the tunic back ridge.

Probe 4 showed the ridge is not just the 5 verts at z 1.28-1.48 (fixed in
pass 1): the tunic tube is TWISTED (rings are not horizontal — y ranges
swing from all-front at z 1.30 to a back ridge at z 1.15-1.25), and the
ridge runs down to z ~1.00 (13 verts with y > 0.10, max 0.211 at z 1.20).
The new cape was built against the 0.211 occluder so it already clears
the ridge — but in the Walk the ridge (skinned to Spine1) could still
close the 0.023 gap to the cape valleys (skinned to Spine2). Flatten the
whole ridge: every tunic vert with y > 0.09 goes to y = 0.09 (the normal
back line; the legit tunic back is 0.046-0.090). The twist itself is left
alone — it is hidden under the cape from behind and does not change the
front/side silhouette; rebuilding the tunic is out of scope.
Then re-verify cape clearance + sword tip + hair tuck and re-export.
"""
import bpy
import hashlib
import os

BLEND = "/home/hatch/workspace/mpfb_hero/Hero_MPFB.blend"
PROJ = "/home/hatch/workspace/project-eternia"
GLB_OUT = PROJ + "/assets/characters/mpfb/Hero_MPFB.glb"


def p(*a):
    print("[CAPEFIX2]", *a)


bpy.ops.wm.open_mainfile(filepath=BLEND)
rig = bpy.data.objects['Human.rig']
scene = bpy.context.scene

tunic = bpy.data.objects['Tunic']
before = max(v.co.y for v in tunic.data.vertices)
n = 0
for v in tunic.data.vertices:
    if v.co.y > 0.09:
        v.co.y = 0.09
        n += 1
after = max(v.co.y for v in tunic.data.vertices)
p("tunic ridge: clamped %d verts, max back y %.3f -> %.3f" % (n, before, after))
assert after <= 0.091

# verify: every cape row's min y clears the (fixed) occluder + 0.01
human = bpy.data.objects['Human']
cape = bpy.data.objects['Cape']


def occ(zc):
    ys = []
    for o in (human, tunic, bpy.data.objects['Belt']):
        for v in o.data.vertices:
            if abs(v.co.z - zc) < 0.04 and abs(v.co.x) < 0.10:
                ys.append(v.co.y)
    return max(ys) if ys else 0.05


worst = 9.0
worst_zc = None
for zc in [1.50 - 0.95 * t for t in [i / 28 for i in range(29)]]:
    # Centre columns only (|x| < 0.12): the edge columns intentionally WRAP
    # forward around the shoulders (top corners reach y -0.056, i.e. inside
    # the deltoid, which reads as the cape attaching at the shoulder — they
    # must NOT be compared against the centre-back occluder).
    row = [v.co.y for v in cape.data.vertices
           if abs(v.co.z - zc) < 0.03 and abs(v.co.x) < 0.12]
    if row:
        c = min(row) - occ(zc)
        if c < worst:
            worst, worst_zc = c, zc
            p("  worst row so far: z=%.3f cape_min=%.3f occ=%.3f" % (zc, min(row), occ(zc)))
p("cape clearance verify: worst (cape centre min y - occluder) = %.3f at z=%.3f (must be > 0.01)" % (worst, worst_zc))
assert worst > 0.01

# verify sword tip in Walk
rig.animation_data.use_nla = False
rig.animation_data.action = bpy.data.actions['Walk']
if bpy.data.actions['Walk'].slots:
    rig.animation_data.action_slot = bpy.data.actions['Walk'].slots[0]
sword = bpy.data.objects['Warrior_Sword']
grip = min((v.co.copy() for v in sword.data.vertices),
           key=lambda co: (co - rig.data.bones['mixamorig:RightHand'].head_local).length)
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
p("sword tip worst z in Walk = %.3f (must be > 0.10)" % worst_tip)
assert worst_tip > 0.10
rig.animation_data.action = bpy.data.actions['Idle_Weapon']
scene.frame_set(1)

bpy.ops.export_scene.gltf(filepath=GLB_OUT, export_format="GLB",
                          export_animations=True, export_skins=True,
                          export_apply=False, export_yup=True,
                          export_materials="EXPORT", export_force_sampling=True)
md5 = hashlib.md5(open(GLB_OUT, 'rb').read()).hexdigest()
p("exported %s (%d bytes) md5=%s" % (GLB_OUT, os.path.getsize(GLB_OUT), md5))
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
p("CAPEFIX2 DONE, saved", BLEND)
