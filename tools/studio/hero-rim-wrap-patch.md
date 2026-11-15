# Hero rim light + wrap lighting — PREPARED PATCH (do NOT apply yet)

**Status:** PREPARED ONLY, 2026-11-15. The hero shaders are owned by the
hero-rebuild agent (`d8c7420a`, MPFB rebuild). Apply this patch only after
that agent commits the new hero, then re-shoot the closeup and re-measure
the cheek pixel values (the face shader's `light_cap` was calibrated by
measurement — any lighting change re-opens that calibration).

## Why

The hero currently has two lighting gaps:

1. **No rim light.** On the shadow side the body and face go flat dark —
   the silhouette melts into the background. A fresnel rim (bright edge
   where the surface turns away from the camera) is the cheapest way to
   keep the hero readable, and it is the signature of the Genshin-style
   look.
2. **No wrap lighting on the skin.** The face shader's `ndl` band is a
   hard terminator: `ndl > 0.55 ? cap : cap * 0.84`. Skin in real life
   scatters light around the terminator (subsurface wrap), so the shadow
   side should fall off softly instead of stepping. The body `_toon()`
   materials have the same hard edge (StandardMaterial3D
   `DIFFUSE_TOON`).

## Part 1 — face shader (`assets/materials/anime_face.gdshader`)

Exact edits (line numbers are the current file's):

### 1a. Add uniforms after line 33 (`uniform float light_cap = 0.15;`)

```glsl
uniform vec3 rim_color : source_color = vec3(1.0, 0.82, 0.62);
uniform float rim_strength = 0.18;
uniform float wrap = 0.45;
```

Start `rim_strength` at **0.18**, not higher: the current file already
has a subtle fresnel emission (`EMISSION = vec3(fres * 0.06)`), and the
face was calibrated to land the cheek at warm tan (241,169,102) — a
strong rim will clip the skin to white again. Tune from screenshots in
0.05 steps.

### 1b. Replace the emission line in `fragment()`

Current:

```glsl
	EMISSION = vec3(fres * 0.06);
```

New:

```glsl
	EMISSION = rim_color * fres * rim_strength;
```

Warm rim, not white: a white rim reads as a plastic edge; warm
(1.0, 0.82, 0.62) reads as sun bouncing off skin.

### 1c. Wrap the NdotL in `light()`

Current:

```glsl
	float ndl = clamp(dot(wn, wl) * 0.5 + 0.5, 0.0, 1.0);
```

New (standard wrap diffuse — the terminator starts at `dot = -wrap`
instead of `dot = 0`):

```glsl
	float ndl = clamp((dot(wn, wl) + wrap) / (1.0 + wrap), 0.0, 1.0);
```

Everything downstream (`band`, `DIFFUSE_LIGHT`) is unchanged, so the
SDF shadow boundary and the calibrated `light_cap` keep working — the
wrap only softens the terminator, it does not move the shadow band.

## Part 2 — body toon (new shader, replaces `_toon()` for HERO parts only)

`_toon()` in `scripts/world/aetheria_slice.gd` (lines ~137-145) returns a
`StandardMaterial3D` with `DIFFUSE_TOON` / `SPECULAR_TOON`. The standard
material has **no rim or wrap hooks**, and its `next_pass` is already
taken by the inverted-hull outline — so the body rim needs a custom
shader, not a material tweak. Do NOT change `_toon()` for NPCs/props;
only the hero's body parts get the new shader.

Create `assets/materials/hero_toon_rim.gdshader` (project-original, full
text below), then in the hero builder replace the `_toon(color)` calls
for the hero body with:

```gdscript
var rim_mat := ShaderMaterial.new()
rim_mat.shader = load("res://assets/materials/hero_toon_rim.gdshader") as Shader
rim_mat.set_shader_parameter("albedo", Color(0.55, 0.58, 0.62, 1.0))  # per part
rim_mat.next_pass = _outline_mat  # outline keeps working as a next pass
```

### `hero_toon_rim.gdshader` (full text — write verbatim)

```glsl
// hero_toon_rim.gdshader — PROJECT-ORIGINAL hero toon + rim + wrap.
// Toon bands (2-step) + fresnel rim in SPECULAR_LIGHT + wrap diffuse.
// Same band positions as the StandardMaterial3D DIFFUSE_TOON the hero
// used before, so the look stays continuous with shots 07-11.
shader_type spatial;
render_mode diffuse_lambert, specular_schlick_ggx;

uniform vec4 albedo : source_color = vec4(0.55, 0.58, 0.62, 1.0);
uniform float roughness = 0.85;
uniform vec3 rim_color : source_color = vec3(1.0, 0.85, 0.65);
uniform float rim_strength = 0.30;
uniform float rim_power = 3.0;
uniform float wrap = 0.45;
uniform float band_edge = 0.55;
uniform float band_dark = 0.72;

void fragment() {
	ALBEDO = albedo.rgb;
	ROUGHNESS = roughness;
	SPECULAR = 0.5;
}

void light() {
	vec3 wn = normalize((INV_VIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
	vec3 wl = normalize((INV_VIEW_MATRIX * vec4(LIGHT, 0.0)).xyz);
	// Wrap diffuse: terminator starts at dot = -wrap.
	float ndl = clamp((dot(wn, wl) + wrap) / (1.0 + wrap), 0.0, 1.0);
	float band = ndl > band_edge ? 1.0 : band_dark;
	DIFFUSE_LIGHT = band * LIGHT_COLOR;
	// Fresnel rim: bright where the surface turns away from the camera.
	float fres = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), rim_power);
	SPECULAR_LIGHT = rim_color * fres * rim_strength * LIGHT_COLOR;
}
```

## Cost (Mali-G57 estimate, NOT measured on the phone)

- Face: 3 uniforms + ~6 ALU in `light()` — negligible, same pass.
- Body: same draw-call count (the custom shader replaces the standard
  material 1:1); ~10 extra ALU per fragment. The outline pass is
  untouched.
- No new textures, no new passes, no extra draw calls.

## Apply + verify

1. Apply Part 1 only, re-shoot the hero closeup, measure the cheek
   pixel values against the calibrated (241,169,102) and check the rim
   is visible on the shadow-side edge without clipping the lit side.
2. Apply Part 2, re-shoot closeup + back/cape, check the armour rim
   reads on the dark side and the toon bands still match shots 07-11.
3. If the face clips to white again, lower `rim_strength` first, then
   `light_cap` — never both at once.

## Rollback

- Part 1: revert the 3 edits (uniforms, EMISSION line, `ndl` line).
- Part 2: restore the `_toon(color)` calls for the hero body parts and
  delete `hero_toon_rim.gdshader`.
