# res://tests/C9EHitAuthoringProductiveTest.gd
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

const DEFAULT_LEVEL := 50
const DEFAULT_SEED := 998877

func _initialize() -> void:
	print("[TEST] Running C9EHitAuthoringProductiveTest...")
	var output_path := _get_arg("--output-config=")
	if output_path.is_empty():
		printerr("FAIL: missing --output-config argument.")
		quit(1)
		return

	var request_result := ChallengeAuthoringRequest.create_from_dictionary({
		"mechanic": "hit_v1",
		"level": DEFAULT_LEVEL,
		"seed": DEFAULT_SEED,
		"profile": "default_hit_v1",
		"overrides": {},
		"content": {
			"hook": "MATHEMATICAL HIT V1",
			"reveal": "",
			"cta": "DOWNLOAD NOW"
		}
	})
	if not bool(request_result.get("success", false)):
		printerr("FAIL: request creation failed: %s" % str(request_result.get("errors", [])))
		quit(1)
		return

	var request: ChallengeAuthoringRequest = request_result.get("request")
	var normative := ChallengeGenerator.generate_normative(request)
	if not bool(normative.get("success", false)):
		printerr("FAIL: normative generation failed: %s" % str(normative.get("error", "")))
		quit(1)
		return

	var canonical: Dictionary = normative.get("challenge", {})
	var schema := Schema.validate_v2(canonical)
	if not bool(schema.get("is_valid", false)):
		printerr("FAIL: generated Canonical V2 invalid: %s" % str(schema.get("errors", [])))
		quit(1)
		return

	if canonical.get("mechanic") != "hit_v1" or canonical.get("mechanic_version") != "1.0":
		printerr("FAIL: mechanic identity mismatch.")
		quit(1)
		return
	if canonical.get("asset_family") != "fam_hit_01":
		printerr("FAIL: asset family mismatch.")
		quit(1)
		return
	if canonical.get("simulation", {}).get("rng_version") != "2.0":
		printerr("FAIL: rng_version mismatch.")
		quit(1)
		return

	var params: Dictionary = canonical.get("simulation", {}).get("parameters", {})
	if float(params.get("hitbox_radius", -1.0)) != 30.0:
		printerr("FAIL: hitbox_radius must match CHALLENGE_005 oracle contract.")
		quit(1)
		return
	if float(params.get("speed_base", -1.0)) != 3.5:
		printerr("FAIL: speed_base must match CHALLENGE_005 oracle contract.")
		quit(1)
		return
	if params.get("origin") != [540.0, 1500.0] or params.get("target") != [540.0, 300.0]:
		printerr("FAIL: origin/target must match CHALLENGE_005 oracle contract.")
		quit(1)
		return

	if canonical.get("video", {}).get("profile_id") != "f4_legacy_60_h0_g7_r0_c0":
		printerr("FAIL: video profile identity mismatch.")
		quit(1)
		return
	var audio: Dictionary = canonical.get("audio", {})
	if audio.get("enabled") != true or audio.get("profile_id") != "c7_profile_multi_noise":
		printerr("FAIL: audio binding mismatch: %s" % str(audio))
		quit(1)
		return

	var runtime_projection := ChallengeMigrationAdapter.canonical_v2_to_runtime_v1(canonical)
	if runtime_projection.is_empty():
		printerr("FAIL: runtime projection empty.")
		quit(1)
		return
	if runtime_projection.get("video_profile") != "f4_legacy_60_h0_g7_r0_c0":
		printerr("FAIL: runtime video profile mismatch.")
		quit(1)
		return

	var runtime_result := ChallengeRuntimeBridge.run_effective_pipeline(runtime_projection)
	if not bool(runtime_result.get("success", false)):
		printerr("FAIL: runtime rejected authoring-generated projection: %s" % str(runtime_result.get("error", "")))
		quit(1)
		return
	var context = runtime_result.get("context")
	if context == null or context.simulation_result == null or context.timeline == null:
		printerr("FAIL: runtime context incomplete.")
		quit(1)
		return

	var runtime_simulation: SimulationResult = context.simulation_result
	if runtime_simulation.minimum_distance < 0.0:
		printerr("FAIL: runtime minimum_distance invalid.")
		quit(1)
		return

	var direct_result := ChallengeExecutionPipeline.execute(canonical)
	if not bool(direct_result.get("success", false)):
		printerr("FAIL: direct canonical execution failed: %s" % str(direct_result.get("error", "")))
		quit(1)
		return
	var direct_simulation: SimulationResult = direct_result.get("simulation_result")
	SimulationMetricsResolver.resolve_metrics(direct_simulation)
	var direct_timeline_result := ChallengeTimelineBuilder.build(canonical, direct_simulation)
	if not direct_timeline_result.success:
		printerr("FAIL: direct timeline build failed: %s" % str(direct_timeline_result.error))
		quit(1)
		return
	var direct_timeline = direct_timeline_result.timeline
	var direct_validation := ChallengeValidator.validate(direct_simulation, direct_timeline.hook_frames, direct_timeline.game_frames)
	if not direct_validation.is_valid:
		printerr("FAIL: direct validation failed: %s" % str(direct_validation.errors))
		quit(1)
		return

	if direct_simulation.winning_frame != runtime_simulation.winning_frame:
		printerr("FAIL: winning_frame mismatch.")
		quit(1)
		return
	if abs(direct_simulation.minimum_distance - runtime_simulation.minimum_distance) > 0.000001:
		printerr("FAIL: minimum_distance mismatch.")
		quit(1)
		return
	if abs(direct_simulation.score - runtime_simulation.score) > 0.000001:
		printerr("FAIL: score mismatch.")
		quit(1)
		return

	var file := FileAccess.open(output_path, FileAccess.WRITE)
	if file == null:
		printerr("FAIL: unable to persist runtime JSON.")
		quit(1)
		return
	file.store_string(JSON.stringify(runtime_projection, "  "))
	file.close()

	print("[C9E_HIT_V1_PRODUCTIVE_GENERATION] PASS")
	print("[C9E_HIT_V1_PRODUCTIVE_GENERATION] GENERATED_CONFIG=%s" % output_path)
	quit(0)

func _get_arg(prefix: String) -> String:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with(prefix):
			return arg.trim_prefix(prefix).strip_edges()
	return ""
