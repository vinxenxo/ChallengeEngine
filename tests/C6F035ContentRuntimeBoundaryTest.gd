extends SceneTree

const ContentRuntime = preload("res://core/runtime/ContentRuntime.gd")
const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")
const ChallengeRuntime = preload("res://core/runtime/ChallengeRuntime.gd")
const VisualLoopRuntime = preload("res://core/runtime/VisualLoopRuntime.gd")
const VisualDrillRuntime = preload("res://core/runtime/VisualDrillRuntime.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F035ContentRuntimeBoundaryTest...")
	_test_registry_fail_closed()
	_test_visual_loop_positive()
	_test_visual_drill_positive()
	_test_visual_negative_contract()
	_test_challenge_boundary_positive()
	_test_common_contract_isolation()

	if failures.is_empty():
		print("[C6F0_3_5_RUNTIME_BOUNDARY_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F0_3_5_RUNTIME_BOUNDARY_SUITE] FAIL")
		quit(1)

func _test_registry_fail_closed() -> void:
	var default_registry := ContentRuntimeRegistry.create_default()
	_assert(not default_registry.has_route("visual_loop", "anything"), "Default registry must not use a wildcard visual route.")
	var registry := ContentRuntimeRegistry.new()
	var register_loop := registry.register_runtime("visual_loop", "test_loop", func(): return VisualLoopRuntime.new())
	_assert(register_loop.success, "Visual loop route registration should succeed.")

	var unknown := registry.resolve({
		"kind": "visual_loop",
		"subtype": "unregistered",
		"payload": {}
	})
	_assert(not unknown.success, "Unknown (kind, subtype) must fail closed.")
	_assert(str(unknown.error_code).begins_with("RUNTIME_ROUTE_NOT_REGISTERED:"), "Unknown route must report RUNTIME_ROUTE_NOT_REGISTERED.")

	var duplicate := registry.register_runtime("visual_loop", "test_loop", func(): return VisualLoopRuntime.new())
	_assert(not duplicate.success and duplicate.error_code == "ROUTE_DUPLICATE", "Duplicate route registration must fail closed.")

	var bad_kind := registry.resolve({"kind": "", "subtype": "x"})
	_assert(not bad_kind.success, "Empty kind must fail closed.")

func _test_visual_loop_positive() -> void:
	var registry := ContentRuntimeRegistry.new()
	_assert(registry.register_runtime("visual_loop", "test_loop", func(): return VisualLoopRuntime.new()).success, "Loop route registration failed.")
	var payload := _valid_loop_payload()
	var resolved := registry.resolve({"kind": "visual_loop", "subtype": "test_loop", "payload": payload})
	_assert(resolved.success, "Valid visual loop must resolve.")
	var runtime: ContentRuntime = resolved.runtime
	_assert(runtime is VisualLoopRuntime, "Visual loop route must instantiate VisualLoopRuntime.")
	_assert(runtime.get_frame_count() == payload.frame_count, "Visual loop frame count must match declaration.")
	_assert(runtime.get_rendered_frame_stream().validate_contract().is_valid, "Visual loop frame stream must validate.")
	var first := runtime.next_frame()
	_assert(first.payload.domain == "visual_loop", "Visual loop frame payload must remain visual-domain specific.")
	_assert(not first.payload.has("phase"), "Visual loop must not invent Challenge phases.")
	var consumed := 1
	while not runtime.is_finished():
		var next := runtime.next_frame()
		_assert(not next.is_empty(), "Visual loop must emit every declared frame.")
		consumed += 1
	_assert(consumed == payload.frame_count, "Visual loop runtime must emit exact declared frame cardinality.")
	_assert(runtime.next_frame().is_empty(), "Visual loop must not emit frames after completion.")

func _test_visual_drill_positive() -> void:
	var registry := ContentRuntimeRegistry.new()
	_assert(registry.register_runtime("visual_drill", "test_drill", func(): return VisualDrillRuntime.new()).success, "Drill route registration failed.")
	var payload := _valid_drill_payload()
	var resolved := registry.resolve({"kind": "visual_drill", "subtype": "test_drill", "payload": payload})
	_assert(resolved.success, "Valid visual drill must resolve.")
	var runtime: ContentRuntime = resolved.runtime
	_assert(runtime is VisualDrillRuntime, "Visual drill route must instantiate VisualDrillRuntime.")
	_assert(runtime.get_frame_count() == payload.frame_count, "Visual drill frame count must match declaration.")
	_assert(runtime.get_rendered_frame_stream().validate_contract().is_valid, "Visual drill frame stream must validate.")
	var frame := runtime.next_frame()
	_assert(frame.payload.domain == "visual_drill", "Visual drill frame payload must remain visual-domain specific.")
	_assert(not frame.payload.has("phase"), "Visual drill must not introduce phase semantics.")

