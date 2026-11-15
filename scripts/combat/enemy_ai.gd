extends CharacterBody3D
## EnemyAI — training dummy that chases the player inside 12 m and
## attacks inside 2 m. Real physics body, real HP.
@export var max_health: int = 40
@export var move_speed: float = 2.2
@export var aggro_range: float = 12.0
@export var attack_range: float = 2.0
@export var attack_damage: int = 5

var health: int = 40
var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity") as float
var _attack_timer: float = 0.0
var _respawn_pos: Vector3 = Vector3.ZERO

func _ready() -> void:
    add_to_group("enemy")
    health = max_health
    _respawn_pos = global_position

func _physics_process(delta: float) -> void:
    var player: Node3D = get_tree().get_first_node_in_group("player") as Node3D
    if player == null or not is_on_floor():
        if not is_on_floor():
            velocity.y -= gravity * delta
        move_and_slide()
        return
    var to_player: Vector3 = player.global_position - global_position
    to_player.y = 0.0
    var dist: float = to_player.length()
    _attack_timer = maxf(0.0, _attack_timer - delta)
    if dist < aggro_range and dist > attack_range:
        var dir: Vector3 = to_player.normalized()
        velocity.x = dir.x * move_speed
        velocity.z = dir.z * move_speed
        rotation.y = lerp_angle(rotation.y, atan2(-dir.x, -dir.z), minf(1.0, 8.0 * delta))
    else:
        velocity.x = move_toward(velocity.x, 0.0, 10.0 * delta)
        velocity.z = move_toward(velocity.z, 0.0, 10.0 * delta)
        if dist <= attack_range and _attack_timer <= 0.0:
            _attack_timer = 1.2
    if not is_on_floor():
        velocity.y -= gravity * delta
    else:
        velocity.y = -0.5
    move_and_slide()

func take_damage(amount: int) -> void:
    health -= amount
    if health <= 0:
        EventBus.enemy_defeated.emit(str(name))
        health = max_health
        global_position = _respawn_pos
        velocity = Vector3.ZERO
