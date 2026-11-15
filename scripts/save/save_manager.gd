extends Node
## SaveManager — JSON save/load to user://savegame.json, with versioning.
const SAVE_PATH := "user://savegame.json"

func save_game() -> bool:
    var data_script: Script = load("res://scripts/save/save_data.gd")
    var data: RefCounted = data_script.new()
    var gm: Node = get_node_or_null("/root/GameManager")
    if gm and gm.player:
        data.player_position = gm.player.global_position
    data.play_time_seconds = gm.play_time_seconds if gm else 0.0
    var xp_node: Node = get_tree().current_scene.find_child("ExperienceSystem", true, false) if get_tree().current_scene else null
    if xp_node:
        data.level = xp_node.level
        data.xp = xp_node.xp
    var inv: Node = get_tree().current_scene.find_child("InventorySystem", true, false) if get_tree().current_scene else null
    if inv:
        data.inventory = inv.to_dict()
    var qm: Node = get_tree().current_scene.find_child("QuestManager", true, false) if get_tree().current_scene else null
    if qm:
        data.completed_quests = qm.completed.duplicate()
    var json_text: String = JSON.stringify(data.to_dict(), "  ")
    var file: FileAccess = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
    if file == null:
        push_error("SaveManager: cannot write " + SAVE_PATH)
        return false
    file.store_string(json_text)
    file.close()
    return true

func load_game() -> Dictionary:
    if not FileAccess.file_exists(SAVE_PATH):
        return {}
    var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
    if parsed == null:
        return {}
    return parsed as Dictionary

func has_save() -> bool:
    return FileAccess.file_exists(SAVE_PATH)
