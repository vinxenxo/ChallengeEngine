# res://tests/ParkingMechanicV2IsolationTest.gd
extends SceneTree

const REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")
const STRUCTURAL = preload("res://core/deterministic/StructuralRNG.gd")
const COSMETIC = preload("res://core/deterministic/CosmeticRNG.gd")
const MECH_CTX = preload("res://core/deterministic/MechanicRNGContext.gd")
const PARKING_V2 = preload("res://core/mechanics/parking/ParkingMechanicV2.gd")

const CHALLENGE_PATH := "res://challenges/CHALLENGE_004.json"

const GAME_FRAMES: int = 420
const SEED: int = 314159
const FLOAT_EPSILON: float = 1e-12

class MutatedStructuralRNG extends StructuralRNG:
	var mutate_stream_id: int = -1

	func _init(registry: RNGStreamRegistry, p_mutate_stream_id: int) -> void:
		super(registry)
		mutate_stream_id = p_mutate_stream_id

	func sample_float(seed: int, stream_id: int, index: int) -> float:
		var value: float = super.sample_float(seed, stream_id, index)
		if last_error != "OK":
			return value
		if stream_id == mutate_stream_id:
			return 1.0 - value
		return value

	func sample_float_range(seed: int, stream_id: int, index: int, min_val: float, max_val: float) -> float:
		var normalized: float = sample_float(seed, stream_id, index)
		if last_error != "OK":
			return NAN
		return min_val + normalized * (max_val - min_val)

class FailingStructuralRNG extends StructuralRNG:
	func sample_float(seed: int, stream_id: int, index: int) -> float:
		last_error = "RNG_DOMAIN_VIOLATION"
		return NAN

	func sample_integer(seed: int, stream_id: int, index: int) -> int:
		last_error = "RNG_DOMAIN_VIOLATION"
		return -1

	func sample_float_range(seed: int, stream_id: int, index: int, min_val: float, max_val: float) -> float:
		last_error = "RNG_DOMAIN_VIOLATION"
		return NAN

func _initialize() -> void:
	var failures: Array[String] = []

	_run_capability_test(failures)
	_run_frame_contract_test(failures)
	_run_repeatability_test(failures)
	_run_cosmetic_invariance_test(failures)
	_run_structural_stream_independence_test(failures)
	_run_structural_reactivity_test(failures)
	_run_error_bubbling_test(failures)
	_run_pure_simulation_test(failures)

	if failures.is_empty():
		print("[PARKING_V2_ISOLATION_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[PARKING_V2_ISOLATION_SUITE] FAIL count=%d" % failures.size())
		quit(1)

func _load_config() -> Dictionary:
	var file: FileAccess = FileAccess.open(CHALLENGE_PATH, FileAccess.READ)
	if file == null:
		return {}

	var json: Variant = JSON.parse_string(file.get_as_text())
	if not (json is Dictionary):
		return {}

	var config: Dictionary = json
	if config.get("challenge_id", "") != "CHALLENGE_004": return {}
	if config.get("mechanic", "") != "parking_v2": return {}
	if config.get("mechanic_version", "") != "2.0": return {}

	var generation: Dictionary = config.get("generation", {})
	if generation.get("seed", -1) != SEED: return {}
	if generation.get("rng_version", "") != "2.0": return {}

	return config

func _create_context(registry: RNGStreamRegistry, structural: StructuralRNG) -> MechanicRNGContext:
	var creation_result = MECH_CTX.create(
		SEED, "2.0", "ParkingMechanic",
		[
			REGISTRY.STREAM_PARKING_DODGE,
			REGISTRY.STREAM_PARKING_SAVE,
			REGISTRY.STREAM_PARKING_OVERSHOOT,
			REGISTRY.STREAM_PARKING_STEERING
		],
		structural,
		registry
	)

	if not creation_result.is_valid:
		return null

	var context: MechanicRNGContext = creation_result.context
	return context

func _simulate_with_context(config: Dictionary, context: MechanicRNGContext) -> SimulationResult:
	var mechanic: ChallengeMechanic = PARKING_V2.new()
	mechanic.set_rng_context(context)
	mechanic.setup(config)
	mechanic.prepare(GAME_FRAMES)
	return mechanic.simulate(GAME_FRAMES, SEED, config)

