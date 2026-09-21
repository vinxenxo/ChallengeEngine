# res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd
extends Node2D

## C11-C.1 — Geometric Waves v1 isolated presentation prototype.
## Passive with respect to product semantics: accepts only precomputed presentation parameters.
## This file intentionally lives outside core/ so the prototype cannot silently become production code.

const WIDTH := 540.0
const BODY_TOP := 144.0
const BODY_HEIGHT := 672.0
const BODY_RECT := Rect2(0.0, BODY_TOP, WIDTH, BODY_HEIGHT)
const GEOMETRIC_WAVES_SHADER = preload("res://tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader")

var _rect: ColorRect
var _material: ShaderMaterial

func _ready() -> void:
    _rect = ColorRect.new()
    _rect.name = "GeometricWavesCanvas"
    _rect.position = BODY_RECT.position
    _rect.size = BODY_RECT.size
    _rect.mouse_filter = Control.MOUSE_FILTER_IGNORE

    _material = ShaderMaterial.new()
    _material.shader = GEOMETRIC_WAVES_SHADER
    _rect.material = _material

    add_child(_rect)

func set_palette(dominant: Color, secondary: Color, highlight: Color) -> void:
    _material.set_shader_parameter("dominant_color", dominant)
    _material.set_shader_parameter("secondary_color", secondary)
    _material.set_shader_parameter("highlight_color", highlight)

func set_style(morph_value: float, wave_frequency: float, line_width: float, glow_strength: float, polygon_sides: float, wave_ratio: float, shape_rotation: float, layer_spread: float, radial_wave_amplitude: float, liss_x_frequency: float, liss_y_frequency: float, interference_scale: float) -> void:
    _material.set_shader_parameter("morph", clamp(morph_value, 0.0, 1.0))
    _material.set_shader_parameter("wave_frequency", max(wave_frequency, 1.0))
    _material.set_shader_parameter("line_width", max(line_width, 0.001))
    _material.set_shader_parameter("glow_strength", clamp(glow_strength, 0.0, 1.0))
    _material.set_shader_parameter("polygon_sides", clamp(polygon_sides, 5.0, 8.0))
    _material.set_shader_parameter("wave_ratio", clamp(wave_ratio, 0.68, 0.96))
    _material.set_shader_parameter("shape_rotation", shape_rotation)
    _material.set_shader_parameter("layer_spread", clamp(layer_spread, 0.0, 0.08))
    _material.set_shader_parameter("radial_wave_amplitude", clamp(radial_wave_amplitude, 0.008, 0.055))
    _material.set_shader_parameter("liss_x_frequency", clamp(liss_x_frequency, 5.0, 12.0))
    _material.set_shader_parameter("liss_y_frequency", clamp(liss_y_frequency, 2.0, 8.0))
    _material.set_shader_parameter("interference_scale", clamp(interference_scale, 0.75, 1.30))

func set_frame(frame_index: int, total_frames: int, seed_phase: float) -> void:
    var total := maxi(1, total_frames)
    var frame := posmod(frame_index, total)
    var phase := TAU * float(frame) / float(total)
    _material.set_shader_parameter("phase", phase)
    _material.set_shader_parameter("seed_phase", seed_phase)

func get_body_rect() -> Rect2:
    return BODY_RECT
