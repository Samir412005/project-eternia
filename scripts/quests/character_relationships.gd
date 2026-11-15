extends Node
## CharacterRelationships — UNFINISHED (Phase 3). Affinity data only.
var affinity: Dictionary = {}

func affinity_with(npc_id: String) -> int:
    return int(affinity.get(npc_id, 0))
