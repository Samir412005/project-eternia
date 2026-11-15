extends RefCounted
## CharacterStats — plain data + derived values. No Node, unit-testable.
var strength: int = 10
var agility: int = 10
var intelligence: int = 10
var vitality: int = 10
var level: int = 1

func max_health() -> int:
    return 80 + vitality * 10 + level * 5

func attack_power() -> int:
    return 8 + strength * 2

func move_speed_bonus() -> float:
    return agility * 0.02

func to_dict() -> Dictionary:
    return {"strength": strength, "agility": agility, "intelligence": intelligence, "vitality": vitality, "level": level}

func from_dict(d: Dictionary) -> void:
    strength = int(d.get("strength", 10))
    agility = int(d.get("agility", 10))
    intelligence = int(d.get("intelligence", 10))
    vitality = int(d.get("vitality", 10))
    level = int(d.get("level", 1))
