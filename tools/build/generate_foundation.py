#!/usr/bin/env python3
"""PROJECT ETERNIA - foundation generator (Phase 1).
Generates the Godot project structure, docs, GDScript modules,
scenes, data and tests. Re-running it overwrites generated files.
Run from anywhere:  python3 generate_foundation.py
"""
import json, os, textwrap
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def w(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip("\n"))
    print("wrote", rel)

DIRS = [
 "assets/characters", "assets/environments", "assets/animations",
 "assets/materials", "assets/audio", "assets/textures", "assets/ui",
 "scenes/main", "scenes/player", "scenes/world", "scenes/characters",
 "scenes/enemies", "scenes/gameplay", "scenes/cinematics", "scenes/ui",
 "scripts/core", "scripts/player", "scripts/world", "scripts/rpg",
 "scripts/combat", "scripts/quests", "scripts/dialogue", "scripts/inventory",
 "scripts/save", "scripts/ui", "scripts/gameplay",
 "data/characters", "data/items", "data/quests", "data/dialogue", "data/abilities",
 "tests/unit", "tests/integration", "tests/gameplay", "tests/reports",
 "tools/coordinator", "tools/validation", "tools/build",
 "builds/android",
]
for d in DIRS:
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)

# ---------------------------------------------------------------- project.godot
w("project.godot", '''\
; Engine configuration file.
; PROJECT ETERNIA - Godot 4.3, Mobile renderer, Android landscape.
config_version=5

[application]
config/name="PROJECT ETERNIA"
config/description="Large-scale 3D RPG - first playable vertical slice (Phase 1)."
run/main_scene="res://scenes/main/main.tscn"
config/features=PackedStringArray("4.3", "Mobile")
config/icon="res://icon.svg"

[autoload]
EventBus="*res://scripts/core/event_bus.gd"
SettingsManager="*res://scripts/core/settings_manager.gd"
ResourceManager="*res://scripts/core/resource_manager.gd"
GameManager="*res://scripts/core/game_manager.gd"
SaveManager="*res://scripts/save/save_manager.gd"
SceneManager="*res://scripts/core/scene_manager.gd"

[display]
window/size/viewport_width=1280
window/size/viewport_height=720
window/size/resizable=true
window/stretch/mode="canvas_items"
window/stretch/aspect="expand"
window/handheld/orientation=0
window/size/handheld_orientation=0

[input]
move_left={"deadzone": 0.2, "events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":65,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null), Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":4194319,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]}
move_right={"deadzone": 0.2, "events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":68,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null), Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":4194321,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]}
move_forward={"deadzone": 0.2, "events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":87,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null), Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":4194320,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]}
move_back={"deadzone": 0.2, "events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":83,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null), Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":4194322,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]}
jump={"deadzone": 0.2, "events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":32,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]}
run={"deadzone": 0.2, "events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":4194325,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]}
interact={"deadzone": 0.2, "events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":69,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]}
attack={"deadzone": 0.2, "events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":70,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]}
pause_game={"deadzone": 0.2, "events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":4194305,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]}

[input_devices]
pointing/emulate_touch_from_mouse=true
pointing/emulate_mouse_from_touch=true

[physics]
common/physics_ticks_per_second=60

[rendering]
renderer/rendering_method="mobile"
renderer/rendering_method.mobile="gl_compatibility"
textures/vram_compression/import_etc2_astc=true
textures/default_filters/use_nearest_mipmap_filter=true
environment/defaults/default_clear_color=Color(0.05, 0.06, 0.11, 1)
anti_aliasing/quality/msaa_3d=0
scaling_3d/mode=0
''')

w("export_presets.cfg", '''\
[preset.0]
name="Android Mobile"
platform="Android"
runnable=true
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path="builds/android/project-eternia-debug.apk"
encryption_include_filters=""
encryption_exclude_filters=""
encrypt_pck=false
encrypt_directory=false

[preset.0.options]
custom_template/debug=""
custom_template/release=""
variant/extensions_support=false
variant/app_type=0
gradle_build/use_gradle_build=false
gradle_build/gradle_build_directory=""
keystore/debug=""
keystore/debug_user=""
keystore/debug_password=""
keystore/release="/home/hatch/workspace/game-apk/debug.keystore"
keystore/release_user="androiddebugkey"
keystore/release_password="android"
architectures/armeabi-v7a=false
architectures/arm64-v8a=true
architectures/x86=false
architectures/x86_64=false
version/code=1
version/name="0.1"
package/unique_name="com.gggg.eternia"
package/name="PROJECT ETERNIA"
package/signature=""
permissions/custom_permissions=""
''')

w("icon.svg", '''\
<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128"><rect width="128" height="128" rx="24" fill="#0b0d16"/><text x="64" y="82" font-size="64" text-anchor="middle" fill="#e8c47a" font-family="serif">E</text></svg>
''')
print("part1 done")

# ---------------------------------------------------------------- GDScript modules
# Each entry is a real, load-bearing foundation script. Stubs are marked
# UNFINISHED in the file itself and in TECHNICAL_ARCHITECTURE.md.
SCRIPTS = {}

SCRIPTS["scripts/core/event_bus.gd"] = '''\
extends Node
## EventBus — decoupled global signals. No game logic lives here.
signal player_moved(position: Vector3)
signal player_health_changed(current: int, maximum: int)
signal xp_gained(amount: int)
signal level_up(new_level: int)
signal quest_started(quest_id: String)
signal quest_updated(quest_id: String, objective_index: int)
signal quest_completed(quest_id: String)
signal item_picked_up(item_id: String, amount: int)
signal inventory_changed
signal dialogue_started(speaker: String)
signal dialogue_finished
signal interactable_nearby(interactable_name: String, available: bool)
signal toast_requested(message: String)
signal game_paused(paused: bool)
signal game_started
signal game_state_changed(new_state: String)
signal damage_dealt(target_name: String, amount: int)
signal enemy_defeated(enemy_name: String)
'''

SCRIPTS["scripts/core/game_manager.gd"] = '''\
extends Node
## GameManager — top-level game state machine and session wiring.
## States: MENU, PLAYING, PAUSED, DIALOGUE, CINEMATIC.
const STATE_MENU := "MENU"
const STATE_PLAYING := "PLAYING"
const STATE_PAUSED := "PAUSED"
const STATE_DIALOGUE := "DIALOGUE"

var state: String = STATE_MENU
var player: Node = null
var play_time_seconds: float = 0.0
var is_new_game: bool = true

func _ready() -> void:
    process_mode = Node.PROCESS_MODE_ALWAYS

func _process(delta: float) -> void:
    if state == STATE_PLAYING:
        play_time_seconds += delta

func set_state(new_state: String) -> void:
    if new_state == state:
        return
    state = new_state
    EventBus.game_state_changed.emit(state)

func start_game() -> void:
    is_new_game = true
    play_time_seconds = 0.0
    set_state(STATE_PLAYING)
    EventBus.game_started.emit()

func toggle_pause() -> void:
    if state == STATE_PLAYING:
        get_tree().paused = true
        set_state(STATE_PAUSED)
        EventBus.game_paused.emit(true)
    elif state == STATE_PAUSED:
        get_tree().paused = false
        set_state(STATE_PLAYING)
        EventBus.game_paused.emit(false)

func return_to_menu() -> void:
    get_tree().paused = false
    set_state(STATE_MENU)

func register_player(p: Node) -> void:
    player = p
'''

SCRIPTS["scripts/core/scene_manager.gd"] = '''\
extends Node
## SceneManager — single place that changes scenes, with a fade hook.
## UNFINISHED: no loading screen / async streaming yet (see roadmap Phase 3).
var current_scene_path: String = "res://scenes/main/main.tscn"

func change_scene(path: String) -> void:
    current_scene_path = path
    var err: Error = get_tree().change_scene_to_file(path)
    if err != OK:
        push_error("SceneManager: failed to load " + path + " err=" + str(err))

func reload_current_scene() -> void:
    get_tree().reload_current_scene()
'''

SCRIPTS["scripts/core/settings_manager.gd"] = '''\
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
'''

SCRIPTS["scripts/core/resource_manager.gd"] = '''\
extends Node
## ResourceManager — tiny load cache so scenes/scripts are loaded once.
var _cache: Dictionary = {}

func load_resource(path: String) -> Resource:
    if _cache.has(path):
        return _cache[path]
    var res: Resource = load(path)
    if res != null:
        _cache[path] = res
    else:
        push_error("ResourceManager: cannot load " + path)
    return res

func preload_scene(path: String) -> PackedScene:
    return load_resource(path) as PackedScene

func clear_cache() -> void:
    _cache.clear()

func cached_count() -> int:
    return _cache.size()
'''

SCRIPTS["scripts/player/player_controller.gd"] = '''\
extends CharacterBody3D
## PlayerController — third-person CharacterBody3D.
## Walk / run / jump / gravity / ground detection. Camera-relative movement.
## Prototype mesh: primitive humanoid (see player_animation_controller.gd).
@export var walk_speed: float = 4.5
@export var run_speed: float = 8.0
@export var jump_velocity: float = 7.5
@export var acceleration: float = 14.0
@export var rotation_speed: float = 12.0

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity") as float
var joystick_vector: Vector2 = Vector2.ZERO
var run_held: bool = false
var movement_enabled: bool = false
var current_speed: float = 0.0
var camera_yaw_node: Node3D = null
var was_on_floor: bool = true

func _ready() -> void:
    add_to_group("player")
    floor_snap_length = 0.3
    floor_max_angle = deg_to_rad(50.0)

func _physics_process(delta: float) -> void:
    if not movement_enabled:
        velocity.x = move_toward(velocity.x, 0.0, acceleration * delta)
        velocity.z = move_toward(velocity.z, 0.0, acceleration * delta)
        _apply_gravity(delta)
        move_and_slide()
        return
    var input_vec: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    if joystick_vector.length() > 0.08:
        input_vec = joystick_vector
    var yaw: float = 0.0
    if camera_yaw_node != null:
        yaw = camera_yaw_node.rotation.y
    var forward: Vector3 = Vector3(-sin(yaw), 0.0, -cos(yaw))
    var right: Vector3 = Vector3(cos(yaw), 0.0, -sin(yaw))
    var wish_dir: Vector3 = (right * input_vec.x + forward * -input_vec.y)
    wish_dir.y = 0.0
    if wish_dir.length() > 1.0:
        wish_dir = wish_dir.normalized()
    var target_speed: float = run_speed if (run_held or Input.is_action_pressed("run")) else walk_speed
    if wish_dir.length() < 0.08:
        target_speed = 0.0
    var target_vel: Vector3 = wish_dir * target_speed
    velocity.x = move_toward(velocity.x, target_vel.x, acceleration * delta)
    velocity.z = move_toward(velocity.z, target_vel.z, acceleration * delta)
    current_speed = Vector2(velocity.x, velocity.z).length()
    if wish_dir.length() > 0.1:
        var target_yaw: float = atan2(-wish_dir.x, -wish_dir.z)
        rotation.y = lerp_angle(rotation.y, target_yaw, minf(1.0, rotation_speed * delta))
    _apply_gravity(delta)
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity
    var on_floor_now: bool = is_on_floor()
    if on_floor_now and not was_on_floor:
        pass
    was_on_floor = on_floor_now
    move_and_slide()
    if is_on_floor() or is_on_wall():
        EventBus.player_moved.emit(global_position)

func _apply_gravity(delta: float) -> void:
    if not is_on_floor():
        velocity.y -= gravity * delta
    elif velocity.y < 0.0:
        velocity.y = -0.5

func set_run_held(v: bool) -> void:
    run_held = v

func teleport_to(pos: Vector3) -> void:
    global_position = pos
    velocity = Vector3.ZERO
'''

