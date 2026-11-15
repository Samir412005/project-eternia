extends Node3D
## AetheriaSlice — first real playable slice of the Aetheria mini-RPG.
## A village street scene built at runtime from CC0 assets (KayKit medieval
## houses/props, Kenney trees) + a REAL rigged hero: Quaternius Warrior
## (CC0, 44-bone rig, 14 embedded clips) re-styled in Blender as an anime
## hero — painted 1024px face (big amber eyes, brows, blush, smile),
## lifted fringe + layered hair cards, baked cloth cape — exported as
## Warrior_Anime.glb (the old FBX + procedural pill hero are gone).
## Face shading: a geometric Genshin-style SDF shadow (anime_face.gdshader,
## own port of the hoyo_toon head-bone math, no painted SDF needed).
## The old procedural pill hero survives only as the green villager NPC.
## Reuses the ETERNIA player controller + camera + HUD.
## Playable: WASD/arrows or the touch joystick move the hero.
## Screenshot mode: run with `-- --aetheria-shots` to capture real
## 1280x720 frames from the actual run into screenshots-aetheria/.

const SHOT_DIR := "/home/hatch/workspace/project-eternia/screenshots-aetheria"
const HERO_SCENE := "res://scenes/player/player.tscn"
const WARRIOR_SCENE := "res://assets/characters/quaternius/Warrior_Anime.glb"
const MPFB_HERO_SCENE := "res://assets/characters/mpfb/Hero_MPFB.glb"
const USE_MPFB_HERO := true # New MPFB-based anime hero (CC0 base mesh, real
	# rigged human, painted face, raycast hair, baked cloth cape, retargeted
	# clips). false = the old Quaternius re-skin (fallback).
const MPFB_HERO_SCALE := 1.0 # MPFB hero is already ~1.70 m.
const MPFB_SHIELD_POS := Vector3(0.46, 1.22, 0.03) # Left forearm, idle pose
	# (the MPFB hero faces +Z in Godot, so his left is +X; the -0.46 value
	# put the shield on the sword arm, verified 11:50).
const SWORD_SCENE := "res://assets/characters/kaykit/sword_1handed.gltf"
const WARRIOR_SCALE := 0.60 # Raw height 2.98m -> ~1.79m.
const SHIELD_SCENE := "res://assets/characters/kaykit/shield_round.gltf"
const FACE_SHADER := "res://assets/materials/anime_face.gdshader"
const CAPE_SHADER := "res://assets/materials/cape_sway.gdshader"
const CAPE_FOLD_TEX := "res://assets/characters/mpfb/Hero_MPFB_Cape_Folds.png"
const CAPE_OUTLINE_SHADER := "res://assets/materials/cape_outline.gdshader"
const TREE_SCENE := "res://assets/environments/kenney-nature/tree_cone.glb"
const FLOWER_SCENE := "res://assets/environments/kenney-nature/flower_redA.glb"
const ROCK_SCENE := "res://assets/environments/kenney-nature/cliff_block_rock.glb"
# Deep-graphics integration (2026-11-15): showcase shaders/materials
# brought into the main slice. PBR sets are ambientCG (CC0, already in
# AssetLicenses.md); the mossy rock is TripoSG output (own generation).
const SPLAT_SHADER := "res://assets/materials/terrain_splat.gdshader"
const WIND_SHADER := "res://assets/materials/wind_sway.gdshader"
const WATER_SHADER := "res://assets/materials/water_stylized.gdshader"
const LUT_SHADER := "res://assets/materials/lut_grade.gdshader"
const LUT_TEX := "res://assets/library/textures/lut/cinematic_warm.png"
const TERRAIN_PATCH_MESH := "res://scenes/tests/terrain_patch.mesh"
const MOSSY_ROCK_SCENE := "res://assets/library/environments/mossy-rock-10k.glb"
const PBR := "res://assets/library/textures/pbr/"
const MED := "res://assets/environments/kaykit-medieval/buildings/green/"
const PROPS := "res://assets/environments/kaykit-medieval/decoration/props/"
const ANIM_IDLE := "Idle_Weapon"
const ANIM_WALK := "Walk"
const ANIM_RUN := "Run"

var _shots_mode: bool = false
var _island_a: Node3D = null
var _island_b: Node3D = null
var _island_t: float = 0.0
var _shot_cam: Camera3D = null
var _outline_mat: ShaderMaterial = null
var _player: CharacterBody3D = null
var _warrior_anim: AnimationPlayer = null
var _warrior_root: Node3D = null
var _current_anim: String = ""
var _face_mat: ShaderMaterial = null
var _skeleton: Skeleton3D = null
var _head_bone_idx: int = -1
var _npc_area: Area3D = null
var _building_colliders: int = 0
var _golem_quest_accepted: bool = false

# ------------------------------------------------------------------ ready

func _ready() -> void:
	_outline_mat = ShaderMaterial.new()
	var outline_shader: Shader = load("res://assets/materials/outline.gdshader") as Shader
	_outline_mat.shader = outline_shader
	_build_environment()
	_build_ground()
	_build_village()
	_build_plaza_density()
	_build_vista()
	_build_horizon()
	_build_npc()
	_build_vignette()
	_build_lightmap_gi()
	_build_multimeshes()
	_build_terrain_patch()
	# NO cloud sheet: _build_cloud_shadows() was REMOVED 2026-11-15 —
	# the sheet does not survive the move to the slice (see the removed
	# function below for the evidence). Do not re-add it without a
	# projection-based cloud approach; a physical sheet bands the sky
	# from every low camera in this scene.
	_build_pond()
	_build_rock_clearing()
	_build_lut_grade()
	_wire_player()
	_ensure_quest_manager()
	DialogueManager.dialogue_started.connect(_on_dialogue_started)
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)
	_shot_cam = get_node_or_null("ShotCam") as Camera3D
	_shots_mode = "--aetheria-shots" in OS.get_cmdline_user_args()
	if "--collision-test" in OS.get_cmdline_user_args():
		_run_collision_test()
	elif "--dialogue-test" in OS.get_cmdline_user_args():
		_run_dialogue_test()
	elif _shots_mode:
		DirAccess.make_dir_recursive_absolute(SHOT_DIR)
		_run_shots()

func _process(delta: float) -> void:
	_island_t += delta
	if _island_a:
		_island_a.position.y = 15.0 + sin(_island_t * 0.5) * 0.6
	if _island_b:
		_island_b.position.y = 18.0 + sin(_island_t * 0.4 + 1.7) * 0.8
	_drive_warrior_anim()
	_update_face_shader()

func _drive_warrior_anim() -> void:
	# In shots mode the screenshot routine sets poses explicitly.
	if _shots_mode or _warrior_anim == null or _player == null:
		return
	var speed: float = 0.0
	if _player.has_method("get"):
		speed = float(_player.get("current_speed"))
	if speed < 0.0:
		speed = 0.0
	var target: String = ANIM_IDLE
	if speed >= 5.5:
		target = ANIM_RUN
	elif speed >= 0.3:
		target = ANIM_WALK
	if target != _current_anim:
		_warrior_anim.play(target)
		_current_anim = target

func _update_face_shader() -> void:
	# The anime face shadow needs the head's world-space right vector so
	# the shadow boundary sweeps correctly as the head turns.
	if _face_mat == null or _skeleton == null or _head_bone_idx < 0:
		return
	var pose: Transform3D = _skeleton.get_bone_global_pose(_head_bone_idx)
	var world_pose: Transform3D = _skeleton.global_transform * pose
	var right: Vector3 = world_pose.basis.x.normalized()
	_face_mat.set_shader_parameter("head_right_world", right)

func _set_warrior_pose(anim_name: String, seek_time: float) -> void:
	# Deterministic pose for screenshots: play, seek, then pause so the
	# low Xvfb frame rate cannot advance the clip past the pose.
	if _warrior_anim == null:
		return
	_warrior_anim.play(anim_name)
	_warrior_anim.seek(seek_time, true)
	_warrior_anim.pause()
	_current_anim = anim_name

# ------------------------------------------------------------------ materials

func _toon(color: Color, roughness: float = 0.85) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = color
	m.roughness = roughness
	m.diffuse_mode = BaseMaterial3D.DIFFUSE_TOON
	m.specular_mode = BaseMaterial3D.SPECULAR_TOON
	m.metallic_specular = 0.4
	# MSAA/SSAO patch (2026-11-15): anisotropic filtering is NOT enabled
	# by default on 3D materials — without this opt-in the project.godot
	# anisotropic_filtering_level changes nothing. The slice's ground /
	# street / plaza are flat-colour _toon() materials today, so this is
	# a no-op until a texture is added; it pins the behaviour for the
	# PBR ground/path materials the slice adopts (splat patch, rock).
	m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	return m

func _flat(color: Color) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = color
	m.roughness = 1.0
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	return m

func _box(parent: Node3D, size: Vector3, pos: Vector3, mat: Material, outline: bool = false) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = size
	mesh.material = mat
	mi.mesh = mesh
	mi.position = pos
	# Graphics pass: the helpers build the NPC only (and the horizon
	# hills, via _sphere) — background dressing casts no shadow, which
	# saves a second draw of each piece into the shadow map.
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	if outline and _outline_mat:
		(mat as StandardMaterial3D).next_pass = _outline_mat
	parent.add_child(mi)
	return mi

func _capsule(parent: Node3D, radius: float, height: float, pos: Vector3, mat: Material, outline: bool = false) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var mesh := CapsuleMesh.new()
	mesh.radius = radius
	mesh.height = height
	# Graphics pass: 16x8 segments (~300 tris) instead of the 64x32
	# default (~3,456 tris) — the NPC body does not need hero tessellation.
	mesh.radial_segments = 16
	mesh.rings = 8
	mesh.material = mat
	mi.mesh = mesh
	mi.position = pos
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	if outline and _outline_mat:
		(mat as StandardMaterial3D).next_pass = _outline_mat
	parent.add_child(mi)
	return mi

func _sphere(parent: Node3D, radius: float, pos: Vector3, mat: Material, outline: bool = false) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var mesh := SphereMesh.new()
	mesh.radius = radius
	mesh.height = radius * 2.0
	# Graphics pass: 24x12 segments (~576 tris) instead of the 64x32
	# default (~4,224 tris) — this helper builds small NPC parts, where
	# the extra tessellation is invisible.
	mesh.radial_segments = 24
	mesh.rings = 12
	mesh.material = mat
	mi.mesh = mesh
	mi.position = pos
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	if outline and _outline_mat:
		(mat as StandardMaterial3D).next_pass = _outline_mat
	parent.add_child(mi)
	return mi

# ------------------------------------------------------------------ environment

