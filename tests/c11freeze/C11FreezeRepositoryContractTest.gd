extends SceneTree

func _initialize() -> void:
	var required_dirs := [
		"res://artifacts",
		"res://artifacts/tests",
		"res://artifacts/qa",
		"res://artifacts/regression",
		"res://artifacts/production",
		"res://tools/c11freeze"
	]
	var required_files := [
		"res://tests/helpers/ArtifactPaths.gd",
		"res://tools/c11freeze/run_seed_stress.py",
		"res://tools/c11freeze/run_physical_export_suite.ps1"
	]
	var failures := 0
	for path in required_dirs:
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(path)):
			print("[FAIL] Missing required consolidation directory: ", path)
			failures += 1
	for path in required_files:
		if not FileAccess.file_exists(path):
			print("[FAIL] Missing required consolidation file: ", path)
			failures += 1
	if failures > 0:
		print("[C11FREEZE_REPOSITORY_CONTRACT_SUITE] FAIL"); quit(1); return
	print("[C11FREEZE_REPOSITORY_CONTRACT_SUITE] PASS"); quit(0)
