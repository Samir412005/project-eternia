extends Node
## SceneManager — single place that changes scenes, with a fade hook.
## UNFINISHED: no loading screen / async streaming yet (see roadmap Phase 3).
var current_scene_path: String = "res://scenes/main/main.tscn"

func change_scene(path: String) -> void:
    current_scene_path = path
    var err: Error = get_tree().change_scene_to_file(path)
    if err != OK:
        push_error("SceneManager: failed to load " + path + " err=" + str(err))

func reload_current_scene() -> void:
    get_tree().reload_current_scene()
