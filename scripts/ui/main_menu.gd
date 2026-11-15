extends Control
## MainMenu — title, New Game, Continue (if a save exists), quality note.
func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    var panel := Panel.new()
    panel.set_anchors_preset(Control.PRESET_FULL_RECT)
    var style := StyleBoxFlat.new()
    style.bg_color = Color(0.04, 0.05, 0.09, 0.92)
    panel.add_theme_stylebox_override("panel", style)
    add_child(panel)
    var title := Label.new()
    title.text = "PROJECT ETERNIA"
    title.set_anchors_preset(Control.PRESET_CENTER_TOP)
    title.position = Vector2(390, 140)
    title.add_theme_font_size_override("font_size", 64)
    add_child(title)
    var sub := Label.new()
    sub.text = "A 3D RPG  -  Phase 1 vertical slice"
    sub.position = Vector2(470, 220)
    sub.add_theme_font_size_override("font_size", 22)
    add_child(sub)
    var start_btn := Button.new()
    start_btn.text = "NEW GAME"
    start_btn.position = Vector2(540, 320)
    start_btn.size = Vector2(200, 64)
    start_btn.pressed.connect(_on_start)
    add_child(start_btn)
    var cont_btn := Button.new()
    cont_btn.text = "CONTINUE"
    cont_btn.position = Vector2(540, 400)
    cont_btn.size = Vector2(200, 64)
    cont_btn.disabled = not SaveManager.has_save()
    cont_btn.pressed.connect(_on_start)
    add_child(cont_btn)
    var note := Label.new()
    note.text = "Prototype art only — real systems, real 3D scene."
    note.position = Vector2(460, 500)
    add_child(note)
    EventBus.game_state_changed.connect(_on_state)
    visible = GameManager.state == GameManager.STATE_MENU

func _on_state(new_state: String) -> void:
    visible = new_state == GameManager.STATE_MENU

func _on_start() -> void:
    GameManager.start_game()
    var scene: Node = get_tree().current_scene
    var qm: Node = scene.find_child("QuestManager", true, false)
    if qm:
        qm.start_quest("first_light")
    var p: Node = GameManager.player
    if p:
        p.movement_enabled = true
