extends Node
## InteractionSystem — the registry PlayerInteraction talks to.
## Interactables self-register by joining the "interactable" group.
func interactables_in_range(_pos: Vector3, _radius: float) -> Array:
    var out: Array = []
    for n in get_tree().get_nodes_in_group("interactable"):
        out.append(n)
    return out
