class_name VFXHitSparks
extends GPUParticles3D
## Hit sparks — one-shot burst (Godot 4.3, Mobile renderer).
## 48 particles, lifetime 0.4 s, frees itself when done.
## Technique reference: Gennai EDGEFLUX Lite hit preset (MIT) — a flash
## + spark burst. This scene is project-original; no Gennai files vendored.
## Usage: VFXHitSparks.spawn(parent, global_pos, normal)

## Loaded at call time (not a const preload) to avoid a script<->scene cycle.


static func spawn(parent: Node, at: Vector3,
		normal: Vector3 = Vector3.UP) -> VFXHitSparks:
	var scene: PackedScene = load("res://scenes/vfx/hit_sparks.tscn") as PackedScene
	var fx: VFXHitSparks = scene.instantiate() as VFXHitSparks
	parent.add_child(fx)
	fx.global_position = at
	if normal.length_squared() > 0.001 and absf(normal.normalized().dot(Vector3.UP)) < 0.99:
		# look_at() fails when the direction is parallel to the up vector;
		# the burst is omnidirectional, so orientation does not matter then.
		fx.look_at_from_position(at, at + normal, Vector3.UP)
	fx.emitting = true
	return fx


func _ready() -> void:
	finished.connect(queue_free)
