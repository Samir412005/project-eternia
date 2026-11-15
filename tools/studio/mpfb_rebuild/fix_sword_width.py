"""CAPE + HERO FIX — pass 5: delete the sword's stray fragments + re-export.

Probe 7: the Warrior_Sword mesh is 7 DISCONNECTED components. Only the
largest (150 verts, spans grip -> tip) is the sword. The other 6 (302
verts) are a clump near the tip — kitbash junk (verts baked from other
bones / a broken scabbard piece) — and they render as the black blob at
the sword's end in shots 09/38, which is why the blade read as a needle
with a blob instead of a sword. The uniform 0.50 rescale in pass 1 was
NOT the problem (the blade width was never the issue), so it is reverted
here by DELETING the fragments instead of widening anything.
Also re-exports the GLB so it embeds the pass-2b repainted face texture
(bigger/brighter eyes) — the .blend's face image loads the current MPFB
PNG on open.
"""
import bpy
import hashlib
import os
from mathutils import Vector

BLEND = "/home/hatch/workspace/mpfb_hero/Hero_MPFB.blend"
PROJ = "/home/hatch/workspace/project-eternia"
GLB_OUT = PROJ + "/assets/characters/mpfb/Hero_MPFB.glb"


def p(*a):
    print("[CAPEFIX5]", *a)


bpy.ops.wm.open_mainfile(filepath=BLEND)
rig = bpy.data.objects['Human.rig']
scene = bpy.context.scene
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.pose.transforms_clear()
bpy.ops.object.mode_set(mode='OBJECT')
rig.animation_data.use_nla = False
rig.animation_data.action = bpy.data.actions['Idle_Weapon']
scene.frame_set(1)

sword = bpy.data.objects['Warrior_Sword']
me = sword.data
hand = rig.data.bones['mixamorig:RightHand'].head_local
verts = [v.co.copy() for v in me.vertices]
grip_i = min(range(len(verts)), key=lambda i: (verts[i] - hand).length)
# connected components via faces
parent = list(range(len(verts)))


def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a


def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb


for f in me.polygons:
    vs = list(f.vertices)
    for i in range(1, len(vs)):
        union(vs[0], vs[i])
keep_root = find(grip_i)
keep = [i for i in range(len(verts)) if find(i) == keep_root]
drop = len(verts) - len(keep)
p("sword components: keeping %d verts (grip component), dropping %d stray verts" % (len(keep), drop))
assert len(keep) > 100, "grip component too small — wrong component!"
# rebuild the mesh from the kept component (remap faces + UVs)
remap = {old: new for new, old in enumerate(keep)}
faces = []
for f in me.polygons:
    if all(v in remap for v in f.vertices):
        faces.append(tuple(remap[v] for v in f.vertices))
uv_layer = me.uv_layers.active.data if me.uv_layers else None
loop_uv = {}
if uv_layer:
    for li, loop in enumerate(me.loops):
        loop_uv.setdefault(loop.vertex_index, []).append(tuple(uv_layer[li].uv))
new_me = bpy.data.meshes.new("Warrior_Sword")
new_me.from_pydata([tuple(verts[i]) for i in keep], [], faces)
new_me.update()
if uv_layer:
    new_uvl = new_me.uv_layers.new(name="UVMap")
    for loop in new_me.loops:
        new_uvl.data[loop.index].uv = loop_uv[keep[loop.vertex_index]][0]
for m in me.materials:
    new_me.materials.append(m)
sword.data = new_me
bpy.data.meshes.remove(me)
# re-add the RightHand vertex group (rebuild drops it)
vg = sword.vertex_groups.new(name="mixamorig:RightHand")
vg.add(list(range(len(new_me.vertices))), 1.0, "REPLACE")
# measure the cleaned sword
sverts = [v.co.copy() for v in new_me.vertices]
grip = min(sverts, key=lambda co: (co - hand).length)
tip = max(sverts, key=lambda co: (co - grip).length)
blade_dir = (tip - grip).normalized()
blade_len = (tip - grip).length
w = max(((v - grip) - blade_dir * ((v - grip).dot(blade_dir))).length
        for v in sverts if (v - grip).dot(blade_dir) > 0.12)
p("sword cleaned: verts=%d len=%.3f blade_width=%.3f tip=%s" % (
    len(sverts), blade_len, w, tuple(round(c, 2) for c in tip)))
assert abs(blade_len - 0.62) < 0.02, "blade length changed!"
assert w < 0.12, "blade still has a wide stray piece!"

# verify tip still clears the ground in the Walk
rig.animation_data.action = bpy.data.actions['Walk']
if bpy.data.actions['Walk'].slots:
    rig.animation_data.action_slot = bpy.data.actions['Walk'].slots[0]
ti = max(range(len(new_me.vertices)),
         key=lambda i: (new_me.vertices[i].co - grip).length)
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
p("CAPEFIX5 DONE, saved", BLEND)
