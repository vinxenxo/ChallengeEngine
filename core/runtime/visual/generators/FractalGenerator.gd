class_name FractalGenerator
extends VisualLoopGenerator

## C6-F0.4.1 — Fractal Procedural Generator.
## Speed acts as a phase offset and amplitude modulator. Base periodicity remains intact for seamless wrapping.

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	var speed := float(layer_params.get("speed", 1.0))
	var complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "normal"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	# Base fundamental phase (period exactly 1 across the normalized loop time)
	var phase := normalized_loop_time * TAU
	
	# Modulations preserve the fundamental 2*PI boundary
	var zoom := 1.0 + 0.5 * sin(phase) * float(complexity) * speed
	var rotation := cos(phase) * 0.25 * float(complexity) * speed
	
	return {
		"generator": "fractal",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"zoom": zoom,
			"rotation": rotation,
			"phase": phase,
			"complexity": complexity
		}
	}