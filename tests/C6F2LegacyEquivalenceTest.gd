# res://tests/C6F2LegacyEquivalenceTest.gd
extends SceneTree

const ADAPTER = preload("res://core/authoring/ChallengeMigrationAdapter.gd")
const SCHEMA = preload("res://core/validation/C6FChallengeSchemaValidator.gd")
const REGISTRY = preload("res://core/mechanics/MechanicRegistry.gd")
const RNG_REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")
const STRUCTURAL_RNG = preload("res://core/deterministic/StructuralRNG.gd")
const RNG_CONTEXT = preload("res://core/deterministic/MechanicRNGContext.gd")

var failures: int = 0

func _init() -> void:
	print("[TEST] Running C6F2LegacyEquivalenceTest...")

	var policy: Dictionary = {
		"authoring_version": "1.0.0",
		"default_engine_version": "0.1",
		"default_asset_family": "fam_garage_01",
		"default_asset_family_version": "1.0",
		"default_theme": "generic",
		"default_profile_id": "test_master_11s",
		"default_profile_version": "1.0",
		"default_mechanic_version": "1.0"
	}

	for id in ["001", "002", "003", "004", "005", "006", "007", "008", "009"]:
		_run_fixture("res://challenges/CHALLENGE_%s.json" % id, policy)

	if failures == 0:
		print("[C6F2_LEGACY_EQUIVALENCE_SUITE] PASS")
		quit(0)
	else:
		print("[C6F2_LEGACY_EQUIVALENCE_SUITE] FAIL failures=%d" % failures)
		quit(1)

func _run_fixture(path: String, policy: Dictionary) -> void:
	var original: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	if original.is_empty():
		_fail(path, "Unable to read JSON")
		return

	# 1. Reuse the frozen F1.1 migration API and policy contract.
	var migrated: Dictionary = ADAPTER.migrate_legacy_v1_to_v2(original, policy)
	if not bool(migrated.get("is_valid", false)):
		_fail(path, "F1.1 migration failed: %s" % str(migrated.get("errors", [])))
		return
	var canonical: Dictionary = migrated.get("config", {})

	# 2. Prove the canonical V2 remains schema-valid before F2 processing.
	var schema_result: Dictionary = SCHEMA.validate_v2(canonical)
	if not bool(schema_result.get("is_valid", false)):
		_fail(path, "Canonical schema failed: %s" % str(schema_result.get("errors", [])))
		return

	# 3. Treat the exact F1.1 simulation parameters as a passthrough authoring
	#    override set. This tests F2 resolver integration without changing legacy
	#    semantics or inventing mechanic-specific mappings.
	var simulation_variant: Variant = canonical.get("simulation", {})
	if not (simulation_variant is Dictionary):
		_fail(path, "Canonical simulation block missing")
		return
	var simulation: Dictionary = simulation_variant
	var parameters_variant: Variant = simulation.get("parameters", {})
	if not (parameters_variant is Dictionary):
		_fail(path, "Canonical simulation.parameters is not a Dictionary")
		return
	var overrides: Dictionary = parameters_variant.duplicate(true)

	var synthetic_profile: Dictionary = {
		"allowed_parameters": overrides.keys(),
		"base_parameters": {},
		"scaling": {}
	}
	var difficulty_variant: Variant = canonical.get("difficulty", {})
	var difficulty: Dictionary = difficulty_variant if difficulty_variant is Dictionary else {}
	var level: int = int(difficulty.get("level", 0))

	var resolve_result: Dictionary = DifficultyResolver.resolve(level, synthetic_profile, overrides)
	if not bool(resolve_result.get("success", false)):
		_fail(path, "F2 resolver rejected valid passthrough parameters: %s" % str(resolve_result.get("error", "")))
		return

	var effective: Dictionary = resolve_result.get("effective_parameters", {})
	if JSON.stringify(effective) != JSON.stringify(overrides):
		_fail(path, "Passthrough resolver changed legacy simulation parameters")
		return

	var canonical_for_runtime: Dictionary = canonical.duplicate(true)
	canonical_for_runtime["simulation"]["parameters"] = effective

	# 4. Reuse the frozen F1.1 canonical -> runtime API.
	var runtime: Dictionary = ADAPTER.canonical_v2_to_runtime_v1(canonical_for_runtime)

	# 5. Structural runtime equivalence remains mandatory.
	var expected: Dictionary = _effective_runtime_projection(original)
	var actual: Dictionary = _effective_runtime_projection(runtime)
	if JSON.stringify(expected) != JSON.stringify(actual):
		_fail(path, "Runtime projection differs after F2 passthrough")
		return

	# 6. Behavioral equivalence: execute the exact C3-C5 harness used by F1.1.
	if not _compare_simulation(path, original, runtime):
		return

func _effective_runtime_projection(cfg: Dictionary) -> Dictionary:
	var out: Dictionary = {}
	out["challenge_id"] = str(cfg.get("challenge_id", ""))
	out["mechanic"] = str(cfg.get("mechanic", ""))
	var generation: Dictionary = cfg.get("generation", {})
	out["generation"] = {
		"seed": int(generation.get("seed", 0)),
		"rng_version": str(generation.get("rng_version", "1.0"))
	}
	var video: Dictionary = cfg.get("video", {})
	out["video"] = {
		"fps": int(video.get("fps", 0)),
		"hook_duration": float(video.get("hook_duration", 0.0)),
		"game_duration": float(video.get("game_duration", 0.0)),
		"reveal_duration": float(video.get("reveal_duration", 0.0)),
		"cta_duration": float(video.get("cta_duration", 0.0))
	}
	out["difficulty"] = cfg.get("difficulty", {})
	out["content"] = cfg.get("content", {})
	return out

