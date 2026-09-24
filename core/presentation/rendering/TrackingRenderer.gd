# res://core/presentation/rendering/TrackingRenderer.gd
extends Node2D

## C11-C 2.5.0 — Tracking Renderer.
## Passive renderer: consumes only deterministic TrackingGenerator state.
## No trajectory math, RNG or mechanic decisions belong here.

const LivingParticlesTronRoadClass = preload("res://tools/prototypes/c11c_living_particles_v1/LivingParticlesTronRoad.gd")
const TrackingTargetLayerClass = preload("res://core/presentation/rendering/TrackingTargetLayer.gd")

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const TARGET_RADIUS: float = 12.0
const TARGET_Z_INDEX: int = 100
const ENVIRONMENT_Z_INDEX: int = 0
const TRON_Z_INDEX: int = -20
const BACKGROUND_Z_INDEX: int = -30
const TRAIL_FADE_SECONDS: float = 12.0
const GROWING_HISTORY: String = "growing_history"

var _frame_state: Dictionary = {}
var _tron: Node2D = null
var _body_background: ColorRect = null
var _target_layer: Node2D = null
var _palette_index: int = -1
var _background_color: Color = Color("050914")
var _trail_color: Color = Color("36E7FF")
var _target_color: Color = Color("F6FFFF")

func _ready() -> void:
    _body_background = ColorRect.new()
    _body_background.name = "TrackingBodyBackground"
    _body_background.position = BODY_RECT.position
    _body_background.size = BODY_RECT.size
    _body_background.color = _background_color
    _body_background.mouse_filter = Control.MOUSE_FILTER_IGNORE
    _body_background.z_index = BACKGROUND_Z_INDEX
    add_child(_body_background)

    _tron = LivingParticlesTronRoadClass.new()
    _tron.name = "TrackingTronRoad"
    _tron.z_index = TRON_Z_INDEX
    add_child(_tron)

    _target_layer = TrackingTargetLayerClass.new()
    _target_layer.name = "TrackingTargetLayer"
    _target_layer.z_index = TARGET_Z_INDEX
    add_child(_target_layer)

func apply_state(model: Dictionary) -> void:
    _frame_state = model.duplicate(true)
    _apply_palette()
    _update_tron_frame()
    _update_target_layer()
    queue_redraw()

func _apply_palette() -> void:
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var params: Dictionary = drill_state.get("parameters", {})
    var variant: float = clampf(float(params.get("tracking_variant", 0.0)), 0.0, 0.999999)
    var index: int = mini(5, int(floor(variant * 6.0)))
    if index == _palette_index:
        return
    _palette_index = index

    var backgrounds: Array[Color] = [
        Color("050914"), Color("070611"), Color("0B050F"),
        Color("100B05"), Color("06130E"), Color("040F15")
    ]
    var trails: Array[Color] = [
        Color("2DE7FF"), Color("FF4CC7"), Color("A66CFF"),
        Color("FFB62E"), Color("59FF93"), Color("31F0D4")
    ]
    var targets: Array[Color] = [
        Color("F6FFFF"), Color("FFF7FD"), Color("FAF7FF"),
        Color("FFFBEF"), Color("F4FFF7"), Color("F2FFFE")
    ]
    _background_color = backgrounds[index]
    _trail_color = trails[index]
    _target_color = targets[index]

    if _body_background != null:
        _body_background.color = _background_color
    if _tron != null:
        if _tron.has_method("set_contrast_reference"):
            _tron.set_contrast_reference(_trail_color, _target_color)
        if _tron.has_method("set_intensity_scale"):
            _tron.set_intensity_scale(0.72)
    if _target_layer != null and _target_layer.has_method("configure"):
        # Position is refreshed in _update_target_layer; this call just keeps palette state coherent.
        _target_layer.configure(Vector2(270.0, 480.0), TARGET_RADIUS, _target_color, _trail_color)

