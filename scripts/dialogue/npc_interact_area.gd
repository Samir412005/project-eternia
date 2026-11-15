extends Area3D
class_name VillagerInteractArea
## VillagerInteractArea — the green villager NPC's interactable zone.
## Mirrors scripts/gameplay/shrine.gd: an Area3D in group "interactable"
## with an interact() that PlayerInteraction calls when the player is in
## range and presses E (the "interact" action).
##
## interact() opens the villager's Dialogue Manager dialogue
## (scripts/dialogue/villager_dialogue.dialogue) in a
## VillagerDialogueBalloon, passing the current scene as an extra game
## state so the dialogue's `do start_golem_quest()` mutation resolves
## to AetheriaSlice.start_golem_quest(). Emits
## DialogueManager.dialogue_started so the slice can freeze the player
## while the balloon is open. A second interact() while the balloon is
## open is ignored — the balloon itself handles advancing.
## If the .dialogue file has no import data yet (fresh checkout), falls
## back to DialogueManager.create_resource_from_text() on the file text.

const DIALOGUE_PATH := "res://scripts/dialogue/villager_dialogue.dialogue"
const BALLOON_SCRIPT_PATH := "res://scripts/dialogue/dialogue_balloon.gd"

var _balloon: CanvasLayer = null


func _ready() -> void:
	monitoring = true
	monitorable = true
	add_to_group("interactable")


func interact() -> CanvasLayer:
	if _balloon != null and is_instance_valid(_balloon) and bool(_balloon.get("is_open")):
		return _balloon
	var resource := _load_dialogue_resource()
	if resource == null:
		push_error("VillagerInteractArea: could not load " + DIALOGUE_PATH)
		return null
	# Created via load() + .new(), not via the global class name, so
	# this never depends on the editor's global-script-class cache.
	var balloon_script: Script = load(BALLOON_SCRIPT_PATH)
	_balloon = balloon_script.new()
	var scene: Node = get_tree().current_scene
	if scene == null:
		push_error("VillagerInteractArea: no current scene for the dialogue balloon")
		return null
	scene.add_child(_balloon)
	var extra: Array = []
	if scene.has_method("start_golem_quest"):
		extra = [scene]
	_balloon.call("start", resource, "start", extra)
	DialogueManager.dialogue_started.emit(resource)
	print("[AETHERIA-DIALOGUE] villager dialogue opened")
	return _balloon


func _load_dialogue_resource() -> DialogueResource:
	var loaded: Resource = load(DIALOGUE_PATH)
	if loaded is DialogueResource:
		return loaded as DialogueResource
	var text: String = FileAccess.get_file_as_string(DIALOGUE_PATH)
	if text.is_empty():
		return null
	var created: Resource = DialogueManager.create_resource_from_text(text)
	if created is DialogueResource:
		return created as DialogueResource
	return null
