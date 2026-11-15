extends Control
## SettingsUI — quality presets only in Phase 1 (audio sliders: Phase 2).
func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.position = Vector2(440, 180)
    panel.size = Vector2(400, 360)
    add_child(panel)
    var title := Label.new()
    title.text = "SETTINGS"
    title.position = Vector2(480, 200)
    title.add_theme_font_size_override("font_size", 32)
    add_child(title)
    var low_btn := Button.new()
    low_btn.text = "Quality: LOW"
    low_btn.position = Vector2(480, 260)
    low_btn.size = Vector2(320, 50)
    low_btn.pressed.connect(func() -> void: SettingsManager.set_quality(0))
    add_child(low_btn)
    var med_btn := Button.new()
    med_btn.text = "Quality: MEDIUM"
    med_btn.position = Vector2(480, 320)
    med_btn.size = Vector2(320, 50)
    med_btn.pressed.connect(func() -> void: SettingsManager.set_quality(1))
    add_child(med_btn)
    var high_btn := Button.new()
    high_btn.text = "Quality: HIGH"
    high_btn.position = Vector2(480, 380)
    high_btn.size = Vector2(320, 50)
    high_btn.pressed.connect(func() -> void: SettingsManager.set_quality(2))
    add_child(high_btn)
    var close_btn := Button.new()
    close_btn.text = "CLOSE"
    close_btn.position = Vector2(480, 450)
    close_btn.size = Vector2(320, 50)
    close_btn.pressed.connect(func() -> void: visible = false)
    add_child(close_btn)

func toggle_visible() -> void:
    visible = not visible
