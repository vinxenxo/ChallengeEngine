extends Node2D

## C11-C.5 — Invisible Forces isolated presentation renderer.

const WIDTH := 540.0
const BODY_TOP := 144.0
const BODY_HEIGHT := 672.0
const BODY_RECT := Rect2(0.0, BODY_TOP, WIDTH, BODY_HEIGHT)
const SHADER = preload("res://tools/prototypes/c11c_invisible_forces_v1/InvisibleForces.gdshader")

var _rect: ColorRect
var _material: ShaderMaterial

func _ready() -> void:
    _rect = ColorRect.new()
    _rect.name = "InvisibleForcesCanvas"
    _rect.position = BODY_RECT.position
    _rect.size = BODY_RECT.size
    _rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
    _material = ShaderMaterial.new()
    _material.shader = SHADER
    _rect.material = _material
    add_child(_rect)

func set_background(background: Color) -> void:
    _material.set_shader_parameter("background_color", background)

func set_palette(deep: Color, primary: Color, secondary: Color, highlight: Color) -> void:
    _material.set_shader_parameter("deep_color", deep)
    _material.set_shader_parameter("primary_color", primary)
    _material.set_shader_parameter("secondary_color", secondary)
    _material.set_shader_parameter("highlight_color", highlight)

func set_style(grammar_mode: int, trace_count: float, curvature: float, glow_strength: float, field_rotation: float, storm_offset: Vector2, pulse_speed: float, field_twist: float, pulse_width: float, storm_scale: float, lens_strength: float, basin_depth: float, pole_separation: float, quadrupole_skew: float, color_phase: float = 0.0) -> void:
    _material.set_shader_parameter("grammar_mode", clamp(grammar_mode, 0, 5))
    _material.set_shader_parameter("trace_count", clamp(trace_count, 50.0, 92.0))
    _material.set_shader_parameter("curvature", clamp(curvature, 0.4, 1.4))
    _material.set_shader_parameter("glow_strength", clamp(glow_strength, 0.0, 1.0))
    _material.set_shader_parameter("field_rotation", field_rotation)
    _material.set_shader_parameter("storm_offset", storm_offset)
    _material.set_shader_parameter("pulse_speed", pulse_speed)
    _material.set_shader_parameter("field_twist", clamp(field_twist, 0.70, 1.35))
    _material.set_shader_parameter("pulse_width", clamp(pulse_width, 0.65, 1.45))
    _material.set_shader_parameter("storm_scale", clamp(storm_scale, 0.74, 1.20))
    _material.set_shader_parameter("lens_strength", clamp(lens_strength, 0.30, 1.10))
    _material.set_shader_parameter("basin_depth", clamp(basin_depth, 0.30, 1.20))
    _material.set_shader_parameter("pole_separation", clamp(pole_separation, 0.12, 0.40))
    _material.set_shader_parameter("quadrupole_skew", clamp(quadrupole_skew, 0.70, 1.35))
    _material.set_shader_parameter("color_phase", color_phase)

func set_frame(frame_index: int, total_frames: int, seed_phase: float, loop_cycles: float = 1.0) -> void:
    var total: int = maxi(1, total_frames)
    var frame: int = posmod(frame_index, total)
    var cycles: float = max(loop_cycles, 1.0)
    _material.set_shader_parameter("phase", TAU * float(frame) / float(total) * cycles)
    _material.set_shader_parameter("seed_phase", seed_phase)