func _build_environment() -> void:
	var env := WorldEnvironment.new()
	env.name = "WorldEnvironment"
	var e := Environment.new()
	e.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var sm := ProceduralSkyMaterial.new()
	# Graphics pass — painted gradient skybox: deeper violet-blue zenith,
	# warm peach horizon band (the old horizon was a flat pale strip), a
	# sharper sky curve so the gradient reads as painted bands, and the
	# ground horizon matched to the fog colour so the sky/ground seam
	# disappears (the dark horizon band in shots 02/10/11 was the 150 m
	# ground plane ending against a mismatched sky ground colour).
	sm.sky_top_color = Color(0.10, 0.30, 0.75, 1.0)
	sm.sky_horizon_color = Color(1.0, 0.72, 0.45, 1.0)
	sm.sky_curve = 0.09
	sm.ground_bottom_color = Color(0.16, 0.20, 0.14, 1.0)
	sm.ground_horizon_color = Color(0.72, 0.74, 0.80, 1.0)
	sm.sun_angle_max = 25.0
	sky.sky_material = sm
	e.sky = sky
	# Graphics pass — ambient source: COLOR, not SKY. Root cause found
	# by an isolated light-scale test (see /tmp/light_scale.gd): with
	# AMBIENT_SOURCE_SKY the custom light() shaders (face, cape) receive
	# a large bluish ambient term (~0.36 grey-blue on a white surface)
	# that washes them toward white — and setting ambient_light_energy
	# = 0.0 did NOT remove it, while AMBIENT_SOURCE_DISABLED made a
	# zero-diffuse test quad render black. That sky-ambient wash is what
	# kept the face pale/cream and pushed the cape toward cream even
	# after the sun+fill rebalance. A dim warm colour ambient keeps the
	# shadow sides of the village readable without the wash.
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	e.ambient_light_color = Color(0.45, 0.38, 0.30, 1.0)
	e.ambient_light_energy = 0.6
	e.fog_enabled = true
	# Graphics pass — fog retuned so the castle reads as a silhouette
	# vista: density 0.005 (the 0.010 value plus a BRIGHT WARM fog colour
	# washed the whole vista to white — shot 14's castle sampled pure
	# (255,254,220) — and the isolated cape test proved fog adds a real
	# lift even at 4 m). Fog colour is now cool grey-blue so distance
	# fades toward blue-grey (depth), not warm cream; scatter and
	# aerial perspective halved for the same reason.
	e.fog_light_color = Color(0.72, 0.76, 0.86, 1.0)
	e.fog_density = 0.005
	e.fog_sun_scatter = 0.15
	e.fog_aerial_perspective = 0.15
	# Graphics pass — post: ACES tonemap kept, gentle colour adjustments
	# (brightness 1.0, contrast 1.02, saturation 1.05), and NO glow.
	# The Environment glow was measured, not assumed: an isolated
	# cape-shader test showed glow 0.35 -> 0.15 -> 0.05 still washing the
	# hero toward cream (quad A went (255,244,190) -> (255,219,170) vs
	# (255,166,132) with glow off — the bloom feeds the hero's own >1.0
	# red channel back onto itself). On this gl_compatibility backend
	# there is no glow intensity that both shows and stays subtle, so it
	# is OFF and the bloom impression comes from the emissive floors
	# (face/cape/plate) — the same rule the VFX department states
	# ("glow is faked with emissive, never real bloom on the phone").
	# Godot 4.3 Environment has NO vignette property (verified against
	# the 4.3 docs and the live property list), so the vignette is a
	# radial-gradient TextureRect overlay — see _build_vignette().
	e.tonemap_mode = Environment.TONE_MAPPER_ACES
	e.tonemap_exposure = 1.0
	e.tonemap_white = 1.0
	e.glow_enabled = false
	# MSAA/SSAO patch (2026-11-15): SSAO on the slice Environment — the
	# project.godot ssao lines are only defaults for new Environments.
	e.ssao_enabled = true
	e.ssao_light_affect = 0.5
	e.adjustment_enabled = true
	e.adjustment_brightness = 1.0
	e.adjustment_contrast = 1.02
	e.adjustment_saturation = 1.05
	env.environment = e
	add_child(env)
	var sun := DirectionalLight3D.new()
	sun.name = "Sun"
	# Graphics pass: sun swung round toward the south (yaw -15, was -28)
	# and lowered (pitch -45, was -52) so it keys the hero's FRONT
	# (chest faces +Z) instead of raking across from the west, and its
	# energy dropped 0.85 -> 0.70 as part of the light-budget rebalance
	# (sun + fill must stay <= ~1.0 x the face light_cap, or the skin
	# clips pale again — see anime_face.gdshader).
	sun.rotation_degrees = Vector3(-45, -15, 0)
	sun.light_energy = 0.70
	sun.light_color = Color(1.0, 0.92, 0.78, 1.0)
	sun.shadow_enabled = true
	# Graphics pass — shadow cost: the default PSSM_4_SPLITS renders the
	# scene up to 4 extra times into the shadow map, which is what pushed
	# the live frame to 619 draw calls / 356k primitives (see the
	# [AETHERIA-BUDGET] print: scene total is only ~92k tris). One
	# orthogonal split renders shadows once; at 1024 px over 90 m the
	# texel is ~9 cm, fine for a toon style, and it roughly halves the
	# frame's draw calls.
	# 90 m -> 60 m: the castle and towers (78 m out) are fog silhouettes
	# whose shadows fall on fog-faded ground — invisible in practice —
	# and culling them from the shadow pass saves ~9k shadow primitives.
	# Everything the player can walk to stays inside 60 m.
	sun.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
	sun.directional_shadow_max_distance = 60.0
	add_child(sun)
	# Pass 2 front fill: the sun comes from the south-west-above, but the
	# hero's chest plate still fell into the darkest toon band (the
	# red/gold tabard was lost). A shadowless warm fill from the front
	# (camera side) key-lights the hero's front without a second shadow map.
	# Graphics pass: fill energy 0.45 -> 0.30 — sun (0.70) + fill (0.30)
	# = 1.00 total, so with the face light_cap at 0.70 the face can no
	# longer clip past 1.0.
	var fill := DirectionalLight3D.new()
	fill.name = "Fill"
	fill.rotation_degrees = Vector3(-30, 0, 0)
	fill.light_energy = 0.30
	fill.light_color = Color(1.0, 0.88, 0.72, 1.0)
	fill.shadow_enabled = false
	add_child(fill)

func _build_ground() -> void:
	var ground := MeshInstance3D.new()
	ground.name = "Ground"
	# Graphics pass: ground plane 150 m -> 400 m. The old plane ENDED at
	# z = -75 while the castle stands at z = -78 — the visible dark band
	# at the horizon in shots 02/10/11 was the plane's edge. At 400 m the
	# edge sits at 86% fog (density 0.010), i.e. invisible, and the new
	# horizon hills (see _build_horizon) cover it from every vista angle.
	# Grass muted (0.30,0.56,0.22 -> 0.26,0.48,0.20): the old green read
	# neon-lime under the new sky.
	var pm := PlaneMesh.new()
	pm.size = Vector2(400, 400)
	pm.material = _toon(Color(0.26, 0.48, 0.20, 1.0))
	ground.mesh = pm
	ground.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	ground.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(ground)
	var body := StaticBody3D.new()
	body.name = "GroundBody"
	var cs := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(400, 1, 400)
	cs.shape = shape
	cs.position = Vector3(0, -0.5, 0)
	body.add_child(cs)
	add_child(body)
	# Cobble street (runs north toward the castle).
	var street := MeshInstance3D.new()
	street.name = "Street"
	var spm := PlaneMesh.new()
	spm.size = Vector2(7, 58)
	spm.material = _toon(Color(0.42, 0.36, 0.28, 1.0))
	street.mesh = spm
	street.position = Vector3(0, 0.02, -14)
	street.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	street.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(street)
	# Stone plaza where the market stands.
	var plaza := MeshInstance3D.new()
	plaza.name = "Plaza"
	var ppm := PlaneMesh.new()
	ppm.size = Vector2(18, 12)
	# Graphics pass: albedo 0.55 -> 0.44 — the pale stone read as a
	# near-white slab in the vista (sampled (246,233,216)); the render
	# runs ~1.4x brighter than the albedo x light model on toon
	# surfaces, so the albedo has to absorb it.
	ppm.material = _toon(Color(0.44, 0.40, 0.33, 1.0))
	plaza.mesh = ppm
	plaza.position = Vector3(0, 0.03, -10)
	plaza.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	plaza.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(plaza)

# ------------------------------------------------------------------ village

func _place(scene_path: String, pos: Vector3, rot_y_deg: float, scale: float = 1.0, static_gi: bool = true, cast_shadow: bool = true) -> Node3D:
	var ps: PackedScene = load(scene_path) as PackedScene
	if ps == null:
		push_warning("AetheriaSlice: failed to load " + scene_path)
		return null
	var node: Node3D = ps.instantiate() as Node3D
	node.position = pos
	node.rotation.y = deg_to_rad(rot_y_deg)
	node.scale = Vector3.ONE * scale
	add_child(node)
	# Graphics pass: static set dressing is marked GI_MODE_STATIC so the
	# LightmapGI bake (see _build_lightmap_gi) can light it; the default
	# is DYNAMIC, which the baker skips.
	if static_gi:
		for mi: MeshInstance3D in node.find_children("*", "MeshInstance3D", true, false):
			mi.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	# Graphics pass — budget: small props cast no shadow (cast_shadow
	# = false). Every shadow caster is drawn a second time into the
	# shadow map, and the shadow pass is what pushed the frame to 325
	# draw calls; a crate's shadow is invisible at this scale, a
	# house's is not. Buildings / tents / trees keep their shadows.
	if not cast_shadow:
		for mi: MeshInstance3D in node.find_children("*", "MeshInstance3D", true, false):
			mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return node

# ------------------------------------------------------------------ collision

func _add_building_collider(node: Node3D) -> void:
	# One StaticBody3D + BoxShape3D per building, sized from the real
	# mesh AABB in the building's local space (so it follows the node's
	# rotation/scale) and shrunk 8% horizontally so the box hugs the
	# walls instead of the roof eaves. Height is floored at 2 m so a
	# low cottage still blocks the 1.7 m hero capsule. Default layer 1
	# = the player's collision layer/mask, so move_and_slide stops.
	if node == null:
		return
	var aabb: AABB = _collect_mesh_aabb(node, Transform3D.IDENTITY)
	if aabb.size == Vector3.ZERO:
		push_warning("AetheriaSlice: no mesh AABB for collider on " + str(node.name))
		return
	var size := aabb.size * Vector3(0.92, 1.0, 0.92)
	size.y = maxf(size.y, 2.0)
	var body := StaticBody3D.new()
	body.name = "BuildingCollider"
	var cs := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = size
	cs.shape = shape
	cs.position = aabb.get_center()
	body.add_child(cs)
	node.add_child(body)
	_building_colliders += 1
	print("[AETHERIA-COLLISION] ", node.name, " collider size=", size, " centre=", aabb.get_center())


func _collect_mesh_aabb(node: Node3D, parent_xf: Transform3D) -> AABB:
	# Recursive walk: accumulates every MeshInstance3D's AABB through
	# the local transform chain, so no global-transform read is needed
	# during _ready (transforms are not settled yet at build time).
	var combined := AABB()
	var first := true
	for child: Node in node.get_children():
		var child3d := child as Node3D
		if child3d == null:
			continue
		var xf: Transform3D = parent_xf * child3d.transform
		var mi := child3d as MeshInstance3D
		if mi != null and mi.mesh != null:
			var a: AABB = xf * mi.mesh.get_aabb()
			if first:
				combined = a
				first = false
			else:
				combined = combined.merge(a)
		var sub: AABB = _collect_mesh_aabb(child3d, xf)
		if sub.size != Vector3.ZERO:
			if first:
				combined = sub
				first = false
			else:
				combined = combined.merge(sub)
	return combined


