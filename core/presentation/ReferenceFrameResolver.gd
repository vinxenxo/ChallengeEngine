class_name ReferenceFrameResolver
extends RefCounted

enum ReferenceMode {
	NONE,
	WINNING_FRAME,
	FINAL_FRAME
}

static func resolve(result: SimulationResult) -> Dictionary:
	if result == null:
		return {
			"is_valid": false,
			"frame_index": -1,
			"mode": ReferenceMode.NONE,
			"mode_name": "NONE",
			"reason": "SimulationResult is null"
		}

	var frames_count: int = result.frames.size()

	if frames_count == 0:
		return {
			"is_valid": false,
			"frame_index": -1,
			"mode": ReferenceMode.NONE,
			"mode_name": "NONE",
			"reason": "SimulationResult contains no frames"
		}

	if (
		result.winning_frame >= 0
		and result.winning_frame < frames_count
	):
		return {
			"is_valid": true,
			"frame_index": result.winning_frame,
			"mode": ReferenceMode.WINNING_FRAME,
			"mode_name": "WINNING_FRAME",
			"reason": "Certified winning_frame"
		}

	return {
		"is_valid": true,
		"frame_index": frames_count - 1,
		"mode": ReferenceMode.FINAL_FRAME,
		"mode_name": "FINAL_FRAME",
		"reason": "No certified winning_frame; using final simulation frame"
	}