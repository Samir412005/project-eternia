// cape_sway.gdshader — toon red cloth with a vertex-sway at the free edge.
// UV.y is 0 at the pinned top, 1 at the bottom (see the Blender cape UVs),
// so the sway grows toward the hem. The vertex function runs pre-skinning,
// in the cape mesh's bind-pose local space, so the sway follows the torso.
// Graphics pass — the cape rendered BLACK from behind (shot 11). Root
// cause: the shader culled back faces (default cull_back), so from behind
// you saw straight through the cloth to the black inverted-hull outline
// duplicate, and the back face got no front light at all. Fix: cull
// disabled + flip the normal on back faces in fragment() so the back is
// lit like the front, a raised darkest band (0.34 -> 0.48), and a small
// red emissive floor so the cloth can never fall to black.
// Pass 3 (Character dept, 2026-11-15) — the cape still read SALMON
// (shot 11 sampled (255,133,92)): the uniform was too bright/warm AND the
// mesh was a flat board, so one uniform band covered the whole cloth.
// Fix: deep-red uniform (0.55,0.07,0.08 — the old (0.75,0.19,0.16) scaled
// to the observed salmon lands at ~(187,49,46)) + top band 0.65 -> 0.60,
// and the mesh now has real pleats, so the three bands vary across the
// cloth instead of one flat salmon. Sway amp 0.09 -> 0.16 so the hem
// visibly moves (outline shader matches: same amp + speed).
// CAPE FIX (2026-11-15) — the mesh HAD folds (hem y-spread 0.337) but
// still read as a flat board: this shader's 3 flat NDL bands quantised
// away all fold shading, and the old cape was buried in the tunic with
// its hem swung through the legs. The mesh is now a rebuilt draped
// cloth (9 modelled pleats, Solidify thickness, knee hem, shoulder
// wrap) AND the fold shading is painted: fold_tex
// (Hero_MPFB_Cape_Folds.png, 9 stripes phase-matched to the modelled
// pleats: ridges x1.30, valleys x0.70, deep-red base (140,18,20)) is
// sampled for ALBEDO, so the fold bands read from every angle even
// where the toon light() bands are flat. cape_color is now a tint
// (default white) instead of the albedo itself.
shader_type spatial;
render_mode diffuse_lambert, specular_disabled, cull_disabled;

uniform sampler2D fold_tex : source_color;
uniform vec4 cape_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float sway_amp = 0.16;
uniform float sway_speed = 2.6;

void vertex() {
	float w = UV.y;
	float ph = TIME * sway_speed + VERTEX.y * 1.2;
	VERTEX.x += sin(ph) * w * sway_amp;
	VERTEX.x += sin(ph * 2.0 + 1.3) * w * sway_amp * 0.35;
	VERTEX.z += cos(ph * 0.7) * w * sway_amp * 0.7;
}

void fragment() {
	// Fold texture: the painted pleat shading (ridges light, valleys
	// dark), phase-matched to the modelled pleats in the mesh.
	vec3 cloth = texture(fold_tex, UV).rgb * cape_color.rgb;
	ALBEDO = cloth;
	// Two-sided cloth: light the back face as if it faced the light.
	if (!FRONT_FACING) {
		NORMAL = -NORMAL;
	}
	// Ambient floor: red even where no directional light reaches.
	// 0.08, not 0.12: the isolated test showed the old floor plus the
	// glow/fog wash pushed the cape toward cream; the floor only needs
	// to keep the cloth from going black.
	EMISSION = cloth * 0.08;
}

void light() {
	float ndl = clamp(dot(NORMAL, LIGHT) * 0.5 + 0.5, 0.0, 1.0);
	// Graphics pass: all bands x0.65. The cape cloth's outer surface
	// is a BACK face (inverted winding), so the fragment flip points
	// its normal at the lights and it takes the TOP band from behind —
	// at 1.0 that plus ACES desaturation bleached it to cream
	// (measured (255,217,159) in shot 11). At 0.60 the back face stays
	// under 1.0, ACES no longer bleaches it, and it reads deep red.
	// Pass 3: top band 0.65 -> 0.60 with the deeper uniform, so the fold
	// crests stay deep red instead of bleaching toward salmon/cream.
	float band = ndl > 0.6 ? 0.60 : (ndl > 0.25 ? 0.44 : 0.31);
	DIFFUSE_LIGHT = vec3(band) * LIGHT_COLOR;
}