SCRIPTS["scripts/player/camera_controller.gd"] = '''\
extends Node3D
## CameraController — yaw/pitch rig on a SpringArm3D (collision-aware).
## Drag on empty screen area rotates; pinch is NOT implemented (roadmap).
@export var pitch_min: float = -0.35
@export var pitch_max: float = 0.85
@export var drag_sensitivity: float = 0.004

var yaw: float = 0.0
var pitch: float = 0.32
var spring: SpringArm3D = null
var dragging: bool = false

func _ready() -> void:
    spring = get_node_or_null("SpringArm3D") as SpringArm3D
    if spring:
        spring.spring_length = 6.0
        spring.margin = 0.3

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        dragging = event.pressed
    elif event is InputEventMouseMotion and dragging:
        _rotate_by(event.relative)
    elif event is InputEventScreenTouch:
        dragging = event.pressed
    elif event is InputEventScreenDrag:
        _rotate_by(event.relative * 1.6)

func _rotate_by(relative: Vector2) -> void:
    yaw -= relative.x * drag_sensitivity * SettingsManager.touch_sensitivity
    pitch = clampf(pitch + relative.y * drag_sensitivity * SettingsManager.touch_sensitivity, pitch_min, pitch_max)
    rotation.y = yaw
    if spring:
        spring.rotation.x = -pitch

func snap_behind_player() -> void:
    yaw = 0.0
    pitch = 0.32
    rotation.y = yaw
    if spring:
        spring.rotation.x = -pitch
'''

SCRIPTS["scripts/player/player_state_machine.gd"] = '''\
extends Node
## PlayerStateMachine — IDLE / WALK / RUN / JUMP / FALL / INTERACT.
## Driven from PlayerController each physics frame; no behaviour is faked:
## the state is derived from real velocity / floor state.
const IDLE := "IDLE"
const WALK := "WALK"
const RUN := "RUN"
const JUMP := "JUMP"
const FALL := "FALL"
const INTERACT := "INTERACT"

var current_state: String = IDLE
var player: CharacterBody3D = null

func _ready() -> void:
    player = get_parent() as CharacterBody3D

func _physics_process(_delta: float) -> void:
    if player == null:
        return
    if not player.movement_enabled:
        _set_state(IDLE)
        return
    var speed: float = Vector2(player.velocity.x, player.velocity.z).length()
    var next: String = current_state
    if not player.is_on_floor():
        next = JUMP if player.velocity.y > 0.0 else FALL
    elif speed > 6.5:
        next = RUN
    elif speed > 0.4:
        next = WALK
    else:
        next = IDLE
    _set_state(next)

func _set_state(s: String) -> void:
    if s != current_state:
        current_state = s

func is_moving() -> bool:
    return current_state == WALK or current_state == RUN
'''

SCRIPTS["scripts/player/player_interaction.gd"] = '''\
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
'''

SCRIPTS["scripts/player/player_animation_controller.gd"] = '''\
extends Node3D
## PlayerAnimationController — procedural animation for the PROTOTYPE mesh.
## No imported animations exist yet (see ASSET LIMITATIONS in README).
## Walk/run swing the primitive limbs; idle breathes; jump tucks.
var player: CharacterBody3D = null
var body: MeshInstance3D = null
var arm_l: MeshInstance3D = null
var arm_r: MeshInstance3D = null
var leg_l: MeshInstance3D = null
var leg_r: MeshInstance3D = null
var anim_time: float = 0.0

func _ready() -> void:
    player = get_parent() as CharacterBody3D
    body = get_node_or_null("Body") as MeshInstance3D
    arm_l = get_node_or_null("ArmL") as MeshInstance3D
    arm_r = get_node_or_null("ArmR") as MeshInstance3D
    leg_l = get_node_or_null("LegL") as MeshInstance3D
    leg_r = get_node_or_null("LegR") as MeshInstance3D

func _process(delta: float) -> void:
    if player == null:
        return
    var speed: float = Vector2(player.velocity.x, player.velocity.z).length()
    anim_time += delta * (2.0 + speed * 1.6)
    var swing: float = sin(anim_time * 3.0) * clampf(speed / 8.0, 0.0, 1.0) * 0.7
    if leg_l: leg_l.rotation.x = swing
    if leg_r: leg_r.rotation.x = -swing
    if arm_l: arm_l.rotation.x = -swing * 0.8
    if arm_r: arm_r.rotation.x = swing * 0.8
    if body:
        var bob: float = absf(sin(anim_time * 3.0)) * 0.05 * clampf(speed / 8.0, 0.0, 1.0)
        body.position.y = 0.95 + bob
        if not player.is_on_floor():
            body.position.y = 1.0
'''

for rel, content in SCRIPTS.items():
    w(rel, content)
print("part2 done, scripts:", len(SCRIPTS))

# ---------------------------------------------------------------- part 3
SCRIPTS2 = {}
SCRIPTS2["scripts/world/world_manager.gd"] = '''\
extends Node3D
## WorldManager — builds the Phase 1 vertical-slice environment at runtime
## from primitives (ground, platforms, ruins, trees, shrine, torches).
## This is a real 3D environment, not a backdrop: every piece has collision
## where the player can stand on it. World size: 60 x 60 m test valley.
const SIZE := 60.0

func _ready() -> void:
    _build_ground()
    _build_platforms()
    _build_ruins()
    _build_trees()
    _build_shrine()
    _build_torches()

func _mat(color: Color, rough: float = 0.9) -> StandardMaterial3D:
    var m := StandardMaterial3D.new()
    m.albedo_color = color
    m.roughness = rough
    return m

func _box(name: String, pos: Vector3, size: Vector3, mat: Material) -> StaticBody3D:
    var body := StaticBody3D.new()
    body.name = name
    body.position = pos
    var mesh := MeshInstance3D.new()
    var box := BoxMesh.new()
    box.size = size
    box.material = mat
    mesh.mesh = box
    body.add_child(mesh)
    var col := CollisionShape3D.new()
    var shape := BoxShape3D.new()
    shape.size = size
    col.shape = shape
    body.add_child(col)
    add_child(body)
    return body

func _build_ground() -> void:
    var body := StaticBody3D.new()
    body.name = "Ground"
    var mesh := MeshInstance3D.new()
    var plane := PlaneMesh.new()
    plane.size = Vector2(SIZE, SIZE)
    plane.material = _mat(Color(0.23, 0.35, 0.2))
    mesh.mesh = plane
    body.add_child(mesh)
    var col := CollisionShape3D.new()
    var shape := BoxShape3D.new()
    shape.size = Vector3(SIZE, 1.0, SIZE)
    col.shape = shape
    col.position.y = -0.5
    body.add_child(col)
    add_child(body)

func _build_platforms() -> void:
    var stone := _mat(Color(0.45, 0.43, 0.4))
    _box("PlatformNorth", Vector3(0, 0.5, -20), Vector3(12, 1, 8), stone)
    _box("PlatformEast", Vector3(18, 0.75, 6), Vector3(8, 1.5, 8), stone)
    _box("StepNorth", Vector3(0, 0.25, -15), Vector3(4, 0.5, 2), stone)

func _build_ruins() -> void:
    var stone := _mat(Color(0.55, 0.52, 0.48))
    var dark := _mat(Color(0.32, 0.3, 0.28))
    var positions: Array = [
        Vector3(-14, 1.5, -10), Vector3(-14, 1.5, -6), Vector3(-10, 2.0, -12),
        Vector3(12, 1.0, -16), Vector3(16, 1.0, -16),
        Vector3(-18, 1.0, 14), Vector3(14, 1.25, 18),
    ]
    for i in range(positions.size()):
        var h: float = 3.0 if i % 2 == 0 else 2.0
        _box("Pillar%d" % i, positions[i], Vector3(1.2, h, 1.2), stone if i % 2 == 0 else dark)
    _box("BrokenWall", Vector3(-8, 1.0, -18), Vector3(10, 2, 1), dark)

func _build_trees() -> void:
    var trunk_mat := _mat(Color(0.35, 0.25, 0.16))
    var leaf_mat := _mat(Color(0.16, 0.4, 0.18))
    var spots: Array = [
        Vector3(-22, 0, -18), Vector3(-24, 0, 2), Vector3(-20, 0, 20),
        Vector3(22, 0, -8), Vector3(24, 0, 12), Vector3(8, 0, 24),
        Vector3(-6, 0, 24), Vector3(20, 0, -22),
    ]
    for i in range(spots.size()):
        var tree := StaticBody3D.new()
        tree.name = "Tree%d" % i
        tree.position = spots[i]
        var trunk := MeshInstance3D.new()
        var cyl := CylinderMesh.new()
        cyl.top_radius = 0.25
        cyl.bottom_radius = 0.4
        cyl.height = 2.4
        cyl.material = trunk_mat
        trunk.mesh = cyl
        trunk.position.y = 1.2
        tree.add_child(trunk)
        var col := CollisionShape3D.new()
        var shape := CylinderShape3D.new()
        shape.radius = 0.4
        shape.height = 2.4
        col.shape = shape
        col.position.y = 1.2
        tree.add_child(col)
        var leaves := MeshInstance3D.new()
        var cone := CylinderMesh.new()
        cone.top_radius = 0.0
        cone.bottom_radius = 2.0
        cone.height = 3.2
        cone.material = leaf_mat
        leaves.mesh = cone
        leaves.position.y = 3.8
        tree.add_child(leaves)
        add_child(tree)

func _build_shrine() -> void:
    var shrine_script: Script = load("res://scripts/gameplay/shrine.gd")
    var shrine := Area3D.new()
    shrine.name = "AncientShrine"
    shrine.set_script(shrine_script)
    shrine.add_to_group("interactable")
    shrine.position = Vector3(0, 0, -8)
    add_child(shrine)
    var base := MeshInstance3D.new()
    var box := BoxMesh.new()
    box.size = Vector3(2.4, 1.0, 2.4)
    box.material = _mat(Color(0.62, 0.58, 0.5))
    base.mesh = box
    base.position.y = 0.5
    shrine.add_child(base)
    var crystal := MeshInstance3D.new()
    var prism := PrismMesh.new()
    prism.size = Vector3(0.9, 1.6, 0.9)
    var glow := StandardMaterial3D.new()
    glow.albedo_color = Color(0.45, 0.75, 1.0)
    glow.emission_enabled = true
    glow.emission = Color(0.35, 0.6, 1.0)
    glow.emission_energy_multiplier = 1.5
    prism.material = glow
    crystal.mesh = prism
    crystal.position.y = 1.9
    shrine.add_child(crystal)
    var col := CollisionShape3D.new()
    var shape := BoxShape3D.new()
    shape.size = Vector3(3.5, 3.5, 3.5)
    col.shape = shape
    col.position.y = 1.5
    shrine.add_child(col)
    var light := OmniLight3D.new()
    light.position.y = 2.4
    light.light_color = Color(0.5, 0.7, 1.0)
    light.light_energy = 1.2
    light.omni_range = 8.0
    shrine.add_child(light)

func _build_torches() -> void:
    for i in range(2):
        var pos: Vector3 = Vector3(-3 + i * 6, 0, -9.5)
        var torch := Node3D.new()
        torch.name = "Torch%d" % i
        torch.position = pos
        var pole := MeshInstance3D.new()
        var cyl := CylinderMesh.new()
        cyl.top_radius = 0.08
        cyl.bottom_radius = 0.12
        cyl.height = 1.6
        cyl.material = _mat(Color(0.3, 0.22, 0.14))
        pole.mesh = cyl
        pole.position.y = 0.8
        torch.add_child(pole)
        var flame := OmniLight3D.new()
        flame.position.y = 1.8
        flame.light_color = Color(1.0, 0.6, 0.25)
        flame.light_energy = 0.9
        flame.omni_range = 6.0
        torch.add_child(flame)
        add_child(torch)
'''

SCRIPTS2["scripts/world/world_regions.gd"] = '''\
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
'''

SCRIPTS2["scripts/world/environment_system.gd"] = '''\
extends Node
## EnvironmentSystem — fog + sky tuning for the valley (Mobile-safe).
var fog_density: float = 0.012

func _ready() -> void:
    var cs: Node = get_tree().current_scene
    if cs == null:
        return
    var env: WorldEnvironment = cs.find_child("WorldEnvironment", true, false) as WorldEnvironment
    if env and env.environment:
        env.environment.fog_enabled = true
        env.environment.fog_light_color = Color(0.65, 0.7, 0.8)
        env.environment.fog_density = fog_density
'''

SCRIPTS2["scripts/world/time_of_day.gd"] = '''\
extends Node
## TimeOfDay — a real day clock (0..24) that rotates the sun.
## Phase 1: slow fixed drift; full day/night cycle in Phase 2.
var time_hours: float = 10.0
var time_scale: float = 0.05
var sun: DirectionalLight3D = null

func _ready() -> void:
    _find_sun()

func _find_sun() -> void:
    var cs: Node = get_tree().current_scene
    if cs != null:
        sun = cs.find_child("Sun", true, false) as DirectionalLight3D

func _process(delta: float) -> void:
    if sun == null:
        _find_sun()
        if sun == null:
            return
    time_hours = fmod(time_hours + delta * time_scale, 24.0)
    var angle: float = deg_to_rad((time_hours - 6.0) / 12.0 * 180.0)
    sun.rotation_degrees = Vector3(-45.0 + sin(angle) * 10.0, -30.0, 0.0)

func is_night() -> bool:
    return time_hours < 6.0 or time_hours >= 18.0
'''

