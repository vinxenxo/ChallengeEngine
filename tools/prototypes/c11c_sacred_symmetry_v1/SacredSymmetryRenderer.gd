extends Node2D

## C11-C.3 — Sacred Symmetry isolated presentation renderer.
## Presentation-only. No simulation state, RNG stream or production runtime access.

const WIDTH := 540.0
const BODY_TOP := 144.0
const BODY_HEIGHT := 672.0
const BODY_RECT := Rect2(0.0, BODY_TOP, WIDTH, BODY_HEIGHT)
const SHADER = preload("res://tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetry.gdshader")

var _rect: ColorRect
var _material: ShaderMaterial

func _ready() -> void:
    _rect = ColorRect.new()
    _rect.name = "SacredSymmetryCanvas"
    _rect.position = BODY_RECT.position
    _rect.size = BODY_RECT.size
    _rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
    _material = ShaderMaterial.new()
    _material.shader = SHADER
    _rect.material = _material
    add_child(_rect)

func set_palette(primary: Color, secondary: Color, highlight: Color, white_gold: Color) -> void:
    _material.set_shader_parameter("primary_color", primary)
    _material.set_shader_parameter("secondary_color", secondary)
    _material.set_shader_parameter("highlight_color", highlight)
    _material.set_shader_parameter("white_gold_color", white_gold)

func set_style(segment_count: float, ring_bias: float, glow_strength: float, gear_inner: float, gear_outer: float) -> void:
    _material.set_shader_parameter("segment_count", max(segment_count, 6.0))
    _material.set_shader_parameter("ring_bias", clamp(ring_bias, 0.0, 1.0))
    _material.set_shader_parameter("glow_strength", clamp(glow_strength, 0.0, 1.0))
    _material.set_shader_parameter("gear_inner", gear_inner)
    _material.set_shader_parameter("gear_outer", gear_outer)

func set_frame(frame_index: int, total_frames: int, seed_phase: float) -> void:
    var total := maxi(1, total_frames)
    var frame := posmod(frame_index, total)
    _material.set_shader_parameter("phase", TAU * float(frame) / float(total))
    _material.set_shader_parameter("seed_phase", seed_phase)
