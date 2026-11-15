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
