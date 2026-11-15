extends GdUnitTestSuite
## Smoke test (gdUnit4 5.1.1 on Godot 4.3): proves the test runner works by
## loading the project's real data files and asserting known values.
## Note: Godot parses JSON numbers as float, so int(...) the values first.

func _load_json(path: String) -> Dictionary:
	var text := FileAccess.get_file_as_string(path)
	assert_str(text).is_not_empty()
	var parsed: Variant = JSON.parse_string(text)
	assert_bool(parsed is Dictionary).is_true()
	return parsed

func test_quests_data_loads() -> void:
	var quests := _load_json("res://data/quests/quests.json")
	assert_bool(quests.has("first_light")).is_true()
	assert_int(int(quests["first_light"]["reward_xp"])).is_equal(50)

func test_golem_quest_data_loads() -> void:
	var quests := _load_json("res://data/quests/quests.json")
	assert_bool(quests.has("golem_quest")).is_true()
	assert_int(int(quests["golem_quest"]["reward_xp"])).is_equal(100)
	assert_bool((quests["golem_quest"]["objectives"] as Array).has("Defeat the rock golem")).is_true()

func test_items_data_loads() -> void:
	var items := _load_json("res://data/items/items.json")
	assert_bool(items.has("iron_sword")).is_true()
	assert_int(int(items["iron_sword"]["attack"])).is_equal(8)
	assert_bool(items.has("health_potion")).is_true()
