extends Node
## ExperienceSystem — XP, levels, real curve. Emits EventBus signals.
var level: int = 1
var xp: int = 0
var xp_to_next: int = 100
var stats: RefCounted = null

func _ready() -> void:
    var script: Script = load("res://scripts/rpg/character_stats.gd")
    stats = script.new()
    stats.level = level

func xp_for_level(l: int) -> int:
    return int(100.0 * pow(float(l), 1.5))

func add_xp(amount: int) -> void:
    if amount <= 0:
        return
    xp += amount
    EventBus.xp_gained.emit(amount)
    while xp >= xp_to_next:
        xp -= xp_to_next
        level += 1
        xp_to_next = xp_for_level(level)
        stats.level = level
        stats.vitality += 1
        stats.strength += 1
        EventBus.level_up.emit(level)
