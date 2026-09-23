extends Node2D

## C11-C 2.2.2 — Living Particles Tron road.
## Presentation-only background layer. Deterministic perspective-grid motion.

const BODY_TOP := 144.0
const BODY_BOTTOM := 816.0
const BODY_WIDTH := 540.0
const VANISHING_POINT := Vector2(270.0, 286.0)
const ELECTRIC_BLUE := Color("38D9FF")
const MAGENTA := Color("FF5CE1")
const SPACE_DARK := Color("050814")

var _travel: float = 0.0
var _primary: Color = Color("B48CFF")
var _secondary: Color = Color("5749C8")
var _highlight: Color = Color("E1D8FF")

func set_contrast_reference(particle_reference: Color, particle_highlight: Color) -> void:
    var reference := particle_reference.lerp(particle_highlight, 0.35)
    var complementary_hue := fmod(reference.h + 0.5, 1.0)
    if reference.s < 0.18:
        complementary_hue = 0.56
    var complement := Color.from_hsv(complementary_hue, 0.84, 0.96, 1.0)
    # Keep a saturated complementary hue instead of merely inverting RGB.
    # This produces a deliberate contrast against both warm and cool particle palettes.
    _primary = complement.lerp(ELECTRIC_BLUE, 0.16)
    if absf(complement.h - ELECTRIC_BLUE.h) < 0.08:
        _primary = complement.lerp(MAGENTA, 0.12)
    _secondary = _primary.lerp(SPACE_DARK, 0.28)
    _highlight = _primary.lerp(Color.WHITE, 0.24)

func set_frame(frame_index: int, total_frames: int, loop_cycles: float = 1.0) -> void:
    var total := maxi(1, total_frames)
    var normalized := float(posmod(frame_index, total)) / float(total)
    var cycles := maxf(loop_cycles, 1.0)
    _travel = fmod(normalized * cycles, 1.0)
    queue_redraw()

func _draw() -> void:
    # Very dark trapezoid keeps the grid legible without becoming another subject.
    var surface_color := Color(_secondary.r, _secondary.g, _secondary.b, 0.20)
    draw_colored_polygon(PackedVector2Array([
        VANISHING_POINT + Vector2(-12.0, 0.0),
        VANISHING_POINT + Vector2(12.0, 0.0),
        Vector2(BODY_WIDTH, BODY_BOTTOM),
        Vector2(0.0, BODY_BOTTOM)
    ]), surface_color)

    # Static perspective rails.
    var rail_positions: Array[float] = [-1.0, 1.0]
    for lane in rail_positions:
        var bottom_x := 270.0 + lane * 250.0
        var rail_color := Color(_primary.r, _primary.g, _primary.b, 0.62)
        draw_line(VANISHING_POINT, Vector2(bottom_x, BODY_BOTTOM), rail_color, 1.6, true)

    # Inner lane lines create the 3D roadway read.
    var lane_positions: Array[float] = [-0.56, 0.0, 0.56]
    for lane in lane_positions:
        var bottom_x := 270.0 + lane * 175.0
        var lane_color := Color(_primary.r, _primary.g, _primary.b, 0.34 if absf(lane) > 0.01 else 0.25)
        draw_line(VANISHING_POINT, Vector2(bottom_x, BODY_BOTTOM), lane_color, 1.0, true)

    # Moving transverse grid. Each segment travels from the vanishing point toward
    # the viewer, creating the perception of forward motion down a Tron road.
    const GRID_ROWS := 14
    for i in range(GRID_ROWS):
        var row_u := fmod(float(i) / float(GRID_ROWS) + _travel, 1.0)
        var perspective := pow(row_u, 1.72)
        var y := lerpf(VANISHING_POINT.y + 8.0, BODY_BOTTOM - 2.0, perspective)
        var half_width := lerpf(20.0, 292.0, perspective)
        var alpha := lerpf(0.24, 0.64, perspective)
        var width := 1.0
        if i % 4 == 0:
            alpha += 0.14
            width = 1.4
        var c := Color(_primary.r, _primary.g, _primary.b, clampf(alpha, 0.0, 0.78))
        draw_line(Vector2(270.0 - half_width, y), Vector2(270.0 + half_width, y), c, width, true)

    # A quieter, brighter center guide gives the road a recognisable visual axis.
    for i in range(10):
        var dash_u := fmod(float(i) / 10.0 + _travel * 1.15, 1.0)
        var p1 := _road_point(dash_u)
        var p2 := _road_point(minf(dash_u + 0.045, 0.998))
        var dash_alpha := lerpf(0.18, 0.38, dash_u)
        draw_line(p1, p2, Color(_highlight.r, _highlight.g, _highlight.b, dash_alpha), 1.3, true)

func _road_point(u: float) -> Vector2:
    var perspective := pow(clampf(u, 0.0, 1.0), 1.72)
    return Vector2(270.0, lerpf(VANISHING_POINT.y + 8.0, BODY_BOTTOM - 2.0, perspective))
