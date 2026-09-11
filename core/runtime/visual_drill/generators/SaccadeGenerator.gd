class_name SaccadeGenerator
extends VisualDrillGenerator

## C6-F0.8-E — Saccade Drill Generator.
## Computes discrete spatial jumps between target positions to train rapid ballistic eye movements.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary, rng_context = null) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", {})
	var targets_def: Array = drill_parameters.get("targets", [])
	var distractors_def: Array = drill_parameters.get("distractors", [])
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	var step_count := 4
	var current_step = int(progress * step_count) % max(1, targets_def.size())
	
	var current_targets = []
	for i in range(targets_def.size()):
		var target = targets_def[i].duplicate(true)
		target["active"] = (i == current_step)
		current_targets.append(target)

	return {
		"generator_type": "saccade",
		"progress": progress,
		"stimulus_state": stimulus_def.duplicate(true),
		"target_states": current_targets,
		"distractor_states": distractors_def.duplicate(true),
		"task_state": task_def.duplicate(true)
	}