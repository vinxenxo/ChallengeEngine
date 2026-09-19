# res://tests/C6F06VisualLoopPhysicalExportTest.gd
extends SceneTree

const ArtifactPaths = preload("res://tests/helpers/ArtifactPaths.gd")

# ============================================================
# C6-F0.6 Step 1 — Visual Loop Physical Export Validation Test
# Checks that the canonical C11 artifact AVI actually exists and is non-empty.
# ============================================================

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F06VisualLoopPhysicalExportTest...")
	
	var target_path: String = ArtifactPaths.absolute("qa/physical_smoke/c10c_e2e/avi/c10c_visual_loop_fractal.avi")
	
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
				print("[INFO] Physical movie file verified successfully. Size: %d bytes." % length)
				
	if failures.is_empty():
		print("[C6F0_6_PHYSICAL_EXPORT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F0_6_PHYSICAL_EXPORT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)