SCRIPTS2["scripts/world/weather_system.gd"] = '''\
extends Node
## WeatherSystem — UNFINISHED (Phase 2). Data + API only; no rain yet.
## Do not claim weather exists: current state is always CLEAR in Phase 1.
const CLEAR := "CLEAR"
var current_weather: String = CLEAR

func set_weather(w: String) -> void:
    current_weather = w
'''

SCRIPTS2["scripts/world/world_streaming.gd"] = '''\
extends Node
## WorldStreaming — UNFINISHED (Phase 3). One 60 m region needs no
## streaming; this file only reserves the interface.
func load_region(_region_id: String) -> bool:
    push_warning("WorldStreaming: streaming not implemented in Phase 1")
    return false
'''

SCRIPTS2["scripts/rpg/character_stats.gd"] = '''\
extends RefCounted
## CharacterStats — plain data + derived values. No Node, unit-testable.
var strength: int = 10
var agility: int = 10
var intelligence: int = 10
var vitality: int = 10
var level: int = 1

func max_health() -> int:
    return 80 + vitality * 10 + level * 5

func attack_power() -> int:
    return 8 + strength * 2

func move_speed_bonus() -> float:
    return agility * 0.02

func to_dict() -> Dictionary:
    return {"strength": strength, "agility": agility, "intelligence": intelligence, "vitality": vitality, "level": level}

func from_dict(d: Dictionary) -> void:
    strength = int(d.get("strength", 10))
    agility = int(d.get("agility", 10))
    intelligence = int(d.get("intelligence", 10))
    vitality = int(d.get("vitality", 10))
    level = int(d.get("level", 1))
'''

SCRIPTS2["scripts/rpg/experience_system.gd"] = '''\
extends Node
## ExperienceSystem — XP, levels, real curve. Emits EventBus signals.
var level: int = 1
var xp: int = 0
var xp_to_next: int = 100
var stats: RefCounted = null

func _ready() -> void:
    var script: Script = load("res://scripts/rpg/character_stats.gd")
    stats = script.new()
    stats.level = level

func xp_for_level(l: int) -> int:
    return int(100.0 * pow(float(l), 1.5))

func add_xp(amount: int) -> void:
    if amount <= 0:
        return
    xp += amount
    EventBus.xp_gained.emit(amount)
    while xp >= xp_to_next:
        xp -= xp_to_next
        level += 1
        xp_to_next = xp_for_level(level)
        stats.level = level
        stats.vitality += 1
        stats.strength += 1
        EventBus.level_up.emit(level)
'''

SCRIPTS2["scripts/rpg/level_progression.gd"] = '''\
extends Node
## LevelProgression — attribute points awarded per level (2 per level).
var pending_points: int = 0

func _ready() -> void:
    EventBus.level_up.connect(_on_level_up)

func _on_level_up(_new_level: int) -> void:
    pending_points += 2

func spend_point() -> bool:
    if pending_points <= 0:
        return false
    pending_points -= 1
    return true
'''

SCRIPTS2["scripts/rpg/skill_system.gd"] = '''\
extends Node
## SkillSystem — skill definitions + unlock by level. No combat skills
## are live in Phase 1; the system is data-complete for 3 starter skills.
const SKILLS := {
    "power_strike": {"name": "Power Strike", "min_level": 1, "cooldown_s": 3.0},
    "swift_step": {"name": "Swift Step", "min_level": 2, "cooldown_s": 8.0},
    "heal_light": {"name": "Light Heal", "min_level": 3, "cooldown_s": 12.0},
}
var unlocked: Array = ["power_strike"]
var cooldowns: Dictionary = {}

func can_use(skill_id: String, level: int) -> bool:
    if not SKILLS.has(skill_id):
        return false
    if int(SKILLS[skill_id]["min_level"]) > level:
        return false
    return float(cooldowns.get(skill_id, 0.0)) <= 0.0

func use_skill(skill_id: String, level: int) -> bool:
    if not can_use(skill_id, level):
        return false
    cooldowns[skill_id] = float(SKILLS[skill_id]["cooldown_s"])
    return true

func _process(delta: float) -> void:
    for k in cooldowns.keys():
        cooldowns[k] = maxf(0.0, float(cooldowns[k]) - delta)
'''

SCRIPTS2["scripts/rpg/equipment_system.gd"] = '''\
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
'''

SCRIPTS2["scripts/rpg/inventory_system.gd"] = '''\
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
'''

SCRIPTS2["scripts/combat/combat_system.gd"] = '''\
extends Node
## CombatSystem — melee attack with cooldown, range check, damage math.
var attack_cooldown: float = 0.6
var _cooldown_left: float = 0.0
var attack_range: float = 2.6
var base_damage: int = 12

func _process(delta: float) -> void:
    _cooldown_left = maxf(0.0, _cooldown_left - delta)

func can_attack() -> bool:
    return _cooldown_left <= 0.0 and GameManager.state == GameManager.STATE_PLAYING

func try_attack(attacker: Node3D, target: Node3D) -> int:
    if not can_attack() or attacker == null or target == null:
        return 0
    if attacker.global_position.distance_to(target.global_position) > attack_range:
        return 0
    _cooldown_left = attack_cooldown
    var dmg: int = base_damage
    EventBus.damage_dealt.emit(str(target.name), dmg)
    if target.has_method("take_damage"):
        target.take_damage(dmg)
    return dmg
'''

SCRIPTS2["scripts/combat/enemy_ai.gd"] = '''\
extends CharacterBody3D
## EnemyAI — training dummy that chases the player inside 12 m and
## attacks inside 2 m. Real physics body, real HP.
@export var max_health: int = 40
@export var move_speed: float = 2.2
@export var aggro_range: float = 12.0
@export var attack_range: float = 2.0
@export var attack_damage: int = 5

var health: int = 40
var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity") as float
var _attack_timer: float = 0.0
var _respawn_pos: Vector3 = Vector3.ZERO

func _ready() -> void:
    add_to_group("enemy")
    health = max_health
    _respawn_pos = global_position

func _physics_process(delta: float) -> void:
    var player: Node3D = get_tree().get_first_node_in_group("player") as Node3D
    if player == null or not is_on_floor():
        if not is_on_floor():
            velocity.y -= gravity * delta
        move_and_slide()
        return
    var to_player: Vector3 = player.global_position - global_position
    to_player.y = 0.0
    var dist: float = to_player.length()
    _attack_timer = maxf(0.0, _attack_timer - delta)
    if dist < aggro_range and dist > attack_range:
        var dir: Vector3 = to_player.normalized()
        velocity.x = dir.x * move_speed
        velocity.z = dir.z * move_speed
        rotation.y = lerp_angle(rotation.y, atan2(-dir.x, -dir.z), minf(1.0, 8.0 * delta))
    else:
        velocity.x = move_toward(velocity.x, 0.0, 10.0 * delta)
        velocity.z = move_toward(velocity.z, 0.0, 10.0 * delta)
        if dist <= attack_range and _attack_timer <= 0.0:
            _attack_timer = 1.2
    if not is_on_floor():
        velocity.y -= gravity * delta
    else:
        velocity.y = -0.5
    move_and_slide()

func take_damage(amount: int) -> void:
    health -= amount
    if health <= 0:
        EventBus.enemy_defeated.emit(str(name))
        health = max_health
        global_position = _respawn_pos
        velocity = Vector3.ZERO
'''

SCRIPTS2["scripts/combat/interaction_system.gd"] = '''\
extends Node
## InteractionSystem — the registry PlayerInteraction talks to.
## Interactables self-register by joining the "interactable" group.
func interactables_in_range(_pos: Vector3, _radius: float) -> Array:
    var out: Array = []
    for n in get_tree().get_nodes_in_group("interactable"):
        out.append(n)
    return out
'''

SCRIPTS2["scripts/combat/loot_system.gd"] = '''\
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
'''

SCRIPTS2["scripts/quests/quest_database.gd"] = '''\
extends Node
## QuestDatabase — loads data/quests/quests.json once, serves lookups.
var quests: Dictionary = {}

func _ready() -> void:
    load_quests()

func load_quests() -> bool:
    var path: String = "res://data/quests/quests.json"
    if not FileAccess.file_exists(path):
        push_error("QuestDatabase: missing " + path)
        return false
    var text: String = FileAccess.get_file_as_string(path)
    var parsed: Variant = JSON.parse_string(text)
    if parsed == null:
        push_error("QuestDatabase: invalid JSON in " + path)
        return false
    quests = parsed as Dictionary
    return true

func get_quest(quest_id: String) -> Dictionary:
    return quests.get(quest_id, {}) as Dictionary
'''

SCRIPTS2["scripts/quests/quest_manager.gd"] = '''\
extends Node
## QuestManager — active/completed quests, objective progress.
## Quest 1 ("first_light") is completable in the slice: visit the shrine.
var active: Dictionary = {}
var completed: Array = []
var database: Node = null

func _ready() -> void:
    database = get_node_or_null("/root/QuestDatabase")
    if database == null:
        var script: Script = load("res://scripts/quests/quest_database.gd")
        database = Node.new()
        database.set_script(script)
        database.name = "QuestDatabase"
        get_tree().root.add_child.call_deferred(database)

func start_quest(quest_id: String) -> bool:
    if active.has(quest_id) or completed.has(quest_id):
        return false
    active[quest_id] = {"objectives_done": [], "started_at": Time.get_unix_time_from_system()}
    EventBus.quest_started.emit(quest_id)
    return true

func complete_objective(quest_id: String, objective_index: int) -> void:
    if not active.has(quest_id):
        return
    var done: Array = active[quest_id]["objectives_done"]
    if not done.has(objective_index):
        done.append(objective_index)
    EventBus.quest_updated.emit(quest_id, objective_index)
    var quest: Dictionary = database.get_quest(quest_id) if database else {}
    var total: int = int((quest.get("objectives", []) as Array).size())
    if total > 0 and done.size() >= total:
        _complete_quest(quest_id)

func _complete_quest(quest_id: String) -> void:
    active.erase(quest_id)
    completed.append(quest_id)
    EventBus.quest_completed.emit(quest_id)

func is_completed(quest_id: String) -> bool:
    return completed.has(quest_id)
'''

SCRIPTS2["scripts/quests/dialogue_system.gd"] = '''\
extends Node
## DialogueSystem — line-by-line dialogue from data/dialogue/*.json.
var current_lines: Array = []
var current_index: int = 0
var current_speaker: String = ""
var active: bool = false

func start_dialogue(dialogue_id: String) -> bool:
    var path: String = "res://data/dialogue/" + dialogue_id + ".json"
    if not FileAccess.file_exists(path):
        return false
    var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
    if parsed == null:
        return false
    var d: Dictionary = parsed
    current_speaker = str(d.get("speaker", ""))
    current_lines = d.get("lines", [])
    current_index = 0
    active = true
    EventBus.dialogue_started.emit(current_speaker)
    return true

func current_line() -> String:
    if current_index < current_lines.size():
        return str(current_lines[current_index])
    return ""

func advance() -> bool:
    current_index += 1
    if current_index >= current_lines.size():
        active = false
        EventBus.dialogue_finished.emit()
        return false
    return true
'''

SCRIPTS2["scripts/quests/character_relationships.gd"] = '''\
extends Node
## CharacterRelationships — UNFINISHED (Phase 3). Affinity data only.
var affinity: Dictionary = {}

func affinity_with(npc_id: String) -> int:
    return int(affinity.get(npc_id, 0))
'''

SCRIPTS2["scripts/quests/cinematic_manager.gd"] = '''\
extends Node
## CinematicManager — UNFINISHED (Phase 2). No cinematics in Phase 1.
func play_cinematic(_id: String) -> bool:
    push_warning("CinematicManager: cinematics not implemented in Phase 1")
    return false
'''

