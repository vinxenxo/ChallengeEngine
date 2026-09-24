class_name VisualAuthoringGenerator
extends RefCounted

## C10-A.1 — Product intent -> canonical Content Envelope V2.
## No RNG stream access. No runtime/generator/rendering access.
## Production subtype policies are loaded from the dedicated authoring registry.

const RequestValidator = preload("res://core/authoring/VisualAuthoringRequestValidator.gd")
const Resolver = preload("res://core/authoring/VisualDifficultyResolver.gd")
const AssemblyContext = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Registry = preload("res://core/authoring/VisualAuthoringRegistry.gd")
const PolicyRegistry = preload("res://core/authoring/VisualAuthoringPolicyRegistry.gd")
const LoopAdapter = preload("res://core/authoring/adapters/VisualLoopAuthoringAdapter.gd")
const DrillAdapter = preload("res://core/authoring/adapters/VisualDrillAuthoringAdapter.gd")
const DrillSeedVariation = preload("res://core/authoring/VisualDrillSeedVariation.gd")

static func generate(request: VisualAuthoringRequest, context: AssemblyContext, supplied_policy: Dictionary = {}) -> Dictionary:
    var errors := RequestValidator.validate(request)
    if not errors.is_empty():
        return {"success": false, "stage": "request_validation", "errors": errors, "content": {}}

    var context_errors := _validate_context(context)
    if not context_errors.is_empty():
        return {"success": false, "stage": "assembly_context", "errors": context_errors, "content": {}}

    if not Registry.supports(request.domain_family, request.subtype):
        return {"success": false, "stage": "route_resolution", "errors": ["Unsupported visual route."], "content": {}}

    var policy := supplied_policy.duplicate(true)
    if policy.is_empty():
        policy = PolicyRegistry.get_policy(request.domain_family, request.subtype)

    if policy.is_empty():
        return {
            "success": false,
            "stage": "policy_resolution",
            "errors": ["No production authoring policy for %s/%s." % [request.domain_family, request.subtype]],
            "content": {}
        }

    var resolution := Resolver.resolve(request.difficulty_tier, policy, request.custom_parameters)
    if not bool(resolution.get("success", false)):
        return {"success": false, "stage": "difficulty_resolution", "errors": [str(resolution.get("error", "unknown"))], "content": {}}

    var resolved: Dictionary = resolution.get("effective_parameters", {}).duplicate(true)
    var payload_result: Dictionary

    if request.domain_family == "visual_loop":
        payload_result = LoopAdapter.build_payload(request, resolved)
    else:
        payload_result = DrillAdapter.build_payload(request, resolved)

    if not bool(payload_result.get("success", false)):
        return {
            "success": false,
            "stage": "adapter",
            "errors": payload_result.get("errors", []),
            "content": {}
        }

    if request.domain_family == "visual_drill":
        var authored_payload: Dictionary = payload_result.get("payload", {})
        payload_result["payload"] = DrillSeedVariation.apply(
            request.subtype,
            context.seed,
            authored_payload
        )

    var envelope := {
        "schema_version": "2.0",
        "content_id": context.content_id,
        "content_version": context.content_version,
        "kind": request.domain_family,
        "subtype": request.subtype,
        "engine_version": context.engine_version,
        "authoring_version": request.authoring_version,
        "rng_version": context.rng_version,
        "seed": context.seed,
        "presentation": context.presentation.duplicate(true),
        "assets": context.assets.duplicate(true),
        "audio": context.audio.duplicate(true),
        "provenance": context.provenance.duplicate(true),
        "payload": payload_result["payload"].duplicate(true)
    }

    return {
        "success": true,
        "stage": "assembly",
        "errors": [],
        "content": envelope,
        "effective_parameters": resolved
    }

static func _validate_context(context: AssemblyContext) -> Array[String]:
    var errors: Array[String] = []
    if context == null:
        return ["Assembly context is null."]

    if context.rng_version.strip_edges().is_empty():
        errors.append("rng_version is required.")
    if context.content_id.strip_edges().is_empty():
        errors.append("content_id is required.")
    if context.content_version.strip_edges().is_empty():
        errors.append("content_version is required.")
    if context.engine_version.strip_edges().is_empty():
        errors.append("engine_version is required.")

    var presentation := context.presentation
    if not presentation.has("profile_id") or str(presentation.get("profile_id", "")).strip_edges().is_empty():
        errors.append("presentation.profile_id is required.")
    if not presentation.has("coordinate_space") or str(presentation.get("coordinate_space", "")).strip_edges().is_empty():
        errors.append("presentation.coordinate_space is required.")

    var assets := context.assets
    if not assets.has("family_id") or str(assets.get("family_id", "")).strip_edges().is_empty():
        errors.append("assets.family_id is required.")

    var audio := context.audio
    if not audio.has("profile_id") or str(audio.get("profile_id", "")).strip_edges().is_empty():
        errors.append("audio.profile_id is required.")
    if not audio.has("enabled") or typeof(audio.get("enabled")) != TYPE_BOOL:
        errors.append("audio.enabled is required and must be boolean.")

    var provenance := context.provenance
    if not provenance.has("author") or str(provenance.get("author", "")).strip_edges().is_empty():
        errors.append("provenance.author is required.")
    if not provenance.has("timestamp_ms") or typeof(provenance.get("timestamp_ms")) != TYPE_INT or int(provenance.get("timestamp_ms", -1)) < 0:
        errors.append("provenance.timestamp_ms is required and must be a non-negative integer.")

    return errors
