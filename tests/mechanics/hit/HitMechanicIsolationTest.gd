# res://tests/mechanics/hit/HitMechanicIsolationTest.gd
class_name HitMechanicIsolationTest
extends SceneTree

var registry: RNGStreamRegistry
var structural_rng: StructuralRNG
var challenge_config: Dictionary
var failures: int = 0

func _init() -> void:
	print("--- INICIANDO HIT MECHANIC ISOLATION SUITE (C3-B2) ---")
	_setup_environment()
	
	_test_exact_420_frames()
	_test_determinism()
	_test_rng_bounds_and_application()
	_test_trajectory_noise_only_on_y()
	_test_winning_frame_is_first_argmin()
	_test_score_calculation()
	_test_close_calls_excludes_winning_frame()
	_test_error_bubbling_unauthorized_stream_in_prepare()
	_test_pure_simulation_without_rng_context()
	
	if failures == 0:
		print("[HIT_V1_ISOLATION_SUITE] PASS")
		quit(0)
	else:
		print("[HIT_V1_ISOLATION_SUITE] FAIL - Errores: ", failures)
		quit(1)

func _setup_environment() -> void:
	registry = RNGStreamRegistry.new()
	structural_rng = StructuralRNG.new(registry)
	challenge_config = {
		"difficulty": {
			"hit": {
				"origin": [540.0, 1500.0],
				"target": [540.0, 300.0],
				"speed_base": 3.5,
				"hitbox_radius": 30.0
			}
		}
	}

func _create_mechanic(allowed_streams: Array[int]) -> HitMechanic:
	var m = HitMechanic.new()
	var ctx_result = MechanicRNGContext.create(998877, "2.0", "HitMechanic", allowed_streams, structural_rng, registry)
	
	if not ctx_result.is_valid:
		print("[FATAL] MechanicRNGContext.create() denegado. Error: ", ctx_result.error_code)
		failures += 1
		return null
		
	m.set_rng_context(ctx_result.context)
	m.setup(challenge_config)
	m.prepare(420)
	return m

# --- FUNCIONES DE ASERCIÓN ---

func _assert(condition: bool, msg: String) -> void:
	if not condition:
		print("[FAIL] ", msg)
		failures += 1

func _assert_eq(actual, expected, msg: String) -> void:
	if actual != expected:
		print("[FAIL] ", msg, " | Esperado: ", expected, " | Actual: ", actual)
		failures += 1

func _assert_approx(actual: float, expected: float, tol: float, msg: String) -> void:
	if abs(actual - expected) > tol:
		print("[FAIL] ", msg, " | Esperado aprox: ", expected, " | Actual: ", actual)
		failures += 1

# --- BATERÍA DE TESTS ---

func _test_exact_420_frames() -> void:
	var m = _create_mechanic([70, 80, 90])
	if m == null: return
	var res = m.simulate(420, 998877, challenge_config)
	if res == null: _assert(false, "simulate() devolvió null"); return
	_assert_eq(res.frames.size(), 420, "Debe generar exactamente 420 FrameSnapshots")

func _test_determinism() -> void:
	var m1 = _create_mechanic([70, 80, 90])
	if m1 == null: return
	var res1 = m1.simulate(420, 998877, challenge_config)
	
	var m2 = _create_mechanic([70, 80, 90])
	var res2 = m2.simulate(420, 998877, challenge_config)
	if res1 == null or res2 == null: _assert(false, "simulate() devolvió null"); return
	
	_assert_eq(res1.winning_frame, res2.winning_frame, "El winning_frame debe ser idéntico entre ejecuciones")
	_assert_eq(res1.minimum_distance, res2.minimum_distance, "La distancia mínima debe ser idéntica")
	_assert_eq(res1.metadata["impact_velocity"], res2.metadata["impact_velocity"], "La velocidad debe ser idéntica")

func _test_rng_bounds_and_application() -> void:
	var m = _create_mechanic([70, 80, 90])
	if m == null: return
	var res = m.simulate(420, 998877, challenge_config)
	if res == null: return
	
	var v: float = res.metadata["impact_velocity"]
	_assert(v >= 2.8 and v <= 4.2, "Velocidad final debe respetar el stream 70 multiplicativo")
	
	var dx = res.metadata["target_prime_x"] - 540.0
	var dy = res.metadata["target_prime_y"] - 300.0
	_assert(dx >= -60.0 and dx <= 60.0, "Offset X (Stream 90) debe estar en [-60, 60]")
	_assert(dy >= -60.0 and dy <= 60.0, "Offset Y (Stream 90) debe estar en [-60, 60]")

