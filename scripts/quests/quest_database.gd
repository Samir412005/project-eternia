extends Node
## QuestDatabase — loads data/quests/quests.json once, serves lookups.
var quests: Dictionary = {}

func _ready() -> void:
    load_quests()

func load_quests() -> bool:
    var path: String = "res://data/quests/quests.json"
    if not FileAccess.file_exists(path):
        push_error("QuestDatabase: missing " + path)
        return false
    var text: String = FileAccess.get_file_as_string(path)
    var parsed: Variant = JSON.parse_string(text)
    if parsed == null:
        push_error("QuestDatabase: invalid JSON in " + path)
        return false
    quests = parsed as Dictionary
    return true

func get_quest(quest_id: String) -> Dictionary:
    return quests.get(quest_id, {}) as Dictionary
