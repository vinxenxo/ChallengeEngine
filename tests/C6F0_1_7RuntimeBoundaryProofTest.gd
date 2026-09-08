extends SceneTree

# ============================================================
# C6-F0.1.7-B — Runtime Boundary Proof
#
# Proof boundary:
#
#   LEGACY V1
#       -> ChallengeLegacyRuntimeOracle
#       -> SimulationResult A
#
#   LEGACY V1
#       -> F1.1 Migration
#       -> ChallengeRuntimeBridge.run_effective_pipeline()
#       -> F3.1 / F3.2 / F3.3
#       -> SimulationResult B
#
# The test MUST NOT:
# - instantiate mechanics directly;
# - build RNG contexts manually;
# - duplicate stream assignments;
# - invent a SimulationOrchestrator API.
# ============================================================

const ChallengeRuntimeBridge = preload(
	"res://core/execution/ChallengeRuntimeBridge.gd"
)

const ChallengeLegacyRuntimeOracle = preload(
	"res://core/execution/ChallengeLegacyRuntimeOracle.gd"
)

const C6FChallengeSchemaValidator = preload(
	"res://core/validation/C6FChallengeSchemaValidator.gd"
)

var failures: int = 0


func _init() -> void:
	print("[TEST] Running C6F0_1_7RuntimeBoundaryProofTest...")

	for id in [
		"001",
		"002",
		"003",
		"004",
		"005",
		"006",
		"007",
		"008",
		"009"
	]:
		_run_fixture(
			"res://challenges/CHALLENGE_%s.json" % id
		)

	if failures == 0:
		print(
			"[C6F0_1_7_RUNTIME_BOUNDARY_PROOF_SUITE] PASS"
		)
		quit(0)
	else:
		push_error(
			"[C6F0_1_7_RUNTIME_BOUNDARY_PROOF_SUITE] FAIL failures=%d"
			% failures
		)
		quit(1)


func _run_fixture(path: String) -> void:
	var file := FileAccess.open(path, FileAccess.READ)

	if file == null:
		_fail(path, "Unable to open fixture.")
		return

	var original_variant = JSON.parse_string(
		file.get_as_text()
	)

	if not original_variant is Dictionary:
		_fail(path, "Fixture JSON is not a Dictionary.")
		return

	var original: Dictionary = original_variant

	# ---------------------------------------------------------
	# A. LEGACY RUNTIME ORACLE
	# ---------------------------------------------------------

	var legacy_package: Dictionary = (
		ChallengeLegacyRuntimeOracle.run(original)
	)

	if not bool(legacy_package.get("valid", false)):
		_fail(
			path,
			"Legacy oracle failed: %s"
			% str(legacy_package.get("errors", []))
		)
		return

	var legacy_result: SimulationResult = (
		legacy_package.get("result")
	)

	if legacy_result == null:
		_fail(path, "Legacy oracle returned null SimulationResult.")
		return

	# ---------------------------------------------------------
	# B. EFFECTIVE CANONICAL RUNTIME
	#
	# run_effective_pipeline() performs:
	# V1 -> F1.1 -> Canonical V2 -> F3.1 -> F3.2 -> F3.3
	# ---------------------------------------------------------

	var effective_package: Dictionary = (
		ChallengeRuntimeBridge.run_effective_pipeline(original)
	)

	if not bool(effective_package.get("success", false)):
		_fail(
			path,
			"Effective runtime failed: %s"
			% str(effective_package.get("error", ""))
		)
		return

	var effective_context = effective_package.get("context")

	if effective_context == null:
		_fail(path, "Effective runtime returned null context.")
		return

	var effective_result: SimulationResult = (
		effective_context.simulation_result
	)

	if effective_result == null:
		_fail(
			path,
			"Effective runtime returned null SimulationResult."
		)
		return

	# ---------------------------------------------------------
	# C. CANONICAL V2 MUST EXIST AND BE SCHEMA VALID
	# ---------------------------------------------------------

	var canonical_v2: Dictionary = (
		effective_context.canonical_v2
	)

	if canonical_v2.is_empty():
		_fail(
			path,
			"Effective runtime produced an empty Canonical V2."
		)
		return

	var schema_result: Dictionary = (
		C6FChallengeSchemaValidator.validate_v2(
			canonical_v2
		)
	)

	if not bool(schema_result.get("is_valid", false)):
		_fail(
			path,
			"Canonical V2 schema invalid: %s"
			% str(schema_result.get("errors", []))
		)
		return

	# ---------------------------------------------------------
	# D. ABSOLUTE SIMULATION PARITY
	# ---------------------------------------------------------

	_compare_simulation_results(
		path,
		legacy_result,
		effective_result
	)


