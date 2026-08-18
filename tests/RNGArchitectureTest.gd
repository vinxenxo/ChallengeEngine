extends SceneTree

const REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")
const STRUCTURAL = preload("res://core/deterministic/StructuralRNG.gd")
const COSMETIC = preload("res://core/deterministic/CosmeticRNG.gd")
const MECH_CTX = preload("res://core/deterministic/MechanicRNGContext.gd")
const PRES_CTX = preload("res://core/deterministic/PresentationRNGContext.gd")

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
	var _denied_val = mech_ctx.sample_float(REGISTRY.STREAM_PARTICLES, 5) 
	if mech_ctx.error_state != "RNG_CONSUMER_NOT_AUTHORIZED":
		failures.append("Test K2 Failed: Runtime no bloqueó stream fuera de scope local.")

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
	var external_array = [REGISTRY.STREAM_TRAJECTORY]
	var mut_res = MECH_CTX.create(12345, "2.0", "PilotMechanic", external_array, structural, registry)
	external_array.append(REGISTRY.STREAM_PARTICLES)
	var mut_ctx = mut_res.context
	var _mut_test_val = mut_ctx.sample_float(REGISTRY.STREAM_PARTICLES, 0)
	if mut_ctx.error_state != "RNG_CONSUMER_NOT_AUTHORIZED":
		failures.append("Test M Failed: El scope del contexto fue vulnerable a mutación externa.")

	# TEST N: Inmutabilidad de RNGStreamDefinition desde el exterior
	var def = registry.get_definition(REGISTRY.STREAM_TRAJECTORY)
	var original_consumers_count = def.get_allowed_consumers().size()
	def.get_allowed_consumers().append("RogueComponent")
	var def_after = registry.get_definition(REGISTRY.STREAM_TRAJECTORY)
	if def_after.get_allowed_consumers().size() != original_consumers_count:
		failures.append("Test N Failed: RNGStreamDefinition permitió mutar su lista de consumidores externamente.")

	# TEST O: Facade Value Equivalence (Primitiva LCG vs Fachadas - O1 a O6)
	var seed_val = 987654
	
	# O1: StructuralRNG.sample_float
	if DeterministicLCG.sample_float(seed_val, REGISTRY.STREAM_TRAJECTORY, 42) != structural.sample_float(seed_val, REGISTRY.STREAM_TRAJECTORY, 42):
		failures.append("Test O1 Failed: Mismatch en StructuralRNG.sample_float")
		
	# O2: StructuralRNG.sample_integer
	if DeterministicLCG.sample_integer(seed_val, REGISTRY.STREAM_TRAJECTORY, 42) != structural.sample_integer(seed_val, REGISTRY.STREAM_TRAJECTORY, 42):
		failures.append("Test O2 Failed: Mismatch en StructuralRNG.sample_integer")
		
	# O3: StructuralRNG.sample_float_range
	if DeterministicLCG.sample_float_range(seed_val, REGISTRY.STREAM_TRAJECTORY, 42, 0.0, 100.0) != structural.sample_float_range(seed_val, REGISTRY.STREAM_TRAJECTORY, 42, 0.0, 100.0):
		failures.append("Test O3 Failed: Mismatch en StructuralRNG.sample_float_range")

	# O4: CosmeticRNG.sample_float
	if DeterministicLCG.sample_float(seed_val, REGISTRY.STREAM_PARTICLES, 15) != cosmetic.sample_float(seed_val, REGISTRY.STREAM_PARTICLES, 15):
		failures.append("Test O4 Failed: Mismatch en CosmeticRNG.sample_float")

	# O5: CosmeticRNG.sample_integer
	if DeterministicLCG.sample_integer(seed_val, REGISTRY.STREAM_PARTICLES, 15) != cosmetic.sample_integer(seed_val, REGISTRY.STREAM_PARTICLES, 15):
		failures.append("Test O5 Failed: Mismatch en CosmeticRNG.sample_integer")

	# O6: CosmeticRNG.sample_float_range
	if DeterministicLCG.sample_float_range(seed_val, REGISTRY.STREAM_PARTICLES, 15, -50.0, 50.0) != cosmetic.sample_float_range(seed_val, REGISTRY.STREAM_PARTICLES, 15, -50.0, 50.0):
		failures.append("Test O6 Failed: Mismatch en CosmeticRNG.sample_float_range")