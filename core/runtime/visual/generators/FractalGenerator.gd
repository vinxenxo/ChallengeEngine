class_name FractalGenerator
extends VisualLoopGenerator

## C6-F0.8-D — Fractal Visual Loop Generator with Cosmetic RNG Integration.
## Computes rich recursive fractal states, layer transformations, and deterministic aesthetic variants.

func generate(frame_index: int, total_frames: int, loop_parameters: Dictionary, rng_context = null) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var visual_params: Dictionary = loop_parameters.get("visual_parameters", {})
	var raw_layers: Array = visual_params.get("layers", [])
	
	var base_hue := 0.5
	var complexity := int(visual_params.get("complexity", 2))
	if rng_context != null:
		base_hue = rng_context.sample_float(2001, 0)
		complexity = int(rng_context.sample_float_range(2001, 1, 1.0, 5.0))
		
	var processed_layers: Array = []
	for i in range(raw_layers.size()):
		var layer = raw_layers[i]
		var speed: float = float(layer.get("speed", 1.0))
		var angle := progress * TAU * speed
		
		processed_layers.append({
			"blend_mode": layer.get("blend_mode", "normal"),
			"speed": speed,
			"complexity": complexity,
			"rotation": angle,
			"zoom": 1.0 + sin(angle * 2.0) * 0.2,
			"phase": angle,
			"base_hue": base_hue
		})

	return {
		"generator_type": "fractal",
		"progress": progress,
		"layers": processed_layers,
		"global_transform": {
			"zoom": 1.0,
			"rotation": progress * TAU * 0.1
		}
	}