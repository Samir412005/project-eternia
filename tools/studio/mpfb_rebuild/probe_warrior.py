"""Probe the Warrior FBX (retarget source) and Warrior_Anime GLB (kitbash source)."""
import bpy
from mathutils import Vector

def p(*a):
    print("[PROBE]", *a)

bpy.ops.wm.read_factory_settings(use_empty=True)
# --- FBX
bpy.ops.import_scene.fbx(
    filepath="/home/hatch/workspace/project-eternia/assets/characters/quaternius/Warrior.fbx")
arms = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE']
p("fbx armatures:", [o.name for o in arms])
arm = arms[0]
p("fbx bone count:", len(arm.data.bones))
# facing: Foot.L tail-head (toes point forward)
for bn in ["Foot.L", "Hips", "Head", "UpperArm.L", "Weapon.R"]:
    b = arm.data.bones.get(bn)
    if b:
        p("bone %-12s head=%s tail=%s" % (bn, tuple(round(c, 3) for c in b.head_local),
                                          tuple(round(c, 3) for c in b.tail_local)))
p("fbx actions:", [(a.name, (int(a.frame_range[0]), int(a.frame_range[1])))
                   for a in bpy.data.actions])
p("fbx object names:", [o.name for o in bpy.context.scene.objects][:12])
# --- GLB (kitbash source)
bpy.ops.import_scene.gltf(
    filepath="/home/hatch/workspace/project-eternia/assets/characters/quaternius/Warrior_Anime.glb")
p("glb objects:", [o.name for o in bpy.context.scene.objects])
for name in ["ShoulderPad_L", "ShoulderPad_R", "Warrior_Sword", "ShoulderPad.L",
             "ShoulderPad.R"]:
    o = bpy.data.objects.get(name)
    if o and o.type == 'MESH':
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        mn = Vector((min(c.x for c in bb), min(c.y for c in bb), min(c.z for c in bb)))
        mx = Vector((max(c.x for c in bb), max(c.y for c in bb), max(c.z for c in bb)))
        p("kitbash %-14s center=%s size=%s verts=%d mats=%s" % (
            name, tuple(round(c, 3) for c in (mn + mx) / 2),
            tuple(round(c, 3) for c in (mx - mn)), len(o.data.vertices),
            [m.name if m else None for m in o.data.materials]))
# the imported GLB rig: right hand + weapon bone positions
for o in bpy.context.scene.objects:
    if o.type == 'ARMATURE' and o.name != arm.name:
        for bn in ["Weapon.R", "Fist.R", "Hand.R", "Head"]:
            b = o.data.bones.get(bn)
            if b:
                p("glb-rig bone %-10s head=%s" % (bn, tuple(round(c, 3) for c in b.head_local)))
p("PROBE DONE")
