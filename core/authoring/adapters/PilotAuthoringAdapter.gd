# res://core/authoring/adapters/PilotAuthoringAdapter.gd
class_name PilotAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String:
	return "pilot"

func rng_version() -> Dictionary:
	return declared("2.0")

func default_video_profile() -> Dictionary:
	return declared("test_master_11s")

func default_presentation_profile() -> Dictionary:
	return declared("social_default_v1")

func required_assets() -> Dictionary:
	return declared("fam_001")

func build_structural_parameters(
	_request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	return derived(effective_parameters.duplicate(true))

func validate_authoring_output(_challenge: Dictionary) -> Array:
	return []