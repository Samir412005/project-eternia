extends Node
## WeatherSystem — UNFINISHED (Phase 2). Data + API only; no rain yet.
## Do not claim weather exists: current state is always CLEAR in Phase 1.
const CLEAR := "CLEAR"
var current_weather: String = CLEAR

func set_weather(w: String) -> void:
    current_weather = w
