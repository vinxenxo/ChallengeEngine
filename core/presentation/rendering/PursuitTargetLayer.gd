extends Node2D

## C11-C.8 — Pursuit perceptual hero. Presentation-only.
## Complex internal geometry never changes the authoritative position.

var _position := Vector2(270.0, 480.0)
var _radius := 20.0
var _primary := Color("FFFFFF")
var _accent := Color("59E7FF")
var _secondary := Color("8D7CFF")
var _tertiary := Color("B7F5FF")
var _contrast := 1.0
var _rotation_phase := 0.0
var _sizygia := false

func configure(position_value: Vector2, radius_value: float, primary: Color, accent: Color, secondary: Color, tertiary: Color, contrast: float, rotation_phase: float, sizygia_active: bool) -> void:
    _position = position_value
    _radius = radius_value
    _primary = primary
    _accent = accent
    _secondary = secondary
    _tertiary = tertiary
    _contrast = clampf(contrast, 0.05, 1.0)
    _rotation_phase = rotation_phase
    _sizygia = sizygia_active
    queue_redraw()

func _draw() -> void:
    var c := _position
    var r := _radius
    var a := _contrast
    var pulse := 1.0 if _sizygia else 0.0

    draw_circle(c, r * 3.8, Color(_accent.r, _accent.g, _accent.b, 0.035 * a))
    draw_circle(c, r * 2.8, Color(_secondary.r, _secondary.g, _secondary.b, (0.07 + pulse * 0.06) * a))

    # Three restrained Euler-like rings.
    _draw_ring(c, r * 2.10, 0.72, _rotation_phase, Color(_accent.r, _accent.g, _accent.b, 0.68 * a), 1.6)
    _draw_ring(c, r * 1.70, 0.52, -_rotation_phase * 1.23, Color(_secondary.r, _secondary.g, _secondary.b, 0.64 * a), 1.4)
    _draw_ring(c, r * 1.34, 0.90, _rotation_phase * 0.72, Color(_tertiary.r, _tertiary.g, _tertiary.b, 0.62 * a), 1.3)

    var outer := _square_points(c, r * 1.55, _rotation_phase)
    var inner_scale := 0.52 if _sizygia else (0.66 + 0.06 * sin(_rotation_phase * 1.7))
    var inner := _square_points(c, r * inner_scale, -_rotation_phase * 1.8)
    for i in range(4):
        draw_line(outer[i], outer[(i + 1) % 4], Color(_primary.r, _primary.g, _primary.b, 0.66 * a), 1.5, true)
        draw_line(inner[i], inner[(i + 1) % 4], Color(_primary.r, _primary.g, _primary.b, 0.76 * a), 1.35, true)
        draw_line(outer[i], inner[i], Color(_accent.r, _accent.g, _accent.b, 0.55 * a), 1.1, true)

    draw_circle(c, r * 0.46, Color(_primary.r, _primary.g, _primary.b, 0.92 * a))
    draw_arc(c, r * 0.76, 0.0, TAU, 48, Color(_accent.r, _accent.g, _accent.b, 0.92 * a), 2.0, true)
    if _sizygia:
        draw_circle(c, r * 2.55, Color(_tertiary.r, _tertiary.g, _tertiary.b, 0.11 * a))

func _draw_ring(center: Vector2, radius: float, flatten: float, phase: float, color: Color, width: float) -> void:
    var points := PackedVector2Array()
    for i in range(65):
        var angle := TAU * float(i) / 64.0
        var local := Vector2(cos(angle), sin(angle) * flatten).rotated(phase) * radius
        points.append(center + local)
    draw_polyline(points, color, width, true)

func _square_points(center: Vector2, radius: float, rotation_value: float) -> Array[Vector2]:
    var points: Array[Vector2] = []
    for p in [Vector2(-1,-1), Vector2(1,-1), Vector2(1,1), Vector2(-1,1)]:
        points.append(center + p.rotated(rotation_value) * radius)
    return points
