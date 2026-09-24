extends Node2D

## C11-C.9 — Peripheral Scan / El Eclipse y la Tormenta Solar.
## Presentation-only. The authored schedule is the sole source of event timing.

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const CENTER := Vector2(270.0, 480.0)
const DrillPaletteBankClass = preload("res://tools/prototypes/c11c_common/C11CDrillPaletteBank.gd")
const C11CDrillEnvironmentClass = preload("res://core/presentation/rendering/C11CDrillEnvironment.gd")

var _frame_state: Dictionary = {}
var _environment: Node2D = Node2D.new()
var _background := Color("020B0C")
var _primary := Color("62FFE1")
var _secondary := Color("43A8FF")
var _tertiary := Color("B7FFF1")
var _target := Color("FAFFFE")
var _palette_index := -1

func _ready() -> void:
    _environment = C11CDrillEnvironmentClass.new()
    _environment.name = "PeripheralScanEnvironment"
    _environment.z_index = -40
    add_child(_environment)

func apply_state(model: Dictionary) -> void:
    _frame_state = model.duplicate(true)
    _apply_palette()
    _update_environment()
    queue_redraw()

func _apply_palette() -> void:
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var params: Dictionary = drill_state.get("parameters", {})
    var pattern := clampf(float(params.get("pattern_variant", 0.0)), 0.0, 0.999999)
    var amplitude := clampf(float(params.get("amplitude_variant", 0.0)), 0.0, 0.999999)
    var variant := fposmod(pattern * 0.63 + amplitude * 0.37, 1.0)
    var palette := DrillPaletteBankClass.peripheral_scan(variant)
    _palette_index = int(floor(variant * 8.0))
    _background = Color(str(palette.get("background", "020B0C")))
    _primary = Color(str(palette.get("accent", "62FFE1")))
    _secondary = Color(str(palette.get("secondary", "43A8FF")))
    _tertiary = Color(str(palette.get("tertiary", "B7FFF1")))
    _target = Color(str(palette.get("target", "FAFFFE")))

func _update_environment() -> void:
    if _environment == null:
        return
    _environment.configure("peripheral_scan", int(_frame_state.get("editorial_seed", 314159)), int(_frame_state.get("presentation_frame_index", 0)), _background, _primary, _secondary, _tertiary, CENTER)

func _draw() -> void:
    if _frame_state.is_empty():
        return
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var trajectory: Dictionary = drill_state.get("trajectory_state", {})
    var task: Dictionary = drill_state.get("task_state", {})
    var rings: Array = trajectory.get("ring_radii_normalized", [0.245, 0.355, 0.450])
    var radii: Array[float] = []
    for r in rings:
        radii.append(float(r) * BODY_RECT.size.x)

    # Quiet orbital radar structure.
    for i in range(radii.size()):
        var ring_alpha := 0.035 + float(i) * 0.005
        draw_arc(CENTER, radii[i], 0.0, TAU, 128, Color(_secondary.r, _secondary.g, _secondary.b, ring_alpha), 1.0, true)

    # Sparse star/particle field: subordinate to the anchor and events.
    var seed_value := int(_frame_state.get("editorial_seed", 314159))
    for i in range(28):
        var x := BODY_RECT.position.x + _hash01(seed_value, 3000 + i * 13) * BODY_RECT.size.x
        var y := BODY_RECT.position.y + _hash01(seed_value, 3100 + i * 17) * BODY_RECT.size.y
        draw_circle(Vector2(x, y), 0.6 + _hash01(seed_value, 3200 + i) * 1.1, Color(_tertiary.r, _tertiary.g, _tertiary.b, 0.035))

    var presentation_frame := int(_frame_state.get("presentation_frame_index", 0))
    var anchor: Dictionary = task.get("anchor_state", {})
    _draw_anchor(anchor, presentation_frame)

    var active_events: Array = task.get("active_events", [])
    for event in active_events:
        if event is Dictionary:
            _draw_event(event, radii)

