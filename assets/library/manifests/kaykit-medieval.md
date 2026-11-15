# KayKit Medieval Hexagon Pack 1.0 — pack manifest (IN PLACE)

- **Current location:** `assets/environments/kaykit-medieval/` (NOT yet in the library — see below)
- **Source:** https://github.com/KayKit-Game-Assets/KayKit-Medieval-Hexagon-Pack-1.0
- **Licence:** CC0 1.0 (public domain).
- **Files in this project:** green set only — buildings (home A/B, tavern, market,
  church, blacksmith, castle, towers, windmill, watermill, well, lumbermill,
  barracks, mine, archery range) + decoration props (crates, sacks, flags, tent,
  buckets, weaponrack, wheelbarrow, ...) + `hexagons_medieval.png` atlas.
- **Full pack:** `~/workspace/tools/downloads/kaykit-medieval.zip`
- **Used by:** the Aetheria village scene (`scripts/world/aetheria_slice.gd`).
- **Why in place:** `aetheria_slice.gd` loads these paths by string and is
  being edited by the hero agent (uncommitted, 2026-11-15). Move only after
  that work is committed — see the migration plan in `assets/library/README.md`.
  Target: `assets/library/environments/kaykit-medieval/`.
