# res://core/validation/WinningFrameDetector.gd
class_name WinningFrameDetector
extends RefCounted

static func analyze_and_score(result: SimulationResult) -> void:
	# 1. Una simulación fallida no se puntúa.
	if result.error_state != "OK":
		return

	# 2. Una mecánica self-scored tiene autoridad absoluta sobre sus métricas.
	if result.is_self_scored:
		return

	# 3. Nada que puntuar.
	if result.frames.is_empty():
		return

	var best_frame: int = -1
	var max_score: float = -INF
	var min_dist: float = INF

	for i: int in range(result.frames.size()):
		var snapshot: FrameSnapshot = result.frames[i]

		if not snapshot.custom_data.has("success_distance"):
			result.error_state = "MISSING_SCORING_METRICS"
			return

		var distance: float = float(
			snapshot.custom_data["success_distance"]
		)

		if is_nan(distance) or is_inf(distance):
			result.error_state = "INVALID_SCORING_DISTANCE"
			return

		if distance < min_dist:
			min_dist = distance

		var distance_score: float = 1.0 / (1.0 + distance)

		var velocity: float = float(
			snapshot.custom_data.get("velocity", 0.0)
		)

		if is_nan(velocity) or is_inf(velocity):
			result.error_state = "INVALID_SCORING_VELOCITY"
			return

		var velocity_score: float = 1.0 / (1.0 + velocity)
		var frame_score: float = (
			distance_score * 0.60
			+ velocity_score * 0.40
		)

		if (
			distance <= result.tolerance_threshold
			and frame_score > max_score
		):
			max_score = frame_score
			best_frame = i

	result.winning_frame = best_frame
	result.score = max_score if best_frame != -1 else 0.0
	result.minimum_distance = min_dist

	print(
		"best_frame=", best_frame,
		" min_dist=", min_dist,
		" tolerance=", result.tolerance_threshold
	)