func _compare_simulation_results(
	path: String,
	legacy_result: SimulationResult,
	effective_result: SimulationResult
) -> void:

	if legacy_result.winning_frame != effective_result.winning_frame:
		_fail(
			path,
			"winning_frame mismatch: legacy=%d effective=%d"
			% [
				legacy_result.winning_frame,
				effective_result.winning_frame
			]
		)
		return

	if legacy_result.frames.size() != effective_result.frames.size():
		_fail(
			path,
			"frame count mismatch: legacy=%d effective=%d"
			% [
				legacy_result.frames.size(),
				effective_result.frames.size()
			]
		)
		return

	if abs(
		legacy_result.minimum_distance
		- effective_result.minimum_distance
	) > 0.000001:
		_fail(
			path,
			"minimum_distance mismatch: legacy=%.9f effective=%.9f"
			% [
				legacy_result.minimum_distance,
				effective_result.minimum_distance
			]
		)
		return

	if abs(
		legacy_result.score
		- effective_result.score
	) > 0.000001:
		_fail(
			path,
			"score mismatch: legacy=%.9f effective=%.9f"
			% [
				legacy_result.score,
				effective_result.score
			]
		)
		return

	# ---------------------------------------------------------
	# Deterministic SimulationResult metadata
	# ---------------------------------------------------------

	for key in [
		"initial_seed",
		"final_seed",
		"seed_used",
		"attempts",
		"rng_version"
	]:
		if not legacy_result.metadata.has(key):
			_fail(
				path,
				"Legacy result missing metadata.%s"
				% key
			)
			return

		if not effective_result.metadata.has(key):
			_fail(
				path,
				"Effective result missing metadata.%s"
				% key
			)
			return

		if legacy_result.metadata[key] != (
			effective_result.metadata[key]
		):
			_fail(
				path,
				"metadata.%s mismatch"
				% key
			)
			return

	# ---------------------------------------------------------
	# Frame-level deterministic parity
	# ---------------------------------------------------------

	for i in range(legacy_result.frames.size()):
		var legacy_frame: FrameSnapshot = (
			legacy_result.frames[i]
		)

		var effective_frame: FrameSnapshot = (
			effective_result.frames[i]
		)

		if legacy_frame == null or effective_frame == null:
			_fail(
				path,
				"Null FrameSnapshot at index %d" % i
			)
			return

		if (
			legacy_frame.position
			.distance_to(effective_frame.position)
			> 0.000001
		):
			_fail(
				path,
				"position mismatch at frame %d"
				% i
			)
			return

		if abs(
			legacy_frame.rotation
			- effective_frame.rotation
		) > 0.000001:
			_fail(
				path,
				"rotation mismatch at frame %d"
				% i
			)
			return

		if (
			legacy_frame.scale
			.distance_to(effective_frame.scale)
			> 0.000001
		):
			_fail(
				path,
				"scale mismatch at frame %d"
				% i
			)
			return

		if abs(
			legacy_frame.opacity
			- effective_frame.opacity
		) > 0.000001:
			_fail(
				path,
				"opacity mismatch at frame %d"
				% i
			)
			return


func _fail(path: String, message: String) -> void:
	failures += 1

	print(
		"[C6F0_1_7-B] FAIL %s -> %s"
		% [path, message]
	)