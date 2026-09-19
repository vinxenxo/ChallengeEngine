# res://tests/C6F06VisualDrillPhysicalExportTest.gd
extends SceneTree

const ArtifactPaths = preload("res://tests/helpers/ArtifactPaths.gd")

# ============================================================
# C6-F0.6 Step 2 — Visual Drill Physical Export Validation Test
# Checks that canonical C11 artifact AVI exists and is non-empty.
# ============================================================

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F06VisualDrillPhysicalExportTest...")
	
	var target_path: String = ArtifactPaths.absolute("qa/physical_smoke/c10c_e2e/avi/c10c_visual_drill_tracking.avi")
	
	await process_frame
	
	if not FileAccess.file_exists(target_path):
		failures.append("Expected physical movie file '%s' was not generated." % target_path)
	else:
		var file: FileAccess = FileAccess.open(target_path, FileAccess.READ)
		if file == null:
			failures.append("Failed to open generated movie file '%s'." % target_path)
		else:
			var length: int = file.get_length()
			file.close()
			if length <= 0:
				failures.append("Generated movie file '%s' is empty (0 bytes)." % target_path)
			else:
				print("[INFO] Tracking drill physical movie file verified. Size: %d bytes." % length)
				
	if failures.is_empty():
		print("[C6F0_6_DRILL_PHYSICAL_EXPORT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F0_6_DRILL_PHYSICAL_EXPORT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)