func _draw_anchor(anchor: Dictionary, presentation_frame: int) -> void:
    var shape := str(anchor.get("shape", "CIRCLE"))
    var slow_phase := float(presentation_frame) * 0.0022
    var breathe := 1.0 + sin(float(presentation_frame) * 0.0075) * 0.02
    var outer_r := 25.0 * breathe

    draw_circle(CENTER, outer_r * 2.8, Color(_primary.r, _primary.g, _primary.b, 0.035))
    draw_circle(CENTER, outer_r * 1.8, Color(_target.r, _target.g, _target.b, 0.065))
    draw_arc(CENTER, outer_r * 1.25, 0.0, TAU, 64, Color(_primary.r, _primary.g, _primary.b, 0.82), 1.7, true)
    draw_circle(CENTER, outer_r * 0.86, Color(_target.r, _target.g, _target.b, 0.90))

    # Very slow Moiré-like interference inside the anchor.
    for i in range(7):
        var rr := outer_r * (0.30 + float(i) * 0.075)
        draw_arc(CENTER, rr, slow_phase + float(i) * 0.55, slow_phase + PI + float(i) * 0.55, 28, Color(_secondary.r, _secondary.g, _secondary.b, 0.19), 0.8, true)

    match shape:
        "TRIANGLE":
            var pts := PackedVector2Array([CENTER + Vector2(0,-8).rotated(slow_phase), CENTER + Vector2(7,6).rotated(slow_phase), CENTER + Vector2(-7,6).rotated(slow_phase)])
            draw_polyline(PackedVector2Array([pts[0],pts[1],pts[2],pts[0]]), Color(_background.r, _background.g, _background.b, 0.90), 1.7, true)
        "SQUARE":
            var pts2 := PackedVector2Array([Vector2(-7,-7),Vector2(7,-7),Vector2(7,7),Vector2(-7,7),Vector2(-7,-7)])
            for i in range(pts2.size()):
                pts2[i] = CENTER + pts2[i].rotated(slow_phase)
            draw_polyline(pts2, Color(_background.r, _background.g, _background.b, 0.90), 1.7, true)
        _:
            draw_arc(CENTER, 7.0, 0.0, TAU, 32, Color(_background.r, _background.g, _background.b, 0.90), 1.7, true)

func _draw_event(event: Dictionary, radii: Array[float]) -> void:
    var ring_index := clampi(int(event.get("ring_index", 0)), 0, maxi(0, radii.size() - 1))
    var radius := radii[ring_index] if not radii.is_empty() else 132.0
    var angle := float(event.get("angle_rad", 0.0))
    var pulse := clampf(float(event.get("pulse_strength", 0.0)), 0.0, 1.0)
    var kind := str(event.get("kind", "distractor"))
    var arc_width := 0.11 if kind == "threat" else 0.075
    var accent := _primary if kind == "threat" else _secondary
    var start := angle - arc_width
    var end := angle + arc_width
    var steps := 18
    for i in range(steps):
        var a0 := lerpf(start, end, float(i) / float(steps))
        var a1 := lerpf(start, end, float(i + 1) / float(steps))
        var local_alpha := pulse * (0.32 + 0.68 * sin(PI * float(i + 1) / float(steps)))
        draw_line(CENTER + Vector2(cos(a0), sin(a0)) * radius, CENTER + Vector2(cos(a1), sin(a1)) * radius, Color(accent.r, accent.g, accent.b, local_alpha), 2.0 if kind == "threat" else 1.2, true)
    draw_circle(CENTER + Vector2(cos(angle), sin(angle)) * radius, 3.5 + pulse * 3.0, Color(accent.r, accent.g, accent.b, pulse * 0.12))

func _hash01(seed_value: int, salt: int) -> float:
    var x := (seed_value ^ int(salt * 374761393)) & 0x7fffffff
    x = int(((x ^ (x >> 13)) * 1274126177) & 0x7fffffff)
    return float((x ^ (x >> 16)) & 0x7fffffff) / 2147483647.0
