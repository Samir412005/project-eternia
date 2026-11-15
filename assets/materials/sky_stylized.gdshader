// sky_stylized.gdshader — PROJECT-ORIGINAL stylized sky for PROJECT ETERNIA.
// Written from the technique (painted gradient + sun disc/glow + procedural
// drifting clouds), not copied from any other game's files.
// Godot 4.3 sky shader, used by a WorldEnvironment Sky resource. The sun
// direction is a uniform — set it to match the scene DirectionalLight3D
// rotation so the disc sits where the light comes from. Clouds are a cheap
// 2-octave hash value-noise on the view direction, drifting with TIME.
shader_type sky;

uniform vec3 horizon_color : source_color = vec3(0.98, 0.75, 0.55);
uniform vec3 mid_color : source_color = vec3(0.45, 0.62, 0.90);
uniform vec3 zenith_color : source_color = vec3(0.10, 0.28, 0.62);
uniform vec3 sun_direction = vec3(-0.574, 0.346, 0.742);
uniform vec3 sun_color : source_color = vec3(1.0, 0.88, 0.62);
uniform float sun_disc_size = 0.9993;
uniform float sun_glow_power = 8.0;
uniform vec3 cloud_color : source_color = vec3(1.0, 0.96, 0.92);
uniform float cloud_coverage = 0.38;
uniform float cloud_speed = 0.012;
uniform float cloud_scale = 2.2;

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

void sky() {
	vec3 dir = normalize(EYEDIR);
	float h = clamp(dir.y, -1.0, 1.0);

	// Painted gradient: warm horizon -> soft mid -> deep zenith.
	// The blue must arrive FAST above the horizon (a camera looking
	// slightly down still sees sky): horizon band is only the first
	// ~8 degrees, then the mid blue takes over.
	vec3 col;
	if (h >= 0.0) {
		col = mix(mid_color, zenith_color, pow(h, 0.55));
		col = mix(horizon_color, col, smoothstep(0.0, 0.15, h));
	} else {
		// Below the horizon: keep the warm haze so the ground line never
		// turns black.
		col = mix(horizon_color, horizon_color * 0.75, clamp(-h * 3.0, 0.0, 1.0));
	}

	// Sun disc + glow (bigger glow so the sun reads even off-centre).
	float sun_amount = clamp(dot(dir, normalize(sun_direction)), 0.0, 1.0);
	float disc = smoothstep(sun_disc_size, 0.9997, sun_amount);
	float glow = pow(sun_amount, sun_glow_power) * 0.4;
	col += sun_color * (disc * 1.0 + glow);

	// Drifting stylized clouds, only above the horizon.
	// Coverage/speed raised after the first capture showed the sky
	// reading as a flat wall: clouds must be visible and must move
	// on a seconds timescale, not a minutes one.
	if (dir.y > 0.02) {
		vec2 cuv = dir.xz / (dir.y + 0.25) * cloud_scale;
		cuv += vec2(TIME * cloud_speed, TIME * cloud_speed * 0.4);
		float n = vnoise(cuv) * 0.65 + vnoise(cuv * 2.3) * 0.35;
		float cover = smoothstep(cloud_coverage, cloud_coverage + 0.22, n);
		float fade = smoothstep(0.0, 0.18, dir.y);
		// Clouds catch the sun: warm on the sun side, soft white elsewhere.
		vec3 cloud_col = mix(cloud_color, sun_color, clamp(sun_amount * 0.5, 0.0, 0.35));
		col = mix(col, cloud_col, cover * fade * 0.9);
	}

	COLOR = col;
}
