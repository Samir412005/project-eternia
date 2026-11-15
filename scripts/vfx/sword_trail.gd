class_name VFXSwordTrail
extends Node3D
## Sword / weapon trail — project-original ribbon (Godot 4.3, Mobile).
##
## Technique reference: Gennai EDGEFLUX Lite (MIT, github.com/kai777123/
## godot-4-free-vfx) — world-space sampling of blade base/tip. This file
## is written from scratch: it samples at most 90 Hz, builds a plain
## linear ribbon (no Catmull-Rom), and fades by age. No Gennai code or
## files are vendored (their sample targets Godot 4.4+, untested on 4.3).
##
## Usage: add as a child of the weapon (or a bone attachment) and set
## base_offset / tip_offset along the blade. With auto_emit_speed > 0 the
## trail only draws while the tip moves fast (i.e. during a swing).
## Particles: 0 — this is a mesh ribbon, one draw call.

const SAMPLE_INTERVAL: float = 1.0 / 90.0
const TRAIL_SHADER: Shader = preload("res://assets/materials/vfx_trail.gdshader")

## Blade start, in this node's local space.
@export var base_offset: Vector3 = Vector3(0.0, 0.15, 0.0)
## Blade tip, in this node's local space.
@export var tip_offset: Vector3 = Vector3(0.0, 1.05, 0.0)
## Draw new trail while true.
@export var emitting: bool = true
## Trail only draws while the tip moves faster than this (m/s); 0 = always.
@export_range(0.0, 30.0, 0.01) var auto_emit_speed: float = 2.0
## Seconds a point of the trail stays visible.
@export_range(0.03, 2.0, 0.005) var lifetime: float = 0.26
@export var trail_color: Color = Color(0.65, 0.85, 1.0)

var _samples: Array[Dictionary] = []
var _mesh: ImmediateMesh
var _mi: MeshInstance3D
var _last_tip: Vector3
var _last_sample_tip: Vector3
var _accum: float = 0.0


func _ready() -> void:
	_mesh = ImmediateMesh.new()
	_mi = MeshInstance3D.new()
	_mi.mesh = _mesh
	_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var mat := ShaderMaterial.new()
	mat.shader = TRAIL_SHADER
	_mi.material_override = mat
	add_child(_mi)
	_last_tip = to_global(tip_offset)
	_last_sample_tip = _last_tip


func _process(delta: float) -> void:
	# Age out old samples.
	var i: int = 0
	while i < _samples.size():
		_samples[i]["age"] = float(_samples[i]["age"]) + delta
		if float(_samples[i]["age"]) >= lifetime:
			_samples.remove_at(i)
		else:
			i += 1
	if emitting:
		var tip: Vector3 = to_global(tip_offset)
		var speed: float = tip.distance_to(_last_tip) / maxf(delta, 0.0001)
		_last_tip = tip
		if speed >= auto_emit_speed:
			_accum += delta
			# Sample at most every 1/90 s, but ALSO whenever the tip has
			# travelled 6 cm since the last sample: at low frame rates
			# (software rendering, slow phones) the time cap alone would
			# starve the ribbon, since samples expire before the next
			# frame arrives.
			if _accum >= SAMPLE_INTERVAL or tip.distance_to(_last_sample_tip) > 0.06:
				_accum = 0.0
				_last_sample_tip = tip
				_samples.append({
					"base": to_global(base_offset),
					"tip": tip,
					"age": 0.0,
				})
	_rebuild()


func _rebuild() -> void:
	_mesh.clear_surfaces()
	if _samples.size() < 2:
		return
	_mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
	for s in _samples:
		var fade: float = 1.0 - float(s["age"]) / lifetime
		var col: Color = trail_color * fade
		_mesh.surface_set_color(col)
		_mesh.surface_add_vertex(to_local(s["base"]))
		_mesh.surface_set_color(col)
		_mesh.surface_add_vertex(to_local(s["tip"]))
	_mesh.surface_end()
