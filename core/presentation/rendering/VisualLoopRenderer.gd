class_name VisualLoopRenderer
extends Node2D

## C6-F0.5 Step 2 / C6-F0.8-D2-C — Visual Loop Renderer Router.
## Hosts specific visual generators (like FractalRenderer) and preserves legacy diagnostic drawing.

const FractalRendererClass = preload("res://core/presentation/rendering/FractalRenderer.gd")

var _frame_state: Dictionary = {}
var _fractal_renderer: Node2D = null

func _ready() -> void:
	_fractal_renderer = FractalRendererClass.new()
	_fractal_renderer.visible = false
	add_child(_fractal_renderer)

func apply_state(model: Dictionary) -> void:
	_frame_state = model.duplicate(true)
	
	var v_state: Dictionary = model.get("visual_frame_state", model)
	var generator_type := str(v_state.get("generator", v_state.get("generator_type", "")))
	
	if generator_type == "fractal":
		_fractal_renderer.visible = true
		_fractal_renderer.apply_state(model)
		queue_redraw()
	else:
		_fractal_renderer.visible = false
		queue_redraw()

func _draw() -> void:
	if _frame_state.is_empty() or (_fractal_renderer != null and _fractal_renderer.visible):
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
		
		if generator_type == "vector_field":
			draw_line(Vector2.ZERO, Vector2(80.0, 0.0), color * Color(0.8, 0.3, 0.5, 1.0), 3.0)
		elif generator_type == "particle_flow":
			draw_circle(Vector2(40.0, 0.0), 4.0, color * Color(0.3, 0.9, 0.5, 1.0))
		elif generator_type == "kaleidoscope":
			draw_rect(Rect2(-30.0, -30.0, 60.0, 60.0), color * Color(0.9, 0.2, 0.2, 1.0))
		elif generator_type == "geometric":
			draw_rect(Rect2(-35.0, -35.0, 70.0, 70.0), color * Color(0.6, 0.3, 0.9, 1.0), false, 4.0)
		else:
			draw_circle(Vector2.ZERO, 30.0, color)
			
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)