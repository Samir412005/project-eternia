// anime_face.gdshader — Genshin-style moving face shadow, geometric version.
// Own port of the MMDX hoyo_toon math (head-bone-relative light azimuth):
// the shadow boundary sweeps across the face as the light orbits the head,
// no painted SDF texture needed. The face UV is a front planar projection
// (U = character's left -> right), so the boundary is a function of U.
// head_right_world is updated per frame from the Head bone (see
// aetheria_slice.gd). Warm rose shadow colour: plain black looks muddy.
// Pass 2: the light multiplier is capped (band max 0.88, not 1.0) — the
// pass-1 skin still clipped to pale/cream under sun + sky ambient even
// after the texture was darkened 0.8x, so the shader itself must not
// hand the face a full-strength light.
// Graphics pass: cap 0.88 -> 0.70 -> 0.50 -> 0.30 -> 0.15, calibrated
// by MEASUREMENT, not by the light model: an isolated face-shader test
// (quad + real face texture + real scene environment) showed the render
// runs ~4-5x brighter than the naive model (sun+fill energies x cap) —
// cap 0.50 still rendered (255,239,177), cap 0.30 rendered (255,214,145),
// and only cap 0.15 lands the cheek at warm tan (241,169,102) in the
// real config (ACES, fog, warm colour ambient). The extra brightness is
// in the engine's light path (per-light DIFFUSE_LIGHT accumulation +
// ACES desaturation of anything over 1.0), so the cap has to absorb it.
// The shadow band stays cap x 0.84, so the SDF shadow side goes
// properly dark — the anime look. (Capping the shader alone could not
// fix it: Godot ADDS the two directional lights, 1.3 x 0.88 was 1.14 —
// and the ambient and glow added more on top.)
// MPFB hero (2026-11-15): the painted eyes read as unreadable dark dots
// at cap 0.15 (shot 10, 12:00) — the cap dims the amber iris and the
// white highlights to near-black. Raised to 0.30: the old calibration
// measured cap 0.30 at (255,214,145) on the cheek — bright warm, not
// clipped white — and the features gain the brightness they need to read.
shader_type spatial;
render_mode diffuse_lambert, specular_disabled, shadows_disabled;

uniform sampler2D albedo_tex : source_color;
uniform vec3 head_right_world = vec3(1.0, 0.0, 0.0);
uniform vec3 shadow_color : source_color = vec3(0.60, 0.36, 0.40);
uniform float shadow_softness = 0.08;
uniform float shadow_reach = 0.5;
uniform float light_cap = 0.30;
uniform vec3 rim_color : source_color = vec3(1.0, 0.82, 0.62);
uniform float rim_strength = 0.18;
uniform float wrap = 0.45;

void fragment() {
	ALBEDO = texture(albedo_tex, UV).rgb;
	float fres = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 3.0);
	EMISSION = rim_color * fres * rim_strength;
}

void light() {
	vec3 wn = normalize((INV_VIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
	vec3 wl = normalize((INV_VIEW_MATRIX * vec4(LIGHT, 0.0)).xyz);
	vec3 l_xz = normalize(wl * vec3(1.0, 0.0, 1.0));
	vec3 h_xz = normalize(head_right_world * vec3(1.0, 0.0, 1.0));
	float azimuth = clamp(dot(l_xz, h_xz), -1.0, 1.0);
	// Shadow on the side away from the light; none for a front light.
	float b_left = azimuth * shadow_reach;
	float b_right = 1.0 + azimuth * shadow_reach;
	float sh_left = (1.0 - smoothstep(b_left - shadow_softness, b_left + shadow_softness, UV.x)) * step(0.001, azimuth);
	float sh_right = smoothstep(b_right - shadow_softness, b_right + shadow_softness, UV.x) * step(azimuth, -0.001);
	float shadow = max(sh_left, sh_right);
	vec3 shade = mix(vec3(1.0), shadow_color, shadow);
	float ndl = clamp((dot(wn, wl) + wrap) / (1.0 + wrap), 0.0, 1.0);
	float band = ndl > 0.55 ? light_cap : light_cap * 0.84;
	DIFFUSE_LIGHT = shade * band * LIGHT_COLOR;
}
