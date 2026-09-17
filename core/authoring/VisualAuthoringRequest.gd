class_name VisualAuthoringRequest
extends RefCounted

## C10-A — Product-level visual authoring intent.
## Contains no RNG seed, presentation binding, asset identity, or runtime state.

var authoring_version: String
var domain_family: String
var subtype: String
var duration_seconds: float
var fps: int
var difficulty_tier: int
var custom_parameters: Dictionary

func _init(
    p_domain_family: String,
    p_subtype: String,
    p_duration_seconds: float,
    p_fps: int,
    p_difficulty_tier: int,
    p_custom_parameters: Dictionary = {},
    p_authoring_version: String = "1.0"
) -> void:
    authoring_version = p_authoring_version
    domain_family = p_domain_family
    subtype = p_subtype
    duration_seconds = p_duration_seconds
    fps = p_fps
    difficulty_tier = p_difficulty_tier
    custom_parameters = p_custom_parameters.duplicate(true)

func to_dictionary() -> Dictionary:
    return {
        "authoring_version": authoring_version,
        "domain_family": domain_family,
        "subtype": subtype,
        "duration_seconds": duration_seconds,
        "fps": fps,
        "difficulty_tier": difficulty_tier,
        "custom_parameters": custom_parameters.duplicate(true)
    }
