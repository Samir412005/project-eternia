extends Node3D
## Main — scene bootstrap: wires systems, registers the player,
## handles pause + attack input at scene level.
var combat: Node = null
var loot: Node = null

func _ready() -> void:
    var player: Node = find_child("Player", true, false)
    if player:
        GameManager.register_player(player)
        player.movement_enabled = false
        var rig: Node = player.find_child("CameraRig", true, false)
        if rig:
            player.camera_yaw_node = rig
    combat = find_child("CombatSystem", true, false)
    loot = find_child("LootSystem", true, false)
    var inv: Node = find_child("InventorySystem", true, false)
    if loot and inv:
        loot.inventory = inv
    EventBus.enemy_defeated.connect(_on_enemy_defeated)

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("pause_game"):
        if GameManager.state == GameManager.STATE_PLAYING or GameManager.state == GameManager.STATE_PAUSED:
            GameManager.toggle_pause()
    if event.is_action_pressed("attack"):
        _try_attack()

func _try_attack() -> void:
    if combat == null or GameManager.player == null:
        return
    var enemy: Node3D = get_tree().get_first_node_in_group("enemy") as Node3D
    if enemy == null:
        return
    combat.try_attack(GameManager.player, enemy)

func _on_enemy_defeated(_enemy_name: String) -> void:
    if loot:
        loot.grant("dummy_defeat")
    EventBus.toast_requested.emit("Training dummy defeated. +3 old coins.")
