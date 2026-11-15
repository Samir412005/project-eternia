extends Node
## LevelProgression — attribute points awarded per level (2 per level).
var pending_points: int = 0

func _ready() -> void:
    EventBus.level_up.connect(_on_level_up)

func _on_level_up(_new_level: int) -> void:
    pending_points += 2

func spend_point() -> bool:
    if pending_points <= 0:
        return false
    pending_points -= 1
    return true
