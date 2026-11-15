# Studio — PROJECT ETERNIA

The professional studio pipeline around this project. Start at `STUDIO.md`
(project root) for the full pipeline, then use the pieces below.

| Piece | Path | What it is |
|---|---|---|
| Pipeline | `../STUDIO.md` | The one path: Blender → Krita → Godot → APK → Verify, with budgets and rules. |
| Asset library | `../assets/library/` | Canonical library: index, pack manifests, moved packs. |
| Licences | `../AssetLicenses.md` | One row per asset pack (source URL + licence). |
| Verification gate | `../tools/studio/verify_gate.sh` | Four gates: import, gdUnit, screenshots, APK. Run it; it reports, it never repairs. |
| Departments | `departments/` | Seven one-page briefs, each with an exact subagent brief template. |

## Departments

1. `departments/01-character.md` — hero, NPCs, face, hair, cape, shaders.
2. `departments/02-environment.md` — village, forest, dungeon, sky, lighting.
3. `departments/03-animation.md` — locomotion, combat, mocap, retargeting.
4. `departments/04-vfx.md` — slashes, fire, golem, particles.
5. `departments/05-sound.md` — music, SFX, mix.
6. `departments/06-build.md` — APK export + signing. Never edits game content.
7. `departments/07-verification.md` — INDEPENDENT audit. Never builds or fixes.
   Nothing reaches the user before its sign-off.

## The one rule

**Nothing is "ready" until the verification gate passes — and the final
verdict is always the user's Galaxy A16.**
