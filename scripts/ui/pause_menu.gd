extends Control
## PauseMenu — Resume / Save / Quit to menu. Game is actually paused.
func _ready() -> void:
    process_mode = Node.PROCESS_MODE_ALWAYS
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.set_anchors_preset(Control.PRESET_FULL_RECT)
    var style := StyleBoxFlat.new()
    style.bg_color = Color(0.02, 0.02, 0.05, 0.85)
    panel.add_theme_stylebox_override("panel", style)
    add_child(panel)
    var title := Label.new()
    title.text = "PAUSED"
    title.position = Vector2(580, 160)
    title.add_theme_font_size_override("font_size", 48)
    add_child(title)
    var resume_btn := Button.new()
    resume_btn.text = "RESUME"
    resume_btn.position = Vector2(540, 260)
    resume_btn.size = Vector2(200, 60)
    resume_btn.pressed.connect(func() -> void: GameManager.toggle_pause())
    add_child(resume_btn)
    var save_btn := Button.new()
    save_btn.text = "SAVE GAME"
    save_btn.position = Vector2(540, 335)
    save_btn.size = Vector2(200, 60)
    save_btn.pressed.connect(_on_save)
    add_child(save_btn)
    var quit_btn := Button.new()
    quit_btn.text = "QUIT TO MENU"
    quit_btn.position = Vector2(540, 410)
    quit_btn.size = Vector2(200, 60)
    quit_btn.pressed.connect(_on_quit)
    add_child(quit_btn)
    EventBus.game_paused.connect(func(paused: bool) -> void: visible = paused)

func _on_save() -> void:
    if SaveManager.save_game():
        EventBus.toast_requested.emit("Game saved.")
    else:
        EventBus.toast_requested.emit("Save failed.")

func _on_quit() -> void:
    if GameManager.player:
        GameManager.player.movement_enabled = false
    GameManager.return_to_menu()
