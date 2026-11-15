class_name VFXEmberLoop
extends GPUParticles3D
## Golem lava ember loop — ambient rising embers (Godot 4.3, Mobile).
## 60 particles max, lifetime 2.5 s, loops forever while emitting.
## Attach as a child of the golem (e.g. at the chest) — local_coords keeps
## the embers following the golem. Unshaded billboard quads with a
## yellow->orange->transparent colour ramp: glow faked, never real bloom.
## Technique reference: Ember VFX 3D Lite (inkharbor, free commercial
## licence, NOT vendored — its files may not be redistributed and Vol. 1
## does not run on Godot 4.3). This scene is project-original.

## 0.0 - 1.0; scales the live particle count (60 at full intensity).
@export_range(0.0, 1.0, 0.05) var intensity: float = 1.0


func _ready() -> void:
	amount = int(60.0 * clampf(intensity, 0.0, 1.0))
	emitting = true
