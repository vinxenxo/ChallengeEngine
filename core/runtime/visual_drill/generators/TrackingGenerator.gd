class_name TrackingGenerator
extends VisualDrillGenerator

## C6-F0.4.2 — Visual Drill Tracking Generator.
## Generates deterministic frame states for tracking exercises.
## Strictly parses definition collections (Arrays) and objects (Dictionaries).

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	var trajectory_def: Dictionary = drill_parameters.get("trajectory", {})
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", {})
	
	var targets_def: Array = drill_parameters.get("targets", [])
	var distractors_def: Array = drill_parameters.get("distractors", [])
	
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var current_stimulus = stimulus_def.duplicate(true)
	if trajectory_def.get("type", "") == "circular":
		var center_x: float = float(trajectory_def.get("center_x", 0.0))
		var center_y: float = float(trajectory_def.get("center_y", 0.0))
		var radius: float = float(trajectory_def.get("radius", 100.0))
		var speed: float = float(trajectory_def.get("speed", 1.0))
		
		var angle := progress * TAU * speed
		current_stimulus["x"] = center_x + cos(angle) * radius
		current_stimulus["y"] = center_y + sin(angle) * radius

	var payload := {
		"generator_type": "tracking",
		"progress": progress,
		"stimulus_state": current_stimulus,
		"target_states": targets_def.duplicate(true),
		"distractor_states": distractors_def.duplicate(true),
		"task_state": task_def.duplicate(true)
	}
	
	return payload