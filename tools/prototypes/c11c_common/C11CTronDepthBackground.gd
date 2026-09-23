extends Node2D

## C11-C 2.4.0 — reusable presentation-only Tron depth background.
## No simulation, RNG or mechanic ownership.

const BODY_TOP: float = 144.0
const BODY_BOTTOM: float = 816.0
const WIDTH: float = 540.0
const VANISHING_POINT := Vector2(270.0, 270.0)

var _background: Color = Color("050914")
var _primary: Color = Color("1A8DFF")
var _highlight: Color = Color("5BFFF0")
var _travel: float = 0.0

func configure(background: Color, primary: Color, highlight: Color) -> void:
	_background = background
	_primary = primary
	_highlight = highlight
	queue_redraw()

func set_frame(frame_index: int, total_frames: int, loop_cycles: float = 1.0) -> void:
	var total: int = maxi(1, total_frames)
	var normalized: float = float(posmod(frame_index, total)) / float(total)
	_travel = fmod(normalized * maxf(1.0, loop_cycles) * 0.85, 1.0)
	queue_redraw()

func _draw() -> void:
	draw_rect(Rect2(0.0, BODY_TOP, WIDTH, BODY_BOTTOM - BODY_TOP), _background, true)
	draw_colored_polygon(PackedVector2Array([
		VANISHING_POINT + Vector2(-10.0, 0.0),
		VANISHING_POINT + Vector2(10.0, 0.0),
		Vector2(WIDTH, BODY_BOTTOM),
		Vector2(0.0, BODY_BOTTOM)
	]), Color(_primary.r, _primary.g, _primary.b, 0.055))
	draw_line(Vector2(42.0, VANISHING_POINT.y), Vector2(WIDTH - 42.0, VANISHING_POINT.y), Color(_highlight.r, _highlight.g, _highlight.b, 0.12), 1.0, true)
	for side: float in [-1.0, 1.0]:
		draw_line(VANISHING_POINT, Vector2(270.0 + side * 254.0, BODY_BOTTOM), Color(_primary.r, _primary.g, _primary.b, 0.38), 1.5, true)
	for lane: float in [-0.54, 0.0, 0.54]:
		draw_line(VANISHING_POINT, Vector2(270.0 + lane * 180.0, BODY_BOTTOM), Color(_primary.r, _primary.g, _primary.b, 0.16 if absf(lane) > 0.01 else 0.10), 1.0, true)
	const ROWS: int = 16
	for i in range(ROWS):
		var u: float = fmod(float(i) / float(ROWS) + _travel, 1.0)
		var perspective: float = pow(u, 1.80)
		var y: float = lerpf(VANISHING_POINT.y + 5.0, BODY_BOTTOM - 3.0, perspective)
		var half_width: float = lerpf(12.0, 294.0, perspective)
		var alpha: float = lerpf(0.07, 0.24, perspective)
		if i % 4 == 0:
			alpha += 0.07
		var c := Color(_primary.r, _primary.g, _primary.b, minf(alpha, 0.36))
		draw_line(Vector2(270.0 - half_width, y), Vector2(270.0 + half_width, y), c, 1.0, true)
	for i in range(10):
		var u: float = fmod(float(i) / 10.0 + _travel * 1.12, 1.0)
		var p1 := _road_point(u)
		var p2 := _road_point(minf(u + 0.04, 0.998))
		draw_line(p1, p2, Color(_highlight.r, _highlight.g, _highlight.b, 0.12), 1.2, true)

func _road_point(u: float) -> Vector2:
	var perspective: float = pow(clampf(u, 0.0, 1.0), 1.80)
	return Vector2(270.0, lerpf(VANISHING_POINT.y + 5.0, BODY_BOTTOM - 3.0, perspective))
