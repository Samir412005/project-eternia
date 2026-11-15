extends RefCounted
## SaveData — versioned save payload (JSON). Version 1.
const SAVE_VERSION := 1
var player_position: Vector3 = Vector3.ZERO
var level: int = 1
var xp: int = 0
var inventory: Dictionary = {}
var completed_quests: Array = []
var play_time_seconds: float = 0.0

func to_dict() -> Dictionary:
    return {
        "version": SAVE_VERSION,
        "player_position": {"x": player_position.x, "y": player_position.y, "z": player_position.z},
        "level": level, "xp": xp, "inventory": inventory,
        "completed_quests": completed_quests,
        "play_time_seconds": play_time_seconds,
    }

func from_dict(d: Dictionary) -> bool:
    if int(d.get("version", 0)) != SAVE_VERSION:
        return false
    var p: Dictionary = d.get("player_position", {})
    player_position = Vector3(float(p.get("x", 0.0)), float(p.get("y", 0.0)), float(p.get("z", 0.0)))
    level = int(d.get("level", 1))
    xp = int(d.get("xp", 0))
    inventory = d.get("inventory", {})
    completed_quests = d.get("completed_quests", [])
    play_time_seconds = float(d.get("play_time_seconds", 0.0))
    return true
