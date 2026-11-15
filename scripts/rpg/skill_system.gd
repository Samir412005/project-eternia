extends Node
## SkillSystem — skill definitions + unlock by level. No combat skills
## are live in Phase 1; the system is data-complete for 3 starter skills.
const SKILLS := {
    "power_strike": {"name": "Power Strike", "min_level": 1, "cooldown_s": 3.0},
    "swift_step": {"name": "Swift Step", "min_level": 2, "cooldown_s": 8.0},
    "heal_light": {"name": "Light Heal", "min_level": 3, "cooldown_s": 12.0},
}
var unlocked: Array = ["power_strike"]
var cooldowns: Dictionary = {}

func can_use(skill_id: String, level: int) -> bool:
    if not SKILLS.has(skill_id):
        return false
    if int(SKILLS[skill_id]["min_level"]) > level:
        return false
    return float(cooldowns.get(skill_id, 0.0)) <= 0.0

func use_skill(skill_id: String, level: int) -> bool:
    if not can_use(skill_id, level):
        return false
    cooldowns[skill_id] = float(SKILLS[skill_id]["cooldown_s"])
    return true

func _process(delta: float) -> void:
    for k in cooldowns.keys():
        cooldowns[k] = maxf(0.0, float(cooldowns[k]) - delta)
