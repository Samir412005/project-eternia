class_name VFXSlashEffect
extends Node3D
## One-shot slash arc — project-original (Godot 4.3, Mobile).
##
## Builds an annular-sector mesh in code, sweeps a bright leading edge
## along it with the vfx_slash shader, then frees itself. No textures,
## no particles, one draw call, no bloom.
## Usage: VFXSlashEffect.spawn(parent, global_pos, rotation, color, radius)

const SLASH_SHADER: Shader = preload("res://assets/materials/vfx_slash.gdshader")

## Arc radius (m).
@export_range(0.3, 4.0, 0.05) var radius: float = 1.2
## Arc sweep in degrees.
@export_range(30.0, 270.0, 1.0) var arc_degrees: float = 110.0
## How long the slash is visible (s).
@export_range(0.05, 1.0, 0.01) var duration: float = 0.25
@export var slash_color: Color = Color(0.65, 0.85, 1.0)

var _time: float = 0.0
var _mat: ShaderMaterial
var _mi: MeshInstance3D


static func spawn(parent: Node, at: Vector3, rot: Vector3,
		color: Color = Color(0.65, 0.85, 1.0), p_radius: float = 1.2) -> VFXSlashEffect:
	# Loaded at call time (not a const preload) to avoid a script<->scene cycle.
	var scene: PackedScene = load("res://scenes/vfx/slash_effect.tscn") as PackedScene
	var fx: VFXSlashEffect = scene.instantiate() as VFXSlashEffect
	fx.slash_color = color
	fx.radius = p_radius
	parent.add_child(fx)
	fx.global_position = at
	fx.rotation = rot
	return fx


func _ready() -> void:
	_mat = ShaderMaterial.new()
	_mat.shader = SLASH_SHADER
	_mat.set_shader_parameter("color", slash_color)
	_mat.set_shader_parameter("progress", 0.0)
	_mi = MeshInstance3D.new()
	_mi.mesh = _build_arc_mesh()
	_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_mi.material_override = _mat
	add_child(_mi)


func _process(delta: float) -> void:
	_time += delta
	var p: float = clampf(_time / duration, 0.0, 1.0)
	_mat.set_shader_parameter("progress", p)
	if _time >= duration:
		queue_free()


func _build_arc_mesh() -> ArrayMesh:
	var segments: int = 24
	var inner: float = radius * 0.55
	var arc: float = deg_to_rad(arc_degrees)
	var verts := PackedVector3Array()
	var uvs := PackedVector2Array()
	var indices := PackedInt32Array()
	for i in range(segments + 1):
		var t: float = float(i) / float(segments)
		var a: float = -arc * 0.5 + arc * t
		var dir := Vector3(cos(a), sin(a), 0.0)
		verts.append(dir * inner)
		uvs.append(Vector2(t, 0.0))
		verts.append(dir * radius)
		uvs.append(Vector2(t, 1.0))
		if i < segments:
			var b: int = i * 2
			indices.append_array(PackedInt32Array([b, b + 1, b + 2, b + 1, b + 3, b + 2]))
	var arrays: Array = []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = verts
	arrays[Mesh.ARRAY_TEX_UV] = uvs
	arrays[Mesh.ARRAY_INDEX] = indices
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	return mesh
