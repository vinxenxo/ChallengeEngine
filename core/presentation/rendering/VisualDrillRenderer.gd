class_name VisualDrillRenderer
extends Node2D

## C6-F0.5 Step 2 — Visual Drill Renderer.
## Pure functional visual representation of a VisualDrillFrameState.

var _frame_state: Dictionary = {}

func apply_state(state: Dictionary) -> void:
	_frame_state = state.duplicate(true)
	queue_redraw()

func _draw() -> void:
	if _frame_state.is_empty():
		return
		
	var stimulus: Dictionary = _frame_state.get("stimulus_state", {})
	if not stimulus.is_empty() and bool(stimulus.get("active", true)):
		var s_pos := Vector2(float(stimulus.get("x", 0.0)), float(stimulus.get("y", 0.0)))
		draw_circle(s_pos, 10.0, Color.WHITE)
		
	var targets: Array = _frame_state.get("target_states", [])
	for target in targets:
		if typeof(target) == TYPE_DICTIONARY:
			var t_pos := Vector2(float(target.get("x", 0.0)), float(target.get("y", 0.0)))
			
			var is_highlighted := false
			if target.has("highlighted") and bool(target["highlighted"]):
				is_highlighted = true
			elif target.has("status") and str(target["status"]) == "active":
				is_highlighted = true
				
			var color := Color(0.2, 1.0, 0.3, 1.0) if is_highlighted else Color(0.4, 0.6, 0.4, 0.8)
			draw_circle(t_pos, 12.0, color)
			draw_arc(t_pos, 16.0, 0, TAU, 16, color, 2.0)
			
	var distractors: Array = _frame_state.get("distractor_states", [])
	for distractor in distractors:
		if typeof(distractor) == TYPE_DICTIONARY:
			var d_pos := Vector2(float(distractor.get("x", 0.0)), float(distractor.get("y", 0.0)))
			draw_circle(d_pos, 8.0, Color(0.8, 0.2, 0.2, 0.7))