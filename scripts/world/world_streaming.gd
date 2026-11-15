extends Node
## WorldStreaming — UNFINISHED (Phase 3). One 60 m region needs no
## streaming; this file only reserves the interface.
func load_region(_region_id: String) -> bool:
    push_warning("WorldStreaming: streaming not implemented in Phase 1")
    return false
