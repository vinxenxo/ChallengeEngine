class_name VisualLoopRenderer
extends Node2D

## C6-F0.5 Step 2 — Visual Loop Renderer.
## Pure functional visual representation of a VisualFrameState.
## Recomputes nothing. It strictly maps pre-calculated 'layer_states'.

var _frame_state: Dictionary = {}

func apply_state(state: Dictionary) -> void:
	_frame_state = state.duplicate(true)
	queue_redraw()

func _draw() -> void:
	if _frame_state.is_empty():
		return
		
	var generator_type := str(_frame_state.get("generator_type", "fractal"))
	var layers: Array = _frame_state.get("layer_states", [])
	
	for layer in layers:
		if typeof(layer) != TYPE_DICTIONARY:
			continue
			
		var layer_rot := float(layer.get("rotation", 0.0))
		var layer_scale := float(layer.get("scale", 1.0))
		var layer_alpha := float(layer.get("alpha", 1.0))
		var color := Color(1.0, 1.0, 1.0, layer_alpha)
		
		draw_set_transform(Vector2.ZERO, layer_rot, Vector2(layer_scale, layer_scale))
		
		if generator_type == "fractal":
			draw_circle(Vector2.ZERO, 50.0, color * Color(0.2, 0.6, 0.9, 1.0))
			draw_arc(Vector2.ZERO, 75.0, 0, TAU, 32, color, 2.0)
		elif generator_type == "vector_field":
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