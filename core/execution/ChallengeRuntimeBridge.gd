class_name ChallengeRuntimeBridge
extends RefCounted

## C6-F4.3 — Legacy V1 -> C6 Effective Runtime Bridge.
##
## Responsibilities:
## - migrate legacy V1 through the certified F1.1 adapter;
## - build a temporary F3-compatible runtime projection without mutating F1.1;
## - execute F3.1 -> F3.2 -> F3.3 as the production runtime path;
## - expose a separate audit gate against the isolated legacy oracle.
##
## Non-responsibilities:
## - no RNG implementation;
## - no simulation mathematics;
## - no winning-frame mathematics;
## - no asset loading;
## - no rendering.

const ChallengeRuntimeContext = preload("res://core/execution/ChallengeRuntimeContext.gd")
const ChallengeMigrationAdapter = preload("res://core/authoring/ChallengeMigrationAdapter.gd")
const ChallengeExecutionPipeline = preload("res://core/execution/ChallengeExecutionPipeline.gd")
const ChallengeTimelineBuilder = preload("res://core/execution/ChallengeTimelineBuilder.gd")
const ChallengePresentationBinder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")
const ChallengeValidator = preload("res://core/validation/ChallengeValidator.gd")
const SimulationMetricsResolver = preload("res://core/simulation/SimulationMetricsResolver.gd")

