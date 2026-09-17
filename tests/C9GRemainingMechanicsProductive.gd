# res://tests/C9GRemainingMechanicsProductive.gd
extends SceneTree

const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const ChallengeGenerator = preload("res://core/authoring/ChallengeGenerator.gd")
const ChallengeMigrationAdapter = preload("res://core/authoring/ChallengeMigrationAdapter.gd")
const ChallengeRuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const ChallengeExecutionPipeline = preload("res://core/execution/ChallengeExecutionPipeline.gd")
const ChallengeTimelineBuilder = preload("res://core/execution/ChallengeTimelineBuilder.gd")
const ChallengeValidator = preload("res://core/validation/ChallengeValidator.gd")
const SimulationMetricsResolver = preload("res://core/simulation/SimulationMetricsResolver.gd")
const Schema = preload("res://core/validation/C6FChallengeSchemaValidator.gd")

const EXPECTED: Dictionary = {
	"key": {
		"mechanic_version": "1.0",
		"rng_version": "1.0",
		"family": "fam_key_01",
		"video": "f4_legacy_60_h0_g7_r0_c2",
		"audio": "c7_profile_tone_only"
	},
	"pilot": {
		"mechanic_version": "2.0",
		"rng_version": "2.0",
		"family": "fam_pilot_01",
		"video": "f4_legacy_60_h3_g7_r0_c2",
		"audio": "c7_profile_mixed_alt"
	},
	"find_v1": {
		"mechanic_version": "1.0",
		"rng_version": "2.0",
		"family": "fam_find_01",
		"video": "f4_legacy_60_h3_g7_r0_c0",
		"audio": "c7_test_profile"
	},
	"choose_v1": {
		"mechanic_version": "1.0",
		"rng_version": "2.0",
		"family": "fam_choose_01",
		"video": "f4_legacy_60_h3_g7_r0_c2",
		"audio": "c7_test_profile"
	},
	"count_v1": {
		"mechanic_version": "1.0",
		"rng_version": "2.0",
		"family": "fam_count_01",
		"video": "f4_legacy_60_h3_g7_r0_c2",
		"audio": "c7_test_profile"
	}
}

func _fail(message: String) -> void:
	printerr("FAIL: %s" % message)
	quit(1)

func _initialize() -> void:
	print("[TEST] Running C9GRemainingMechanicsProductive...")
	var input_path := _get_arg("--input-batch=")
	var output_dir := _get_arg("--output-dir=")
	if input_path.is_empty() or output_dir.is_empty():
		_fail("missing --input-batch or --output-dir")
		return

	var input := FileAccess.open(input_path, FileAccess.READ)
	if input == null:
		_fail("unable to read input batch: %s" % input_path)
		return
	var json := JSON.new()
	var parse_error := json.parse(input.get_as_text())
	input.close()
	if parse_error != OK or typeof(json.data) != TYPE_ARRAY:
		_fail("authoring_remaining_c9_batch.json must be a JSON array")
		return

	var requests: Array = json.data
	if requests.size() != 5:
		_fail("expected exactly 5 remaining mechanics, got %d" % requests.size())
		return

	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output_dir))
	var generated_ids: Dictionary = {}
	var generated := 0

	for req_data in requests:
		if typeof(req_data) != TYPE_DICTIONARY:
			_fail("batch entry is not a Dictionary")
			return
		var mechanic := str(req_data.get("mechanic", ""))
		if not EXPECTED.has(mechanic):
			_fail("unexpected remaining mechanic: %s" % mechanic)
			return

		var request_result := ChallengeAuthoringRequest.create_from_dictionary(req_data)
		if not bool(request_result.get("success", false)):
			_fail("request creation failed for %s: %s" % [mechanic, str(request_result.get("errors", []))])
			return
		var request: ChallengeAuthoringRequest = request_result.get("request")

		var normative := ChallengeGenerator.generate_normative(request)
		if not bool(normative.get("success", false)):
			_fail("normative generation failed for %s: %s" % [mechanic, str(normative.get("error", ""))])
			return

		var canonical: Dictionary = normative.get("challenge", {})
		var schema := Schema.validate_v2(canonical)
		if not bool(schema.get("is_valid", false)):
			_fail("Canonical V2 invalid for %s: %s" % [mechanic, str(schema.get("errors", []))])
			return

		var expected: Dictionary = EXPECTED[mechanic]
		if str(canonical.get("mechanic")) != mechanic:
			_fail("mechanic identity mismatch for %s" % mechanic)
			return
		if str(canonical.get("mechanic_version")) != expected["mechanic_version"]:
			_fail("mechanic_version mismatch for %s" % mechanic)
			return
		if str(canonical.get("asset_family")) != expected["family"]:
			_fail("asset family mismatch for %s" % mechanic)
			return
		if str(canonical.get("simulation", {}).get("rng_version")) != expected["rng_version"]:
			_fail("rng_version mismatch for %s" % mechanic)
			return
		if str(canonical.get("video", {}).get("profile_id")) != expected["video"]:
			_fail("video profile mismatch for %s" % mechanic)
			return
		var audio: Dictionary = canonical.get("audio", {})
		if audio.get("enabled") != true or str(audio.get("profile_id")) != expected["audio"]:
			_fail("audio profile mismatch for %s: %s" % [mechanic, str(audio)])
			return

		if not _validate_mechanic_contract(mechanic, canonical.get("simulation", {}).get("parameters", {})):
			return

		var runtime_projection := ChallengeMigrationAdapter.canonical_v2_to_runtime_v1(canonical)
		if runtime_projection.is_empty():
			_fail("runtime projection empty for %s" % mechanic)
			return

		var runtime_result := ChallengeRuntimeBridge.run_effective_pipeline(runtime_projection)
		if not bool(runtime_result.get("success", false)):
			_fail("runtime rejected generated %s: %s" % [mechanic, str(runtime_result.get("error", ""))])
			return

		var context = runtime_result.get("context")
		if context == null or context.simulation_result == null or context.timeline == null:
			_fail("runtime context incomplete for %s" % mechanic)
			return

		var direct_result := ChallengeExecutionPipeline.execute(canonical)
		if not bool(direct_result.get("success", false)):
			_fail("direct canonical execution failed for %s: %s" % [mechanic, str(direct_result.get("error", ""))])
			return
		var direct_simulation: SimulationResult = direct_result.get("simulation_result")
		SimulationMetricsResolver.resolve_metrics(direct_simulation)
		var direct_timeline_result := ChallengeTimelineBuilder.build(canonical, direct_simulation)
		if not direct_timeline_result.success:
			_fail("direct timeline failed for %s: %s" % [mechanic, str(direct_timeline_result.error)])
			return
		var direct_timeline = direct_timeline_result.timeline
		var direct_validation := ChallengeValidator.validate(direct_simulation, direct_timeline.hook_frames, direct_timeline.game_frames)
		if not direct_validation.is_valid:
			_fail("direct validation failed for %s: %s" % [mechanic, str(direct_validation.errors)])
			return

		var runtime_simulation: SimulationResult = context.simulation_result
		if direct_simulation.winning_frame != runtime_simulation.winning_frame:
			_fail("winning_frame mismatch for %s" % mechanic)
			return
		if abs(direct_simulation.minimum_distance - runtime_simulation.minimum_distance) > 0.000001:
			_fail("minimum_distance mismatch for %s" % mechanic)
			return
		if abs(direct_simulation.score - runtime_simulation.score) > 0.000001:
			_fail("score mismatch for %s" % mechanic)
			return

		var challenge_id := str(runtime_projection.get("challenge_id", "")).strip_edges()
		if challenge_id.is_empty() or generated_ids.has(challenge_id):
			_fail("invalid or duplicate challenge_id for %s" % mechanic)
			return

		var output_path := output_dir.path_join("CHALLENGE_%s.json" % challenge_id)
		var output_file := FileAccess.open(output_path, FileAccess.WRITE)
		if output_file == null:
			_fail("unable to write %s" % output_path)
			return
		output_file.store_string(JSON.stringify(runtime_projection, "  "))
		output_file.close()
		generated_ids[challenge_id] = true
		generated += 1
		print("  -> [%s] PASS" % mechanic)

	if generated != requests.size():
		_fail("generated=%d expected=%d" % [generated, requests.size()])
		return

	print("[C9-G] AUTHORING -> RUNTIME: PASS (5/5)")
	print("[C9-G] GENERATED_COUNT=%d" % generated)
	quit(0)

