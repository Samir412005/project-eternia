"""PROJECT ETERNIA — Character dept, pass 3 fix-up: relink hero textures.

ROOT CAUSE found after the first pass-3 export: when Warrior_Anime.blend
was moved OUT of the project tree (commit 702691f), its four image
filepaths ("//Warrior_Face_Anime.png" etc., relative to the .blend) broke —
the PNGs live in the project, not next to the external .blend. Blender
opened the images as 0x0 / has_data=False, so the pass-3 GLB export
embedded a 1x1 placeholder instead of the real face/hair/body/sword
textures (new GLB 768 KB vs old 1,775,692 bytes).

Fix: relink all four images to ABSOLUTE disk paths (absolute so the
external .blend location can never break them again), reload, verify
pixels are back, save the .blend, re-export the GLB with the pass-2
export settings.

Run: ~/workspace/tools/blender-4.5/blender --background --python tools/studio/relink_hero_textures.py
"""
import bpy

BLEND = "/home/hatch/workspace/blender-sources/project-eternia/hero/Warrior_Anime.blend"
GLB = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/Warrior_Anime.glb"
ASSETS = "/home/hatch/workspace/project-eternia/assets/characters/quaternius/"

RELINK = {
    "Hair_Strands": ASSETS + "Hair_Strands.png",
    "Warrior_Face_Anime": ASSETS + "Warrior_Face_Anime.png",
    "Warrior_Sword_Texture": ASSETS + "Warrior_Sword_Texture.png",
    "Warrior_Texture": ASSETS + "Warrior_Texture.png",
}

bpy.ops.wm.open_mainfile(filepath=BLEND)

ok = True
for name, path in RELINK.items():
    img = bpy.data.images.get(name)
    if img is None:
        print("RELINK: MISSING image datablock", name)
        ok = False
        continue
    img.filepath = path
    img.reload()
    print("RELINK: %s -> %s size=%s has_data=%s" % (name, path, tuple(img.size), img.has_data))
    if not img.has_data or img.size[0] == 0:
        ok = False

if not ok:
    raise SystemExit("RELINK: FAILED — a texture did not reload; aborting before export")

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("RELINK: saved", BLEND)

bpy.ops.export_scene.gltf(
    filepath=GLB,
    export_format="GLB",
    export_animations=True,
    export_skins=True,
    export_apply=False,
    export_yup=True,
    export_materials="EXPORT",
)
print("RELINK: exported", GLB)
