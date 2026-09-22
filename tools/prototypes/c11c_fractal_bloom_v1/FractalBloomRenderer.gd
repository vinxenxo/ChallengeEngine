extends Node2D

## C11-C.2 — Fractal Bloom v1 isolated presentation prototype.
## Presentation-only. The controller supplies frame/seed parameters; this renderer
## never reads simulation state and never touches engine RNG streams.

const WIDTH := 540.0
const BODY_TOP := 144.0
const BODY_HEIGHT := 672.0
const BODY_RECT := Rect2(0.0, BODY_TOP, WIDTH, BODY_HEIGHT)
const FRACTAL_SHADER = preload("res://tools/prototypes/c11c_fractal_bloom_v1/FractalBloom.gdshader")

var _rect: ColorRect
var _material: ShaderMaterial

func _ready() -> void:
    _rect = ColorRect.new()
    _rect.name = "FractalBloomCanvas"
    _rect.position = BODY_RECT.position
    _rect.size = BODY_RECT.size
    _rect.mouse_filter = Control.MOUSE_FILTER_IGNORE

    _material = ShaderMaterial.new()
    _material.shader = FRACTAL_SHADER
    _rect.material = _material
    add_child(_rect)

func set_background(background: Color) -> void:
    _material.set_shader_parameter("background_color", background)

func set_palette(indigo: Color, violet: Color, cyan: Color, highlight: Color) -> void:
    _material.set_shader_parameter("indigo_color", indigo)
    _material.set_shader_parameter("violet_color", violet)
    _material.set_shader_parameter("cyan_color", cyan)
    _material.set_shader_parameter("highlight_color", highlight)

func set_style(grammar_mode: int, zoom_strength: float, warp_strength: float, bloom_strength: float, layer_softness: float, julia_x_bias: float, julia_y_bias: float, zoom_cycles: float, warp_frequency: float, layer_spread: float, breath_strength: float, branch_density: float, detail_scale: float, spiral_amount: float, color_diversity: float = 0.9, color_phase: float = 0.0) -> void:
    _material.set_shader_parameter("grammar_mode", clamp(grammar_mode, 0, 4))
    _material.set_shader_parameter("zoom_strength", clamp(zoom_strength, 0.08, 1.90))
    _material.set_shader_parameter("warp_strength", clamp(warp_strength, 0.0, 0.08))
    _material.set_shader_parameter("bloom_strength", clamp(bloom_strength, 0.0, 1.0))
    _material.set_shader_parameter("layer_softness", clamp(layer_softness, 0.2, 1.5))
    _material.set_shader_parameter("julia_x_bias", clamp(julia_x_bias, -0.08, 0.08))
    _material.set_shader_parameter("julia_y_bias", clamp(julia_y_bias, -0.08, 0.08))
    _material.set_shader_parameter("zoom_cycles", clamp(zoom_cycles, 1.0, 3.0))
    _material.set_shader_parameter("warp_frequency", clamp(warp_frequency, 2.0, 5.5))
    _material.set_shader_parameter("layer_spread", clamp(layer_spread, 0.0, 0.22))
    _material.set_shader_parameter("breath_strength", clamp(breath_strength, 0.03, 0.13))
    _material.set_shader_parameter("branch_density", clamp(branch_density, 0.70, 1.40))
    _material.set_shader_parameter("detail_scale", clamp(detail_scale, 0.80, 1.40))
    _material.set_shader_parameter("spiral_amount", clamp(spiral_amount, 0.30, 1.60))
    _material.set_shader_parameter("color_diversity", clamp(color_diversity, 0.82, 1.0))
    _material.set_shader_parameter("color_phase", color_phase)

func set_frame(frame_index: int, total_frames: int, seed_phase: float, loop_cycles: float = 1.0) -> void:
    var total: int = maxi(1, total_frames)
    var frame: int = posmod(frame_index, total)
    var cycles: float = max(loop_cycles, 1.0)
    _material.set_shader_parameter("phase", TAU * float(frame) / float(total) * cycles)
    _material.set_shader_parameter("seed_phase", seed_phase)


func get_body_rect() -> Rect2:
    return BODY_RECT
