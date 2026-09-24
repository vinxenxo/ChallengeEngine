extends Node2D

## C11-C 2.2.1 / 2.5.0 — Living Particles Tron road.
## Presentation-only background layer. Deterministic perspective-grid motion.
## Reused by Tracking without duplicating the 3D road implementation.

const BODY_TOP := 144.0
const BODY_BOTTOM := 816.0
const BODY_WIDTH := 540.0
const VANISHING_POINT := Vector2(270.0, 286.0)
const ELECTRIC_BLUE := Color("657BFF")
const SPACE_DARK := Color("090D1A")

var _travel: float = 0.0
var _primary: Color = Color("B48CFF")
var _secondary: Color = Color("5749C8")
var _highlight: Color = Color("E1D8FF")
var _intensity_scale: float = 1.0

func set_contrast_reference(particle_reference: Color, _particle_highlight: Color) -> void:
    var complement := Color(
        clampf(1.0 - particle_reference.r, 0.0, 1.0),
        clampf(1.0 - particle_reference.g, 0.0, 1.0),
        clampf(1.0 - particle_reference.b, 0.0, 1.0),
        1.0
    )
    _primary = complement.lerp(ELECTRIC_BLUE, 0.18).lerp(Color.WHITE, 0.14)
    _secondary = _primary.lerp(SPACE_DARK, 0.42)
    _highlight = _primary.lerp(Color.WHITE, 0.28)
    queue_redraw()

func set_intensity_scale(value: float) -> void:
    _intensity_scale = clampf(value, 0.0, 1.0)
    queue_redraw()

func set_frame(frame_index: int, total_frames: int, loop_cycles: float = 1.0) -> void:
    var total: int = maxi(1, total_frames)
    var normalized: float = float(posmod(frame_index, total)) / float(total)
    var cycles: float = maxf(loop_cycles, 1.0)
    _travel = fmod(normalized * cycles, 1.0)
    queue_redraw()

func _alpha(value: float) -> float:
    return clampf(value * _intensity_scale, 0.0, 0.78)

func _draw() -> void:
    var surface_color := Color(_secondary.r, _secondary.g, _secondary.b, _alpha(0.12))
    draw_colored_polygon(PackedVector2Array([
        VANISHING_POINT + Vector2(-12.0, 0.0),
        VANISHING_POINT + Vector2(12.0, 0.0),
        Vector2(BODY_WIDTH, BODY_BOTTOM),
        Vector2(0.0, BODY_BOTTOM)
    ]), surface_color)

    var rail_positions: Array[float] = [-1.0, 1.0]
    for lane: float in rail_positions:
        var bottom_x: float = 270.0 + lane * 250.0
        var rail_color := Color(_primary.r, _primary.g, _primary.b, _alpha(0.42))
        draw_line(VANISHING_POINT, Vector2(bottom_x, BODY_BOTTOM), rail_color, 1.6, true)

    var lane_positions: Array[float] = [-0.56, 0.0, 0.56]
    for lane: float in lane_positions:
        var bottom_x: float = 270.0 + lane * 175.0
        var lane_color := Color(_primary.r, _primary.g, _primary.b, _alpha(0.23 if absf(lane) > 0.01 else 0.17))
        draw_line(VANISHING_POINT, Vector2(bottom_x, BODY_BOTTOM), lane_color, 1.0, true)

    const GRID_ROWS := 14
    for i in range(GRID_ROWS):
        var row_u: float = fmod(float(i) / float(GRID_ROWS) + _travel, 1.0)
        var perspective: float = pow(row_u, 1.72)
        var y: float = lerpf(VANISHING_POINT.y + 8.0, BODY_BOTTOM - 2.0, perspective)
        var half_width: float = lerpf(20.0, 292.0, perspective)
        var alpha: float = lerpf(0.16, 0.46, perspective)
        var width: float = 1.0
        if i % 4 == 0:
            alpha += 0.12
            width = 1.4
        var c := Color(_primary.r, _primary.g, _primary.b, _alpha(alpha))
        draw_line(Vector2(270.0 - half_width, y), Vector2(270.0 + half_width, y), c, width, true)

    for i in range(10):
        var dash_u: float = fmod(float(i) / 10.0 + _travel * 1.15, 1.0)
        var p1 := _road_point(dash_u)
        var p2 := _road_point(minf(dash_u + 0.045, 0.998))
        var dash_alpha: float = lerpf(0.12, 0.32, dash_u)
        draw_line(p1, p2, Color(_highlight.r, _highlight.g, _highlight.b, _alpha(dash_alpha)), 1.3, true)

func _road_point(u: float) -> Vector2:
    var perspective: float = pow(clampf(u, 0.0, 1.0), 1.72)
    return Vector2(270.0, lerpf(VANISHING_POINT.y + 8.0, BODY_BOTTOM - 2.0, perspective))
