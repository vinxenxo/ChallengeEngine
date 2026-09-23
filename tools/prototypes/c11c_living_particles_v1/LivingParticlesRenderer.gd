extends Node2D

## C11-C.4 v2.2.1 — Living Particles visual grammar renderer.
## Presentation-only. No simulation state, RNG stream or production runtime access.

const WIDTH := 540.0
const BODY_TOP := 144.0
const BODY_HEIGHT := 672.0
const BODY_RECT := Rect2(0.0, BODY_TOP, WIDTH, BODY_HEIGHT)
const SHADER = preload("res://tools/prototypes/c11c_living_particles_v1/LivingParticles.gdshader")
const TronRoadClass = preload("res://tools/prototypes/c11c_living_particles_v1/LivingParticlesTronRoad.gd")

var _rect: ColorRect
var _material: ShaderMaterial
var _road: Node2D

func _ready() -> void:
    _road = TronRoadClass.new()
    _road.name = "LivingParticlesTronRoad"
    _road.z_index = -10
    add_child(_road)

    _rect = ColorRect.new()
    _rect.name = "LivingParticlesCanvas"
    _rect.position = BODY_RECT.position
    _rect.size = BODY_RECT.size
    _rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
    _material = ShaderMaterial.new()
    _material.shader = SHADER
    _rect.material = _material
    _rect.z_index = 1
    add_child(_rect)

func set_background(background: Color) -> void:
    _material.set_shader_parameter("background_color", background)

func set_palette(deep: Color, mid: Color, bright: Color, highlight: Color) -> void:
    _material.set_shader_parameter("deep_color", deep)
    _material.set_shader_parameter("mid_color", mid)
    _material.set_shader_parameter("bright_color", bright)
    _material.set_shader_parameter("highlight_color", highlight)
    if _road != null and _road.has_method("set_contrast_reference"):
        _road.set_contrast_reference(mid, highlight)

func set_style(grammar_mode: int, particle_count: float, glow_strength: float, attractor_a: Vector2, attractor_b: Vector2, swirl_bias: float, particle_spread: float, turbulence: float, attractor_strength: float, particle_size_scale: float, phase_rate: float, collision_strength: float, core_scale: float, density_bias: float, color_diversity: float, color_phase: float) -> void:
    _material.set_shader_parameter("grammar_mode", clamp(grammar_mode, 0, 4))
    _material.set_shader_parameter("particle_count", clamp(particle_count, 72.0, 180.0))
    _material.set_shader_parameter("glow_strength", clamp(glow_strength, 0.0, 1.0))
    _material.set_shader_parameter("attractor_a", attractor_a)
    _material.set_shader_parameter("attractor_b", attractor_b)
    _material.set_shader_parameter("swirl_bias", swirl_bias)
    _material.set_shader_parameter("particle_spread", clamp(particle_spread, 0.74, 1.24))
    _material.set_shader_parameter("turbulence", clamp(turbulence, 0.010, 0.055))
    _material.set_shader_parameter("attractor_strength", clamp(attractor_strength, 0.60, 1.60))
    _material.set_shader_parameter("particle_size_scale", clamp(particle_size_scale, 0.68, 1.40))
    var safe_phase_rate: float = float(clampi(int(round(phase_rate)), 1, 3))
    _material.set_shader_parameter("phase_rate", safe_phase_rate)
    _material.set_shader_parameter("collision_strength", clamp(collision_strength, 0.60, 1.50))
    _material.set_shader_parameter("core_scale", clamp(core_scale, 0.72, 1.30))
    _material.set_shader_parameter("density_bias", clamp(density_bias, 0.80, 1.25))
    _material.set_shader_parameter("color_diversity", clamp(color_diversity, 0.0, 1.0))
    _material.set_shader_parameter("color_phase", color_phase)

func set_frame(frame_index: int, total_frames: int, seed_phase: float, loop_cycles: float = 1.0) -> void:
    var total: int = maxi(1, total_frames)
    var frame: int = posmod(frame_index, total)
    var cycles: float = max(loop_cycles, 1.0)
    _material.set_shader_parameter("phase", TAU * float(frame) / float(total) * cycles)
    _material.set_shader_parameter("seed_phase", seed_phase)
    if _road != null and _road.has_method("set_frame"):
        _road.set_frame(frame, total, cycles)