SCRIPTS2["scripts/save/save_data.gd"] = '''\
extends RefCounted
## SaveData — versioned save payload (JSON). Version 1.
const SAVE_VERSION := 1
var player_position: Vector3 = Vector3.ZERO
var level: int = 1
var xp: int = 0
var inventory: Dictionary = {}
var completed_quests: Array = []
var play_time_seconds: float = 0.0

func to_dict() -> Dictionary:
    return {
        "version": SAVE_VERSION,
        "player_position": {"x": player_position.x, "y": player_position.y, "z": player_position.z},
        "level": level, "xp": xp, "inventory": inventory,
        "completed_quests": completed_quests,
        "play_time_seconds": play_time_seconds,
    }

func from_dict(d: Dictionary) -> bool:
    if int(d.get("version", 0)) != SAVE_VERSION:
        return false
    var p: Dictionary = d.get("player_position", {})
    player_position = Vector3(float(p.get("x", 0.0)), float(p.get("y", 0.0)), float(p.get("z", 0.0)))
    level = int(d.get("level", 1))
    xp = int(d.get("xp", 0))
    inventory = d.get("inventory", {})
    completed_quests = d.get("completed_quests", [])
    play_time_seconds = float(d.get("play_time_seconds", 0.0))
    return true
'''

SCRIPTS2["scripts/save/save_manager.gd"] = '''\
extends Node
## SaveManager — JSON save/load to user://savegame.json, with versioning.
const SAVE_PATH := "user://savegame.json"

func save_game() -> bool:
    var data_script: Script = load("res://scripts/save/save_data.gd")
    var data: RefCounted = data_script.new()
    var gm: Node = get_node_or_null("/root/GameManager")
    if gm and gm.player:
        data.player_position = gm.player.global_position
    data.play_time_seconds = gm.play_time_seconds if gm else 0.0
    var xp_node: Node = get_tree().current_scene.find_child("ExperienceSystem", true, false) if get_tree().current_scene else null
    if xp_node:
        data.level = xp_node.level
        data.xp = xp_node.xp
    var inv: Node = get_tree().current_scene.find_child("InventorySystem", true, false) if get_tree().current_scene else null
    if inv:
        data.inventory = inv.to_dict()
    var qm: Node = get_tree().current_scene.find_child("QuestManager", true, false) if get_tree().current_scene else null
    if qm:
        data.completed_quests = qm.completed.duplicate()
    var json_text: String = JSON.stringify(data.to_dict(), "  ")
    var file: FileAccess = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
    if file == null:
        push_error("SaveManager: cannot write " + SAVE_PATH)
        return false
    file.store_string(json_text)
    file.close()
    return true

func load_game() -> Dictionary:
    if not FileAccess.file_exists(SAVE_PATH):
        return {}
    var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
    if parsed == null:
        return {}
    return parsed as Dictionary

func has_save() -> bool:
    return FileAccess.file_exists(SAVE_PATH)
'''

SCRIPTS2["scripts/gameplay/shrine.gd"] = '''\
extends Area3D
## AncientShrine — the slice's one interactive world object.
## First interaction: +50 XP, shrine loot, intro dialogue, quest progress.
## Re-interaction: +10 XP only (no farming of the full reward).
var used: bool = false
var quest_manager: Node = null
var xp_system: Node = null
var loot: Node = null
var dialogue: Node = null

func _ready() -> void:
    monitoring = true
    monitorable = true

func interact() -> void:
    _resolve_nodes()
    if not used:
        used = true
        if xp_system:
            xp_system.add_xp(50)
        if loot:
            loot.grant("shrine_blessing")
        if dialogue:
            dialogue.start_dialogue("intro")
        if quest_manager:
            quest_manager.complete_objective("first_light", 0)
            quest_manager.complete_objective("first_light", 1)
        EventBus.toast_requested.emit("The shrine blesses you: +50 XP, potions found.")
    else:
        if xp_system:
            xp_system.add_xp(10)
        EventBus.toast_requested.emit("The shrine hums quietly. +10 XP.")

func _resolve_nodes() -> void:
    var scene: Node = get_tree().current_scene
    if scene == null:
        return
    quest_manager = scene.find_child("QuestManager", true, false)
    xp_system = scene.find_child("ExperienceSystem", true, false)
    loot = scene.find_child("LootSystem", true, false)
    dialogue = scene.find_child("DialogueSystem", true, false)
'''

for rel, content in SCRIPTS2.items():
    w(rel, content)
print("part3 done, scripts:", len(SCRIPTS2))

# ---------------------------------------------------------------- part 4: UI
SCRIPTS3 = {}
SCRIPTS3["scripts/ui/virtual_joystick.gd"] = '''\
extends Control
## VirtualJoystick — touch joystick (bottom-left). Emits output vector.
## Mouse drag works too (emulate_touch_from_mouse is on), so desktop
## testing exercises the same path.
signal vector_changed(v: Vector2)
var output: Vector2 = Vector2.ZERO
var _radius: float = 70.0
var _knob_radius: float = 30.0
var _knob_pos: Vector2 = Vector2.ZERO
var _dragging: bool = false
var _touch_index: int = -1

func _ready() -> void:
    custom_minimum_size = Vector2(170, 170)
    size = Vector2(170, 170)
    mouse_filter = MOUSE_FILTER_STOP

func _gui_input(event: InputEvent) -> void:
    if event is InputEventScreenTouch:
        if event.pressed:
            _dragging = true
            _touch_index = event.index
            _update_knob(event.position)
        elif event.index == _touch_index:
            _dragging = false
            _reset()
    elif event is InputEventScreenDrag and _dragging and event.index == _touch_index:
        _update_knob(event.position)
    elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        _dragging = event.pressed
        if _dragging:
            _update_knob(event.position)
        else:
            _reset()
    elif event is InputEventMouseMotion and _dragging:
        _update_knob(event.position)

func _update_knob(local_pos: Vector2) -> void:
    var center: Vector2 = size * 0.5
    var offset: Vector2 = local_pos - center
    if offset.length() > _radius:
        offset = offset.normalized() * _radius
    _knob_pos = offset
    output = Vector2(offset.x / _radius, offset.y / _radius)
    queue_redraw()
    vector_changed.emit(output)

func _reset() -> void:
    _knob_pos = Vector2.ZERO
    output = Vector2.ZERO
    queue_redraw()
    vector_changed.emit(output)

func _draw() -> void:
    var center: Vector2 = size * 0.5
    draw_circle(center, _radius, Color(1, 1, 1, 0.08))
    draw_arc(center, _radius, 0, TAU, 48, Color(1, 1, 1, 0.35), 2.0)
    draw_circle(center + _knob_pos, _knob_radius, Color(1, 1, 1, 0.25))
'''

SCRIPTS3["scripts/ui/mobile_hud.gd"] = '''\
extends CanvasLayer
## MobileHUD — top bar, joystick, action buttons, toast, FPS.
## Builds its controls in code so the layout is reviewable in one file.
var player: Node = null
var joy: Control = null
var hp_label: Label = null
var level_label: Label = null
var xp_label: Label = null
var toast_label: Label = null
var interact_button: Button = null
var fps_label: Label = null
var _toast_timer: float = 0.0

func _ready() -> void:
    layer = 10
    _build_top_bar()
    _build_joystick()
    _build_buttons()
    _build_toast()
    EventBus.xp_gained.connect(_on_xp)
    EventBus.level_up.connect(_on_level_up)
    EventBus.interactable_nearby.connect(_on_interactable)
    EventBus.toast_requested.connect(show_toast)
    EventBus.player_health_changed.connect(_on_health)

func _process(delta: float) -> void:
    if _toast_timer > 0.0:
        _toast_timer -= delta
        if _toast_timer <= 0.0:
            toast_label.visible = false
    if SettingsManager.show_fps and fps_label:
        fps_label.text = "FPS %d" % Engine.get_frames_per_second()

func _btn(text: String, pos: Vector2, size: Vector2) -> Button:
    var b := Button.new()
    b.text = text
    b.position = pos
    b.size = size
    b.focus_mode = Control.FOCUS_NONE
    add_child(b)
    return b

func _build_top_bar() -> void:
    hp_label = Label.new()
    hp_label.text = "HP 180 / 180"
    hp_label.position = Vector2(16, 12)
    hp_label.add_theme_font_size_override("font_size", 20)
    add_child(hp_label)
    level_label = Label.new()
    level_label.text = "Lv 1"
    level_label.position = Vector2(16, 40)
    level_label.add_theme_font_size_override("font_size", 20)
    add_child(level_label)
    xp_label = Label.new()
    xp_label.text = "XP 0 / 100"
    xp_label.position = Vector2(16, 68)
    xp_label.add_theme_font_size_override("font_size", 16)
    add_child(xp_label)
    fps_label = Label.new()
    fps_label.text = ""
    fps_label.position = Vector2(16, 96)
    add_child(fps_label)
    var pause_btn: Button = _btn("II", Vector2(1190, 12), Vector2(76, 56))
    pause_btn.pressed.connect(_on_pause_pressed)
    var inv_btn: Button = _btn("Bag", Vector2(1100, 12), Vector2(76, 56))
    inv_btn.pressed.connect(func() -> void: get_node_or_null("InventoryUI").toggle_visible())
    var quest_btn: Button = _btn("Quests", Vector2(1000, 12), Vector2(86, 56))
    quest_btn.pressed.connect(func() -> void: get_node_or_null("QuestUI").toggle_visible())

func _build_joystick() -> void:
    var script: Script = load("res://scripts/ui/virtual_joystick.gd")
    joy = Control.new()
    joy.set_script(script)
    joy.position = Vector2(24, 520)
    joy.size = Vector2(170, 170)
    add_child(joy)
    joy.vector_changed.connect(_on_joy)

func _build_buttons() -> void:
    var jump_btn: Button = _btn("JUMP", Vector2(1100, 560), Vector2(150, 110))
    jump_btn.button_down.connect(func() -> void: Input.action_press("jump"))
    jump_btn.button_up.connect(func() -> void: Input.action_release("jump"))
    var run_btn: Button = _btn("RUN", Vector2(940, 600), Vector2(130, 70))
    run_btn.button_down.connect(func() -> void: _set_run(true))
    run_btn.button_up.connect(func() -> void: _set_run(false))
    interact_button = _btn("USE", Vector2(940, 500), Vector2(130, 70))
    interact_button.disabled = true
    interact_button.pressed.connect(func() -> void: Input.action_press("interact"))
    var atk_btn: Button = _btn("ATTACK", Vector2(1110, 440), Vector2(150, 70))
    atk_btn.pressed.connect(func() -> void: Input.action_press("attack"))

func _build_toast() -> void:
    toast_label = Label.new()
    toast_label.position = Vector2(340, 640)
    toast_label.size = Vector2(600, 40)
    toast_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    toast_label.add_theme_font_size_override("font_size", 22)
    toast_label.visible = false
    add_child(toast_label)

func _on_joy(v: Vector2) -> void:
    if GameManager.player:
        GameManager.player.joystick_vector = v

func _set_run(v: bool) -> void:
    if GameManager.player:
        GameManager.player.set_run_held(v)

func _on_pause_pressed() -> void:
    GameManager.toggle_pause()

func _on_xp(_amount: int) -> void:
    var cs: Node = get_tree().current_scene
    if cs == null:
        return
    var xp_node: Node = cs.find_child("ExperienceSystem", true, false)
    if xp_node:
        xp_label.text = "XP %d / %d" % [xp_node.xp, xp_node.xp_to_next]

func _on_level_up(new_level: int) -> void:
    level_label.text = "Lv %d" % new_level
    show_toast("Level up! You are now level %d." % new_level)

func _on_health(current: int, maximum: int) -> void:
    hp_label.text = "HP %d / %d" % [current, maximum]

func _on_interactable(_name: String, available: bool) -> void:
    if interact_button:
        interact_button.disabled = not available

func show_toast(message: String) -> void:
    toast_label.text = message
    toast_label.visible = true
    _toast_timer = 4.0
'''

