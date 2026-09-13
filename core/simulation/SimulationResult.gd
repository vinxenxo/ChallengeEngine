# res://core/simulation/SimulationResult.gd
class_name SimulationResult
extends RefCounted

var frames: Array[FrameSnapshot] = []
var winning_frame: int = -1
var score: float = 0.0
var minimum_distance: float = INF
var tolerance_threshold: float = 0.0
var metadata: Dictionary = {}

# C4-A: Contrato de estado explícito
var error_state: String = "OK"

# C4-A: Promesa semántica del modelo de scoring (True = Modelo A / False = Modelo B)
var is_self_scored: bool = false

## Evalúa si la simulación cumplió con el contrato estricto del pipeline.
## Ejecuta validación en 4 capas concéntricas (C4-B).
func validate_contract(expected_game_frames: int) -> Dictionary:
	
	# =========================================================
	# CAPA 1: ERROR STATE (Prioridad Absoluta)
	# =========================================================
	var current_error: String = error_state
	
	# Puente de retrocompatibilidad temporal para mecánicas que inyectan el error en metadata
	if current_error == "OK" and metadata.has("error") and str(metadata["error"]) != "OK":
		current_error = str(metadata["error"])
		
	if current_error != "OK":
		return {
			"is_valid": false,
			"error_code": current_error,
			"message": "Simulation aborted internally with error state: %s" % current_error
		}

	# =========================================================
	# CAPA 2: ESTRUCTURA TEMPORAL
	# =========================================================
	if frames.size() != expected_game_frames:
		return {
			"is_valid": false,
			"error_code": "SIMULATION_FRAME_COUNT_MISMATCH",
			"message": "Expected %d frames, but mechanic generated %d." % [expected_game_frames, frames.size()]
		}

	for i in range(frames.size()):
		var snapshot: FrameSnapshot = frames[i]
		if snapshot == null or not snapshot.is_valid_snapshot():
			return {
				"is_valid": false,
				"error_code": "CORRUPTED_FRAME_SNAPSHOT",
				"message": "Snapshot at frame index %d is null or contains invalid transform values (NaN/INF)." % i
			}

	# =========================================================
	# CAPA 3: ÍNDICES / MÉTRICAS
	# =========================================================
	if winning_frame < -1 or winning_frame >= frames.size():
		return {
			"is_valid": false,
			"error_code": "INVALID_WINNING_FRAME_BOUNDS",
			"message": "Winning frame %d is strictly out of bounds [-1, %d]." % [winning_frame, frames.size() - 1]
		}

	if is_nan(score) or score < 0.0 or score > 1.0:
		return {
			"is_valid": false,
			"error_code": "INVALID_SCORE_VALUE",
			"message": "Score %f is invalid. Must be in [0.0, 1.0]." % score
		}

	if is_nan(minimum_distance):
		return {
			"is_valid": false,
			"error_code": "INVALID_MINIMUM_DISTANCE",
			"message": "Minimum distance cannot be NaN."
		}

	# Promesa estricta de is_self_scored: Si afirma estar autoevaluada, la métrica no puede ser INF.
	if is_self_scored and is_inf(minimum_distance):
		return {
			"is_valid": false,
			"error_code": "UNRESOLVED_METRICS_IN_SELF_SCORED",
			"message": "Mechanic is marked as self-scored but minimum_distance is still INF."
		}

	# =========================================================
	# CAPA 4: METADATA Y COHERENCIA MÍNIMA
	# =========================================================
	if is_nan(tolerance_threshold) or tolerance_threshold < 0.0 or is_inf(tolerance_threshold):
		return {
			"is_valid": false,
			"error_code": "INVALID_TOLERANCE_THRESHOLD",
			"message": "Tolerance threshold %f is invalid." % tolerance_threshold
		}

	return {"is_valid": true, "error_code": "OK", "message": "Contract validated successfully."}