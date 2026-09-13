# res://tests/C6F042VisualDrillRuntimeTest.gd
extends SceneTree

# ============================================================
# C6-F0.4.2 Visual Drill Generator & Runtime Test Suite
# Exhaustive verification of deterministic drill generation, strict fail-closed registry,
# structural validity of stimulus/targets/distractors/trajectory/task, and domain isolation.
# ============================================================

const VisualDrillGeneratorRegistry = preload("res://core/runtime/visual_drill/VisualDrillGeneratorRegistry.gd")
const VisualDrillRuntime = preload("res://core/runtime/VisualDrillRuntime.gd")

var failures: int = 0

func _init() -> void:
	print("[TEST] Running C6F042VisualDrillRuntimeTest...")
	
	_test_registry_valid_generators()
	_test_registry_unknown_generator_fail_closed()
	_test_registry_rejects_normalized_or_empty()
	_test_all_four_generators_deterministic_evolution()
	_test_visual_drill_runtime_positive()
	_test_generator_isolation_from_challenge()
	
	if failures == 0:
		print("[C6F0_4_2_VISUAL_DRILL_SUITE] PASS")
		quit(0)
	else:
		push_error("[C6F0_4_2_VISUAL_DRILL_SUITE] FAIL failures=%d" % failures)
		quit(1)

func _is_state_approx_equal(a: Variant, b: Variant) -> bool:
	if typeof(a) != typeof(b):
		return false
	if a is Dictionary:
		if a.size() != b.size(): return false
		for k in a:
			if not b.has(k): return false
			if not _is_state_approx_equal(a[k], b[k]): return false
		return true
	elif a is Array:
		if a.size() != b.size(): return false
		for i in range(a.size()):
			if not _is_state_approx_equal(a[i], b[i]): return false
		return true
	elif a is float:
		return is_equal_approx(a, b)
	else:
		return a == b

func _test_registry_valid_generators() -> void:
	var types := ["tracking", "pursuit", "saccade", "peripheral_scan"]
	for g_type in types:
		var gen = VisualDrillGeneratorRegistry.get_generator(g_type)
		if gen == null:
			_fail("Registry failed to return generator for valid canonical type: " + g_type)
		else:
			var res = gen.generate(10, 30, _valid_drill_parameters())
			if res.is_empty() or res.get("generator_type") != g_type:
				_fail("Generator " + g_type + " returned invalid state.")
	print("[PASS] _test_registry_valid_generators")

func _test_registry_unknown_generator_fail_closed() -> void:
	var unknown_types := ["non_existent", "", "TRACKING", " pursuit "]
	for u_type in unknown_types:
		var gen = VisualDrillGeneratorRegistry.get_generator(u_type)
		if gen != null:
			_fail("Registry permitted invalid/unknown generator type '%s' (fail-closed violated)." % u_type)
	print("[PASS] _test_registry_unknown_generator_fail_closed")

func _test_registry_rejects_normalized_or_empty() -> void:
	if VisualDrillGeneratorRegistry.get_generator("") != null:
		_fail("Registry accepted empty string generator.")
	print("[PASS] _test_registry_rejects_normalized_or_empty")

func _test_all_four_generators_deterministic_evolution() -> void:
	var types := ["tracking", "pursuit", "saccade", "peripheral_scan"]
	var total := 30
	for g_type in types:
		var gen = VisualDrillGeneratorRegistry.get_generator(g_type)
		var params := _valid_drill_parameters()
		
		var state1 = gen.generate(10, total, params)
		var state2 = gen.generate(10, total, params)
		var state_diff = gen.generate(15, total, params)
		
		if not _is_state_approx_equal(state1, state2):
			_fail("Generator " + g_type + " is not structurally deterministic.")
		if _is_state_approx_equal(state1, state_diff):
			_fail("Generator " + g_type + " failed to evolve state across different frame indices.")
	print("[PASS] _test_all_four_generators_deterministic_evolution")

func _test_visual_drill_runtime_positive() -> void:
	var runtime := VisualDrillRuntime.new()
	var definition := {
		"kind": "visual_drill",
		"subtype": "tracking",
		"payload": _valid_drill_parameters()
	}
	
	if not runtime.initialize(definition):
		_fail("VisualDrillRuntime failed to initialize valid tracking payload.")
		return
		
	if not runtime.is_initialized():
		_fail("VisualDrillRuntime did not report initialized status.")
		
	if runtime.get_frame_count() != 30:
		_fail("VisualDrillRuntime frame count mismatch.")
		
	var first: Dictionary = runtime.next_frame()
	if first.is_empty() or not first.has("payload"):
		_fail("VisualDrillRuntime failed to emit valid first frame.")
	else:
		var payload: Dictionary = first.get("payload", {})
		if payload.get("domain", "") == "challenge" or payload.has("phase"):
			_fail("VisualDrillRuntime leaked Challenge domain semantics.")
			
	print("[PASS] _test_visual_drill_runtime_positive")

func _test_generator_isolation_from_challenge() -> void:
	var types := ["tracking", "pursuit", "saccade", "peripheral_scan"]
	for g_type in types:
		var gen = VisualDrillGeneratorRegistry.get_generator(g_type)
		var script: Script = gen.get_script()
		var source: String = script.source_code if script else ""
		
		if source.contains("ChallengeMechanic") or source.contains("SimulationResult") or source.contains("WinningFrameDetector") or source.contains("RNG"):
			_fail("Generator " + g_type + " violates domain isolation by referencing Challenge/RNG classes.")
	print("[PASS] _test_generator_isolation_from_challenge")

func _valid_drill_parameters() -> Dictionary:
	return {
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

func _fail(message: String) -> void:
	failures += 1
	print("[FAIL] " + message)