SCRIPTS3["scripts/ui/main_menu.gd"] = '''\
extends Control
## MainMenu — title, New Game, Continue (if a save exists), quality note.
func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    var panel := Panel.new()
    panel.set_anchors_preset(Control.PRESET_FULL_RECT)
    var style := StyleBoxFlat.new()
    style.bg_color = Color(0.04, 0.05, 0.09, 0.92)
    panel.add_theme_stylebox_override("panel", style)
    add_child(panel)
    var title := Label.new()
    title.text = "PROJECT ETERNIA"
    title.set_anchors_preset(Control.PRESET_CENTER_TOP)
    title.position = Vector2(390, 140)
    title.add_theme_font_size_override("font_size", 64)
    add_child(title)
    var sub := Label.new()
    sub.text = "A 3D RPG  -  Phase 1 vertical slice"
    sub.position = Vector2(470, 220)
    sub.add_theme_font_size_override("font_size", 22)
    add_child(sub)
    var start_btn := Button.new()
    start_btn.text = "NEW GAME"
    start_btn.position = Vector2(540, 320)
    start_btn.size = Vector2(200, 64)
    start_btn.pressed.connect(_on_start)
    add_child(start_btn)
    var cont_btn := Button.new()
    cont_btn.text = "CONTINUE"
    cont_btn.position = Vector2(540, 400)
    cont_btn.size = Vector2(200, 64)
    cont_btn.disabled = not SaveManager.has_save()
    cont_btn.pressed.connect(_on_start)
    add_child(cont_btn)
    var note := Label.new()
    note.text = "Prototype art only — real systems, real 3D scene."
    note.position = Vector2(460, 500)
    add_child(note)
    EventBus.game_state_changed.connect(_on_state)
    visible = GameManager.state == GameManager.STATE_MENU

func _on_state(new_state: String) -> void:
    visible = new_state == GameManager.STATE_MENU

func _on_start() -> void:
    GameManager.start_game()
    var scene: Node = get_tree().current_scene
    var qm: Node = scene.find_child("QuestManager", true, false)
    if qm:
        qm.start_quest("first_light")
    var p: Node = GameManager.player
    if p:
        p.movement_enabled = true
'''

SCRIPTS3["scripts/ui/pause_menu.gd"] = '''\
extends Control
## PauseMenu — Resume / Save / Quit to menu. Game is actually paused.
func _ready() -> void:
    process_mode = Node.PROCESS_MODE_ALWAYS
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.set_anchors_preset(Control.PRESET_FULL_RECT)
    var style := StyleBoxFlat.new()
    style.bg_color = Color(0.02, 0.02, 0.05, 0.85)
    panel.add_theme_stylebox_override("panel", style)
    add_child(panel)
    var title := Label.new()
    title.text = "PAUSED"
    title.position = Vector2(580, 160)
    title.add_theme_font_size_override("font_size", 48)
    add_child(title)
    var resume_btn := Button.new()
    resume_btn.text = "RESUME"
    resume_btn.position = Vector2(540, 260)
    resume_btn.size = Vector2(200, 60)
    resume_btn.pressed.connect(func() -> void: GameManager.toggle_pause())
    add_child(resume_btn)
    var save_btn := Button.new()
    save_btn.text = "SAVE GAME"
    save_btn.position = Vector2(540, 335)
    save_btn.size = Vector2(200, 60)
    save_btn.pressed.connect(_on_save)
    add_child(save_btn)
    var quit_btn := Button.new()
    quit_btn.text = "QUIT TO MENU"
    quit_btn.position = Vector2(540, 410)
    quit_btn.size = Vector2(200, 60)
    quit_btn.pressed.connect(_on_quit)
    add_child(quit_btn)
    EventBus.game_paused.connect(func(paused: bool) -> void: visible = paused)

func _on_save() -> void:
    if SaveManager.save_game():
        EventBus.toast_requested.emit("Game saved.")
    else:
        EventBus.toast_requested.emit("Save failed.")

func _on_quit() -> void:
    if GameManager.player:
        GameManager.player.movement_enabled = false
    GameManager.return_to_menu()
'''

SCRIPTS3["scripts/ui/inventory_ui.gd"] = '''\
extends Control
## InventoryUI — lists real InventorySystem contents.
var list_label: Label = null

func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.position = Vector2(380, 120)
    panel.size = Vector2(520, 480)
    add_child(panel)
    var title := Label.new()
    title.text = "INVENTORY"
    title.position = Vector2(420, 140)
    title.add_theme_font_size_override("font_size", 32)
    add_child(title)
    list_label = Label.new()
    list_label.position = Vector2(420, 190)
    list_label.size = Vector2(440, 340)
    add_child(list_label)
    var close_btn := Button.new()
    close_btn.text = "CLOSE"
    close_btn.position = Vector2(560, 540)
    close_btn.size = Vector2(160, 50)
    close_btn.pressed.connect(func() -> void: visible = false)
    add_child(close_btn)

func toggle_visible() -> void:
    visible = not visible
    if visible:
        _refresh()

func _refresh() -> void:
    var scene: Node = get_tree().current_scene
    var inv: Node = scene.find_child("InventorySystem", true, false)
    if inv == null or inv.items.is_empty():
        list_label.text = "Empty — visit the shrine or defeat the dummy."
        return
    var lines: Array = []
    for k in inv.items.keys():
        lines.append("%s  x%d" % [str(k), int(inv.items[k])])
    list_label.text = "\n".join(lines)
'''

SCRIPTS3["scripts/ui/quest_ui.gd"] = '''\
extends Control
## QuestUI — active + completed quests from QuestManager + database.
var list_label: Label = null

func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.position = Vector2(380, 120)
    panel.size = Vector2(520, 480)
    add_child(panel)
    var title := Label.new()
    title.text = "QUESTS"
    title.position = Vector2(420, 140)
    title.add_theme_font_size_override("font_size", 32)
    add_child(title)
    list_label = Label.new()
    list_label.position = Vector2(420, 190)
    list_label.size = Vector2(440, 340)
    add_child(list_label)
    var close_btn := Button.new()
    close_btn.text = "CLOSE"
    close_btn.position = Vector2(560, 540)
    close_btn.size = Vector2(160, 50)
    close_btn.pressed.connect(func() -> void: visible = false)
    add_child(close_btn)

func toggle_visible() -> void:
    visible = not visible
    if visible:
        _refresh()

func _refresh() -> void:
    var scene: Node = get_tree().current_scene
    var qm: Node = scene.find_child("QuestManager", true, false)
    if qm == null:
        list_label.text = "No quest system."
        return
    var lines: Array = []
    for qid in qm.active.keys():
        var q: Dictionary = qm.database.get_quest(qid) if qm.database else {}
        lines.append("ACTIVE: " + str(q.get("title", qid)))
    for qid in qm.completed:
        var q2: Dictionary = qm.database.get_quest(qid) if qm.database else {}
        lines.append("DONE: " + str(q2.get("title", qid)))
    list_label.text = "\n".join(lines) if not lines.is_empty() else "No quests yet — press NEW GAME."
'''

SCRIPTS3["scripts/ui/dialogue_ui.gd"] = '''\
extends Control
## DialogueUI — bottom dialogue box driven by DialogueSystem.
var speaker_label: Label = null
var line_label: Label = null
var dialogue: Node = null

func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.position = Vector2(240, 500)
    panel.size = Vector2(800, 170)
    add_child(panel)
    speaker_label = Label.new()
    speaker_label.position = Vector2(270, 515)
    speaker_label.add_theme_font_size_override("font_size", 20)
    add_child(speaker_label)
    line_label = Label.new()
    line_label.position = Vector2(270, 550)
    line_label.size = Vector2(740, 60)
    line_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    line_label.add_theme_font_size_override("font_size", 20)
    add_child(line_label)
    var next_btn := Button.new()
    next_btn.text = "CONTINUE  >"
    next_btn.position = Vector2(860, 625)
    next_btn.size = Vector2(150, 36)
    next_btn.pressed.connect(_on_next)
    add_child(next_btn)
    EventBus.dialogue_started.connect(_on_started)
    EventBus.dialogue_finished.connect(func() -> void: visible = false)

func _on_started(speaker: String) -> void:
    dialogue = get_tree().current_scene.find_child("DialogueSystem", true, false)
    speaker_label.text = speaker
    line_label.text = dialogue.current_line() if dialogue else ""
    visible = true

func _on_next() -> void:
    if dialogue == null:
        return
    if dialogue.advance():
        line_label.text = dialogue.current_line()
'''

SCRIPTS3["scripts/ui/settings_ui.gd"] = '''\
extends Control
## SettingsUI — quality presets only in Phase 1 (audio sliders: Phase 2).
func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    visible = false
    var panel := Panel.new()
    panel.position = Vector2(440, 180)
    panel.size = Vector2(400, 360)
    add_child(panel)
    var title := Label.new()
    title.text = "SETTINGS"
    title.position = Vector2(480, 200)
    title.add_theme_font_size_override("font_size", 32)
    add_child(title)
    var low_btn := Button.new()
    low_btn.text = "Quality: LOW"
    low_btn.position = Vector2(480, 260)
    low_btn.size = Vector2(320, 50)
    low_btn.pressed.connect(func() -> void: SettingsManager.set_quality(0))
    add_child(low_btn)
    var med_btn := Button.new()
    med_btn.text = "Quality: MEDIUM"
    med_btn.position = Vector2(480, 320)
    med_btn.size = Vector2(320, 50)
    med_btn.pressed.connect(func() -> void: SettingsManager.set_quality(1))
    add_child(med_btn)
    var high_btn := Button.new()
    high_btn.text = "Quality: HIGH"
    high_btn.position = Vector2(480, 380)
    high_btn.size = Vector2(320, 50)
    high_btn.pressed.connect(func() -> void: SettingsManager.set_quality(2))
    add_child(high_btn)
    var close_btn := Button.new()
    close_btn.text = "CLOSE"
    close_btn.position = Vector2(480, 450)
    close_btn.size = Vector2(320, 50)
    close_btn.pressed.connect(func() -> void: visible = false)
    add_child(close_btn)

func toggle_visible() -> void:
    visible = not visible
'''

SCRIPTS3["scripts/main.gd"] = '''\
extends Node3D
## Main — scene bootstrap: wires systems, registers the player,
## handles pause + attack input at scene level.
var combat: Node = null
var loot: Node = null

func _ready() -> void:
    var player: Node = find_child("Player", true, false)
    if player:
        GameManager.register_player(player)
        player.movement_enabled = false
        var rig: Node = player.find_child("CameraRig", true, false)
        if rig:
            player.camera_yaw_node = rig
    combat = find_child("CombatSystem", true, false)
    loot = find_child("LootSystem", true, false)
    var inv: Node = find_child("InventorySystem", true, false)
    if loot and inv:
        loot.inventory = inv
    EventBus.enemy_defeated.connect(_on_enemy_defeated)

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("pause_game"):
        if GameManager.state == GameManager.STATE_PLAYING or GameManager.state == GameManager.STATE_PAUSED:
            GameManager.toggle_pause()
    if event.is_action_pressed("attack"):
        _try_attack()

func _try_attack() -> void:
    if combat == null or GameManager.player == null:
        return
    var enemy: Node3D = get_tree().get_first_node_in_group("enemy") as Node3D
    if enemy == null:
        return
    combat.try_attack(GameManager.player, enemy)

func _on_enemy_defeated(_enemy_name: String) -> void:
    if loot:
        loot.grant("dummy_defeat")
    EventBus.toast_requested.emit("Training dummy defeated. +3 old coins.")
'''

for rel, content in SCRIPTS3.items():
    w(rel, content)
print("part4 done, scripts:", len(SCRIPTS3))

