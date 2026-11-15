// cape_outline.gdshader — inverted-hull outline for the cape, with the same
// vertex sway as cape_sway.gdshader so the outline follows the cloth.
// Used on a duplicate of the cape MeshInstance3D (see aetheria_slice.gd).
// Pass 3: sway amp/speed match cape_sway (0.16 / 2.6) or the hull lags the cloth.
shader_type spatial;
render_mode cull_front, unshaded, fog_disabled;

uniform vec4 outline_color : source_color = vec4(0.04, 0.03, 0.07, 1.0);
uniform float outline_width : hint_range(0.0, 0.1) = 0.035;
uniform float sway_amp = 0.16;
uniform float sway_speed = 2.6;

void vertex() {
	float w = UV.y;
	float ph = TIME * sway_speed + VERTEX.y * 1.2;
	VERTEX.x += sin(ph) * w * sway_amp;
	VERTEX.x += sin(ph * 2.0 + 1.3) * w * sway_amp * 0.35;
	VERTEX.z += cos(ph * 0.7) * w * sway_amp * 0.7;
	VERTEX += NORMAL * outline_width;
}

void fragment() {
	ALBEDO = outline_color.rgb;
}
