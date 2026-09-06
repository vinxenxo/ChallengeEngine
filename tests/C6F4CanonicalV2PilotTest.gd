extends SceneTree

const ADAPTER = preload("res://core/authoring/ChallengeMigrationAdapter.gd")
const SCHEMA = preload("res://core/validation/C6FChallengeSchemaValidator.gd")
const BRIDGE = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const EXECUTION = preload("res://core/execution/ChallengeExecutionPipeline.gd")
const TIMELINE = preload("res://core/execution/ChallengeTimelineBuilder.gd")
const ORACLE = preload("res://core/execution/ChallengeLegacyRuntimeOracle.gd")

const POLICY := {
	"authoring_version": "1.0.0",
	"default_engine_version": "0.1",
	"default_asset_family": "fam_001",
	"default_asset_family_version": "1.0",
	"default_theme": "generic",
	"default_profile_id": "test_master_11s",
	"default_profile_version": "1.0",
	"default_mechanic_version": "1.0",
	"default_difficulty_level": 0
}

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F4CanonicalV2PilotTest...")
	_run_test()

	if failures.is_empty():
		print("[C6F4_CANONICAL_V2_PILOT_SUITE] PASS")
		quit(0)
		return

	for failure in failures:
		printerr("FAIL: " + failure)
	print("[C6F4_CANONICAL_V2_PILOT_SUITE] FAIL count=%d" % failures.size())
	quit(1)

func _run_test() -> void:
	var path := "res://challenges/CHALLENGE_003.json"
	var legacy: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	if legacy.is_empty():
		failures.append("Unable to read CHALLENGE_003.json")
		return

	var migration := ADAPTER.migrate_legacy_v1_to_v2(legacy, POLICY)
	if not bool(migration.get("is_valid", false)):
		failures.append("F1.1 migration failed: %s" % str(migration.get("errors", [])))
		return

	var canonical: Dictionary = migration.get("config", {}).duplicate(true)
	var schema := SCHEMA.validate_v2(canonical)
	if not bool(schema.get("is_valid", false)):
		failures.append("Canonical V2 schema failed: %s" % str(schema.get("errors", [])))
		return

	var effective := BRIDGE.run_effective_pipeline(legacy)
	if not bool(effective.get("success", false)):
		failures.append("Effective runtime failed: %s" % str(effective.get("error", "")))
		return

	var runtime_input: Dictionary = effective.get("runtime_input", {})
	if runtime_input.is_empty():
		failures.append("Effective runtime returned empty runtime_input.")
		return

	# F4.4 Phase 1 invariant: Pilot receives the migrated Canonical V2 directly.
	if runtime_input.has("generation"):
		failures.append("Pilot effective runtime still contains legacy generation projection.")
	if not (runtime_input.get("video") is Dictionary):
		failures.append("Pilot effective runtime video is not the canonical V2 dictionary.")
	if (runtime_input.get("difficulty", {}).get("tolerance", {}) is Dictionary) and not runtime_input.get("difficulty", {}).get("tolerance", {}).is_empty():
		failures.append("Pilot effective runtime leaked legacy difficulty.tolerance into the root contract.")
	for key in ["start_x", "end_x", "target_start", "target_velocity", "trajectory_amplitude", "control_amplitude"]:
		if runtime_input.get("content", {}).has(key):
			failures.append("Pilot effective runtime leaked legacy content.%s into the root contract." % key)
	if not runtime_input.get("simulation", {}).get("parameters", {}).has("trajectory_amplitude"):
		failures.append("Canonical V2 simulation.parameters is missing pilot trajectory_amplitude.")
	if not runtime_input.get("simulation", {}).get("parameters", {}).has("tolerance"):
		failures.append("Canonical V2 simulation.parameters is missing pilot tolerance.")

	# Prove the strict Canonical V2 can execute without the bridge projection.
	var direct_input := canonical.duplicate(true)
	var direct_exec := EXECUTION.execute(direct_input)
	if not bool(direct_exec.get("success", false)):
		failures.append("Direct pure Canonical V2 execution failed: %s" % str(direct_exec.get("error", "")))
		return

	var direct_result: SimulationResult = direct_exec.get("simulation_result")
	if direct_result == null or direct_result.frames.is_empty():
		failures.append("Direct pure Canonical V2 execution returned no simulation frames.")
		return

	var direct_timeline := TIMELINE.build(direct_input, direct_result)
	if not direct_timeline.success:
		failures.append("Direct pure Canonical V2 timeline failed: %s" % direct_timeline.error)
		return

	var oracle := ORACLE.run(legacy)
	if not bool(oracle.get("valid", false)):
		failures.append("Legacy oracle failed: %s" % str(oracle.get("message", "")))
		return

	var direct_context = effective.get("context")
	var direct_gate := BRIDGE.verify_equivalence(
		oracle.get("timeline"),
		oracle.get("result"),
		direct_context
	)
	if not bool(direct_gate.get("success", false)):
		failures.append("Effective/oracle equivalence failed: %s" % str(direct_gate.get("failures", [])))

	if direct_result.winning_frame != direct_context.simulation_result.winning_frame:
		failures.append("Direct pure V2 and effective V2 winning_frame differ.")
	if direct_result.frames.size() != direct_context.simulation_result.frames.size():
		failures.append("Direct pure V2 and effective V2 frame counts differ.")