func _update_tron_frame() -> void:
    if _tron == null:
        return
    var frame_index: int = int(_frame_state.get("editorial_frame_index", 0))
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var trajectory: Dictionary = drill_state.get("trajectory_state", {})
    var total_frames: int = int(_frame_state.get("editorial_frame_count", 630))
    if trajectory.has("phase_progress"):
        frame_index = int(round(float(trajectory.get("phase_progress", 0.0)) * float(maxi(1, total_frames - 1))))
    if _tron.has_method("set_frame"):
        _tron.set_frame(frame_index, total_frames, 1.0)

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
    _target_layer.configure(position, radius, _target_color, _trail_color)

func _draw() -> void:
    if _frame_state.is_empty():
        return

    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var trajectory: Dictionary = drill_state.get("trajectory_state", {})
    var target_states: Array = drill_state.get("target_states", [])
    if trajectory.is_empty() or target_states.size() != 1:
        return

    var center := Vector2(float(trajectory.get("center_x", 270.0)), float(trajectory.get("center_y", 480.0)))
    var bounds: Dictionary = trajectory.get("bounds", {})
    var radius: float = float(bounds.get("target_radius", TARGET_RADIUS))

    # Quiet operating boundary. The future path remains undisclosed.
    var amplitude_x: float = float(trajectory.get("amplitude_x", 160.0))
    var amplitude_y: float = float(trajectory.get("amplitude_y", 210.0))
    draw_ellipse(center, amplitude_x + 20.0, amplitude_y + 20.0, Color(_trail_color.r, _trail_color.g, _trail_color.b, 0.045), 1.0)

    # History-only trail. Alpha is derived from elapsed time, not travelled distance.
    # At constant FPS each history sample is 1/fps apart; older samples therefore fade
    # according to absolute age, while the growing_history mode preserves accumulated path history.
    var trail: Array = trajectory.get("trail_points", [])
    var fps: float = float(_frame_state.get("presentation_fps", 30))
    if trail.size() >= 2:
        var last_index: int = trail.size() - 1
        var step: int = 1 if trail.size() <= 360 else 2
        var previous_index: int = 0
        for i in range(step, trail.size(), step):
            var a_data: Dictionary = trail[previous_index]
            var b_data: Dictionary = trail[i]
            var a := Vector2(float(a_data.get("x", center.x)), float(a_data.get("y", center.y)))
            var b := Vector2(float(b_data.get("x", center.x)), float(b_data.get("y", center.y)))
            var age_seconds: float = float(last_index - i) / maxf(1.0, fps)
            var fade: float = clampf(1.0 - age_seconds / TRAIL_FADE_SECONDS, 0.0, 1.0)
            var alpha: float = 0.34 * pow(fade, 0.70)
            var width: float = lerpf(0.9, 3.6, fade)
            # Soft outer glow remains subordinate to the target while giving the
            # history trail the continuous "snake" read on mobile.
            draw_line(a, b, Color(_trail_color.r, _trail_color.g, _trail_color.b, alpha * 0.20), width * 2.8, true)
            draw_line(a, b, Color(_trail_color.r, _trail_color.g, _trail_color.b, alpha), width, true)
            previous_index = i
        if previous_index != last_index:
            var a_data: Dictionary = trail[previous_index]
            var b_data: Dictionary = trail[last_index]
            var a := Vector2(float(a_data.get("x", center.x)), float(a_data.get("y", center.y)))
            var b := Vector2(float(b_data.get("x", center.x)), float(b_data.get("y", center.y)))
            draw_line(a, b, Color(_trail_color.r, _trail_color.g, _trail_color.b, 0.075), 9.0, true)
            draw_line(a, b, Color(_trail_color.r, _trail_color.g, _trail_color.b, 0.36), 3.6, true)
            var head_data: Dictionary = trail[last_index]
            var head := Vector2(float(head_data.get("x", center.x)), float(head_data.get("y", center.y)))
            draw_circle(head, TARGET_RADIUS * 0.95, Color(_trail_color.r, _trail_color.g, _trail_color.b, 0.12))

func _draw_ellipse(center: Vector2, radius_x: float, radius_y: float, color: Color, width: float) -> void:
    var points := PackedVector2Array()
    for i in range(96):
        var angle: float = TAU * float(i) / 96.0
        points.append(center + Vector2(cos(angle) * radius_x, sin(angle) * radius_y))
    points.append(points[0])
    draw_polyline(points, color, width, true)
