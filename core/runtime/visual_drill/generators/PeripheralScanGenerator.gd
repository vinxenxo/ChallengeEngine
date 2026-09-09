class_name PeripheralScanGenerator
extends VisualDrillGenerator

## C6-F0.4.2 — Peripheral Scan Procedural Generator.
## Computes central fixation reference and peripheral target distributions.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames - 1)
	var progress := float(frame_index) / float(total)
	
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", {})
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	# Peripheral targets flashing or pulsing deterministically
	var pulse := 0.5 + 0.5 * sin(progress * TAU * 4.0)
	
	return {
		"generator_type": "peripheral_scan",
		"stimulus_state": {
			"type": stimulus_def.get("type", "dot"),
			"x": 0.0,
			"y": 0.0,
			"fixation": true
		},
		"target_states": [
			{"id": 0, "x": -200.0, "y": 0.0, "intensity": pulse},
			{"id": 1, "x": 200.0, "y": 0.0, "intensity": 1.0 - pulse}
		],
		"distractor_states": [
			{"id": 10, "x": 0.0, "y": -150.0, "intensity": 0.3}
		],
		"trajectory_state": {
			"pattern": "radial_scan",
			"pulse": pulse
		},
		"task_state": {
			"type": task_def.get("type", "peripheral_scan"),
			"status": "scanning"
		}
	}