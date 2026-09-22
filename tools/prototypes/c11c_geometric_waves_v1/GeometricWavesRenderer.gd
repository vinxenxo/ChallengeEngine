# res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd
extends Node2D

## C11-C.1 v1.5 — Geometric Waves presentation renderer.
## Five mathematical wave grammars; presentation-only and deterministic.

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

func set_background(background: Color) -> void:
    _material.set_shader_parameter("background_color", background)

func set_palette(dominant: Color, secondary: Color, highlight: Color) -> void:
    _material.set_shader_parameter("dominant_color", dominant)
    _material.set_shader_parameter("secondary_color", secondary)
    _material.set_shader_parameter("highlight_color", highlight)

func set_style(
    grammar_mode: int,
    palette_mode: int,
    morph_value: float,
    wave_frequency: float,
    line_width: float,
    glow_strength: float,
    polygon_sides: float,
    wave_ratio: float,
    shape_rotation: float,
    layer_spread: float,
    radial_wave_amplitude: float,
    liss_x_frequency: float,
    liss_y_frequency: float,
    interference_scale: float,
    hero_scale: float,
    perspective_strength: float,
    depth_strength: float,
    secondary_phase: float,
    color_phase: float,
    stroke_scale: float
) -> void:
    _material.set_shader_parameter("grammar_mode", clampi(grammar_mode, 0, 4))
    _material.set_shader_parameter("palette_mode", clampi(palette_mode, 0, 4))
    _material.set_shader_parameter("morph", clamp(morph_value, 0.0, 1.0))
    _material.set_shader_parameter("wave_frequency", max(wave_frequency, 5.0))
    _material.set_shader_parameter("line_width", max(line_width, 0.001))
    _material.set_shader_parameter("glow_strength", clamp(glow_strength, 0.0, 1.0))
    _material.set_shader_parameter("polygon_sides", clamp(polygon_sides, 5.0, 8.0))
    _material.set_shader_parameter("wave_ratio", clamp(wave_ratio, 0.60, 1.05))
    _material.set_shader_parameter("shape_rotation", shape_rotation)
    _material.set_shader_parameter("layer_spread", clamp(layer_spread, 0.0, 0.10))
    _material.set_shader_parameter("radial_wave_amplitude", clamp(radial_wave_amplitude, 0.008, 0.08))
    _material.set_shader_parameter("liss_x_frequency", clamp(liss_x_frequency, 3.0, 16.0))
    _material.set_shader_parameter("liss_y_frequency", clamp(liss_y_frequency, 2.0, 12.0))
    _material.set_shader_parameter("interference_scale", clamp(interference_scale, 0.65, 1.55))
    _material.set_shader_parameter("hero_scale", clamp(hero_scale, 0.76, 1.06))
    _material.set_shader_parameter("perspective_strength", clamp(perspective_strength, 0.20, 1.20))
    _material.set_shader_parameter("depth_strength", clamp(depth_strength, 0.20, 1.0))
    _material.set_shader_parameter("secondary_phase", secondary_phase)
    _material.set_shader_parameter("color_phase", color_phase)
    _material.set_shader_parameter("stroke_scale", clamp(stroke_scale, 0.72, 1.40))

func set_frame(frame_index: int, total_frames: int, seed_phase: float, loop_cycles: float = 1.0) -> void:
    var total: int = maxi(1, total_frames)
    var frame: int = posmod(frame_index, total)
    var cycles: float = max(loop_cycles, 1.0)
    _material.set_shader_parameter("phase", TAU * float(frame) / float(total) * cycles)
    _material.set_shader_parameter("seed_phase", seed_phase)


func get_body_rect() -> Rect2:
    return BODY_RECT
