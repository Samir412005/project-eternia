// lut_grade.gdshader — PROJECT-ORIGINAL cinematic LUT grade for PROJECT ETERNIA.
// Applies a Hald CLUT (32^3, stored as a 1024x32 strip) to the whole
// screen through a full-screen ColorRect sampling the screen texture.
// Why not WorldEnvironment: Godot 4.3's Environment has NO LUT slot —
// only brightness/contrast/saturation adjustments — so the LUT lives
// here (canvas_item + hint_screen_texture), the standard Godot 4 way to
// grade without a CompositorEffect. Written from the technique, not
// copied from any other game's files. The LUT texture must be imported
// with mipmaps OFF (tile bleed) — see assets/library/textures/lut/
// MANIFEST.md.
shader_type canvas_item;

uniform sampler2D screen_tex : hint_screen_texture, repeat_disable, filter_linear;
uniform sampler2D lut_tex : repeat_disable, filter_linear;
uniform float strength = 1.0;

vec3 apply_lut(vec3 c) {
	c = clamp(c, 0.0, 1.0);
	float b = c.b * 31.0;
	float b0 = floor(b);
	float b1 = min(b0 + 1.0, 31.0);
	float f = fract(b);
	vec2 uv0 = vec2((b0 * 32.0 + c.r * 31.0 + 0.5) / 1024.0, (c.g * 31.0 + 0.5) / 32.0);
	vec2 uv1 = vec2((b1 * 32.0 + c.r * 31.0 + 0.5) / 1024.0, (c.g * 31.0 + 0.5) / 32.0);
	vec3 c0 = texture(lut_tex, uv0).rgb;
	vec3 c1 = texture(lut_tex, uv1).rgb;
	return mix(c0, c1, f);
}

void fragment() {
	vec3 col = texture(screen_tex, SCREEN_UV).rgb;
	vec3 graded = apply_lut(col);
	COLOR = vec4(mix(col, graded, strength), 1.0);
}
