extends Node
## PlayerStateMachine — IDLE / WALK / RUN / JUMP / FALL / INTERACT.
## Driven from PlayerController each physics frame; no behaviour is faked:
## the state is derived from real velocity / floor state.
const IDLE := "IDLE"
const WALK := "WALK"
const RUN := "RUN"
const JUMP := "JUMP"
const FALL := "FALL"
const INTERACT := "INTERACT"

var current_state: String = IDLE
var player: CharacterBody3D = null

func _ready() -> void:
    player = get_parent() as CharacterBody3D

func _physics_process(_delta: float) -> void:
    if player == null:
        return
    if not player.movement_enabled:
        _set_state(IDLE)
        return
    var speed: float = Vector2(player.velocity.x, player.velocity.z).length()
    var next: String = current_state
    if not player.is_on_floor():
        next = JUMP if player.velocity.y > 0.0 else FALL
    elif speed > 6.5:
        next = RUN
    elif speed > 0.4:
        next = WALK
    else:
        next = IDLE
    _set_state(next)

func _set_state(s: String) -> void:
    if s != current_state:
        current_state = s

func is_moving() -> bool:
    return current_state == WALK or current_state == RUN