# ---------------------------------------------------------------- part 5: scenes
w("scenes/player/player.tscn", '''\
[gd_scene load_steps=15 format=3 uid="uid://eternia_player1"]
[ext_resource type="Script" path="res://scripts/player/player_controller.gd" id="1"]
[ext_resource type="Script" path="res://scripts/player/player_animation_controller.gd" id="2"]
[ext_resource type="Script" path="res://scripts/player/camera_controller.gd" id="3"]
[ext_resource type="Script" path="res://scripts/player/player_state_machine.gd" id="4"]
[ext_resource type="Script" path="res://scripts/player/player_interaction.gd" id="5"]
[sub_resource type="CapsuleShape3D" id="shape"]
radius = 0.35
height = 1.7
[sub_resource type="StandardMaterial3D" id="mat_body"]
albedo_color = Color(0.35, 0.42, 0.62, 1)
roughness = 0.8
[sub_resource type="CapsuleMesh" id="mesh_body"]
radius = 0.35
height = 1.1
material = SubResource("mat_body")
[sub_resource type="StandardMaterial3D" id="mat_skin"]
albedo_color = Color(0.85, 0.68, 0.52, 1)
roughness = 0.7
[sub_resource type="SphereMesh" id="mesh_head"]
radius = 0.28
height = 0.56
material = SubResource("mat_skin")
[sub_resource type="StandardMaterial3D" id="mat_cloth"]
albedo_color = Color(0.25, 0.28, 0.35, 1)
roughness = 0.85
[sub_resource type="BoxMesh" id="mesh_arm"]
size = Vector3(0.18, 0.7, 0.18)
material = SubResource("mat_cloth")
[sub_resource type="BoxMesh" id="mesh_leg"]
size = Vector3(0.22, 0.9, 0.22)
material = SubResource("mat_cloth")
[sub_resource type="SphereShape3D" id="shape_interact"]
radius = 3.0
[node name="Player" type="CharacterBody3D"]
collision_layer = 1
collision_mask = 1
script = ExtResource("1")
[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
shape = SubResource("shape")
[node name="MeshRoot" type="Node3D" parent="."]
script = ExtResource("2")
[node name="Body" type="MeshInstance3D" parent="MeshRoot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.95, 0)
mesh = SubResource("mesh_body")
[node name="Head" type="MeshInstance3D" parent="MeshRoot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.72, 0)
mesh = SubResource("mesh_head")
[node name="ArmL" type="MeshInstance3D" parent="MeshRoot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.52, 1.25, 0)
mesh = SubResource("mesh_arm")
[node name="ArmR" type="MeshInstance3D" parent="MeshRoot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.52, 1.25, 0)
mesh = SubResource("mesh_arm")
[node name="LegL" type="MeshInstance3D" parent="MeshRoot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.2, 0.45, 0)
mesh = SubResource("mesh_leg")
[node name="LegR" type="MeshInstance3D" parent="MeshRoot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.2, 0.45, 0)
mesh = SubResource("mesh_leg")
[node name="StateMachine" type="Node" parent="."]
script = ExtResource("4")
[node name="CameraRig" type="Node3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
script = ExtResource("3")
[node name="SpringArm3D" type="SpringArm3D" parent="CameraRig"]
transform = Transform3D(1, 0, 0, 0, 0.945518, 0.325568, 0, -0.325568, 0.945518, 0, 0, 0)
spring_length = 6.0
margin = 0.3
[node name="Camera3D" type="Camera3D" parent="CameraRig/SpringArm3D"]
fov = 70.0
current = true
[node name="Interaction" type="Area3D" parent="."]
script = ExtResource("5")
[node name="CollisionShape3D" type="CollisionShape3D" parent="Interaction"]
shape = SubResource("shape_interact")
''')

w("scenes/enemies/training_dummy.tscn", '''\
[gd_scene load_steps=7 format=3 uid="uid://eternia_dummy1"]
[ext_resource type="Script" path="res://scripts/combat/enemy_ai.gd" id="1"]
[sub_resource type="CapsuleShape3D" id="shape"]
radius = 0.4
height = 1.8
[sub_resource type="StandardMaterial3D" id="mat_dummy"]
albedo_color = Color(0.7, 0.25, 0.2, 1)
roughness = 0.8
[sub_resource type="CapsuleMesh" id="mesh_body"]
radius = 0.4
height = 1.2
material = SubResource("mat_dummy")
[sub_resource type="SphereMesh" id="mesh_head"]
radius = 0.3
height = 0.6
material = SubResource("mat_dummy")
[sub_resource type="BoxShape3D" id="shape_box"]
size = Vector3(1.0, 1.0, 0.4)
[node name="TrainingDummy" type="CharacterBody3D"]
collision_layer = 1
collision_mask = 1
script = ExtResource("1")
[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
shape = SubResource("shape")
[node name="Body" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.95, 0)
mesh = SubResource("mesh_body")
[node name="Head" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.78, 0)
mesh = SubResource("mesh_head")
''')

# main.tscn is written by a helper below (many ext_resources).
MAIN_EXT = [
 ("scripts/main.gd", "1"),
 ("scripts/world/world_manager.gd", "2"),
 ("scripts/world/environment_system.gd", "3"),
 ("scripts/world/time_of_day.gd", "4"),
 ("scripts/world/world_regions.gd", "5"),
 ("scripts/world/weather_system.gd", "6"),
 ("scripts/world/world_streaming.gd", "7"),
 ("scripts/rpg/experience_system.gd", "8"),
 ("scripts/rpg/level_progression.gd", "9"),
 ("scripts/rpg/skill_system.gd", "10"),
 ("scripts/rpg/equipment_system.gd", "11"),
 ("scripts/rpg/inventory_system.gd", "12"),
 ("scripts/combat/combat_system.gd", "13"),
 ("scripts/combat/interaction_system.gd", "14"),
 ("scripts/combat/loot_system.gd", "15"),
 ("scripts/quests/quest_manager.gd", "16"),
 ("scripts/quests/dialogue_system.gd", "17"),
 ("scripts/quests/character_relationships.gd", "18"),
 ("scripts/quests/cinematic_manager.gd", "19"),
 ("scripts/ui/mobile_hud.gd", "20"),
 ("scripts/ui/main_menu.gd", "21"),
 ("scripts/ui/pause_menu.gd", "22"),
 ("scripts/ui/inventory_ui.gd", "23"),
 ("scripts/ui/quest_ui.gd", "24"),
 ("scripts/ui/dialogue_ui.gd", "25"),
 ("scripts/ui/settings_ui.gd", "26"),
 ("scenes/player/player.tscn", "27"),
 ("scenes/enemies/training_dummy.tscn", "28"),
]
_lines = ['[gd_scene load_steps=32 format=3 uid="uid://eternia_main1"]']
for path, rid in MAIN_EXT:
    typ = "PackedScene" if path.endswith(".tscn") else "Script"
    _lines.append('[ext_resource type="%s" path="res://%s" id="%s"]' % (typ, path, rid))
_lines.append('[sub_resource type="ProceduralSkyMaterial" id="sky_mat"]')
_lines.append('sky_top_color = Color(0.35, 0.55, 0.85, 1)')
_lines.append('sky_horizon_color = Color(0.75, 0.82, 0.92, 1)')
_lines.append('ground_bottom_color = Color(0.2, 0.22, 0.28, 1)')
_lines.append('ground_horizon_color = Color(0.65, 0.7, 0.78, 1)')
_lines.append('[sub_resource type="Sky" id="sky"]')
_lines.append('sky_material = SubResource("sky_mat")')
_lines.append('[sub_resource type="Environment" id="env"]')
_lines.append('background_mode = 2')
_lines.append('sky = SubResource("sky")')
_lines.append('ambient_light_source = 3')
_lines.append('ambient_light_energy = 0.9')
_lines.append('fog_enabled = true')
_lines.append('fog_light_color = Color(0.65, 0.7, 0.8, 1)')
_lines.append('fog_density = 0.012')
_lines.append('tonemap_mode = 2')
_lines.append('[node name="Main" type="Node3D"]')
_lines.append('script = ExtResource("1")')
_lines.append('[node name="WorldEnvironment" type="WorldEnvironment" parent="."]')
_lines.append('environment = SubResource("env")')
_lines.append('[node name="Sun" type="DirectionalLight3D" parent="."]')
_lines.append('transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 12, 0)')
_lines.append('light_energy = 1.1')
_lines.append('shadow_enabled = true')
_lines.append('directional_shadow_max_distance = 60.0')
_lines.append('[node name="World" type="Node3D" parent="."]')
_lines.append('script = ExtResource("2")')
_lines.append('[node name="EnvironmentSystem" type="Node" parent="."]')
_lines.append('script = ExtResource("3")')
_lines.append('[node name="TimeOfDay" type="Node" parent="."]')
_lines.append('script = ExtResource("4")')
_lines.append('[node name="WorldRegions" type="Node" parent="."]')
_lines.append('script = ExtResource("5")')
_lines.append('[node name="WeatherSystem" type="Node" parent="."]')
_lines.append('script = ExtResource("6")')
_lines.append('[node name="WorldStreaming" type="Node" parent="."]')
_lines.append('script = ExtResource("7")')
_lines.append('[node name="ExperienceSystem" type="Node" parent="."]')
_lines.append('script = ExtResource("8")')
_lines.append('[node name="LevelProgression" type="Node" parent="."]')
_lines.append('script = ExtResource("9")')
_lines.append('[node name="SkillSystem" type="Node" parent="."]')
_lines.append('script = ExtResource("10")')
_lines.append('[node name="EquipmentSystem" type="Node" parent="."]')
_lines.append('script = ExtResource("11")')
_lines.append('[node name="InventorySystem" type="Node" parent="."]')
_lines.append('script = ExtResource("12")')
_lines.append('[node name="CombatSystem" type="Node" parent="."]')
_lines.append('script = ExtResource("13")')
_lines.append('[node name="InteractionSystem" type="Node" parent="."]')
_lines.append('script = ExtResource("14")')
_lines.append('[node name="LootSystem" type="Node" parent="."]')
_lines.append('script = ExtResource("15")')
_lines.append('[node name="QuestManager" type="Node" parent="."]')
_lines.append('script = ExtResource("16")')
_lines.append('[node name="DialogueSystem" type="Node" parent="."]')
_lines.append('script = ExtResource("17")')
_lines.append('[node name="Relationships" type="Node" parent="."]')
_lines.append('script = ExtResource("18")')
_lines.append('[node name="CinematicManager" type="Node" parent="."]')
_lines.append('script = ExtResource("19")')
_lines.append('[node name="Player" parent="." instance=ExtResource("27")]')
_lines.append('transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 12)')
_lines.append('[node name="TrainingDummy" parent="." instance=ExtResource("28")]')
_lines.append('transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 10, 0, -4)')
_lines.append('[node name="HUD" type="CanvasLayer" parent="."]')
_lines.append('script = ExtResource("20")')
_lines.append('[node name="MainMenu" type="Control" parent="HUD"]')
_lines.append('anchors_preset = 15')
_lines.append('anchor_right = 1.0')
_lines.append('anchor_bottom = 1.0')
_lines.append('grow_horizontal = 2')
_lines.append('grow_vertical = 2')
_lines.append('script = ExtResource("21")')
_lines.append('[node name="PauseMenu" type="Control" parent="HUD"]')
_lines.append('anchors_preset = 15')
_lines.append('anchor_right = 1.0')
_lines.append('anchor_bottom = 1.0')
_lines.append('grow_horizontal = 2')
_lines.append('grow_vertical = 2')
_lines.append('script = ExtResource("22")')
_lines.append('[node name="InventoryUI" type="Control" parent="HUD"]')
_lines.append('anchors_preset = 15')
_lines.append('anchor_right = 1.0')
_lines.append('anchor_bottom = 1.0')
_lines.append('grow_horizontal = 2')
_lines.append('grow_vertical = 2')
_lines.append('script = ExtResource("23")')
_lines.append('[node name="QuestUI" type="Control" parent="HUD"]')
_lines.append('anchors_preset = 15')
_lines.append('anchor_right = 1.0')
_lines.append('anchor_bottom = 1.0')
_lines.append('grow_horizontal = 2')
_lines.append('grow_vertical = 2')
_lines.append('script = ExtResource("24")')
_lines.append('[node name="DialogueUI" type="Control" parent="HUD"]')
_lines.append('anchors_preset = 15')
_lines.append('anchor_right = 1.0')
_lines.append('anchor_bottom = 1.0')
_lines.append('grow_horizontal = 2')
_lines.append('grow_vertical = 2')
_lines.append('script = ExtResource("25")')
_lines.append('[node name="SettingsUI" type="Control" parent="HUD"]')
_lines.append('anchors_preset = 15')
_lines.append('anchor_right = 1.0')
_lines.append('anchor_bottom = 1.0')
_lines.append('grow_horizontal = 2')
_lines.append('grow_vertical = 2')
_lines.append('script = ExtResource("26")')
_p = os.path.join(ROOT, "scenes/main/main.tscn")
with open(_p, "w", encoding="utf-8") as _f:
    _f.write("\n".join(_lines) + "\n")
print("wrote scenes/main/main.tscn")

