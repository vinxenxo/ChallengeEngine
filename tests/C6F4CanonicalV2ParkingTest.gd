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
	print("[TEST] Running C6F4CanonicalV2ParkingTest...")
	_run_test()

	if failures.is_empty():
		print("[C6F4_CANONICAL_V2_PARKING_SUITE] PASS")
		quit(0)
		return

	for failure in failures:
		printerr("FAIL: " + failure)
	print("[C6F4_CANONICAL_V2_PARKING_SUITE] FAIL count=%d" % failures.size())
	quit(1)

func _run_test() -> void:
	var path := "res://challenges/CHALLENGE_004.json"
	var legacy = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not legacy is Dictionary or legacy.is_empty():
		failures.append("Unable to read CHALLENGE_004.json")
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

	var params: Dictionary = canonical.get("simulation", {}).get("parameters", {})
	if not params.has("parking"):
		failures.append("Canonical V2 simulation.parameters missing parking block.")
	if not params.has("tolerance"):
		failures.append("Canonical V2 simulation.parameters missing tolerance block.")

	# Direct strict Canonical V2 execution.
	var direct_input := canonical.duplicate(true)
	direct_input.erase("generation")
	direct_input["difficulty"] = {"level": int(canonical.get("difficulty", {}).get("level", 0))}
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

	# Effective runtime must use pure V2 for parking_v2.
	var effective := BRIDGE.run_effective_pipeline(legacy)
	if not bool(effective.get("success", false)):
		failures.append("Effective runtime failed: %s" % str(effective.get("error", "")))
		return

	var context: ChallengeRuntimeContext = effective.get("context")
	if context == null or context.simulation_result == null or context.timeline == null:
		failures.append("Effective runtime returned an incomplete RuntimeContext.")
		return

	var runtime_input: Dictionary = effective.get("runtime_input", {})
	if runtime_input.has("generation"):
		failures.append("Effective parking_v2 runtime input still contains legacy generation.")
	if not (runtime_input.get("video", null) is Dictionary):
		failures.append("Effective parking_v2 runtime input does not preserve inline Canonical V2 video.")
	var root_difficulty: Dictionary = runtime_input.get("difficulty", {})
	if root_difficulty.has("parking") or root_difficulty.has("tolerance"):
		failures.append("Effective parking_v2 runtime input restored legacy mechanical difficulty fields.")

	# Independent legacy oracle.
	var oracle := ORACLE.run(legacy)
	if not bool(oracle.get("valid", false)):
		failures.append("Legacy oracle failed: %s" % str(oracle.get("message", "")))
		return

	var gate := BRIDGE.verify_equivalence(
		oracle.get("timeline"),
		oracle.get("result"),
		context
	)
	if not bool(gate.get("success", false)):
		failures.append("Effective/oracle equivalence failed: %s" % str(gate.get("failures", [])))

	if direct_result.winning_frame != context.simulation_result.winning_frame:
		failures.append("Direct pure V2 and effective V2 winning_frame differ.")
	if direct_result.frames.size() != context.simulation_result.frames.size():
		failures.append("Direct pure V2 and effective V2 frame counts differ.")
	if abs(direct_result.minimum_distance - context.simulation_result.minimum_distance) > 0.000001:
		failures.append("Direct pure V2 and effective V2 minimum_distance differ.")
	if abs(direct_result.score - context.simulation_result.score) > 0.000001:
		failures.append("Direct pure V2 and effective V2 score differ.")