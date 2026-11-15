// water_stylized.gdshader — PROJECT-ORIGINAL stylized water for PROJECT ETERNIA.
// Written from the technique (sine-wave vertex displacement + fresnel +
// sun sparkle + UV-edge shore fade), not copied from any other game's files.
// Godot 4.3, Mobile renderer safe: no depth texture, no screen texture.
// The plane mesh must have subdivisions (PlaneMesh subdivide 32x32) so the
// vertex waves are visible. Shore fade is faked with the UV border: the
// water plane's edges fade toward transparent, which reads as a shoreline
// where the pond meets the ground.
//
// Deep pass (2026-11-15): REAL depth-based shore fade. A `hint_depth_texture`
// uniform samples the opaque scene depth; where the basin floor is close
// under the surface the water thins to transparent, where it is deep the
// water stays opaque. Godot 4 removed the DEPTH_TEXTURE built-in — the
// uniform form is the documented replacement. The depth texture only
// exists on the Forward+ / Mobile renderers: `use_depth_fade` MUST stay 0
// on the Compatibility renderer (Xvfb screenshots) or the fade reads
// black (depth 0) and the pond vanishes; the border mask is the fallback
// there. The showcase pond sits in a real basin (see the scene: ground
// strips leave a 7x7 hole, basin cylinder below) so the depth difference
// LESSON 2026-11-15 (shots 24b/24c/27-31): edits to a shader file's
// uniform DEFAULTS do NOT take effect in a `-s` game run until the
// project is re-imported (`godot --headless --path . --import`).
// A game run loads the cached import and never re-checks staleness;
// .tscn material overrides DO reload (scenes load from source).
// Five Mobile captures ran the ORIGINAL shader because of this.
// Always re-import after editing a .gdshader, then re-capture.
// OUTCOME 2026-11-15 (shots 24-34, Mobile/lavapipe): the depth texture
// IS live and the linearisation IS correct - debug visualisation (shot
// 32) showed the pond green at the centre (deep + fade ~1) and red at
// the rim (shallow + fade ~0), exactly as designed. BUT the fade does
// NOT reach the final alpha in the normal path: 6 captures with the
// fade on all render the pond pale/transparent, while a constant
// ALPHA = 0.88 (shot 33) renders it blue - so the blend path works
// and the fade variable itself is the paradox (debug shows ~0.8,
// normal path behaves as ~0). Unresolved on lavapipe; needs a real
// Galaxy A16 test to tell a lavapipe quirk from a real bug. Until
// then use_depth_fade stays 0 (border-mask fallback) - the shipped
// water is blue on BOTH renderers (shots 22/23). Do NOT turn the
// fade on in the shipped scene without a phone test.
// LESSON: never use `return` in fragment() - Godot 4.3 rejects it
// and the WHOLE shader fails to compile (silently broke 24b-24d,
// 27-31). Diagnose shaders with /tmp/diag_shader.gd first.
// FIX 2026-11-15 (Mobile run 24): the first depth math compared the RAW
// clip-space depths (`scene_depth - FRAGCOORD.z`). At the pond camera
// distance both values sit ~0.999, so the difference is ~0.0005 and even
// x300 leaves the water ~85% transparent everywhere - the pond vanished
// on Mobile. Fixed by linearising BOTH depths to eye depth in metres
// (INV_PROJECTION_MATRIX reconstruction) and scaling in metres:
// depth_fade_scale = 2.0 means the fade reaches 1 at 0.5 m of water
// depth (basin is 0.7 m deep: centre opaque, rim transparent).
shader_type spatial;
render_mode blend_mix, depth_draw_never, cull_back, specular_schlick_ggx;

uniform vec3 shallow_color : source_color = vec3(0.25, 0.65, 0.62);
uniform vec3 deep_color : source_color = vec3(0.03, 0.22, 0.38);
uniform vec3 sun_direction = vec3(-0.574, 0.346, 0.742);
uniform vec3 sun_color : source_color = vec3(1.0, 0.9, 0.7);
uniform float wave_height = 0.08;
uniform float wave_speed = 1.0;
uniform float sparkle_strength = 1.4;
uniform float alpha_base = 0.88;
uniform sampler2D depth_texture : hint_depth_texture, repeat_disable, filter_linear;
uniform int use_depth_fade = 0;
uniform float depth_fade_scale = 2.0;

