extends Node
## QuestManager — active/completed quests, objective progress.
## Quest 1 ("first_light") is completable in the slice: visit the shrine.
var active: Dictionary = {}
var completed: Array = []
var database: Node = null

func _ready() -> void:
    database = get_node_or_null("/root/QuestDatabase")
    if database == null:
        var script: Script = load("res://scripts/quests/quest_database.gd")
        database = Node.new()
        database.set_script(script)
        database.name = "QuestDatabase"
        get_tree().root.add_child.call_deferred(database)

func start_quest(quest_id: String) -> bool:
    if active.has(quest_id) or completed.has(quest_id):
        return false
    active[quest_id] = {"objectives_done": [], "started_at": Time.get_unix_time_from_system()}
    EventBus.quest_started.emit(quest_id)
    return true

func complete_objective(quest_id: String, objective_index: int) -> void:
    if not active.has(quest_id):
        return
    var done: Array = active[quest_id]["objectives_done"]
    if not done.has(objective_index):
        done.append(objective_index)
    EventBus.quest_updated.emit(quest_id, objective_index)
    var quest: Dictionary = database.get_quest(quest_id) if database else {}
    var total: int = int((quest.get("objectives", []) as Array).size())
    if total > 0 and done.size() >= total:
        _complete_quest(quest_id)

func _complete_quest(quest_id: String) -> void:
    active.erase(quest_id)
    completed.append(quest_id)
    EventBus.quest_completed.emit(quest_id)

func is_completed(quest_id: String) -> bool:
    return completed.has(quest_id)
