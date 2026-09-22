extends Node2D

## C11-C.3 v1.6 — Sacred Symmetry visual grammar renderer.
## Presentation-only. Exact symmetry belongs to the shader grammar.

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

func set_background(background: Color) -> void:
    _material.set_shader_parameter("background_color", background)

func set_palette(primary: Color, secondary: Color, highlight: Color, white_gold: Color, accent: Color) -> void:
    _material.set_shader_parameter("primary_color", primary)
    _material.set_shader_parameter("secondary_color", secondary)
    _material.set_shader_parameter("highlight_color", highlight)
    _material.set_shader_parameter("white_gold_color", white_gold)
    _material.set_shader_parameter("accent_color", accent)

func set_style(grammar_mode: int, segment_count: float, ring_bias: float, glow_strength: float, gear_inner: float, gear_outer: float, ring_scale: float, core_scale: float, tick_density: float, mechanical_rate: float, macro_scale: float, node_density: float, fold_depth: float, color_diversity: float, color_phase: float) -> void:
    _material.set_shader_parameter("grammar_mode", clamp(grammar_mode, 0, 4))
    _material.set_shader_parameter("segment_count", max(segment_count, 4.0))
    _material.set_shader_parameter("ring_bias", clamp(ring_bias, 0.0, 1.0))
    _material.set_shader_parameter("glow_strength", clamp(glow_strength, 0.0, 1.0))
    _material.set_shader_parameter("gear_inner", gear_inner)
    _material.set_shader_parameter("gear_outer", gear_outer)
    _material.set_shader_parameter("ring_scale", clamp(ring_scale, 0.86, 1.04))
    _material.set_shader_parameter("core_scale", clamp(core_scale, 0.76, 1.24))
    _material.set_shader_parameter("tick_density", clamp(tick_density, 0.70, 1.45))
    _material.set_shader_parameter("mechanical_rate", clamp(mechanical_rate, 0.80, 2.30))
    _material.set_shader_parameter("macro_scale", clamp(macro_scale, 0.84, 1.02))
    _material.set_shader_parameter("node_density", clamp(node_density, 0.65, 1.35))
    _material.set_shader_parameter("fold_depth", clamp(fold_depth, 0.70, 1.30))
    _material.set_shader_parameter("color_diversity", clamp(color_diversity, 0.0, 1.0))
    _material.set_shader_parameter("color_phase", color_phase)

func set_frame(frame_index: int, total_frames: int, seed_phase: float, loop_cycles: float = 1.0) -> void:
    var total: int = maxi(1, total_frames)
    var frame: int = posmod(frame_index, total)
    var cycles: float = max(loop_cycles, 1.0)
    _material.set_shader_parameter("phase", TAU * float(frame) / float(total) * cycles)
    _material.set_shader_parameter("seed_phase", seed_phase)

