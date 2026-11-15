# Department 03 — Animation

**Owns:** all motion — hero locomotion, combat moves, NPC idles, creature
animation, and the retargeting pipeline that makes clips fit the project's rigs.

## Inputs / Outputs

| | |
|---|---|
| Inputs | Quaternius embedded clips, Mixamo FBX, UAL mocap clips, vid2anim captures (phone video → Blender). |
| Outputs | Clips in `assets/library/animations/<source>/`, retargeted actions on the project rigs, AnimationPlayer/AnimationTree wiring in the scene. |
| Tools | Blender 4.5.9 LTS (retarget, Graph Editor cleanup), vid2anim 0.1.1 (MIT, CPU MediaPipe), Mixamo (free Adobe account, 0.01 scale gotcha). |

## Gate (must ALL pass before handoff to Build)

1. Walk/Run/Idle loop cleanly (no foot slide, no popping); combat clips hit
   on the right frame.
2. Every clip is retargeted to the project rig in Blender first — never a raw
   Mixamo FBX in the game scene.
3. Single-camera mocap (vid2anim) gets 30–60 min of Graph Editor cleanup per
   clip; feet slide and hand jitter are fixed, not shipped.
4. Headless import: 0 SCRIPT ERRORs. Licence rows in `AssetLicenses.md`
   (Mixamo = free under Adobe terms, NOT CC0 — record it exactly).

## Rules

- Mixamo is the backbone for walk/run/idle. vid2anim is for signature moves
  Mixamo doesn't have (sword slash, roll, victory).
- The Ultimate Animated Character pack has NO Crouch clip — crouch is
  procedural (lowered capsule + slowed movement), never a faked clip.
- Never ship an uncleaned mocap clip. If a clip can't be cleaned in an
  afternoon, cut it.

## Subagent brief template (copy, fill the brackets, spawn)

> You are the Animation department of PROJECT ETERNIA (Godot 4.3, Mobile
> renderer, branch `aetheria-slice`, project `~/workspace/project-eternia/`).
> Read `AGENTS.md` and `STUDIO.md` first and follow them (Godot 4.3 only,
> CC0/free only, verify headless after every edit). Do NOT touch the hero
> mesh, other departments' files, or `main`.
>
> Task: [e.g. add the Sword_Attack + Roll clips to the Warrior: retarget in
> Blender, clean the curves, wire them to the combat input with hit frames].
>
> Use only: Blender 4.5.9, vid2anim (CPU MediaPipe), Mixamo clips already
> on disk. No paid mocap, no MoCap AI (paid — vid2anim does the same free).
>
> Deliver: the clips under `assets/library/animations/`, licence rows in
> `AssetLicenses.md`, and a real screenshot or short capture proving the move
> plays in the actual Godot run (read it visually yourself). Report any foot
> slide or jitter honestly. Verify: headless import 0 script errors,
> gdUnit 5/5. Commit on `aetheria-slice` only.
