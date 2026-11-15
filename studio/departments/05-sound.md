# Department 05 — Sound

**Owns:** all audio — music, SFX, UI sounds, and the mix that keeps them
audible on a phone speaker without clipping.

## Inputs / Outputs

| | |
|---|---|
| Inputs | Kenney RPG Audio (CC0), LMMS compositions, Audacity recordings/edits, Poly Haven / ambientCG-free SFX (CC0 only). |
| Outputs | `.ogg` files in `assets/library/audio/<pack>/`, AudioStreamPlayers wired in scenes, mix levels in `data/audio/`. |
| Tools | LMMS 1.2.2 (compose; apt install — does NOT survive a VM restart, reinstall after restart), Audacity 3.4.2 (edit; same apt caveat), Kenney CC0 packs. |

## Gate (must ALL pass before handoff to Build)

1. All audio is `.ogg`, 44.1 kHz, stereo — never 96 kHz, never uncompressed WAV in the shipped APK.
2. No copyrighted music, no generated recitation, no invented verses — ever.
   New music/nasheed needs the user's explicit approval first.
3. Every SFX is audible in a real play session (not just in the editor) and
   has a volume that doesn't clip on a phone speaker.
4. Headless import: 0 SCRIPT ERRORs. Licence rows in `AssetLicenses.md`.

## Rules

- Sound is the last department to touch a slice, never the first — a silent
  game that plays is better than a musical game that crashes.
- Keep the APK audio budget small: SFX < 5 MB total, music streamed, not
  embedded per scene.
- If LMMS/Audacity are gone after a VM restart (apt), reinstall before
  working — don't work around it with an unlicensed download.

## Subagent brief template (copy, fill the brackets, spawn)

> You are the Sound department of PROJECT ETERNIA (Godot 4.3, Mobile
> renderer, branch `aetheria-slice`, project `~/workspace/project-eternia/`).
> Read `AGENTS.md` and `STUDIO.md` first and follow them (Godot 4.3 only,
> CC0/free only, verify headless after every edit). Do NOT touch the hero,
> other departments' files, or `main`.
>
> Task: [e.g. wire the Kenney RPG Audio SFX (door, book, chop) to the
> village interactions and add one LMMS ambient loop, all .ogg 44.1 kHz].
>
> Use only: Kenney CC0 audio, LMMS 1.2.2, Audacity 3.4.2 (reinstall via apt
> first if a VM restart removed them). No copyrighted music, no generated
> recitation, no new music without user approval.
>
> Deliver: the audio files under `assets/library/audio/`, licence rows in
> `AssetLicenses.md`, and a report of what plays where (verified by a real
> headless run log, not by assumption). Verify: headless import 0 script
> errors, gdUnit 5/5. Commit on `aetheria-slice` only.