func _validate_mechanic_contract(mechanic: String, parameters: Dictionary) -> bool:
	match mechanic:
		"key":
			var tolerance: Dictionary = parameters.get("tolerance", {})
			if abs(float(tolerance.get("rotation_deg", -1.0)) - 4.5) > 0.000001:
				_fail("key tolerance.rotation_deg oracle mismatch")
				return false
		"pilot":
			if abs(float(parameters.get("start_x", -1.0))) > 0.000001 or abs(float(parameters.get("end_x", -1.0)) - 100.0) > 0.000001:
				_fail("pilot start/end mismatch")
				return false
			if abs(float(parameters.get("target_start", -1.0))) > 0.000001:
				_fail("pilot target_start mismatch")
				return false
			if abs(float(parameters.get("target_velocity", -1.0)) - 0.2386634844868735) > 0.000001:
				_fail("pilot target_velocity mismatch")
				return false
			if abs(float(parameters.get("trajectory_amplitude", -1.0)) - 2.0) > 0.000001 or abs(float(parameters.get("control_amplitude", -1.0)) - 0.5) > 0.000001:
				_fail("pilot amplitude mismatch")
				return false
		"find_v1":
			var find_parameters: Dictionary = parameters.get("find", {})
			if int(find_parameters.get("distractor_count", -1)) != 3 or abs(float(find_parameters.get("capture_radius", -1.0)) - 85.0) > 0.000001 or abs(float(find_parameters.get("target_drift_radius", -1.0)) - 50.0) > 0.000001:
				_fail("find difficulty mismatch")
				return false
			if find_parameters.get("target_origin") != [540.0, 960.0]:
				_fail("find target_origin mismatch")
				return false
		"choose_v1":
			var choose_parameters: Dictionary = parameters.get("choose", {})
			if int(choose_parameters.get("options_count", -1)) != 3 or choose_parameters.get("positions") != [[270.0, 960.0], [540.0, 960.0], [810.0, 960.0]]:
				_fail("choose contract mismatch")
				return false
		"count_v1":
			var count_parameters: Dictionary = parameters.get("count", {})
			if int(count_parameters.get("min_value", -1)) != 3 or int(count_parameters.get("max_value", -1)) != 10:
				_fail("count range mismatch")
				return false
			if count_parameters.get("start_pos") != [180.0, 850.0] or abs(float(count_parameters.get("step_x", -1.0)) - 100.0) > 0.000001:
				_fail("count layout mismatch")
				return false
	return true

func _get_arg(prefix: String) -> String:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with(prefix):
			return arg.trim_prefix(prefix).strip_edges()
	return ""
