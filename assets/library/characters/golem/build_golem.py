# PROJECT ETERNIA — Rock Golem boss (VFX dept, 2026-11-15)
# Blender 4.5.9, run headless:
#   blender --background --python build_golem.py
# Procedural only: displaced icospheres/boxes, no imported meshes.
# Lava cracks = generated emissive texture (random-walk glowing cracks
# on dark rock) + a few thin emissive crack strips + emissive eyes.
# Output: Golem.glb + Golem.blend + Golem_LavaCracks.png
# Budget: <= 10k tris. Two materials (Rock, Lava) -> 2 draw calls.
import bpy, math, random, os
from mathutils import Vector

random.seed(20261115)
OUT = "/home/hatch/workspace/project-eternia/assets/library/characters/golem"
# .blend lives OUTSIDE the Godot tree: a .blend inside the project makes
# `godot --headless --import` hang forever (proven 2026-11-15).
BLEND_OUT = "/home/hatch/workspace/blender-sources/project-eternia/golem"

# --- clean scene -------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

# --- lava-crack texture (512x512, generated pixel data) ---------------
W = H = 512
px = [0.0] * (W * H * 4)
def set_px(x, y, r, g, b, a=1.0):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 4
        px[i], px[i+1], px[i+2], px[i+3] = r, g, b, a

# dark basalt base with per-pixel noise
for y in range(H):
    for x in range(W):
        n = random.uniform(0.10, 0.20)
        # subtle large-scale mottling
        m = 0.03 * math.sin(x * 0.05) * math.cos(y * 0.04)
        set_px(x, y, n + m, n + m, n + m + 0.01)

def crack(x, y, angle, length, width):
    """Random-walk glowing crack: bright yellow core, orange halo."""
    for _ in range(length):
        angle += random.uniform(-0.45, 0.45)
        x += int(math.cos(angle) * 2)
        y += int(math.sin(angle) * 2)
        for dy in range(-width, width + 1):
            for dx in range(-width, width + 1):
                d = math.hypot(dx, dy)
                if d <= width:
                    core = max(0.0, 1.0 - d / (width + 0.5))
                    # core: hot yellow-white; edge: deep orange
                    r = 1.0
                    g = 0.25 + 0.65 * core
                    b = 0.05 + 0.25 * core
                    set_px(x + dx, y + dy, r, g, b)

# main crack network (a few long branching cracks)
for _ in range(10):
    crack(random.randint(60, W - 60), random.randint(60, H - 60),
          random.uniform(0, 6.28), random.randint(80, 160), 3)
for _ in range(20):  # short branches
    crack(random.randint(40, W - 40), random.randint(40, H - 40),
          random.uniform(0, 6.28), random.randint(20, 50), 1)

img = bpy.data.images.new("Golem_LavaCracks", width=W, height=H, alpha=True)
img.pixels = px
img.filepath_raw = os.path.join(OUT, "Golem_LavaCracks.png")
img.file_format = 'PNG'
img.save()

# --- materials ---------------------------------------------------------
def rock_material(with_cracks):
    mat = bpy.data.materials.new("Golem_Rock_Cracks" if with_cracks else "Golem_Rock")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.16, 0.15, 0.15, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.95
    bsdf.inputs["Metallic"].default_value = 0.0
    if with_cracks:
        tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex.image = img
        mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = 3.0
        # also tint albedo slightly with the texture (dark rock stays dark)
        mix = mat.node_tree.nodes.new("ShaderNodeMixRGB")
        mix.blend_type = 'MULTIPLY'
        mix.inputs[0].default_value = 1.0
        mix.inputs[1].default_value = (0.16, 0.15, 0.15, 1.0)
        mat.node_tree.links.new(tex.outputs["Color"], mix.inputs[2])
        mat.node_tree.links.new(mix.outputs["Color"], bsdf.inputs["Base Color"])
    return mat

rock_plain = rock_material(False)
rock_crack = rock_material(True)

lava = bpy.data.materials.new("Golem_Lava")
lava.use_nodes = True
bsdf = lava.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (1.0, 0.25, 0.02, 1.0)
bsdf.inputs["Emission Color"].default_value = (1.0, 0.30, 0.02, 1.0)
bsdf.inputs["Emission Strength"].default_value = 4.0
bsdf.inputs["Roughness"].default_value = 0.6

# --- rock part helper --------------------------------------------------
def rock(name, kind, loc, scale, subdiv=2, seed=0, disp=0.12, mat=None):
    if kind == 'ico':
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdiv, radius=1.0, location=loc)
    elif kind == 'box':
        bpy.ops.mesh.primitive_cube_add(location=loc)
    elif kind == 'cyl':
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=1.0, depth=1.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    # displace with a clouds texture for a jagged rock silhouette
    tex = bpy.data.textures.new(name + "_disp", type='CLOUDS')
    tex.noise_scale = 0.55
    tex.noise_depth = 2
    mod = o.modifiers.new("Displace", 'DISPLACE')
    mod.texture = tex
    mod.strength = disp
    mod.texture_coords = 'LOCAL'
    random.seed(seed)
    tex.noise_scale = random.uniform(0.45, 0.7)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier=mod.name)
    for p in o.data.polygons:
        p.use_smooth = True
    if mat:
        o.data.materials.append(mat)
    return o

