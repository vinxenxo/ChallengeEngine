# res://tests/C9BParkingV2ProductiveGenerationTest.gd
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

## Authoring difficulty uses the 0-100 scale; 50 resolves to HARD.
## CHALLENGE_004 legacy metadata uses level=3, but its actual parameters are HARD.
const DEFAULT_LEVEL := 50
const DEFAULT_SEED := 314159
const DEFAULT_OUTPUT_PATH := "user://c9_b_parking_v2_runtime.json"

func _initialize() -> void:
	print("[TEST] Running C9BParkingV2ProductiveGenerationTest...")

	var output_path := _resolve_output_path()
	var request_result := ChallengeAuthoringRequest.create_from_dictionary({
		"mechanic": "parking_v2",
		"level": DEFAULT_LEVEL,
		"seed": DEFAULT_SEED,
		"profile": "default_parking_v2",
		"overrides": {},
		"content": {
			"hook": "¡SOLO EL 1% APARCA SIN ROZAR!",
			"reveal": "",
			"cta": "¿Lo has clavado?"
		}
	})

	if not bool(request_result.get("success", false)):
		printerr("FAIL: request creation failed: %s" % str(request_result.get("errors", [])))
		quit(1)
		return

	var request: ChallengeAuthoringRequest = request_result.get("request")
	if request == null:
		printerr("FAIL: request object is null.")
		quit(1)
		return

	# ---------------------------------------------------------
	# 1. Authoring -> Canonical V2
	# ---------------------------------------------------------
	var normative := ChallengeGenerator.generate_normative(request)
	if not bool(normative.get("success", false)):
		printerr("FAIL: normative generation failed: %s" % str(normative.get("error", "")))
		quit(1)
		return

	var canonical: Dictionary = normative.get("challenge", {})
	if canonical.is_empty():
		printerr("FAIL: normative generation returned an empty challenge.")
		quit(1)
		return

	var schema := Schema.validate_v2(canonical)
	if not bool(schema.get("is_valid", false)):
		printerr("FAIL: generated Canonical V2 invalid: %s" % str(schema.get("errors", [])))
		quit(1)
		return

	if canonical.get("mechanic") != "parking_v2":
		printerr("FAIL: Canonical V2 mechanic mismatch.")
		quit(1)
		return
	if canonical.get("mechanic_version") != "2.0":
		printerr("FAIL: Canonical V2 mechanic_version mismatch: %s" % str(canonical.get("mechanic_version")))
		quit(1)
		return
	if canonical.get("simulation", {}).get("rng_version") != "2.0":
		printerr("FAIL: Canonical V2 rng_version mismatch.")
		quit(1)
		return

	var canonical_params: Dictionary = canonical.get("simulation", {}).get("parameters", {})
	var canonical_parking: Dictionary = canonical_params.get("parking", {})
	var canonical_tolerance: Dictionary = canonical_params.get("tolerance", {})
	if float(canonical_tolerance.get("distance_px", -1.0)) != 15.0:
		printerr("FAIL: parking_v2 authoring distance tolerance must match CHALLENGE_004 oracle contract.")
		quit(1)
		return
	if float(canonical_tolerance.get("angle_deg", -1.0)) != 6.0:
		printerr("FAIL: parking_v2 authoring angle tolerance must match CHALLENGE_004 oracle contract.")
		quit(1)
		return
	if float(canonical_parking.get("steering_noise", -1.0)) != 0.05:
		printerr("FAIL: parking_v2 authoring steering_noise must match CHALLENGE_004 oracle contract.")
		quit(1)
		return
	if float(canonical_parking.get("max_speed_px", -1.0)) != 12.0:
		printerr("FAIL: parking_v2 authoring max_speed_px must match CHALLENGE_004 oracle contract.")
		quit(1)
		return

	var canonical_video: Dictionary = canonical.get("video", {})
	if canonical_video.get("profile_id") != "parking_v2_social_15s":
		printerr("FAIL: Canonical V2 video profile identity mismatch: %s" % str(canonical_video.get("profile_id", "")))
		quit(1)
		return

	var canonical_audio: Dictionary = canonical.get("audio", {})
	if canonical_audio.get("enabled") != true or canonical_audio.get("profile_id") != "c7_profile_mixed_overlap":
		printerr("FAIL: Canonical V2 audio binding mismatch: %s" % str(canonical_audio))
		quit(1)
		return

	# ---------------------------------------------------------
	# 2. Canonical V2 -> runtime V1 projection
	# ---------------------------------------------------------
	var runtime_projection := ChallengeMigrationAdapter.canonical_v2_to_runtime_v1(canonical)
	if typeof(runtime_projection) != TYPE_DICTIONARY or runtime_projection.is_empty():
		printerr("FAIL: canonical_v2_to_runtime_v1 returned an empty projection.")
		quit(1)
		return

	for required_key in [
		"schema_version",
		"challenge_id",
		"mechanic",
		"generation",
		"video",
		"difficulty",
		"presentation",
		"assets"
	]:
		if not runtime_projection.has(required_key):
			printerr("FAIL: runtime projection missing '%s'." % required_key)
			quit(1)
			return

	if runtime_projection.get("mechanic") != "parking_v2":
		printerr("FAIL: runtime projection mechanic mismatch.")
		quit(1)
		return
	if runtime_projection.get("mechanic_version") != "2.0":
		printerr("FAIL: runtime projection mechanic_version mismatch.")
		quit(1)
		return
	if runtime_projection.get("generation", {}).get("rng_version") != "2.0":
		printerr("FAIL: runtime projection RNG version mismatch.")
		quit(1)
		return

	var canonical_v2_runtime: Dictionary = runtime_projection.get("canonical_v2", {})
	var runtime_audio: Dictionary = canonical_v2_runtime.get("audio", {})
	if runtime_audio.get("enabled") != true or runtime_audio.get("profile_id") != "c7_profile_mixed_overlap":
		printerr("FAIL: runtime projection lost audio binding: %s" % str(runtime_audio))
		quit(1)
		return

	# ---------------------------------------------------------
	# 3. Runtime integration — same effective path as production
	# ---------------------------------------------------------
	var runtime_result := ChallengeRuntimeBridge.run_effective_pipeline(runtime_projection)
	if not bool(runtime_result.get("success", false)):
		printerr("FAIL: effective runtime rejected authoring-generated projection: %s" % str(runtime_result.get("error", "")))
		quit(1)
		return

	var context = runtime_result.get("context")
	if context == null:
		printerr("FAIL: runtime returned no ChallengeRuntimeContext.")
		quit(1)
		return

	var simulation_result: SimulationResult = context.simulation_result
	var timeline = context.timeline
	if simulation_result == null or timeline == null:
		printerr("FAIL: runtime returned incomplete simulation/timeline context.")
		quit(1)
		return

	if simulation_result.frames.is_empty():
		printerr("FAIL: runtime simulation returned no frames.")
		quit(1)
		return

	if timeline.fps != 60:
		printerr("FAIL: runtime timeline FPS mismatch: %s" % str(timeline.fps))
		quit(1)
		return
	if timeline.game_frames != 420:
		printerr("FAIL: runtime game frame count mismatch: %s" % str(timeline.game_frames))
		quit(1)
		return
	if simulation_result.winning_frame < 0:
		printerr("FAIL: runtime produced invalid winning_frame.")
		quit(1)
		return

	# ---------------------------------------------------------
	# 4. Direct canonical execution parity
	# ---------------------------------------------------------
	var direct_result := ChallengeExecutionPipeline.execute(canonical)
	if not bool(direct_result.get("success", false)):
		printerr("FAIL: direct Canonical V2 execution failed: %s" % str(direct_result.get("error", "")))
		quit(1)
		return

	var direct_simulation: SimulationResult = direct_result.get("simulation_result")
	if direct_simulation == null:
		printerr("FAIL: direct Canonical V2 execution returned null SimulationResult.")
		quit(1)
		return

	# Match the certified production path: resolve derived simulation metrics
	# before timeline/validation equivalence checks.
	SimulationMetricsResolver.resolve_metrics(direct_simulation)

	# ChallengeExecutionPipeline.execute() is simulation-only and deliberately does
	# not resolve the winning frame. The effective production path performs the
	# certified F3.2 timeline build, whose WinningFrameDetector is the scoring
	# authority. Reproduce that same post-simulation step before comparing.
	var direct_timeline_result := ChallengeTimelineBuilder.build(canonical, direct_simulation)
	if not direct_timeline_result.success:
		printerr("FAIL: direct Canonical V2 timeline/scoring failed: %s" % str(direct_timeline_result.error))
		quit(1)
		return

	var direct_timeline = direct_timeline_result.timeline
	if direct_timeline == null:
		printerr("FAIL: direct Canonical V2 timeline is null after scoring.")
		quit(1)
		return

	var direct_validation := ChallengeValidator.validate(
		direct_simulation,
		direct_timeline.hook_frames,
		direct_timeline.game_frames
	)
	if not direct_validation.is_valid:
		printerr("FAIL: direct Canonical V2 validation failed: %s" % str(direct_validation.errors))
		quit(1)
		return

	if direct_simulation.winning_frame != simulation_result.winning_frame:
		printerr("FAIL: authoring/runtime winning_frame mismatch.")
		quit(1)
		return
	if direct_simulation.frames.size() != simulation_result.frames.size():
		printerr("FAIL: authoring/runtime frame count mismatch.")
		quit(1)
		return
	if abs(direct_simulation.minimum_distance - simulation_result.minimum_distance) > 0.000001:
		printerr("FAIL: authoring/runtime minimum_distance mismatch.")
		quit(1)
		return
	if abs(direct_simulation.score - simulation_result.score) > 0.000001:
		printerr("FAIL: authoring/runtime score mismatch.")
		quit(1)
		return

	# ---------------------------------------------------------
	# 5. Persist production-ready generated definition
	# ---------------------------------------------------------
	var file := FileAccess.open(output_path, FileAccess.WRITE)
	if file == null:
		printerr("FAIL: unable to write generated runtime JSON: %s" % output_path)
		quit(1)
		return

	file.store_string(JSON.stringify(runtime_projection, "  "))
	file.close()

	if not FileAccess.file_exists(output_path):
		printerr("FAIL: generated runtime JSON was not persisted: %s" % output_path)
		quit(1)
		return

	print("[C9B_PARKING_V2_PRODUCTIVE_GENERATION] PASS")
	print("[C9B_PARKING_V2_PRODUCTIVE_GENERATION] GENERATED_CONFIG=%s" % output_path)
	quit(0)

func _resolve_output_path() -> String:
	var args := OS.get_cmdline_user_args()
	for arg in args:
		if arg.begins_with("--output-config="):
			var value := arg.trim_prefix("--output-config=").strip_edges()
			if not value.is_empty():
				return value
	return DEFAULT_OUTPUT_PATH
