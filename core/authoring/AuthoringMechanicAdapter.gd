# res://core/authoring/AuthoringMechanicAdapter.gd
class_name AuthoringMechanicAdapter
extends RefCounted

enum Source { DECLARED, DERIVED, UNAVAILABLE }

func declared(val: Variant) -> Dictionary:
	return {
		"source": Source.DECLARED,
		"value": val,
		"error": ""
	}

func derived(val: Variant) -> Dictionary:
	return {
		"source": Source.DERIVED,
		"value": val,
		"error": ""
	}

func unavailable(err: String) -> Dictionary:
	return {
		"source": Source.UNAVAILABLE,
		"value": null,
		"error": err
	}

func mechanic_id() -> String:
	return ""

func rng_version() -> Dictionary:
	return unavailable("rng_version not implemented")

func default_video_profile() -> Dictionary:
	return unavailable("default_video_profile not implemented")

func default_presentation_profile() -> Dictionary:
	return unavailable("default_presentation_profile not implemented")

func required_assets() -> Dictionary:
	return unavailable("required_assets not implemented")

func build_structural_parameters(
	request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	return unavailable("build_structural_parameters not implemented")

func validate_authoring_output(challenge: Dictionary) -> Array:
	return ["validate_authoring_output not implemented"]