class_name TrackingGenerator
extends VisualDrillGenerator

## C6-F0.4.2 — Tracking Procedural Generator.
## Computes continuous smooth pursuit / tracking trajectories and target/stimulus states.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames - 1)
	var progress := float(frame_index) / float(total)
	
	var trajectory_def: Dictionary = drill_parameters.get("trajectory", {})
	var pattern := str(trajectory_def.get("pattern", "linear"))
	var speed := float(trajectory_def.get("speed", 1.0))
	
	# Deterministic trajectory math
	var angle := progress * TAU * speed
	var pos_x := cos(angle) * 150.0
	var pos_y := sin(angle * 0.5) * 100.0 if pattern == "lissajous" else sin(angle) * 100.0
	
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", {})
	var targets_def: Dictionary = drill_parameters.get("targets", {})
	var distractors_def: Dictionary = drill_parameters.get("distractors", {})
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	return {
		"generator_type": "tracking",
		"stimulus_state": {
			"type": stimulus_def.get("type", "dot"),
			"x": pos_x,
			"y": pos_y,
			"active": true
		},
		"target_states": [
			{"id": 0, "x": pos_x, "y": pos_y, "status": "active"}
		],
		"distractor_states": [],
		"trajectory_state": {
			"pattern": pattern,
			"current_angle": angle
		},
		"task_state": {
			"type": task_def.get("type", "tracking"),
			"status": "in_progress"
		}
	}