# res://core/authoring/adapters/CatchAuthoringAdapter.gd
class_name CatchAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String:
	return "catch_v1"

func mechanic_version() -> Dictionary:
	return declared("1.0")

func rng_version() -> Dictionary:
	return declared("2.0")

func default_video_profile() -> Dictionary:
	return declared("f4_legacy_60_h0_g7_r0_c2")

func default_presentation_profile() -> Dictionary:
	return declared("social_default_v1")

func required_assets() -> Dictionary:
	return declared("fam_catch_01")

func default_audio_profile() -> Dictionary:
	return declared("c7_profile_mixed_alt")

func build_structural_parameters(
	_request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	var parameters := effective_parameters.duplicate(true)
	parameters["catcher_origin"] = [540.0, 1700.0]
	parameters["catcher_direction"] = [0.0, -1.0]
	parameters["target_origin"] = [540.0, 400.0]
	parameters["target_direction"] = [0.0, 1.0]
	return derived(parameters)

func validate_authoring_output(challenge: Dictionary) -> Array:
	var errors: Array = []
	var params: Dictionary = challenge.get("simulation", {}).get("parameters", {})
	for key in ["catcher_origin", "catcher_direction", "target_origin", "target_direction"]:
		if not params.has(key):
			errors.append("catch_v1 requires %s structural parameter." % key)
	if params.has("catcher_origin") and params["catcher_origin"] != [540.0, 1700.0]:
		errors.append("catch_v1 catcher_origin must match CHALLENGE_006 oracle contract.")
	if params.has("catcher_direction") and params["catcher_direction"] != [0.0, -1.0]:
		errors.append("catch_v1 catcher_direction must match CHALLENGE_006 oracle contract.")
	if params.has("target_origin") and params["target_origin"] != [540.0, 400.0]:
		errors.append("catch_v1 target_origin must match CHALLENGE_006 oracle contract.")
	if params.has("target_direction") and params["target_direction"] != [0.0, 1.0]:
		errors.append("catch_v1 target_direction must match CHALLENGE_006 oracle contract.")
	return errors
