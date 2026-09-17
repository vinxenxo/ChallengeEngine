# res://core/authoring/adapters/PilotAuthoringAdapter.gd
class_name PilotAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String:
	return "pilot"

func mechanic_version() -> Dictionary:
	return declared("2.0")

func rng_version() -> Dictionary:
	return declared("2.0")

func default_video_profile() -> Dictionary:
	return declared("f4_legacy_60_h3_g7_r0_c2")

func default_presentation_profile() -> Dictionary:
	return declared("social_default_v1")

func required_assets() -> Dictionary:
	return declared("fam_pilot_01")

func default_audio_profile() -> Dictionary:
	return declared("c7_profile_mixed_alt")

func build_structural_parameters(
	_request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	var parameters := effective_parameters.duplicate(true)
	parameters["start_x"] = 0.0
	parameters["end_x"] = 100.0
	parameters["target_start"] = 0.0
	parameters["trajectory_amplitude"] = 2.0
	parameters["control_amplitude"] = 0.5
	return derived(parameters)

func validate_authoring_output(challenge: Dictionary) -> Array:
	var errors: Array = []
	var params: Dictionary = challenge.get("simulation", {}).get("parameters", {})
	for key in ["start_x", "end_x", "target_start", "target_velocity", "trajectory_amplitude", "control_amplitude"]:
		if not params.has(key):
			errors.append("pilot requires %s structural parameter." % key)
	if float(params.get("start_x", -1.0)) != 0.0 or float(params.get("end_x", -1.0)) != 100.0:
		errors.append("pilot start_x/end_x must match CHALLENGE_003 oracle contract.")
	if float(params.get("target_start", -1.0)) != 0.0:
		errors.append("pilot target_start must match CHALLENGE_003 oracle contract.")
	if float(params.get("trajectory_amplitude", -1.0)) != 2.0:
		errors.append("pilot trajectory_amplitude must match CHALLENGE_003 oracle contract.")
	if float(params.get("control_amplitude", -1.0)) != 0.5:
		errors.append("pilot control_amplitude must match CHALLENGE_003 oracle contract.")
	return errors
