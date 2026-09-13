# res://tests/mechanics/catch/CatchMechanicIsolationTest.gd
class_name CatchMechanicIsolationTest
extends SceneTree

var registry: RNGStreamRegistry
var structural_rng: StructuralRNG
var challenge_config: Dictionary
var failures: int = 0

func _init() -> void:
	print("--- INICIANDO CATCH MECHANIC ISOLATION SUITE (C3-F-A) ---")
	_setup_environment()
	
	_test_lifecycle_pure_simulation()
	_test_determinism()
	_test_error_bubbling_unauthorized_stream_in_setup()
	_test_rng_independence()
	
	if failures == 0:
		print("[CATCH_V1_ISOLATION_SUITE] PASS")
		quit(0)
	else:
		print("[CATCH_V1_ISOLATION_SUITE] FAIL - Errores: ", failures)
		quit(1)

func _setup_environment() -> void:
	registry = RNGStreamRegistry.new()
	structural_rng = StructuralRNG.new(registry)
	challenge_config = {
		"difficulty": {
			"catch": {
				"catcher_origin": [540.0, 1700.0],
				"catcher_direction": [0.0, -1.0],
				"catcher_speed_base": 6.0,
				"target_origin": [540.0, 400.0],
				"target_direction": [0.0, 1.0],
				"target_speed_base": 2.5,
				"catch_radius": 45.0
			}
		}
	}

func _create_mechanic(allowed_streams: Array[int]) -> CatchMechanic:
	var m = CatchMechanic.new()
	var ctx_result = MechanicRNGContext.create(123456, "2.0", "CatchMechanic", allowed_streams, structural_rng, registry)
	
	if not ctx_result.is_valid:
		print("[FATAL] MechanicRNGContext.create() denegado. Error: ", ctx_result.error_code)
		failures += 1
		return null
		
	# ORDEN ESTRICTO: Context -> Setup -> Simulate
	m.set_rng_context(ctx_result.context)
	m.setup(challenge_config)
	return m

# --- FUNCIONES DE ASERCIÓN ---

func _assert(condition: bool, msg: String) -> void:
	if not condition:
		print("[FAIL] ", msg)
		failures += 1

# --- BATERÍA DE TESTS ---

func _test_lifecycle_pure_simulation() -> void:
	var m = _create_mechanic([100, 110, 120])
	if m == null: return
	
	_assert(m._is_setup, "setup() debería haber terminado exitosamente.")
	_assert(m._is_prepared, "setup() debería haber marcado _is_prepared = true para mecánica estructural.")
	
	# Eliminamos contexto RNG para asegurar pureza en simulación
	m.set_rng_context(null)
	
	var res = m.simulate(420, 123456, challenge_config)
	_assert(res != null, "simulate() no debe devolver null.")
	_assert(res.frames.size() == 420, "simulate() debe producir exactamente 420 frames.")
	_assert(res.winning_frame >= 0, "Debe calcular un winning_frame válido.")

func _test_determinism() -> void:
	var m1 = _create_mechanic([100, 110, 120])
	var m2 = _create_mechanic([100, 110, 120])
	if m1 == null or m2 == null: return
	
	var res1 = m1.simulate(420, 123456, challenge_config)
	var res2 = m2.simulate(420, 123456, challenge_config)
	
	_assert(res1.winning_frame == res2.winning_frame, "Determinismo: winning_frame idéntico.")
	_assert(res1.minimum_distance == res2.minimum_distance, "Determinismo: minimum_distance idéntico.")

func _test_error_bubbling_unauthorized_stream_in_setup() -> void:
	var m = CatchMechanic.new()
	# Autorizamos solo el stream 100 y 110 (falta deliberadamente el 120)
	var ctx_result = MechanicRNGContext.create(123456, "2.0", "CatchMechanic", [100, 110], structural_rng, registry)
	m.set_rng_context(ctx_result.context)
	
	# El error ahora ocurre estructuralmente en el setup
	m.setup(challenge_config)
	
	_assert(not m._is_setup, "setup() debe fallar y marcar _is_setup = false.")
	_assert(not m._is_prepared, "setup() debe fallar y marcar _is_prepared = false.")
	_assert(m._error_state == "RNG_CONSUMER_NOT_AUTHORIZED", "El error debe ser por consumo no autorizado.")
	
	var res = m.simulate(420, 123456, challenge_config)
	_assert(res.winning_frame == -1, "simulate() debe abortar si setup() falló.")
	_assert(res.metadata.get("error", "") == "RNG_CONSUMER_NOT_AUTHORIZED", "El error debe burbujear al SimulationResult.")

func _test_rng_independence() -> void:
	var m = _create_mechanic([100, 110, 120])
	if m == null: return
	var res = m.simulate(420, 123456, challenge_config)
	
	var dt = res.metadata.get("delta_target", 0.0)
	var db = res.metadata.get("delta_bias", 0.0)
	var dpx = res.metadata.get("delta_phase_x", 0.0)
	
	_assert(dt >= -0.20 and dt <= 0.20, "delta_target en rango.")
	_assert(db >= -0.15 and db <= 0.15, "delta_bias en rango.")
	_assert(dpx >= -50.0 and dpx <= 50.0, "delta_phase_x en rango.")