# CHANGELOG — PROJECT ETERNIA

## aetheria-slice — 2026-11-15 (branch `aetheria-slice`)
- First real Aetheria mini-RPG slice: village street scene (`scenes/main/aetheria_slice.tscn`,
  built at runtime by `scripts/world/aetheria_slice.gd`) — KayKit medieval houses/props
  + Kenney trees/flowers, procedural toon hero (red cape, geometric anime face,
  real KayKit sword + shield, inverted-hull outline), one NPC villager, distant
  castle + two floating islands, saturated ProceduralSky + fog + one sun.
- Reuses ETERNIA player controller, SpringArm camera and MobileHUD (walk/run/jump).
- Real screenshots from the actual Godot run (Compatibility renderer, Xvfb, 1280x720)
  in `screenshots-aetheria/` — see its README.md for an honest read of each shot.
- Verification: headless import 0 script errors, gdUnit 5/5 PASS, Android APK
  `builds/android/aetheria-slice-signed.apk` (31,045,515 bytes, apksigner v3 verified).
- Not in this slice: golem/combat, dialogue/quest, house collision, walk animation
  on the new hero model. Main scene on this branch is the slice (main stays intact).

## aetheria-slice — Warrior hero, 2026-11-15 (branch `aetheria-slice`)
- Procedural pill hero replaced with the real rigged **Quaternius Warrior**
  (CC0, RPG Characters pack, `assets/characters/quaternius/Warrior.fbx` +
  `Warrior_Texture.png` / `Warrior_Sword_Texture.png`), scaled 0.60 to ~1.79 m.
  Its own sword stays rigged to the Weapon.R bone (blade visible in front
  shots); red cape (widened so its edges show from the front) + KayKit round
  shield on the left arm; toon shading + inverted-hull outline.
- Idle_Weapon / Walk / Run clips wired to the controller speed; cape sway in
  `_process`; screenshot poses set deterministically (play → seek → pause).
- New real screenshots `screenshots-aetheria/04-warrior-street.png`,
  `05-warrior-closeup.png`, `06-warrior-walk.png` (1280x720, Xvfb) — see the
  README there for the honest read. Two screenshot bugs fixed, not hidden:
  outline width 0.035 ballooned to a ~3.5 m black blob on the skinned mesh
  (armature 100x scale; fixed with a 0.00035 outline material) and the FBX
  importer left the texture atlas unlinked (flat white mannequin; fixed by
  assigning the atlas explicitly).
- Verification: headless import 0 script errors, gdUnit 5/5 PASS, Android APK
  `~/workspace/your_files/aetheria-slice.apk` (34,110,865 bytes, apksigner
  v1+v2+v3 verified, com.gggg.eternia v0.1).
- Still not in this slice: golem/combat, dialogue/quest, house collision;
  the face is minimal by design (no anime eyes); the cape is a rigid box.

## 0.1.0 — 2026-11-15 (Phase 1)
- Environment audit completed (Godot 4.3, SDK 34, JDK 17; Blender + NDK missing).
- Godot project created: Mobile renderer, Android landscape, arm64.
- Modular foundation: Core, Player, World, RPG, Combat, Quests, Save, UI (see TECHNICAL_ARCHITECTURE.md for per-module status; Weather, Streaming, Relationships, Cinematics are documented as unfinished).
- Playable vertical slice: 60 m valley, third-person player (walk/run/jump), SpringArm camera, shrine interaction, training dummy, HUD + joystick, pause + main menu, save/load v1.
- Automated validation: `tests/run_tests.gd` + `tools/validation/validate.sh`.
- Android debug APK built from export preset "Android Mobile".
