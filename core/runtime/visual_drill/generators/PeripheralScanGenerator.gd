class_name PeripheralScanGenerator
extends VisualDrillGenerator

## C6-F0.8-E — Peripheral Scan Drill Generator.
## Distributes stimuli and distractors spatially to train wide-field attention and peripheral detection.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary, rng_context = null) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", {})
	var targets_def: Array = drill_parameters.get("targets", [])
	var distractors_def: Array = drill_parameters.get("distractors", [])
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	var current_distractors = []
	for i in range(distractors_def.size()):
		var dist = distractors_def[i].duplicate(true)
		dist["highlighted"] = fmod(progress * 4.0 + float(i), 2.0) < 1.0
		current_distractors.append(dist)

	return {
		"generator_type": "peripheral_scan",
		"progress": progress,
		"stimulus_state": stimulus_def.duplicate(true),
		"target_states": targets_def.duplicate(true),
		"distractor_states": current_distractors,
		"task_state": task_def.duplicate(true)
	}