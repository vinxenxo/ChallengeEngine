class_name SaccadeGenerator
extends VisualDrillGenerator

## C6-F0.4.2 — Saccade Procedural Generator.
## Computes discrete spatial step transitions and target activations.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames - 1)
	var progress := float(frame_index) / float(total)
	
	# Switch active target index every 25% of progress
	var active_step := mini(3, int(progress * 4.0))
	var positions := [
		Vector2(-150, -100),
		Vector2(150, -100),
		Vector2(150, 100),
		Vector2(-150, 100)
	]
	var current_pos: Vector2 = positions[active_step]
	
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", {})
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	var target_list: Array[Dictionary] = []
	for i in range(positions.size()):
		target_list.append({
			"id": i,
			"x": positions[i].x,
			"y": positions[i].y,
			"highlighted": (i == active_step)
		})
		
	return {
		"generator_type": "saccade",
		"stimulus_state": {
			"type": stimulus_def.get("type", "ring"),
			"x": current_pos.x,
			"y": current_pos.y,
			"active_index": active_step
		},
		"target_states": target_list,
		"distractor_states": [],
		"trajectory_state": {
			"pattern": "discrete_jump",
			"step": active_step
		},
		"task_state": {
			"type": task_def.get("type", "saccade"),
			"active_target": active_step
		}
	}