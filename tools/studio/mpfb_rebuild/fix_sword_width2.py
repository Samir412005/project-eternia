"""CAPE + HERO FIX — pass 6: restore the sword blade's width (length-only).

Pass 5 deleted the 302 stray verts (the black blob at the tip) and the
blade now reads as a clean sword, but it is a foil: 0.036 m wide at
0.612 m long. The blade was halved in width by pass 1's uniform 0.50
rescale (the original kitbash width was 0.072 m). Fix: stretch ONLY the
components PERPENDICULAR to the blade axis by 2.0x, for verts past the
guard (par > 0.12) — the guard/pommel near the grip stay as-is, the tip
stays on the axis (its perp is ~0) so the length cannot grow. Now safe:
the fragments that polluted the first width attempt are gone.
"""
import bpy
import hashlib
import os
from mathutils import Vector

BLEND = "/home/hatch/workspace/mpfb_hero/Hero_MPFB.blend"
PROJ = "/home/hatch/workspace/project-eternia"
GLB_OUT = PROJ + "/assets/characters/mpfb/Hero_MPFB.glb"


def p(*a):
    print("[CAPEFIX6]", *a)


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
hand = rig.data.bones['mixamorig:RightHand'].head_local
sverts = [v.co.copy() for v in sword.data.vertices]
grip = min(sverts, key=lambda co: (co - hand).length)
tip = max(sverts, key=lambda co: (co - grip).length)
blade_dir = (tip - grip).normalized()
blade_len = (tip - grip).length
w_before = max(((v - grip) - blade_dir * ((v - grip).dot(blade_dir))).length
               for v in sverts if (v - grip).dot(blade_dir) > 0.12)
p("sword before: verts=%d len=%.3f blade_width=%.3f" % (
    len(sverts), blade_len, 2 * w_before))
for v in sword.data.vertices:
    off = v.co - grip
    par = off.dot(blade_dir)
    if par > 0.12:
        perp = off - blade_dir * par
        v.co = grip + blade_dir * par + perp * 2.0
sverts = [v.co.copy() for v in sword.data.vertices]
tip2 = max(sverts, key=lambda co: (co - grip).length)
w_after = max(((v - grip) - blade_dir * ((v - grip).dot(blade_dir))).length
              for v in sverts if (v - grip).dot(blade_dir) > 0.12)
p("sword after: len=%.3f blade_width=%.3f" % ((tip2 - grip).length, 2 * w_after))
assert abs((tip2 - grip).length - blade_len) < 0.01, "blade length changed!"
assert abs(w_after - 2.0 * w_before) < 0.005, "blade width did not double!"

rig.animation_data.action = bpy.data.actions['Walk']
if bpy.data.actions['Walk'].slots:
    rig.animation_data.action_slot = bpy.data.actions['Walk'].slots[0]
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
p("CAPEFIX6 DONE, saved", BLEND)
