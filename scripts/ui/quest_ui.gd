extends Control
## QuestUI — active + completed quests from QuestManager + database.
var list_label: Label = null

func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.position = Vector2(380, 120)
    panel.size = Vector2(520, 480)
    add_child(panel)
    var title := Label.new()
    title.text = "QUESTS"
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
    var qm: Node = scene.find_child("QuestManager", true, false)
    if qm == null:
        list_label.text = "No quest system."
        return
    var lines: Array = []
    for qid in qm.active.keys():
        var q: Dictionary = qm.database.get_quest(qid) if qm.database else {}
        lines.append("ACTIVE: " + str(q.get("title", qid)))
    for qid in qm.completed:
        var q2: Dictionary = qm.database.get_quest(qid) if qm.database else {}
        lines.append("DONE: " + str(q2.get("title", qid)))
    list_label.text = "
".join(lines) if not lines.is_empty() else "No quests yet — press NEW GAME."