const MIGRATION_POLICY := {
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

static func build_shadow_context(
	legacy_config: Dictionary,
	legacy_result: SimulationResult
) -> Dictionary:
	var context := ChallengeRuntimeContext.new()

	if legacy_config.is_empty():
		return _failure("SHADOW_INPUT_INVALID", "Legacy challenge configuration is empty.", context)

	if legacy_result == null or legacy_result.error_state != "OK":
		return _failure("SHADOW_INPUT_INVALID", "Legacy SimulationResult is null or failed.", context)

	# ---------------------------------------------------------
	# 1. Certified F1.1 migration — no mutation of the result.
	# ---------------------------------------------------------
	var migration := ChallengeMigrationAdapter.migrate_legacy_v1_to_v2(
		legacy_config,
		MIGRATION_POLICY
	)

	if not bool(migration.get("is_valid", false)):
		return _failure(
			"SHADOW_MIGRATION_FAILED",
			"F1.1 migration failed: %s" % str(migration.get("errors", [])),
			context
		)

	var canonical_v2: Dictionary = migration.get("config", {}).duplicate(true)
	if canonical_v2.is_empty():
		return _failure("SHADOW_MIGRATION_FAILED", "F1.1 returned an empty canonical V2 configuration.", context)

	context.canonical_v2 = canonical_v2.duplicate(true)

	# ---------------------------------------------------------
	# 2. Build a strict, non-persistent F3 runtime projection.
	# ---------------------------------------------------------
	var effective_seed := int(
		legacy_result.metadata.get(
			"seed_used",
			legacy_result.metadata.get("final_seed", legacy_config.get("generation", {}).get("seed", 0))
		)
	)

	var f3_input_result := _build_f3_runtime_input(
		canonical_v2,
		legacy_config,
		effective_seed
	)
	if not bool(f3_input_result.get("success", false)):
		return _failure(
			"SHADOW_F3_ADAPTATION_FAILED",
			str(f3_input_result.get("error", "F3 runtime adaptation failed.")),
			context
		)

	var f3_input: Dictionary = f3_input_result["config"]

	# ---------------------------------------------------------
	# 3. F3.1 — Simulation orchestration.
	# ---------------------------------------------------------
	var execution := ChallengeExecutionPipeline.execute(f3_input)
	if not bool(execution.get("success", false)):
		return _failure(
			"SHADOW_F3_1_FAILED",
			"F3.1 failed: %s" % str(execution.get("error", "unknown error")),
			context
		)

	context.simulation_result = execution.get("simulation_result")
	if context.simulation_result == null:
		return _failure("SHADOW_F3_1_FAILED", "F3.1 returned a null SimulationResult.", context)

	# ---------------------------------------------------------
	# 4. F3.2 — Timeline construction.
	# ---------------------------------------------------------
	var timeline_result = ChallengeTimelineBuilder.build(
		f3_input,
		context.simulation_result
	)
	if not timeline_result.success:
		return _failure(
			"SHADOW_F3_2_FAILED",
			"F3.2 failed: %s" % timeline_result.error,
			context
		)

	context.timeline = timeline_result.timeline
	if context.timeline == null:
		return _failure("SHADOW_F3_2_FAILED", "F3.2 returned a null VideoTimeline.", context)

	# ---------------------------------------------------------
	# 5. F3.3 — Presentation binding.
	# ---------------------------------------------------------
	var binding_result := ChallengePresentationBinder.bind(
		f3_input,
		context.timeline,
		context.simulation_result
	)
	if not binding_result.success:
		return _failure(
			"SHADOW_F3_3_FAILED",
			"F3.3 failed: %s" % binding_result.error,
			context
		)

	context.presentation_binding = binding_result

	return {
		"success": true,
		"error_code": "",
		"error": "",
		"context": context,
		"runtime_input": f3_input
	}


## C6-F4.3 production entry point.
## Executes the effective C6 runtime with the same deterministic seed-attempt
## policy as the frozen legacy path, then applies the certified F3 contracts.
static func run_effective_pipeline(legacy_config: Dictionary) -> Dictionary:
	var context := ChallengeRuntimeContext.new()
	if legacy_config.is_empty():
		return _failure("EFFECTIVE_INPUT_INVALID", "Challenge configuration is empty.", context)

	var migration := ChallengeMigrationAdapter.migrate_legacy_v1_to_v2(
		legacy_config,
		MIGRATION_POLICY
	)
	if not bool(migration.get("is_valid", false)):
		return _failure(
			"EFFECTIVE_MIGRATION_FAILED",
			"F1.1 migration failed: %s" % str(migration.get("errors", [])),
			context
		)

	var canonical_v2: Dictionary = migration.get("config", {}).duplicate(true)
	if canonical_v2.is_empty():
		return _failure("EFFECTIVE_MIGRATION_FAILED", "F1.1 returned an empty canonical V2 configuration.", context)
	context.canonical_v2 = canonical_v2.duplicate(true)

	var generation: Dictionary = legacy_config.get("generation", {})
	var initial_seed := int(generation.get("seed", 12345))
	var current_seed := initial_seed
	var rng_version := str(generation.get("rng_version", "1.0"))
	var attempts := 0
	const MAX_ATTEMPTS := 100

	while attempts < MAX_ATTEMPTS:
		attempts += 1
		var runtime_input: Dictionary
		if str(canonical_v2.get("mechanic", "")) == "pilot":
			# C6-F4.4 Phase 1: Pilot consumes strict Canonical V2 directly.
			runtime_input = canonical_v2.duplicate(true)
			runtime_input["simulation"]["seed"] = current_seed
		else:
			var adapted := _build_f3_runtime_input(canonical_v2, legacy_config, current_seed)
			if not bool(adapted.get("success", false)):
				return _failure(
					"EFFECTIVE_F3_ADAPTATION_FAILED",
					str(adapted.get("error", "F3 runtime adaptation failed.")),
					context
				)
			runtime_input = adapted["config"]
		var execution := ChallengeExecutionPipeline.execute(runtime_input)
		if not bool(execution.get("success", false)):
			return _failure(
				"EFFECTIVE_F3_1_FAILED",
				"F3.1 failed: %s" % str(execution.get("error", "unknown error")),
				context
			)

		var result: SimulationResult = execution.get("simulation_result")
		if result == null:
			return _failure("EFFECTIVE_F3_1_FAILED", "F3.1 returned a null SimulationResult.", context)

		var video_binding = runtime_input.get("video", "")
		var video_profile: Dictionary = {}
		var game_frames: int = 0
		if video_binding is Dictionary:
			# F4.4 Phase 1: Canonical V2 keeps temporal fields flat under video.
			# Resolve frame cardinality directly from that canonical block; do not
			# manufacture a VideoProfile-shaped object or inject legacy defaults.
			video_profile = video_binding.duplicate(true)
			if not video_profile.has("fps") or not video_profile.has("game_duration"):
				return _failure(
					"EFFECTIVE_VIDEO_PROFILE_FAILED",
					"Canonical V2 video is missing mandatory fps/game_duration fields.",
					context
				)
			var canonical_fps := int(round(float(video_profile.get("fps"))))
			var canonical_game_duration := float(video_profile.get("game_duration"))
			game_frames = int(round(canonical_game_duration * float(canonical_fps)))
		else:
			var video_profile_id := str(video_binding)
			video_profile = VideoProfileRegistry.get_profile(video_profile_id)
			if video_profile.is_empty():
				return _failure("EFFECTIVE_VIDEO_PROFILE_FAILED", "Unable to resolve effective VideoProfile binding: %s" % str(video_binding), context)

			var fps := int(video_profile.get("fps", 30))
			var phases: Dictionary = video_profile.get("phases", {})
			if not phases.has("game_duration"):
				return _failure("EFFECTIVE_VIDEO_PROFILE_FAILED", "Resolved VideoProfile is missing mandatory game_duration.", context)
			game_frames = int(round(float(phases.get("game_duration")) * float(fps)))

		var contract_check: Dictionary = result.validate_contract(game_frames)
		if not bool(contract_check.get("is_valid", false)):
			return _failure(
				"EFFECTIVE_SIMULATION_CONTRACT_FAILED",
				str(contract_check.get("message", "Simulation contract violation.")),
				context
			)

		SimulationMetricsResolver.resolve_metrics(result)
		if result.error_state != "OK":
			return _failure(
				"EFFECTIVE_METRICS_FAILED",
				"Metric resolution failed: %s" % result.error_state,
				context
			)

		var timeline_result := ChallengeTimelineBuilder.build(runtime_input, result)
		if not timeline_result.success:
			return _failure(
				"EFFECTIVE_F3_2_FAILED",
				"F3.2 failed: %s" % str(timeline_result.error),
				context
			)

		var timeline: VideoTimeline = timeline_result.timeline
		if timeline == null:
			return _failure("EFFECTIVE_F3_2_FAILED", "F3.2 returned a null VideoTimeline.", context)

		var binding_result := ChallengePresentationBinder.bind(
			runtime_input,
			timeline,
			result
		)
		if not binding_result.success:
			return _failure(
				"EFFECTIVE_F3_3_FAILED",
				"F3.3 failed: %s" % str(binding_result.error),
				context
			)

		var validation: ValidationResult = ChallengeValidator.validate(
			result,
			timeline.hook_frames,
			timeline.game_frames
		)
		if validation.is_valid:
			result.metadata["initial_seed"] = initial_seed
			result.metadata["final_seed"] = current_seed
			result.metadata["seed_used"] = current_seed
			result.metadata["attempts"] = attempts
			result.metadata["rng_version"] = rng_version

			context.simulation_result = result
			context.timeline = timeline
			context.presentation_binding = binding_result
			return {
				"success": true,
				"error_code": "",
				"error": "",
				"context": context,
				"runtime_input": runtime_input,
				"validation": validation
			}

		current_seed = _lcg_next_seed(current_seed)

	return _failure(
		"EFFECTIVE_NO_VALID_SIMULATION",
		"No valid simulation found after %d attempts." % MAX_ATTEMPTS,
		context
	)


static func _lcg_next_seed(seed: int) -> int:
	return int((seed * 1103515245 + 12345) & 0x7fffffff)


static func verify_equivalence(
	legacy_timeline: VideoTimeline,
	legacy_result: SimulationResult,
	shadow_context: ChallengeRuntimeContext
) -> Dictionary:
	var failures: Array[String] = []

	if legacy_timeline == null:
		failures.append("Legacy timeline is null.")

	if legacy_result == null:
		failures.append("Legacy SimulationResult is null.")

	if shadow_context == null:
		failures.append("Shadow context is null.")
	else:
		if shadow_context.simulation_result == null:
			failures.append("Shadow SimulationResult is null.")
		if shadow_context.timeline == null:
			failures.append("Shadow VideoTimeline is null.")
		if shadow_context.presentation_binding == null or not shadow_context.presentation_binding.success:
			failures.append("Shadow PresentationBindingResult is missing or failed.")

	if not failures.is_empty():
		return _gate_result(failures)

	var shadow_result := shadow_context.simulation_result
	var shadow_timeline := shadow_context.timeline

	# Temporal contract gate.
	_compare_int("fps", legacy_timeline.fps, shadow_timeline.fps, failures)
	_compare_int("hook_frames", legacy_timeline.hook_frames, shadow_timeline.hook_frames, failures)
	_compare_int("game_frames", legacy_timeline.game_frames, shadow_timeline.game_frames, failures)
	_compare_int("reveal_frames", legacy_timeline.reveal_frames, shadow_timeline.reveal_frames, failures)
	_compare_int("cta_frames", legacy_timeline.cta_frames, shadow_timeline.cta_frames, failures)
	_compare_int("total_frames", legacy_timeline.total_frames, shadow_timeline.total_frames, failures)

	# Simulation cardinality and local winning-frame gate.
	_compare_int("winning_frame", legacy_result.winning_frame, shadow_result.winning_frame, failures)
	_compare_int("frame_count", legacy_result.frames.size(), shadow_result.frames.size(), failures)

	# Contract-critical deterministic metadata gate.
	# Only values actually stored in SimulationResult.metadata belong here.
	# minimum_distance and score are first-class SimulationResult fields;
	# winning_frame_in_valid_window is derived by ValidationResult.
	var metadata_keys := [
		"initial_seed",
		"final_seed",
		"seed_used",
		"attempts",
		"rng_version",
		"close_calls"
	]
	for key in metadata_keys:
		if not legacy_result.metadata.has(key) or not shadow_result.metadata.has(key):
			failures.append("metadata key '%s' missing from legacy/effective result." % key)
			continue
		if not _variants_equivalent(
			legacy_result.metadata[key],
			shadow_result.metadata[key],
			"metadata.%s" % key,
			-1,
			failures
		):
			break

	# First-class SimulationResult metrics are compared directly.
	if abs(legacy_result.minimum_distance - shadow_result.minimum_distance) > 0.000001:
		failures.append("minimum_distance mismatch: legacy=%.9f shadow=%.9f" % [legacy_result.minimum_distance, shadow_result.minimum_distance])
	if abs(legacy_result.score - shadow_result.score) > 0.000001:
		failures.append("score mismatch: legacy=%.9f shadow=%.9f" % [legacy_result.score, shadow_result.score])

	# ValidationResult is not stored inside SimulationResult, so derive the
	# temporal-window predicate from the already-compared timeline and frame.
	var legacy_absolute := legacy_result.winning_frame + legacy_timeline.hook_frames
	var shadow_absolute := shadow_result.winning_frame + shadow_timeline.hook_frames
	var legacy_in_window := legacy_absolute >= legacy_timeline.hook_frames and legacy_absolute < legacy_timeline.hook_frames + legacy_timeline.game_frames
	var shadow_in_window := shadow_absolute >= shadow_timeline.hook_frames and shadow_absolute < shadow_timeline.hook_frames + shadow_timeline.game_frames
	if legacy_in_window != shadow_in_window:
		failures.append("winning_frame_in_valid_window mismatch: legacy=%s shadow=%s" % [legacy_in_window, shadow_in_window])

	if failures.is_empty():
		for index in range(legacy_result.frames.size()):
			var frame_failures: Array[String] = []
			_compare_frame_snapshot(
				legacy_result.frames[index],
				shadow_result.frames[index],
				index,
				frame_failures
			)
			if not frame_failures.is_empty():
				failures.append_array(frame_failures)
				break

	return _gate_result(failures)


static func _build_f3_runtime_input(
	canonical_v2: Dictionary,
	legacy_config: Dictionary,
	effective_seed: int
) -> Dictionary:
	var config := canonical_v2.duplicate(true)

	# F3.1 consumes generation.seed/rng_version while F1.1 stores the same
	# values under simulation. Keep both coherent in this transient projection.
	var simulation: Dictionary = config.get("simulation", {})
	if not simulation is Dictionary:
		return {
			"success": false,
			"error": "Canonical V2 simulation section is not a Dictionary."
		}

	config["generation"] = {
		"seed": effective_seed,
		"rng_version": str(simulation.get("rng_version", "1.0"))
	}

	# Keep the duplicated simulation metadata coherent with the effective seed.
	config["simulation"]["seed"] = effective_seed

	var video: Dictionary = config.get("video", {})
	if not video is Dictionary:
		return {
			"success": false,
			"error": "Canonical V2 video section is not a Dictionary."
		}

	var profile_id := _resolve_static_legacy_video_profile(video)
	if profile_id.is_empty():
		return {
			"success": false,
			"error": "No certified F4 static VideoProfile maps to legacy video configuration: %s" % str(video)
		}

	config["video"] = profile_id

	# Legacy mechanics in the frozen runtime still consume their declarative
	# physics input from the top-level difficulty/content sections. F1.1 keeps
	# those semantics under simulation.parameters for canonical V2; therefore
	# the transient F3 runtime projection restores only this compatibility view.
	if legacy_config.has("difficulty") and legacy_config["difficulty"] is Dictionary:
		config["difficulty"] = legacy_config["difficulty"].duplicate(true)
	if legacy_config.has("content") and legacy_config["content"] is Dictionary:
		config["content"] = legacy_config["content"].duplicate(true)

	# The presentation and assets remain exactly as migrated by F1.1.
	return {
		"success": true,
		"error": "",
		"config": config
	}


static func _resolve_static_legacy_video_profile(video: Dictionary) -> String:
	var fps := int(video.get("fps", -1))
	var hook := float(video.get("hook_duration", 0.0))
	var game := float(video.get("game_duration", 0.0))
	var reveal := float(video.get("reveal_duration", 0.0))
	var cta := float(video.get("cta_duration", 0.0))

	if fps != 60 or not is_finite(hook) or not is_finite(game) or not is_finite(reveal) or not is_finite(cta):
		return ""

	if is_equal_approx(hook, 0.0) and is_equal_approx(game, 7.0) and is_equal_approx(reveal, 0.0) and is_equal_approx(cta, 0.0):
		return "f4_legacy_60_h0_g7_r0_c0"
	if is_equal_approx(hook, 0.0) and is_equal_approx(game, 7.0) and is_equal_approx(reveal, 0.0) and is_equal_approx(cta, 2.0):
		return "f4_legacy_60_h0_g7_r0_c2"
	if is_equal_approx(hook, 3.0) and is_equal_approx(game, 7.0) and is_equal_approx(reveal, 0.0) and is_equal_approx(cta, 0.0):
		return "f4_legacy_60_h3_g7_r0_c0"
	if is_equal_approx(hook, 3.0) and is_equal_approx(game, 7.0) and is_equal_approx(reveal, 0.0) and is_equal_approx(cta, 2.0):
		return "f4_legacy_60_h3_g7_r0_c2"
	if is_equal_approx(hook, 3.0) and is_equal_approx(game, 7.0) and is_equal_approx(reveal, 3.0) and is_equal_approx(cta, 2.0):
		return "f4_legacy_60_h3_g7_r3_c2"

	return ""


static func _compare_frame_snapshot(
	legacy_frame: FrameSnapshot,
	shadow_frame: FrameSnapshot,
	index: int,
	failures: Array[String]
) -> void:
	if legacy_frame == null or shadow_frame == null:
		failures.append("FrameSnapshot null at frame %d." % index)
		return

	if legacy_frame.position.distance_to(shadow_frame.position) > 0.000001:
		failures.append("position mismatch at frame %d: %s vs %s" % [index, legacy_frame.position, shadow_frame.position])
		return
	if abs(legacy_frame.rotation - shadow_frame.rotation) > 0.000001:
		failures.append("rotation mismatch at frame %d: %.9f vs %.9f" % [index, legacy_frame.rotation, shadow_frame.rotation])
		return
	if legacy_frame.scale.distance_to(shadow_frame.scale) > 0.000001:
		failures.append("scale mismatch at frame %d: %s vs %s" % [index, legacy_frame.scale, shadow_frame.scale])
		return
	if abs(legacy_frame.opacity - shadow_frame.opacity) > 0.000001:
		failures.append("opacity mismatch at frame %d: %.9f vs %.9f" % [index, legacy_frame.opacity, shadow_frame.opacity])
		return

	if not _variants_equivalent(legacy_frame.custom_data, shadow_frame.custom_data, "custom_data", index, failures):
		return


static func _variants_equivalent(
	left: Variant,
	right: Variant,
	path: String,
	frame_index: int,
	failures: Array[String]
) -> bool:
	if typeof(left) != typeof(right):
		failures.append("%s type mismatch at frame %d: %s vs %s" % [path, frame_index, typeof(left), typeof(right)])
		return false

	if left is Dictionary:
		if left.size() != right.size():
			failures.append("%s size mismatch at frame %d" % [path, frame_index])
			return false
		for key in left.keys():
			if not right.has(key):
				failures.append("%s missing key '%s' at frame %d" % [path, str(key), frame_index])
				return false
			if not _variants_equivalent(left[key], right[key], "%s.%s" % [path, str(key)], frame_index, failures):
				return false
		return true

	if left is Array:
		if left.size() != right.size():
			failures.append("%s length mismatch at frame %d" % [path, frame_index])
			return false
		for i in range(left.size()):
			if not _variants_equivalent(left[i], right[i], "%s[%d]" % [path, i], frame_index, failures):
				return false
		return true

	if left is Vector2:
		if left.distance_to(right) > 0.000001:
			failures.append("%s Vector2 mismatch at frame %d: %s vs %s" % [path, frame_index, left, right])
			return false
		return true

	if left is float:
		if abs(float(left) - float(right)) > 0.000001:
			failures.append("%s float mismatch at frame %d: %.9f vs %.9f" % [path, frame_index, left, right])
			return false
		return true

	return left == right


static func _compare_int(
	name: String,
	left: int,
	right: int,
	failures: Array[String]
) -> void:
	if left != right:
		failures.append("%s mismatch: legacy=%d shadow=%d" % [name, left, right])


static func _gate_result(failures: Array[String]) -> Dictionary:
	return {
		"success": failures.is_empty(),
		"error_code": "" if failures.is_empty() else "SHADOW_EQUIVALENCE_FAILED",
		"error": "" if failures.is_empty() else " | ".join(failures),
		"failures": failures
	}


static func _failure(
	code: String,
	message: String,
	context: ChallengeRuntimeContext
) -> Dictionary:
	return {
		"success": false,
		"error_code": code,
		"error": message,
		"context": context
	}
