shader_type spatial;
render_mode cull_front, unshaded, fog_disabled;

// Inverted-hull outline: draws the mesh once more, scaled out along its
// normals, front faces culled. Use as a next_pass on a hero material.
// Cheap on mobile: +1 draw call per outlined mesh — hero only.
uniform vec4 outline_color : source_color = vec4(0.04, 0.03, 0.07, 1.0);
uniform float outline_width : hint_range(0.0, 0.1) = 0.035;

void vertex() {
	VERTEX += NORMAL * outline_width;
}

void fragment() {
	ALBEDO = outline_color.rgb;
}
