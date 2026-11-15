extends SceneTree
## Automated validation for Phase 1. Run:
##   godot --headless --path . -s tests/run_tests.gd
## Prints TEST PASS/FAIL lines and quits with 0 (all pass) or 1.
var passed: int = 0
var failed: int = 0
var failures: Array = []

func _init() -> void:
    call_deferred("_run")

func _check(test_name: String, ok: bool, detail: String = "") -> void:
    if ok:
        passed += 1
        print("TEST PASS " + test_name)
    else:
        failed += 1
        failures.append(test_name)
        print("TEST FAIL " + test_name + (" — " + detail if detail != "" else ""))

func _run() -> void:
    # 1. Main scene loads and instantiates.
    var main_scene: PackedScene = load("res://scenes/main/main.tscn")
    _check("main_scene_loads", main_scene != null)
    var main_inst: Node = null
    if main_scene:
        main_inst = main_scene.instantiate()
        root.add_child(main_inst)
    _check("main_instantiates", main_inst != null)
    # 2. Key nodes exist.
    if main_inst:
        _check("player_exists", main_inst.find_child("Player", true, false) != null)
        _check("world_exists", main_inst.find_child("World", true, false) != null)
        _check("shrine_exists", main_inst.find_child("AncientShrine", true, false) != null)
        _check("hud_exists", main_inst.find_child("HUD", true, false) != null)
        _check("camera_exists", main_inst.find_child("Camera3D", true, false) != null)
        var world: Node = main_inst.find_child("World", true, false)
        _check("world_has_content", world != null and world.get_child_count() >= 10, "children=" + str(world.get_child_count() if world else -1))
        var player: Node = main_inst.find_child("Player", true, false)
        if player:
            _check("player_speeds_sane", player.walk_speed > 0.0 and player.run_speed > player.walk_speed and player.jump_velocity > 0.0)
            _check("player_gravity_set", player.gravity > 0.0)
    # 3. Player scene loads alone.
    var pscene: PackedScene = load("res://scenes/player/player.tscn")
    _check("player_scene_loads", pscene != null)
    # 4. Inventory system.
    var inv_script: Script = load("res://scripts/rpg/inventory_system.gd")
    var inv: Node = Node.new()
    inv.set_script(inv_script)
    root.add_child(inv)
    _check("inventory_add", inv.add_item("health_potion", 2) and inv.count("health_potion") == 2)
    _check("inventory_remove", inv.remove_item("health_potion", 1) and inv.count("health_potion") == 1)
    _check("inventory_reject_overdraw", not inv.remove_item("health_potion", 99))
    # 5. Experience / level-up curve.
    var xp_script: Script = load("res://scripts/rpg/experience_system.gd")
    var xp_node: Node = Node.new()
    xp_node.set_script(xp_script)
    root.add_child(xp_node)
    xp_node.add_xp(50)
    _check("xp_accumulates", xp_node.xp == 50 and xp_node.level == 1)
    xp_node.add_xp(60)
    _check("level_up_works", xp_node.level == 2 and xp_node.xp == 10, "level=%d xp=%d" % [xp_node.level, xp_node.xp])
    # 6. Quest database + manager.
    var db_script: Script = load("res://scripts/quests/quest_database.gd")
    var db: Node = Node.new()
    db.set_script(db_script)
    root.add_child(db)
    _check("quest_db_loads", db.quests.has("first_light"))
    var qm_script: Script = load("res://scripts/quests/quest_manager.gd")
    var qm: Node = Node.new()
    qm.set_script(qm_script)
    root.add_child(qm)
    qm.database = db
    _check("quest_starts", qm.start_quest("first_light"))
    qm.complete_objective("first_light", 0)
    qm.complete_objective("first_light", 1)
    _check("quest_completes", qm.is_completed("first_light"))
    # 7. Save data round-trip (versioned).
    var sd_script: Script = load("res://scripts/save/save_data.gd")
    var sd: RefCounted = sd_script.new()
    sd.level = 3
    sd.xp = 42
    sd.inventory = {"old_coin": 5}
    sd.completed_quests = ["first_light"]
    var sd2: RefCounted = sd_script.new()
    _check("save_roundtrip", sd2.from_dict(sd.to_dict()) and sd2.level == 3 and sd2.xp == 42 and sd2.inventory.get("old_coin", 0) == 5)
    var sd_bad: RefCounted = sd_script.new()
    _check("save_rejects_bad_version", not sd_bad.from_dict({"version": 99}))
    # 8. All GDScript files parse (loadable).
    var bad: Array = []
    var dir: DirAccess = DirAccess.open("res://scripts")
    var stack: Array = ["res://scripts"]
    while not stack.is_empty():
        var dpath: String = stack.pop_back()
        var d: DirAccess = DirAccess.open(dpath)
        if d == null:
            continue
        d.list_dir_begin()
        var fname: String = d.get_next()
        while fname != "":
            var full: String = dpath + "/" + fname
            if d.current_is_dir() and not fname.begins_with("."):
                stack.append(full)
            elif fname.ends_with(".gd"):
                var s: Script = load(full)
                if s == null:
                    bad.append(full)
            fname = d.get_next()
        d.list_dir_end()
    _check("all_scripts_parse", bad.is_empty(), "bad=" + str(bad))
    print("TEST SUMMARY passed=%d failed=%d" % [passed, failed])
    if not failures.is_empty():
        print("TEST FAILURES: " + ", ".join(failures))
    quit(0 if failed == 0 else 1)
