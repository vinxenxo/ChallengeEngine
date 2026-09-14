# res://core/authoring/adapters/ParkingV2AuthoringAdapter.gd
class_name ParkingV2AuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String:
	return "parking_v2"

func mechanic_version() -> Dictionary:
	return declared("2.0")

func rng_version() -> Dictionary:
	return declared("2.0")

func default_video_profile() -> Dictionary:
	return declared("parking_v2_social_15s")

func default_presentation_profile() -> Dictionary:
	return declared("social_default_v1")

func required_assets() -> Dictionary:
	return declared("fam_garage_01")

func build_structural_parameters(
	_request: ChallengeAuthoringRequest,
	effective_parameters: Dictionary
) -> Dictionary:
	return derived(effective_parameters.duplicate(true))

func validate_authoring_output(_challenge: Dictionary) -> Array:
	return []
