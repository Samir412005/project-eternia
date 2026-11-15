shader_type spatial;
render_mode unshaded, cull_disabled, depth_draw_never, blend_add;

// Sword-trail ribbon shader (PROJECT ETERNIA, project-original).
// The ribbon mesh carries its fade in the vertex colour: bright at the
// blade, black at the tail. Additive blending makes black invisible, so
// no alpha sorting is needed and it costs one draw call on Mobile.
// Glow is faked with additive colour only — never real bloom.
varying vec4 v_col;

void vertex() {
	v_col = COLOR;
}

void fragment() {
	ALBEDO = v_col.rgb;
}
