// wind_sway.gdshader — PROJECT-ORIGINAL vertex wind for PROJECT ETERNIA.
// Sways trees and grass tufts: the sway weight grows with world height
// (base stays planted, tips move most), a fast ripple rides on a slow
// gust. Written from the technique, not copied from any other game's files.
// Godot 4.3, Mobile renderer safe (vertex math only, no textures unless
// use_alpha is on). One shader serves trees (sway_height ~2.6) and grass
// quads (sway_height ~0.6); set use_alpha=1 + alpha_tex for cutout grass
// (depth_prepass_alpha is Godot 4's cutout path — there is no
// alpha_scissor render mode in 4.3).
shader_type spatial;
render_mode cull_disabled, depth_prepass_alpha;

uniform vec4 color : source_color = vec4(0.25, 0.55, 0.25, 1.0);
uniform float wind_strength = 0.10;
uniform float wind_speed = 1.3;
uniform float sway_height = 2.6;
uniform int use_alpha = 0;
uniform sampler2D alpha_tex;
uniform float alpha_cutoff = 0.45;

varying vec2 uv;

void vertex() {
	uv = UV;
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	float w = clamp(wp.y / sway_height, 0.0, 1.0);
	// Slow gust (large scale) modulates a fast ripple (small scale).
	float gust = 0.6 + 0.4 * sin(TIME * 0.35 + wp.x * 0.12 + wp.z * 0.09);
	float s = sin(TIME * wind_speed + wp.x * 0.7 + wp.z * 0.5) * wind_strength * w * gust;
	float s2 = cos(TIME * wind_speed * 0.83 + wp.z * 0.9) * wind_strength * 0.6 * w * gust;
	VERTEX.x += s;
	VERTEX.z += s2;
}

void fragment() {
	ALBEDO = color.rgb;
	ROUGHNESS = 0.9;
	SPECULAR = 0.5;
	if (use_alpha == 1) {
		ALPHA = texture(alpha_tex, uv).a;
	}
}