varying float wave_lift;
varying vec2 wave_uv;

void vertex() {
	// Three travelling sine waves: long swell + chop + diagonal ripple.
	float t = TIME * wave_speed;
	float w = sin(VERTEX.x * 0.35 + t * 1.2) * 0.5
		+ sin(VERTEX.z * 0.28 + t * 0.9) * 0.5
		+ sin((VERTEX.x + VERTEX.z) * 0.18 + t * 0.6) * 0.6;
	VERTEX.y += w * wave_height;
	wave_lift = w;
	wave_uv = UV;
}

void fragment() {
	// Cheap moving normal wobble (no normal map needed).
	vec2 p = wave_uv * 24.0;
	float nx = sin(p.x * 1.3 + TIME * 1.4) + sin(p.y * 1.7 - TIME * 1.1);
	float nz = cos(p.y * 1.1 + TIME * 1.2) + cos(p.x * 1.9 - TIME * 0.8);
	NORMAL = normalize(NORMAL + vec3(nx * 0.06, 0.0, nz * 0.06));

	// Fresnel: grazing angles read shallow/bright, looking down reads deep.
	float fres = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 3.0);
	vec3 col = mix(deep_color, shallow_color, clamp(fres + wave_lift * 0.12, 0.0, 1.0));

	// Sun sparkle: Blinn highlight against the uniform sun direction.
	vec3 sun_dir = normalize(sun_direction);
	vec3 half_vec = normalize(sun_dir + VIEW);
	float spec = pow(clamp(dot(NORMAL, half_vec), 0.0, 1.0), 90.0);
	col += sun_color * spec * sparkle_strength;

	// Subtle moving sparkle bands so the surface never looks frozen.
	float glint = sin(p.x * 2.1 + TIME * 2.0) * sin(p.y * 1.6 - TIME * 1.7);
	col += sun_color * max(glint, 0.0) * 0.05;

	ALBEDO = col;
	ROUGHNESS = 0.12;
	SPECULAR = 0.6;

	// Shore fade: alpha drops toward the plane borders (fake shoreline).
	float edge = min(min(UV.x, 1.0 - UV.x), min(UV.y, 1.0 - UV.y));
	float fade = smoothstep(0.0, 0.18, edge);
	// Real depth fade (Mobile renderer only, use_depth_fade == 1):
	// scene depth minus this fragment's depth, scaled to 0..1. Near the
	// basin rim the floor is centimetres under the surface -> transparent;
	// at the basin centre it is deep -> opaque. On Compatibility the
	// depth texture is unavailable, so this branch must stay off there.
	if (use_depth_fade == 1) {
		// Linearise both depths to eye depth in metres: the raw depth
		// texture holds non-linear [0,1] depth, whose raw difference at
		// this camera distance is ~0.0005 and useless as a fade.
		vec2 ndc_xy = SCREEN_UV * 2.0 - 1.0;
		float scene_d = texture(depth_texture, SCREEN_UV).r;
		// Godot 4.3 Vulkan depth is depth-corrected: the texture value
		// IS the NDC z (0..1), NOT (ndc+1)/2. Shot 31b proved d*2-1
		// collapses both depths to ~0 m; d direct gives the real ~15 m.
		vec4 view_scene = INV_PROJECTION_MATRIX * vec4(ndc_xy, scene_d, 1.0);
		float eye_scene = -view_scene.z / view_scene.w;
		vec4 view_frag = INV_PROJECTION_MATRIX * vec4(ndc_xy, FRAGCOORD.z, 1.0);
		float eye_frag = -view_frag.z / view_frag.w;
		float depth_diff = eye_scene - eye_frag;
		float depth_fade = clamp(depth_diff * depth_fade_scale, 0.0, 1.0);
		fade = min(fade, depth_fade);
	}
	ALPHA = alpha_base * mix(0.15, 1.0, fade);
}