func _test_trajectory_noise_only_on_y() -> void:
	var m = _create_mechanic([70, 80, 90])
	if m == null: return
	var res = m.simulate(420, 998877, challenge_config)
	if res == null: return
	
	var origin = Vector2(540.0, 1500.0)
	var target_prime = Vector2(res.metadata["target_prime_x"], res.metadata["target_prime_y"])
	var u = (target_prime - origin).normalized()
	var v = res.metadata["impact_velocity"]
	
	for f in range(420):
		var pos = res.frames[f].position
		var expected_base_x = origin.x + (u.x * v * float(f))
		var expected_base_y = origin.y + (u.y * v * float(f))
		
		_assert_approx(pos.x, expected_base_x, 0.0001, "El eje X no debe tener ruido de trayectoria en frame " + str(f))
		
		var noise_y = pos.y - expected_base_y
		_assert(noise_y >= -4.01 and noise_y <= 4.01, "El ruido en Y debe estar dentro de [-4.0, 4.0] en frame " + str(f))

func _test_winning_frame_is_first_argmin() -> void:
	var m = _create_mechanic([70, 80, 90])
	if m == null: return
	var res = m.simulate(420, 998877, challenge_config)
	if res == null: return
	
	var wf = res.winning_frame
	var min_dist = res.minimum_distance
	var target_prime = Vector2(res.metadata["target_prime_x"], res.metadata["target_prime_y"])
	
	for i in range(wf):
		var df = res.frames[i].position.distance_to(target_prime)
		_assert(df > min_dist, "El winning_frame debe ser el PRIMER argmin. Frame " + str(i) + " tiene dist <= min_dist")

func _test_score_calculation() -> void:
	var m = _create_mechanic([70, 80, 90])
	if m == null: return
	var res = m.simulate(420, 998877, challenge_config)
	if res == null: return
	
	var score = res.score
	var dist = res.minimum_distance
	var expected_score = clampf(1.0 - (dist / 30.0), 0.0, 1.0)
	_assert_approx(score, expected_score, 0.0001, "Score debe cumplir la fórmula clamp(1 - dist/radius)")

func _test_close_calls_excludes_winning_frame() -> void:
	var m = _create_mechanic([70, 80, 90])
	if m == null: return
	var res = m.simulate(420, 998877, challenge_config)
	if res == null: return
	
	var wf = res.winning_frame
	var target_prime = Vector2(res.metadata["target_prime_x"], res.metadata["target_prime_y"])
	var radius: float = 30.0
	
	var raw_close_calls: int = 0
	var wf_is_hit: bool = false
	
	for f in range(res.frames.size()):
		if res.frames[f].position.distance_to(target_prime) <= radius:
			raw_close_calls += 1
			if f == wf:
				wf_is_hit = true
				
	var expected_close_calls = raw_close_calls - 1 if wf_is_hit else raw_close_calls
	_assert_eq(res.metadata["close_calls"], expected_close_calls, "close_calls debe excluir explícitamente el winning_frame")

func _test_error_bubbling_unauthorized_stream_in_prepare() -> void:
	# Contexto SIN Stream 80 (autoriza solo 70 y 90)
	var m = HitMechanic.new()
	var ctx_result = MechanicRNGContext.create(998877, "2.0", "HitMechanic", [70, 90], structural_rng, registry)
	m.set_rng_context(ctx_result.context)
	m.setup(challenge_config)
	m.prepare(420)
	
	_assert(m._is_prepared == false, "prepare() debe marcar _is_prepared como false ante stream no autorizado")
	_assert(m._error_state != "OK", "Debe registrar un estado de error por consumo no autorizado (Stream 80) en prepare()")

func _test_pure_simulation_without_rng_context() -> void:
	var m = _create_mechanic([70, 80, 90])
	if m == null: return
	
	# Anulamos el contexto RNG tras prepare() para demostrar simulación puramente determinista sin él
	m.set_rng_context(null)
	var res = m.simulate(420, 998877, challenge_config)
	
	_assert(res != null and res.frames.size() == 420, "simulate() debe completarse con éxito sin contexto RNG gracias a los datos congelados en prepare()")