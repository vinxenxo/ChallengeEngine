# res://tests/C6F08TrackingPlaybackValidationTest.gd
extends SceneTree

# ============================================================
# C6-F0.8-E2 — Tracking Drill Playback & Physical Validation
# Validates Stream 2011 binding, rendering visibility, and geometry.
# ============================================================

const VisualContentPlayerScript = preload("res://core/presentation/rendering/VisualContentPlayer.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")

var failures: Array[String] = []
const MAX_PLAYBACK_WAIT_FRAMES: int = 180

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
		
	var captured_position: Variant = null
	var wait_frames: int = 0
	while not player.playback_finished and wait_frames < MAX_PLAYBACK_WAIT_FRAMES:
		if player._current_frame_index == 1 and captured_position == null:
			var tracker_renderer = _find_renderer(player, "TrackingRenderer.gd")
			if tracker_renderer == null:
				_assert(false, "[%s] TrackingRenderer must exist." % mode)
			else:
				_assert(tracker_renderer.visible, "[%s] TrackingRenderer must be visible." % mode)
				var state: Dictionary = tracker_renderer._frame_state.get("drill_frame_state", tracker_renderer._frame_state)
				var targets: Array = state.get("target_states", [])
				_assert(targets.size() == 1, "[%s] Tracking must expose exactly one rendered target." % mode)
				var trajectory: Dictionary = state.get("trajectory_state", {})
				_assert(str(trajectory.get("type", "")) == "lissajous", "[%s] Tracking trajectory must be Lissajous." % mode)
				var target: Dictionary = targets[0] if not targets.is_empty() else {}
				captured_position = Vector2(float(target.get("x", 0.0)), float(target.get("y", 0.0)))
				_assert(captured_position.y >= 144.0 and captured_position.y <= 816.0, "[%s] Tracking target must remain inside Body." % mode)
				_assert(tracker_renderer._frame_state.get("trajectory_state", {}).get("trail_points", []).size() >= 1, "[%s] Tracking history trail must be emitted." % mode)
		wait_frames += 1
		await process_frame

	if not player.playback_finished:
		_assert(false, "[%s] Playback did not finish within %d process frames." % [mode, MAX_PLAYBACK_WAIT_FRAMES])

	node.queue_free()
	await process_frame
	return captured_position

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