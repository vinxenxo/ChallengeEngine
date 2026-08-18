class_name SimulationResult
extends RefCounted

var frames: Array[FrameSnapshot] = []
var winning_frame: int = -1
var score: float = 0.0
var minimum_distance: float = INF
var tolerance_threshold: float = 0.0
var metadata: Dictionary = {}

## Evalúa si la simulación cumplió con el contrato estricto de generación de cuadros
func validate_contract(expected_game_frames: int) -> Dictionary:
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

	return {"is_valid": true, "error_code": "", "message": ""}