func _build_village() -> void:
	# Houses line both sides of the street, doors facing it.
	# Every building gets a StaticBody3D box collider matching its
	# mesh footprint (see _add_building_collider) so the hero can no
	# longer walk through walls — verified by -- --collision-test.
	_add_building_collider(_place(MED + "building_home_A_green.gltf", Vector3(-7.2, 0, 2), 90, 1.6))
	_add_building_collider(_place(MED + "building_home_B_green.gltf", Vector3(7.2, 0, 4), -90, 1.6))
	_add_building_collider(_place(MED + "building_tavern_green.gltf", Vector3(-7.6, 0, -8), 90, 1.6))
	_add_building_collider(_place(MED + "building_market_green.gltf", Vector3(7.6, 0, -10), -90, 1.6))
	_add_building_collider(_place(MED + "building_home_A_green.gltf", Vector3(-7.2, 0, -18), 90, 1.6))
	_add_building_collider(_place(MED + "building_church_green.gltf", Vector3(7.6, 0, -22), -90, 1.6))
	_add_building_collider(_place(MED + "building_blacksmith_green.gltf", Vector3(-7.6, 0, -28), 90, 1.6))
	_add_building_collider(_place(MED + "building_windmill_green.gltf", Vector3(12, 0, -34), -30, 1.6))
	_add_building_collider(_place(MED + "building_well_green.gltf", Vector3(4.5, 0, -4), 0))
	print("[AETHERIA-COLLISION] building colliders: ", _building_colliders)
	# Market props: crates, sacks, tent, flags, barrels.
	# Graphics pass: small props cast no shadow (see _place) — the tent
	# keeps its shadow, the rest are too small for it to read.
	_place(PROPS + "crate_B_big.gltf", Vector3(6.2, 0, -7.5), 20, 1.0, true, false)
	_place(PROPS + "crate_A_small.gltf", Vector3(6.8, 0, -8.6), -15, 1.0, true, false)
	_place(PROPS + "sack.gltf", Vector3(5.6, 0, -9.2), 40, 1.0, true, false)
	_place(PROPS + "tent.gltf", Vector3(-6.0, 0, -12.5), 90)
	_place(PROPS + "weaponrack.gltf", Vector3(-6.8, 0, -26), 90, 1.0, true, false)
	_place(PROPS + "crate_long_A.gltf", Vector3(-6.4, 0, -25), 0, 1.0, true, false)
	_place(PROPS + "flag_red.gltf", Vector3(-8.2, 0, -1), 0, 1.0, true, false)
	_place(PROPS + "flag_green.gltf", Vector3(8.2, 0, 1), 0, 1.0, true, false)
	_place(PROPS + "wheelbarrow.gltf", Vector3(5.8, 0, -14), -40, 1.0, true, false)
	# Kenney trees + flowers frame the street. Collected as transforms
	# and drawn as two MultiMeshes (see _build_multimeshes): 19 separate
	# tree draws + 10 flower draws become 6.
	var tree_spots: Array[Vector3] = [
		Vector3(-14, 0, -2), Vector3(14, 0, -14), Vector3(-13, 0, -30),
		Vector3(13, 0, 8), Vector3(-15, 0, 10), Vector3(15, 0, -26),
		Vector3(-12, 0, -38), Vector3(12, 0, -40), Vector3(-16, 0, -18),
	]
	for i: int in range(tree_spots.size()):
		_tree_near_xf.append(_xf(tree_spots[i], float(i * 37), 1.4 + float(i % 3) * 0.3))
	var flower_spots: Array[Vector3] = [
		Vector3(3.9, 0, 6), Vector3(-3.9, 0, 0), Vector3(3.9, 0, -16),
		Vector3(-3.9, 0, -24), Vector3(3.9, 0, -30), Vector3(-3.9, 0, 12),
	]
	for i: int in range(flower_spots.size()):
		_flower_xf.append(_xf(flower_spots[i], float(i * 61), 1.0))

func _build_plaza_density() -> void:
	# Graphics pass — the plaza foreground (z = 0..10, around the hero at
	# z = 8) was wide empty street in every v1 shot. Fill it with a second
	# market stall + goods on both sides, kept OFF the street centre
	# (x in [-3.5, 3.5] stays clear for the hero and the camera) and off
	# the hero's own spot. All kit props (KayKit CC0), ~16 placements.
	# West stall: second tent + lumber/pallet goods.
	_place(PROPS + "tent.gltf", Vector3(-6.0, 0, 5.5), -90)
	_place(PROPS + "pallet.gltf", Vector3(-6.6, 0, 2.5), 30, 1.0, true, false)
	_place(PROPS + "resource_lumber.gltf", Vector3(-6.8, 0, 3.8), 10, 1.0, true, false)
	_place(PROPS + "crate_long_B.gltf", Vector3(-6.4, 0, 1.2), 0, 1.0, true, false)
	_place(PROPS + "bucket_empty.gltf", Vector3(-4.2, 0, 4.5), 0, 1.0, true, false)
	# East stall: crates, sacks, barrels, water bucket.
	_place(PROPS + "crate_B_big.gltf", Vector3(6.2, 0, 5.0), 15, 1.0, true, false)
	_place(PROPS + "crate_A_small.gltf", Vector3(6.9, 0, 6.2), -20, 1.0, true, false)
	_place(PROPS + "sack.gltf", Vector3(5.7, 0, 6.4), 60, 1.0, true, false)
	_place(PROPS + "barrel.gltf", Vector3(6.5, 0, 3.6), 0, 1.0, true, false)
	_place(PROPS + "bucket_water.gltf", Vector3(4.2, 0, 2.0), 0, 1.0, true, false)
	# Archery target by the east house + two more flags.
	_place(PROPS + "target.gltf", Vector3(7.5, 0, -1.5), -90, 1.0, true, false)
	_place(PROPS + "flag_yellow.gltf", Vector3(-8.2, 0, 7), 0, 1.0, true, false)
	_place(PROPS + "flag_blue.gltf", Vector3(8.2, 0, -3), 0, 1.0, true, false)
	# Foreground flowers lining the street + two framing trees.
	for i: int in range(4):
		var spots: Array[Vector3] = [
			Vector3(3.9, 0, 2), Vector3(-3.9, 0, 4.5),
			Vector3(3.9, 0, 9.5), Vector3(-3.9, 0, -3),
		]
		_flower_xf.append(_xf(spots[i], float(i * 47), 1.0))
	for i: int in range(2):
		var tree_spots: Array[Vector3] = [Vector3(-14, 0, 6), Vector3(14, 0, 2)]
		_tree_near_xf.append(_xf(tree_spots[i], float(120 + i * 61), 1.5))

# ------------------------------------------------------------------ vista

func _tint_tree(tree: Node3D, tint: Color = Color(0.22, 0.50, 0.24, 1.0)) -> void:
	# Kenney tree_cone is ONE mesh (trunk + foliage share the cyan-ish
	# texture); a flat green toon override keeps the stylised pine shape
	# and reads as a tree under this sky.
	if tree == null:
		return
	var green := _toon(tint)
	for child: Node in tree.find_children("*", "MeshInstance3D", true, false):
		var mi := child as MeshInstance3D
		if mi != null:
			mi.material_override = green

func _build_horizon() -> void:
	# Graphics pass — horizon depth layers that hide the ground-plane
	# edge from every vista angle (the 400 m plane ends at 86% fog, and
	# these silhouettes sit in front of that edge):
	#   1. a ridge of flattened dark hills behind the castle (z = -100),
	#      plus two flank hills, all fog-faded;
	#   2. a darker tree line flanking the road to the castle, for depth
	#      between the village (z = -30) and the castle (z = -78).
	# All static (baked GI) and cheap: 7 spheres + 8 reused Kenney trees.
	var hill_mat := _toon(Color(0.16, 0.30, 0.22, 1.0))
	var hill_spots: Array[Vector3] = [
		Vector3(-60, -2.0, -100), Vector3(-30, -2.5, -102),
		Vector3(0, -2.0, -104), Vector3(30, -2.5, -102),
		Vector3(60, -2.0, -100), Vector3(-95, -2.0, -45),
		Vector3(95, -2.0, -45),
	]
	for i: int in range(hill_spots.size()):
		var hill := _sphere(self, 30.0, hill_spots[i], hill_mat)
		hill.scale = Vector3(1.6, 0.35, 1.0)
		hill.gi_mode = GeometryInstance3D.GI_MODE_STATIC
		# Low-poly dome: the default SphereMesh is 64x32 segments
		# (~4,224 tris) — 7 hills would cost ~30k tris for background
		# silhouettes. 16x8 is ~256 tris each and reads identically
		# through the fog.
		var hill_mesh := hill.mesh as SphereMesh
		hill_mesh.radial_segments = 16
		hill_mesh.rings = 8
	var far_tree_spots: Array[Vector3] = [
		Vector3(-11, 0, -48), Vector3(11, 0, -52), Vector3(-13, 0, -60),
		Vector3(13, 0, -64), Vector3(-10, 0, -68), Vector3(10, 0, -70),
		Vector3(-16, 0, -44), Vector3(16, 0, -46),
	]
	for i: int in range(far_tree_spots.size()):
		_tree_far_xf.append(_xf(far_tree_spots[i], float(i * 53), 1.8 + float(i % 3) * 0.3))

# Graphics pass — MultiMesh vegetation. The builders above only COLLECT
# transforms; this builds one MultiMeshInstance3D per group at the end
# of _ready. 19 trees + 10 flowers were 29 MeshInstances (2 surfaces
# each = 58 main-pass draws + 58 shadow-pass draws); now they are 3
# MultiMeshes = 6 main draws + 4 shadow draws (far trees cast none).
var _tree_near_xf: Array[Transform3D] = []
var _tree_far_xf: Array[Transform3D] = []
var _flower_xf: Array[Transform3D] = []

func _xf(pos: Vector3, rot_y_deg: float, scale: float) -> Transform3D:
	var b := Basis(Vector3.UP, deg_to_rad(rot_y_deg)).scaled(Vector3.ONE * scale)
	return Transform3D(b, pos)

func _kit_mesh(scene_path: String) -> Mesh:
	var ps: PackedScene = load(scene_path) as PackedScene
	if ps == null:
		return null
	var tmp: Node = ps.instantiate()
	for mi in tmp.find_children("*", "MeshInstance3D", true, false):
		var mesh: Mesh = (mi as MeshInstance3D).mesh
		tmp.free()
		return mesh
	tmp.free()
	return null

func _build_multimeshes() -> void:
	# Wind sway (deep-graphics integration 2026-11-15): the near trees
	# use the showcase wind shader (same green as the old _toon, so the
	# look is unchanged except for the motion). The far trees keep _toon
	# (fog silhouettes — sway would not read). The wind ShaderMaterial
	# cannot carry next_pass, so the near trees lose their black outline
	# (check shots 43a/43b); the flowers keep their own colours and get
	# no wind (the shader's flat colour would erase them).
	var wind_mat := ShaderMaterial.new()
	wind_mat.shader = load(WIND_SHADER) as Shader
	wind_mat.set_shader_parameter("color", Color(0.22, 0.50, 0.24, 1.0))
	wind_mat.set_shader_parameter("sway_height", 2.6)
	wind_mat.set_shader_parameter("use_alpha", 0)
	_build_one_multimesh(TREE_SCENE, _tree_near_xf, wind_mat, true)
	_build_one_multimesh(TREE_SCENE, _tree_far_xf, _toon(Color(0.16, 0.38, 0.20, 1.0)), false)
	_build_one_multimesh(FLOWER_SCENE, _flower_xf, null, false)

