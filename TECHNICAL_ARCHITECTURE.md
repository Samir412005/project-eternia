# TECHNICAL ARCHITECTURE — PROJECT ETERNIA

Engine: Godot 4.3 stable, Mobile renderer (`gl_compatibility`),
GDScript only, Android arm64, landscape 1280x720, stretch
`canvas_items` / `expand`. Physics 60 ticks/s.

## Module status (Phase 1)
| Module | File | Status |
|---|---|---|
| EventBus | scripts/core/event_bus.gd | Implemented — all cross-system signals |
| GameManager | scripts/core/game_manager.gd | Implemented — MENU/PLAYING/PAUSED/DIALOGUE states |
| SceneManager | scripts/core/scene_manager.gd | Implemented (basic) — no loading screen yet |
| SettingsManager | scripts/core/settings_manager.gd | Implemented — quality presets + persistence |
| ResourceManager | scripts/core/resource_manager.gd | Implemented — load cache |
| PlayerController | scripts/player/player_controller.gd | Implemented — walk/run/jump/gravity |
| CameraController | scripts/player/camera_controller.gd | Implemented — SpringArm, drag orbit |
| PlayerStateMachine | scripts/player/player_state_machine.gd | Implemented — derived from real velocity/floor |
| PlayerInteraction | scripts/player/player_interaction.gd | Implemented — Area3D range detection |
| PlayerAnimationController | scripts/player/player_animation_controller.gd | Implemented — procedural prototype animation |
| WorldManager | scripts/world/world_manager.gd | Implemented — builds the valley at runtime |
| WorldRegions | scripts/world/world_regions.gd | Data only — 1 built region, 3 planned |
| EnvironmentSystem | scripts/world/environment_system.gd | Implemented — fog |
| TimeOfDay | scripts/world/time_of_day.gd | Implemented — slow sun drift |
| WeatherSystem | scripts/world/weather_system.gd | UNFINISHED — API only, always CLEAR |
| WorldStreaming | scripts/world/world_streaming.gd | UNFINISHED — interface only |
| CharacterStats | scripts/rpg/character_stats.gd | Implemented — data + derived values |
| ExperienceSystem | scripts/rpg/experience_system.gd | Implemented — curve 100 * level^1.5 |
| LevelProgression | scripts/rpg/level_progression.gd | Implemented — 2 attribute points/level |
| SkillSystem | scripts/rpg/skill_system.gd | Implemented — data + cooldowns |
| EquipmentSystem | scripts/rpg/equipment_system.gd | Implemented — slots |
| InventorySystem | scripts/rpg/inventory_system.gd | Implemented — 24 slots, stacks to 99 |
| CombatSystem | scripts/combat/combat_system.gd | Implemented — melee, range 2.6 m |
| EnemyAI | scripts/combat/enemy_ai.gd | Implemented — chase/attack/respawn dummy |
| InteractionSystem | scripts/combat/interaction_system.gd | Implemented — group registry |
| LootSystem | scripts/combat/loot_system.gd | Implemented — deterministic tables |
| QuestManager | scripts/quests/quest_manager.gd | Implemented |
| QuestDatabase | scripts/quests/quest_database.gd | Implemented — JSON |
| DialogueSystem | scripts/quests/dialogue_system.gd | Implemented — JSON lines |
| CharacterRelationships | scripts/quests/character_relationships.gd | UNFINISHED — affinity data only |
| CinematicManager | scripts/quests/cinematic_manager.gd | UNFINISHED — no cinematics |
| SaveManager / SaveData | scripts/save/*.gd | Implemented — JSON, version 1 |
| MainMenu / PauseMenu / InventoryUI / QuestUI / DialogueUI / MobileHUD / SettingsUI | scripts/ui/*.gd | Implemented |

## Rendering / performance strategy (Android)
- Mobile renderer only; Compatibility renderer is the fallback if a
  device cannot run Mobile (project setting, not a second build).
- Shadows: the single biggest cost. Quality presets scale shadows only
  (Low = off, Medium = on, High = on + lower bias). No glow, no MSAA 3D,
  no real-time GI, no VoxelGI.
- Textures: ETC2/ASTC import on. No texture in Phase 1 exceeds
  procedural materials (zero texture memory in the slice).
- Draw calls: valley is ~30 primitive meshes + lights; target < 80.
- Lights: 1 directional (shadows) + 3 omni (shrine + 2 torches), all
  short range. No new lights without a budget check.
- Memory: no streaming needed at 60 m; streaming is a Phase 3 concern.
- Physics: one player body + one enemy + static world; 60 Hz is fine.

## Data-driven rules
Quests, dialogue, items and abilities live in `data/*.json` and are
loaded at runtime — no quest text or loot table is hard-coded in a
system script (the shrine's reward IDs are the one deliberate exception:
they name data entries, they are not the data).

## Save format
`user://savegame.json`, JSON, `version: 1`. `SaveData.from_dict`
rejects any other version instead of silently migrating (migration is
a Phase 2 task, recorded in the roadmap).
