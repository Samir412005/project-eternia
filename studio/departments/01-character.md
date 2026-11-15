# Department 01 — Character

**Owns:** the hero and every NPC/creature — base mesh, face, hair, cape,
armour, textures, rig, and the Godot shaders that shade them.

## Inputs / Outputs

| | |
|---|---|
| Inputs | Library packs (Quaternius RPG Nov 2020 + Ultimate Animated Character — CC0), MPFB 2.0.18 / CharMorph bases, Krita face textures, Mixamo/UAL/vid2anim clips. |
| Outputs | `assets/library/characters/<name>/` (GLB/FBX + textures + `.blend` source), shaders in `assets/materials/`, hero wired into the scene. |
| Tools | Blender 4.5.9 LTS (model/rig/animate), Krita 5.3.4.1 (paint), Godot 4.3 (Toon + inverted-hull outline + SDF face shader). |

## Gate (must ALL pass before handoff to Build)

1. Hero ≤ 15k tris; textures ≤ 1024 px (2048 hero only).
2. Face reads as anime in a real 1280×720 screenshot — big painted eyes,
   hair cards framing the face (never shadowing it), cape reads as flowing
   cloth from front AND behind.
3. Walk/Run/Idle clips wired to controller speed; no T-pose, no sliding feet.
4. Headless import: 0 SCRIPT ERRORs. Licence row in `AssetLicenses.md`.

## Rules

- Never ship a procedural pill hero. Never use VRoid-derived content without
  reading the live VRoid terms. Never use Human Generator assets (paid).
  Never use MMD game models (technique only).
- The SDF face-shader kit licence must be read before depending on it; if
  unclear, port the MMDX `hoyo_toon` math.
- Work on a branch, one change at a time, test each change before the next.

## Subagent brief template (copy, fill the brackets, spawn)

> You are the Character department of PROJECT ETERNIA (Godot 4.3, Mobile
> renderer, branch `aetheria-slice`, project `~/workspace/project-eternia/`).
> Read `AGENTS.md` and `STUDIO.md` first and follow them (Godot 4.3 only,
> CC0/free only, verify headless after every edit). Do NOT touch
> `scenes/main/main.tscn`, other departments' files, or `main`.
>
> Task: [e.g. re-style the Warrior hero face: remodel eyes, paint the 1024px
> anime face texture in Krita, add hair cards, bake the cloth cape].
>
> Use only: Blender 4.5.9 (`~/workspace/tools/blender-4.5/`), Krita
> (`~/workspace/tools/krita/squashfs-root/usr/bin/krita` under xvfb-run),
> Quaternius CC0 packs in `assets/library/manifests/`.
>
> Deliver: the new/changed asset files under `assets/library/characters/`,
> the licence row added to `AssetLicenses.md`, and NEW real screenshots
> (1280×720, Xvfb, actual Godot run) in `screenshots-aetheria/` that you
> have read visually yourself. Report honestly what the face/hair/cape
> actually look like, including remaining flaws. Verify: headless import
> 0 script errors, gdUnit 5/5. Commit on `aetheria-slice` only.
