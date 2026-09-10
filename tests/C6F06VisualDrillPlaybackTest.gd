extends SceneTree

# ============================================================
# C6-F0.6 Step 2 — Visual Drill Playback Verification Test
# Validates initialization and frame progression of VisualContentPlayer with visual_drill/tracking.
# ============================================================

const VisualContentPlayerScript = preload("res://core/presentation/rendering/VisualContentPlayer.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F06VisualDrillPlaybackTest...")
	
	var node := Node2D.new()
	var player = VisualContentPlayerScript.new()
	player.content_definition_path = "definitions/visual_drill_tracking_canonical.json"
	node.add_child(player)
	root.add_child(node)
	
	var timeout := 0.0
	while not player.is_ready_initialized and timeout < 2.0:
		await process_frame
		timeout += 0.016
		
	if not player.is_ready_initialized or player._runtime == null:
		failures.append("VisualContentPlayer failed to initialize drill definition within timeout window.")
		_conclude()
		return
		
	while not player.playback_finished:
		await process_frame
		
	if player._current_frame_index != player._total_frames:
		failures.append("Frame count mismatch: processed %d, expected %d." % [player._current_frame_index, player._total_frames])
		
	node.queue_free()
	await process_frame
	_conclude()

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F0_6_DRILL_PLAYBACK_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F0_6_DRILL_PHYSICAL_EXPORT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)
