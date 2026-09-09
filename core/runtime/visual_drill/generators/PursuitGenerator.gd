class_name PursuitGenerator
extends VisualDrillGenerator

## C6-F0.4.2 — Pursuit Procedural Generator.
## Computes multi-element relative pursuit kinematics.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames - 1)
	var progress := float(frame_index) / float(total)
	
	var angle := progress * TAU * 1.5
	var target_x := cos(angle) * 200.0
	var target_y := sin(angle) * 200.0
	
	# Pursuer lags behind target deterministically
	var lag_angle := (progress - 0.05) * TAU * 1.5
	var pursuer_x := cos(lag_angle) * 180.0
	var pursuer_y := sin(lag_angle) * 180.0
	
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", {})
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	return {
		"generator_type": "pursuit",
		"stimulus_state": {
			"type": stimulus_def.get("type", "target"),
			"x": target_x,
			"y": target_y,
			"active": true
		},
		"target_states": [
			{"id": 0, "x": target_x, "y": target_y, "role": "lead"},
			{"id": 1, "x": pursuer_x, "y": pursuer_y, "role": "pursuer"}
		],
		"distractor_states": [],
		"trajectory_state": {
			"pattern": "orbital",
			"phase": angle
		},
		"task_state": {
			"type": task_def.get("type", "pursuit"),
			"status": "active"
		}
	}