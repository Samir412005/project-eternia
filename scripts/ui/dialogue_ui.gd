extends Control
## DialogueUI — bottom dialogue box driven by DialogueSystem.
var speaker_label: Label = null
var line_label: Label = null
var dialogue: Node = null

func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.position = Vector2(240, 500)
    panel.size = Vector2(800, 170)
    add_child(panel)
    speaker_label = Label.new()
    speaker_label.position = Vector2(270, 515)
    speaker_label.add_theme_font_size_override("font_size", 20)
    add_child(speaker_label)
    line_label = Label.new()
    line_label.position = Vector2(270, 550)
    line_label.size = Vector2(740, 60)
    line_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    line_label.add_theme_font_size_override("font_size", 20)
    add_child(line_label)
    var next_btn := Button.new()
    next_btn.text = "CONTINUE  >"
    next_btn.position = Vector2(860, 625)
    next_btn.size = Vector2(150, 36)
    next_btn.pressed.connect(_on_next)
    add_child(next_btn)
    EventBus.dialogue_started.connect(_on_started)
    EventBus.dialogue_finished.connect(func() -> void: visible = false)

func _on_started(speaker: String) -> void:
    dialogue = get_tree().current_scene.find_child("DialogueSystem", true, false)
    speaker_label.text = speaker
    line_label.text = dialogue.current_line() if dialogue else ""
    visible = true

func _on_next() -> void:
    if dialogue == null:
        return
    if dialogue.advance():
        line_label.text = dialogue.current_line()
