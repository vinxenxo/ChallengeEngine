# res://core/presentation/rendering/TrackingRenderer.gd
extends Node2D

## C11-C.6 Tracking Renderer v1.0.
## Passive renderer: consumes only the deterministic TrackingGenerator state.
## No trajectory math, RNG or mechanic decisions belong here.

var _frame_state: Dictionary = {}
var _content_rect := Rect2(24.0, 144.0, 492.0, 672.0)

const TARGET_COLOR := Color(0.92, 0.98, 1.0, 1.0)
const TRAIL_COLOR := Color(0.25, 0.82, 1.0, 1.0)
const FIELD_COLOR := Color(0.12, 0.36, 0.58, 1.0)

func apply_state(model: Dictionary) -> void:
	_frame_state = model.duplicate(true)
	var geometry: Dictionary = model.get("geometry", {})
	var content_rect: Rect2 = geometry.get("content_rect", _content_rect)
	_content_rect = content_rect
	queue_redraw()

func _draw() -> void:
	if _frame_state.is_empty():
		return

	var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
	var trajectory: Dictionary = drill_state.get("trajectory_state", {})
	var target_states: Array = drill_state.get("target_states", [])
	if trajectory.is_empty() or target_states.size() != 1:
		return

	# Quiet body field: enough contrast to separate the drill from the page frame,
	# intentionally far below target luminance.
	draw_rect(_content_rect, Color(0.008, 0.016, 0.028, 0.90), true)

	var bounds: Dictionary = trajectory.get("bounds", {})
	var center := Vector2(
		float(trajectory.get("center_x", 270.0)),
		float(trajectory.get("center_y", 480.0))
	)
	var radius := float(bounds.get("target_radius", 12.0))
	var amplitude_x := float(trajectory.get("amplitude_x", 160.0))
	var amplitude_y := float(trajectory.get("amplitude_y", 210.0))

	# Very quiet mathematical guide: an ellipse-scale field shows the intended
	# operating zone without exposing the future trajectory.
	var field_outer := Vector2(amplitude_x + 22.0, amplitude_y + 22.0)
	draw_arc(center, minf(field_outer.x, field_outer.y), 0.0, TAU, 96, Color(FIELD_COLOR.r, FIELD_COLOR.g, FIELD_COLOR.b, 0.12), 1.0, true)
	var ellipse_scales: Array[float] = [0.72, 0.48]
	for axis_scale: float in ellipse_scales:
		var rx: float = amplitude_x * axis_scale
		var ry: float = amplitude_y * axis_scale
		_draw_ellipse(center, rx, ry, Color(FIELD_COLOR.r, FIELD_COLOR.g, FIELD_COLOR.b, 0.055), 1.0)

	var trail: Array = trajectory.get("trail_points", [])
	if trail.size() >= 2:
		for i in range(1, trail.size()):
			var a_data: Dictionary = trail[i - 1]
			var b_data: Dictionary = trail[i]
			var a := Vector2(float(a_data.get("x", center.x)), float(a_data.get("y", center.y)))
			var b := Vector2(float(b_data.get("x", center.x)), float(b_data.get("y", center.y)))
			var t := float(i) / float(maxi(1, trail.size() - 1))
			var alpha := lerpf(0.04, 0.30, t)
			var width := lerpf(1.0, 2.4, t)
			draw_line(a, b, Color(TRAIL_COLOR.r, TRAIL_COLOR.g, TRAIL_COLOR.b, alpha), width, true)

	var target: Dictionary = target_states[0]
	var target_position := Vector2(float(target.get("x", center.x)), float(target.get("y", center.y)))

	# Perceptual hero: strong center, ring, halo and four cardinal ticks.
	draw_circle(target_position, radius * 2.5, Color(TARGET_COLOR.r, TARGET_COLOR.g, TARGET_COLOR.b, 0.06))
	draw_circle(target_position, radius * 1.45, Color(TRAIL_COLOR.r, TRAIL_COLOR.g, TRAIL_COLOR.b, 0.18))
	draw_arc(target_position, radius * 1.30, 0.0, TAU, 48, TARGET_COLOR, 2.0, true)
	draw_circle(target_position, radius * 0.58, TARGET_COLOR)

	var tick_inner := radius * 1.7
	var tick_outer := radius * 2.25
	var tick_angles: Array[float] = [0.0, PI * 0.5, PI, PI * 1.5]
	for angle: float in tick_angles:
		var direction := Vector2(cos(angle), sin(angle))
		draw_line(target_position + direction * tick_inner, target_position + direction * tick_outer, TARGET_COLOR, 1.6, true)

func _draw_ellipse(center: Vector2, radius_x: float, radius_y: float, color: Color, width: float) -> void:
	var points := PackedVector2Array()
	for i in range(96):
		var angle := TAU * float(i) / 96.0
		points.append(center + Vector2(cos(angle) * radius_x, sin(angle) * radius_y))
	points.append(points[0])
	draw_polyline(points, color, width, true)
