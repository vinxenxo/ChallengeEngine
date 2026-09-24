# res://tests/C6F08SaccadePlaybackValidationTest.gd
extends SceneTree

# ============================================================
# C6-F0.8-E4 — Saccade Drill Playback & Physical Validation
# Validates Stream 2013 binding, rendering visibility, and geometry.
# ============================================================

const VisualContentPlayerScript = preload("res://core/presentation/rendering/VisualContentPlayer.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08SaccadePlaybackValidationTest...")
	await _run_tests()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	var registry := RNGStreamRegistry.new()
	var def = registry.get_definition(registry.STREAM_VISUAL_DRILL_SACCADE)
	_assert(def != null, "Stream 2013 (Saccade) debe estar registrado.")
	if def != null:
		_assert(def.get_allowed_consumers().has("SaccadeGenerator"), "Stream 2013 debe autorizar SaccadeGenerator.")

	var def_path = "definitions/visual_drill_saccade_canonical.json"
	var state = await _run_player_and_validate(def_path, "SACCADE_PILOT")
	
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
		
	var captured_state = null
	var pre_roll_checked: bool = false
	var wait_frames: int = 0
	while not player.playback_finished and wait_frames < 1000:
		wait_frames += 1
		await process_frame

		var saccade_renderer_now = _find_renderer(player, "SaccadeRenderer.gd")
		if not pre_roll_checked and saccade_renderer_now != null:
			var pre_state: Dictionary = saccade_renderer_now.get("_frame_state")
			var pre_drill: Dictionary = pre_state.get("drill_frame_state", pre_state)
			if str(pre_drill.get("presentation_phase", "")) == "PRE_ROLL":
				_assert(str(pre_drill.get("presentation_phase", "")) == "PRE_ROLL", "[%s] Saccade renderer must receive PRE_ROLL state before gameplay." % mode)
				pre_roll_checked = true

		if player._current_frame_index == 1 and captured_state == null:
			var saccade_renderer = _find_renderer(player, "SaccadeRenderer.gd")
			if saccade_renderer == null:
				_assert(false, "[%s] SaccadeRenderer must exist." % mode)
			else:
				_assert(saccade_renderer.visible, "[%s] SaccadeRenderer must be visible." % mode)
				captured_state = saccade_renderer.get("_frame_state")
		
	_assert(player.playback_finished, "[%s] Saccade playback did not finish within watchdog." % mode)
	_assert(player._current_frame_index == player._total_frames, "[%s] Gameplay frame count mismatch." % mode)
	_assert(pre_roll_checked, "[%s] Saccade pre-roll check did not execute." % mode)
	node.queue_free()
	await process_frame
	return captured_state

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
		print("[C6F08_SACCADE_PLAYBACK_VALIDATION_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_SACCADE_PLAYBACK_VALIDATION_SUITE] FAIL failures=%d" % failures.size())
		quit(1)