# animations/ — shared animation clips (EMPTY)

Home for animation clips shared across characters: Mixamo FBX clips,
Universal Animation Library (UAL) clips, and vid2anim captures.

**Rules:**
- One folder per source: `mixamo/`, `ual/`, `vid2anim/`.
- Every clip gets a row in `AssetLicenses.md` (Mixamo clips are free under
  Adobe's Mixamo terms — free for use, not CC0; record that exactly).
- Clips are retargeted to the project's rigs in Blender before Godot import;
  never import a raw Mixamo FBX into the game scene.
- Naming: `<character>_<action>.fbx` (e.g. `warrior_sword_attack.fbx`).
- Budget: walk/run/idle loops only for NPCs; signature moves (slash, roll)
  for the hero only.
