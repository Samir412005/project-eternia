extends CanvasLayer
## MobileHUD — top bar, joystick, action buttons, toast, FPS.
## Builds its controls in code so the layout is reviewable in one file.
var player: Node = null
var joy: Control = null
var hp_label: Label = null
var level_label: Label = null
var xp_label: Label = null
var toast_label: Label = null
var interact_button: Button = null
var fps_label: Label = null
var _toast_timer: float = 0.0

func _ready() -> void:
    layer = 10
    _build_top_bar()
    _build_joystick()
    _build_buttons()
    _build_toast()
    EventBus.xp_gained.connect(_on_xp)
    EventBus.level_up.connect(_on_level_up)
    EventBus.interactable_nearby.connect(_on_interactable)
    EventBus.toast_requested.connect(show_toast)
    EventBus.player_health_changed.connect(_on_health)

func _process(delta: float) -> void:
    if _toast_timer > 0.0:
        _toast_timer -= delta
        if _toast_timer <= 0.0:
            toast_label.visible = false
    if SettingsManager.show_fps and fps_label:
        fps_label.text = "FPS %d" % Engine.get_frames_per_second()

func _btn(text: String, pos: Vector2, size: Vector2) -> Button:
    var b := Button.new()
    b.text = text
    b.position = pos
    b.size = size
    b.focus_mode = Control.FOCUS_NONE
    add_child(b)
    return b

func _build_top_bar() -> void:
    hp_label = Label.new()
    hp_label.text = "HP 180 / 180"
    hp_label.position = Vector2(16, 12)
    hp_label.add_theme_font_size_override("font_size", 20)
    add_child(hp_label)
    level_label = Label.new()
    level_label.text = "Lv 1"
    level_label.position = Vector2(16, 40)
    level_label.add_theme_font_size_override("font_size", 20)
    add_child(level_label)
    xp_label = Label.new()
    xp_label.text = "XP 0 / 100"
    xp_label.position = Vector2(16, 68)
    xp_label.add_theme_font_size_override("font_size", 16)
    add_child(xp_label)
    fps_label = Label.new()
    fps_label.text = ""
    fps_label.position = Vector2(16, 96)
    add_child(fps_label)
    var pause_btn: Button = _btn("II", Vector2(1190, 12), Vector2(76, 56))
    pause_btn.pressed.connect(_on_pause_pressed)
    var inv_btn: Button = _btn("Bag", Vector2(1100, 12), Vector2(76, 56))
    inv_btn.pressed.connect(func() -> void: get_node_or_null("InventoryUI").toggle_visible())
    var quest_btn: Button = _btn("Quests", Vector2(1000, 12), Vector2(86, 56))
    quest_btn.pressed.connect(func() -> void: get_node_or_null("QuestUI").toggle_visible())

func _build_joystick() -> void:
    var script: Script = load("res://scripts/ui/virtual_joystick.gd")
    joy = Control.new()
    joy.set_script(script)
    joy.position = Vector2(24, 520)
    joy.size = Vector2(170, 170)
    add_child(joy)
    joy.vector_changed.connect(_on_joy)

func _build_buttons() -> void:
    var jump_btn: Button = _btn("JUMP", Vector2(1100, 560), Vector2(150, 110))
    jump_btn.button_down.connect(func() -> void: Input.action_press("jump"))
    jump_btn.button_up.connect(func() -> void: Input.action_release("jump"))
    var run_btn: Button = _btn("RUN", Vector2(940, 600), Vector2(130, 70))
    run_btn.button_down.connect(func() -> void: _set_run(true))
    run_btn.button_up.connect(func() -> void: _set_run(false))
    interact_button = _btn("USE", Vector2(940, 500), Vector2(130, 70))
    interact_button.disabled = true
    interact_button.pressed.connect(func() -> void: Input.action_press("interact"))
    var atk_btn: Button = _btn("ATTACK", Vector2(1110, 440), Vector2(150, 70))
    atk_btn.pressed.connect(func() -> void: Input.action_press("attack"))

func _build_toast() -> void:
    toast_label = Label.new()
    toast_label.position = Vector2(340, 640)
    toast_label.size = Vector2(600, 40)
    toast_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    toast_label.add_theme_font_size_override("font_size", 22)
    toast_label.visible = false
    add_child(toast_label)

func _on_joy(v: Vector2) -> void:
    if GameManager.player:
        GameManager.player.joystick_vector = v

func _set_run(v: bool) -> void:
    if GameManager.player:
        GameManager.player.set_run_held(v)

func _on_pause_pressed() -> void:
    GameManager.toggle_pause()

func _on_xp(_amount: int) -> void:
    var cs: Node = get_tree().current_scene
    if cs == null:
        return
    var xp_node: Node = cs.find_child("ExperienceSystem", true, false)
    if xp_node:
        xp_label.text = "XP %d / %d" % [xp_node.xp, xp_node.xp_to_next]

func _on_level_up(new_level: int) -> void:
    level_label.text = "Lv %d" % new_level
    show_toast("Level up! You are now level %d." % new_level)

func _on_health(current: int, maximum: int) -> void:
    hp_label.text = "HP %d / %d" % [current, maximum]

func _on_interactable(_name: String, available: bool) -> void:
    if interact_button:
        interact_button.disabled = not available

func show_toast(message: String) -> void:
    toast_label.text = message
    toast_label.visible = true
    _toast_timer = 4.0
