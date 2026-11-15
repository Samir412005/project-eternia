extends Node
## SettingsManager — persisted settings + scalable Android quality presets.
const SAVE_PATH := "user://settings.cfg"
const QUALITY_LOW := 0
const QUALITY_MEDIUM := 1
const QUALITY_HIGH := 2

var quality: int = QUALITY_MEDIUM
var music_volume: float = 0.7
var sfx_volume: float = 0.8
var touch_sensitivity: float = 1.0
var show_fps: bool = false

func _ready() -> void:
    load_settings()
    apply_quality()

func load_settings() -> void:
    var cfg := ConfigFile.new()
    if cfg.load(SAVE_PATH) != OK:
        return
    quality = int(cfg.get_value("graphics", "quality", QUALITY_MEDIUM))
    music_volume = float(cfg.get_value("audio", "music_volume", 0.7))
    sfx_volume = float(cfg.get_value("audio", "sfx_volume", 0.8))
    touch_sensitivity = float(cfg.get_value("controls", "touch_sensitivity", 1.0))
    show_fps = bool(cfg.get_value("debug", "show_fps", false))

func save_settings() -> void:
    var cfg := ConfigFile.new()
    cfg.set_value("graphics", "quality", quality)
    cfg.set_value("audio", "music_volume", music_volume)
    cfg.set_value("audio", "sfx_volume", sfx_volume)
    cfg.set_value("controls", "touch_sensitivity", touch_sensitivity)
    cfg.set_value("debug", "show_fps", show_fps)
    cfg.save(SAVE_PATH)

func set_quality(q: int) -> void:
    quality = clampi(q, QUALITY_LOW, QUALITY_HIGH)
    apply_quality()
    save_settings()

func apply_quality() -> void:
    # Mobile renderer: shadows are the dominant cost. Scale them, never the
    # mesh counts, so gameplay stays identical across presets.
    var sun: DirectionalLight3D = _find_sun()
    match quality:
        QUALITY_LOW:
            if sun: sun.shadow_enabled = false
            get_viewport().scaling_3d_mode = 0  # SCALING_3D_MODE_OFF
        QUALITY_MEDIUM:
            if sun:
                sun.shadow_enabled = true
                sun.shadow_bias = 0.05
            get_viewport().scaling_3d_mode = 0  # SCALING_3D_MODE_OFF
        QUALITY_HIGH:
            if sun:
                sun.shadow_enabled = true
                sun.shadow_bias = 0.02

func _find_sun() -> DirectionalLight3D:
    var scene: Node = get_tree().current_scene
    if scene == null:
        return null
    return scene.find_child("Sun", true, false) as DirectionalLight3D
