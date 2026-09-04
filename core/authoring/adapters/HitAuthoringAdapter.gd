class_name HitAuthoringAdapter
extends AuthoringMechanicAdapter

func mechanic_id() -> String: return "hit_v1"
func rng_version() -> Dictionary: return declared("2.0")
func default_video_profile() -> Dictionary: return unavailable("No contractual default video profile defined for hit_v1.")
func default_presentation_profile() -> Dictionary: return unavailable("No contractual default presentation profile defined for hit_v1.")
func required_assets() -> Dictionary: return unavailable("No contractual asset family defined for hit_v1.")

func build_structural_parameters(_request: ChallengeAuthoringRequest, effective_parameters: Dictionary) -> Dictionary:
	return derived(effective_parameters.duplicate(true))

func validate_authoring_output(_challenge: Dictionary) -> Array:
	return []