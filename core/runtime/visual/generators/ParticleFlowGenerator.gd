class_name ParticleFlowGenerator
extends VisualLoopGenerator

## C6-F0.8-D5 — Particle Flow Generator Pilot
## Complies strictly with Stream 2003 variation contract (palette_variant, emission_variant).

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	return generate_with_variation(loop_frame, total_frames, layer_params, {})

func generate_with_variation(loop_frame: int, total_frames: int, layer_params: Dictionary, variation: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	# Stream 2003 contract mapping
	var palette_var := float(variation.get("palette_variant", 0.0))
	var emission_var := float(variation.get("emission_variant", 0.5))
	
	var speed := float(layer_params.get("speed", 1.0))
	var base_complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "alpha"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	var emitter_spread := 0.5 + (palette_var * 0.5)
	var emission_multiplier := 0.75 + (emission_var * 0.5)
	var particle_count := int(round(clamp(float(base_complexity) * 12.0 * emission_multiplier, 8.0, 64.0)))
	
	var time_cycle := fposmod((normalized_loop_time * speed), 1.0) * TAU
	var dispersion := sin(time_cycle) * emitter_spread
	
	return {
		"generator": "particle_flow",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"time_cycle": time_cycle,
			"dispersion": dispersion,
			"particle_count": particle_count,
			"global_rotation": 0.0,
			"zoom": 1.0 + (palette_var * 0.15)
		}
	}