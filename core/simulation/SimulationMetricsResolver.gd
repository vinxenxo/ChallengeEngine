# res://core/simulation/SimulationMetricsResolver.gd
class_name SimulationMetricsResolver
extends RefCounted

const MIN_CLOSE_CALL_FRAMES: int = 12

static func resolve_metrics(result: SimulationResult) -> void:
	# 1. Salvaguardas operativas: No derivar nada sobre errores o vacíos
	if result.error_state != "OK":
		return
		
	if result.frames.is_empty():
		return

	# 2. Respetar la autoridad de la mecánica si ya provee el dato
	if result.metadata.has("close_calls"):
		result.metadata["close_calls_source"] = "MECHANIC"
		return

	# 3. Validar pre-requisitos matemáticos antes de operar
	if is_nan(result.tolerance_threshold) or is_inf(result.tolerance_threshold) or result.tolerance_threshold < 0.0:
		result.error_state = "INVALID_TOLERANCE_FOR_METRICS"
		return

	var close_threshold: float = result.tolerance_threshold * 3.5
	var current_streak: int = 0
	var close_calls_count: int = 0

	# 4. Derivación del algoritmo legacy (Rachas episódicas)
	for i: int in range(result.frames.size()):
		var snapshot: FrameSnapshot = result.frames[i]
		
		if not snapshot.custom_data.has("success_distance"):
			result.error_state = "MISSING_SPATIAL_DATA_FOR_METRICS"
			return
			
		var distance: float = float(snapshot.custom_data["success_distance"])
		
		if is_nan(distance) or is_inf(distance):
			result.error_state = "INVALID_SPATIAL_DATA_FOR_METRICS"
			return

		if distance < close_threshold:
			current_streak += 1
		else:
			if current_streak >= MIN_CLOSE_CALL_FRAMES:
				close_calls_count += 1
			current_streak = 0

	# Cerrar racha final si la simulación terminó en proximidad
	if current_streak >= MIN_CLOSE_CALL_FRAMES:
		close_calls_count += 1

	# 5. Inyectar resultado con firma de Provenance
	result.metadata["close_calls"] = close_calls_count
	result.metadata["close_calls_source"] = "DERIVED"