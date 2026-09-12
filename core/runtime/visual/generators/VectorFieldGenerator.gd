class_name VectorFieldGenerator
extends VisualLoopGenerator

## C6-F0.8-D4 — Vector Field Generator Pilot
## Generador migrado para soportar variación determinista inyectada, manteniendo periodicidad.

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	# Fallback seguro para invocaciones legacy
	return generate_with_variation(loop_frame, total_frames, layer_params, {})

func generate_with_variation(loop_frame: int, total_frames: int, layer_params: Dictionary, variation: Dictionary) -> Dictionary:
	var total := maxi(1, total_frames)
	var normalized_loop_time := fposmod(float(loop_frame) / float(total), 1.0)
	
	# 1. Extracción de variación cosmética inyectada (con valores por defecto seguros)
	var palette_var := float(variation.get("palette_variant", 0.0))
	var comp_var_raw := float(variation.get("complexity_variant", 0.5))
	var phase_var := float(variation.get("phase_offset", 0.0))
	var rot_var := float(variation.get("rotation_offset", 0.0))
	
	# 2. Extracción de parámetros lógicos base
	var speed := float(layer_params.get("speed", 1.0))
	var base_complexity := int(layer_params.get("complexity", 1))
	var blend_mode := str(layer_params.get("blend_mode", "normal"))
	var color_palette := str(layer_params.get("color_palette", "default"))
	
	# 3. Matemática Específica de Aislamiento
	# Modulamos la complejidad [0.8x a 1.2x]
	var comp_multiplier := 0.8 + (comp_var_raw * 0.4)
	var modulated_complexity := float(base_complexity) * comp_multiplier
	
	# El ángulo base se desfasa usando phase_var, manteniendo el ciclo TAU perfecto
	var flow_angle := fposmod(normalized_loop_time + phase_var, 1.0) * TAU
	
	# La turbulencia se ve afectada por la complejidad modulada
	var turbulence := sin(flow_angle * modulated_complexity) * 2.0 * speed
	
	# Añadimos un ángulo de rotación global en base a rot_var (constante en todo el loop)
	var global_rotation := rot_var * TAU
	
	return {
		"generator": "vector_field",
		"blend_mode": blend_mode,
		"color_palette": color_palette,
		"parameters": {
			"flow_angle": flow_angle,
			"turbulence": turbulence,
			"grid_density": int(round(clamp(modulated_complexity * 4.0, 4.0, 32.0))),
			"global_rotation": global_rotation,
			"zoom": 1.0 + (palette_var * 0.2)
		}
	}