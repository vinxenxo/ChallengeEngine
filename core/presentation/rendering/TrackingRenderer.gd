# res://core/presentation/rendering/TrackingRenderer.gd
extends Node2D

## C11-C 2.4.0 — Tracking Renderer production-oriented presentation baseline.
## Passive renderer: consumes only deterministic TrackingGenerator state.
## No trajectory math, RNG or mechanic decisions belong here.

const TronDepthBackgroundClass = preload("res://tools/prototypes/c11c_common/C11CTronDepthBackground.gd")

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const TARGET_RADIUS: float = 12.0

var _frame_state: Dictionary = {}
var _tron: Node2D = null
var _palette_index: int = -1
var _background_color: Color = Color("050914")
var _trail_color: Color = Color("36E7FF")
var _target_color: Color = Color("F6FFFF")
var _tron_primary: Color = Color("1A8DFF")
var _tron_highlight: Color = Color("5BFFF0")

func _ready() -> void:
	_tron = TronDepthBackgroundClass.new()
	_tron.name = "TrackingTronDepthBackground"
	_tron.z_index = -20
	add_child(_tron)

func apply_state(model: Dictionary) -> void:
	_frame_state = model.duplicate(true)
	_apply_palette()
	_update_tron_frame()
	queue_redraw()

func _apply_palette() -> void:
	var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
	var params: Dictionary = drill_state.get("parameters", {})
	var variant: float = clampf(float(params.get("tracking_variant", 0.0)), 0.0, 0.999999)
	var index: int = mini(3, int(floor(variant * 4.0)))
	if index == _palette_index:
		return
	_palette_index = index
	var backgrounds: Array[Color] = [Color("050914"), Color("0A0714"), Color("100B05"), Color("06130E")]
	var trails: Array[Color] = [Color("36E7FF"), Color("FF4FD8"), Color("FFC84A"), Color("63FF8D")]
	var targets: Array[Color] = [Color("F6FFFF"), Color("FFF8FF"), Color("FFFDF2"), Color("F5FFF9")]
	var tron_primary: Array[Color] = [Color("1A8DFF"), Color("C02BFF"), Color("FF6B1A"), Color("1AC9A0")]
	var tron_highlight: Array[Color] = [Color("5BFFF0"), Color("FF73ED"), Color("FFE064"), Color("7DFFB4")]
	_background_color = backgrounds[index]
	_trail_color = trails[index]
	_target_color = targets[index]
	_tron_primary = tron_primary[index]
	_tron_highlight = tron_highlight[index]
	if _tron != null and _tron.has_method("configure"):
		_tron.configure(_background_color, _tron_primary, _tron_highlight)

func _update_tron_frame() -> void:
	if _tron == null:
		return
	var frame_index: int = int(_frame_state.get("editorial_frame_index", 0))
	var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
	var trajectory: Dictionary = drill_state.get("trajectory_state", {})
	var total_frames: int = int(_frame_state.get("editorial_frame_count", 510))
	if trajectory.has("phase_progress"):
		frame_index = int(round(float(trajectory.get("phase_progress", 0.0)) * float(maxi(1, total_frames - 1))))
	if _tron.has_method("set_frame"):
		_tron.set_frame(frame_index, total_frames, 1.0)

func _draw() -> void:
	if _frame_state.is_empty():
		return

	# Full-width Body fill: the 24px presentation safe-area is not the Body surface.
	draw_rect(BODY_RECT, _background_color, true)

	var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
	var trajectory: Dictionary = drill_state.get("trajectory_state", {})
	var target_states: Array = drill_state.get("target_states", [])
	if trajectory.is_empty() or target_states.size() != 1:
		return

	var center := Vector2(float(trajectory.get("center_x", 270.0)), float(trajectory.get("center_y", 480.0)))
	var bounds: Dictionary = trajectory.get("bounds", {})
	var radius: float = float(bounds.get("target_radius", TARGET_RADIUS))

	# Quiet operating boundary; the future path itself remains undisclosed.
	var amplitude_x: float = float(trajectory.get("amplitude_x", 160.0))
	var amplitude_y: float = float(trajectory.get("amplitude_y", 210.0))
	_draw_ellipse(center, amplitude_x + 20.0, amplitude_y + 20.0, Color(_tron_highlight.r, _tron_highlight.g, _tron_highlight.b, 0.05), 1.0)

	# Growing-history trail: it contains only positions already visited.
	var trail: Array = trajectory.get("trail_points", [])
	if trail.size() >= 2:
		var last_index: int = trail.size() - 1
		var step: int = 1 if trail.size() <= 180 else 2
		var previous_index: int = 0
		for i in range(step, trail.size(), step):
			var a_data: Dictionary = trail[previous_index]
			var b_data: Dictionary = trail[i]
			var a := Vector2(float(a_data.get("x", center.x)), float(a_data.get("y", center.y)))
			var b := Vector2(float(b_data.get("x", center.x)), float(b_data.get("y", center.y)))
			var progress: float = float(i) / float(maxi(1, last_index))
			var alpha: float = lerpf(0.02, 0.36, progress)
			var width: float = lerpf(1.0, 3.8, progress)
			draw_line(a, b, Color(_trail_color.r, _trail_color.g, _trail_color.b, alpha), width, true)
			previous_index = i
		if previous_index != last_index:
			var a_data: Dictionary = trail[previous_index]
			var b_data: Dictionary = trail[last_index]
			draw_line(Vector2(float(a_data.get("x", center.x)), float(a_data.get("y", center.y))), Vector2(float(b_data.get("x", center.x)), float(b_data.get("y", center.y))), Color(_trail_color.r, _trail_color.g, _trail_color.b, 0.36), 3.8, true)

	var target: Dictionary = target_states[0]
	var target_position := Vector2(float(target.get("x", center.x)), float(target.get("y", center.y)))
	# Target is the perceptual hero and the brightest element in the Body.
	draw_circle(target_position, radius * 2.7, Color(_target_color.r, _target_color.g, _target_color.b, 0.045))
	draw_circle(target_position, radius * 1.55, Color(_trail_color.r, _trail_color.g, _trail_color.b, 0.17))
	draw_arc(target_position, radius * 1.30, 0.0, TAU, 48, _target_color, 2.0, true)
	draw_circle(target_position, radius * 0.58, _target_color)

	var tick_inner: float = radius * 1.75
	var tick_outer: float = radius * 2.25
	var tick_angles: Array[float] = [0.0, PI * 0.5, PI, PI * 1.5]
	for angle: float in tick_angles:
		var direction := Vector2(cos(angle), sin(angle))
		draw_line(target_position + direction * tick_inner, target_position + direction * tick_outer, _target_color, 1.6, true)

func _draw_ellipse(center: Vector2, radius_x: float, radius_y: float, color: Color, width: float) -> void:
	var points := PackedVector2Array()
	for i in range(96):
		var angle := TAU * float(i) / 96.0
		points.append(center + Vector2(cos(angle) * radius_x, sin(angle) * radius_y))
	points.append(points[0])
	draw_polyline(points, color, width, true)
