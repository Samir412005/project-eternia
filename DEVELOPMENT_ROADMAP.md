# DEVELOPMENT ROADMAP — PROJECT ETERNIA

## Phase 1 — Foundation + vertical slice (THIS DELIVERY, 2026-11-15)
- [x] Environment audit (ENVIRONMENT_AUDIT.md)
- [x] Modular project structure + docs
- [x] Core / Player / World / RPG / Combat / Quest / Save / UI foundations
- [x] Playable 60 m valley: move, run, jump, camera, shrine, dummy, HUD, pause
- [x] Automated validation (`tests/run_tests.gd`)
- [x] Android debug APK (arm64)
- Exit criterion: project opens headless, tests pass, APK installs.
  **Next gate: user tests the APK on the Galaxy A16 and reports
  install / start / movement / FPS.**

## Phase 2 — Content + feel
- Imported character + animations (needs Blender or CC0 assets + approval)
- Full day/night cycle, weather (rain), music/SFX, cinematics intro
- 2 more quests, first NPC with dialogue tree, save migration v1 -> v2
- Real-device FPS pass on Galaxy A16, quality preset tuning
- Exit criterion: 30 FPS sustained on A16 in the valley.

## Phase 3 — World growth
- World streaming, Ashen Woods region, 3 more shrines
- Relationships, crafting, more enemies + boss dummy
- Exit criterion: 3 regions load without hitches on A16.

## Phase 4 — Production hardening
- Full quest chain, balance pass, accessibility, localisation (AR/EN)
- Release signing, store listing prep, crash reporting
- Exit criterion: release candidate APK.

## Phase 5 — Live
- Updates driven by player feedback. No scope promises beyond Phase 4.
