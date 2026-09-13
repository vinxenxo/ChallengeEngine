# res://core/runtime/visual_drill/generators/PursuitGenerator.gd
class_name PursuitGenerator
extends VisualDrillGenerator

## Visual Drill Pursuit Generator.
## Generates deterministic frame states for the pursuit exercise supporting Stream 2012.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	return generate_with_variation(frame_index, total_frames, drill_parameters, {})

func generate_with_variation(frame_index: int, total_frames: int, drill_parameters: Dictionary, variation: Dictionary) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(maxi(1, total_frames - 1))
		
	var pursuit_var := float(variation.get("pursuit_variant", 0.0))
	
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", { "x": 0.0, "y": 0.0, "active": true })
	var targets_def: Array = drill_parameters.get("targets", [])
	var distractors_def: Array = drill_parameters.get("distractors", [])
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	return {
		"generator_type": "pursuit",
		"progress": progress,
		"stimulus_state": stimulus_def.duplicate(true),
		"target_states": targets_def.duplicate(true),
		"distractor_states": distractors_def.duplicate(true),
		"task_state": task_def.duplicate(true),
		"parameters": {
			"pursuit_variant": pursuit_var
		}
	}