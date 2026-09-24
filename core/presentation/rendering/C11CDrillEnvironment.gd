# res://core/presentation/rendering/C11CDrillEnvironment.gd
class_name C11CDrillEnvironment
extends Node2D

## C11-C 2.9.0 — Shared passive Visual Drill environment.
## Background-only presentation layer. It never calculates gameplay truth,
## target trajectories, answer events or future paths.

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)

var _family: String = "tracking"
var _seed: int = 314159
var _frame_index: int = 0
var _background: Color = Color("030813")
var _primary: Color = Color("40D9FF")
var _secondary: Color = Color("FF8E61")
var _tertiary: Color = Color("C9F4FF")
var _target_position: Vector2 = Vector2(270.0, 480.0)

func configure(family: String, seed_value: int, frame_index: int, background: Color, primary: Color, secondary: Color, tertiary: Color, target_position: Vector2 = Vector2(270.0, 480.0)) -> void:
    _family = family
    _seed = seed_value
    _frame_index = maxi(0, frame_index)
    _background = background
    _primary = primary
    _secondary = secondary
    _tertiary = tertiary
    _target_position = target_position
    queue_redraw()

func _draw() -> void:
    draw_rect(BODY_RECT, _background, true)
    match _family:
        "tracking":
            _draw_tracking()
        "saccade":
            _draw_saccade()
        "pursuit":
            _draw_pursuit()
        "peripheral_scan":
            _draw_peripheral()
        _:
            _draw_saccade()

func _draw_tracking() -> void:
    # Atmospheric contour bands: no line follows the emitted target path.
    var drift := float(_frame_index) * 0.0017
    var centers: Array[Vector2] = [
        Vector2(90.0 + sin(drift) * 12.0, 300.0),
        Vector2(420.0 + cos(drift * 0.87) * 14.0, 620.0),
        Vector2(310.0, 270.0 + sin(drift * 0.61) * 10.0)
    ]
    var radii: Array[float] = [188.0, 246.0, 312.0]
    for i in range(3):
        var c := centers[i]
        var r := radii[i]
        draw_arc(c, r, 0.26 + drift, 1.76 + drift, 72, Color(_secondary.r, _secondary.g, _secondary.b, 0.055), 5.0, true)
        draw_arc(c, r + 18.0, 3.16 - drift * 0.5, 4.72 - drift * 0.5, 72, Color(_primary.r, _primary.g, _primary.b, 0.035), 2.0, true)
    for i in range(22):
        var x := BODY_RECT.position.x + _hash01(1100 + i * 13) * BODY_RECT.size.x
        var y := BODY_RECT.position.y + _hash01(1200 + i * 17) * BODY_RECT.size.y
        var a := 0.028 + 0.018 * _hash01(1300 + i)
        draw_circle(Vector2(x, y), 0.7 + _hash01(1400 + i) * 1.0, Color(_tertiary.r, _tertiary.g, _tertiary.b, a))

func _draw_saccade() -> void:
    # Sparse constellation haze. No edges connect targets or predict jumps.
    for i in range(34):
        var x := BODY_RECT.position.x + _hash01(1700 + i * 11) * BODY_RECT.size.x
        var y := BODY_RECT.position.y + _hash01(1800 + i * 17) * BODY_RECT.size.y
        var radius := 0.55 + _hash01(1900 + i) * 1.45
        var alpha := 0.025 + 0.025 * _hash01(2000 + i)
        draw_circle(Vector2(x, y), radius, Color(_tertiary.r, _tertiary.g, _tertiary.b, alpha))
    for ring in range(3):
        var center := Vector2(270.0 + (ring - 1) * 62.0, 480.0 + (ring - 1) * 54.0)
        var radius := 82.0 + ring * 54.0
        draw_arc(center, radius, -0.4, 1.55, 48, Color(_secondary.r, _secondary.g, _secondary.b, 0.025), 1.0, true)

func _draw_pursuit() -> void:
    # Deep-space field used beneath the dedicated radial DOF layer.
    for i in range(42):
        var x := BODY_RECT.position.x + _hash01(2300 + i * 13) * BODY_RECT.size.x
        var y := BODY_RECT.position.y + _hash01(2400 + i * 17) * BODY_RECT.size.y
        var point := Vector2(x, y)
        var distance_factor := clampf(point.distance_to(_target_position) / 380.0, 0.0, 1.0)
        var radius := lerpf(0.45, 2.4, distance_factor)
        var alpha := lerpf(0.17, 0.035, distance_factor)
        draw_circle(point, radius, Color(_tertiary.r, _tertiary.g, _tertiary.b, alpha))
    for i in range(5):
        var x := 90.0 + _hash01(2500 + i * 9) * 360.0
        var y := BODY_RECT.position.y + 70.0 + _hash01(2600 + i * 7) * (BODY_RECT.size.y - 140.0)
        var haze_r := 70.0 + _hash01(2700 + i) * 95.0
        draw_circle(Vector2(x, y), haze_r, Color(_secondary.r, _secondary.g, _secondary.b, 0.012))

func _draw_peripheral() -> void:
    for i in range(32):
        var x := BODY_RECT.position.x + _hash01(3000 + i * 13) * BODY_RECT.size.x
        var y := BODY_RECT.position.y + _hash01(3100 + i * 17) * BODY_RECT.size.y
        var radius := 0.45 + _hash01(3200 + i) * 1.2
        draw_circle(Vector2(x, y), radius, Color(_tertiary.r, _tertiary.g, _tertiary.b, 0.025 + _hash01(3300 + i) * 0.018))
    draw_arc(Vector2(270.0, 480.0), 252.0, 0.0, TAU, 128, Color(_primary.r, _primary.g, _primary.b, 0.018), 2.0, true)

func _hash01(salt: int) -> float:
    var x: int = (int(_seed) ^ int(salt * 374761393)) & 0x7fffffff
    x = int(((x ^ (x >> 13)) * 1274126177) & 0x7fffffff)
    x = int(((x ^ (x >> 16)) * 2246822519) & 0x7fffffff)
    return float((x ^ (x >> 13)) & 0x7fffffff) / 2147483647.0