func _compare_simulation(path: String, a: Dictionary, b: Dictionary) -> bool:
	var mechanic_id: String = str(a.get("mechanic", ""))
	var a_video: Dictionary = a.get("video", {})
	var fps: int = int(a_video.get("fps", 60))
	var game_frames: int = int(round(float(a_video.get("game_duration", 7.0)) * fps))
	var a_generation: Dictionary = a.get("generation", {})
	var seed: int = int(a_generation.get("seed", 0))
	var rng_version: String = str(a_generation.get("rng_version", "1.0"))

	var ra: SimulationResult = _simulate_one(mechanic_id, game_frames, seed, rng_version, a)
	var rb: SimulationResult = _simulate_one(mechanic_id, game_frames, seed, rng_version, b)
	if ra == null or rb == null:
		return _fail(path, "Simulation setup unsupported/failed")

	if ra.winning_frame != rb.winning_frame:
		return _fail(path, "winning_frame changed: %d != %d" % [ra.winning_frame, rb.winning_frame])
	if ra.frames.size() != rb.frames.size():
		return _fail(path, "frame count changed")
	if not is_equal_approx(ra.score, rb.score):
		return _fail(path, "score changed: %f != %f" % [ra.score, rb.score])
	if not is_equal_approx(ra.minimum_distance, rb.minimum_distance):
		return _fail(path, "minimum_distance changed: %f != %f" % [ra.minimum_distance, rb.minimum_distance])
	if not is_equal_approx(ra.tolerance_threshold, rb.tolerance_threshold):
		return _fail(path, "tolerance_threshold changed: %f != %f" % [ra.tolerance_threshold, rb.tolerance_threshold])
	if ra.error_state != rb.error_state:
		return _fail(path, "error_state changed: %s != %s" % [ra.error_state, rb.error_state])
	if ra.is_self_scored != rb.is_self_scored:
		return _fail(path, "is_self_scored changed")
	if JSON.stringify(ra.metadata) != JSON.stringify(rb.metadata):
		return _fail(path, "metadata changed")

	for i in range(ra.frames.size()):
		var fa: FrameSnapshot = ra.frames[i]
		var fb: FrameSnapshot = rb.frames[i]
		if not fa.position.is_equal_approx(fb.position):
			return _fail(path, "frame %d position changed" % i)
		if not is_equal_approx(fa.rotation, fb.rotation):
			return _fail(path, "frame %d rotation changed" % i)
		if not fa.scale.is_equal_approx(fb.scale):
			return _fail(path, "frame %d scale changed" % i)
		if not is_equal_approx(fa.opacity, fb.opacity):
			return _fail(path, "frame %d opacity changed" % i)
		if fa.texture_index != fb.texture_index:
			return _fail(path, "frame %d texture_index changed" % i)
		if fa.variant_id != fb.variant_id:
			return _fail(path, "frame %d variant_id changed" % i)
		if JSON.stringify(fa.custom_data) != JSON.stringify(fb.custom_data):
			return _fail(path, "frame %d custom_data changed" % i)

	return true

func _simulate_one(mechanic_id: String, game_frames: int, seed: int, rng_version: String, cfg: Dictionary) -> SimulationResult:
	var mechanic: ChallengeMechanic = REGISTRY.create_mechanic(mechanic_id)
	if mechanic == null:
		return null

	if rng_version == "2.0":
		var registry: RNGStreamRegistry = RNG_REGISTRY.new()
		var structural: StructuralRNG = STRUCTURAL_RNG.new(registry)
		var streams: Array[int] = []
		var consumer: String = ""
		match mechanic_id:
			"pilot":
				streams = [10, 20]
				consumer = "PilotMechanic"
			"parking_v2":
				streams = [30, 40, 50, 60]
				consumer = "ParkingMechanic"
			"hit_v1":
				streams = [70, 80, 90]
				consumer = "HitMechanic"
			"catch_v1":
				streams = [100, 110, 120]
				consumer = "CatchMechanic"
			"find_v1":
				streams = [130, 140, 150, 160]
				consumer = "FindMechanic"
			_:
				streams = []

		if not streams.is_empty():
			var created = RNG_CONTEXT.create(seed, rng_version, consumer, streams, structural, registry)
			if not created.is_valid:
				return null
			var context_variant: Variant = created.context
			if context_variant == null:
				return null
			mechanic.set_rng_context(context_variant)

		mechanic.setup(cfg)

	if mechanic_id in ["pilot", "parking_v2", "hit_v1", "catch_v1", "find_v1", "choose_v1", "count_v1"]:
		mechanic.prepare(game_frames)
	else:
		mechanic.setup(cfg)

	return mechanic.simulate(game_frames, seed, cfg)

func _fail(path: String, message: String) -> bool:
	failures += 1
	print("[C6F2] FAIL %s -> %s" % [path, message])
	return false