func _build_one_multimesh(scene_path: String, xfs: Array[Transform3D], override_mat: Material, cast_shadow: bool) -> void:
	if xfs.is_empty():
		return
	var mesh: Mesh = _kit_mesh(scene_path)
	if mesh == null:
		push_warning("AetheriaSlice: no mesh in " + scene_path)
		return
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.mesh = mesh
	mm.instance_count = xfs.size()
	for i: int in range(xfs.size()):
		mm.set_instance_transform(i, xfs[i])
	var mmi := MultiMeshInstance3D.new()
	mmi.multimesh = mm
	if override_mat != null:
		mmi.material_override = override_mat
	mmi.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	if not cast_shadow:
		mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mmi)

# ------------------------------------------------------------------ deep graphics (slice integration 2026-11-15)

func _splat_material(texture_scale: float = 0.3) -> ShaderMaterial:
	# Triplanar splat material (showcase SplatMat): ambientCG grass /
	# dirt / stone PBR sets, no UVs needed — works on the terrain patch
	# AND on the TripoSG rock (which has no UVs). The dirt weights are
	# the tuned defaults in terrain_splat.gdshader (grass dominates the
	# flat top since 2026-11-15).
	var m := ShaderMaterial.new()
	m.shader = load(SPLAT_SHADER) as Shader
	m.set_shader_parameter("grass_albedo", load(PBR + "grass_ground/albedo.jpg") as Texture2D)
	m.set_shader_parameter("grass_normal", load(PBR + "grass_ground/normal.jpg") as Texture2D)
	m.set_shader_parameter("grass_rough", load(PBR + "grass_ground/roughness.jpg") as Texture2D)
	m.set_shader_parameter("dirt_albedo", load(PBR + "dirt_path/albedo.jpg") as Texture2D)
	m.set_shader_parameter("dirt_normal", load(PBR + "dirt_path/normal.jpg") as Texture2D)
	m.set_shader_parameter("dirt_rough", load(PBR + "dirt_path/roughness.jpg") as Texture2D)
	m.set_shader_parameter("stone_albedo", load(PBR + "stone_wall/albedo.jpg") as Texture2D)
	m.set_shader_parameter("stone_normal", load(PBR + "stone_wall/normal.jpg") as Texture2D)
	m.set_shader_parameter("stone_rough", load(PBR + "stone_wall/roughness.jpg") as Texture2D)
	m.set_shader_parameter("texture_scale", texture_scale)
	# Set the tuned blend bands EXPLICITLY (not just as shader-file
	# defaults): a -s game run does not reliably pick up edited
	# .gdshader defaults without a re-import (see water_stylized's
	# header lesson), and these values are the slice's verified tuning
	# — grass dominates the flat top (dirt 0.25-0.60, low-dirt 0.25),
	# stone only on the very steepest faces (0.70-0.90).
	m.set_shader_parameter("dirt_slope_start", 0.25)
	m.set_shader_parameter("dirt_slope_end", 0.60)
	m.set_shader_parameter("stone_slope_start", 0.70)
	m.set_shader_parameter("stone_slope_end", 0.90)
	return m

func _mesh_with_fixed_normals(src: Mesh) -> Mesh:
	# Recomputes smooth vertex normals from the triangles. Two shipped
	# assets need it:
	#   * scenes/tests/terrain_patch.mesh ships with INVERTED normals
	#     (mean (0,-0.91,-0.05) — probed 2026-11-15). The splat shader
	#     then reads slope = 1 on every face, so dirt+stone win
	#     everywhere and the hill renders as a dirt mound. The "dirt too
	#     strong" in showcase shot 17 was this, not the dirt weights
	#     (the 2026-11-15 weight tuning alone could not fix it).
	#   * the TripoSG rock GLB has NO normals at all (and no UVs), so
	#     its lighting and its splat slope are undefined — the small
	#     rock rendered near-black brown in shot 40.
	# The winding is trusted but verified: if the recomputed mean normal
	# points down (mean y < -0.1, the heightfield case) the normals are
	# negated; if the mean is near zero (a closed mesh like the rock)
	# the outward test decides (majority pointing at the centroid =
	# inverted). Returns a NEW ArrayMesh; the source is untouched (the
	# shared terrain_patch.mesh file still carries the inverted
	# normals — that file is a separate asset fix).
	if src == null or src.get_surface_count() == 0:
		return src
	var arrays: Array = src.surface_get_arrays(0)
	var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	if verts.is_empty():
		return src
	var index: PackedInt32Array = arrays[Mesh.ARRAY_INDEX]
	var normals := PackedVector3Array()
	normals.resize(verts.size())
	var tri_count: int = verts.size() / 3
	if not index.is_empty():
		tri_count = index.size() / 3
	for t in range(tri_count):
		var ia: int = t * 3
		var ib: int = t * 3 + 1
		var ic: int = t * 3 + 2
		if not index.is_empty():
			ia = index[t * 3]
			ib = index[t * 3 + 1]
			ic = index[t * 3 + 2]
		var fn: Vector3 = (verts[ib] - verts[ia]).cross(verts[ic] - verts[ia])
		if fn.length_squared() < 0.00000001:
			continue
		normals[ia] += fn
		normals[ib] += fn
		normals[ic] += fn
	var mean := Vector3.ZERO
	for n in normals:
		mean += n
	mean /= max(normals.size(), 1)
	var centroid := Vector3.ZERO
	for v in verts:
		centroid += v
	centroid /= max(verts.size(), 1)
	var outward: int = 0
	var inward: int = 0
	for i in range(normals.size()):
		var n: Vector3 = normals[i]
		if n.length_squared() < 0.00000001:
			continue
		if n.dot(verts[i] - centroid) > 0.0:
			outward += 1
		else:
			inward += 1
	var flip: bool = false
	# NOTE: use the NORMALIZED mean here, not the raw sum. The raw sum's
	# magnitude scales with face area (the terrain patch's faces are
	# ~0.125 m, so its raw mean.y is only 0.09 even though it points
	# straight up) — a +/-0.1 threshold on the raw sum misreads it and
	# falls through to the outward test, which wrongly flips a correct
	# heightfield (its base vertices point at the centroid). The
	# normalized mean is unambiguous: |y| ~ 1 for a heightfield, ~0 for
	# a closed mesh (where the outward test is the right decider).
	var mean_n: Vector3 = Vector3.ZERO
	if mean.length_squared() > 0.00000001:
		mean_n = mean.normalized()
	if mean_n.y < -0.5:
		flip = true
	elif mean_n.y > 0.5:
		flip = false
	else:
		flip = inward > outward
	for i in range(normals.size()):
		var n: Vector3 = normals[i]
		if n.length_squared() < 0.00000001:
			normals[i] = Vector3.UP
		elif flip:
			normals[i] = -n.normalized()
		else:
			normals[i] = n.normalized()
	var out_arrays: Array = arrays.duplicate()
	out_arrays[Mesh.ARRAY_NORMAL] = normals
	# Tangents (if any) were built from the old normals — drop them
	# rather than keep stale ones; the splat shader does not use them.
	out_arrays[Mesh.ARRAY_TANGENT] = null
	var fixed := ArrayMesh.new()
	fixed.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, out_arrays)
	return fixed

func _build_terrain_patch() -> void:
	# (a) Terrain splat on a village ground patch: the showcase's
	# 12x12 m hill mesh at (22, 0, -12), east open ground — clear of the
	# near tree at (14, -14) by 2 m and of the windmill (12, -34).
	# The hill's base ring sits at y ~ -0.17, so it emerges from the
	# ground plane with no gap and no z-fight.
	var patch := MeshInstance3D.new()
	patch.name = "TerrainPatch"
	patch.mesh = _mesh_with_fixed_normals(load(TERRAIN_PATCH_MESH) as Mesh)
	patch.material_override = _splat_material()
	patch.position = Vector3(22, 0, -12)
	patch.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	add_child(patch)

# _build_cloud_shadows() REMOVED 2026-11-15 — the cloud-shadow sheet
# does NOT survive the move from the showcase to the main slice:
#  (1) it never darkens the ground here: the 42a/42b high pair (3 s
#      apart, camera above the sheet) has IDENTICAL ground luminance
#      grids, and a Python replication of the shader's value noise
#      shows clouds SHOULD cover the east band (cover > 0.3 at
#      x 16..24) yet that ground is not darkened at all;
#  (2) it bands the sky as dark blotches from every low camera (shots
#      39, 41, 43a) — a visible regression, and the edge fade only hides
#      the sheet's borders, not its interior clouds.
# The showcase's own note predicted the low-camera half of this
# ("prove it from the high camera only"); the slice's fog wash means
# even the high camera shows no ground shadows. The shader file
# (cloud_shadow.gdshader, with the UV edge fade) is kept for the
# showcase. A cloud technique that works here needs a projection-based
# approach (light-space or screen-space), not a physical sheet.

func _build_pond() -> void:
	# (e) Pond + reflection probe: there was NO pond in the slice, so one
	# is added on the east open ground at (24, 0, 6) — clear of the near
	# trees at x <= 16 and of the terrain patch (z -18..-6). Same pattern
	# as the showcase: 7x7 water plane (32x32 subdiv for the waves) at
	# y = 0.06, dirt basin cylinder below, probe above. The slice ground
	# is a solid 400 m plane (no hole), so the basin's top disc (radius
	# 5, y = 0.02) reads as a dirt shore ring around the water instead
	# of a dug basin. use_depth_fade stays 0 (unresolved lavapipe
	# paradox — needs the Galaxy A16 test). The water sun direction is
	# the slice's own sun: rotation (-45, -15, 0) -> to-sun
	# (-0.183, 0.707, 0.683), NOT the showcase's (-0.574, 0.346, 0.742).
	var water := MeshInstance3D.new()
	water.name = "PondWater"
	var wplane := PlaneMesh.new()
	wplane.size = Vector2(7, 7)
	wplane.subdivide_width = 32
	wplane.subdivide_depth = 32
	water.mesh = wplane
	var wmat := ShaderMaterial.new()
	wmat.shader = load(WATER_SHADER) as Shader
	wmat.set_shader_parameter("sun_direction", Vector3(-0.183, 0.707, 0.683))
	wmat.set_shader_parameter("use_depth_fade", 0)
	water.material_override = wmat
	water.position = Vector3(24, 0.06, 6)
	water.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(water)
	var basin := MeshInstance3D.new()
	basin.name = "PondBasin"
	var cyl := CylinderMesh.new()
	cyl.top_radius = 5.0
	cyl.bottom_radius = 3.0
	cyl.height = 0.7
	basin.mesh = cyl
	var bmat := StandardMaterial3D.new()
	bmat.albedo_texture = load(PBR + "dirt_path/albedo.jpg") as Texture2D
	bmat.normal_texture = load(PBR + "dirt_path/normal.jpg") as Texture2D
	bmat.roughness_texture = load(PBR + "dirt_path/roughness.jpg") as Texture2D
	bmat.uv1_scale = Vector3(2, 2, 1)
	bmat.roughness = 1.0
	bmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	basin.material_override = bmat
	basin.position = Vector3(24, -0.33, 6)
	basin.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	basin.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	add_child(basin)
	var probe := ReflectionProbe.new()
	probe.name = "ProbePond"
	probe.position = Vector3(24, 1.2, 6)
	probe.size = Vector3(12, 6, 12)
	probe.update_mode = ReflectionProbe.UPDATE_ONCE
	add_child(probe)

