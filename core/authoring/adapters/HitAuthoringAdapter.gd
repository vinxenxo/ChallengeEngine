# res://core/authoring/adapters/HitAuthoringAdapter.gd
class_name HitAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String:
	return "hit_v1"

func mechanic_version() -> Dictionary:
	return declared("1.0")

func rng_version() -> Dictionary:
	return declared("2.0")

func default_video_profile() -> Dictionary:
	return declared("f4_legacy_60_h0_g7_r0_c0")

func default_presentation_profile() -> Dictionary:
	return declared("social_default_v1")

func required_assets() -> Dictionary:
	return declared("fam_hit_01")

func default_audio_profile() -> Dictionary:
	return declared("c7_profile_multi_noise")

func build_structural_parameters(
	_request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	var parameters := effective_parameters.duplicate(true)
	parameters["origin"] = [540.0, 1500.0]
	parameters["target"] = [540.0, 300.0]
	return derived(parameters)

func validate_authoring_output(challenge: Dictionary) -> Array:
	var errors: Array = []
	var params: Dictionary = challenge.get("simulation", {}).get("parameters", {})
	if not params.has("origin") or not params.has("target"):
		errors.append("hit_v1 requires origin and target structural parameters.")
	return errors
