extends Node2D

## C11-C 2.6.0 — Tracking target presentation layer.
## Explicit perceptual-hero layer. Presentation-only.

const TARGET_Z_INDEX: int = 100

var _position: Vector2 = Vector2(270.0, 480.0)
var _radius: float = 12.0
var _target_color: Color = Color("FFFFFF")
var _accent_color: Color = Color("16E6FF")
var _secondary_color: Color = Color("FF3EBA")

func _ready() -> void:
    z_index = TARGET_Z_INDEX

func configure(position_value: Vector2, radius_value: float, target_color: Color, accent_color: Color, secondary_color: Color = Color("FF3EBA")) -> void:
    _position = position_value
    _radius = radius_value
    _target_color = target_color
    _accent_color = accent_color
    _secondary_color = secondary_color
    queue_redraw()

func _draw() -> void:
    draw_circle(_position, _radius * 3.2, Color(_target_color.r, _target_color.g, _target_color.b, 0.035))
    draw_circle(_position, _radius * 2.5, Color(_accent_color.r, _accent_color.g, _accent_color.b, 0.13))
    draw_arc(_position, _radius * 2.00, -0.72, 1.12, 20, Color(_secondary_color.r, _secondary_color.g, _secondary_color.b, 0.56), 1.35, true)
    draw_arc(_position, _radius * 1.56, 1.88, 2.88, 18, Color(_secondary_color.r, _secondary_color.g, _secondary_color.b, 0.40), 1.1, true)
    draw_arc(_position, _radius * 1.30, 0.0, TAU, 64, _target_color, 2.0, true)
    draw_circle(_position, _radius * 0.58, _target_color)

    var tick_inner: float = _radius * 1.72
    var tick_outer: float = _radius * 2.24
    var tick_angles: Array[float] = [0.0, PI * 0.5, PI, PI * 1.5]
    for angle: float in tick_angles:
        var direction := Vector2(cos(angle), sin(angle))
        draw_line(_position + direction * tick_inner, _position + direction * tick_outer, _target_color, 1.6, true)
