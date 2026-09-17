extends SceneTree

## C10-A — Contract test.
## This test is intentionally limited to authoring output shape and runtime resolution.
## It proves nothing about physical Movie Maker export until executed in the real project.

const Request = preload("res://core/authoring/VisualAuthoringRequest.gd")
const Context = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Generator = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")

var failures: Array[String] = []

func _init() -> void:
    print("[TEST] Running C10AVisualAuthoringPipelineTest...")
    _test_visual_loop_request_to_runtime()
    _test_visual_drill_request_to_runtime()
    _test_reject_unknown_custom_parameter()
    _test_seed_is_external()
    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _context(seed_value: int, content_id: String, family_id: String) -> Context:
    return Context.new(
        seed_value,
        "2.0",
        content_id,
        "1.0.0",
        "4.7.1",
        {"profile_id": "social_default_v1", "coordinate_space": "CANVAS_540X960"},
        {"family_id": family_id},
        {"profile_id": "", "enabled": false},
        {"author": "C10-A-test", "timestamp_ms": 0}
    )

func _loop_policy() -> Dictionary:
    return {
        "allowed_parameters": [
            "seamless", "boundary_tolerance", "blend_mode", "speed", "complexity", "color_palette"
        ],
        "base_parameters": {
            "seamless": true,
            "boundary_tolerance": 0.01,
            "blend_mode": "normal",
            "speed": 1.0,
            "complexity": 1,
            "color_palette": "default"
        },
        "tiers": {
            "1": {"speed": 0.7, "complexity": 1},
            "2": {"speed": 0.85, "complexity": 2},
            "3": {"speed": 1.0, "complexity": 3},
            "4": {"speed": 1.2, "complexity": 4},
            "5": {"speed": 1.4, "complexity": 5}
        }
    }

func _drill_policy() -> Dictionary:
    return {
        "allowed_parameters": [
            "speed_multiplier", "pacing_mode", "stimulus", "targets", "distractors", "trajectory", "task"
        ],
        "base_parameters": {
            "speed_multiplier": 1.0,
            "pacing_mode": "constant",
            "stimulus": {"type": "dot", "size": 10.0, "color": "white"},
            "targets": [{"id": 0, "x": 0.0, "y": 0.0, "status": "active"}],
            "distractors": [],
            "trajectory": {"pattern": "linear", "speed": 1.0},
            "task": {"type": "tracking"}
        },
        "tiers": {
            "1": {"speed_multiplier": 0.7},
            "2": {"speed_multiplier": 0.85},
            "3": {"speed_multiplier": 1.0},
            "4": {"speed_multiplier": 1.2},
            "5": {"speed_multiplier": 1.4}
        }
    }

func _test_visual_loop_request_to_runtime() -> void:
    var request := Request.new("visual_loop", "fractal", 2.0, 30, 3, {"color_palette": "neon"})
    var result := Generator.generate(request, _context(12345, "C10A_LOOP_FRACTAL", "visual_default"), _loop_policy())
    _assert(bool(result.get("success", false)), "visual_loop authoring must succeed")
    if not bool(result.get("success", false)):
        return

    var definition: Dictionary = result.get("content", {})
    _assert(definition.get("kind", "") == "visual_loop", "loop kind mismatch")
    _assert(definition.get("subtype", "") == "fractal", "loop subtype mismatch")
    _assert(int(definition["payload"]["frame_count"]) == 60, "loop frame count mismatch")
    _assert(int(definition.get("seed", -1)) == 12345, "seed must be injected by context")

    var registry = ContentRuntimeRegistry.create_default()
    var resolution: Dictionary = registry.resolve(definition)
    _assert(bool(resolution.get("success", false)), "canonical visual_loop must resolve through runtime registry")
    if bool(resolution.get("success", false)):
        var runtime = resolution.get("runtime")
        _assert(runtime != null, "runtime instance missing")
        if runtime != null:
            _assert(runtime.is_initialized(), "visual loop runtime not initialized")

func _test_visual_drill_request_to_runtime() -> void:
    var request := Request.new("visual_drill", "tracking", 2.0, 30, 3, {})
    var result := Generator.generate(request, _context(12345, "C10A_DRILL_TRACKING", "visual_default"), _drill_policy())
    _assert(bool(result.get("success", false)), "visual_drill authoring must succeed")
    if not bool(result.get("success", false)):
        return

    var definition: Dictionary = result.get("content", {})
    _assert(definition.get("kind", "") == "visual_drill", "drill kind mismatch")
    _assert(definition.get("subtype", "") == "tracking", "drill subtype mismatch")
    _assert(int(definition["payload"]["frame_count"]) == 60, "drill frame count mismatch")

    var registry = ContentRuntimeRegistry.create_default()
    var resolution: Dictionary = registry.resolve(definition)
    _assert(bool(resolution.get("success", false)), "canonical visual_drill must resolve through runtime registry")
    if bool(resolution.get("success", false)):
        var runtime = resolution.get("runtime")
        _assert(runtime != null, "runtime instance missing")
        if runtime != null:
            _assert(runtime.is_initialized(), "visual drill runtime not initialized")

func _test_reject_unknown_custom_parameter() -> void:
    var request := Request.new("visual_loop", "fractal", 2.0, 30, 3, {"palette_variant": 0.5})
    var result := Generator.generate(request, _context(1, "C10A_BAD", "visual_default"), _loop_policy())
    _assert(not bool(result.get("success", false)), "RNG-level custom parameter must be rejected by authoring layer")

func _test_seed_is_external() -> void:
    var request := Request.new("visual_loop", "fractal", 2.0, 30, 3, {})
    _assert(not request.to_dictionary().has("seed"), "VisualAuthoringRequest must not own seed")

func _conclude() -> void:
    if failures.is_empty():
        print("[C10A_VISUAL_AUTHORING_PIPELINE_SUITE] PASS")
        quit(0)
        return

    for failure in failures:
        push_error(failure)
    print("[C10A_VISUAL_AUTHORING_PIPELINE_SUITE] FAIL failures=%d" % failures.size())
    quit(1)
