class_name KaleidoscopeGenerator
extends VisualLoopGenerator

## C6-F0.8-D — Kaleidoscope Visual Loop Generator.
## Computes radial symmetry sectors, angular offsets, and mirrored transforms.

func generate(frame_index: int, total_frames: int, loop_parameters: Dictionary, rng_context = null) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var sectors := 6
	var rotation_speed := 1.0
	if rng_context != null:
		sectors = int(rng_context.sample_float_range(2004, 0, 4.0, 12.0))
		rotation_speed = rng_context.sample_float_range(2004, 1, 0.5, 2.0)
		
	return {
		"generator_type": "kaleidoscope",
		"progress": progress,
		"sectors": sectors,
		"rotation": progress * TAU * rotation_speed
	}