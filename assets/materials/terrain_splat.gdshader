// terrain_splat.gdshader — PROJECT-ORIGINAL triplanar PBR splat for PROJECT ETERNIA.
// Blends the ambientCG PBR sets (grass / dirt / stone) by world height and
// slope, with triplanar mapping so steep faces never stretch. Written from
// the technique, not copied from any other game's files.
// Godot 4.3, Mobile renderer safe (plain texture samples, no depth/screen
// texture). Cost: ~21 texture samples per fragment — use on small patches
// only; a whole open world on the A16 wants a cheaper 2-axis variant.
// The mesh must be REAL height-varied geometry (see scenes/tests/
// terrain_patch.mesh): the slope term reads the world normal.
shader_type spatial;

uniform sampler2D grass_albedo : source_color;
uniform sampler2D grass_normal : hint_normal;
uniform sampler2D grass_rough;
uniform sampler2D dirt_albedo : source_color;
uniform sampler2D dirt_normal : hint_normal;
uniform sampler2D dirt_rough;
uniform sampler2D stone_albedo : source_color;
uniform sampler2D stone_normal : hint_normal;
uniform sampler2D stone_rough;

uniform float texture_scale = 0.3;
uniform float normal_strength = 0.7;
uniform float dirt_slope_start = 0.25;
uniform float dirt_slope_end = 0.60;
uniform float stone_slope_start = 0.70;
uniform float stone_slope_end = 0.90;
uniform float low_dirt_height = 0.8;

varying vec3 world_pos;
varying vec3 world_normal;

vec3 tri_albedo(sampler2D tex, vec3 wp, vec3 wn, float scale) {
	vec3 w = pow(abs(wn), vec3(4.0));
	w /= (w.x + w.y + w.z + 0.0001);
	vec3 cx = texture(tex, wp.zy * scale).rgb;
	vec3 cy = texture(tex, wp.xz * scale).rgb;
	vec3 cz = texture(tex, wp.xy * scale).rgb;
	return cx * w.x + cy * w.y + cz * w.z;
}

// Sampled tangent-space normals, reoriented per projection axis into
// world space (X face: sampled z -> world x; Y face: sampled z -> world
// y; Z face: already aligned), then blended by the same weights.
vec3 tri_normal(sampler2D tex, vec3 wp, vec3 wn, float scale) {
	vec3 w = pow(abs(wn), vec3(4.0));
	w /= (w.x + w.y + w.z + 0.0001);
	vec3 nx = texture(tex, wp.zy * scale).rgb * 2.0 - 1.0;
	vec3 ny = texture(tex, wp.xz * scale).rgb * 2.0 - 1.0;
	vec3 nz = texture(tex, wp.xy * scale).rgb * 2.0 - 1.0;
	nx = vec3(nx.z, nx.y, nx.x);
	ny = vec3(ny.x, ny.z, ny.y);
	return nx * w.x + ny * w.y + nz * w.z;
}

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	world_normal = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
}

void fragment() {
	vec3 wp = world_pos;
	vec3 wn = normalize(world_normal);
	float slope = 1.0 - clamp(wn.y, 0.0, 1.0);

	// Dirt on moderate slopes (worn hillsides) and on low flat ground;
	// stone on the steepest faces; grass is the default.
	// TUNED 2026-11-15 (slice integration): showcase shot 17 proved the
	// dirt too strong — the flat top read as dirt, not grass. The
	// slope band moved up (0.25-0.60) and the low-ground dirt term
	// dropped 0.6 -> 0.25, so grass dominates the flat top and dirt
	// only shows on real slopes and at the very base.
	// RETUNED same day (slice shot 39): the ridge's steep EAST face
	// (slope ~0.55, shaded — the sun is in the south-west) rendered
	// as a near-black grey scar under the old stone band (0.55-0.80).
	// Stone now starts at 0.70, so that face reads as dirt (warm brown
	// in shade) instead of grey stone; only the very steepest faces
	// (>0.70) get stone.
	float dirt_w = smoothstep(dirt_slope_start, dirt_slope_end, slope);
	dirt_w += (1.0 - smoothstep(0.1, low_dirt_height, wp.y)) * 0.25;
	float stone_w = smoothstep(stone_slope_start, stone_slope_end, slope);
	float grass_w = 1.0;
	float total = grass_w + dirt_w + stone_w;
	grass_w /= total;
	dirt_w /= total;
	stone_w /= total;

	vec3 alb = tri_albedo(grass_albedo, wp, wn, texture_scale) * grass_w
		+ tri_albedo(dirt_albedo, wp, wn, texture_scale) * dirt_w
		+ tri_albedo(stone_albedo, wp, wn, texture_scale) * stone_w;
	vec3 nrm = tri_normal(grass_normal, wp, wn, texture_scale) * grass_w
		+ tri_normal(dirt_normal, wp, wn, texture_scale) * dirt_w
		+ tri_normal(stone_normal, wp, wn, texture_scale) * stone_w;
	float rgh = texture(grass_rough, wp.xz * texture_scale).r * grass_w
		+ texture(dirt_rough, wp.xz * texture_scale).r * dirt_w
		+ texture(stone_rough, wp.xz * texture_scale).r * stone_w;

	ALBEDO = alb;
	// NORMAL here is view-space: perturb the world normal, then go back.
	vec3 wn_vs = NORMAL;
	vec3 wn_ws = normalize((INV_VIEW_MATRIX * vec4(wn_vs, 0.0)).xyz);
	vec3 perturbed_ws = normalize(wn_ws + nrm * normal_strength);
	NORMAL = (VIEW_MATRIX * vec4(perturbed_ws, 0.0)).xyz;
	ROUGHNESS = clamp(rgh, 0.05, 1.0);
	SPECULAR = 0.5;
}
