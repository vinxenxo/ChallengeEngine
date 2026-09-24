# res://core/presentation/rendering/TrackingRenderer.gd
extends Node2D

## C11-C 2.6.0 — Tracking Renderer.
## Passive renderer: consumes deterministic TrackingGenerator state only.
## No trajectory math, RNG, Tron background or future-path disclosure belongs here.

const TrackingTargetLayerClass = preload("res://core/presentation/rendering/TrackingTargetLayer.gd")
const DrillPaletteBankClass = preload("res://tools/prototypes/c11c_common/C11CDrillPaletteBank.gd")

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const TARGET_RADIUS: float = 12.0
const TARGET_Z_INDEX: int = 100
const BACKGROUND_Z_INDEX: int = -30
const TRAIL_FADE_SECONDS: float = 12.0
const GROWING_HISTORY: String = "growing_history"

var _frame_state: Dictionary = {}
var _body_background: ColorRect = null
var _target_layer: Node2D = null
var _palette_index: int = -1
var _background_color: Color = Color("030813")
var _trail_color: Color = Color("16E6FF")
var _secondary_color: Color = Color("FF3EBA")
var _target_color: Color = Color("FFFFFF")

func _ready() -> void:
    _body_background = ColorRect.new()
    _body_background.name = "TrackingBodyBackground"
    _body_background.position = BODY_RECT.position
    _body_background.size = BODY_RECT.size
    _body_background.color = _background_color
    _body_background.mouse_filter = Control.MOUSE_FILTER_IGNORE
    _body_background.z_index = BACKGROUND_Z_INDEX
    add_child(_body_background)

    _target_layer = TrackingTargetLayerClass.new()
    _target_layer.name = "TrackingTargetLayer"
    _target_layer.z_index = TARGET_Z_INDEX
    add_child(_target_layer)

func apply_state(model: Dictionary) -> void:
    _frame_state = model.duplicate(true)
    _apply_palette()
    _update_target_layer()
    queue_redraw()

func _apply_palette() -> void:
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var params: Dictionary = drill_state.get("parameters", {})
    var variant: float = clampf(float(params.get("tracking_variant", 0.0)), 0.0, 0.999999)
    var palette := DrillPaletteBankClass.tracking(variant)
    var palette_name := str(palette.get("name", ""))
    var index: int = int(floor(variant * 12.0))
    if index == _palette_index:
        return
    _palette_index = index

    _background_color = Color(str(palette.get("background", "030813")))
    _trail_color = Color(str(palette.get("accent", "16E6FF")))
    _secondary_color = Color(str(palette.get("secondary", "FF3EBA")))
    _target_color = Color(str(palette.get("target", "FFFFFF")))

    if _body_background != null:
        _body_background.color = _background_color
    if _target_layer != null and _target_layer.has_method("configure"):
        _target_layer.set_meta("tracking_palette", palette_name)

func _update_target_layer() -> void:
    if _target_layer == null or not _target_layer.has_method("configure"):
        return
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var trajectory: Dictionary = drill_state.get("trajectory_state", {})
    var target_states: Array = drill_state.get("target_states", [])
    if trajectory.is_empty() or target_states.size() != 1:
        return
    var target: Dictionary = target_states[0]
    var position := Vector2(float(target.get("x", 270.0)), float(target.get("y", 480.0)))
    var radius: float = float(target.get("radius", trajectory.get("bounds", {}).get("target_radius", TARGET_RADIUS)))
    _target_layer.configure(position, radius, _target_color, _trail_color, _secondary_color)

func _draw() -> void:
    if _frame_state.is_empty():
        return

    draw_rect(BODY_RECT, _background_color, true)

    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var trajectory: Dictionary = drill_state.get("trajectory_state", {})
    var target_states: Array = drill_state.get("target_states", [])
    if trajectory.is_empty() or target_states.size() != 1:
        return

    # History-only trail. Only already-emitted positions are rendered.
    var trail: Array = trajectory.get("trail_points", [])
    var fps: float = float(_frame_state.get("presentation_fps", 30))
    if trail.size() < 2:
        return

    var last_index: int = trail.size() - 1
    var step: int = 1 if trail.size() <= 360 else 2
    var previous_index: int = 0

    for i in range(step, trail.size(), step):
        var a_data: Dictionary = trail[previous_index]
        var b_data: Dictionary = trail[i]
        var a := Vector2(float(a_data.get("x", 270.0)), float(a_data.get("y", 480.0)))
        var b := Vector2(float(b_data.get("x", 270.0)), float(b_data.get("y", 480.0)))
        var age_seconds: float = float(last_index - i) / maxf(1.0, fps)
        var fade: float = clampf(1.0 - age_seconds / TRAIL_FADE_SECONDS, 0.0, 1.0)
        var alpha: float = 0.30 * pow(fade, 0.72)
        var width: float = lerpf(0.8, 3.8, fade)
        var segment_color: Color = _secondary_color.lerp(_trail_color, clampf(fade * 1.35, 0.0, 1.0))

        draw_line(a, b, Color(segment_color.r, segment_color.g, segment_color.b, alpha * 0.16), width * 3.2, true)
        draw_line(a, b, Color(segment_color.r, segment_color.g, segment_color.b, alpha), width, true)

        if i % 30 == 0 and fade > 0.22:
            draw_circle(b, lerpf(0.7, 1.6, fade), Color(segment_color.r, segment_color.g, segment_color.b, alpha * 0.42))
        previous_index = i

    if previous_index != last_index:
        var a_data: Dictionary = trail[previous_index]
        var b_data: Dictionary = trail[last_index]
        var a := Vector2(float(a_data.get("x", 270.0)), float(a_data.get("y", 480.0)))
        var b := Vector2(float(b_data.get("x", 270.0)), float(b_data.get("y", 480.0)))
        draw_line(a, b, Color(_trail_color.r, _trail_color.g, _trail_color.b, 0.10), 10.0, true)
        draw_line(a, b, Color(_trail_color.r, _trail_color.g, _trail_color.b, 0.42), 3.8, true)

    var head_data: Dictionary = trail[last_index]
    var head := Vector2(float(head_data.get("x", 270.0)), float(head_data.get("y", 480.0)))
    draw_circle(head, TARGET_RADIUS * 1.75, Color(_trail_color.r, _trail_color.g, _trail_color.b, 0.08))
    draw_circle(head, TARGET_RADIUS * 0.88, Color(_target_color.r, _target_color.g, _target_color.b, 0.16))
