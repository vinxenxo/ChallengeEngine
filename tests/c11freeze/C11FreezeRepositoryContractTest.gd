extends SceneTree

func _initialize() -> void:
	var required_dirs := [
		"res://artifacts",
		"res://artifacts/tests",
		"res://artifacts/qa",
		"res://artifacts/regression",
		"res://artifacts/production",
		"res://artifacts/releases/c11-b",
		"res://assets/reference",
		"res://tests/fixtures/c7/challenges",
		"res://tests/fixtures/c7_a2_mixed",
		"res://tests/fixtures/seeds",
		"res://schemas",
		"res://docs",
		"res://tools/c11freeze",
		"res://tools/maintenance"
	]
	var required_files := [
		"res://tests/helpers/ArtifactPaths.gd",
		"res://tests/fixtures/seeds/stress_v1.json",
		"res://tools/qa/c7/prepare_c7_a2_video_only_fixture.ps1",
		"res://schemas/challenge_schema.json",
		"res://tools/c11freeze/run_seed_stress.py",
		"res://tools/c11freeze/run_physical_export_suite.ps1",
		"res://tools/maintenance/verify_repository_layout.ps1",
		"res://docs/04_REPOSITORY_STRUCTURE.md",
		"res://docs/05_TESTING_AND_REGRESSION.md",
		"res://docs/07_ROADMAP.md",
		"res://docs/contracts/C11_ARCHITECTURE_MANIFESTO.md",
		"res://docs/operations/TEST_RUNBOOK.md",
		"res://docs/master-prompts/START_PROMPT_C11C_ART_DIRECTION.md"
	]
	var forbidden_dirs := [
		"res://output",
		"res://output_c7",
		"res://output_batch_audit",
		"res://qa",
		"res://c9_c_generated_configs",
		"res://c9_g_generated_configs",
		"res://export",
		"res://scripts"
	]
	var failures := 0
	for path in required_dirs:
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(path)):
			print("[FAIL] Missing required repository directory: ", path)
			failures += 1
	for path in required_files:
		if not FileAccess.file_exists(path):
			print("[FAIL] Missing required repository file: ", path)
			failures += 1
	for path in forbidden_dirs:
		if DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(path)):
			print("[FAIL] Obsolete repository root still present: ", path)
			failures += 1
	if failures > 0:
		print("[C11FREEZE_REPOSITORY_CONTRACT_SUITE] FAIL"); quit(1); return
	print("[C11FREEZE_REPOSITORY_CONTRACT_SUITE] PASS"); quit(0)
