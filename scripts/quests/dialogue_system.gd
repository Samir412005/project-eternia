extends Node
## DialogueSystem — line-by-line dialogue from data/dialogue/*.json.
var current_lines: Array = []
var current_index: int = 0
var current_speaker: String = ""
var active: bool = false

func start_dialogue(dialogue_id: String) -> bool:
    var path: String = "res://data/dialogue/" + dialogue_id + ".json"
    if not FileAccess.file_exists(path):
        return false
    var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
    if parsed == null:
        return false
    var d: Dictionary = parsed
    current_speaker = str(d.get("speaker", ""))
    current_lines = d.get("lines", [])
    current_index = 0
    active = true
    EventBus.dialogue_started.emit(current_speaker)
    return true

func current_line() -> String:
    if current_index < current_lines.size():
        return str(current_lines[current_index])
    return ""

func advance() -> bool:
    current_index += 1
    if current_index >= current_lines.size():
        active = false
        EventBus.dialogue_finished.emit()
        return false
    return true
