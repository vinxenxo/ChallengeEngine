# res://tests/C6EPresentationProfileIsolationTest.gd
extends SceneTree

func _initialize() -> void:
	var failures: Array[String] = []

	# ---------------------------------------------------------
	# SIMULATION TRUTH FIJA
	# ---------------------------------------------------------

	var result := SimulationResult.new()

	for i in range(3):
		var snapshot := FrameSnapshot.new()
		snapshot.position = Vector2(float(i), float(i * 2))
		snapshot.variant_id = i
		result.frames.append(snapshot)

	result.winning_frame = 1
	result.score = 0.75
	result.minimum_distance = 2.5
	result.metadata = {
		"seed_used": 12345,
		"attempts": 1
	}

	var baseline := _simulation_signature(result)

	var winning_frame_game := result.winning_frame

	# ---------------------------------------------------------
	# PROFILE A
	# ---------------------------------------------------------

	var cfg_a: Dictionary = {
		"asset_family": "fam_a",
		"presentation": {
			"profile": "profile_a",
			"profile_overrides": {
				"typography": {
					"scale": 1.0
				},
				"safe_area": {
					"left": 40.0,
					"right": 40.0,
					"top": 80.0,
					"bottom": 120.0
				},
				"composition": {
					"gameplay": "center"
				}
			}
		}
	}

	# ---------------------------------------------------------
	# PROFILE B
	# ---------------------------------------------------------

	var cfg_b: Dictionary = {
		"asset_family": "fam_a",
		"presentation": {
			"profile": "profile_b",
			"profile_overrides": {
				"typography": {
					"scale": 1.35
				},
				"safe_area": {
					"left": 80.0,
					"right": 80.0,
					"top": 160.0,
					"bottom": 200.0
				},
				"composition": {
					"gameplay": "lower_center"
				}
			}
		}
	}

	# ---------------------------------------------------------
	# PRESENTATION ONLY
	# ---------------------------------------------------------

	var profile_a := PresentationProfile.from_challenge(cfg_a)
	var profile_b := PresentationProfile.from_challenge(cfg_b)

	var validation_a := profile_a.validate()
	var validation_b := profile_b.validate()

	if not bool(validation_a.get("is_valid", false)):
		failures.append(
			"Profile A invalid: " + str(validation_a.get("errors", []))
		)

	if not bool(validation_b.get("is_valid", false)):
		failures.append(
			"Profile B invalid: " + str(validation_b.get("errors", []))
		)

	var model_a := profile_a.build_render_model(
		"GAME",
		{"text": "A"}
	)

	var model_b := profile_b.build_render_model(
		"GAME",
		{"text": "A"}
	)

	# ---------------------------------------------------------
	# PROFILE DIFFERENCE
	# ---------------------------------------------------------

	if _presentation_signature(model_a) == _presentation_signature(model_b):
		failures.append(
			"Profiles A and B resolved to the same presentation model."
		)

	# ---------------------------------------------------------
	# SIMULATION IMMUTABILITY
	# ---------------------------------------------------------

	if _simulation_signature(result) != baseline:
		failures.append(
			"SimulationResult changed while building presentation profiles."
		)

	if result.winning_frame != 1:
		failures.append(
			"winning_frame changed under presentation profiles."
		)

	if winning_frame_game != 1:
		failures.append(
			"winning_frame_game changed under presentation profiles."
		)

	if result.frames.size() != 3:
		failures.append(
			"Simulation frame count changed unexpectedly."
		)

	if failures.is_empty():
		print(
			"[C6E_PRESENTATION_PROFILE_ISOLATION_SUITE] PASS"
		)
		quit(0)
	else:
		for failure in failures:
			push_error(failure)

		print(
			"[C6E_PRESENTATION_PROFILE_ISOLATION_SUITE] FAIL count=%d"
			% failures.size()
		)

		quit(1)


func _presentation_signature(model: Dictionary) -> String:
	return str([
		model.get("profile_id", ""),
		model.get("source_canvas_size", Vector2()),
		model.get("master_output_size", Vector2()),
		model.get("safe_area", Rect2()),
		model.get("typography", {}),
		model.get("composition", {}),
		model.get("asset_family", ""),
		model.get("theme_name", ""),
		model.get("phase", "")
	])


func _simulation_signature(result: SimulationResult) -> String:
	var parts: Array[String] = [
		str(result.winning_frame),
		str(result.score),
		str(result.minimum_distance),
		JSON.stringify(result.metadata)
	]

	for frame in result.frames:
		parts.append(str(frame.position))
		parts.append(str(frame.rotation))
		parts.append(str(frame.scale))
		parts.append(str(frame.opacity))
		parts.append(str(frame.texture_index))
		parts.append(str(frame.variant_id))
		parts.append(
			JSON.stringify(frame.custom_data)
		)

	return "|".join(parts)