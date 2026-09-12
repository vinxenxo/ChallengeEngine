class_name GeometricGenerator
extends VisualLoopGenerator

## C6-F0.8-D7 — Geometric Generator Pilot
## Complies strictly with Stream 2005 variation contract (palette_variant, shape_variant).

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	return generate_with_variation(loop_frame, total_frames, layer_params, {})

func generate_with_variation(loop_frame: int, total_frames: int, layer_params: Dictionary, variation: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	# Stream 2005 contract mapping
	var palette_var := float(variation.get("palette_variant", 0.0))
	var shape_var := float(variation.get("shape_variant", 0.5))
	
	var speed := float(layer_params.get("speed", 1.0))
	var base_complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "normal"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	# Mapeo de shape_variant a número de lados discretos [3, 8]
	var sides := int(round(clamp(float(base_complexity) + (shape_var * 4.0), 3.0, 8.0)))
	var rotation_angle := fposmod(normalized_loop_time * speed, 1.0) * TAU
	
	return {
		"generator": "geometric",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"rotation_angle": rotation_angle,
			"sides": sides,
			"zoom": 1.0 + (palette_var * 0.2)
		}
	}