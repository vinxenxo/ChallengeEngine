# res://core/presentation/rendering/SaccadeRenderer.gd
extends Node2D

## C11-C.7 / 2.5.1 — Saccade presentation baseline.
## Random/polar jump baseline: no decorative background, no spatial interpolation.
## The mechanic owns position and phase; this layer only expresses them visually.

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const CENTER_X: float = 270.0
const CENTER_Y: float = 480.0
const TARGET_RADIUS: float = 12.0

var _frame_state: Dictionary = {}
var _palette_index: int = -1
var _background_color: Color = Color("060914")
var _accent_color: Color = Color("37E7FF")
var _target_color: Color = Color("F7FFFF")

func apply_state(model: Dictionary) -> void:
    _frame_state = model.duplicate(true)
    _apply_palette()
    queue_redraw()

func _apply_palette() -> void:
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var params: Dictionary = drill_state.get("parameters", {})
    var variant: float = clampf(float(params.get("saccade_variant", 0.0)), 0.0, 0.999999)
    var index: int = mini(5, int(floor(variant * 6.0)))
    if index == _palette_index:
        return
    _palette_index = index

    var backgrounds: Array[Color] = [
        Color("060914"), Color("100611"), Color("090714"),
        Color("120C05"), Color("06140D"), Color("041116")
    ]
    var accents: Array[Color] = [
        Color("2DE7FF"), Color("FF4CC7"), Color("A66CFF"),
        Color("FFB62E"), Color("59FF93"), Color("31F0D4")
    ]
    var targets: Array[Color] = [
        Color("F6FFFF"), Color("FFF7FD"), Color("FAF7FF"),
        Color("FFFBEF"), Color("F4FFF7"), Color("F2FFFE")
    ]
    _background_color = backgrounds[index]
    _accent_color = accents[index]
    _target_color = targets[index]

func _draw() -> void:
    if _frame_state.is_empty():
        return

    # Solid Body fill only. This is the intentional "no decorative background"
    # baseline for random/polar saccades.
    draw_rect(BODY_RECT, _background_color, true)

    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var saccade_state: Dictionary = drill_state.get("saccade_state", drill_state.get("mechanic_state", {}).get("saccade_state", {}))
    var target_states: Array = drill_state.get("target_states", [])
    if target_states.size() != 1:
        return

    var target: Dictionary = target_states[0]
    var position := Vector2(float(target.get("x", CENTER_X)), float(target.get("y", CENTER_Y)))
    var radius: float = float(target.get("radius", TARGET_RADIUS))
    var scale_value: float = float(saccade_state.get("scale", target.get("scale", 1.0)))
    var opacity: float = float(saccade_state.get("opacity", target.get("opacity", 1.0)))
    var flash_strength: float = float(saccade_state.get("flash_strength", 0.0))

    if str(drill_state.get("presentation_phase", "GAME")) == "PRE_ROLL":
        scale_value = 1.0
        opacity = 1.0
        flash_strength = 0.0

    if scale_value <= 0.001 or opacity <= 0.001:
        return

    var r: float = radius * scale_value

    # Premium but intentionally compact target stack. Every element shares the
    # current mechanic position; none of these visuals infer a path between jumps.
    draw_circle(position, r * 3.6, Color(_accent_color.r, _accent_color.g, _accent_color.b, 0.035 * opacity))
    draw_circle(position, r * 2.6, Color(_target_color.r, _target_color.g, _target_color.b, 0.025 * opacity))
    draw_arc(position, r * 2.05, 0.0, TAU, 64, Color(_accent_color.r, _accent_color.g, _accent_color.b, 0.16 * opacity), 1.0, true)
    draw_arc(position, r * 1.35, 0.0, TAU, 64, Color(_target_color.r, _target_color.g, _target_color.b, 0.92 * opacity), 1.8, true)
    draw_circle(position, r * 0.62, Color(_target_color.r, _target_color.g, _target_color.b, opacity))

    var tick_inner: float = r * 1.65
    var tick_outer: float = r * 2.18
    var tick_angles: Array[float] = [0.0, PI * 0.5, PI, PI * 1.5]
    for angle: float in tick_angles:
        var direction := Vector2(cos(angle), sin(angle))
        draw_line(position + direction * tick_inner, position + direction * tick_outer, Color(_target_color.r, _target_color.g, _target_color.b, 0.78 * opacity), 1.4, true)

    if flash_strength > 0.0:
        draw_circle(position, r * (2.8 + flash_strength * 4.0), Color(1.0, 1.0, 1.0, flash_strength * 0.14))
