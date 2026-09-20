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

func set_palette(deep: Color, primary: Color, secondary: Color, highlight: Color) -> void:
    _material.set_shader_parameter("deep_color", deep)
    _material.set_shader_parameter("primary_color", primary)
    _material.set_shader_parameter("secondary_color", secondary)
    _material.set_shader_parameter("highlight_color", highlight)

func set_style(trace_count: float, curvature: float, glow_strength: float, field_rotation: float, storm_offset: Vector2, pulse_speed: float) -> void:
    _material.set_shader_parameter("trace_count", clamp(trace_count, 12.0, 40.0))
    _material.set_shader_parameter("curvature", clamp(curvature, 0.4, 1.4))
    _material.set_shader_parameter("glow_strength", clamp(glow_strength, 0.0, 1.0))
    _material.set_shader_parameter("field_rotation", field_rotation)
    _material.set_shader_parameter("storm_offset", storm_offset)
    _material.set_shader_parameter("pulse_speed", pulse_speed)

func set_frame(frame_index: int, total_frames: int, seed_phase: float) -> void:
    var total := maxi(1, total_frames)
    var frame := posmod(frame_index, total)
    _material.set_shader_parameter("phase", TAU * float(frame) / float(total))
    _material.set_shader_parameter("seed_phase", seed_phase)
