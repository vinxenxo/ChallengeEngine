extends SceneTree

# ============================================================
# C6-F0.5 Step 2 — Physical Rendering & Viewport Integration Test Suite
# ============================================================

const ContentRendererHost = preload("res://core/presentation/rendering/ContentRendererHost.gd")
const VisualLoopRenderer = preload("res://core/presentation/rendering/VisualLoopRenderer.gd")
const VisualDrillRenderer = preload("res://core/presentation/rendering/VisualDrillRenderer.gd")

var failures: Array[String] = []
var test_root: Node

func _initialize() -> void:
	print("[TEST] Running C6F05PhysicalRenderingTest...")
	
	test_root = Node.new()
	root.add_child(test_root)
	
	_run_all_tests()

func _run_all_tests() -> void:
	await _test_renderer_host_lifecycle_and_replacement()
	await _test_visual_loop_renderer_pure_representation()
	await _test_visual_drill_renderer_pure_representation()
	_test_physical_renderer_isolation()
	
	test_root.queue_free()
	# Await process frame guarantees nodes are actually deleted and RIDs are cleared
	await process_frame 
	
	if failures.is_empty():
		print("[C6F0_5_PHYSICAL_RENDERING_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F0_5_PHYSICAL_RENDERING_SUITE] FAIL failures=%d" % failures.size())
		quit(1)

func _test_renderer_host_lifecycle_and_replacement() -> void:
	var host := ContentRendererHost.new()
	test_root.add_child(host)
	
	var loop_renderer := VisualLoopRenderer.new()
	host.mount_renderer(loop_renderer)
	
	_assert(host.get_child_count() == 1, "Host must retain exactly one renderer child after mounting.")
	_assert(host._current_renderer is VisualLoopRenderer, "Host must properly map current renderer to VisualLoopRenderer.")
	
	var drill_renderer := VisualDrillRenderer.new()
	host.mount_renderer(drill_renderer)
	
	_assert(host.get_child_count() == 1, "Host must cleanly swap renderers via remove_child without node leakage/overlapping.")
	_assert(host._current_renderer is VisualDrillRenderer, "Host must replace with VisualDrillRenderer cleanly.")
	
	host.queue_free()
	await process_frame
	print("[PASS] _test_renderer_host_lifecycle_and_replacement")

func _test_visual_loop_renderer_pure_representation() -> void:
	var renderer := VisualLoopRenderer.new()
	test_root.add_child(renderer)
	
	var state_a := {
		"generator_type": "fractal", 
		"layer_states": [
			{"rotation": 1.5, "scale": 2.0, "alpha": 1.0}
		]
	}
	renderer.apply_state(state_a)
	
	var loaded_layers = renderer._frame_state.get("layer_states", [])
	_assert(loaded_layers.size() == 1, "VisualLoopRenderer must store layer state identically.")
	_assert(loaded_layers[0].get("rotation", 0.0) == 1.5, "VisualLoopRenderer must preserve pre-calculated math strictly.")
	
	renderer.queue_free()
	await process_frame
	print("[PASS] _test_visual_loop_renderer_pure_representation")

func _test_visual_drill_renderer_pure_representation() -> void:
	var renderer := VisualDrillRenderer.new()
	test_root.add_child(renderer)
	
	var state := {
		"generator_type": "tracking",
		"stimulus_state": {"x": 0.0, "y": 0.0},
		"target_states": [{"x": 100.0, "y": 100.0}],
		"distractor_states": [{"x": -50.0, "y": -50.0}]
	}
	
	renderer.apply_state(state)
	_assert(renderer._frame_state.get("generator_type", "") == "tracking", "VisualDrillRenderer must store drill state correctly.")
	_assert(renderer._frame_state.get("target_states", []).size() == 1, "VisualDrillRenderer must retain targets.")
	
	renderer.queue_free()
	await process_frame
	print("[PASS] _test_visual_drill_renderer_pure_representation")

func _test_physical_renderer_isolation() -> void:
	var files_to_check := [
		"res://core/presentation/rendering/ContentRendererHost.gd",
		"res://core/presentation/rendering/VisualLoopRenderer.gd",
		"res://core/presentation/rendering/VisualDrillRenderer.gd"
	]
	
	var forbidden := [
		"ChallengeMechanic",
		"SimulationResult",
		"WinningFrameDetector",
		"RNG"
	]
	
	for path in files_to_check:
		if FileAccess.file_exists(path):
			var source := FileAccess.get_file_as_string(path)
			for token in forbidden:
				_assert(not source.contains(token), "Renderer file '%s' must not reference forbidden token '%s'." % [path, token])
				
	print("[PASS] _test_physical_renderer_isolation")

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)