func _build_rock_clearing() -> void:
	# (step 4) TripoSG mossy rock in the golem-fight clearing, west of
	# the village at (-24, 0, -56) — the dialogue says the golem lives in
	# the forest clearing BEHIND the village. The GLB is ALREADY Y-up
	# (a low wide boulder, Y extent smallest — probed 2026-11-15), so it
	# is placed UPRIGHT: the task's Y-up -> Z-up rotation would lay it
	# on its side. The mesh's local origin is 0.357 m above its base, so
	# each rock is lifted by 0.357 * scale to sit on the ground.
	# Material: the triplanar splat shader (no UVs needed) — grass reads
	# as moss on the flat top, stone on the steep faces, dirt at the
	# base; texture_scale 0.8 for finer detail on a ~2 m rock.
	var rock_mesh: Mesh = _mesh_with_fixed_normals(_kit_mesh(MOSSY_ROCK_SCENE))
	if rock_mesh == null:
		push_warning("AetheriaSlice: mossy rock mesh not found")
		return
	var rock_mat := _splat_material(0.8)
	var spots: Array = [
		[Vector3(-24, 0.464, -56), 1.3, 0.0],
		[Vector3(-21.5, 0.25, -53.5), 0.7, 1.2],
	]
	for s in spots:
		var rock := MeshInstance3D.new()
		rock.name = "MossyRock"
		rock.mesh = rock_mesh
		rock.material_override = rock_mat
		rock.position = s[0] as Vector3
		rock.rotation.y = float(s[2])
		rock.scale = Vector3.ONE * float(s[1])
		rock.gi_mode = GeometryInstance3D.GI_MODE_STATIC
		add_child(rock)

func _build_lut_grade() -> void:
	# (d) Mobile LUT grade: the showcase's Hald-CLUT grade as a
	# full-screen ColorRect on its own CanvasLayer (layer 0, added after
	# the vignette so it grades the whole frame including the vignette).
	# It is VISIBLE ONLY on the Vulkan driver (the LUT renders BLACK on
	# Compatibility — proven in the showcase): the driver is detected by
	# get_video_adapter_api_version() starting with "1." (Vulkan) vs
	# "4." (OpenGL/Compatibility). `--aetheria-no-lut` forces it off so
	# the Mobile on/off pair can be captured in two runs.
	var is_vulkan: bool = RenderingServer.get_video_adapter_api_version().begins_with("1.")
	var force_off: bool = "--aetheria-no-lut" in OS.get_cmdline_user_args()
	var layer := CanvasLayer.new()
	layer.name = "LUTGrade"
	layer.layer = 0
	layer.visible = is_vulkan and not force_off
	var rect := ColorRect.new()
	rect.name = "LUTRect"
	rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	var lut_mat := ShaderMaterial.new()
	lut_mat.shader = load(LUT_SHADER) as Shader
	lut_mat.set_shader_parameter("lut_tex", load(LUT_TEX) as Texture2D)
	lut_mat.set_shader_parameter("strength", 1.0)
	rect.material = lut_mat
	layer.add_child(rect)
	add_child(layer)

func _build_vista() -> void:
	# Distant castle silhouette, fog-faded on the northern hill.
	_place(MED + "building_castle_green.gltf", Vector3(0, 0, -78), 0, 2.4)
	_place(MED + "building_tower_A_green.gltf", Vector3(-16, 0, -72), 0, 1.9)
	_place(MED + "building_tower_B_green.gltf", Vector3(16, 0, -72), 0, 1.9)
	_island_a = _build_floating_island(Vector3(21, 15, -48), 2.6)
	_island_b = _build_floating_island(Vector3(-25, 18, -62), 1.7)

func _build_floating_island(pos: Vector3, island_scale: float) -> Node3D:
	var island := Node3D.new()
	island.name = "FloatingIsland"
	island.position = pos
	add_child(island)
	# The rock block sits flat-side up, its top face touching the grass disc
	# (flipping it left a visible gap and read as a floating cube).
	# No shadow: the islands hang in the sky, their shadows would fall
	# far from any readable surface and cost a shadow-pass draw each.
	var rock: Node3D = _place_in(island, ROCK_SCENE, Vector3(0, 0, 0), 0, island_scale * 1.4, true, false)
	if rock:
		rock.position.y = -0.55 * island_scale
	var top := MeshInstance3D.new()
	var cyl := CylinderMesh.new()
	cyl.top_radius = 1.3 * island_scale
	cyl.bottom_radius = 0.9 * island_scale
	cyl.height = 0.5
	cyl.material = _toon(Color(0.30, 0.56, 0.22, 1.0))
	top.mesh = cyl
	top.position = Vector3(0, 0.5 * island_scale, 0)
	top.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	top.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	island.add_child(top)
	var tree: Node3D = _place_in(island, TREE_SCENE, Vector3(0.5, 0.8 * island_scale, 0.3), 0, 0.9 * island_scale, true, false)
	if tree:
		tree.position.y = 0.8 * island_scale
		_tint_tree(tree)
	return island

func _place_in(parent: Node3D, scene_path: String, pos: Vector3, rot_y_deg: float, scale: float = 1.0, static_gi: bool = true, cast_shadow: bool = true) -> Node3D:
	var ps: PackedScene = load(scene_path) as PackedScene
	if ps == null:
		push_warning("AetheriaSlice: failed to load " + scene_path)
		return null
	var node: Node3D = ps.instantiate() as Node3D
	node.position = pos
	node.rotation.y = deg_to_rad(rot_y_deg)
	node.scale = Vector3.ONE * scale
	parent.add_child(node)
	# Pass static_gi=false for anything parented to the moving hero
	# (e.g. the shield): baked lighting must not freeze to its spawn pose.
	if static_gi:
		for mi: MeshInstance3D in node.find_children("*", "MeshInstance3D", true, false):
			mi.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	if not cast_shadow:
		for mi: MeshInstance3D in node.find_children("*", "MeshInstance3D", true, false):
			mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return node

func _build_vignette() -> void:
	# Graphics pass — light vignette. Godot 4.3 Environment has no
	# vignette property, so this is a radial-gradient overlay: fully
	# transparent in the centre, up to 0.32 black at the corners. One
	# 256x256 texture generated once at startup, one TextureRect, no
	# per-frame cost; CanvasLayer layer 0 so it sits above the 3D view
	# but below the HUD (layer 1).
	var size := 256
	var img := Image.create(size, size, false, Image.FORMAT_RGBA8)
	var center := Vector2(size * 0.5, size * 0.5)
	var max_d: float = center.length()
	for y: int in range(size):
		for x: int in range(size):
			var d: float = Vector2(x + 0.5, y + 0.5).distance_to(center) / max_d
			var a: float = clamp((d - 0.55) / 0.45, 0.0, 1.0)
			a = a * a * 0.32
			img.set_pixel(x, y, Color(0, 0, 0, a))
	var layer := CanvasLayer.new()
	layer.name = "VignetteLayer"
	layer.layer = 0
	var rect := TextureRect.new()
	rect.texture = ImageTexture.create_from_image(img)
	rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	rect.stretch_mode = TextureRect.STRETCH_SCALE
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(rect)
	add_child(layer)

func _build_lightmap_gi() -> void:
	# Graphics pass — LightmapGI node, staged for the bake.
	# Config: medium quality (mobile-sized lightmaps), 2 bounces,
	# directional lightmaps (the toon materials respond to light
	# direction), light probes ON so the dynamic hero picks up baked
	# bounce. Static set dressing is marked GI_MODE_STATIC in _place /
	# _place_in / _build_ground / _build_horizon; the hero, NPC and
	# shield stay DYNAMIC.
	# HONEST LIMIT (2026-11-15): the node is configured and present,
	# but there is NO baked LightmapGIData yet, and none can be produced
	# from here: (a) LightmapGI has no script bake() in Godot 4.3 —
	# baking is editor-only; (b) this whole village is built at RUNTIME
	# by this script, so at editor time the scene contains no geometry
	# to bake — the editor bake would find zero static meshes;
	# (c) the editor itself stalls on this project's import (see the
	# import-stall note). The real bake needs a follow-up step first:
	# save the runtime-built village out as a real .tscn (a "bake to
	# scene" tool run), then bake in the editor. Until then the node
	# contributes nothing at runtime (no light_data = no-op, verified:
	# the smoke run below shows no new errors) and the lighting you see
	# comes from the rebalanced sun + fill + sky ambient.
	var gi := LightmapGI.new()
	gi.name = "LightmapGI"
	# NOTE: bake_quality / generate_probes are method-only in 4.3 (no
	# settable property — direct assignment is a runtime SCRIPT ERROR,
	# caught by the smoke run on the first attempt).
	gi.set_bake_quality(LightmapGI.BAKE_QUALITY_MEDIUM)
	gi.bounces = 2
	gi.bounce_indirect_energy = 0.8
	gi.directional = true
	gi.set_generate_probes(LightmapGI.GENERATE_PROBES_SUBDIV_8)
	# 2048, not 1024: the engine rejects anything smaller for the GI
	# atlas ("minimum allowed value is 2048") — this is one atlas, not
	# a per-asset texture, so it does not break the <=1024 asset budget.
	gi.max_texture_size = 2048
	add_child(gi)

# ------------------------------------------------------------------ characters

