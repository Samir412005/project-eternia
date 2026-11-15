extends Node
## InventorySystem — real dict inventory with capacity and stacking.
const MAX_SLOTS := 24
const MAX_STACK := 99
var items: Dictionary = {}

func add_item(item_id: String, amount: int = 1) -> bool:
    if amount <= 0:
        return false
    if not items.has(item_id) and items.size() >= MAX_SLOTS:
        return false
    var current: int = int(items.get(item_id, 0))
    items[item_id] = mini(current + amount, MAX_STACK)
    EventBus.item_picked_up.emit(item_id, amount)
    EventBus.inventory_changed.emit()
    return true

func remove_item(item_id: String, amount: int = 1) -> bool:
    var current: int = int(items.get(item_id, 0))
    if current < amount:
        return false
    var remaining: int = current - amount
    if remaining <= 0:
        items.erase(item_id)
    else:
        items[item_id] = remaining
    EventBus.inventory_changed.emit()
    return true

func count(item_id: String) -> int:
    return int(items.get(item_id, 0))

func total_items() -> int:
    var t: int = 0
    for v in items.values():
        t += int(v)
    return t

func to_dict() -> Dictionary:
    return items.duplicate()

func from_dict(d: Dictionary) -> void:
    items.clear()
    for k in d.keys():
        items[str(k)] = int(d[k])
