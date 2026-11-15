extends Node
## WorldRegions — data for the regions the game will grow into.
## Phase 1 has ONE real region (the valley). The rest are data-only
## placeholders, NOT claimed as built.
const REGIONS := {
    "eternia_valley": {"name": "Eternia Valley", "built": true, "size_m": 60},
    "ashen_woods": {"name": "Ashen Woods", "built": false, "size_m": 0},
    "sunken_city": {"name": "Sunken City", "built": false, "size_m": 0},
    "frost_peaks": {"name": "Frost Peaks", "built": false, "size_m": 0},
}

func is_built(region_id: String) -> bool:
    return bool(REGIONS.get(region_id, {}).get("built", false))

func built_regions() -> Array:
    var out: Array = []
    for k in REGIONS.keys():
        if REGIONS[k]["built"]:
            out.append(k)
    return out
