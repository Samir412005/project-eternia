# KayKit Character Pack Adventures — pack manifest (IN PLACE)

- **Current location:** `assets/characters/kaykit/` (NOT yet in the library — see below)
- **Source:** https://github.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0
- **Licence:** CC0 1.0 (public domain).
- **Files in this project:** weapons and items only — `sword_1handed`, `sword_2handed`,
  `shield_round` (+ variants), axes, staff, wands, daggers, crossbows, mugs,
  quivers, spellbooks, smokebomb, arrows + knight/rogue/mage/barbarian textures.
- **IMPORTANT:** this repo holds weapons/items ONLY — the character meshes
  themselves are NOT in it. That is why the first Aetheria hero was a
  procedural pill: there was no character mesh in this pack.
- **Full pack:** `~/workspace/tools/downloads/kaykit-chars.zip`
- **Used by:** the hero's sword and shield (`scripts/world/aetheria_slice.gd`).
- **Why in place:** same conflict — `aetheria_slice.gd` is being edited by
  the hero agent. Move only after that work is committed.
  Target: `assets/library/characters/kaykit-weapons/`.
