# Department 06 — Build

**Owns:** the APK — export, signing, size, and the build scripts that make
the same APK twice. Nothing else. Build never edits game content to make an
export pass.

## Inputs / Outputs

| | |
|---|---|
| Inputs | The project at a committed state, preset `export_presets.cfg` ("Android Mobile", arm64-only, android-34, `com.gggg.eternia` v0.1), debug keystore. |
| Outputs | Signed APK in `builds/android/` (gitignored) or `~/workspace/your_files/` for delivery; build log in `reports/`. |
| Tools | Godot 4.3 headless export, JDK Temurin 17.0.21, Android SDK build-tools 34.0.0 + apksigner, `tools/studio/verify_gate.sh` Gate 4. |

## Gate (must ALL pass before handoff to Verification)

1. Export exit 0.
2. `apksigner verify`: v1+v2+v3 all `true`, `Number of signers: 1`.
3. APK > 10 MB and < 100 MB (aim < 40 MB). `docs/` excluded
   (`exclude_filter="docs/*"` — the 1.8 GB offline docs must never enter an APK again).
4. The APK is built from a COMMITTED state — never from uncommitted files.
   If the tree is dirty, Build stops and says so.

## Rules

- If Godot reports "apksigner tools failed", put `jdk17/bin` on PATH and
  sign manually with the debug keystore. Never ship an unsigned APK.
- Never change a scene, script, or asset to fix a build failure — report it
  to the owning department and stop.
- One APK per slice, named `<slice>.apk` in `~/workspace/your_files/`.
  Old APKs are never re-sent (user rule, 2026-11-14).

## Subagent brief template (copy, fill the brackets, spawn)

> You are the Build department of PROJECT ETERNIA (Godot 4.3, Mobile
> renderer, branch `aetheria-slice`, project `~/workspace/project-eternia/`).
> Read `AGENTS.md` and `STUDIO.md` first and follow them (Godot 4.3 only,
> CC0/free only). Do NOT edit any scene, script, or asset — if the export
> fails because of game content, report it and stop.
>
> Task: [e.g. build the signed APK for the current slice from the committed
> state and verify it with apksigner].
>
> Use only: Godot 4.3 headless export, JDK 17 (`~/workspace/game-apk/tools/jdk17`),
> Android SDK 34.0.0 (`~/workspace/game-apk/tools/android-sdk`), debug
> keystore (`~/workspace/game-apk/debug.keystore`).
>
> Deliver: the signed APK path + size + apksigner output (`v1+v2+v3: true`,
> `Number of signers: 1`), and the export log. If the tree is dirty, say so
> and stop — do not build from uncommitted files. Verify with
> `./tools/studio/verify_gate.sh` Gate 4 only if the full gate is not run.
