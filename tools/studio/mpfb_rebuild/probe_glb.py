"""Probe the exported Hero_MPFB.glb: facing, bone names, animations, and
render the Walk clip mid-stride + Idle from the front to verify the retarget."""
import bpy
from mathutils import Vector

def p(*a):
    print("[PROBE-GLB]", *a)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(
    filepath="/home/hatch/workspace/project-eternia/assets/characters/mpfb/Hero_MPFB.glb")
objs = bpy.context.scene.objects
p("objects:", sorted(o.name for o in objs))
arm = [o for o in objs if o.type == 'ARMATURE'][0]
p("armature:", arm.name, "bones:", len(arm.data.bones))
# facing: find the Face_Anime mesh and the nose direction (face verts have
# the most negative Y in Blender after a glTF import? print the face centre)
for o in objs:
    if o.type == 'MESH' and o.data.materials:
        mats = [m.name if m else None for m in o.data.materials]
        if "Face_Anime" in mats or "HairCards" in mats or "Cape_Red" in mats:
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
            mn = Vector((min(c.x for c in bb), min(c.y for c in bb), min(c.z for c in bb)))
            mx = Vector((max(c.x for c in bb), max(c.y for c in bb), max(c.z for c in bb)))
            p("mesh %-12s centre=%s size=%s mats=%s" % (
                o.name, tuple(round(c, 2) for c in (mn + mx) / 2),
                tuple(round(c, 2) for c in (mx - mn)), mats))
# the head bone's forward: the nose is the most -Y (or +Y) head vertex
human = bpy.data.objects.get("Human")
if human:
    nose = max(human.data.vertices, key=lambda v: -v.co.y if v.co.z > 1.5 else -99)
    # instead: the face-centre vertex average for face-region verts
    face_verts = [v.co for v in human.data.vertices
                  if v.co.z > 1.5 and v.co.z < 1.62]
    if face_verts:
        avg_y = sum(v.y for v in face_verts) / len(face_verts)
        p("head front (face verts) avg y=%.3f (negative = faces -Y)" % avg_y)
p("actions:", sorted(a.name for a in bpy.data.actions))
for a in bpy.data.actions:
    p("action %-14s frames %d-%d fcurves=%d" % (
        a.name, int(a.frame_range[0]), int(a.frame_range[1]),
        sum(len(fc.data_path) for fc in a.fcurves) if hasattr(a, 'fcurves') else 0))
# verify the walk clip actually moves the legs: sample the LeftUpLeg rotation
rig = arm
if not rig.animation_data:
    rig.animation_data_create()
walk = bpy.data.actions.get("Walk")
if walk:
    rig.animation_data.action = walk
    for f in (1, 8, 16, 24, 31):
        bpy.context.scene.frame_set(f)
        bpy.context.view_layer.update()
        for bn in ("mixamorig:LeftUpLeg", "mixamorig:RightUpLeg",
                   "mixamorig:Hips", "mixamorig:LeftArm"):
            pb = rig.pose.bones.get(bn)
            if pb:
                p("Walk f=%2d %-22s rot=%s loc=%s" % (
                    f, bn, tuple(round(c, 2) for c in pb.rotation_quaternion),
                    tuple(round(c, 2) for c in pb.location)))
p("PROBE-GLB DONE")
