class_name ChallengeValidator
extends RefCounted

const MIN_CLOSE_CALL_FRAMES: int = 12
const MIN_CLOSE_CALLS: int = 0
const MAX_CLOSE_CALLS: int = 20


static func validate(
	result: SimulationResult,
	hook_frames: int = 0,
	game_frames: int = -1
) -> ValidationResult:

	var validation: ValidationResult = ValidationResult.new()

	validation.minimum_distance = result.minimum_distance
	validation.score = result.score
	validation.winning_frame = result.winning_frame

	# ---------------------------------------------------------
	# 1. SIMULACIÓN
	# ---------------------------------------------------------

	if result.frames.is_empty():
		validation.errors.append("Simulation produced no frames.")
		return validation

	if result.winning_frame < 0 or result.winning_frame >= result.frames.size():
		validation.errors.append("No valid winning frame was detected.")
		return validation

	if not is_finite(result.minimum_distance):
		validation.errors.append("Minimum distance is not finite.")
		return validation

	# ---------------------------------------------------------
	# 2. VENTANA TEMPORAL
	# ---------------------------------------------------------

	validation.absolute_winning_frame = (
		result.winning_frame + hook_frames
	)

	validation.valid_window_start = hook_frames

	if game_frames >= 0:
		validation.valid_window_end_exclusive = hook_frames + game_frames

		validation.winning_frame_in_valid_window = (
			validation.absolute_winning_frame >= validation.valid_window_start
			and
			validation.absolute_winning_frame < validation.valid_window_end_exclusive
		)

		if not validation.winning_frame_in_valid_window:
			validation.errors.append(
				"Winning frame outside GAME window: %d (expected %d <= frame < %d)." %
				[
					validation.absolute_winning_frame,
					validation.valid_window_start,
					validation.valid_window_end_exclusive
				]
			)

	# ---------------------------------------------------------
	# 3. CLOSE CALLS (Soporte nativo para Metadata / Hit o legacy)
	# ---------------------------------------------------------

	var close_calls_count: int = 0

	if result.metadata.has("close_calls"):
		close_calls_count = int(result.metadata["close_calls"])
	else:
		var close_threshold: float = result.tolerance_threshold * 3.5
		var current_streak: int = 0

		for i: int in range(result.frames.size()):
			var distance: float = float(
				result.frames[i].custom_data.get("success_distance", INF)
			)

			if distance < close_threshold:
				current_streak += 1
			else:
				if current_streak >= MIN_CLOSE_CALL_FRAMES:
					close_calls_count += 1
				current_streak = 0

		if current_streak >= MIN_CLOSE_CALL_FRAMES:
			close_calls_count += 1

	validation.close_calls = close_calls_count

	if close_calls_count < MIN_CLOSE_CALLS or close_calls_count > MAX_CLOSE_CALLS:
		validation.errors.append(
			"Close-call count outside accepted range: %d (expected %d-%d)." %
			[
				close_calls_count,
				MIN_CLOSE_CALLS,
				MAX_CLOSE_CALLS
			]
		)
		return validation

	# ---------------------------------------------------------
	# 4. RESULTADO FINAL
	# ---------------------------------------------------------

	validation.is_valid = validation.errors.is_empty()

	print(
		"[VALIDATION] ",
		"relative_winning_frame=", validation.winning_frame,
		" absolute_winning_frame=", validation.absolute_winning_frame,
		" valid_window=",
		validation.valid_window_start,
		"-",
		validation.valid_window_end_exclusive,
		" close_calls=",
		validation.close_calls,
		" valid=",
		validation.is_valid
	)

	return validation


static func is_finite(value: float) -> bool:
	return not is_nan(value) and not is_inf(value)