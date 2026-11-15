extends Node
## GameManager — top-level game state machine and session wiring.
## States: MENU, PLAYING, PAUSED, DIALOGUE, CINEMATIC.
const STATE_MENU := "MENU"
const STATE_PLAYING := "PLAYING"
const STATE_PAUSED := "PAUSED"
const STATE_DIALOGUE := "DIALOGUE"

var state: String = STATE_MENU
var player: Node = null
var play_time_seconds: float = 0.0
var is_new_game: bool = true

func _ready() -> void:
    process_mode = Node.PROCESS_MODE_ALWAYS

func _process(delta: float) -> void:
    if state == STATE_PLAYING:
        play_time_seconds += delta

func set_state(new_state: String) -> void:
    if new_state == state:
        return
    state = new_state
    EventBus.game_state_changed.emit(state)

func start_game() -> void:
    is_new_game = true
    play_time_seconds = 0.0
    set_state(STATE_PLAYING)
    EventBus.game_started.emit()

func toggle_pause() -> void:
    if state == STATE_PLAYING:
        get_tree().paused = true
        set_state(STATE_PAUSED)
        EventBus.game_paused.emit(true)
    elif state == STATE_PAUSED:
        get_tree().paused = false
        set_state(STATE_PLAYING)
        EventBus.game_paused.emit(false)

func return_to_menu() -> void:
    get_tree().paused = false
    set_state(STATE_MENU)

func register_player(p: Node) -> void:
    player = p
