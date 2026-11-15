# Department 04 — VFX

**Owns:** all effects — sword slashes, fire, magic, hit sparks, golem lava
cracks, particles, and the shaders that make them read on a Mali-G57.

## Inputs / Outputs

| | |
|---|---|
| Inputs | Free Godot VFX packs (Gennai sword trails, Ember VFX Lite, Godot VFX Library — MIT/free-commercial), TripoSG/TRELLIS props from free Colab T4 (props only). |
| Outputs | GPUParticles3D/CPUParticles3D setups, trail meshes, emissive materials, effect scenes under `scenes/vfx/`. |
| Tools | Godot 4.3 (Mobile renderer — GPUParticles work here; Compatibility drops them, so VFX is tested on Mobile), Blender 4.5.9 (effect meshes). |

## Gate (must ALL pass before handoff to Build)

1. Live particles < 2,000 total at any moment; one effect ≤ 200 particles.
2. Every effect is visible in a real screenshot from an actual run — an
   effect that only exists in the editor is not done.
3. No Forward+-only features (SDFGI/VoxelGI are Forward+-only, not on
   Mobile). Glow is faked with emissive + billboards, never real bloom on
   the phone.
4. Headless import: 0 SCRIPT ERRORs. Licence rows in `AssetLicenses.md`.

## Rules

- AI 3D (TripoSG/TRELLIS) is for props (rocks, golem base, furniture) —
  never the hero, never a face. Every AI output gets Blender cleanup +
  retopology before Godot.
- The golem's lava cracks are emissive texture + a small particle ember
  loop, not a shader that costs a frame.
- Test VFX on the Mobile renderer only. A VFX pass on Compatibility proves
  nothing about the phone.

## Subagent brief template (copy, fill the brackets, spawn)

> You are the VFX department of PROJECT ETERNIA (Godot 4.3, Mobile
> renderer, branch `aetheria-slice`, project `~/workspace/project-eternia/`).
> Read `AGENTS.md` and `STUDIO.md` first and follow them (Godot 4.3 only,
> CC0/free only, verify headless after every edit). Do NOT touch the hero,
> other departments' files, or `main`.
>
> Task: [e.g. build the golem boss: rock body with emissive lava cracks,
> sword-slash trail, hit sparks, ember particles — all under the particle budget].
>
> Use only: free Godot VFX packs (Gennai/Ember, MIT), Blender 4.5.9 for
> effect meshes, TripoSG/TRELLIS on free Colab T4 for the golem base mesh
> (props only, with Blender cleanup).
>
> Deliver: the effect scenes + assets, licence rows in `AssetLicenses.md`,
> and NEW real screenshots (1280×720, Xvfb, actual Godot run, Mobile
> renderer) proving each effect is visible — read them visually yourself.
> Report particle counts and any effect that doesn't read honestly. Verify:
> headless import 0 script errors, gdUnit 5/5. Commit on `aetheria-slice` only.
