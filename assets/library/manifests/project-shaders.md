# Project shaders — manifest (IN PLACE, owned by Character dept)

- **Current location:** `assets/materials/`
- **Licence:** project-original (written in this studio, no third-party code).
- **Files:** `outline.gdshader` (inverted-hull outline — 0.00035 width for
  skinned meshes; the 0.035 width ballooned before skinning), `anime_face.gdshader`,
  `cape_outline.gdshader`, `cape_sway.gdshader` (hero agent, in flux, 2026-11-15).
- **Pending (licence UNVERIFIED — do not ship):** the Godot Anime SDF Shader Kit
  (`albanogiovanni/godot-anime-sdf-shader`, Genshin face-shadow technique).
  Its licence was not stated in the catalog listing. The hero agent must read
  the repo licence before depending on it; if unclear, port the MMDX
  `hoyo_toon` math instead (technique documented, no third-party code).
- **Rule:** a shader is not "in the game" until it is imported, applied to
  the hero, and visible in a real screenshot from an actual run.
