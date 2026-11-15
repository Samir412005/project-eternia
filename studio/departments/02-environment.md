# Department 02 — Environment

**Owns:** the world — village, forest, dungeon, terrain, sky, water, lighting,
and every building/prop/tree/rock in it.

## Inputs / Outputs

| | |
|---|---|
| Inputs | KayKit Medieval Hexagon Pack (CC0), Kenney Nature Kit (CC0), Poly Haven HDRI (CC0, reference only), Blender heightmaps, Material Maker textures. |
| Outputs | `assets/library/environments/<kit>/`, scenes under `scenes/world/`, baked LightmapGI data. |
| Tools | Blender 4.5.9 LTS (terrain/props), Material Maker 1.8 (procedural textures), Godot 4.3 (ProceduralSky, fog, one directional sun + baked GI). |

## Gate (must ALL pass before handoff to Build)

1. One zone at a time: village OR forest OR dungeon — never a seamless open
   world (load screens between zones, Honkai-style).
2. Visible tris < 100k, draw calls < 200 per frame in the zone.
3. No visible ground-plane edge at the horizon (fog + silhouette + painted
   skybox hide it); no empty plaza — every open space has a purpose/prop.
4. Headless import: 0 SCRIPT ERRORs. Licence rows in `AssetLicenses.md`.

## Rules

- Terrain3D is FORBIDDEN on 4.3 (needs 4.5+). Use a hand-built heightmap
  mesh or modular kits until the 4.7 branch exists.
- The shipped game uses ProceduralSky + one sun + baked LightmapGI. The HDRI
  is a lighting reference only — never a runtime skybox on the phone.
- One building ≤ 5k tris. Reuse kit pieces; never model a one-off building
  the kit already has.

## Subagent brief template (copy, fill the brackets, spawn)

> You are the Environment department of PROJECT ETERNIA (Godot 4.3, Mobile
> renderer, branch `aetheria-slice`, project `~/workspace/project-eternia/`).
> Read `AGENTS.md` and `STUDIO.md` first and follow them (Godot 4.3 only,
> CC0/free only, verify headless after every edit). Do NOT touch the hero,
> other departments' files, or `main`.
>
> Task: [e.g. build the forest zone: terrain mesh, trees/rocks from the
> Kenney kit, golem arena, fog + vista backdrop, load screen from the village].
>
> Use only: Blender 4.5.9, Material Maker 1.8, the KayKit/Kenney CC0 kits in
> `assets/library/manifests/`.
>
> Deliver: the zone scene + assets under `assets/library/environments/`,
> licence rows in `AssetLicenses.md`, and NEW real screenshots (1280×720,
> Xvfb, actual Godot run) in `screenshots-aetheria/` that you have read
> visually yourself. Report the visible tri/draw-call counts and any horizon
> or empty-space flaws honestly. Verify: headless import 0 script errors,
> gdUnit 5/5. Commit on `aetheria-slice` only.
