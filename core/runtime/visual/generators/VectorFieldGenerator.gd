class_name VectorFieldGenerator
extends VisualLoopGenerator

## C6-F0.4.1 — Vector Field Procedural Generator.
## Speed acts as turbulence amplitude multiplier, maintaining fundamental base periodic boundary.

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	var speed := float(layer_params.get("speed", 1.0))
	var complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "normal"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	var flow_angle := normalized_loop_time * TAU
	var turbulence := sin(flow_angle * float(complexity)) * 2.0 * speed
	
	return {
		"generator": "vector_field",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"flow_angle": flow_angle,
			"turbulence": turbulence,
			"grid_density": complexity * 4
		}
	}