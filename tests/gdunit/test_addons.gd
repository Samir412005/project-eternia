extends GdUnitTestSuite
## Addon smoke test (Godot 4.3): Beehave 2.9.2, Dialogue Manager 2.45.0,
## GUT 9.4.0 — proves each addon loads and its core class works headless.

func test_beehave_tree_instantiates() -> void:
	var tree := BeehaveTree.new()
	assert_object(tree).is_not_null()
	tree.free()

func test_gut_test_class_loads() -> void:
	var gut_script: GDScript = load("res://addons/gut/test.gd")
	assert_object(gut_script).is_not_null()

func test_dialogue_manager_autoload_and_line() -> void:
	assert_object(DialogueManager).is_not_null()
	var res: Resource = DialogueManager.create_resource_from_text("~ start\nEternia: Hello, traveller.\n")
	assert_object(res).is_not_null()
	var line: DialogueLine = await DialogueManager.get_next_dialogue_line(res, "start")
	assert_object(line).is_not_null()
	assert_str(line.text).is_equal("Hello, traveller.")
	assert_str(line.character).is_equal("Eternia")

func test_villager_dialogue_quest() -> void:
	# The slice's villager dialogue (scripts/dialogue/): Arabic quest
	# lines, start/accept/decline titles, first line is the greeting.
	var res: Resource = load("res://scripts/dialogue/villager_dialogue.dialogue")
	if not (res is DialogueResource):
		var text: String = FileAccess.get_file_as_string("res://scripts/dialogue/villager_dialogue.dialogue")
		res = DialogueManager.create_resource_from_text(text)
	assert_object(res).is_not_null()
	var titles: PackedStringArray = (res as DialogueResource).get_titles()
	assert_bool(titles.has("start")).is_true()
	assert_bool(titles.has("accept")).is_true()
	assert_bool(titles.has("decline")).is_true()
	var line: DialogueLine = await DialogueManager.get_next_dialogue_line(res, "start")
	assert_object(line).is_not_null()
	assert_str(line.character).is_equal("القروي")
	assert_bool(line.text.contains("إيثيريا")).is_true()