func _build_hero_visual(parent: Node3D, palette: Dictionary) -> Node3D:
	# Procedural toon humanoid: tunic, head with geometric anime eyes,
	# hair, red cape (hero only), real KayKit sword + shield (hero only).
	var root := Node3D.new()
	root.name = "HeroVisual"
	parent.add_child(root)
	var tunic: Color = palette.get("tunic", Color(0.27, 0.41, 0.72, 1.0))
	var skin: Color = palette.get("skin", Color(0.85, 0.63, 0.45, 1.0))
	var hair_c: Color = palette.get("hair", Color(0.29, 0.17, 0.08, 1.0))
	var pants: Color = palette.get("pants", Color(0.17, 0.18, 0.23, 1.0))
	var has_cape: bool = palette.get("cape", false)
	var has_weapons: bool = palette.get("weapons", false)
	var tunic_mat := _toon(tunic)
	var skin_mat := _toon(skin)
	var hair_mat := _toon(hair_c)
	var pants_mat := _toon(pants)
	var dark_mat := _toon(Color(0.10, 0.07, 0.06, 1.0))
	_capsule(root, 0.34, 1.10, Vector3(0, 0.95, 0), tunic_mat, true)
	_box(root, Vector3(0.72, 0.10, 0.42), Vector3(0, 0.60, 0), _toon(Color(0.42, 0.29, 0.16, 1.0)), true)
	var head := _sphere(root, 0.27, Vector3(0, 1.70, 0), skin_mat, true)
	var hair := _sphere(root, 0.29, Vector3(0, 1.84, -0.04), hair_mat, true)
	hair.scale = Vector3(1.0, 0.62, 1.0)
	# Anime eyes: small dark boxes + tiny white glints, on the face front (+Z).
	_box(root, Vector3(0.05, 0.09, 0.03), Vector3(-0.09, 1.71, 0.252), dark_mat)
	_box(root, Vector3(0.05, 0.09, 0.03), Vector3(0.09, 1.71, 0.252), dark_mat)
	_box(root, Vector3(0.016, 0.025, 0.012), Vector3(-0.082, 1.74, 0.27), _flat(Color(1, 1, 1, 1)))
	_box(root, Vector3(0.016, 0.025, 0.012), Vector3(0.098, 1.74, 0.27), _flat(Color(1, 1, 1, 1)))
	_box(root, Vector3(0.07, 0.018, 0.02), Vector3(0, 1.585, 0.25), _toon(Color(0.48, 0.23, 0.16, 1.0)))
	# Arms and legs.
	_box(root, Vector3(0.17, 0.68, 0.17), Vector3(-0.50, 1.22, 0), tunic_mat, true)
	var arm_r := _box(root, Vector3(0.17, 0.68, 0.17), Vector3(0.50, 1.22, 0), tunic_mat, true)
	_box(root, Vector3(0.20, 0.85, 0.20), Vector3(-0.19, 0.45, 0), pants_mat, true)
	_box(root, Vector3(0.20, 0.85, 0.20), Vector3(0.19, 0.45, 0), pants_mat, true)
	_box(root, Vector3(0.22, 0.12, 0.30), Vector3(-0.19, 0.06, 0.03), _toon(Color(0.42, 0.29, 0.16, 1.0)), true)
	_box(root, Vector3(0.22, 0.12, 0.30), Vector3(0.19, 0.06, 0.03), _toon(Color(0.42, 0.29, 0.16, 1.0)), true)
	if has_cape:
		var cape := _box(root, Vector3(0.82, 1.15, 0.05), Vector3(0, 1.12, -0.36), _toon(Color(0.75, 0.19, 0.16, 1.0)), true)
		cape.rotation.x = 0.16
	if has_weapons:
		var sword: Node3D = _place_in(arm_r, SWORD_SCENE, Vector3(0, -0.42, 0.06), 0, 1.0)
		if sword:
			sword.rotation.x = -1.1
		var shield: Node3D = _place_in(root, SHIELD_SCENE, Vector3(-0.62, 1.05, 0.10), 0, 0.8)
		if shield:
			shield.rotation.y = deg_to_rad(90)
	return root

func _build_warrior_hero(mesh_root: Node3D, scene_path: String = WARRIOR_SCENE,
		hero_scale: float = WARRIOR_SCALE, head_bone: String = "Head",
		shield_pos: Vector3 = Vector3(0.48, 1.90, 0.02)) -> void:
	# Real rigged anime hero, built in Blender from a CC0 base (MPFB by
	# default, Quaternius re-skin behind the USE_MPFB_HERO fallback).
	# The GLB carries its textures embedded, so no atlas fix is needed
	# here. The MPFB GLB skeleton is scale 1 (metres), so the outline
	# width is the normal 0.035 — the old FBX needed 0.00035 because its
	# armature carried a 100x scale.
	var ps: PackedScene = load(scene_path) as PackedScene
	if ps == null:
		push_warning("AetheriaSlice: failed to load " + scene_path)
		return
	var warrior: Node3D = ps.instantiate() as Node3D
	warrior.scale = Vector3.ONE * hero_scale
	warrior.name = "Warrior"
	mesh_root.add_child(warrior)
	_warrior_root = warrior
	_warrior_anim = warrior.find_child("AnimationPlayer", true, false) as AnimationPlayer
	_skeleton = warrior.find_child("Skeleton3D", true, false) as Skeleton3D
	if _skeleton:
		_head_bone_idx = _skeleton.find_bone(head_bone)
	# Face shader (geometric Genshin SDF shadow) + cape sway shader.
	var face_shader: Shader = load(FACE_SHADER) as Shader
	_face_mat = ShaderMaterial.new()
	_face_mat.shader = face_shader
	var cape_shader: Shader = load(CAPE_SHADER) as Shader
	var cape_mat := ShaderMaterial.new()
	cape_mat.shader = cape_shader
	# CAPE FIX (2026-11-15): the painted fold texture (9 stripes,
	# phase-matched to the rebuilt cape's modelled pleats). Without it
	# the shader's flat NDL bands wash the folds out to one flat red.
	cape_mat.set_shader_parameter("fold_tex", load(CAPE_FOLD_TEX) as Texture2D)
	var cape_outline_shader: Shader = load(CAPE_OUTLINE_SHADER) as Shader
	var cape_outline_mat := ShaderMaterial.new()
	cape_outline_mat.shader = cape_outline_shader
	# CAPE FIX (2026-11-15): 0.015, not the shader default 0.035 — the
	# wider hull fragments into black shards along the folded hem/top
	# edge (shots 36/37/38). The fold texture now carries the definition.
	cape_outline_mat.set_shader_parameter("outline_width", 0.015)
	# Inverted-hull outline for the toon surfaces (0.035: GLB is metres).
	var warrior_outline := ShaderMaterial.new()
	warrior_outline.shader = load("res://assets/materials/outline.gdshader") as Shader
	warrior_outline.set_shader_parameter("outline_width", 0.035)
	# Rim+wrap patch (2026-11-15): hero toon + fresnel rim + wrap
	# diffuse, for the hero's flat-colour body parts only (see below).
	var rim_shader: Shader = load("res://assets/materials/hero_toon_rim.gdshader") as Shader
	var cape_mi: MeshInstance3D = null
	# Rim parts need their outline restored as duplicate meshes (see the
	# block after the loop): ShaderMaterial next_pass does not render.
	var rim_outline_mis: Array[MeshInstance3D] = []
	for mi: MeshInstance3D in warrior.find_children("*", "MeshInstance3D", true, false):
		if mi.mesh == null:
			continue
		if mi.name == "Cape":
			cape_mi = mi
		for si: int in range(mi.mesh.get_surface_count()):
			var mat: Material = mi.mesh.surface_get_material(si)
			if mat == null:
				continue
			# Identify by the glTF material NAME (preserved on import).
			# Do NOT use the texture path: embedded GLB textures are
			# extracted to "Warrior_Anime_<name>.png", so a substring check
			# on the path is fragile. resource_name is exact.
			var mat_name: String = mat.resource_name
			if mat_name == "Face_Anime":
				# Face surface: PLAIN toon material, NOT the SDF face
				# shader. The SDF shader (geometric Genshin shadow) was
				# designed for the old hero's FLAT face plate; on the
				# MPFB hero's CURVED 3D face it dims the painted amber
				# eyes to unreadable dark dots and scrambles the features
				# (shot 10, 12:01 — head reads bald, face gone). The
				# painted texture already carries eyes/lashes/brows/blush/
				# smile; a plain toon material lets it show. No outline
				# on the face either (it would ring the face in black).
				# RIM+WRAP PATCH (2026-11-15) NOTE: the rim uniforms +
				# wrap ndl were applied to anime_face.gdshader, but that
				# shader is NOT wired to this surface (same reason as
				# above) — so the face rim has no visible effect yet; the
				# face must keep reading exactly as shot 10 until the
				# SDF shader is re-proven on the curved face.
				var sm := mat as StandardMaterial3D
				sm.diffuse_mode = BaseMaterial3D.DIFFUSE_TOON
				sm.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
				sm.metallic = 0.0
			elif mi.name == "Cape" or mat_name == "Cape_Red":
				# Baked cloth cape: toon + vertex sway shader.
				mi.mesh.surface_set_material(si, cape_mat)
			elif mat_name == "HairCards":
				# Hair cards: toon + ALPHA SCISSOR (the GLB exporter wrote
				# BLEND; scissor is cheaper on mobile and avoids sort bugs).
				# NO outline: the 0.035 inverted hull swallows the thin
				# strands in black, so they render as black scribbles
				# (shot 10, 12:01). The strands must show brown, not black.
				var sm := mat as StandardMaterial3D
				sm.diffuse_mode = BaseMaterial3D.DIFFUSE_TOON
				sm.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
				sm.metallic = 0.0
				sm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
				sm.alpha_scissor_threshold = 0.5
			elif mat is StandardMaterial3D:
				var sm := mat as StandardMaterial3D
				sm.diffuse_mode = BaseMaterial3D.DIFFUSE_TOON
				sm.specular_mode = BaseMaterial3D.SPECULAR_TOON
				sm.metallic_specular = 0.4
				# The Warrior FBX import set Metallic=1 on its materials
				# (the old "black hero" bug) — the MPFB kitbash inherits
				# it on the sword, which then mirrors the blue sky
				# (angle-dependent blue blade, shot 10, 12:00). No metal.
				sm.metallic = 0.0
				# CAPE FIX (2026-11-15): NO outline on Skin or Hair — the
				# inverted hull (0.035 on the decimated head) pokes black
				# triangular shards THROUGH the face, and the pure-black
				# (0,0,0) pixels scribbled across the eyes/cheeks in
				# shots 10 (runs 1-2) are the hull, not the face texture
				# (whose darkest is (20,10,4)). The face texture's eyes
				# render white + bright amber underneath it. The body
				# keeps its outline; the head reads clean without it.
				if mat_name != "Skin" and mat_name != "Hair":
					sm.next_pass = warrior_outline
				if mat_name == "Warrior_Sword_Texture":
					# The kitbashed sword rendered BRIGHT BLUE in Godot
					# (shot 10, 11:50) — disabling the toon specular did
					# NOT fix it (12:00), so the blue is in the
					# Warrior_Sword_Texture atlas itself (blue-tinted
					# steel, reads grey in Blender, saturated blue under
					# Godot's sRGB + sun). Steel, not a lightsaber: drop
					# the blue texture, plain steel-grey albedo.
					sm.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
					sm.albedo_texture = null
					# 0.38, not 0.55: the 0.55 steel rendered near-white
					# under the toon brightest band + sun and dominated
					# the closeup (shot 10, 12:05). Mid-grey steel.
					sm.albedo_color = Color(0.38, 0.40, 0.43)
				if mat_name == "Plate_Steel":
					# The chest plate rendered WHITE (shot 10, 11:50) —
					# the toon specular adds a broad white highlight on
					# the facing plate. No toon specular, darker steel.
					sm.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
					sm.albedo_color = Color(0.30, 0.32, 0.35)
				if mat_name == "Warrior_Texture" and mi.name in ["Warrior_Body", "ShoulderPad_L", "ShoulderPad_R"]:
					# Graphics pass: the plate armour is painted near-black
					# in the shared Warrior_Texture atlas, so Godot's fixed
					# toon bands (no band parameter is exposed on
					# StandardMaterial3D) drop it into the darkest band and
					# it reads charcoal. A small warm emissive floor lifts
					# the dark end of the range without blowing the
					# highlights; the face uses its own shader and the
					# sword its own texture, so neither is touched.
					sm.emission_enabled = true
					sm.emission = Color(0.14, 0.12, 0.10)
				# RIM+WRAP PATCH (2026-11-15), Part 2: the hero's
				# flat-colour body parts get the custom toon+rim shader
				# (tunic + sleeves, chest plate, sword). ONLY these:
				# every one is a flat albedo with no texture (verified by
				# probe 2026-11-15: Tunic_Blue / Plate_Steel /
				# Warrior_Sword_Texture all has_tex=false, sword texture
				# already nulled above), so the verbatim shader's flat
				# albedo uniform loses nothing. The textured parts stay
				# on StandardMaterial3D toon — Face_Anime (painted face),
				# HairCards (alpha cutout), Skin (head must keep NO
				# outline), Pants/Boots/Belt (small, keep their outline
				# via next_pass) — the verbatim rim shader has no texture
				# slot, and swapping an atlas/textured part onto it would
				# destroy the paint. Albedo is read from sm AFTER the
				# Plate_Steel / sword darkening above, so the calibrated
				# final colours carry over. next_pass is set exactly as
				# the patch prescribes; whether the outline still renders
				# on a ShaderMaterial is verified in shots 09/10 (the
				# cape code notes ShaderMaterials have no next_pass — if
				# the torso outline is gone there, the duplicate-mesh
				# pattern from the cape is used instead).
				if mat_name in ["Tunic_Blue", "Plate_Steel", "Warrior_Sword_Texture"]:
					var rim_mat := ShaderMaterial.new()
					rim_mat.shader = rim_shader
					rim_mat.set_shader_parameter("albedo", Color(sm.albedo_color.r, sm.albedo_color.g, sm.albedo_color.b, 1.0))
					# next_pass deliberately NOT set: with
					# rim_mat.next_pass = warrior_outline the rim parts
					# rendered pure (0,0,0) in shots 09/10 (the
					# ShaderMaterial next pass misbehaves — the base pass
					# was invisible then too, see the cull note in
					# hero_toon_rim.gdshader). The torso outline is
					# restored with the duplicate-mesh pattern (CapeOutline)
					# only if the re-shoot shows the edge is lost.
					mi.mesh.surface_set_material(si, rim_mat)
					# Record the MeshInstance once for the outline
					# duplicate below (one surface per rim mesh, but
					# guard anyway — a second surface would double the
					# hull and z-fight).
					if mi not in rim_outline_mis:
						rim_outline_mis.append(mi)
	# Cape outline: duplicate of the cape mesh with the swaying outline
	# shader, so the black edge follows the cloth (ShaderMaterials have no
	# next_pass). Same parent (the Skeleton3D) = identical skinning.
	if cape_mi != null:
		var cape_outline := MeshInstance3D.new()
		cape_outline.name = "CapeOutline"
		cape_outline.mesh = cape_mi.mesh
		cape_outline.material_override = cape_outline_mat
		cape_outline.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		cape_mi.get_parent().add_child(cape_outline)
	# Rim-part outlines: the same duplicate-mesh pattern for the five
	# rim-shader parts (Tunic, Sleeve_L/R, ChestPlate, Warrior_Sword).
	# Their ShaderMaterials cannot carry next_pass (proven: setting it
	# renders the parts pure black in shots 09/10), so without these
	# duplicates the torso loses the black toon edge it had under
	# StandardMaterial3D. +5 draw calls (budget 172 -> ~177, still <200).
	for rim_mi in rim_outline_mis:
		var rim_outline := MeshInstance3D.new()
		rim_outline.name = rim_mi.name + "Outline"
		rim_outline.mesh = rim_mi.mesh
		rim_outline.material_override = warrior_outline
		rim_outline.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		rim_mi.get_parent().add_child(rim_outline)
	# KayKit round shield on the LEFT arm (+X is the character's left).
	# Static offset at the forearm's rest position, like the previous slice.
	# static_gi=false: it moves with the hero, so it must NOT be baked.
	var shield: Node3D = _place_in(warrior, SHIELD_SCENE, shield_pos, 90, 0.8, false)
	if shield:
		shield.name = "Shield"
	# The hero's own sword stays rigged to the hand bone (Weapon.R on the
	# old Warrior, mixamorig:RightHand on the MPFB hero); it moves with
	# the hand and the Sword_Attack clips. Its visibility is checked in
	# the screenshots before deciding on the KayKit sword instead.
	if _warrior_anim:
		_warrior_anim.play(ANIM_IDLE)
		_current_anim = ANIM_IDLE

