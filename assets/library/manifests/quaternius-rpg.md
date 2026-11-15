# Quaternius RPG Characters (Nov 2020) — pack manifest (IN PLACE)

- **Current location:** `assets/characters/quaternius/` (NOT yet in the library — see below)
- **Source:** https://quaternius.com/ — pack "RPG Characters", Nov 2020.
  On-disk copy: `~/workspace/video-lab/assets/characters/rpg_characters/RPG Characters - Nov 2020/`
  (Blends, FBX, OBJ, Textures, Preview.jpg, License.txt).
- **Licence:** **CC0 1.0** — verified from the pack's own shipped `License.txt`
  ("CC0 1.0 Universal, Public Domain Dedication"). This Nov 2020 pack predates
  Quaternius's licence change; newer Quaternius packs are QAL v1.0 — check the
  licence file of EACH pack, never assume.
- **Files in this project:** `Warrior.fbx` (44-bone rig, 14 embedded clips incl.
  Idle/Walk/Run/Sword_Attack; raw height 2.95 m, scaled to ~1.8 m in-game),
  `Warrior_Texture.png`, `Warrior_Sword_Texture.png`. The pack also holds
  Cleric, Monk, Ranger, Rogue, Wizard FBX + 7 weapon FBX (not imported yet).
- **Used by:** the Aetheria hero (Warrior).
- **Why in place:** the hero agent is actively re-styling the Warrior in this
  folder right now (uncommitted `Warrior_Anime.glb`, face/hair textures,
  `aetheria_slice.gd` edits). Move only after that work is committed.
  Target: `assets/library/characters/quaternius-rpg/`.
- **Derived work in this folder (project-original, hero agent, in flux):**
  `Warrior_Anime.glb`, `Warrior_Face_Anime.png`, `Hair_Strands.png`,
  `Warrior_Anime_Hair_Strands.png` and the `Warrior_Anime_*` textures —
  derived from the CC0 Warrior.fbx, painted/modelled in this studio.