func _test_visual_negative_contract() -> void:
	var loop := VisualLoopRuntime.new()
	var bad_loop := loop.initialize({"kind": "visual_loop", "subtype": "bad", "payload": {
		"duration": 1.0,
		"fps": 30,
		"frame_count": 29,
		"visual_parameters": {"generator": "fractal", "layers": [{"blend_mode": "normal", "speed": 1.0, "complexity": 1}]}
	}})
	_assert(not bad_loop, "Visual loop frame_count mismatch must fail.")

	var drill := VisualDrillRuntime.new()
	var bad_drill := drill.initialize({"kind": "visual_drill", "subtype": "bad", "payload": {
		"duration": 1.0,
		"fps": 30,
		"frame_count": 30,
		"exercise_parameters": {"difficulty_tier": 1, "speed_multiplier": 1.0},
		"stimulus": {"shape": "dot", "size": 1.0, "color": "white"},
		"targets": {"count": 1},
		"distractors": {"count": 0},
		"trajectory": {"pattern": "linear", "speed": 1.0}
	}})
	_assert(not bad_drill, "Visual drill missing task must fail.")

func _test_challenge_boundary_positive() -> void:
	var registry := ContentRuntimeRegistry.create_default()
	var challenge_config := _load_json("res://challenges/CHALLENGE_001.json")
	var resolved := registry.resolve({
		"kind": "challenge",
		"subtype": "key",
		"definition": challenge_config
	})
	_assert(resolved.success, "Challenge key route must resolve through the sovereign runtime.")
	var runtime: ContentRuntime = resolved.runtime
	_assert(runtime is ChallengeRuntime, "Challenge route must instantiate ChallengeRuntime.")
	_assert(runtime.get_frame_count() > 0, "Challenge runtime must expose a non-empty frame stream.")
	_assert(runtime.get_rendered_frame_stream().validate_contract().is_valid, "Challenge frame stream must validate.")
	var first := runtime.next_frame()
	_assert(first.payload.domain == "challenge", "Challenge frame must be challenge-domain opaque payload.")
	_assert(first.payload.has("snapshot"), "Challenge frame payload must carry its opaque snapshot slot.")

func _test_common_contract_isolation() -> void:
	var base_source := FileAccess.get_file_as_string("res://core/runtime/ContentRuntime.gd")
	var stream_source := FileAccess.get_file_as_string("res://core/runtime/RenderedFrameStream.gd")
	var forbidden := ["SimulationResult", "WinningFrameDetector", "ChallengeMechanic", "PresentationUI", "CTAComponent"]
	for token in forbidden:
		_assert(not base_source.contains(token), "ContentRuntime must not depend on forbidden token '%s'." % token)
		_assert(not stream_source.contains(token), "RenderedFrameStream must not depend on forbidden token '%s'." % token)

func _valid_loop_payload() -> Dictionary:
	return {
		"duration": 1.0,
		"fps": 30,
		"frame_count": 30,
		"loop": {"seamless": true, "boundary_tolerance": 0.01},
		"visual_parameters": {
			"generator": "fractal",
			"layers": [
				{"blend_mode": "normal", "speed": 1.0, "complexity": 2}
			]
		}
	}

func _valid_drill_payload() -> Dictionary:
	return {
		"duration": 1.0,
		"fps": 30,
		"frame_count": 30,
		"exercise_parameters": {"difficulty_tier": 2, "speed_multiplier": 1.2, "pacing_mode": "constant"},
		"stimulus": {"shape": "dot", "size": 8.0, "color": "white"},
		"targets": {"count": 1},
		"distractors": {"count": 2},
		"trajectory": {"pattern": "linear", "speed": 1.0},
		"task": {"type": "tracking"}
	}

func _load_json(path: String) -> Dictionary:
	var text := FileAccess.get_file_as_string(path)
	var parsed = JSON.parse_string(text)
	return parsed if parsed is Dictionary else {}

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
