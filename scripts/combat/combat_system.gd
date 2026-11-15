extends Node
## CombatSystem — melee attack with cooldown, range check, damage math.
var attack_cooldown: float = 0.6
var _cooldown_left: float = 0.0
var attack_range: float = 2.6
var base_damage: int = 12

func _process(delta: float) -> void:
    _cooldown_left = maxf(0.0, _cooldown_left - delta)

func can_attack() -> bool:
    return _cooldown_left <= 0.0 and GameManager.state == GameManager.STATE_PLAYING

func try_attack(attacker: Node3D, target: Node3D) -> int:
    if not can_attack() or attacker == null or target == null:
        return 0
    if attacker.global_position.distance_to(target.global_position) > attack_range:
        return 0
    _cooldown_left = attack_cooldown
    var dmg: int = base_damage
    EventBus.damage_dealt.emit(str(target.name), dmg)
    if target.has_method("take_damage"):
        target.take_damage(dmg)
    return dmg
