extends Area3D
## AncientShrine — the slice's one interactive world object.
## First interaction: +50 XP, shrine loot, intro dialogue, quest progress.
## Re-interaction: +10 XP only (no farming of the full reward).
var used: bool = false
var quest_manager: Node = null
var xp_system: Node = null
var loot: Node = null
var dialogue: Node = null

func _ready() -> void:
    monitoring = true
    monitorable = true

func interact() -> void:
    _resolve_nodes()
    if not used:
        used = true
        if xp_system:
            xp_system.add_xp(50)
        if loot:
            loot.grant("shrine_blessing")
        if dialogue:
            dialogue.start_dialogue("intro")
        if quest_manager:
            quest_manager.complete_objective("first_light", 0)
            quest_manager.complete_objective("first_light", 1)
        EventBus.toast_requested.emit("The shrine blesses you: +50 XP, potions found.")
    else:
        if xp_system:
            xp_system.add_xp(10)
        EventBus.toast_requested.emit("The shrine hums quietly. +10 XP.")

func _resolve_nodes() -> void:
    var scene: Node = get_tree().current_scene
    if scene == null:
        return
    quest_manager = scene.find_child("QuestManager", true, false)
    xp_system = scene.find_child("ExperienceSystem", true, false)
    loot = scene.find_child("LootSystem", true, false)
    dialogue = scene.find_child("DialogueSystem", true, false)
