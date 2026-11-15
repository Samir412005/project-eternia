// light_shaft.gdshader — PROJECT-ORIGINAL sun shafts (god rays) for PROJECT ETERNIA.
// A soft vertical-gradient quad, additively blended: bright near the sun,
// fading out toward the ground and the edges. Written from the technique,
// not copied from any other game's files. Godot 4.3, Mobile renderer safe
// (unshaded, one texture sample, no depth write). The gradient texture is
// symmetric top/bottom so the quad reads as a shaft from either camera
// side; the quad itself must be tilted to match the sun direction.
shader_type spatial;
render_mode blend_add, depth_draw_never, cull_disabled, unshaded, fog_disabled;

uniform sampler2D gradient_tex : source_color;
uniform vec4 shaft_color : source_color = vec4(1.0, 0.88, 0.62, 1.0);
uniform float intensity = 0.12; // was 0.5: blew out to white pillars on both renderers (shots 21/23/24/25)

void fragment() {
	vec4 g = texture(gradient_tex, UV);
	ALBEDO = shaft_color.rgb * g.rgb;
	ALPHA = g.a * intensity;
}
