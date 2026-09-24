# res://tests/C6F06VisualDrillPlaybackTest.gd
extends SceneTree

# ============================================================
# C6-F0.6 Step 2 — Visual Drill Playback Verification Test
# Validates initialization and frame progression of VisualContentPlayer with visual_drill/tracking.
# ============================================================

const VisualContentPlayerScript = preload("res://core/presentation/rendering/VisualContentPlayer.gd")
const VisualDrillPresentationPhaseLogic = preload("res://core/presentation/VisualDrillPresentationPhaseLogic.gd")

var failures: Array[String] = []
const MAX_WAIT_FRAMES: int = 1000

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
		
	var wait_frames: int = 0
	while not player.playback_finished and wait_frames < MAX_WAIT_FRAMES:
		wait_frames += 1
		await process_frame

	if not player.playback_finished:
		failures.append("Visual Drill playback did not finish within %d process frames." % MAX_WAIT_FRAMES)

	if player._current_frame_index != player._total_frames:
		failures.append("Frame count mismatch: processed %d, expected %d." % [player._current_frame_index, player._total_frames])
	if player._is_visual_drill:
		var expected_total_frames: int = VisualDrillPresentationPhaseLogic.total_presentation_frames(player._total_frames, player._stream.fps)
		if player._visual_drill_countdown_frames != 90 or player._visual_drill_end_cta_frames != 90 or player._presentation_total_frames != expected_total_frames:
			failures.append("Visual Drill presentation frame contract mismatch: countdown=%d end_cta=%d total=%d expected=%d." % [player._visual_drill_countdown_frames, player._visual_drill_end_cta_frames, player._presentation_total_frames, expected_total_frames])
		var expected_total_seconds: float = VisualDrillPresentationPhaseLogic.total_presentation_seconds(player._total_frames, player._stream.fps)
		if expected_total_seconds < 20.0 or expected_total_seconds > 30.0:
			failures.append("Visual Drill total duration outside 20-30s contract: %.3fs." % expected_total_seconds)
		
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