func _build_npc() -> void:
	# One villager by the market, green tunic, no cape or weapons.
	var npc := _build_hero_visual(self, {
		"tunic": Color(0.29, 0.48, 0.23, 1.0),
		"skin": Color(0.82, 0.60, 0.44, 1.0),
		"hair": Color(0.55, 0.55, 0.55, 1.0),
		"pants": Color(0.30, 0.28, 0.20, 1.0),
		"cape": false,
		"weapons": false,
	})
	npc.position = Vector3(3.5, 0, -8)
	npc.rotation.y = deg_to_rad(35)
	# Interactable zone: PlayerInteraction (radius 3 m around the hero)
	# picks this Area3D up and forwards the E press to interact(),
	# which opens the villager's Dialogue Manager dialogue.
	# (Created via set_script + .call("interact") — not via the global
	# class name — so the slice never depends on the editor's
	# global-script-class cache, which headless runs do not refresh.)
	var area := Area3D.new()
	area.set_script(load("res://scripts/dialogue/npc_interact_area.gd"))
	area.name = "InteractArea"
	area.position = Vector3(0, 1.0, 0)
	var shape := CollisionShape3D.new()
	var sphere := SphereShape3D.new()
	sphere.radius = 2.2
	shape.shape = sphere
	area.add_child(shape)
	npc.add_child(area)
	_npc_area = area

# ------------------------------------------------------------------ player

func _wire_player() -> void:
	var player: Node = get_node_or_null("Player")
	if player == null:
		push_warning("AetheriaSlice: no Player node in scene")
		return
	# Swap the primitive prototype visuals for the real hero: MPFB rebuild
	# by default, old Quaternius re-skin behind the fallback flag.
	var mesh_root: Node3D = player.find_child("MeshRoot", true, false) as Node3D
	if mesh_root:
		for child_name: String in ["Body", "Head", "ArmL", "ArmR", "LegL", "LegR"]:
			var part: Node = mesh_root.find_child(child_name, false, false)
			if part:
				part.visible = false
		if USE_MPFB_HERO:
			_build_warrior_hero(mesh_root, MPFB_HERO_SCENE, MPFB_HERO_SCALE,
				"mixamorig:Head", MPFB_SHIELD_POS)
		else:
			_build_warrior_hero(mesh_root)
	_player = player as CharacterBody3D
	player.position = Vector3(0, 0, 8)
	player.rotation.y = 0.0
	GameManager.register_player(player)
	player.set("movement_enabled", true)
	var rig: Node = player.find_child("CameraRig", true, false)
	if rig:
		player.set("camera_yaw_node", rig)
	GameManager.start_game()

# ------------------------------------------------------------------ dialogue + quest

func _ensure_quest_manager() -> void:
	# main.tscn has a QuestManager child; the slice scene does not.
	# Create one so the villager's `do start_golem_quest()` mutation
	# and the combat agent's complete_objective() have a real target.
	if find_child("QuestManager", false, false) != null:
		return
	var qm := Node.new()
	qm.set_script(load("res://scripts/quests/quest_manager.gd"))
	qm.name = "QuestManager"
	add_child(qm)


func _on_dialogue_started(_resource: DialogueResource) -> void:
	# Freeze the hero while the balloon is open.
	if _player != null:
		_player.set("movement_enabled", false)


func _on_dialogue_ended(_resource: DialogueResource) -> void:
	if _player != null:
		_player.set("movement_enabled", true)


func start_golem_quest() -> void:
	# Dialogue Manager mutation target: called by the villager dialogue's
	# `do start_golem_quest()` line when the hero accepts the quest.
	# The combat agent completes it with
	# QuestManager.complete_objective("golem_quest", 0).
	if _golem_quest_accepted:
		return
	_golem_quest_accepted = true
	var qm: Node = find_child("QuestManager", false, false)
	if qm != null and qm.has_method("start_quest"):
		qm.start_quest("golem_quest")
	print("[AETHERIA-QUEST] golem_quest accepted — defeat the rock golem in the forest clearing")


func _run_collision_test() -> void:
	# Headless check: drive the hero west into home_A (centre
	# (-7.2, 0, 2), east face ≈ x -6.52) and confirm the position
	# stops at the wall instead of passing through the house.
	await get_tree().process_frame
	await get_tree().process_frame
	_player.teleport_to(Vector3(-4.5, 0, 2))
	await get_tree().process_frame
	await get_tree().process_frame
	var start_x: float = _player.global_position.x
	_player.joystick_vector = Vector2(-1, 0)
	print("[AETHERIA-COLLISION-TEST] start_x=", start_x, " driving west into home_A")
	for i: int in range(8):
		await get_tree().create_timer(0.5).timeout
		print("[AETHERIA-COLLISION-TEST] t=", (i + 1) * 0.5, "s pos=", _player.global_position)
	_player.joystick_vector = Vector2.ZERO
	var end_x: float = _player.global_position.x
	var blocked: bool = end_x > -6.5
	print("[AETHERIA-COLLISION-TEST] end_x=", end_x, " blocked=", blocked, " (house east face ≈ -6.52)")
	print("[AETHERIA-COLLISION-TEST] ", "PASS — hero stopped at the house wall" if blocked else "FAIL — hero walked through the house")
	get_tree().quit()


func _run_dialogue_test() -> void:
	# Headless check: walk the whole villager dialogue — open, advance
	# through the greeting to the response menu, pick "accept", advance
	# to END — and confirm the golem quest actually starts.
	await get_tree().process_frame
	await get_tree().process_frame
	_player.teleport_to(Vector3(3.5, 0, -5.5))
	await get_tree().process_frame
	await get_tree().process_frame
	if _npc_area == null:
		print("[AETHERIA-DIALOGUE-TEST] FAIL — no NPC interact area")
		get_tree().quit()
		return
	var balloon = _npc_area.call("interact")
	if balloon == null:
		print("[AETHERIA-DIALOGUE-TEST] FAIL — interact() returned no balloon")
		get_tree().quit()
		return
	var waits := 0
	while balloon.dialogue_line == null and waits < 60:
		await get_tree().process_frame
		waits += 1
	if balloon.dialogue_line == null:
		print("[AETHERIA-DIALOGUE-TEST] FAIL — first dialogue line never loaded")
		get_tree().quit()
		return
	print("[AETHERIA-DIALOGUE-TEST] line1 character=", balloon.dialogue_line.character, " text=", balloon.dialogue_line.text)
	for i: int in range(3):
		await get_tree().process_frame
		await get_tree().process_frame
		balloon.advance_dialogue()
	waits = 0
	while balloon.dialogue_line != null and balloon.dialogue_line.responses.is_empty() and waits < 60:
		await get_tree().process_frame
		waits += 1
	if balloon.dialogue_line == null or balloon.dialogue_line.responses.is_empty():
		print("[AETHERIA-DIALOGUE-TEST] FAIL — no response menu reached")
		get_tree().quit()
		return
	var response_texts: Array = []
	for r: DialogueResponse in balloon.dialogue_line.responses:
		response_texts.append(r.text)
	print("[AETHERIA-DIALOGUE-TEST] responses=", response_texts)
	balloon.select_response(0)
	var steps := 0
	# Guard with is_instance_valid: the balloon queue_free()s itself
	# when the dialogue ends, so a bare balloon.is_open read after
	# that is a SCRIPT ERROR on a freed object.
	while is_instance_valid(balloon) and balloon.is_open and steps < 10:
		await get_tree().process_frame
		await get_tree().process_frame
		if is_instance_valid(balloon):
			balloon.advance_dialogue()
		steps += 1
	await get_tree().process_frame
	await get_tree().process_frame
	var balloon_open: bool = is_instance_valid(balloon) and balloon.is_open
	var qm: Node = find_child("QuestManager", false, false)
	var quest_active: bool = qm != null and (qm.get("active") as Dictionary).has("golem_quest")
	print("[AETHERIA-DIALOGUE-TEST] balloon_open=", balloon_open, " quest_accepted=", _golem_quest_accepted, " quest_active=", quest_active)
	if not balloon_open and _golem_quest_accepted and quest_active:
		print("[AETHERIA-DIALOGUE-TEST] PASS — dialogue closed, golem_quest active")
	else:
		print("[AETHERIA-DIALOGUE-TEST] FAIL — dialogue did not complete the quest")
	get_tree().quit()


