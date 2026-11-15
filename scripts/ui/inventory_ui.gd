extends Control
## InventoryUI — lists real InventorySystem contents.
var list_label: Label = null

func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.position = Vector2(380, 120)
    panel.size = Vector2(520, 480)
    add_child(panel)
    var title := Label.new()
    title.text = "INVENTORY"
    title.position = Vector2(420, 140)
    title.add_theme_font_size_override("font_size", 32)
    add_child(title)
    list_label = Label.new()
    list_label.position = Vector2(420, 190)
    list_label.size = Vector2(440, 340)
    add_child(list_label)
    var close_btn := Button.new()
    close_btn.text = "CLOSE"
    close_btn.position = Vector2(560, 540)
    close_btn.size = Vector2(160, 50)
    close_btn.pressed.connect(func() -> void: visible = false)
    add_child(close_btn)

func toggle_visible() -> void:
    visible = not visible
    if visible:
        _refresh()

func _refresh() -> void:
    var scene: Node = get_tree().current_scene
    var inv: Node = scene.find_child("InventorySystem", true, false)
    if inv == null or inv.items.is_empty():
        list_label.text = "Empty — visit the shrine or defeat the dummy."
        return
    var lines: Array = []
    for k in inv.items.keys():
        lines.append("%s  x%d" % [str(k), int(inv.items[k])])
    list_label.text = "
".join(lines)
