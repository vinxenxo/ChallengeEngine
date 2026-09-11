class_name VectorFieldGenerator
extends VisualLoopGenerator

## C6-F0.8-D — Vector Field Visual Loop Generator.
## Computes dynamic multi-vector grids and turbulent flow states.

func generate(frame_index: int, total_frames: int, loop_parameters: Dictionary, rng_context = null) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var visual_params: Dictionary = loop_parameters.get("visual_parameters", {})
	var turbulence := 1.0
	if rng_context != null:
		turbulence = rng_context.sample_float_range(2002, 0, 0.5, 2.5)
		
	return {
		"generator_type": "vector_field",
		"progress": progress,
		"grid_resolution": {"cols": 8, "rows": 14},
		"turbulence": turbulence,
		"time_phase": progress * TAU * 2.0
	}