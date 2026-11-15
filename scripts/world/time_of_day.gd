extends Node
## TimeOfDay — a real day clock (0..24) that rotates the sun.
## Phase 1: slow fixed drift; full day/night cycle in Phase 2.
var time_hours: float = 10.0
var time_scale: float = 0.05
var sun: DirectionalLight3D = null

func _ready() -> void:
    _find_sun()

func _find_sun() -> void:
    var cs: Node = get_tree().current_scene
    if cs != null:
        sun = cs.find_child("Sun", true, false) as DirectionalLight3D

func _process(delta: float) -> void:
    if sun == null:
        _find_sun()
        if sun == null:
            return
    time_hours = fmod(time_hours + delta * time_scale, 24.0)
    var angle: float = deg_to_rad((time_hours - 6.0) / 12.0 * 180.0)
    sun.rotation_degrees = Vector3(-45.0 + sin(angle) * 10.0, -30.0, 0.0)

func is_night() -> bool:
    return time_hours < 6.0 or time_hours >= 18.0
