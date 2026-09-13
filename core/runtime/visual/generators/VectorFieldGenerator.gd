# res://core/runtime/visual/generators/VectorFieldGenerator.gd
class_name VectorFieldGenerator
extends VisualLoopGenerator

## C6-F0.8-D4 — Vector Field Generator Pilot
## Complies strictly with Stream 2002 variation contract (palette_variant, turbulence_variant).

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	return generate_with_variation(loop_frame, total_frames, layer_params, {})

func generate_with_variation(loop_frame: int, total_frames: int, layer_params: Dictionary, variation: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	# Stream 2002 contract mapping
	var palette_var := float(variation.get("palette_variant", 0.0))
	var turbulence_var := float(variation.get("turbulence_variant", 0.5))
	
	var speed := float(layer_params.get("speed", 1.0))
	var base_complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "normal"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	var turbulence_multiplier := 0.5 + (turbulence_var * 1.0)
	var flow_angle := normalized_loop_time * TAU
	var turbulence := sin(flow_angle * float(base_complexity)) * 2.0 * speed * turbulence_multiplier
	
	return {
		"generator": "vector_field",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"flow_angle": flow_angle,
			"turbulence": turbulence,
			"grid_density": base_complexity * 4,
			"zoom": 1.0 + (palette_var * 0.2)
		}
	}