# res://core/runtime/visual_drill/generators/TrackingGenerator.gd
class_name TrackingGenerator
extends VisualDrillGenerator

## Visual Drill Tracking Generator.
## Generates deterministic frame states for the tracking exercise supporting Stream 2011.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	return generate_with_variation(frame_index, total_frames, drill_parameters, {})

func generate_with_variation(frame_index: int, total_frames: int, drill_parameters: Dictionary, variation: Dictionary) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(maxi(1, total_frames - 1))
		
	var tracking_var := float(variation.get("tracking_variant", 0.0))
	
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", { "x": 0.0, "y": 0.0, "active": true })
	var targets_def: Array = drill_parameters.get("targets", [])
	var distractors_def: Array = drill_parameters.get("distractors", [])
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	return {
		"generator_type": "tracking",
		"progress": progress,
		"stimulus_state": stimulus_def.duplicate(true),
		"target_states": targets_def.duplicate(true),
		"distractor_states": distractors_def.duplicate(true),
		"task_state": task_def.duplicate(true),
		"parameters": {
			"tracking_variant": tracking_var
		}
	}