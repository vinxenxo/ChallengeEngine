# res://tests/C6F041VisualLoopRuntimeTest.gd
extends SceneTree

# ============================================================
# C6-F0.4.1 Visual Loop Runtime Test Suite
# Deterministic evolution regression, absolute seamless boundary closure regardless of speed,
# fail-closed initialization, runtime VisualFrameState production, and architectural isolation.
# ============================================================

const VisualLoopGeneratorRegistry = preload("res://core/runtime/visual/VisualLoopGeneratorRegistry.gd")
const VisualFrameState = preload("res://core/runtime/visual/VisualFrameState.gd")
const VisualLoopRuntime = preload("res://core/runtime/VisualLoopRuntime.gd")

var failures: int = 0

func _init() -> void:
	print("[TEST] Running C6F041VisualLoopRuntimeTest...")

	_test_registry_valid_generators()
	_test_registry_unknown_generator_fail_closed()
	_test_registry_rejects_normalized_or_empty()
	_test_all_five_generators_deterministic_evolution()
	_test_all_five_generators_seamless_boundary()
	_test_runtime_initialization_fail_closed()
	_test_visual_loop_runtime_produces_visual_frame_state()
	_test_generator_isolation_from_challenge()

	if failures == 0:
		print("[C6F0_4_1_VISUAL_LOOP_RUNTIME_SUITE] PASS")
		quit(0)
	else:
		push_error("[C6F0_4_1_VISUAL_LOOP_RUNTIME_SUITE] FAIL failures=%d" % failures)
		quit(1)

func _is_state_approx_equal(a: Variant, b: Variant) -> bool:
	if typeof(a) != typeof(b):
		return false
	if a is Dictionary:
		if a.size() != b.size():
			return false
		for k in a:
			if not b.has(k):
				return false
			if not _is_state_approx_equal(a[k], b[k]):
				return false
		return true
	elif a is Array:
		if a.size() != b.size():
			return false
		for i in range(a.size()):
			if not _is_state_approx_equal(a[i], b[i]):
				return false
		return true
	elif a is float:
		return is_equal_approx(a, b)
	else:
		return a == b

func _test_registry_valid_generators() -> void:
	var types := ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]
	for g_type in types:
		var gen = VisualLoopGeneratorRegistry.get_generator(g_type)
		if gen == null:
			_fail("Registry failed to return generator for valid canonical type: " + g_type)
		else:
			var res: Dictionary = gen.generate(15, 30, {"speed": 1.0, "complexity": 3, "blend_mode": "normal"})
			if res.is_empty() or res.get("generator") != g_type:
				_fail("Generator " + g_type + " returned invalid logical layer state.")
	print("[PASS] _test_registry_valid_generators")

func _test_registry_unknown_generator_fail_closed() -> void:
	var unknown_types := ["non_existent", ""]
	for u_type in unknown_types:
		if VisualLoopGeneratorRegistry.get_generator(u_type) != null:
			_fail("Registry permitted unknown generator type '%s'." % u_type)
	print("[PASS] _test_registry_unknown_generator_fail_closed")

func _test_registry_rejects_normalized_or_empty() -> void:
	if VisualLoopGeneratorRegistry.get_generator(" FRACTAL ") != null:
		_fail("Registry accepted padded string generator without strict match.")
	print("[PASS] _test_registry_rejects_normalized_or_empty")

func _test_all_five_generators_deterministic_evolution() -> void:
	var types := ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]
	var total := 60
	for g_type in types:
		var gen = VisualLoopGeneratorRegistry.get_generator(g_type)
		var params := {"speed": 2.5, "complexity": 3, "blend_mode": "normal", "color_palette": "test"}
		var state1: Dictionary = gen.generate(25, total, params)
		var state2: Dictionary = gen.generate(25, total, params)
		var state_diff: Dictionary = gen.generate(26, total, params)
		if not _is_state_approx_equal(state1, state2):
			_fail("Generator " + g_type + " is not structurally deterministic.")
		if _is_state_approx_equal(state1, state_diff):
			_fail("Generator " + g_type + " failed to evolve state across different loop_frames.")
	print("[PASS] _test_all_five_generators_deterministic_evolution")

func _test_all_five_generators_seamless_boundary() -> void:
	var types := ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]
	var total := 60
	for g_type in types:
		var gen = VisualLoopGeneratorRegistry.get_generator(g_type)
		var params := {"speed": 3.7, "complexity": 3}
		var start_state: Dictionary = gen.generate(0, total, params)
		var end_state: Dictionary = gen.generate(total, total, params)
		if not _is_state_approx_equal(start_state, end_state):
			_fail("Generator " + g_type + " failed deep periodic seamless boundary closure with speed 3.7.")
	print("[PASS] _test_all_five_generators_seamless_boundary")

func _test_runtime_initialization_fail_closed() -> void:
	var definition := {
		"kind": "visual_loop",
		"subtype": "geometric",
		"payload": {
			"duration": 1.0,
			"fps": 30,
			"frame_count": 30,
			"visual_parameters": {"generator": "garbage_type"}
		}
	}
	var runtime := VisualLoopRuntime.new()
	if runtime.initialize(definition) == true:
		_fail("VisualLoopRuntime initialized successfully with an unknown generator (fail-closed violated).")
	if runtime.get_current_render_state() != null:
		_fail("VisualLoopRuntime emitted state despite failed initialization.")
	print("[PASS] _test_runtime_initialization_fail_closed")

func _test_visual_loop_runtime_produces_visual_frame_state() -> void:
	var definition := {
		"kind": "visual_loop",
		"subtype": "geometric",
		"payload": {
			"duration": 1.0,
			"fps": 30,
			"frame_count": 30,
			"visual_parameters": {
				"generator": "geometric",
				"layers": [{"blend_mode": "normal", "speed": 1.0, "complexity": 2}]
			}
		}
	}
	var runtime := VisualLoopRuntime.new()
	if not runtime.initialize(definition):
		_fail("Runtime failed to initialize valid geometric payload. error=" + runtime.get_error())
		return

	var first_frame: Dictionary = runtime.next_frame()
	var vfs: VisualFrameState = runtime.get_current_render_state()
	if first_frame.is_empty():
		_fail("VisualLoopRuntime returned an empty first frame.")
	elif vfs == null or vfs.generator_type != "geometric" or vfs.layer_states.is_empty():
		_fail("VisualLoopRuntime failed to produce valid VisualFrameState.")
	else:
		print("[PASS] _test_visual_loop_runtime_produces_visual_frame_state")

func _test_generator_isolation_from_challenge() -> void:
	var types := ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]
	for g_type in types:
		var gen = VisualLoopGeneratorRegistry.get_generator(g_type)
		var script: Script = gen.get_script()
		var source: String = script.source_code if script else ""
		if source.contains("ChallengeMechanic") or source.contains("SimulationResult") or source.contains("WinningFrameDetector") or source.contains("RNG"):
			_fail("Generator " + g_type + " violates domain isolation by referencing Challenge/RNG classes.")
	print("[PASS] _test_generator_isolation_from_challenge")

func _fail(message: String) -> void:
	failures += 1
	print("[FAIL] " + message)
