extends Node3D
## VFX demo scene driver (NOT wired into the game — verification only).
## Swings a sword with a live trail, spawns a slash + hit sparks every
## 1.4 s, and shows the rock golem with its ember loop. Run this scene
## headless / in Xvfb and screenshot it to prove each effect is visible.
## Particle budget in this scene: 48 (sparks, one-shot) + 60 (embers)
## = 108 live max, well under the 2,000 studio budget.

const SlashEffect := preload("res://scripts/vfx/slash_effect.gd")
const HitSparks := preload("res://scripts/vfx/hit_sparks.gd")

var _time: float = 0.0
var _timer: float = 0.0


func _ready() -> void:
	$Camera3D.look_at(Vector3(0.0, 1.3, 0.0), Vector3.UP)


func _process(delta: float) -> void:
	_time += delta
	$SwordPivot.rotation.z = sin(_time * 2.0) * 1.2
	$SwordPivot.rotation.y = _time * 0.35
	_timer += delta
	if _timer >= 1.4:
		_timer = 0.0
		var tip: Vector3 = $SwordPivot/BladeTip.global_position
		SlashEffect.spawn(self, tip, Vector3(0.0, 0.0, randf() * 0.6 - 0.3),
			Color(0.65, 0.85, 1.0), 1.2)
		HitSparks.spawn(self, $Target.global_position)
