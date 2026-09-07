extends SceneTree

const ADAPTER = preload("res://core/authoring/ChallengeMigrationAdapter.gd")
const SCHEMA = preload("res://core/validation/C6FChallengeSchemaValidator.gd")
const BRIDGE = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const EXECUTION = preload("res://core/execution/ChallengeExecutionPipeline.gd")
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
	print("[TEST] Running C6F4CanonicalV2FindTest...")
	_run_test()

	if failures.is_empty():
		print("[C6F4_CANONICAL_V2_FIND_SUITE] PASS")
		quit(0)
		return

	for failure in failures:
		printerr("FAIL: " + failure)
	print("[C6F4_CANONICAL_V2_FIND_SUITE] FAIL count=%d" % failures.size())
	quit(1)

func _run_test() -> void:
	var path := "res://challenges/CHALLENGE_007.json"
	var legacy = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not legacy is Dictionary or legacy.is_empty():
		failures.append("Unable to read CHALLENGE_007.json")
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

	var simulation: Dictionary = canonical.get("simulation", {})
	var params: Dictionary = simulation.get("parameters", {})
	var find_params = params.get("find", {})
	if not find_params is Dictionary or find_params.is_empty():
		failures.append("Canonical V2 simulation.parameters.find is missing or empty.")
		return

	for key in [
		"safe_area_x_min", "safe_area_x_max", "safe_area_y_min", "safe_area_y_max",
		"scanner_cx", "scanner_cy", "scanner_ax", "scanner_ay",
		"scanner_wx", "scanner_wy", "target_drift_radius", "target_drift_frequency",
		"distractor_count", "capture_radius"
	]:
		if not find_params.has(key):
			failures.append("Canonical V2 find parameters missing '%s'." % key)

	# Direct pure Canonical V2 execution.
	var direct_input := canonical.duplicate(true)
	direct_input.erase("generation")
	direct_input.erase("difficulty")
	direct_input.erase("content")

	var direct_exec := EXECUTION.execute(direct_input)
	if not bool(direct_exec.get("success", false)):
		failures.append("Direct pure Canonical V2 execution failed: %s" % str(direct_exec.get("error", "")))
		return

	var direct_result: SimulationResult = direct_exec.get("simulation_result")
	if direct_result == null or direct_result.frames.is_empty():
		failures.append("Direct pure Canonical V2 execution returned no simulation frames.")
		return

	if direct_result.winning_frame < 0:
		failures.append("Direct pure Canonical V2 execution returned invalid winning_frame.")

	var direct_topology = direct_result.metadata.get("distractor_topology", [])
	if not direct_topology is Array or direct_topology.size() != 3:
		failures.append("Direct pure Canonical V2 result lost distractor_topology.")

	# Effective runtime must use pure V2 for find_v1.
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
		failures.append("Effective find_v1 runtime input still contains legacy generation.")
	if not (runtime_input.get("video", null) is Dictionary):
		failures.append("Effective find_v1 runtime input does not preserve inline Canonical V2 video.")

	var root_difficulty: Dictionary = runtime_input.get("difficulty", {})
	if root_difficulty.has("find"):
		failures.append("Effective find_v1 runtime input restored legacy mechanical difficulty fields.")

	var effective_result: SimulationResult = context.simulation_result
	var effective_topology = effective_result.metadata.get("distractor_topology", [])
	if not effective_topology is Array or effective_topology.size() != direct_topology.size():
		failures.append("Effective result lost or changed distractor_topology cardinality.")
	else:
		_compare_topology(direct_topology, effective_topology, "direct/effective")

	# Independent legacy oracle.
	var oracle := ORACLE.run(legacy)
	if not bool(oracle.get("valid", false)):
		failures.append("Legacy oracle failed: %s" % str(oracle.get("message", "")))
		return

	var oracle_result: SimulationResult = oracle.get("result")
	if oracle_result == null:
		failures.append("Legacy oracle returned a null SimulationResult.")
		return

	var oracle_topology = oracle_result.metadata.get("distractor_topology", [])
	if not oracle_topology is Array or oracle_topology.size() != effective_topology.size():
		failures.append("Legacy oracle lost or changed distractor_topology cardinality.")
	else:
		_compare_topology(effective_topology, oracle_topology, "effective/oracle")

	var gate := BRIDGE.verify_equivalence(
		oracle.get("timeline"),
		oracle_result,
		context
	)
	if not bool(gate.get("success", false)):
		failures.append("Effective/oracle equivalence failed: %s" % str(gate.get("failures", [])))

	# Direct V2 and effective V2 must agree on all frozen result metrics.
	if direct_result.winning_frame != effective_result.winning_frame:
		failures.append("Direct pure V2 and effective V2 winning_frame differ.")
	if direct_result.frames.size() != effective_result.frames.size():
		failures.append("Direct pure V2 and effective V2 frame counts differ.")
	if abs(direct_result.minimum_distance - effective_result.minimum_distance) > 0.000001:
		failures.append("Direct pure V2 and effective V2 minimum_distance differ.")
	if abs(direct_result.score - effective_result.score) > 0.000001:
		failures.append("Direct pure V2 and effective V2 score differ.")
	if direct_result.metadata.get("close_calls", -1) != effective_result.metadata.get("close_calls", -2):
		failures.append("Direct pure V2 and effective V2 close_calls differ.")

func _compare_topology(expected: Array, actual: Array, label: String) -> void:
	if expected.size() != actual.size():
		failures.append("%s distractor_topology size mismatch." % label)
		return
	for index in range(expected.size()):
		var expected_pos = expected[index]
		var actual_pos = actual[index]
		if not expected_pos is Vector2 or not actual_pos is Vector2:
			failures.append("%s distractor_topology[%d] is not Vector2." % [label, index])
			continue
		if expected_pos.distance_to(actual_pos) > 0.000001:
			failures.append(
				"%s distractor_topology[%d] mismatch: expected=%s actual=%s"
				% [label, index, str(expected_pos), str(actual_pos)]
			)
