extends SceneTree

const REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")
const STRUCTURAL = preload("res://core/deterministic/StructuralRNG.gd")
const COSMETIC = preload("res://core/deterministic/CosmeticRNG.gd")
const MECH_CTX = preload("res://core/deterministic/MechanicRNGContext.gd")
const PRES_CTX = preload("res://core/deterministic/PresentationRNGContext.gd")

# Mock local para simular un fallo en tiempo de ejecución de la fachada con Context válido
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
	_run_architecture_tests(failures)

	if failures.is_empty():
		print("[RNG_ARCHITECTURE_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[RNG_ARCHITECTURE_SUITE] FAIL count=%d" % failures.size())
		quit(1)

func _run_architecture_tests(failures: Array[String]) -> void:
	var registry = REGISTRY.new()
	var structural = STRUCTURAL.new(registry)
	var cosmetic = COSMETIC.new(registry)
	
	# TEST 1: Creación Válida vía Factory
	var mech_res = MECH_CTX.create(12345, "2.0", "PilotMechanic", [REGISTRY.STREAM_TRAJECTORY, REGISTRY.STREAM_CONTROL], structural, registry)
	if not mech_res.is_valid:
		failures.append("Test 1 Failed: Contexto estructural válido fue rechazado.")
	var mech_ctx = mech_res.context

	var pres_res = PRES_CTX.create(12345, "2.0", "PilotVisuals", [REGISTRY.STREAM_PARTICLES], cosmetic, registry)
	if not pres_res.is_valid:
		failures.append("Test 1 Failed: Contexto de presentación válido fue rechazado.")

	# TEST 2: Registry rechaza stream desconocido en scope local durante construcción
	var fake_res = MECH_CTX.create(12345, "2.0", "PilotMechanic", [999], structural, registry)
	if fake_res.is_valid or fake_res.error_code != "RNG_CONTEXT_INVALID":
		failures.append("Test 2 Failed: Falló al rechazar un stream no registrado. Código: %s" % fake_res.error_code)

	# TEST K: Capability Intersection (K2: Runtime Deny)
	var denied_val = mech_ctx.sample_float(REGISTRY.STREAM_PARTICLES, 5) 
	if mech_ctx.error_state != "RNG_CONSUMER_NOT_AUTHORIZED" or not is_nan(denied_val):
		failures.append("Test K2 Failed: Runtime no bloqueó stream fuera de scope local o no devolvió NAN.")

	# K3: Registry DENY en construcción
	var rogue_res = MECH_CTX.create(12345, "2.0", "HackerMechanic", [REGISTRY.STREAM_TRAJECTORY], structural, registry)
	if rogue_res.is_valid or rogue_res.error_code != "RNG_CONTEXT_INVALID":
		failures.append("Test K3 Failed: Construcción no bloqueó consumer no autorizado por Registry.")

	# TEST L: Validación Directa de Fachadas (Domain Isolation & Unregistered)
	var l1_val = structural.sample_float(12345, REGISTRY.STREAM_PARTICLES, 0)
	if not is_nan(l1_val) or structural.last_error != "RNG_DOMAIN_VIOLATION":
		failures.append("Test L1 Failed: StructuralRNG no bloqueó stream cosmético correctamente.")

	var l2_val = cosmetic.sample_float(12345, REGISTRY.STREAM_TRAJECTORY, 0)
	if not is_nan(l2_val) or cosmetic.last_error != "RNG_DOMAIN_VIOLATION":
		failures.append("Test L2 Failed: CosmeticRNG no bloqueó stream estructural correctamente.")

	var l3_val = structural.sample_float(12345, 999, 0)
	if not is_nan(l3_val) or structural.last_error != "RNG_STREAM_UNREGISTERED":
		failures.append("Test L3 Failed: StructuralRNG no detectó stream desconocido.")

	var l4_val = cosmetic.sample_float(12345, 999, 0)
	if not is_nan(l4_val) or cosmetic.last_error != "RNG_STREAM_UNREGISTERED":
		failures.append("Test L4 Failed: CosmeticRNG no detectó stream desconocido.")

	# TEST M: Inmutabilidad del Scope Array por Referencia
	var external_array: Array[int] = [REGISTRY.STREAM_TRAJECTORY]
	var mut_res = MECH_CTX.create(12345, "2.0", "PilotMechanic", external_array, structural, registry)
	external_array.append(REGISTRY.STREAM_PARTICLES)
	var mut_ctx = mut_res.context
	var mut_test_val = mut_ctx.sample_float(REGISTRY.STREAM_PARTICLES, 0)
	if mut_ctx.error_state != "RNG_CONSUMER_NOT_AUTHORIZED" or not is_nan(mut_test_val):
		failures.append("Test M Failed: El scope del contexto fue vulnerable a mutación externa o no devolvió NAN.")

	# TEST N: Inmutabilidad de RNGStreamDefinition desde el exterior
	var def = registry.get_definition(REGISTRY.STREAM_TRAJECTORY)
	var original_consumers_count = def.get_allowed_consumers().size()
	def.get_allowed_consumers().append("RogueComponent")
	var def_after = registry.get_definition(REGISTRY.STREAM_TRAJECTORY)
	if def_after.get_allowed_consumers().size() != original_consumers_count:
		failures.append("Test N Failed: RNGStreamDefinition permitió mutar su lista de consumidores externamente.")

	# TEST O: Facade Value Equivalence
	var seed_val = 987654
	if DeterministicLCG.sample_float(seed_val, REGISTRY.STREAM_TRAJECTORY, 42) != structural.sample_float(seed_val, REGISTRY.STREAM_TRAJECTORY, 42):
		failures.append("Test O1 Failed: Mismatch en StructuralRNG.sample_float")
	if DeterministicLCG.sample_integer(seed_val, REGISTRY.STREAM_TRAJECTORY, 42) != structural.sample_integer(seed_val, REGISTRY.STREAM_TRAJECTORY, 42):
		failures.append("Test O2 Failed: Mismatch en StructuralRNG.sample_integer")
	if DeterministicLCG.sample_float_range(seed_val, REGISTRY.STREAM_TRAJECTORY, 42, 0.0, 100.0) != structural.sample_float_range(seed_val, REGISTRY.STREAM_TRAJECTORY, 42, 0.0, 100.0):
		failures.append("Test O3 Failed: Mismatch en StructuralRNG.sample_float_range")
	if DeterministicLCG.sample_float(seed_val, REGISTRY.STREAM_PARTICLES, 15) != cosmetic.sample_float(seed_val, REGISTRY.STREAM_PARTICLES, 15):
		failures.append("Test O4 Failed: Mismatch en CosmeticRNG.sample_float")
	if DeterministicLCG.sample_integer(seed_val, REGISTRY.STREAM_PARTICLES, 15) != cosmetic.sample_integer(seed_val, REGISTRY.STREAM_PARTICLES, 15):
		failures.append("Test O5 Failed: Mismatch en CosmeticRNG.sample_integer")
	if DeterministicLCG.sample_float_range(seed_val, REGISTRY.STREAM_PARTICLES, 15, -50.0, 50.0) != cosmetic.sample_float_range(seed_val, REGISTRY.STREAM_PARTICLES, 15, -50.0, 50.0):
		failures.append("Test O6 Failed: Mismatch en CosmeticRNG.sample_float_range")

	# TEST U: Error State Coherence & Bubbling Validation
	# U1: Context local error & recovery
	var u_ctx_res = MECH_CTX.create(12345, "2.0", "PilotMechanic", [REGISTRY.STREAM_TRAJECTORY], structural, registry)
	var u_ctx = u_ctx_res.context
	var u1_val = u_ctx.sample_float(REGISTRY.STREAM_PARTICLES, 0)
	if u_ctx.error_state != "RNG_CONSUMER_NOT_AUTHORIZED" or not is_nan(u1_val):
		failures.append("Test U1 Failed: Context no registró error local o no devolvió NAN.")
	
	var u1_ok_val = u_ctx.sample_float(REGISTRY.STREAM_TRAJECTORY, 0)
	if u_ctx.error_state != "OK" or is_nan(u1_ok_val):
		failures.append("Test U1 Failed: Context error_state no se reseteó a 'OK' o devolvió inválido. Obtenido: %s" % u_ctx.error_state)

	# U2: Bubbling from facade failure through valid Context
	var failing_rng = FailingStructuralRNG.new(registry)
	var fail_ctx_res = MECH_CTX.create(12345, "2.0", "PilotMechanic", [REGISTRY.STREAM_TRAJECTORY], failing_rng, registry)
	if not fail_ctx_res.is_valid:
		failures.append("Test U2 Failed: No pudo crearse Context válido para bubbling.")
	else:
		var fail_ctx = fail_ctx_res.context
		var bubbled_val = fail_ctx.sample_float(REGISTRY.STREAM_TRAJECTORY, 0)
		if fail_ctx.error_state != "RNG_DOMAIN_VIOLATION" or not is_nan(bubbled_val):
			failures.append("Test U2 Failed: Context no propagó last_error de la fachada o no devolvió NAN. Obtenido: %s" % fail_ctx.error_state)

	# Direct Facade Coherence checks
	structural.sample_float(12345, REGISTRY.STREAM_PARTICLES, 0)
	if structural.last_error != "RNG_DOMAIN_VIOLATION":
		failures.append("Test U2 Failed: StructuralRNG last_error incorrecto.")
	structural.sample_float(12345, REGISTRY.STREAM_TRAJECTORY, 0)
	if structural.last_error != "OK":
		failures.append("Test U2 Failed: StructuralRNG last_error no se reseteó a 'OK'.")

	cosmetic.sample_float(12345, REGISTRY.STREAM_TRAJECTORY, 0)
	if cosmetic.last_error != "RNG_DOMAIN_VIOLATION":
		failures.append("Test U2 Failed: CosmeticRNG last_error incorrecto.")
	cosmetic.sample_float(12345, REGISTRY.STREAM_PARTICLES, 0)
	if cosmetic.last_error != "OK":
		failures.append("Test U2 Failed: CosmeticRNG last_error no se reseteó a 'OK'.")

	# TEST V: Parking V2 Production Streams Validation (Phase 0.3.2)
	var parking_streams = [
		REGISTRY.STREAM_PARKING_DODGE,
		REGISTRY.STREAM_PARKING_SAVE,
		REGISTRY.STREAM_PARKING_OVERSHOOT,
		REGISTRY.STREAM_PARKING_STEERING
	]
	
	for s_id in parking_streams:
		if not registry.is_registered(s_id):
			failures.append("Test V Failed: Stream %d is not registered." % s_id)
		else:
			var s_def = registry.get_definition(s_id)
			if s_def.get_domain() != REGISTRY.Domain.STRUCTURAL_MAIN:
				failures.append("Test V Failed: Stream %d domain is not STRUCTURAL_MAIN." % s_id)
			if not registry.is_consumer_authorized(s_id, "ParkingMechanic"):
				failures.append("Test V Failed: Consumer 'ParkingMechanic' not authorized for stream %d." % s_id)
				
	# Ensure legacy streams are intact
	if not registry.is_registered(REGISTRY.STREAM_TRAJECTORY) or not registry.is_registered(REGISTRY.STREAM_PARTICLES) or not registry.is_registered(REGISTRY.STREAM_CONTROL):
		failures.append("Test V Failed: Legacy Pilot streams (10, 20 or 1010) are missing or modified.")