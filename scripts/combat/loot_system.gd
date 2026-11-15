extends Node
## LootSystem — deterministic starter loot table (no RNG claims).
const LOOT_TABLE := {
    "shrine_blessing": [{"item_id": "health_potion", "amount": 2}, {"item_id": "old_coin", "amount": 5}],
    "dummy_defeat": [{"item_id": "old_coin", "amount": 3}],
}
var inventory: Node = null

func grant(loot_id: String) -> Array:
    var granted: Array = []
    for entry in LOOT_TABLE.get(loot_id, []):
        if inventory != null:
            inventory.add_item(str(entry["item_id"]), int(entry["amount"]))
        granted.append(entry)
    return granted
