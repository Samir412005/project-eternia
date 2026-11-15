# PROJECT ETERNIA

Large-scale 3D RPG — Godot 4.3 (GDScript), Android target, third-person.
**Phase 1 (this delivery):** environment audit + modular foundation +
first playable vertical slice + automated validation + Android debug APK.

## Quick start (desktop test)
```bash
/home/hatch/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64 --path . res://scenes/main/main.tscn
```
Controls: WASD / arrows move, Space jump, Shift run, E interact, F attack,
Esc pause. Mouse drag orbits the camera; the on-screen joystick does the
same on touch.

## What is real in Phase 1
- A real 60 x 60 m 3D valley: ground, platforms, ruins, trees, shrine,
  torches — all with collision; a controllable third-person player
  (walk / run / jump / gravity / ground detection); SpringArm camera
  with collision; a chasing training dummy with HP; a working shrine
  interaction (+50 XP, loot, dialogue, quest progress); XP + level-up;
  inventory; quests (one completable); dialogue; JSON save/load v1;
  pause menu; main menu; mobile HUD with joystick.
- Automated tests: `tests/run_tests.gd` (run headless, see
  `tools/validation/validate.sh`).

## Asset limitations (honest)
- The player, dummy, trees, ruins and shrine are **primitive meshes**
  (capsules, boxes, cones). There are no imported characters,
  animations, textures or music yet. The prototype is labelled as such
  in-game and in `GAME_DESIGN.md`.
- Blender is NOT installed in this environment (see
  `ENVIRONMENT_AUDIT.md`), so no new modelled assets were produced here.
- No final storyline or hero identity is decided — `GAME_DESIGN.md` is
  a **proposal**, not a final design.

## Android build
```bash
export ANDROID_HOME=/home/hatch/workspace/game-apk/tools/android-sdk
export JAVA_HOME=/home/hatch/workspace/game-apk/tools/jdk17
export PATH=$JAVA_HOME/bin:$PATH
godot --headless --path . --export-debug "Android Mobile" builds/android/project-eternia-debug.apk
```
Output: `builds/android/project-eternia-debug.apk` (arm64, Mobile renderer).
