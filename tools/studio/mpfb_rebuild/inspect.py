"""Inspect MPFB base + rigs + Quaternius sources. Prints facts only, saves nothing."""
import bpy
import json
import os

# MPFB loads only as the bl_ext extension (plain `import mpfb` breaks on
# MPFB_CONTEXTUAL_INFORMATION=None). Enable first, import via bl_ext path.
bpy.ops.preferences.addon_enable(module="bl_ext.user_default.mpfb")

BLENDER = os.path.expanduser("~/.config/blender/4.5/extensions/user_default/mpfb")

def p(*a):
    print("[INSPECT]", *a)

# --- clean scene ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# --- MPFB human ---
from bl_ext.user_default.mpfb.services.humanservice import HumanService
human = HumanService.create_human()
p("human object:", human.name, "verts:", len(human.data.vertices),
  "polys:", len(human.data.polygons), "dims:", tuple(round(v, 3) for v in human.dimensions))
p("uv layers:", [uv.name for uv in human.data.uv_layers])
p("materials:", [m.name if m else None for m in human.data.materials])
p("modifiers:", [(m.type, m.name) for m in human.modifiers])
p("vertex groups:", len(human.vertex_groups))
# face UV bounds: find verts near the head top
import mathutils
head_v = [v for v in human.data.vertices if v.co.z > 1.55]
p("verts above z=1.55 (head region):", len(head_v))
if head_v:
    xs = [v.co.x for v in head_v]; ys = [v.co.y for v in head_v]; zs = [v.co.z for v in head_v]
    p("head bbox x:", round(min(xs), 3), round(max(xs), 3),
      "y:", round(min(ys), 3), round(max(ys), 3),
      "z:", round(min(zs), 3), round(max(zs), 3))

# --- mixamo rig ---
rig = HumanService.add_builtin_rig(human, "mixamo")
p("rig object:", rig.name if rig else None)
if rig:
    bones = [b.name for b in rig.data.bones]
    p("rig bone count:", len(bones))
    p("rig bones:", bones)
    # head bone
    for cand in ("Head", "head", "mixamorig:Head"):
        if cand in bones:
            p("head bone candidate:", cand)

# --- Warrior FBX ---
fbx_path = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/Warrior.fbx"
bpy.ops.import_scene.fbx(filepath=fbx_path)
arms = [o for o in bpy.data.objects if o.type == 'ARMATURE']
p("fbx armatures:", [(a.name, len(a.data.bones)) for a in arms])
for a in arms:
    p("fbx bones:", [b.name for b in a.data.bones])
p("fbx actions:", [a.name for a in bpy.data.actions])
for a in bpy.data.actions:
    p("  action:", a.name, "frames:", a.frame_range, "fcurves:", len(a.fcurves))

# --- Warrior_Anime.glb objects ---
glb_path = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/Warrior_Anime.glb"
bpy.ops.import_scene.gltf(filepath=glb_path)
for o in bpy.data.objects:
    if o.type == 'MESH':
        tris = sum(len(p.vertices) - 2 for p in o.data.polygons)
        p("glb mesh:", o.name, "verts:", len(o.data.vertices), "tris~:", tris,
          "mats:", [m.name if m else None for m in o.data.materials],
          "vgroups:", len(o.vertex_groups))
    elif o.type == 'ARMATURE':
        p("glb armature:", o.name, "bones:", len(o.data.bones))
p("DONE")