rock_parts, lava_parts = [], []

# torso (cracked) — bulky, ~2.2 m tall overall golem
rock_parts.append(rock("Torso", 'ico', (0, 0, 1.55), (0.85, 0.62, 0.75), 3, 11, 0.14, rock_crack))
# pelvis
rock_parts.append(rock("Pelvis", 'ico', (0, 0, 0.95), (0.62, 0.48, 0.42), 2, 12, 0.12, rock_plain))
# head (cracked, smaller) + jaw
rock_parts.append(rock("Head", 'ico', (0, 0, 2.35), (0.42, 0.38, 0.36), 3, 13, 0.10, rock_crack))
rock_parts.append(rock("Jaw", 'box', (0, 0.28, 2.18), (0.30, 0.14, 0.12), 1, 14, 0.05, rock_plain))
# shoulders
rock_parts.append(rock("Shoulder_L", 'ico', (-0.95, 0, 2.05), (0.37, 0.35, 0.34), 3, 15, 0.12, rock_plain))
rock_parts.append(rock("Shoulder_R", 'ico', (0.95, 0, 2.05), (0.37, 0.35, 0.34), 3, 16, 0.12, rock_plain))
# arms: upper + forearm + big fists
for s, x in (("L", -1.02), ("R", 1.02)):
    rock_parts.append(rock(f"ArmUpper_{s}", 'cyl', (x, 0, 1.65), (0.30, 0.30, 0.45), 1, 17, 0.08, rock_plain))
    rock_parts.append(rock(f"ArmFore_{s}", 'cyl', (x, 0, 1.05), (0.33, 0.33, 0.42), 1, 18, 0.08, rock_plain))
    rock_parts.append(rock(f"Fist_{s}", 'ico', (x, 0, 0.55), (0.34, 0.32, 0.34), 2, 19, 0.10, rock_plain))
# legs + feet
for s, x in (("L", -0.38), ("R", 0.38)):
    rock_parts.append(rock(f"Leg_{s}", 'cyl', (x, 0, 0.55), (0.30, 0.30, 0.42), 1, 20, 0.08, rock_plain))
    rock_parts.append(rock(f"Foot_{s}", 'box', (x, 0.12, 0.12), (0.34, 0.48, 0.14), 1, 21, 0.05, rock_plain))
# back spikes (rocky silhouette)
for i, z in enumerate((1.95, 1.65, 1.35)):
    rock_parts.append(rock(f"Spike_{i}", 'ico', (0, -0.55, z), (0.16, 0.16, 0.28), 1, 22 + i, 0.06, rock_plain))

# --- lava details (emissive geometry, no bloom needed) -----------------
def lava_part(name, kind, loc, scale):
    if kind == 'sphere':
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=1.0, location=loc)
    else:
        bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(lava)
    lava_parts.append(o)
    return o

# glowing eyes (slightly proud of the head surface) + brow slit
lava_part("Eye_L", 'sphere', (-0.16, 0.47, 2.42), (0.07, 0.05, 0.05))
lava_part("Eye_R", 'sphere', (0.16, 0.47, 2.42), (0.07, 0.05, 0.05))
lava_part("Mouth", 'box', (0, 0.45, 2.22), (0.14, 0.025, 0.03))
# chest crack strip (guaranteed visible glow even where UV cracks are faint)
lava_part("ChestCrack", 'box', (0, 0.60, 1.60), (0.04, 0.03, 0.35))
lava_part("ChestCrack2", 'box', (0.25, 0.52, 1.35), (0.035, 0.03, 0.24))

# --- join into two meshes (1 draw call per material) -------------------
def join_all(parts, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    j = bpy.context.active_object
    j.name = name
    return j

body = join_all(rock_parts, "Golem_Body")
glow = join_all(lava_parts, "Golem_Lava")
# keep both selected for export; set origin to feet centre
bpy.ops.object.select_all(action='SELECT')
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

tris = sum(len(o.data.polygons) for o in (body, glow))
print(f"GOLEM_TRIS={tris} body={len(body.data.polygons)} lava={len(glow.data.polygons)}")
print(f"GOLEM_HEIGHT~2.7m parts_rock={len(rock_parts)} parts_lava={len(lava_parts)}")
assert tris <= 10000, f"over budget: {tris}"

# --- save + export -----------------------------------------------------
os.makedirs(BLEND_OUT, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BLEND_OUT, "Golem.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "Golem.glb"),
                          export_format='GLB', export_apply=True,
                          export_yup=True)
print("GOLEM_DONE " + OUT)
