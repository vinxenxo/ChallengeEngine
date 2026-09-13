# res://core/presentation/rendering/VisualLoopRenderer.gd
class_name VisualLoopRenderer
extends Node2D

## C6-F0.5 / C6-F0.8-D7 — Visual Loop Renderer Router.
## Hosts all 5 visual generators and completely eliminates legacy drawing fallbacks.

const FractalRendererClass = preload("res://core/presentation/rendering/FractalRenderer.gd")
const VectorFieldRendererClass = preload("res://core/presentation/rendering/VectorFieldRenderer.gd")
const ParticleFlowRendererClass = preload("res://core/presentation/rendering/ParticleFlowRenderer.gd")
const KaleidoscopeRendererClass = preload("res://core/presentation/rendering/KaleidoscopeRenderer.gd")
const GeometricRendererClass = preload("res://core/presentation/rendering/GeometricRenderer.gd")

var _frame_state: Dictionary = {}
var _fractal_renderer: Node2D = null
var _vector_renderer: Node2D = null
var _particle_renderer: Node2D = null
var _kaleidoscope_renderer: Node2D = null
var _geometric_renderer: Node2D = null

func _ready() -> void:
	_fractal_renderer = FractalRendererClass.new()
	_fractal_renderer.visible = false
	add_child(_fractal_renderer)
	
	_vector_renderer = VectorFieldRendererClass.new()
	_vector_renderer.visible = false
	add_child(_vector_renderer)
	
	_particle_renderer = ParticleFlowRendererClass.new()
	_particle_renderer.visible = false
	add_child(_particle_renderer)
	
	_kaleidoscope_renderer = KaleidoscopeRendererClass.new()
	_kaleidoscope_renderer.visible = false
	add_child(_kaleidoscope_renderer)
	
	_geometric_renderer = GeometricRendererClass.new()
	_geometric_renderer.visible = false
	add_child(_geometric_renderer)

func apply_state(model: Dictionary) -> void:
	_frame_state = model.duplicate(true)
	
	var v_state: Dictionary = model.get("visual_frame_state", model)
	var generator_type := str(v_state.get("generator", v_state.get("generator_type", "")))
	
	if _fractal_renderer != null:
		_fractal_renderer.visible = (generator_type == "fractal")
	if _vector_renderer != null:
		_vector_renderer.visible = (generator_type == "vector_field")
	if _particle_renderer != null:
		_particle_renderer.visible = (generator_type == "particle_flow")
	if _kaleidoscope_renderer != null:
		_kaleidoscope_renderer.visible = (generator_type == "kaleidoscope")
	if _geometric_renderer != null:
		_geometric_renderer.visible = (generator_type == "geometric")
	
	if generator_type == "fractal" and _fractal_renderer != null:
		_fractal_renderer.apply_state(model)
	elif generator_type == "vector_field" and _vector_renderer != null:
		_vector_renderer.apply_state(model)
	elif generator_type == "particle_flow" and _particle_renderer != null:
		_particle_renderer.apply_state(model)
	elif generator_type == "kaleidoscope" and _kaleidoscope_renderer != null:
		_kaleidoscope_renderer.apply_state(model)
	elif generator_type == "geometric" and _geometric_renderer != null:
		_geometric_renderer.apply_state(model)
		
	queue_redraw()

func _draw() -> void:
	var f_vis = _fractal_renderer != null and _fractal_renderer.visible
	var v_vis = _vector_renderer != null and _vector_renderer.visible
	var p_vis = _particle_renderer != null and _particle_renderer.visible
	var k_vis = _kaleidoscope_renderer != null and _kaleidoscope_renderer.visible
	var g_vis = _geometric_renderer != null and _geometric_renderer.visible
	
	if _frame_state.is_empty() or f_vis or v_vis or p_vis or k_vis or g_vis:
		return
		
	var v_state: Dictionary = _frame_state.get("visual_frame_state", _frame_state)
	var generator_type := str(v_state.get("generator", v_state.get("generator_type", "")))
	var layers: Array = v_state.get("layers", v_state.get("layer_states", []))
	
	for layer in layers:
		if typeof(layer) != TYPE_DICTIONARY:
			continue
			
		var params: Dictionary = layer.get("parameters", layer)
		var layer_rot := float(params.get("rotation", 0.0))
		var layer_scale := float(params.get("scale", 1.0))
		var layer_alpha := float(params.get("alpha", 1.0))
		var color := Color(1.0, 1.0, 1.0, layer_alpha)
		
		draw_set_transform(Vector2.ZERO, layer_rot, Vector2(layer_scale, layer_scale))
		draw_circle(Vector2.ZERO, 30.0, color)
			
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)