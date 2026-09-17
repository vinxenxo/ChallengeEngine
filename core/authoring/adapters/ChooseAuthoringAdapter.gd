# res://core/authoring/adapters/ChooseAuthoringAdapter.gd
class_name ChooseAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String:
	return "choose_v1"

func mechanic_version() -> Dictionary:
	return declared("1.0")

func rng_version() -> Dictionary:
	return declared("2.0")

func default_video_profile() -> Dictionary:
	return declared("f4_legacy_60_h3_g7_r0_c2")

func default_presentation_profile() -> Dictionary:
	return declared("social_default_v1")

func required_assets() -> Dictionary:
	return declared("fam_choose_01")

func default_audio_profile() -> Dictionary:
	return declared("c7_test_profile")

func build_structural_parameters(
	_request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	var choose_parameters := effective_parameters.duplicate(true)
	choose_parameters["options_count"] = 3
	choose_parameters["positions"] = [
		[270.0, 960.0],
		[540.0, 960.0],
		[810.0, 960.0]
	]
	return derived({"choose": choose_parameters})

func validate_authoring_output(challenge: Dictionary) -> Array:
	var errors: Array = []
	var choose_parameters: Dictionary = challenge.get("simulation", {}).get("parameters", {}).get("choose", {})
	if not choose_parameters.has("options_count"):
		errors.append("choose_v1 requires choose.options_count.")
	if choose_parameters.get("positions") != [
		[270.0, 960.0],
		[540.0, 960.0],
		[810.0, 960.0]
	]:
		errors.append("choose_v1 positions must match canonical oracle layout.")
	return errors