func _run_capability_test(failures: Array[String]) -> void:
	var registry := REGISTRY.new()
	var structural := STRUCTURAL.new(registry)
	var context := _create_context(registry, structural)

	if context == null:
		failures.append("P1 Failed: ParkingMechanic capability could not be created.")

func _run_frame_contract_test(failures: Array[String]) -> void:
	var config := _load_config()
	if config.is_empty():
		failures.append("P2 Failed: CHALLENGE_004 could not be loaded or failed fixture assertions.")
		return

	var registry := REGISTRY.new()
	var structural := STRUCTURAL.new(registry)
	var context := _create_context(registry, structural)

	var result := _simulate_with_context(config, context)

	if context.error_state != "OK":
		failures.append("P2 Failed: RNG error during valid simulation: %s" % context.error_state)
		return

	if result.frames.size() != GAME_FRAMES:
		failures.append("P2 Failed: Expected %d frames, got %d." % [GAME_FRAMES, result.frames.size()])

	if result.metadata.get("mechanic", "") != "parking_v2":
		failures.append("P2 Failed: SimulationResult mechanic metadata is not parking_v2.")

	if result.metadata.get("rng_version", "") != "2.0":
		failures.append("P2 Failed: rng_version metadata is not 2.0.")

func _run_repeatability_test(failures: Array[String]) -> void:
	var config := _load_config()

	var registry_a := REGISTRY.new()
	var structural_a := STRUCTURAL.new(registry_a)
	var context_a := _create_context(registry_a, structural_a)
	var result_a := _simulate_with_context(config, context_a)

	var registry_b := REGISTRY.new()
	var structural_b := STRUCTURAL.new(registry_b)
	var context_b := _create_context(registry_b, structural_b)
	var result_b := _simulate_with_context(config, context_b)

	if not _simulation_results_equal(result_a, result_b):
		failures.append("P3 Failed: repeated simulations are not exactly identical.")

func _run_cosmetic_invariance_test(failures: Array[String]) -> void:
	var config := _load_config()

	var registry_a := REGISTRY.new()
	var structural_a := STRUCTURAL.new(registry_a)
	var result_a := _simulate_with_context(
		config,
		_create_context(registry_a, structural_a)
	)

	var cosmetic := COSMETIC.new(registry_a)
	registry_a._register(1020, "PARKING_TEST_CAMERA", REGISTRY.Domain.PRESENTATION, "Test", "frame", "2.0", ["ParkingTestCamera"])
	registry_a._register(1030, "PARKING_TEST_PARTICLES", REGISTRY.Domain.PRESENTATION, "Test", "entity", "2.0", ["ParkingTestParticles"])

	for i in range(500):
		cosmetic.sample_float(SEED, 1020, i)
		cosmetic.sample_float(SEED, 1030, 499 - i)

	var registry_b := REGISTRY.new()
	var structural_b := STRUCTURAL.new(registry_b)
	var result_b := _simulate_with_context(
		config,
		_create_context(registry_b, structural_b)
	)

	if not _simulation_results_equal(result_a, result_b):
		failures.append("P4 Failed: cosmetic RNG consumption altered Parking V2.")

func _run_structural_stream_independence_test(failures: Array[String]) -> void:
	var registry := REGISTRY.new()
	var structural := STRUCTURAL.new(registry)
	var expected: Dictionary = {}

	for stream_id in [REGISTRY.STREAM_PARKING_DODGE, REGISTRY.STREAM_PARKING_SAVE, REGISTRY.STREAM_PARKING_OVERSHOOT]:
		expected[stream_id] = structural.sample_float(SEED, stream_id, 0)

	var steering_baseline: Array[float] = []
	for i in range(GAME_FRAMES * 2):
		steering_baseline.append(structural.sample_float(SEED, REGISTRY.STREAM_PARKING_STEERING, i))

	structural.sample_float(SEED, REGISTRY.STREAM_PARKING_STEERING, 0)

	var actual_expected: Dictionary = {}
	for stream_id in [REGISTRY.STREAM_PARKING_OVERSHOOT, REGISTRY.STREAM_PARKING_DODGE, REGISTRY.STREAM_PARKING_SAVE]:
		actual_expected[stream_id] = structural.sample_float(SEED, stream_id, 0)

	for stream_id in expected.keys():
		if expected[stream_id] != actual_expected[stream_id]:
			failures.append("P5 Failed: Stream independence violated for stream %d." % stream_id)

	for i in range(GAME_FRAMES * 2):
		if structural.sample_float(SEED, REGISTRY.STREAM_PARKING_STEERING, i) != steering_baseline[i]:
			failures.append("P5 Failed: Steering stream changed at index %d." % i)
			break

