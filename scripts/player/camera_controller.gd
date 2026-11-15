extends Node3D
## CameraController — yaw/pitch rig on a SpringArm3D (collision-aware).
## Drag on empty screen area rotates; pinch is NOT implemented (roadmap).
@export var pitch_min: float = -0.35
@export var pitch_max: float = 0.85
@export var drag_sensitivity: float = 0.004

var yaw: float = 0.0
var pitch: float = 0.32
var spring: SpringArm3D = null
var dragging: bool = false

func _ready() -> void:
    spring = get_node_or_null("SpringArm3D") as SpringArm3D
    if spring:
        spring.spring_length = 6.0
        spring.margin = 0.3

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        dragging = event.pressed
    elif event is InputEventMouseMotion and dragging:
        _rotate_by(event.relative)
    elif event is InputEventScreenTouch:
        dragging = event.pressed
    elif event is InputEventScreenDrag:
        _rotate_by(event.relative * 1.6)

func _rotate_by(relative: Vector2) -> void:
    yaw -= relative.x * drag_sensitivity * SettingsManager.touch_sensitivity
    pitch = clampf(pitch + relative.y * drag_sensitivity * SettingsManager.touch_sensitivity, pitch_min, pitch_max)
    rotation.y = yaw
    if spring:
        spring.rotation.x = -pitch

func snap_behind_player() -> void:
    yaw = 0.0
    pitch = 0.32
    rotation.y = yaw
    if spring:
        spring.rotation.x = -pitch
