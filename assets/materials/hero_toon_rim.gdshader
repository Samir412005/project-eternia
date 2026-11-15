// hero_toon_rim.gdshader — PROJECT-ORIGINAL hero toon + rim + wrap.
// Toon bands (2-step) + fresnel rim + wrap diffuse.
// Same band positions as the StandardMaterial3D DIFFUSE_TOON the hero
// used before, so the look stays continuous with shots 07-11.
//
// DEVIATIONS FROM tools/studio/hero-rim-wrap-patch.md (verbatim text),
// each proven by isolated tests 2026-11-15 (scripts in /tmp/test_rim*.gd):
//  1. render_mode cull_disabled (not in the patch): the MPFB GLB is
//     double-sided / inverted winding (the glTF importer sets
//     cull_disabled on the imported StandardMaterial3Ds), so the
//     default cull_back culls the outward faces and the parts are
//     INVISIBLE (bare skin shows through — tests 3/5). Same fix the
//     cape shader already carries. Without this the patch cannot work
//     on this hero at all.
//  2. View-space dot(NORMAL, LIGHT) for ndl instead of the
//     INV_VIEW_MATRIX world-space transform: dot is rotation-invariant,
//     so the value is identical when it works — but the INV_VIEW_MATRIX
//     version has a proven failure mode on skinned meshes under the
//     shadowed sun (test 8: light() contribution vanishes when
//     LIGHT_COLOR is not referenced; test 11: the view-space version
//     renders correctly in the same setup).
//  3. light_cap uniform (0.40) scaling the diffuse, face-shader
//     pattern: the un-capped diffuse clips the torso to pure white
//     under the slice's shadowed sun + fill (tests 6/7: (1,1,1)) — the
//     same "render runs brighter than the model" the face shader
//     solved with light_cap 0.30. 0.40 was fitted from the slice's own
//     shot 10 (cap 0.55 still rendered the plate (240,251,255) vs the
//     toon baseline (204,220,242)); the T-pose test's 0.55 was useless
//     because everything saturates in the T-pose. Re-measure in shot 10.
//  4. Rim in EMISSION + specular_disabled instead of SPECULAR_LIGHT +
//     specular_schlick_ggx: the face-shader pattern (EMISSION fresnel
//     rim), which is proven to render under the shadowed sun; the
//     specular path's interaction with the shadowed light is unproven
//     here, and specular_disabled also removes the sky-reflection term
//     that blows flat plates facing the camera to white.
shader_type spatial;
render_mode diffuse_lambert, specular_disabled, cull_disabled;

uniform vec4 albedo : source_color = vec4(0.55, 0.58, 0.62, 1.0);
uniform float roughness = 0.85;
uniform vec3 rim_color : source_color = vec3(1.0, 0.85, 0.65);
uniform float rim_strength = 0.45;
uniform float rim_power = 3.0;
uniform float wrap = 0.45;
uniform float band_edge = 0.55;
uniform float band_dark = 0.72;
uniform float light_cap = 0.40;

void fragment() {
	ALBEDO = albedo.rgb;
	ROUGHNESS = roughness;
	// Fresnel rim as emission (face-shader pattern): warm edge light
	// on the shadow-side silhouette, independent of the specular path.
	float fres = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), rim_power);
	EMISSION = rim_color * fres * rim_strength;
}

void light() {
	// Wrap diffuse: terminator starts at dot = -wrap. View-space dot
	// (see header note 2) — identical value to the world-space form.
	float ndl = clamp((dot(NORMAL, LIGHT) + wrap) / (1.0 + wrap), 0.0, 1.0);
	float band = ndl > band_edge ? 1.0 : band_dark;
	DIFFUSE_LIGHT = band * light_cap * LIGHT_COLOR;
}
