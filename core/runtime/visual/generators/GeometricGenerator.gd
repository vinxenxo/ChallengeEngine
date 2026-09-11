class_name GeometricGenerator
extends VisualLoopGenerator

## C6-F0.8-D — Geometric Visual Loop Generator.
## Computes nested regular polygons, orbit frequencies, and multi-layer scaling.

func generate(frame_index: int, total_frames: int, loop_parameters: Dictionary, rng_context = null) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var sides := 4
	var orbit_radius := 120.0
	if rng_context != null:
		sides = int(rng_context.sample_float_range(2005, 0, 3.0, 8.0))
		orbit_radius = rng_context.sample_float_range(2005, 1, 80.0, 180.0)
		
	return {
		"generator_type": "geometric",
		"progress": progress,
		"sides": sides,
		"orbit_radius": orbit_radius,
		"phase": progress * TAU
	}