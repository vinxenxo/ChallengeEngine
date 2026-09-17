extends SceneTree

## C10-C — Visual Authoring -> Production Runtime E2E integration test.
## Scope: consumes envelopes produced by VisualAuthoringGenerator in memory.
## Does not modify C6-F0.8 runtime, generators, RNG, binders, renderers or Movie Maker.

const Request = preload("res://core/authoring/VisualAuthoringRequest.gd")
const Context = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Generator = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const ContentRuntime = preload("res://core/runtime/ContentRuntime.gd")
const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")
const RenderedFrameStream = preload("res://core/runtime/RenderedFrameStream.gd")

const LOOP_SUBTYPES: Array[String] = [
    "fractal",
    "vector_field",
    "particle_flow",
    "kaleidoscope",
    "geometric"
]
const DRILL_SUBTYPES: Array[String] = [
    "tracking",
    "pursuit",
    "saccade",
    "peripheral_scan"
]
const ALL_ROUTES: Array[Dictionary] = [
    {"domain_family": "visual_loop", "subtype": "fractal"},
    {"domain_family": "visual_loop", "subtype": "vector_field"},
    {"domain_family": "visual_loop", "subtype": "particle_flow"},
    {"domain_family": "visual_loop", "subtype": "kaleidoscope"},
    {"domain_family": "visual_loop", "subtype": "geometric"},
    {"domain_family": "visual_drill", "subtype": "tracking"},
    {"domain_family": "visual_drill", "subtype": "pursuit"},
    {"domain_family": "visual_drill", "subtype": "saccade"},
    {"domain_family": "visual_drill", "subtype": "peripheral_scan"}
]

const SEED: int = 12345
const TIER: int = 2
const DURATION_SECONDS: float = 2.0
const FPS: int = 30
const EXPECTED_FRAME_COUNT: int = 60

var failures: Array[String] = []

func _init() -> void:
    print("[TEST] Running C10CEndToEndTest...")
    _test_authoring_to_runtime_9_of_9()
    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _request(domain_family: String, subtype: String) -> Request:
    return Request.new(
        domain_family,
        subtype,
        DURATION_SECONDS,
        FPS,
        TIER,
        {}
    )

func _context(seed_value: int, content_id: String) -> Context:
    return Context.new(
        seed_value,
        "2.0",
        content_id,
        "1.0.0",
        "4.7.1",
        {"profile_id": "social_default_v1", "coordinate_space": "2d"},
        {"family_id": "fam_001"},
        {"profile_id": "default_procedural_music", "enabled": false},
        {"author": "c10_visual_authoring_e2e", "timestamp_ms": 0}
    )

func _generate(route: Dictionary) -> Dictionary:
    var domain_family: String = str(route["domain_family"])
    var subtype: String = str(route["subtype"])
    var request: Request = _request(domain_family, subtype)
    var content_id: String = "C10C_E2E_%s_%s" % [domain_family.to_upper(), subtype.to_upper()]
    var context: Context = _context(SEED, content_id)
    return Generator.generate(request, context)

