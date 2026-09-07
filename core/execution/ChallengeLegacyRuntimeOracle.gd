class_name ChallengeLegacyRuntimeOracle
extends RefCounted

## C6-F4.3 — Isolated legacy runtime oracle.
##
## This class intentionally preserves the F3.3 legacy orchestration semantics
## for regression auditing. It is NEVER the production execution path.
##
## Non-responsibilities:
## - no authoring migration;
## - no presentation/rendering;
## - no changes to mechanic mathematics;
## - no alternate RNG implementation.

const MechanicRegistry = preload("res://core/mechanics/MechanicRegistry.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")
const StructuralRNG = preload("res://core/deterministic/StructuralRNG.gd")
const CosmeticRNG = preload("res://core/deterministic/CosmeticRNG.gd")
const MechanicRNGContext = preload("res://core/deterministic/MechanicRNGContext.gd")
const PresentationRNGContext = preload("res://core/deterministic/PresentationRNGContext.gd")

static func run(legacy_config: Dictionary) -> Dictionary:
	var timeline := VideoTimeline.new(legacy_config.get("video", {}))
	return run_with_timeline(legacy_config, timeline)

static func run_with_timeline(
	legacy_config: Dictionary,
	timeline: VideoTimeline
) -> Dictionary:
	if legacy_config.is_empty() or timeline == null:
		return {
			"valid": false,
			"error_code": "LEGACY_ORACLE_INPUT_INVALID",
			"message": "Legacy oracle input or timeline is invalid.",
			"errors": ["Missing legacy configuration or timeline."]
		}

	var rng_registry := RNGStreamRegistry.new()
	var structural_rng := StructuralRNG.new(rng_registry)
	var cosmetic_rng := CosmeticRNG.new(rng_registry)

	var mechanic_id: String = str(legacy_config.get("mechanic", ""))
	var mechanic: ChallengeMechanic = MechanicRegistry.create_mechanic(mechanic_id)

	if mechanic == null:
		return {
			"valid": false,
			"error_code": "UNKNOWN_MECHANIC_ID",
			"message": "La mecánica requerida '%s' no está registrada en MechanicRegistry." % mechanic_id,
			"errors": ["Unregistered mechanic_id: %s" % mechanic_id]
		}

	var generation_config: Dictionary = legacy_config.get("generation", {})
	var initial_seed: int = int(generation_config.get("seed", 12345))
	var rng_version: String = str(generation_config.get("rng_version", "1.0"))
	var current_seed: int = initial_seed

	var is_v2: bool = rng_version == "2.0"

	var pilot_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_TRAJECTORY,
		RNGStreamRegistry.STREAM_CONTROL
	]
	var parking_v2_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_PARKING_DODGE,
		RNGStreamRegistry.STREAM_PARKING_SAVE,
		RNGStreamRegistry.STREAM_PARKING_OVERSHOOT,
		RNGStreamRegistry.STREAM_PARKING_STEERING
	]
	var hit_v1_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_HIT_SPEED_VARIANCE,
		RNGStreamRegistry.STREAM_HIT_TRAJECTORY_NOISE,
		RNGStreamRegistry.STREAM_HIT_TARGET_OFFSET
	]
	var catch_v1_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_CATCH_TARGET_MOTION,
		RNGStreamRegistry.STREAM_CATCH_PURSUER_BIAS,
		RNGStreamRegistry.STREAM_CATCH_INITIAL_PHASE
	]
	var find_v1_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_FIND_SPATIAL_PLACEMENT,
		RNGStreamRegistry.STREAM_FIND_TOPOLOGY_GENERATION,
		RNGStreamRegistry.STREAM_FIND_SCANNER_TRAJECTORY,
		RNGStreamRegistry.STREAM_FIND_TARGET_DRIFT
	]

	var attempts: int = 0
	const MAX_ATTEMPTS: int = 100

	var sim_result: SimulationResult = null
	var sim_validation: ValidationResult = null

	while attempts < MAX_ATTEMPTS:
		attempts += 1
		var context_result = null

		if is_v2:
			match mechanic_id.to_lower():
				"pilot":
					context_result = _create_mechanic_rng_context(
						current_seed, "PilotMechanic", pilot_allowed_streams,
						structural_rng, rng_registry
					)
				"parking_v2":
					context_result = _create_mechanic_rng_context(
						current_seed, "ParkingMechanic", parking_v2_allowed_streams,
						structural_rng, rng_registry
					)
				"hit_v1":
					context_result = _create_mechanic_rng_context(
						current_seed, "HitMechanic", hit_v1_allowed_streams,
						structural_rng, rng_registry
					)
				"catch_v1":
					context_result = _create_mechanic_rng_context(
						current_seed, "CatchMechanic", catch_v1_allowed_streams,
						structural_rng, rng_registry
					)
				"find_v1":
					context_result = _create_mechanic_rng_context(
						current_seed, "FindMechanic", find_v1_allowed_streams,
						structural_rng, rng_registry
					)
				"choose_v1":
					context_result = _create_mechanic_rng_context(
						current_seed, "ChooseMechanic", [],
						structural_rng, rng_registry
					)
				"count_v1":
					context_result = _create_mechanic_rng_context(
						current_seed, "CountMechanic", [],
						structural_rng, rng_registry
					)
				_:
					return {
						"valid": false,
						"error_code": "RNG_CONTEXT_INVALID",
						"message": "No existe contrato RNG V2.0 para la mecánica '%s'." % mechanic_id,
						"errors": ["Missing V2.0 mechanic RNG contract: %s" % mechanic_id]
					}

			if not context_result.is_valid:
				return {
					"valid": false,
					"error_code": str(context_result.error_code),
					"message": "No se pudo crear la capability RNG de la mecánica.",
					"errors": [str(context_result.error_code)]
				}

			mechanic.set_rng_context(context_result.context)

		mechanic.setup(legacy_config)
		if not mechanic._is_setup or mechanic._error_state != "OK":
			current_seed = lcg_next_seed(current_seed)
			continue

		if mechanic.requires_temporal_preparation():
			mechanic.prepare(timeline.game_frames)
			if not mechanic._is_prepared or mechanic._error_state != "OK":
				current_seed = lcg_next_seed(current_seed)
				continue

		var test_result: SimulationResult = mechanic.simulate(
			timeline.game_frames,
			current_seed,
			legacy_config
		)

		if is_v2 and mechanic_id.to_lower() in [
			"pilot", "parking_v2", "hit_v1", "catch_v1", "find_v1", "choose_v1", "count_v1"
		] and context_result.context.error_state != "OK":
			return {
				"valid": false,
				"error_code": "MECHANIC_SIMULATION_ERROR",
				"message": "El contexto RNG reportó un error durante la simulación.",
				"errors": [str(context_result.context.error_state)]
			}

		var contract_check: Dictionary = test_result.validate_contract(timeline.game_frames)
		if not bool(contract_check.get("is_valid", false)):
			return {
				"valid": false,
				"error_code": str(contract_check.get("error_code", "SIMULATION_CONTRACT_VIOLATION")),
				"message": str(contract_check.get("message", "")),
				"errors": [str(contract_check.get("message", ""))]
			}

		SimulationMetricsResolver.resolve_metrics(test_result)
		if test_result.error_state != "OK":
			return {
				"valid": false,
				"error_code": test_result.error_state,
				"message": "Fallo en la resolución de métricas: %s" % test_result.error_state,
				"errors": [test_result.error_state]
			}

		WinningFrameDetector.analyze_and_score(test_result)
		var validation: ValidationResult = ChallengeValidator.validate(
			test_result,
			timeline.hook_frames,
			timeline.game_frames
		)

		if validation.is_valid:
			sim_result = test_result
			sim_validation = validation
			break

		current_seed = lcg_next_seed(current_seed)

	if sim_result == null or sim_validation == null:
		return {
			"valid": false,
			"error_code": "NO_VALID_SIMULATION",
			"message": "No se encontró una simulación válida que cumpliera los criterios narrativos tras %d intentos." % attempts,
			"errors": ["Exhausted %d seed attempts without finding a valid simulation." % attempts]
		}

	sim_result.metadata["initial_seed"] = initial_seed
	sim_result.metadata["final_seed"] = current_seed
	sim_result.metadata["seed_used"] = current_seed
	sim_result.metadata["attempts"] = attempts
	sim_result.metadata["rng_version"] = rng_version

	return {
		"valid": true,
		"result": sim_result,
		"validation": sim_validation,
		"timeline": timeline,
		"errors": []
	}

static func _create_mechanic_rng_context(
	seed: int,
	consumer_id: String,
	allowed_streams: Array[int],
	structural_rng: StructuralRNG,
	rng_registry: RNGStreamRegistry
):
	return MechanicRNGContext.create(
		seed,
		"2.0",
		consumer_id,
		allowed_streams,
		structural_rng,
		rng_registry
	)

static func _create_presentation_rng_context(
	seed: int,
	consumer_id: String,
	allowed_streams: Array[int],
	cosmetic_rng: CosmeticRNG,
	rng_registry: RNGStreamRegistry
):
	return PresentationRNGContext.create(
		seed,
		"2.0",
		consumer_id,
		allowed_streams,
		cosmetic_rng,
		rng_registry
	)

static func lcg_next_seed(seed: int) -> int:
	return int((seed * 1103515245 + 12345) & 0x7fffffff)
