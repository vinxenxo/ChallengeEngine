class_name FractalGenerator
extends VisualLoopGenerator

## C6-F0.8-D2-A — Fractal Generator Pilot
## Pure mathematical function taking logical parameters and decoupled variation.

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	# Fallback seguro para invocaciones legacy
	return generate_with_variation(loop_frame, total_frames, layer_params, {})

func generate_with_variation(loop_frame: int, total_frames: int, layer_params: Dictionary, variation: Dictionary) -> Dictionary:
	# Normalización periódica (fposmod garantiza que frame 0 == frame total_frames)
	var normalized_time := fposmod(float(loop_frame) / float(max(total_frames, 1)), 1.0)
	
	# 1. Extracción de variación cosmética inyectada (con valores por defecto limpios)
	var palette_var := float(variation.get("palette_variant", 0.0))
	var comp_var_raw := float(variation.get("complexity_variant", 0.5)) # Centro por defecto
	var phase_var := float(variation.get("phase_offset", 0.0))
	var rot_var := float(variation.get("rotation_offset", 0.0))
	
	# 2. Extracción de parámetros lógicos de la capa
	var base_speed := float(layer_params.get("speed", 1.0))
	var base_complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "alpha"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	# 3. Matemática Específica y Segura de Aislamiento
	# Mapeamos [0, 1) a un multiplicador lógico [0.8, 1.2] para no colapsar la complejidad
	var comp_multiplier := 0.8 + (comp_var_raw * 0.4)
	var modulated_complexity := float(base_complexity) * comp_multiplier
	
	# Ciclo armónico utilizando TAU para cierre periódico perfecto
	var cycle := (normalized_time * base_speed + phase_var) * TAU
	
	var final_complexity := modulated_complexity + (sin(cycle) * 0.2)
	var final_rotation := rot_var + (cos(cycle) * 0.1)
	var final_zoom := 1.0 + (palette_var * 0.1)
	
	# 4. Strict Baseline Logical Layer State Contract
	return {
		"generator": "fractal",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"zoom": final_zoom,
			"rotation": final_rotation,
			"phase": phase_var + normalized_time,
			"complexity": int(round(clamp(final_complexity, 1.0, 10.0)))
		}
	}