func _test_authoring_to_runtime_9_of_9() -> void:
    var registry: ContentRuntimeRegistry = ContentRuntimeRegistry.create_default()
    var passed: int = 0

    for route in ALL_ROUTES:
        var domain_family: String = str(route["domain_family"])
        var subtype: String = str(route["subtype"])
        var authoring_result: Dictionary = _generate(route)

        _assert(
            bool(authoring_result.get("success", false)),
            "Authoring generation failed for %s/%s: %s" % [domain_family, subtype, str(authoring_result.get("errors", []))]
        )
        if not bool(authoring_result.get("success", false)):
            continue

        var envelope: Dictionary = authoring_result.get("content", {})
        _assert(envelope.get("schema_version", "") == "2.0", "Envelope schema_version mismatch for %s/%s" % [domain_family, subtype])
        _assert(envelope.get("kind", "") == domain_family, "Envelope kind mismatch for %s/%s" % [domain_family, subtype])
        _assert(envelope.get("subtype", "") == subtype, "Envelope subtype mismatch for %s/%s" % [domain_family, subtype])
        _assert(int(envelope.get("seed", -1)) == SEED, "Envelope seed mismatch for %s/%s" % [domain_family, subtype])
        _assert(str(envelope.get("rng_version", "")) == "2.0", "Envelope RNG version mismatch for %s/%s" % [domain_family, subtype])
        _assert(int(envelope.get("payload", {}).get("frame_count", -1)) == EXPECTED_FRAME_COUNT, "Envelope frame_count mismatch for %s/%s" % [domain_family, subtype])
        _assert(int(envelope.get("payload", {}).get("fps", -1)) == FPS, "Envelope FPS mismatch for %s/%s" % [domain_family, subtype])

        var resolution: Dictionary = registry.resolve(envelope)
        _assert(
            bool(resolution.get("success", false)),
            "Runtime registry rejected generated envelope for %s/%s: %s" % [domain_family, subtype, str(resolution.get("error_code", ""))]
        )
        if not bool(resolution.get("success", false)):
            continue

        var runtime: ContentRuntime = resolution.get("runtime")
        _assert(runtime != null, "Runtime is null after successful resolution for %s/%s" % [domain_family, subtype])
        if runtime == null:
            continue

        _assert(runtime.is_initialized(), "Runtime is not initialized for %s/%s" % [domain_family, subtype])
        _assert(runtime.get_frame_count() == EXPECTED_FRAME_COUNT, "Runtime frame_count mismatch for %s/%s" % [domain_family, subtype])

        var stream: RenderedFrameStream = runtime.get_rendered_frame_stream()
        _assert(stream != null, "RenderedFrameStream missing for %s/%s" % [domain_family, subtype])
        if stream == null:
            continue

        var validation: Dictionary = stream.validate_contract()
        _assert(
            bool(validation.get("is_valid", false)),
            "RenderedFrameStream contract invalid for %s/%s: %s" % [domain_family, subtype, str(validation.get("errors", []))]
        )
        _assert(stream.kind == domain_family, "Stream kind mismatch for %s/%s" % [domain_family, subtype])
        _assert(stream.subtype == subtype, "Stream subtype mismatch for %s/%s" % [domain_family, subtype])
        _assert(stream.fps == FPS, "Stream FPS mismatch for %s/%s" % [domain_family, subtype])

        var first: Dictionary = runtime.next_frame()
        _assert(not first.is_empty(), "Runtime emitted no first frame for %s/%s" % [domain_family, subtype])
        if first.is_empty():
            continue

        _assert(int(first.get("frame_index", -1)) == 0, "First frame index is not 0 for %s/%s" % [domain_family, subtype])
        var first_payload: Dictionary = first.get("payload", {})
        _assert(first_payload.get("domain", "") == domain_family, "First frame domain mismatch for %s/%s" % [domain_family, subtype])
        _assert(not first_payload.has("phase"), "Visual frame introduced Challenge phase semantics for %s/%s" % [domain_family, subtype])

        var consumed: int = 1
        while not runtime.is_finished():
            var next_frame: Dictionary = runtime.next_frame()
            _assert(not next_frame.is_empty(), "Runtime emitted an empty frame before completion for %s/%s" % [domain_family, subtype])
            if next_frame.is_empty():
                break

            _assert(
                int(next_frame.get("frame_index", -1)) == consumed,
                "Non-sequential frame index for %s/%s: expected %d" % [domain_family, subtype, consumed]
            )
            consumed += 1

        _assert(consumed == EXPECTED_FRAME_COUNT, "Consumed %d/%d frames for %s/%s" % [consumed, EXPECTED_FRAME_COUNT, domain_family, subtype])
        _assert(runtime.next_frame().is_empty(), "Runtime emitted a frame after completion for %s/%s" % [domain_family, subtype])
        passed += 1

    print("[C10C] Authoring -> Runtime -> RenderedFrameStream: %d/9" % passed)
    _assert(passed == 9, "C10-C runtime E2E must pass 9/9")

func _conclude() -> void:
    if failures.is_empty():
        print("[C10C_VISUAL_AUTHORING_RUNTIME_E2E_SUITE] PASS — 9/9")
        quit(0)
        return

    for failure in failures:
        push_error(failure)
    print("[C10C_VISUAL_AUTHORING_RUNTIME_E2E_SUITE] FAIL failures=%d" % failures.size())
    quit(1)
