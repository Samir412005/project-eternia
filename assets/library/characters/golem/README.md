# Rock Golem boss — VFX dept (2026-11-15)

Procedural rock golem (Blender 4.5.9, displaced icospheres/boxes).
GLB: `Golem.glb` — 1,880 polys / 2,204 tris, ~2.7 m tall, 2 materials
(Rock + Lava), lava cracks = generated emissive texture
(`Golem_LavaCracks.png`, emission strength 3) + emissive lava geometry
(eyes, mouth, chest seams). Glow faked with emissive only, never bloom.
Rebuild: `blender --background --python build_golem.py`.

## Where is the .blend source?

`Golem.blend` lives OUTSIDE this project, at
`~/workspace/blender-sources/project-eternia/golem/Golem.blend`.

**Why (proven 2026-11-15):** a `.blend` file inside the Godot project tree
makes `godot --headless --path . --import` hang forever (0 CPU, no output,
killed by timeout at 90/180/240/300 s — reproduced in a minimal project:
import with the .blend present hangs, import with it removed finishes in
~12 s). The same applies to any `.blend` in the tree — the hero's
`assets/characters/quaternius/Warrior_Anime.blend` breaks the real
project's import the same way. Do NOT move a `.blend` back into this tree.
