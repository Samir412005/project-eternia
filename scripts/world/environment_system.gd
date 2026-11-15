extends Node
## EnvironmentSystem — fog + sky tuning for the valley (Mobile-safe).
var fog_density: float = 0.012

func _ready() -> void:
    var cs: Node = get_tree().current_scene
    if cs == null:
        return
    var env: WorldEnvironment = cs.find_child("WorldEnvironment", true, false) as WorldEnvironment
    if env and env.environment:
        env.environment.fog_enabled = true
        env.environment.fog_light_color = Color(0.65, 0.7, 0.8)
        env.environment.fog_density = fog_density
