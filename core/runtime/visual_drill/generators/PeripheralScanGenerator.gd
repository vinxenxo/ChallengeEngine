class_name PeripheralScanGenerator
extends VisualDrillGenerator

## C6-F0.4.2 — Visual Drill PeripheralScan Generator.
## Generates deterministic frame states for the drill exercise.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", { "x": 0.0, "y": 0.0, "active": true })
	var targets_def: Array = drill_parameters.get("targets", [])
	var distractors_def: Array = drill_parameters.get("distractors", [])
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	return {
		"generator_type": "peripheral_scan",
		"progress": progress,
		"stimulus_state": stimulus_def.duplicate(true),
		"target_states": targets_def.duplicate(true),
		"distractor_states": distractors_def.duplicate(true),
		"task_state": task_def.duplicate(true)
	}