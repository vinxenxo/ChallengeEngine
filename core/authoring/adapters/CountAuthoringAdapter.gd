# res://core/authoring/adapters/CountAuthoringAdapter.gd
class_name CountAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String:
	return "count_v1"

func mechanic_version() -> Dictionary:
	return declared("1.0")

func rng_version() -> Dictionary:
	return declared("2.0")

func default_video_profile() -> Dictionary:
	return declared("f4_legacy_60_h3_g7_r0_c2")

func default_presentation_profile() -> Dictionary:
	return declared("social_default_v1")

func required_assets() -> Dictionary:
	return declared("fam_count_01")

func default_audio_profile() -> Dictionary:
	return declared("c7_test_profile")

func build_structural_parameters(
	_request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	var count_parameters := effective_parameters.duplicate(true)
	count_parameters["min_value"] = 3
	count_parameters["max_value"] = 10
	count_parameters["start_pos"] = [180.0, 850.0]
	count_parameters["step_x"] = 100.0
	return derived({"count": count_parameters})

func validate_authoring_output(challenge: Dictionary) -> Array:
	var errors: Array = []
	var count_parameters: Dictionary = challenge.get("simulation", {}).get("parameters", {}).get("count", {})
	if not count_parameters.has("min_value") or not count_parameters.has("max_value"):
		errors.append("count_v1 requires count.min_value/max_value.")
	if count_parameters.get("start_pos") != [180.0, 850.0]:
		errors.append("count_v1 start_pos must match CHALLENGE_009 oracle contract.")
	if float(count_parameters.get("step_x", -1.0)) != 100.0:
		errors.append("count_v1 step_x must match CHALLENGE_009 oracle contract.")
	return errors
