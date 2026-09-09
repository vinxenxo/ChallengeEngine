class_name KaleidoscopeGenerator
extends VisualLoopGenerator

## C6-F0.4.1 — Kaleidoscope Procedural Generator.
## Speed modifies radial amplitude, preserving the fundamental closed-loop angle.

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	var speed := float(layer_params.get("speed", 1.0))
	var complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "normal"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	var sectors := maxi(3, complexity * 2)
	var angle_offset := normalized_loop_time * TAU
	
	return {
		"generator": "kaleidoscope",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"sectors": sectors,
			"angle_offset": angle_offset,
			"symmetry_factor": 1.0 + (0.2 * cos(angle_offset) * speed)
		}
	}