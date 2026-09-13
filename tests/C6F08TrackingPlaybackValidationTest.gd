# res://tests/C6F08TrackingPlaybackValidationTest.gd
extends SceneTree

# ============================================================
# C6-F0.8-E2 — Tracking Drill Playback & Physical Validation
# Validates Stream 2011 binding, rendering visibility, and geometry.
# ============================================================

const VisualContentPlayerScript = preload("res://core/presentation/rendering/VisualContentPlayer.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08TrackingPlaybackValidationTest...")
	await _run_tests()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	# 0. Auditoría Stream 2011
	var registry := RNGStreamRegistry.new()
	var def = registry.get_definition(registry.STREAM_VISUAL_DRILL_TRACKING)
	_assert(def != null, "Stream 2011 (Tracking) debe estar registrado.")
	if def != null:
		_assert(def.get_allowed_consumers().has("TrackingGenerator"), "Stream 2011 debe autorizar TrackingGenerator.")

	var def_path = "definitions/visual_drill_tracking_canonical.json"
	var state = await _run_player_and_validate(def_path, "TRACKING_PILOT")
	
	_conclude()

func _run_player_and_validate(def_path: String, mode: String):
	var node := Node2D.new()
	var player = VisualContentPlayerScript.new()
	player.content_definition_path = def_path
	node.add_child(player)
	root.add_child(node)
	
	var timeout := 0.0
	while not player.is_ready_initialized and timeout < 3.0:
		await process_frame
		timeout += 0.016
		
	_assert(player.is_ready_initialized, "[%s] VisualContentPlayer failed to initialize." % mode)
	if not player.is_ready_initialized:
		node.queue_free()
		return null
		
	var captured_params = null
	while not player.playback_finished:
		if player._current_frame_index == 1 and captured_params == null:
			var tracker_renderer = _find_renderer(player, "TrackingRenderer.gd")
			if tracker_renderer == null:
				_assert(false, "[%s] TrackingRenderer must exist." % mode)
			else:
				_assert(tracker_renderer.visible, "[%s] TrackingRenderer must be visible." % mode)
				var rect = tracker_renderer.get("_rect")
				if rect == null:
					_assert(false, "[%s] Geometry Contract: _rect not found." % mode)
				else:
					_assert(rect.size.x > 0 and rect.size.y > 0, "[%s] Geometry Contract invalid." % mode)
					var mat = rect.material as ShaderMaterial
					if mat != null:
						captured_params = mat.get_shader_parameter("tracking_variant")
		await process_frame
		
	node.queue_free()
	await process_frame
	return captured_params

func _find_renderer(node: Node, script_name: String) -> Node:
	var script = node.get_script()
	if script != null and script_name in script.resource_path:
		return node
	for child in node.get_children():
		var found = _find_renderer(child, script_name)
		if found != null:
			return found
	return null

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_TRACKING_PLAYBACK_VALIDATION_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_TRACKING_PLAYBACK_VALIDATION_SUITE] FAIL failures=%d" % failures.size())
		quit(1)