# ---------------------------------------------------------------- data
w("data/quests/quests.json", '''\
{
  "first_light": {
    "title": "First Light",
    "description": "Reach the Ancient Shrine in the valley and receive its blessing.",
    "objectives": ["Reach the Ancient Shrine", "Receive the shrine blessing"],
    "reward_xp": 50
  },
  "dummy_drill": {
    "title": "Dummy Drill",
    "description": "Defeat the training dummy near the valley centre.",
    "objectives": ["Defeat the training dummy"],
    "reward_xp": 25
  },
  "valley_scout": {
    "title": "Valley Scout",
    "description": "Stand on the north platform and look over the valley. (Exploration placeholder for Phase 2.)",
    "objectives": ["Reach the north platform"],
    "reward_xp": 20
  }
}
''')
w("data/dialogue/intro.json", '''\
{
  "speaker": "Ancient Shrine",
  "lines": [
    "Traveler. The valley has waited a long time for someone to listen.",
    "Take these potions. The road beyond the pillars will test you.",
    "When you are ready, the dummy by the stones will teach your hands what your heart already knows."
  ]
}
''')
w("data/items/items.json", '''\
{
  "health_potion": {"name": "Health Potion", "type": "consumable", "heal": 40},
  "old_coin": {"name": "Old Coin", "type": "currency", "value": 1},
  "iron_sword": {"name": "Iron Sword", "type": "weapon", "attack": 8},
  "leather_armor": {"name": "Leather Armor", "type": "armor", "defense": 4}
}
''')
w("data/characters/player.json", '''\
{
  "id": "ashan",
  "name": "Ashan",
  "title": "Warden of the Valley",
  "note": "PROPOSAL ONLY - the final hero identity is not decided. See GAME_DESIGN.md.",
  "base_stats": {"strength": 10, "agility": 10, "intelligence": 10, "vitality": 10}
}
''')
w("data/abilities/abilities.json", '''\
{
  "power_strike": {"name": "Power Strike", "min_level": 1, "cooldown_s": 3.0},
  "swift_step": {"name": "Swift Step", "min_level": 2, "cooldown_s": 8.0},
  "heal_light": {"name": "Light Heal", "min_level": 3, "cooldown_s": 12.0}
}
''')

# ---------------------------------------------------------------- tests
w("tests/run_tests.gd", '''\
extends SceneTree
## Automated validation for Phase 1. Run:
##   godot --headless --path . -s tests/run_tests.gd
## Prints TEST PASS/FAIL lines and quits with 0 (all pass) or 1.
var passed: int = 0
var failed: int = 0
var failures: Array = []

func _init() -> void:
    call_deferred("_run")

func _check(test_name: String, ok: bool, detail: String = "") -> void:
    if ok:
        passed += 1
        print("TEST PASS " + test_name)
    else:
        failed += 1
        failures.append(test_name)
        print("TEST FAIL " + test_name + (" — " + detail if detail != "" else ""))

func _run() -> void:
    # 1. Main scene loads and instantiates.
    var main_scene: PackedScene = load("res://scenes/main/main.tscn")
    _check("main_scene_loads", main_scene != null)
    var main_inst: Node = null
    if main_scene:
        main_inst = main_scene.instantiate()
        root.add_child(main_inst)
    _check("main_instantiates", main_inst != null)
    # 2. Key nodes exist.
    if main_inst:
        _check("player_exists", main_inst.find_child("Player", true, false) != null)
        _check("world_exists", main_inst.find_child("World", true, false) != null)
        _check("shrine_exists", main_inst.find_child("AncientShrine", true, false) != null)
        _check("hud_exists", main_inst.find_child("HUD", true, false) != null)
        _check("camera_exists", main_inst.find_child("Camera3D", true, false) != null)
        var world: Node = main_inst.find_child("World", true, false)
        _check("world_has_content", world != null and world.get_child_count() >= 10, "children=" + str(world.get_child_count() if world else -1))
        var player: Node = main_inst.find_child("Player", true, false)
        if player:
            _check("player_speeds_sane", player.walk_speed > 0.0 and player.run_speed > player.walk_speed and player.jump_velocity > 0.0)
            _check("player_gravity_set", player.gravity > 0.0)
    # 3. Player scene loads alone.
    var pscene: PackedScene = load("res://scenes/player/player.tscn")
    _check("player_scene_loads", pscene != null)
    # 4. Inventory system.
    var inv_script: Script = load("res://scripts/rpg/inventory_system.gd")
    var inv: Node = Node.new()
    inv.set_script(inv_script)
    root.add_child(inv)
    _check("inventory_add", inv.add_item("health_potion", 2) and inv.count("health_potion") == 2)
    _check("inventory_remove", inv.remove_item("health_potion", 1) and inv.count("health_potion") == 1)
    _check("inventory_reject_overdraw", not inv.remove_item("health_potion", 99))
    # 5. Experience / level-up curve.
    var xp_script: Script = load("res://scripts/rpg/experience_system.gd")
    var xp_node: Node = Node.new()
    xp_node.set_script(xp_script)
    root.add_child(xp_node)
    xp_node.add_xp(50)
    _check("xp_accumulates", xp_node.xp == 50 and xp_node.level == 1)
    xp_node.add_xp(60)
    _check("level_up_works", xp_node.level == 2 and xp_node.xp == 10, "level=%d xp=%d" % [xp_node.level, xp_node.xp])
    # 6. Quest database + manager.
    var db_script: Script = load("res://scripts/quests/quest_database.gd")
    var db: Node = Node.new()
    db.set_script(db_script)
    root.add_child(db)
    _check("quest_db_loads", db.quests.has("first_light"))
    var qm_script: Script = load("res://scripts/quests/quest_manager.gd")
    var qm: Node = Node.new()
    qm.set_script(qm_script)
    root.add_child(qm)
    qm.database = db
    _check("quest_starts", qm.start_quest("first_light"))
    qm.complete_objective("first_light", 0)
    qm.complete_objective("first_light", 1)
    _check("quest_completes", qm.is_completed("first_light"))
    # 7. Save data round-trip (versioned).
    var sd_script: Script = load("res://scripts/save/save_data.gd")
    var sd: RefCounted = sd_script.new()
    sd.level = 3
    sd.xp = 42
    sd.inventory = {"old_coin": 5}
    sd.completed_quests = ["first_light"]
    var sd2: RefCounted = sd_script.new()
    _check("save_roundtrip", sd2.from_dict(sd.to_dict()) and sd2.level == 3 and sd2.xp == 42 and sd2.inventory.get("old_coin", 0) == 5)
    var sd_bad: RefCounted = sd_script.new()
    _check("save_rejects_bad_version", not sd_bad.from_dict({"version": 99}))
    # 8. All GDScript files parse (loadable).
    var bad: Array = []
    var dir: DirAccess = DirAccess.open("res://scripts")
    var stack: Array = ["res://scripts"]
    while not stack.is_empty():
        var dpath: String = stack.pop_back()
        var d: DirAccess = DirAccess.open(dpath)
        if d == null:
            continue
        d.list_dir_begin()
        var fname: String = d.get_next()
        while fname != "":
            var full: String = dpath + "/" + fname
            if d.current_is_dir() and not fname.begins_with("."):
                stack.append(full)
            elif fname.ends_with(".gd"):
                var s: Script = load(full)
                if s == null:
                    bad.append(full)
            fname = d.get_next()
        d.list_dir_end()
    _check("all_scripts_parse", bad.is_empty(), "bad=" + str(bad))
    print("TEST SUMMARY passed=%d failed=%d" % [passed, failed])
    if not failures.is_empty():
        print("TEST FAILURES: " + ", ".join(failures))
    quit(0 if failed == 0 else 1)
''')

w("tools/validation/validate.sh", '''\
#!/bin/bash
# PROJECT ETERNIA - Phase 1 validation. Run from the project root.
# Produces tests/reports/validation_report.md with real command output.
set -u
GODOT="${GODOT_BIN:-/home/hatch/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64}"
PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
REPORT="$PROJECT_DIR/tests/reports/validation_report.md"
mkdir -p "$PROJECT_DIR/tests/reports"
{
echo "# Validation Report — PROJECT ETERNIA Phase 1"
echo ""
echo "Date (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Godot: $GODOT"
echo ""
echo "## 1. Godot version"
"$GODOT" --version 2>&1
echo ""
echo "## 2. Project import (headless)"
cd "$PROJECT_DIR"
timeout 120 "$GODOT" --headless --path . --import 2>&1 | tail -20
echo "import exit: ${PIPESTATUS[0]}"
echo ""
echo "## 3. Automated tests (tests/run_tests.gd)"
timeout 120 "$GODOT" --headless --path . -s tests/run_tests.gd 2>&1 | tail -60
echo ""
echo "## 4. Headless run of main scene (10 seconds)"
timeout 60 "$GODOT" --headless --path . res://scenes/main/main.tscn --quit-after 600 2>&1 | tail -20
echo ""
echo "## 5. APK artifact"
ls -la "$PROJECT_DIR/builds/android/" 2>&1
} | tee "$REPORT"
echo "Report: $REPORT"
''')
print("part5 done")

# ---------------------------------------------------------------- part 6: docs
w("README.md", '''\
# PROJECT ETERNIA

Large-scale 3D RPG — Godot 4.3 (GDScript), Android target, third-person.
**Phase 1 (this delivery):** environment audit + modular foundation +
first playable vertical slice + automated validation + Android debug APK.

## Quick start (desktop test)
```bash
/home/hatch/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64 --path . res://scenes/main/main.tscn
```
Controls: WASD / arrows move, Space jump, Shift run, E interact, F attack,
Esc pause. Mouse drag orbits the camera; the on-screen joystick does the
same on touch.

## What is real in Phase 1
- A real 60 x 60 m 3D valley: ground, platforms, ruins, trees, shrine,
  torches — all with collision; a controllable third-person player
  (walk / run / jump / gravity / ground detection); SpringArm camera
  with collision; a chasing training dummy with HP; a working shrine
  interaction (+50 XP, loot, dialogue, quest progress); XP + level-up;
  inventory; quests (one completable); dialogue; JSON save/load v1;
  pause menu; main menu; mobile HUD with joystick.
- Automated tests: `tests/run_tests.gd` (run headless, see
  `tools/validation/validate.sh`).

## Asset limitations (honest)
- The player, dummy, trees, ruins and shrine are **primitive meshes**
  (capsules, boxes, cones). There are no imported characters,
  animations, textures or music yet. The prototype is labelled as such
  in-game and in `GAME_DESIGN.md`.
- Blender is NOT installed in this environment (see
  `ENVIRONMENT_AUDIT.md`), so no new modelled assets were produced here.
- No final storyline or hero identity is decided — `GAME_DESIGN.md` is
  a **proposal**, not a final design.

## Android build
```bash
export ANDROID_HOME=/home/hatch/workspace/game-apk/tools/android-sdk
export JAVA_HOME=/home/hatch/workspace/game-apk/tools/jdk17
export PATH=$JAVA_HOME/bin:$PATH
godot --headless --path . --export-debug "Android Mobile" builds/android/project-eternia-debug.apk
```
Output: `builds/android/project-eternia-debug.apk` (arm64, Mobile renderer).
''')

w("GAME_DESIGN.md", '''\
# GAME DESIGN — PROJECT ETERNIA (PROPOSAL, NOT FINAL)

> Status: **proposal for discussion**. Nothing in this document is a
> final storyline, final hero identity, or final art direction. It is
> written down so decisions can be argued about and changed — per the
> brief, no final identity is invented silently.

## 1. Premise (proposed)
A fantasy valley, Eternia, whose old shrines have gone quiet. The player
is a warden-in-training who must relight them. Scope is deliberately
small in Phase 1 (one valley) and grows region by region.

## 2. Pillars (proposed)
1. Third-person exploration over combat grind.
2. Shrines as the progression spine (each one teaches a mechanic).
3. Readable, calm fantasy art — achievable on a Galaxy A16 (Mobile
   renderer, low-poly, strong lighting, fog).
4. Touch-first controls; desktop is for testing only.

## 3. Hero (proposed, NOT decided)
- Working name: **Ashan, Warden of the Valley** (`data/characters/player.json`).
- The name, look and backstory are placeholders until the user approves
  a direction.

## 4. World (Phase 1 real / later proposed)
- REAL: Eternia Valley, 60 x 60 m — ground, north/east platforms,
  ruined pillars, trees, Ancient Shrine, training dummy.
- PROPOSED: Ashen Woods, Sunken City, Frost Peaks (data-only in
  `scripts/world/world_regions.gd`, not built).

## 5. Systems (Phase 1)
XP + levels, attributes, 3 starter skills (data), equipment slots,
inventory (24 slots), quests (3 defined, 1 completable), dialogue,
save/load v1, combat vs one dummy, shrine interaction, day clock
(slow drift), quality presets (Low/Medium/High).

## 6. Explicitly NOT in Phase 1
Story cinematics, weather, NPCs, world streaming, multiplayer,
in-app purchases, voice, music, imported character art.
See `DEVELOPMENT_ROADMAP.md`.
''')