# ------------------------------------------------------------------ screenshots

func _setup_dialogue_shot():
	# Shot 13 staging: put the hero face-to-face with the villager,
	# open the dialogue, and advance past the greeting to the golem
	# line (line 3) so the shot shows the quest itself. Returns the
	# open balloon so _run_shots can close it after the capture —
	# otherwise it would still be open over shot 14 (the vista).
	if _player != null:
		_player.teleport_to(Vector3(3.5, 0, -5.4))
		_player.rotation.y = PI
	await get_tree().process_frame
	await get_tree().process_frame
	if _npc_area == null:
		push_warning("AetheriaSlice: no NPC area for dialogue shot")
		return null
	var balloon = _npc_area.call("interact")
	if balloon == null:
		push_warning("AetheriaSlice: dialogue balloon did not open for shot 13")
		return null
	var waits := 0
	while balloon.dialogue_line == null and waits < 60:
		await get_tree().process_frame
		waits += 1
	for i: int in range(2):
		await get_tree().process_frame
		await get_tree().process_frame
		balloon.advance_dialogue()
	waits = 0
	while balloon.dialogue_line != null and balloon.dialogue_line.text.is_empty() and waits < 30:
		await get_tree().process_frame
		waits += 1
	print("[AETHERIA-SHOT] dialogue line for shot 13: ", balloon.current_text())
	await get_tree().process_frame
	await get_tree().process_frame
	return balloon


func _run_shots() -> void:
	await get_tree().process_frame
	await get_tree().process_frame
	# Graphics pass — budget counts from the live renderer, printed so
	# the run log carries the real tri/draw-call numbers (STUDIO.md:
	# <100k tris, <200 draw calls, <2,000 live particles).
	print("[AETHERIA-BUDGET] draw_calls=",
		RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME),
		" primitives=",
		RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME),
		" objects=",
		RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_OBJECTS_IN_FRAME))
	var hud: CanvasLayer = get_node_or_null("HUD") as CanvasLayer
	if hud:
		hud.visible = false
	# Hero-relative framing (pass 2): print the hero's REAL position first,
	# then aim shots 10/11 at the actual hero instead of assumed coords.
	var hero_pos: Vector3 = Vector3(0, 0, 8)
	var head_pos: Vector3 = hero_pos + Vector3(0, 1.62, 0)
	if _player != null:
		hero_pos = _player.global_position
	if _skeleton != null and _head_bone_idx >= 0:
		var _pose: Transform3D = _skeleton.get_bone_global_pose(_head_bone_idx)
		head_pos = (_skeleton.global_transform * _pose).origin
	print("[AETHERIA-SHOT] hero_pos=", hero_pos,
		" head_pos=", head_pos,
		" warrior_root=", _warrior_root.global_position if _warrior_root else Vector3.ZERO)
	var shots: Array = [
		{
			# Face closeup from the front (+Z): the hero faces +Z in
			# Godot — CONFIRMED 12:25 by reading shots 07 (-Z, back) and
			# 11 (+Z, face) from the same run after a forced re-import.
			# (The -Z "fix" at 12:20 was a misread: the stale .scn had
			# flipped the apparent facing. +Z is correct. Do NOT flip
			# again without re-reading both shots from one run.)
			"path": SHOT_DIR + "/07-anime-hero-closeup.png",
			"pos": Vector3(0.6, 1.85, 9.7), "target": Vector3(0, 1.6, 8.0),
			"anim": ANIM_IDLE, "seek": 0.4
		},
		{
			"path": SHOT_DIR + "/08-anime-hero-street.png",
			"pos": Vector3(2.6, 2.1, 13.5), "target": Vector3(0, 1.2, 5.0),
			"anim": ANIM_IDLE, "seek": 0.4
		},
		{
			# Walk, closer + from the sword side (-X): the shield is on the
			# left arm (+X) and blocked the body from the old +X camera.
			"path": SHOT_DIR + "/09-anime-hero-walk.png",
			"pos": Vector3(-2.6, 1.5, 8.0), "target": Vector3(0, 1.0, 8.0),
			"anim": ANIM_WALK, "seek": 0.5
		},
		{
			# Face closeup: camera IN FRONT (+Z), 1.55 m. Hero faces +Z
			# (confirmed 12:25, shots 07+11 from one run). 1.55 m: hero
			# fills the shot, eyes readable, sword not dominant.
			"path": SHOT_DIR + "/10-hero-pass2-closeup.png",
			"pos": head_pos + Vector3(0.10, 0.05, 1.55),
			"target": head_pos + Vector3(0, 0.0, 0.05),
			"anim": ANIM_IDLE, "seek": 0.4
		},
		{
			# Back / cape: camera BEHIND (-Z) — the cape hangs on -Z
			# (the hero's back, away from his +Z facing).
			"path": SHOT_DIR + "/11-hero-back-cape.png",
			"pos": hero_pos + Vector3(0, 1.65, -2.2),
			"target": hero_pos + Vector3(0, 1.05, 0),
			"anim": ANIM_WALK, "seek": 0.5
		},
		{
			# CAPE FIX (2026-11-15) — cape verification set, hero-relative.
			# 36 front: the cape draped over the shoulders from the front.
			"path": SHOT_DIR + "/36-cape-front.png",
			"pos": hero_pos + Vector3(0.3, 1.5, 2.4),
			"target": hero_pos + Vector3(0, 1.1, 0),
			"anim": ANIM_IDLE, "seek": 0.4
		},
		{
			# 37 back: the cape's fold bands, full length, mid-walk.
			"path": SHOT_DIR + "/37-cape-back.png",
			"pos": hero_pos + Vector3(0, 1.6, -2.4),
			"target": hero_pos + Vector3(0, 1.0, 0),
			"anim": ANIM_WALK, "seek": 0.5
		},
		{
			# 38 side: the drape profile + hem flare from the sword side.
			"path": SHOT_DIR + "/38-cape-side.png",
			"pos": hero_pos + Vector3(-2.4, 1.4, 0),
			"target": hero_pos + Vector3(0, 1.0, 0),
			"anim": ANIM_WALK, "seek": 0.5
		},
		{
			# Dialogue shot: hero face-to-face with the green villager,
			# balloon open on the golem line (line 3 of the dialogue).
			"path": SHOT_DIR + "/13-dialogue.png",
			"pos": Vector3(6.8, 2.0, -4.6), "target": Vector3(3.5, 1.0, -6.8),
			"anim": ANIM_IDLE, "seek": 0.4,
			"dialogue": true
		},
		{
			# Graphics pass — NEW vista shot: wide elevated view down the
			# street over the plaza, village, castle silhouette, floating
			# islands, horizon hills and the painted sky/fog gradient.
			"path": SHOT_DIR + "/14-vista-graphics.png",
			"pos": Vector3(14, 7, 26), "target": Vector3(0, 2, -50),
			"anim": ANIM_IDLE, "seek": 0.4
		},
		{
			# Deep-graphics integration (2026-11-15) — 39: terrain splat
			# patch at (22, 0, -12), east open ground. Grass must dominate
			# the flat top; dirt only on slopes and at the base.
			"path": SHOT_DIR + "/39-terrain-splat.png",
			"pos": Vector3(28, 3.5, -2), "target": Vector3(22, 1.0, -12),
			"anim": ANIM_IDLE, "seek": 0.4
		},
		{
			# 40: mossy-rock clearing at (-24, 0, -56), the golem's forest
			# clearing behind the village (dialogue line 3).
			"path": SHOT_DIR + "/40-rock-clearing.png",
			"pos": Vector3(-18, 3.5, -48), "target": Vector3(-24, 0.8, -56),
			"anim": ANIM_IDLE, "seek": 0.4
		},
		{
			# 41: pond at (24, 0, 6) with the reflection probe above it.
			"path": SHOT_DIR + "/41-pond.png",
			"pos": Vector3(30, 4, 14), "target": Vector3(24, 0.3, 6),
			"anim": ANIM_IDLE, "seek": 0.4
		},
		{
			# 43a/43b: wind sway on the near (west) trees. Same framing,
			# 1.5 s apart — the tree tops must have visibly moved.
			"path": SHOT_DIR + "/43a-wind.png",
			"pos": Vector3(-4, 2.5, 6), "target": Vector3(-14, 2.0, -10),
			"anim": ANIM_IDLE, "seek": 0.4
		},
		{
			"path": SHOT_DIR + "/43b-wind.png",
			"pos": Vector3(-4, 2.5, 6), "target": Vector3(-14, 2.0, -10),
			"anim": ANIM_IDLE, "seek": 0.4, "wait_sec": 1.5
		},
	]
	for s: Dictionary in shots:
		if _shot_cam == null:
			break
		# Time-based pairs (clouds 42b, wind 43b): wait before the
		# second capture so the sway/clouds have visibly moved.
		if float(s.get("wait_sec", 0.0)) > 0.0:
			await get_tree().create_timer(float(s["wait_sec"])).timeout
		_shot_cam.position = s["pos"] as Vector3
		_shot_cam.look_at_from_position(s["pos"] as Vector3, s["target"] as Vector3, Vector3.UP)
		_shot_cam.current = true
		var dialogue_balloon = null
		if bool(s.get("dialogue", false)):
			dialogue_balloon = await _setup_dialogue_shot()
		await get_tree().process_frame
		await get_tree().process_frame
		_set_warrior_pose(s["anim"] as String, float(s["seek"]))
		await get_tree().process_frame
		var img: Image = get_viewport().get_texture().get_image()
		var err: int = img.save_png(s["path"] as String)
		print("[AETHERIA-SHOT] ", s["path"], " err=", err, " size=", img.get_size(), " first_px=", img.get_pixel(8, 8))
		if dialogue_balloon != null and is_instance_valid(dialogue_balloon):
			dialogue_balloon.call("close")
	print("[AETHERIA-BUDGET] end-of-shots draw_calls=",
		RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME),
		" primitives=",
		RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME))
	if hud:
		hud.visible = true
	print("[AETHERIA-SHOT] done — quitting")
	get_tree().quit()
