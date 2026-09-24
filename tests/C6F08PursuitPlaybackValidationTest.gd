extends SceneTree

## C11-C.8 2.8.0 — Pursuit playback validation.
## Validates runtime binding and the authored arc-length state surface.

const VisualContentPlayerScript = preload("res://core/presentation/rendering/VisualContentPlayer.gd")

var failures: Array[String] = []

func _initialize() -> void:
    print("[TEST] Running C6F08PursuitPlaybackValidationTest...")
    await _run_tests()

func _run_tests() -> void:
    var node := Node2D.new()
    var player := VisualContentPlayerScript.new()
    player.content_definition_path = "definitions/visual_drill_pursuit_canonical.json"
    node.add_child(player)
    root.add_child(node)
    var timeout := 0.0
    while not player.is_ready_initialized and timeout < 3.0:
        await process_frame
        timeout += 0.016
    _assert(player.is_ready_initialized, "Pursuit VisualContentPlayer failed to initialize.")
    if player.is_ready_initialized:
        while not player.playback_finished:
            await process_frame
        var state: Dictionary = player._last_visual_drill_frame.get("payload", {})
        _assert(str(state.get("generator_type", "")) == "pursuit", "Pursuit final stream state must identify pursuit.")
        _assert(state.get("target_states", []).size() == 1, "Pursuit must expose one target in playback.")
        _assert(str(state.get("trajectory_state", {}).get("parameterization", "")) == "arc_length", "Pursuit playback must expose arc-length parameterization.")
        _assert(player._presentation_total_frames == 690, "Pursuit total presentation frames must be 690.")
    node.queue_free()
    await process_frame
    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C6F08_PURSUIT_PLAYBACK_VALIDATION_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C6F08_PURSUIT_PLAYBACK_VALIDATION_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
