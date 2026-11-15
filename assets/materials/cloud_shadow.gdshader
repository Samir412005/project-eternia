// cloud_shadow.gdshader — PROJECT-ORIGINAL scrolling cloud shadows for PROJECT ETERNIA.
// A large flat sheet above the scene; a two-octave value-noise cloud layer
// drifts with TIME and darkens the ground where the clouds are. Written
// from the technique, not copied from any other game's files. Godot 4.3,
// Mobile renderer safe (one noise evaluation, no textures).
// Placement note: the sheet must sit ABOVE everything it should shadow
// (y ~2.9 in the showcase: above the trees and house, below the camera),
// and it only darkens surfaces that pass the depth test behind it — so
// from a low camera (below the sheet) it would band the sky; prove it
// from the high camera only.
// SLICE LESSON 2026-11-15: in the main slice every camera sits below
// any sheet height that clears the windmill (~10 m), so the sheet can
// only darken ground seen from a camera ABOVE it — the dedicated high
// shot (42) proves the clouds move; the street/vista shots cannot show
// them. Edge fade added the same day so the sheet's borders never read
// as hard dark blotches against the sky from the vista camera.
shader_type spatial;
render_mode blend_mix, depth_draw_never, unshaded, fog_disabled, cull_disabled;

uniform float cloud_speed = 0.02;
uniform float cloud_scale = 0.06;
uniform float cloud_coverage = 0.45;
uniform float shadow_strength = 0.32;

varying vec3 world_pos;
varying vec2 uv;

float hash21(vec2 p) {
	p = fract(p * vec2(123.34, 456.21));
	p += dot(p, p + 45.32);
	return fract(p.x * p.y);
}

float vnoise(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	vec2 u = f * f * (3.0 - 2.0 * f);
	float a = hash21(i);
	float b = hash21(i + vec2(1.0, 0.0));
	float c = hash21(i + vec2(0.0, 1.0));
	float d = hash21(i + vec2(1.0, 1.0));
	return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	uv = UV;
}

void fragment() {
	vec2 p = world_pos.xz * cloud_scale + vec2(TIME * cloud_speed, TIME * cloud_speed * 0.6);
	float n = vnoise(p) * 0.65 + vnoise(p * 2.3) * 0.35;
	float cover = smoothstep(cloud_coverage, cloud_coverage + 0.28, n);
	// Edge fade: the sheet's borders fade to transparent over the
	// outer 15% of the UV, so from a camera below the sheet its edge
	// never reads as a hard dark band against the sky.
	float edge = smoothstep(0.0, 0.15, uv.x) * smoothstep(1.0, 0.85, uv.x)
		* smoothstep(0.0, 0.15, uv.y) * smoothstep(1.0, 0.85, uv.y);
	ALBEDO = vec3(0.0);
	ALPHA = cover * shadow_strength * edge;
}
