# ENVIRONMENT AUDIT — PROJECT ETERNIA

**Date:** 2026-11-15 (fresh check, this session)
**Machine:** Linux htch-runtime, Ubuntu 24.04.5 LTS, x86_64, kernel 7.0.0-44
**CPU:** 4 vCPU — AMD EPYC 9D25 (runtime shares 1.5 CPU to this cell)
**RAM:** 7.7 GiB total; ~0.7–1.2 GiB available at audit time (7.1 GiB used,
  1.0 GiB swap, 445 MiB swap used) — **tight; headless Godot + export
  must run with nothing else heavy beside it**
**Disk:** 150 GiB volume, 130 GiB free (`/home/hatch`)
**GPU:** none (software rendering only on this VM)

## Verified installations
| Tool | Version | Path |
|---|---|---|
| Godot | 4.3.stable.official.77dcf97d8 | `/home/hatch/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64` (NOT in PATH) |
| Godot export templates | 4.3.stable (incl. android_debug.apk, android_release.apk, android_source.zip) | `~/.local/share/godot/export_templates/4.3.stable/` |
| JDK | Temurin 17.0.21+9 | `/home/hatch/workspace/game-apk/tools/jdk17` (NOT in PATH, no system java) |
| Android SDK | build-tools 34.0.0, platform android-34, platform-tools, cmdline-tools, licenses | `/home/hatch/workspace/game-apk/tools/android-sdk` (ANDROID_HOME unset in shell) |
| Godot editor settings | android_sdk_path + java_sdk_path + debug keystore already configured | `~/.config/godot/editor_settings-4.3.tres` |
| Debug keystore | present | `/home/hatch/workspace/game-apk/debug.keystore` + `~/.local/share/godot/keystores/debug.keystore` |
| Git | 2.43.0 | system |
| Python | 3.12.3 | system |

## Missing dependencies
| Tool | Status | Impact |
|---|---|---|
| Blender | NOT installed (`blender: command not found`, not in apt list) | No modelled/imported assets can be produced here; Phase 1 uses primitives. Install needs user approval (apt). |
| Android NDK | No `ndk` directory in the SDK | Not needed for template export (`use_gradle_build=false`, proven by THE LAST SIGNAL). Needed only for custom native/GDExtension builds. |
| Gradle | Not installed standalone | Not needed for template export. Needed only for Gradle builds. |
| System Java / ANDROID_HOME | Not in PATH / env | Builds must set `JAVA_HOME` + `ANDROID_HOME` per command (done in the build steps). |
| GPU / VRAM | None | No GPU-accelerated preview; Mobile renderer + headless testing only. |

## Android export readiness
**READY (template path):** Godot 4.3 + templates 4.3 + SDK 34 + JDK 17 +
debug keystore are all present and this exact combination already
produced working APKs (Breakout, THE LAST SIGNAL v0.1/v0.2) from this
machine. Export preset uses `use_gradle_build=false`, arm64-v8a only,
package `com.gggg.eternia`.

## Known limitations
- RAM is the binding constraint: 7.7 GiB total with most of it in use
  at audit time. Export runs must not overlap with browser or video work.
- No GPU: editor 3D preview and in-editor playtesting are CPU-bound;
  real-device testing (Galaxy A16) is the only true performance test.
- No real FPS data exists for this project on the Galaxy A16 yet.
- AI agent integrations: this session runs on Muse Spark (Meta Muse);
  there is no separate installed "Muse Wonder" / "Muse Code" CLI in
  this environment — agent collaboration happens inside this Muse
  session, with Git checkpoints before major changes. No API keys or
  secrets are used or stored by this project.
