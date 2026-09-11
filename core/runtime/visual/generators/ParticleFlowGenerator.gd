class_name ParticleFlowGenerator
extends VisualLoopGenerator

## C6-F0.4.1 — Particle Flow Procedural Generator.
## Stateless periodic flow. Sampled particles act as diagnostic representation. Speed modulates radius amplitude.

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	var speed := float(layer_params.get("speed", 1.0))
	var complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "normal"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	var particle_count := complexity * 16
	var representative_particles: Array[Dictionary] = []
	
	for i in range(min(particle_count, 8)):
		var pi_norm := float(i) / float(particle_count)
		# Angle wraps perfectly across normalized_loop_time. Speed alters starting spatial rotation, not time frequency.
		var angle := fposmod(normalized_loop_time * TAU + pi_norm * TAU, TAU)
		var radius := 50.0 + (30.0 * sin(normalized_loop_time * TAU * 2.0 + pi_norm * PI) * speed)
		representative_particles.append({
			"id": i,
			"x": cos(angle) * radius,
			"y": sin(angle) * radius
		})
		
	return {
		"generator": "particle_flow",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"particle_count": particle_count,
			"emitter_phase": fposmod(normalized_loop_time * TAU, TAU),
			"representative_particles": representative_particles
		}
	}