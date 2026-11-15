shader_type spatial;
render_mode unshaded, cull_disabled, depth_draw_never, blend_add;

// One-shot slash arc (PROJECT ETERNIA, project-original).
// UV.x runs along the arc (0 = start, 1 = end), UV.y across its width.
// A bright leading edge sweeps along the arc as `progress` goes 0 -> 1;
// the arc fades out behind it. Additive, no bloom, one draw call.
uniform vec4 color : source_color = vec4(0.65, 0.85, 1.0, 1.0);
uniform float progress : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	float d = abs(UV.x - progress);
	float band = smoothstep(0.28, 0.0, d);
	float radial = smoothstep(0.0, 0.25, UV.y) * smoothstep(1.0, 0.55, UV.y);
	float edge = smoothstep(0.0, 0.08, UV.x) * smoothstep(1.0, 0.92, UV.x);
	ALBEDO = color.rgb * band * radial * edge * 3.0;
}