func _run_structural_reactivity_test(failures: Array[String]) -> void:
	var config := _load_config()

	var registry_base := REGISTRY.new()
	var structural_base := STRUCTURAL.new(registry_base)
	var context_base := _create_context(registry_base, structural_base)
	var result_base := _simulate_with_context(config, context_base)

	var registry_mut := REGISTRY.new()
	var structural_mut := MutatedStructuralRNG.new(registry_mut, REGISTRY.STREAM_PARKING_STEERING)
	var context_mut := _create_context(registry_mut, structural_mut)
	var result_mut := _simulate_with_context(config, context_mut)

	if _simulation_results_equal(result_base, result_mut):
		failures.append("P6 Failed: mutation of PARKING_STEERING_NOISE did not alter the result.")

	var dodge_base = result_base.metadata.get("dodge_offset", 0.0)
	var dodge_mut = result_mut.metadata.get("dodge_offset", 0.0)
	if abs(dodge_base - dodge_mut) > FLOAT_EPSILON:
		failures.append("P6 Failed: PARKING_DODGE_OFFSET was incorrectly affected by steering noise mutation.")

func _run_error_bubbling_test(failures: Array[String]) -> void:
	var registry := REGISTRY.new()
	var failing_rng := FailingStructuralRNG.new(registry)
	var context := _create_context(registry, failing_rng)

	if context == null:
		failures.append("P7 Failed: Could not construct valid Parking V2 capability.")
		return

	var config := _load_config()
	var mechanic: ChallengeMechanic = PARKING_V2.new()
	mechanic.set_rng_context(context)
	mechanic.setup(config)
	mechanic.prepare(GAME_FRAMES)

	var result := mechanic.simulate(GAME_FRAMES, SEED, config)

	# El error debe haberse propagado desde el setup() o prepare() al _error_state de la mecanica.
	if mechanic._error_state != "RNG_DOMAIN_VIOLATION":
		failures.append("P7 Failed: RNG error did not bubble to mechanic _error_state. State: %s" % mechanic._error_state)

	if not result.frames.is_empty():
		failures.append("P7 Failed: failed simulation returned partial frames.")

func _run_pure_simulation_test(failures: Array[String]) -> void:
	var config := _load_config()
	var registry := REGISTRY.new()
	var structural := STRUCTURAL.new(registry)
	var context := _create_context(registry, structural)

	var mechanic: ChallengeMechanic = PARKING_V2.new()
	mechanic.set_rng_context(context)
	mechanic.setup(config)
	mechanic.prepare(GAME_FRAMES)

	# C3-D P8 - Extirpación transaccional: Anulamos la capacidad de RNG antes de simular
	mechanic.set_rng_context(null)
	var result := mechanic.simulate(GAME_FRAMES, SEED, config)

	if result == null or result.frames.size() != GAME_FRAMES:
		failures.append("P8 Failed: simulate() falló o exigió un contexto de RNG que ya no debería usar.")

func _simulation_results_equal(a: SimulationResult, b: SimulationResult) -> bool:
	if a.frames.size() != b.frames.size(): return false
	if a.winning_frame != b.winning_frame: return false
	if abs(a.minimum_distance - b.minimum_distance) > FLOAT_EPSILON: return false
	if abs(a.score - b.score) > FLOAT_EPSILON: return false

	var custom_keys := [
		"success_distance",
		"spatial_distance",
		"velocity",
		"angle_error",
		"steering",
		"braking",
		"dodge_offset",
		"save_offset",
		"overshoot_dist"
	]

	for i in range(a.frames.size()):
		var af := a.frames[i]
		var bf := b.frames[i]

		if af.position != bf.position: return false
		if af.rotation != bf.rotation: return false
		if af.scale != bf.scale: return false
		if af.opacity != bf.opacity: return false

		for key in custom_keys:
			var av = af.custom_data.get(key, null)
			var bv = bf.custom_data.get(key, null)
			if typeof(av) == TYPE_FLOAT or typeof(av) == TYPE_INT:
				if abs(float(av) - float(bv)) > FLOAT_EPSILON: return false
			else:
				if av != bv: return false

	return true