# res://core/runtime/visual/generators/KaleidoscopeGenerator.gd
class_name KaleidoscopeGenerator
extends VisualLoopGenerator

## C6-F0.8-D6 — Kaleidoscope Generator Pilot
## Complies strictly with Stream 2004 variation contract (palette_variant, symmetry_variant).

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	return generate_with_variation(loop_frame, total_frames, layer_params, {})

func generate_with_variation(loop_frame: int, total_frames: int, layer_params: Dictionary, variation: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	# Stream 2004 contract mapping
	var palette_var := float(variation.get("palette_variant", 0.0))
	var symmetry_var := float(variation.get("symmetry_variant", 0.5))
	
	var speed := float(layer_params.get("speed", 1.0))
	var base_complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "alpha"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	# Mapeo de symmetry_variant a divisiones geométricas discretas [4, 12]
	var symmetry_folds := int(round(clamp(float(base_complexity) * 2.0 + (symmetry_var * 6.0), 4.0, 12.0)))
	
	var rotation_angle := fposmod(normalized_loop_time * speed, 1.0) * TAU
	
	return {
		"generator": "kaleidoscope",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"rotation_angle": rotation_angle,
			"symmetry_folds": symmetry_folds,
			"zoom": 1.0 + (palette_var * 0.2)
		}
	}