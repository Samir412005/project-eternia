"""CAPE + HERO FIX — pass 7: fix the HairCap's normals + re-export.

Probe 9: the HairCap has 1394 outward vs 1302 INWARD faces — half its
surface is backface-culled in Godot, so the skin shows through the crown
and the hero reads bald from the front/back. The "bowl-helmet" in runs
1-2 was the outline hull hiding this. Fix: recalculate the cap's normals
consistently outward, verify, re-export the GLB.
"""
import bpy
import hashlib
import os

BLEND = "/home/hatch/workspace/mpfb_hero/Hero_MPFB.blend"
PROJ = "/home/hatch/workspace/project-eternia"
GLB_OUT = PROJ + "/assets/characters/mpfb/Hero_MPFB.glb"


def p(*a):
    print("[CAPEFIX7]", *a)


bpy.ops.wm.open_mainfile(filepath=BLEND)
cap = bpy.data.objects['HairCap']
bpy.context.view_layer.objects.active = cap
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')
# verify against the head centre
from mathutils import Vector
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
head = max(meshes, key=lambda o: len(o.data.vertices))
c = Vector((0, 0, 0))
for v in head.data.vertices:
    c += v.co
c /= len(head.data.vertices)
out = inn = 0
for f in cap.data.polygons:
    if f.normal.dot(f.center - c) > 0:
        out += 1
    else:
        inn += 1
p("cap faces after recalc: outward=%d inward=%d" % (out, inn))
assert out > inn * 4, "recalc did not fix the winding!"
bpy.ops.export_scene.gltf(filepath=GLB_OUT, export_format="GLB",
                          export_animations=True, export_skins=True,
                          export_apply=False, export_yup=True,
                          export_materials="EXPORT", export_force_sampling=True)
md5 = hashlib.md5(open(GLB_OUT, 'rb').read()).hexdigest()
p("exported %s (%d bytes) md5=%s" % (GLB_OUT, os.path.getsize(GLB_OUT), md5))
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
p("CAPEFIX7 DONE, saved", BLEND)
