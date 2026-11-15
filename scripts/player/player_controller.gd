extends CharacterBody3D
## PlayerController — third-person CharacterBody3D.
## Walk / run / jump / gravity / ground detection. Camera-relative movement.
## Prototype mesh: primitive humanoid (see player_animation_controller.gd).
@export var walk_speed: float = 4.5
@export var run_speed: float = 8.0
@export var jump_velocity: float = 7.5
@export var acceleration: float = 14.0
@export var rotation_speed: float = 12.0

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity") as float
var joystick_vector: Vector2 = Vector2.ZERO
var run_held: bool = false
var movement_enabled: bool = false
var current_speed: float = 0.0
var camera_yaw_node: Node3D = null
var was_on_floor: bool = true

func _ready() -> void:
    add_to_group("player")
    floor_snap_length = 0.3
    floor_max_angle = deg_to_rad(50.0)

func _physics_process(delta: float) -> void:
    if not movement_enabled:
        velocity.x = move_toward(velocity.x, 0.0, acceleration * delta)
        velocity.z = move_toward(velocity.z, 0.0, acceleration * delta)
        _apply_gravity(delta)
        move_and_slide()
        return
    var input_vec: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    if joystick_vector.length() > 0.08:
        input_vec = joystick_vector
    var yaw: float = 0.0
    if camera_yaw_node != null:
        yaw = camera_yaw_node.rotation.y
    var forward: Vector3 = Vector3(-sin(yaw), 0.0, -cos(yaw))
    var right: Vector3 = Vector3(cos(yaw), 0.0, -sin(yaw))
    var wish_dir: Vector3 = (right * input_vec.x + forward * -input_vec.y)
    wish_dir.y = 0.0
    if wish_dir.length() > 1.0:
        wish_dir = wish_dir.normalized()
    var target_speed: float = run_speed if (run_held or Input.is_action_pressed("run")) else walk_speed
    if wish_dir.length() < 0.08:
        target_speed = 0.0
    var target_vel: Vector3 = wish_dir * target_speed
    velocity.x = move_toward(velocity.x, target_vel.x, acceleration * delta)
    velocity.z = move_toward(velocity.z, target_vel.z, acceleration * delta)
    current_speed = Vector2(velocity.x, velocity.z).length()
    if wish_dir.length() > 0.1:
        var target_yaw: float = atan2(-wish_dir.x, -wish_dir.z)
        rotation.y = lerp_angle(rotation.y, target_yaw, minf(1.0, rotation_speed * delta))
    _apply_gravity(delta)
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity
    var on_floor_now: bool = is_on_floor()
    if on_floor_now and not was_on_floor:
        pass
    was_on_floor = on_floor_now
    move_and_slide()
    if is_on_floor() or is_on_wall():
        EventBus.player_moved.emit(global_position)

func _apply_gravity(delta: float) -> void:
    if not is_on_floor():
        velocity.y -= gravity * delta
    elif velocity.y < 0.0:
        velocity.y = -0.5

func set_run_held(v: bool) -> void:
    run_held = v

func teleport_to(pos: Vector3) -> void:
    global_position = pos
    velocity = Vector3.ZERO
