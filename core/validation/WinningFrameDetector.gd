class_name WinningFrameDetector
extends RefCounted

static func analyze_and_score(result: SimulationResult) -> void:
	var best_frame: int = -1
	var max_score: float = -INF
	var min_dist: float = INF

	for i: int in range(result.frames.size()):
		var snapshot: FrameSnapshot = result.frames[i]
		var distance: float = float(snapshot.custom_data.get("success_distance", INF))

		if distance < min_dist:
			min_dist = distance

		var distance_score: float = 1.0 / (1.0 + distance)
		var velocity: float = float(snapshot.custom_data.get("velocity", 0.0))
		var velocity_score: float = 1.0 / (1.0 + velocity)
		var frame_score: float = (distance_score * 0.60) + (velocity_score * 0.40)

		if distance <= result.tolerance_threshold and frame_score > max_score:
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
