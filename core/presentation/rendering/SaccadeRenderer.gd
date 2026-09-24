# res://core/presentation/rendering/SaccadeRenderer.gd
extends Node2D

## C11-C 2.6.0 — Saccade presentation.
## Random/polar jump baseline: no decorative background, no spatial interpolation.
## The mechanic owns position, phase and jump_index; this layer only expresses them.

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const CENTER_X: float = 270.0
const CENTER_Y: float = 480.0
const TARGET_RADIUS: float = 12.0
const DrillPaletteBankClass = preload("res://tools/prototypes/c11c_common/C11CDrillPaletteBank.gd")

var _frame_state: Dictionary = {}
var _palette_index: int = -1
var _background_color: Color = Color("030813")
var _accent_color: Color = Color("16E6FF")
var _secondary_color: Color = Color("FF3EBA")
var _target_color: Color = Color("FFFFFF")
var _counter_color: Color = Color("06111A")
var _counter_label: Label = null

func _ready() -> void:
    _counter_label = Label.new()
    _counter_label.name = "SaccadeJumpCounter"
    _counter_label.size = Vector2(24.0, 20.0)
    _counter_label.pivot_offset = Vector2(12.0, 10.0)
    _counter_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    _counter_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
    _counter_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    _counter_label.add_theme_font_size_override("font_size", 10)
    _counter_label.add_theme_constant_override("outline_size", 1)
    _counter_label.z_index = 120
    add_child(_counter_label)

func apply_state(model: Dictionary) -> void:
    _frame_state = model.duplicate(true)
    _apply_palette()
    _update_counter()
    queue_redraw()

func _apply_palette() -> void:
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var params: Dictionary = drill_state.get("parameters", {})
    var variant: float = clampf(float(params.get("saccade_variant", 0.0)), 0.0, 0.999999)
    var palette := DrillPaletteBankClass.saccade(variant)
    var index: int = int(floor(variant * 12.0))
    if index == _palette_index:
        return
    _palette_index = index

    _background_color = Color(str(palette.get("background", "030813")))
    _accent_color = Color(str(palette.get("accent", "16E6FF")))
    _secondary_color = Color(str(palette.get("secondary", "FF3EBA")))
    _target_color = Color(str(palette.get("target", "FFFFFF")))
    _counter_color = Color(str(palette.get("counter", "06111A")))

func _update_counter() -> void:
    if _counter_label == null:
        return

    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var saccade_state: Dictionary = drill_state.get("saccade_state", drill_state.get("mechanic_state", {}).get("saccade_state", {}))
    var target_states: Array = drill_state.get("target_states", [])
    if target_states.size() != 1 or saccade_state.is_empty():
        _counter_label.visible = false
        return

    var target: Dictionary = target_states[0]
    var position := Vector2(float(target.get("x", CENTER_X)), float(target.get("y", CENTER_Y)))
    var radius: float = float(target.get("radius", TARGET_RADIUS))
    var jump_index: int = maxi(0, int(saccade_state.get("jump_index", 0)))
    var scale_value: float = float(saccade_state.get("scale", target.get("scale", 1.0)))
    var opacity: float = float(saccade_state.get("opacity", target.get("opacity", 1.0)))

    if str(drill_state.get("presentation_phase", "GAME")) == "PRE_ROLL":
        scale_value = 1.0
        opacity = 1.0

    _counter_label.text = str(jump_index + 1)
    _counter_label.position = position - Vector2(12.0, 10.0)
    _counter_label.scale = Vector2.ONE * scale_value
    _counter_label.modulate = Color(1.0, 1.0, 1.0, opacity)
    _counter_label.add_theme_color_override("font_color", _counter_color)
    _counter_label.add_theme_color_override("font_outline_color", Color(_secondary_color.r, _secondary_color.g, _secondary_color.b, 0.42))
    _counter_label.visible = opacity > 0.001 and scale_value > 0.001

func _draw() -> void:
    if _frame_state.is_empty():
        return

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
    draw_circle(position, r * 3.8, Color(_accent_color.r, _accent_color.g, _accent_color.b, 0.035 * opacity))
    draw_arc(position, r * 2.2, -0.55, 1.25, 28, Color(_secondary_color.r, _secondary_color.g, _secondary_color.b, 0.50 * opacity), 1.15, true)
    draw_arc(position, r * 1.68, 2.05, 3.45, 28, Color(_secondary_color.r, _secondary_color.g, _secondary_color.b, 0.34 * opacity), 1.0, true)
    draw_arc(position, r * 2.05, 0.0, TAU, 64, Color(_accent_color.r, _accent_color.g, _accent_color.b, 0.18 * opacity), 1.0, true)
    draw_arc(position, r * 1.35, 0.0, TAU, 64, Color(_target_color.r, _target_color.g, _target_color.b, 0.94 * opacity), 1.8, true)
    draw_circle(position, r * 0.72, Color(_target_color.r, _target_color.g, _target_color.b, opacity))

    var tick_inner: float = r * 1.65
    var tick_outer: float = r * 2.18
    var tick_angles: Array[float] = [0.0, PI * 0.5, PI, PI * 1.5]
    for angle: float in tick_angles:
        var direction := Vector2(cos(angle), sin(angle))
        draw_line(position + direction * tick_inner, position + direction * tick_outer, Color(_target_color.r, _target_color.g, _target_color.b, 0.78 * opacity), 1.4, true)

    if flash_strength > 0.0:
        draw_circle(position, r * (2.8 + flash_strength * 4.0), Color(1.0, 1.0, 1.0, flash_strength * 0.14))
