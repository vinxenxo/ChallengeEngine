class_name ParticleFlowGenerator
extends VisualLoopGenerator

## C6-F0.8-D — Particle Flow Visual Loop Generator.
## Computes multi-particle arrays, velocities, emission phases, and cosmetic variants.

func generate(frame_index: int, total_frames: int, loop_parameters: Dictionary, rng_context = null) -> Dictionary:
	var progress := 0.0
	if total_frames > 1:
		progress = float(frame_index) / float(total_frames - 1)
		
	var particle_count := 30
	var emission_spread := 100.0
	if rng_context != null:
		particle_count = int(rng_context.sample_float_range(2003, 0, 20.0, 60.0))
		emission_spread = rng_context.sample_float_range(2003, 1, 50.0, 150.0)
		
	return {
		"generator_type": "particle_flow",
		"progress": progress,
		"particle_count": particle_count,
		"emission_spread": emission_spread,
		"time_phase": progress * TAU * 3.0
	}