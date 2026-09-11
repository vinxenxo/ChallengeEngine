class_name PursuitGenerator
extends VisualDrillGenerator

## C6-F0.8-E — Pursuit Drill Generator.
## Computes active moving target trajectories requiring smooth continuous visual pursuit.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary, rng_context = null) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var trajectory_def: Dictionary = drill_parameters.get("trajectory", {})
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", {})
	var targets_def: Array = drill_parameters.get("targets", [])
	var distractors_def: Array = drill_parameters.get("distractors", [])
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	var current_targets = []
	for t in targets_def:
		var target = t.duplicate(true)
		var base_x = float(target.get("x", 0.0))
		var base_y = float(target.get("y", 0.0))
		target["x"] = base_x + sin(progress * TAU) * 50.0
		target["y"] = base_y + cos(progress * TAU) * 50.0
		current_targets.append(target)

	return {
		"generator_type": "pursuit",
		"progress": progress,
		"stimulus_state": stimulus_def.duplicate(true),
		"target_states": current_targets,
		"distractor_states": distractors_def.duplicate(true),
		"task_state": task_def.duplicate(true)
	}