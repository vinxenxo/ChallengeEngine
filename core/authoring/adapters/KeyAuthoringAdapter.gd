# res://core/authoring/adapters/KeyAuthoringAdapter.gd
class_name KeyAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String:
	return "key"

func mechanic_version() -> Dictionary:
	return declared("1.0")

func rng_version() -> Dictionary:
	return declared("1.0")

func default_video_profile() -> Dictionary:
	return declared("f4_legacy_60_h0_g7_r0_c2")

func default_presentation_profile() -> Dictionary:
	return declared("social_default_v1")

func required_assets() -> Dictionary:
	return declared("fam_key_01")

func default_audio_profile() -> Dictionary:
	return declared("c7_profile_tone_only")

func build_structural_parameters(
	_request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	return derived(effective_parameters.duplicate(true))

func validate_authoring_output(challenge: Dictionary) -> Array:
	var errors: Array = []
	var params: Dictionary = challenge.get("simulation", {}).get("parameters", {})
	var tolerance: Dictionary = params.get("tolerance", {})
	if not tolerance.has("rotation_deg"):
		errors.append("key requires tolerance.rotation_deg.")
	return errors
