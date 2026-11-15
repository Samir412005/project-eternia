extends CanvasLayer
class_name VillagerDialogueBalloon
## VillagerDialogueBalloon — the slice's dialogue balloon for
## Dialogue Manager 2.45.0 (Godot 4.3, Mobile renderer).
##
## Built entirely in code (no .tscn): bottom panel with the speaker name
## + line + response buttons, all in Noto Sans Arabic (the project's
## Arabic font) so the Arabic dialogue renders shaped and RTL.
## Text is shown instantly (no type-out): deterministic for screenshots.
## Advance: E (interact), Enter/Space (ui_accept), or left click.
## When the line offers responses, the buttons take the input instead.
## Closes itself at END and emits DialogueManager.dialogue_ended, which
## the slice listens to for un-freezing the player.

const FONT_REGULAR := "res://assets/library/fonts/noto-sans-arabic/NotoSansArabic-Regular.ttf"
const FONT_BOLD := "res://assets/library/fonts/noto-sans-arabic/NotoSansArabic-Bold.ttf"

var resource: DialogueResource = null
var dialogue_line: DialogueLine = null
var is_open: bool = false

var _game_states: Array = []
var _advancing: bool = false
var _panel: PanelContainer = null
var _name_label: Label = null
var _text_label: Label = null
var _hint_label: Label = null
var _responses_box: VBoxContainer = null


func _ready() -> void:
	layer = 10
	visible = false
	var regular: Font = load(FONT_REGULAR) as Font
	var bold: Font = load(FONT_BOLD) as Font
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.06, 0.11, 0.93)
	style.corner_radius_top_left = 14
	style.corner_radius_top_right = 14
	style.corner_radius_bottom_left = 14
	style.corner_radius_bottom_right = 14
	style.border_color = Color(0.85, 0.68, 0.30, 0.9)
	style.set_border_width_all(2)
	style.content_margin_left = 24
	style.content_margin_right = 24
	style.content_margin_top = 14
	style.content_margin_bottom = 14
	_panel = PanelContainer.new()
	_panel.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_panel.offset_left = 140
	_panel.offset_right = -140
	# 284 px tall: name (~30) + wrapped line (~70) + two response
	# buttons (2×46 + 8) + margins/separations (~50). The first
	# version used 192 px and the second response button rendered
	# below the viewport — verified in shot 13, fixed here.
	_panel.offset_top = -300
	_panel.offset_bottom = -16
	_panel.add_theme_stylebox_override("panel", style)
	add_child(_panel)
	var vbox := VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 6)
	_panel.add_child(vbox)
	_name_label = Label.new()
	_name_label.add_theme_font_override("font", bold)
	_name_label.add_theme_font_size_override("font_size", 24)
	_name_label.add_theme_color_override("font_color", Color(1.0, 0.85, 0.40))
	_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	vbox.add_child(_name_label)
	_text_label = Label.new()
	_text_label.add_theme_font_override("font", regular)
	_text_label.add_theme_font_size_override("font_size", 26)
	_text_label.add_theme_color_override("font_color", Color(1, 1, 1))
	_text_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_text_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_text_label.custom_minimum_size = Vector2(0, 64)
	vbox.add_child(_text_label)
	_responses_box = VBoxContainer.new()
	_responses_box.add_theme_constant_override("separation", 8)
	_responses_box.visible = false
	vbox.add_child(_responses_box)
	_hint_label = Label.new()
	_hint_label.add_theme_font_override("font", regular)
	_hint_label.add_theme_font_size_override("font_size", 18)
	_hint_label.add_theme_color_override("font_color", Color(0.75, 0.75, 0.78))
	_hint_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_hint_label.text = "اضغط E للمتابعة"
	vbox.add_child(_hint_label)


func start(res: DialogueResource, title: String, extra_game_states: Array = []) -> void:
	resource = res
	_game_states = [self] + extra_game_states
	is_open = true
	visible = true
	dialogue_line = await resource.get_next_dialogue_line(title, _game_states)
	_show_line(dialogue_line)


func advance_dialogue() -> void:
	if not is_open or _advancing or dialogue_line == null:
		return
	if not dialogue_line.responses.is_empty():
		return
	_advancing = true
	dialogue_line = await resource.get_next_dialogue_line(dialogue_line.next_id, _game_states)
	_advancing = false
	_show_line(dialogue_line)


## Headless/test helper: pick a response by index (same as clicking it).
func select_response(index: int) -> void:
	if not is_open or dialogue_line == null:
		return
	if index < 0 or index >= dialogue_line.responses.size():
		return
	_on_response_selected(dialogue_line.responses[index])


func current_text() -> String:
	return _text_label.text if _text_label else ""


func _input(event: InputEvent) -> void:
	if not is_open:
		return
	if dialogue_line != null and not dialogue_line.responses.is_empty():
		return
	var advance := false
	if event is InputEventMouseButton:
		var mb := event as InputEventMouseButton
		advance = mb.button_index == MOUSE_BUTTON_LEFT and mb.pressed
	elif event.is_action_pressed("interact") or event.is_action_pressed("ui_accept"):
		advance = true
	if advance:
		get_viewport().set_input_as_handled()
		advance_dialogue()


func _show_line(line: DialogueLine) -> void:
	if line == null:
		close()
		return
	dialogue_line = line
	_name_label.text = line.character
	_text_label.text = line.text
	for child: Node in _responses_box.get_children():
		child.queue_free()
	_responses_box.visible = not line.responses.is_empty()
	_hint_label.visible = line.responses.is_empty()
	if not line.responses.is_empty():
		var regular: Font = load(FONT_REGULAR) as Font
		for i: int in range(line.responses.size()):
			var response: DialogueResponse = line.responses[i]
			if not response.is_allowed:
				continue
			var button := Button.new()
			button.text = response.text
			button.add_theme_font_override("font", regular)
			button.add_theme_font_size_override("font_size", 24)
			button.custom_minimum_size = Vector2(0, 46)
			button.pressed.connect(_on_response_selected.bind(response))
			_responses_box.add_child(button)
		var first: Button = _responses_box.get_child(0) as Button
		if first:
			first.grab_focus()


func _on_response_selected(response: DialogueResponse) -> void:
	if not is_open or _advancing:
		return
	_advancing = true
	dialogue_line = await resource.get_next_dialogue_line(response.next_id, _game_states)
	_advancing = false
	_show_line(dialogue_line)


func close() -> void:
	if not is_open:
		return
	is_open = false
	visible = false
	DialogueManager.dialogue_ended.emit(resource)
	queue_free()
