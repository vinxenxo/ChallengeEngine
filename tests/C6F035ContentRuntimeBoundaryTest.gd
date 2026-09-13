# res://tests/C6F035ContentRuntimeBoundaryTest.gd
extends SceneTree

# ============================================================
# C6-F0.3.5 — Polymorphic Content Runtime Boundary Suite
# Contracted against ContentRuntimeRegistry.create_default()/resolve(definition).
# ============================================================

const ContentRuntime = preload("res://core/runtime/ContentRuntime.gd")
const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")
const ChallengeRuntime = preload("res://core/runtime/ChallengeRuntime.gd")
const VisualLoopRuntime = preload("res://core/runtime/VisualLoopRuntime.gd")
const VisualDrillRuntime = preload("res://core/runtime/VisualDrillRuntime.gd")
const RenderedFrameStream = preload("res://core/runtime/RenderedFrameStream.gd")

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
		print("[C6F0_3_5_RUNTIME_BOUNDARY_SUITE] FAIL failures=%d" % failures.size())
		quit(1)


func _test_registry_fail_closed() -> void:
	var registry := ContentRuntimeRegistry.create_default()

	# Canonical positive routes must exist.
	var canonical_routes: Array[String] = [
		"visual_loop::fractal",
		"visual_loop::vector_field",
		"visual_loop::particle_flow",
		"visual_loop::kaleidoscope",
		"visual_loop::geometric",
		"visual_drill::tracking",
		"visual_drill::pursuit",
		"visual_drill::saccade",
		"visual_drill::peripheral_scan",
		"challenge::key",
		"challenge::parking",
		"challenge::pilot"
	]

	var routes := registry.registered_routes()
	for expected in canonical_routes:
		_assert(routes.has(expected), "Missing canonical default route: %s" % expected)

	# Unknown route.
	var unknown: Dictionary = registry.resolve({
		"kind": "visual_loop",
		"subtype": "unregistered"
	})
	_assert(not bool(unknown.get("success", false)), "Unknown route must fail closed.")
	_assert(unknown.get("runtime") == null, "Unknown route must never leak runtime.")

	# Missing/empty routing metadata.
	var empty_kind: Dictionary = registry.resolve({
		"kind": "",
		"subtype": "fractal"
	})
	_assert(not bool(empty_kind.get("success", false)), "Empty kind must fail closed.")
	_assert(empty_kind.get("runtime") == null, "Empty kind must never return runtime.")

	var empty_subtype: Dictionary = registry.resolve({
		"kind": "visual_loop",
		"subtype": ""
	})
	_assert(not bool(empty_subtype.get("success", false)), "Empty subtype must fail closed.")
	_assert(empty_subtype.get("runtime") == null, "Empty subtype must never return runtime.")

	# Exact routing. No normalization.
	var padded: Dictionary = registry.resolve({
		"kind": "visual_loop",
		"subtype": " FRACTAL "
	})
	_assert(not bool(padded.get("success", false)), "Padded subtype must fail closed.")

	var uppercase: Dictionary = registry.resolve({
		"kind": "visual_loop",
		"subtype": "FRACTAL"
	})
	_assert(not bool(uppercase.get("success", false)), "Uppercase subtype must fail closed.")

	print("[PASS] _test_registry_fail_closed")


func _test_visual_loop_positive() -> void:
	var registry := ContentRuntimeRegistry.create_default()
	var definition := _valid_loop_definition()

	var result: Dictionary = registry.resolve(definition)

	_assert(
		bool(result.get("success", false)),
		"Canonical visual_loop/fractal must resolve. error=%s" % str(result.get("error_code", ""))
	)
	if not bool(result.get("success", false)):
		return

	var runtime: ContentRuntime = result.get("runtime")
	_assert(runtime != null, "Resolved visual loop runtime must not be null.")
	if runtime == null:
		return

	_assert(runtime is VisualLoopRuntime, "visual_loop/fractal must instantiate VisualLoopRuntime.")
	if not (runtime is VisualLoopRuntime):
		return

	_assert(runtime.is_initialized(), "VisualLoopRuntime must be initialized by registry resolution.")
	_assert(
		runtime.get_frame_count() == int(definition["payload"]["frame_count"]),
		"Visual loop frame count must match declaration."
	)

	var stream: RenderedFrameStream = runtime.get_rendered_frame_stream()
	_assert(stream != null, "VisualLoopRuntime must expose RenderedFrameStream.")
	if stream == null:
		return

	var validation: Dictionary = stream.validate_contract()
	_assert(
		bool(validation.get("is_valid", false)),
		"Visual loop frame stream must validate: %s" % str(validation.get("errors", []))
	)

	var first: Dictionary = runtime.next_frame()
	_assert(not first.is_empty(), "Visual loop must emit first frame.")
	if first.is_empty():
		return

	var frame_payload: Dictionary = first.get("payload", {})
	_assert(
		frame_payload.get("domain", "") == "visual_loop",
		"Visual loop frame must remain visual-domain specific."
	)
	_assert(
		not frame_payload.has("phase"),
		"Visual loop frame must not invent Challenge phase semantics."
	)

	var consumed := 1
	while not runtime.is_finished():
		var next: Dictionary = runtime.next_frame()
		_assert(not next.is_empty(), "Visual loop must emit every declared frame.")
		if next.is_empty():
			break
		consumed += 1

	_assert(
		consumed == int(definition["payload"]["frame_count"]),
		"Visual loop must emit exact declared frame cardinality."
	)
	_assert(runtime.next_frame().is_empty(), "Visual loop must stop after completion.")

	print("[PASS] _test_visual_loop_positive")


