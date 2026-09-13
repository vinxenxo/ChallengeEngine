# res://core/authoring/ChallengeAuthoringPolicy.gd
class_name ChallengeAuthoringPolicy
extends RefCounted

## C6-F0.1.6 — Authoring -> Canonical V2 policy.
## This is authoring-contract metadata, not simulation/runtime state.

const CANONICAL_SCHEMA_VERSION: String = "2.0"
const AUTHORING_VERSION: String = "1.0.0"
const ENGINE_VERSION: String = "0.1"
const DEFAULT_MECHANIC_VERSION: String = "1.0"
const DEFAULT_PRESENTATION_PROFILE_VERSION: String = "1.0"
const DEFAULT_COORDINATE_SPACE: String = "CANVAS_1080X1920"
const DEFAULT_SECONDARY_BINDING: String = "target_position"

static func build_presentation_binding() -> Dictionary:
	return {
		"coordinate_space": DEFAULT_COORDINATE_SPACE,
		"secondary_binding": DEFAULT_SECONDARY_BINDING,
		"profile_version": DEFAULT_PRESENTATION_PROFILE_VERSION
	}
