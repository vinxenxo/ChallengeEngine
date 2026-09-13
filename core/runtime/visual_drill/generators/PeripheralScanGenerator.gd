# res://core/runtime/visual_drill/generators/PeripheralScanGenerator.gd
class_name PeripheralScanGenerator
extends VisualDrillGenerator

## C6-F0.8-E1 — Visual Drill PeripheralScan Generator.
## Generates deterministic frame states for the peripheral scan exercise supporting Stream 2014.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	return generate_with_variation(frame_index, total_frames, drill_parameters, {})

func generate_with_variation(frame_index: int, total_frames: int, drill_parameters: Dictionary, variation: Dictionary) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(maxi(1, total_frames - 1))
		
	var pattern_var := float(variation.get("pattern_variant", 0.0))
	var amplitude_var := float(variation.get("amplitude_variant", 0.5))
	
	var stimulus_def: Dictionary = drill_parameters.get("stimulus", { "x": 0.0, "y": 0.0, "active": true })
	var targets_def: Array = drill_parameters.get("targets", [])
	var distractors_def: Array = drill_parameters.get("distractors", [])
	var task_def: Dictionary = drill_parameters.get("task", {})
	
	var modulated_stimulus = stimulus_def.duplicate(true)
	if modulated_stimulus.has("x") and modulated_stimulus.has("y"):
		var offset_scale := 0.8 + (amplitude_var * 0.4)
		var angle_shift := pattern_var * TAU
		var x := float(modulated_stimulus["x"])
		var y := float(modulated_stimulus["y"])
		modulated_stimulus["x"] = x * offset_scale + cos(angle_shift + progress * TAU) * 5.0
		modulated_stimulus["y"] = y * offset_scale + sin(angle_shift + progress * TAU) * 5.0

	return {
		"generator_type": "peripheral_scan",
		"progress": progress,
		"stimulus_state": modulated_stimulus,
		"target_states": targets_def.duplicate(true),
		"distractor_states": distractors_def.duplicate(true),
		"task_state": task_def.duplicate(true),
		"parameters": {
			"pattern_variant": pattern_var,
			"amplitude_variant": amplitude_var
		}
	}