func _test_visual_drill_positive() -> void:
	var registry := ContentRuntimeRegistry.create_default()
	var definition := _valid_drill_definition()

	var result: Dictionary = registry.resolve(definition)

	_assert(
		bool(result.get("success", false)),
		"Canonical visual_drill/tracking must resolve. error=%s" % str(result.get("error_code", ""))
	)
	if not bool(result.get("success", false)):
		return

	var runtime: ContentRuntime = result.get("runtime")
	_assert(runtime != null, "Resolved visual drill runtime must not be null.")
	if runtime == null:
		return

	_assert(runtime is VisualDrillRuntime, "visual_drill/tracking must instantiate VisualDrillRuntime.")
	if not (runtime is VisualDrillRuntime):
		return

	_assert(runtime.is_initialized(), "VisualDrillRuntime must be initialized by registry resolution.")
	_assert(
		runtime.get_frame_count() == int(definition["payload"]["frame_count"]),
		"Visual drill frame count must match declaration."
	)

	var stream: RenderedFrameStream = runtime.get_rendered_frame_stream()
	_assert(stream != null, "VisualDrillRuntime must expose RenderedFrameStream.")
	if stream == null:
		return

	var validation: Dictionary = stream.validate_contract()
	_assert(
		bool(validation.get("is_valid", false)),
		"Visual drill frame stream must validate: %s" % str(validation.get("errors", []))
	)

	var first: Dictionary = runtime.next_frame()
	_assert(not first.is_empty(), "Visual drill must emit first frame.")
	if first.is_empty():
		return

	var payload: Dictionary = first.get("payload", {})
	_assert(
		payload.get("domain", "") == "visual_drill",
		"Visual drill frame must remain visual-domain specific."
	)
	_assert(
		not payload.has("phase"),
		"Visual drill must not introduce phase semantics."
	)

	print("[PASS] _test_visual_drill_positive")


func _test_visual_negative_contract() -> void:
	var registry := ContentRuntimeRegistry.create_default()

	var unknown_loop: Dictionary = registry.resolve({
		"kind": "visual_loop",
		"subtype": "unknown_loop"
	})
	_assert(
		not bool(unknown_loop.get("success", false)),
		"Unknown visual loop subtype must fail closed."
	)
	_assert(unknown_loop.get("runtime") == null, "Unknown loop route must not leak runtime.")

	var bad_loop := _valid_loop_definition()
	bad_loop["payload"]["frame_count"] = 29
	var bad_loop_result: Dictionary = registry.resolve(bad_loop)
	_assert(
		not bool(bad_loop_result.get("success", false)),
		"Visual loop frame_count mismatch must fail during resolution."
	)
	_assert(
		bad_loop_result.get("runtime") == null,
		"Failed visual loop initialization must never leak runtime."
	)

	var unknown_drill: Dictionary = registry.resolve({
		"kind": "visual_drill",
		"subtype": "unknown_drill"
	})
	_assert(
		not bool(unknown_drill.get("success", false)),
		"Unknown visual drill subtype must fail closed."
	)
	_assert(unknown_drill.get("runtime") == null, "Unknown drill route must not leak runtime.")

	var bad_drill := _valid_drill_definition()
	bad_drill["payload"].erase("task")
	var bad_drill_result: Dictionary = registry.resolve(bad_drill)
	_assert(
		not bool(bad_drill_result.get("success", false)),
		"Visual drill missing task must fail during resolution."
	)
	_assert(
		bad_drill_result.get("runtime") == null,
		"Failed visual drill initialization must never leak runtime."
	)

	print("[PASS] _test_visual_negative_contract")