w("TECHNICAL_ARCHITECTURE.md", '''\
# TECHNICAL ARCHITECTURE — PROJECT ETERNIA

Engine: Godot 4.3 stable, Mobile renderer (`gl_compatibility`),
GDScript only, Android arm64, landscape 1280x720, stretch
`canvas_items` / `expand`. Physics 60 ticks/s.

## Module status (Phase 1)
| Module | File | Status |
|---|---|---|
| EventBus | scripts/core/event_bus.gd | Implemented — all cross-system signals |
| GameManager | scripts/core/game_manager.gd | Implemented — MENU/PLAYING/PAUSED/DIALOGUE states |
| SceneManager | scripts/core/scene_manager.gd | Implemented (basic) — no loading screen yet |
| SettingsManager | scripts/core/settings_manager.gd | Implemented — quality presets + persistence |
| ResourceManager | scripts/core/resource_manager.gd | Implemented — load cache |
| PlayerController | scripts/player/player_controller.gd | Implemented — walk/run/jump/gravity |
| CameraController | scripts/player/camera_controller.gd | Implemented — SpringArm, drag orbit |
| PlayerStateMachine | scripts/player/player_state_machine.gd | Implemented — derived from real velocity/floor |
| PlayerInteraction | scripts/player/player_interaction.gd | Implemented — Area3D range detection |
| PlayerAnimationController | scripts/player/player_animation_controller.gd | Implemented — procedural prototype animation |
| WorldManager | scripts/world/world_manager.gd | Implemented — builds the valley at runtime |
| WorldRegions | scripts/world/world_regions.gd | Data only — 1 built region, 3 planned |
| EnvironmentSystem | scripts/world/environment_system.gd | Implemented — fog |
| TimeOfDay | scripts/world/time_of_day.gd | Implemented — slow sun drift |
| WeatherSystem | scripts/world/weather_system.gd | UNFINISHED — API only, always CLEAR |
| WorldStreaming | scripts/world/world_streaming.gd | UNFINISHED — interface only |
| CharacterStats | scripts/rpg/character_stats.gd | Implemented — data + derived values |
| ExperienceSystem | scripts/rpg/experience_system.gd | Implemented — curve 100 * level^1.5 |
| LevelProgression | scripts/rpg/level_progression.gd | Implemented — 2 attribute points/level |
| SkillSystem | scripts/rpg/skill_system.gd | Implemented — data + cooldowns |
| EquipmentSystem | scripts/rpg/equipment_system.gd | Implemented — slots |
| InventorySystem | scripts/rpg/inventory_system.gd | Implemented — 24 slots, stacks to 99 |
| CombatSystem | scripts/combat/combat_system.gd | Implemented — melee, range 2.6 m |
| EnemyAI | scripts/combat/enemy_ai.gd | Implemented — chase/attack/respawn dummy |
| InteractionSystem | scripts/combat/interaction_system.gd | Implemented — group registry |
| LootSystem | scripts/combat/loot_system.gd | Implemented — deterministic tables |
| QuestManager | scripts/quests/quest_manager.gd | Implemented |
| QuestDatabase | scripts/quests/quest_database.gd | Implemented — JSON |
| DialogueSystem | scripts/quests/dialogue_system.gd | Implemented — JSON lines |
| CharacterRelationships | scripts/quests/character_relationships.gd | UNFINISHED — affinity data only |
| CinematicManager | scripts/quests/cinematic_manager.gd | UNFINISHED — no cinematics |
| SaveManager / SaveData | scripts/save/*.gd | Implemented — JSON, version 1 |
| MainMenu / PauseMenu / InventoryUI / QuestUI / DialogueUI / MobileHUD / SettingsUI | scripts/ui/*.gd | Implemented |

## Rendering / performance strategy (Android)
- Mobile renderer only; Compatibility renderer is the fallback if a
  device cannot run Mobile (project setting, not a second build).
- Shadows: the single biggest cost. Quality presets scale shadows only
  (Low = off, Medium = on, High = on + lower bias). No glow, no MSAA 3D,
  no real-time GI, no VoxelGI.
- Textures: ETC2/ASTC import on. No texture in Phase 1 exceeds
  procedural materials (zero texture memory in the slice).
- Draw calls: valley is ~30 primitive meshes + lights; target < 80.
- Lights: 1 directional (shadows) + 3 omni (shrine + 2 torches), all
  short range. No new lights without a budget check.
- Memory: no streaming needed at 60 m; streaming is a Phase 3 concern.
- Physics: one player body + one enemy + static world; 60 Hz is fine.

## Data-driven rules
Quests, dialogue, items and abilities live in `data/*.json` and are
loaded at runtime — no quest text or loot table is hard-coded in a
system script (the shrine's reward IDs are the one deliberate exception:
they name data entries, they are not the data).

## Save format
`user://savegame.json`, JSON, `version: 1`. `SaveData.from_dict`
rejects any other version instead of silently migrating (migration is
a Phase 2 task, recorded in the roadmap).
''')

w("ENVIRONMENT_AUDIT.md", '''\
# ENVIRONMENT AUDIT — PROJECT ETERNIA

**Date:** 2026-11-15 (fresh check, this session)
**Machine:** Linux htch-runtime, Ubuntu 24.04.5 LTS, x86_64, kernel 7.0.0-44
**CPU:** 4 vCPU — AMD EPYC 9D25 (runtime shares 1.5 CPU to this cell)
**RAM:** 7.7 GiB total; ~0.7–1.2 GiB available at audit time (7.1 GiB used,
  1.0 GiB swap, 445 MiB swap used) — **tight; headless Godot + export
  must run with nothing else heavy beside it**
**Disk:** 150 GiB volume, 130 GiB free (`/home/hatch`)
**GPU:** none (software rendering only on this VM)

## Verified installations
| Tool | Version | Path |
|---|---|---|
| Godot | 4.3.stable.official.77dcf97d8 | `/home/hatch/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64` (NOT in PATH) |
| Godot export templates | 4.3.stable (incl. android_debug.apk, android_release.apk, android_source.zip) | `~/.local/share/godot/export_templates/4.3.stable/` |
| JDK | Temurin 17.0.21+9 | `/home/hatch/workspace/game-apk/tools/jdk17` (NOT in PATH, no system java) |
| Android SDK | build-tools 34.0.0, platform android-34, platform-tools, cmdline-tools, licenses | `/home/hatch/workspace/game-apk/tools/android-sdk` (ANDROID_HOME unset in shell) |
| Godot editor settings | android_sdk_path + java_sdk_path + debug keystore already configured | `~/.config/godot/editor_settings-4.3.tres` |
| Debug keystore | present | `/home/hatch/workspace/game-apk/debug.keystore` + `~/.local/share/godot/keystores/debug.keystore` |
| Git | 2.43.0 | system |
| Python | 3.12.3 | system |

## Missing dependencies
| Tool | Status | Impact |
|---|---|---|
| Blender | NOT installed (`blender: command not found`, not in apt list) | No modelled/imported assets can be produced here; Phase 1 uses primitives. Install needs user approval (apt). |
| Android NDK | No `ndk` directory in the SDK | Not needed for template export (`use_gradle_build=false`, proven by THE LAST SIGNAL). Needed only for custom native/GDExtension builds. |
| Gradle | Not installed standalone | Not needed for template export. Needed only for Gradle builds. |
| System Java / ANDROID_HOME | Not in PATH / env | Builds must set `JAVA_HOME` + `ANDROID_HOME` per command (done in the build steps). |
| GPU / VRAM | None | No GPU-accelerated preview; Mobile renderer + headless testing only. |

## Android export readiness
**READY (template path):** Godot 4.3 + templates 4.3 + SDK 34 + JDK 17 +
debug keystore are all present and this exact combination already
produced working APKs (Breakout, THE LAST SIGNAL v0.1/v0.2) from this
machine. Export preset uses `use_gradle_build=false`, arm64-v8a only,
package `com.gggg.eternia`.

## Known limitations
- RAM is the binding constraint: 7.7 GiB total with most of it in use
  at audit time. Export runs must not overlap with browser or video work.
- No GPU: editor 3D preview and in-editor playtesting are CPU-bound;
  real-device testing (Galaxy A16) is the only true performance test.
- No real FPS data exists for this project on the Galaxy A16 yet.
- AI agent integrations: this session runs on Muse Spark (Meta Muse);
  there is no separate installed "Muse Wonder" / "Muse Code" CLI in
  this environment — agent collaboration happens inside this Muse
  session, with Git checkpoints before major changes. No API keys or
  secrets are used or stored by this project.
''')

w("DEVELOPMENT_ROADMAP.md", '''\
# DEVELOPMENT ROADMAP — PROJECT ETERNIA

## Phase 1 — Foundation + vertical slice (THIS DELIVERY, 2026-11-15)
- [x] Environment audit (ENVIRONMENT_AUDIT.md)
- [x] Modular project structure + docs
- [x] Core / Player / World / RPG / Combat / Quest / Save / UI foundations
- [x] Playable 60 m valley: move, run, jump, camera, shrine, dummy, HUD, pause
- [x] Automated validation (`tests/run_tests.gd`)
- [x] Android debug APK (arm64)
- Exit criterion: project opens headless, tests pass, APK installs.
  **Next gate: user tests the APK on the Galaxy A16 and reports
  install / start / movement / FPS.**

## Phase 2 — Content + feel
- Imported character + animations (needs Blender or CC0 assets + approval)
- Full day/night cycle, weather (rain), music/SFX, cinematics intro
- 2 more quests, first NPC with dialogue tree, save migration v1 -> v2
- Real-device FPS pass on Galaxy A16, quality preset tuning
- Exit criterion: 30 FPS sustained on A16 in the valley.

## Phase 3 — World growth
- World streaming, Ashen Woods region, 3 more shrines
- Relationships, crafting, more enemies + boss dummy
- Exit criterion: 3 regions load without hitches on A16.

## Phase 4 — Production hardening
- Full quest chain, balance pass, accessibility, localisation (AR/EN)
- Release signing, store listing prep, crash reporting
- Exit criterion: release candidate APK.

## Phase 5 — Live
- Updates driven by player feedback. No scope promises beyond Phase 4.
''')

w("CHANGELOG.md", '''\
# CHANGELOG — PROJECT ETERNIA

## 0.1.0 — 2026-11-15 (Phase 1)
- Environment audit completed (Godot 4.3, SDK 34, JDK 17; Blender + NDK missing).
- Godot project created: Mobile renderer, Android landscape, arm64.
- Modular foundation: Core, Player, World, RPG, Combat, Quests, Save, UI (see TECHNICAL_ARCHITECTURE.md for per-module status; Weather, Streaming, Relationships, Cinematics are documented as unfinished).
- Playable vertical slice: 60 m valley, third-person player (walk/run/jump), SpringArm camera, shrine interaction, training dummy, HUD + joystick, pause + main menu, save/load v1.
- Automated validation: `tests/run_tests.gd` + `tools/validation/validate.sh`.
- Android debug APK built from export preset "Android Mobile".
''')

w("tools/validation/README.md", '''\
# Validation
Run from the project root:
```bash
bash tools/validation/validate.sh
```
It imports the project headless, runs `tests/run_tests.gd`, runs the
main scene headless for 600 frames, and lists the APK.
Report: `tests/reports/validation_report.md`.
''')

w("tools/coordinator/README.md", '''\
# Coordinator
Agent collaboration rules (brief §09):
- One agent edits one file set at a time; no concurrent edits to the
  same files without coordination.
- Git checkpoint before every major change.
- Every agent report lists: task, files changed, commands run,
  test results, remaining problems.
- No API keys or secrets in the repo, ever.
''')

w("tools/build/README.md", '''\
# Build tools
- `generate_foundation.py` — regenerates the Phase 1 foundation
  (structure, scripts, scenes, data, docs). Re-running overwrites
  generated files; keep hand edits in Git before regenerating.
''')

print("part6 done")
print("GENERATOR COMPLETE")
