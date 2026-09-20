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

func set_palette(indigo: Color, violet: Color, cyan: Color, highlight: Color) -> void:
    _material.set_shader_parameter("indigo_color", indigo)
    _material.set_shader_parameter("violet_color", violet)
    _material.set_shader_parameter("cyan_color", cyan)
    _material.set_shader_parameter("highlight_color", highlight)

func set_style(zoom_strength: float, warp_strength: float, bloom_strength: float, layer_softness: float) -> void:
    _material.set_shader_parameter("zoom_strength", clamp(zoom_strength, 0.1, 1.2))
    _material.set_shader_parameter("warp_strength", clamp(warp_strength, 0.0, 0.08))
    _material.set_shader_parameter("bloom_strength", clamp(bloom_strength, 0.0, 1.0))
    _material.set_shader_parameter("layer_softness", clamp(layer_softness, 0.2, 1.5))

func set_frame(frame_index: int, total_frames: int, seed_phase: float) -> void:
    var total := maxi(1, total_frames)
    var frame := posmod(frame_index, total)
    var phase := TAU * float(frame) / float(total)
    _material.set_shader_parameter("phase", phase)
    _material.set_shader_parameter("seed_phase", seed_phase)

func get_body_rect() -> Rect2:
    return BODY_RECT
