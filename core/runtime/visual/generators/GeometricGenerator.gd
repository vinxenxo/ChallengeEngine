class_name GeometricGenerator
extends VisualLoopGenerator

## C6-F0.4.1 — Geometric Procedural Generator.
## Primitive shapes maintain a 1-period cycle across the loop time regardless of amplitude speed.

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	var speed := float(layer_params.get("speed", 1.0))
	var complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "normal"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	var phase := normalized_loop_time * TAU
	var scale := 1.0 + (0.3 * sin(phase * float(complexity)) * speed)
	
	return {
		"generator": "geometric",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"scale": scale,
			"orbit_angle": phase,
			"sides": maxi(3, complexity + 2)
		}
	}