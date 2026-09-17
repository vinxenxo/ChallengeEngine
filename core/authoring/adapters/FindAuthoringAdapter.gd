# res://core/authoring/adapters/FindAuthoringAdapter.gd
class_name FindAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String:
	return "find_v1"

func mechanic_version() -> Dictionary:
	return declared("1.0")

func rng_version() -> Dictionary:
	return declared("2.0")

func default_video_profile() -> Dictionary:
	return declared("f4_legacy_60_h3_g7_r0_c0")

func default_presentation_profile() -> Dictionary:
	return declared("social_default_v1")

func required_assets() -> Dictionary:
	return declared("fam_find_01")

func default_audio_profile() -> Dictionary:
	return declared("c7_test_profile")

func build_structural_parameters(
	_request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	var find_parameters := effective_parameters.duplicate(true)
	find_parameters["safe_area_x_min"] = 150.0
	find_parameters["safe_area_x_max"] = 930.0
	find_parameters["safe_area_y_min"] = 250.0
	find_parameters["safe_area_y_max"] = 1670.0
	find_parameters["scanner_cx"] = 540.0
	find_parameters["scanner_cy"] = 960.0
	find_parameters["scanner_ax"] = 320.0
	find_parameters["scanner_ay"] = 680.0
	find_parameters["scanner_wx"] = 0.013
	find_parameters["scanner_wy"] = 0.017
	find_parameters["target_drift_frequency"] = 0.005
	find_parameters["distractor_count"] = 3
	find_parameters["capture_radius"] = 85.0
	find_parameters["target_drift_radius"] = 50.0
	find_parameters["target_origin"] = [540.0, 960.0]
	return derived({"find": find_parameters})

func validate_authoring_output(challenge: Dictionary) -> Array:
	var errors: Array = []
	var params: Dictionary = challenge.get("simulation", {}).get("parameters", {})
	var find_parameters: Dictionary = params.get("find", {})
	for key in [
		"safe_area_x_min", "safe_area_x_max", "safe_area_y_min", "safe_area_y_max",
		"scanner_cx", "scanner_cy", "scanner_ax", "scanner_ay",
		"scanner_wx", "scanner_wy", "target_drift_frequency",
		"distractor_count", "capture_radius", "target_drift_radius"
	]:
		if not find_parameters.has(key):
			errors.append("find_v1 requires find.%s structural parameter." % key)
	return errors
