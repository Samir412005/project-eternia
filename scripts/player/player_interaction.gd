extends Area3D
## PlayerInteraction — detects InteractionSystem interactables in range
## and forwards the player's interact press to them.
var nearby: Array = []
var player: Node = null

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)
    area_entered.connect(_on_area_entered)
    area_exited.connect(_on_area_exited)

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("interact"):
        try_interact()

func try_interact() -> void:
    if nearby.is_empty():
        return
    var target: Node = nearby[0]
    if target.has_method("interact"):
        target.interact()

func _on_body_entered(b: Node3D) -> void:
    if b.is_in_group("interactable"):
        _add(b)

func _on_body_exited(b: Node3D) -> void:
    _remove(b)

func _on_area_entered(a: Area3D) -> void:
    if a.is_in_group("interactable"):
        _add(a)

func _on_area_exited(a: Area3D) -> void:
    _remove(a)

func _add(n: Node) -> void:
    if not nearby.has(n):
        nearby.append(n)
        EventBus.interactable_nearby.emit(str(n.name), true)

func _remove(n: Node) -> void:
    nearby.erase(n)
    if nearby.is_empty():
        EventBus.interactable_nearby.emit("", false)
