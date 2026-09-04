class_name PilotAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String: return "pilot"
func rng_version() -> Dictionary: return declared("2.0")
func default_video_profile() -> Dictionary: return unavailable("No contractual default video profile defined for pilot.")
func default_presentation_profile() -> Dictionary: return unavailable("No contractual default presentation profile defined for pilot.")
func required_assets() -> Dictionary: return unavailable("No contractual asset family defined for pilot.")

func build_structural_parameters(_request: ChallengeAuthoringRequest, effective_parameters: Dictionary) -> Dictionary:
	return derived(effective_parameters.duplicate(true))

func validate_authoring_output(_challenge: Dictionary) -> Array:
	return []