func _test_challenge_boundary_positive() -> void:
	var registry := ContentRuntimeRegistry.create_default()
	var challenge_definition := _load_json("res://challenges/CHALLENGE_001.json")

	_assert(not challenge_definition.is_empty(), "Challenge fixture must load.")
	if challenge_definition.is_empty():
		return

	var routed_definition := {
		"kind": "challenge",
		"subtype": "key",
		"definition": challenge_definition
	}

	var result: Dictionary = registry.resolve(routed_definition)
	_assert(
		bool(result.get("success", false)),
		"Challenge key route must resolve. error=%s" % str(result.get("error_code", ""))
	)
	if not bool(result.get("success", false)):
		return

	var runtime: ContentRuntime = result.get("runtime")
	_assert(runtime != null, "Resolved ChallengeRuntime must not be null.")
	if runtime == null:
		return

	_assert(runtime is ChallengeRuntime, "Challenge key must instantiate ChallengeRuntime.")
	if not (runtime is ChallengeRuntime):
		return

	_assert(runtime.is_initialized(), "ChallengeRuntime must be initialized.")
	_assert(runtime.get_frame_count() > 0, "Challenge runtime must expose frames.")

	var stream: RenderedFrameStream = runtime.get_rendered_frame_stream()
	_assert(stream != null, "Challenge runtime must expose RenderedFrameStream.")
	if stream == null:
		return

	var validation: Dictionary = stream.validate_contract()
	_assert(
		bool(validation.get("is_valid", false)),
		"Challenge frame stream must validate: %s" % str(validation.get("errors", []))
	)

	var first: Dictionary = runtime.next_frame()
	_assert(not first.is_empty(), "Challenge runtime must emit first frame.")
	if first.is_empty():
		return

	var payload: Dictionary = first.get("payload", {})
	_assert(
		payload.get("domain", "") == "challenge",
		"Challenge frame must remain Challenge-domain opaque."
	)
	_assert(
		payload.has("snapshot"),
		"Challenge frame must preserve its opaque snapshot slot."
	)

	print("[PASS] _test_challenge_boundary_positive")


func _test_common_contract_isolation() -> void:
	var base_source := FileAccess.get_file_as_string(
		"res://core/runtime/ContentRuntime.gd"
	)
	var stream_source := FileAccess.get_file_as_string(
		"res://core/runtime/RenderedFrameStream.gd"
	)

	var forbidden := [
		"SimulationResult",
		"WinningFrameDetector",
		"ChallengeMechanic",
		"PresentationUI",
		"CTAComponent"
	]

	for token in forbidden:
		_assert(
			not base_source.contains(token),
			"ContentRuntime must not depend on '%s'." % token
		)
		_assert(
			not stream_source.contains(token),
			"RenderedFrameStream must not depend on '%s'." % token
		)

	print("[PASS] _test_common_contract_isolation")


func _valid_loop_definition() -> Dictionary:
	return {
		"kind": "visual_loop",
		"subtype": "fractal",
		"payload": {
			"duration": 1.0,
			"fps": 30,
			"frame_count": 30,
			"loop": {
				"seamless": true,
				"boundary_tolerance": 0.01
			},
			"visual_parameters": {
				"generator": "fractal",
				"layers": [
					{
						"blend_mode": "normal",
						"speed": 1.0,
						"complexity": 2
					}
				]
			}
		}
	}


func _valid_drill_definition() -> Dictionary:
	return {
		"kind": "visual_drill",
		"subtype": "tracking",
		"payload": {
			"duration": 1.0,
			"fps": 30,
			"frame_count": 30,
			"exercise_parameters": {
				"difficulty_tier": 2,
				"speed_multiplier": 1.2,
				"pacing_mode": "constant"
			},
			"stimulus": {
				"shape": "dot",
				"size": 8.0,
				"color": "white"
			},
			"targets": [
				{
					"id": "t1",
					"x": 50.0,
					"y": 50.0,
					"highlighted": true,
					"status": "active"
				}
			],
			"distractors": [
				{
					"id": "d1",
					"x": -50.0,
					"y": -50.0
				},
				{
					"id": "d2",
					"x": 100.0,
					"y": -100.0
				}
			],
			"trajectory": {
				"pattern": "linear",
				"speed": 1.0
			},
			"task": {
				"type": "tracking",
				"target_id": "t1"
			}
		}
	}

func _load_json(path: String) -> Dictionary:
	var text := FileAccess.get_file_as_string(path)
	var parsed = JSON.parse_string(text)
	return parsed if parsed is Dictionary else {}


func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
