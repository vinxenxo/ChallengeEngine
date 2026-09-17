class_name VisualAuthoringRequestValidator
extends RefCounted

## C10-A — Strict fail-closed request validation.

const ALLOWED_DOMAINS := ["visual_loop", "visual_drill"]
const LOOP_SUBTYPES := ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]
const DRILL_SUBTYPES := ["tracking", "pursuit", "saccade", "peripheral_scan"]

static func validate(request: VisualAuthoringRequest) -> Array[String]:
    var errors: Array[String] = []

    if request == null:
        errors.append("Request is null.")
        return errors

    if request.authoring_version.strip_edges().is_empty():
        errors.append("authoring_version is required.")

    if not ALLOWED_DOMAINS.has(request.domain_family):
        errors.append("Unsupported domain_family '%s'." % request.domain_family)

    if request.domain_family == "visual_loop" and not LOOP_SUBTYPES.has(request.subtype):
        errors.append("Unsupported visual_loop subtype '%s'." % request.subtype)

    if request.domain_family == "visual_drill" and not DRILL_SUBTYPES.has(request.subtype):
        errors.append("Unsupported visual_drill subtype '%s'." % request.subtype)

    if not is_finite(request.duration_seconds) or request.duration_seconds < 0.1:
        errors.append("duration_seconds must be finite and >= 0.1.")

    if request.fps != 30 and request.fps != 60:
        errors.append("fps must be exactly 30 or 60.")

    if request.difficulty_tier < 1 or request.difficulty_tier > 5:
        errors.append("difficulty_tier must be an integer in range 1..5.")

    if request.custom_parameters == null:
        errors.append("custom_parameters must be a Dictionary.")

    return errors
