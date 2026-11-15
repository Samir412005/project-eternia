# Asset Library — PROJECT ETERNIA

**The canonical asset library.** Every third-party asset in this project lives here
or is indexed here. Rule: **new assets go directly into `assets/library/`** — never
into a loose top-level folder. Licences for every pack are recorded in
`AssetLicenses.md` at the project root (one row per pack, with source URL).

## Layout

```
assets/library/
├── characters/        # rigged characters (see manifests/ — packs still in place)
├── environments/      # kits, nature, HDRI
│   └── poly-haven-hdri/          # Poly Haven HDRI 1K (CC0) — MOVED here
├── audio/             # music + SFX packs
│   └── kenney-rpg-audio/         # Kenney RPG Audio (CC0) — MOVED here
├── fonts/             # font packs
│   └── noto-sans-arabic/         # Noto Sans Arabic v2.009 (OFL 1.1) — MOVED here
├── animations/        # shared animation clips (Mixamo, UAL, vid2anim) — EMPTY, see README
├── textures/          # painted / procedural textures (Krita, Material Maker) — EMPTY, see README
├── ui/                # UI art, icons, HUD elements — EMPTY, see README
└── manifests/         # one README per pack that still lives outside the library
```

## Pack index (current locations)

| Pack | Licence | Location | Status |
|---|---|---|---|
| Kenney RPG Audio (3 sounds) | CC0 1.0 | `assets/library/audio/kenney-rpg-audio/` | **Moved** 2026-11-15 |
| Noto Sans Arabic (Regular + Bold) | OFL 1.1 | `assets/library/fonts/noto-sans-arabic/` | **Moved** 2026-11-15 |
| Poly Haven kloppenheim_06_puresky 1K HDRI | CC0 1.0 | `assets/library/environments/poly-haven-hdri/` | **Moved** 2026-11-15 |
| KayKit Medieval Hexagon Pack 1.0 (green set) | CC0 1.0 | `assets/environments/kaykit-medieval/` | **In place — BLOCKED** (see below) |
| Kenney Nature Kit (3 samples) | CC0 1.0 | `assets/environments/kenney-nature/` | **In place — BLOCKED** |
| KayKit Character Pack Adventures (weapons/items only) | CC0 1.0 | `assets/characters/kaykit/` | **In place — BLOCKED** |
| Quaternius RPG Characters Nov 2020 (Warrior etc.) | CC0 1.0 | `assets/characters/quaternius/` | **In place — BLOCKED** |
| Quaternius Ultimate Animated Character (Casual/Soldier) | CC0 1.0 | NOT imported — on disk at `~/workspace/game-apk/last-signal/project/assets/character/` | **Available** |
| Project shaders (toon, outline, SDF face, cape) | Project original | `assets/materials/` | **In place — owned by Character dept** |

## Why some packs are still in place (conflict note, 2026-11-15)

`scripts/world/aetheria_slice.gd` — currently being edited by the hero agent
(uncommitted) — loads the KayKit, Kenney-nature, KayKit-Medieval and Quaternius
paths by string (`res://assets/...`). Moving those files now would break the
hero agent's in-flight work and the slice scene. **Do not move them until the
hero agent's work is committed.** The migration plan below runs only then.

## Migration plan (run only after the hero agent commits)

```bash
cd ~/workspace/project-eternia
git mv assets/environments/kaykit-medieval assets/library/environments/kaykit-medieval
git mv assets/environments/kenney-nature  assets/library/environments/kenney-nature
git mv assets/characters/kaykit           assets/library/characters/kaykit-weapons
git mv assets/characters/quaternius       assets/library/characters/quaternius-rpg
# then update every res://assets/... path in scripts/world/aetheria_slice.gd
# to the new res://assets/library/... paths, and fix source_file= lines in
# the moved .import files the same way (see the 2026-11-15 moves for the pattern)
godot --headless --path . --import   # must exit 0 with 0 SCRIPT ERRORs
./tools/studio/verify_gate.sh        # all four gates must PASS
```

## Rules

1. **Licence first.** No asset enters the library without a row in
   `AssetLicenses.md` (source URL + licence). CC0 / OFL only for shipping.
   **Quaternius:** the Nov 2020 RPG pack and the Ultimate Animated Character
   pack are CC0 1.0 per their shipped License.txt files. Newer Quaternius
   packs are QAL v1.0 — check the licence file of EACH pack at download time
   and record it; never assume CC0.
2. **VRoid-derived content is FORBIDDEN** in this project unless the live
   VRoid terms have been read and the permission recorded in
   `AssetLicenses.md`. Same for MMD game models (technique only, never the
   models) and any AI-generated 3D used as the hero (props only).
3. **Full packs stay outside the project.** Only the files the game actually
   uses are copied in. The full zips live in `~/workspace/tools/downloads/`.
4. **LFS.** `*.glb *.fbx *.png *.hdr *.ttf *.ogg *.wav *.mp3 *.exr` are
   Git-LFS-tracked (see `.gitattributes`). After a VM restart, `git-lfs`
   must be reinstalled via apt before committing binaries.
5. **Budgets (Galaxy A16).** One hero ≤ 15k tris; one building ≤ 5k tris;
   textures ≤ 1024 px (2048 hero only); total visible tris < 100k;
   draw calls < 200; live particles < 2,000.
