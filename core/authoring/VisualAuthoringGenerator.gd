class_name VisualAuthoringGenerator
extends RefCounted

## C10-A — Product intent -> canonical Content Envelope V2.
## This layer never creates or consumes RNG streams.

const RequestValidator = preload("res://core/authoring/VisualAuthoringRequestValidator.gd")
const Resolver = preload("res://core/authoring/VisualDifficultyResolver.gd")
const AssemblyContext = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Registry = preload("res://core/authoring/VisualAuthoringRegistry.gd")
const LoopAdapter = preload("res://core/authoring/adapters/VisualLoopAuthoringAdapter.gd")
const DrillAdapter = preload("res://core/authoring/adapters/VisualDrillAuthoringAdapter.gd")

static func generate(request: VisualAuthoringRequest, context: AssemblyContext, policy: Dictionary) -> Dictionary:
    var errors := RequestValidator.validate(request)
    if not errors.is_empty():
        return {"success": false, "stage": "request_validation", "errors": errors, "content": {}}

    if context == null:
        return {"success": false, "stage": "assembly_context", "errors": ["Assembly context is null."], "content": {}}

    if not Registry.supports(request.domain_family, request.subtype):
        return {"success": false, "stage": "route_resolution", "errors": ["Unsupported visual route."], "content": {}}

    var resolution := Resolver.resolve(request.difficulty_tier, policy, request.custom_parameters)
    if not bool(resolution.get("success", false)):
        return {"success": false, "stage": "difficulty_resolution", "errors": [str(resolution.get("error", "unknown"))], "content": {}}

    var payload: Dictionary
    if request.domain_family == "visual_loop":
        payload = LoopAdapter.build_payload(request, resolution.get("effective_parameters", {}))
    else:
        payload = DrillAdapter.build_payload(request, resolution.get("effective_parameters", {}))

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
        "payload": payload
    }

    return {
        "success": true,
        "stage": "assembly",
        "errors": [],
        "content": envelope,
        "effective_parameters": resolution.get("effective_parameters", {}).duplicate(true)
    }
