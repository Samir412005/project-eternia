extends Node
## EventBus — decoupled global signals. No game logic lives here.
signal player_moved(position: Vector3)
signal player_health_changed(current: int, maximum: int)
signal xp_gained(amount: int)
signal level_up(new_level: int)
signal quest_started(quest_id: String)
signal quest_updated(quest_id: String, objective_index: int)
signal quest_completed(quest_id: String)
signal item_picked_up(item_id: String, amount: int)
signal inventory_changed
signal dialogue_started(speaker: String)
signal dialogue_finished
signal interactable_nearby(interactable_name: String, available: bool)
signal toast_requested(message: String)
signal game_paused(paused: bool)
signal game_started
signal game_state_changed(new_state: String)
signal damage_dealt(target_name: String, amount: int)
signal enemy_defeated(enemy_name: String)
