extends Node
## EquipmentSystem — slots + equip/unequip. Starts empty (no items yet
## except what LootSystem grants). Stats come from CharacterStats.
const SLOTS := ["weapon", "armor", "amulet", "ring"]
var equipped: Dictionary = {}

func equip(slot: String, item_id: String) -> bool:
    if not SLOTS.has(slot):
        return false
    equipped[slot] = item_id
    return true

func unequip(slot: String) -> String:
    return str(equipped.get(slot, "")) if equipped.erase(slot) else ""

func equipped_in(slot: String) -> String:
    return str(equipped.get(slot, ""))
