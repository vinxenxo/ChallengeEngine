class_name CatchMechanicIsolationTest
extends SceneTree

var failures: int = 0

func _init() -> void:
	print("--- INICIANDO CATCH MECHANIC ISOLATION SUITE ---")

	_test_determinism()
	_test_rng_bounds_and_streams()
	_test_winning_frame_argmin()
	_test_captured_and_score()
	_test_unauthorized_stream_bubbling()

	if failures == 0:
		print("[CATCH_V1_ISOLATION_SUITE] PASS")
		quit(0)
	else:
		print("[CATCH_V1_ISOLATION_SUITE] FAIL - Errores: ", failures)
		quit(1)

func _test_determinism() -> void:
	var config = _get_default_config()
	var reg = RNGStreamRegistry.new()
	var s_rng = StructuralRNG.new(reg)

	var ctx1 = MechanicRNGContext.create(884422, "2.0", "CatchMechanic", [100, 110, 120], s_rng, reg)
	var mech1 = CatchMechanic.new()
	mech1.setup(config)
	mech1.set_rng_context(ctx1.context)
	var res1 = mech1.simulate(420, 884422, config)

	var ctx2 = MechanicRNGContext.create(884422, "2.0", "CatchMechanic", [100, 110, 120], s_rng, reg)
	var mech2 = CatchMechanic.new()
	mech2.setup(config)
	mech2.set_rng_context(ctx2.context)
	var res2 = mech2.simulate(420, 884422, config)

	if res1.winning_frame != res2.winning_frame or not is_equal_approx(res1.minimum_distance, res2.minimum_distance):
		print("[FAIL] _test_determinism: Los resultados no son deterministas para la semilla 884422.")
		failures += 1
	else:
		print("[PASS] _test_determinism")

func _test_rng_bounds_and_streams() -> void:
	var config = _get_default_config()
	var reg = RNGStreamRegistry.new()
	var s_rng = StructuralRNG.new(reg)

	var ctx = MechanicRNGContext.create(999, "2.0", "CatchMechanic", [100, 110, 120], s_rng, reg)
	var mech = CatchMechanic.new()
	mech.setup(config)
	mech.set_rng_context(ctx.context)
	var res = mech.simulate(420, 999, config)

	var dt = res.metadata.get("delta_target", 0.0)
	var db = res.metadata.get("delta_bias", 0.0)
	var dp = res.metadata.get("delta_phase_x", 0.0)

	if dt < -0.20 or dt > 0.20 or db < -0.15 or db > 0.15 or dp < -50.0 or dp > 50.0:
		print("[FAIL] _test_rng_bounds_and_streams: Valores RNG fuera de los rangos contractuales (100, 110, 120).")
		failures += 1
	else:
		print("[PASS] _test_rng_bounds_and_streams")

func _test_winning_frame_argmin() -> void:
	var config = _get_default_config()
	var reg = RNGStreamRegistry.new()
	var s_rng = StructuralRNG.new(reg)

	var ctx = MechanicRNGContext.create(111, "2.0", "CatchMechanic", [100, 110, 120], s_rng, reg)
	var mech = CatchMechanic.new()
	mech.setup(config)
	mech.set_rng_context(ctx.context)
	var res = mech.simulate(420, 111, config)

	var wf = res.winning_frame
	var min_d = res.minimum_distance

	var t0 = Vector2(540.0, 400.0) + Vector2(res.metadata["delta_phase_x"], 0.0)
	var c0 = Vector2(540.0, 1700.0)
	var dt = res.metadata["delta_target"]
	var db = res.metadata["delta_bias"]
	var vt = Vector2(0.0, 1.0).normalized() * (2.5 * (1.0 + dt))
	var vc = Vector2(0.0, -1.0).normalized() * (6.0 * (1.0 + db))

	var calculated_min = INF
	var calculated_wf = -1
	for f in range(420):
		var dist = (c0 + vc * float(f)).distance_to(t0 + vt * float(f))
		if dist < calculated_min:
			calculated_min = dist
			calculated_wf = f

	if wf != calculated_wf or not is_equal_approx(min_d, calculated_min):
		print("[FAIL] _test_winning_frame_argmin: El argmin discreto o minimum_distance difiere de la analítica.")
		failures += 1
	else:
		print("[PASS] _test_winning_frame_argmin")

func _test_captured_and_score() -> void:
	var config = _get_default_config()
	var reg = RNGStreamRegistry.new()
	var s_rng = StructuralRNG.new(reg)

	var ctx = MechanicRNGContext.create(222, "2.0", "CatchMechanic", [100, 110, 120], s_rng, reg)
	var mech = CatchMechanic.new()
	mech.setup(config)
	mech.set_rng_context(ctx.context)
	var res = mech.simulate(420, 222, config)

	var radius = 45.0
	var expected_captured = res.minimum_distance <= radius
	var actual_captured = res.metadata.get("captured", false)

	if expected_captured != actual_captured:
		print("[FAIL] _test_captured_and_score: Inconsistencia en el indicador booleano de captura.")
		failures += 1
	else:
		print("[PASS] _test_captured_and_score")

func _test_unauthorized_stream_bubbling() -> void:
	var config = _get_default_config()
	var reg = RNGStreamRegistry.new()
	var s_rng = StructuralRNG.new(reg)

	var ctx_result = MechanicRNGContext.create(
		333,
		"2.0",
		"CatchMechanic",
		[100],
		s_rng,
		reg
	)

	if not ctx_result.is_valid:
		print(
			"[FAIL] _test_unauthorized_stream_bubbling: "
			+ "La capability válida para el stream 100 fue rechazada: "
			+ str(ctx_result.error_code)
		)
		failures += 1
		return

	var mech = CatchMechanic.new()
	mech.setup(config)
	mech.set_rng_context(ctx_result.context)

	var res = mech.simulate(420, 333, config)

	# El stream 110 debe provocar el error durante simulate().
	if ctx_result.context.error_state == "OK":
		print(
			"[FAIL] _test_unauthorized_stream_bubbling: "
			+ "Stream 110 fue consumido sin registrar error."
		)
		failures += 1
		return

	# La simulación debe abortar limpiamente.
	if res == null:
		print(
			"[PASS] _test_unauthorized_stream_bubbling "
			+ "(Simulación abortada limpiamente)"
		)
		return

	if res.winning_frame == -1:
		print(
			"[PASS] _test_unauthorized_stream_bubbling "
			+ "(Simulación abortada limpiamente)"
		)
		return

	print(
		"[FAIL] _test_unauthorized_stream_bubbling: "
		+ "La simulación continuó después del error DDI."
	)
	failures += 1

func _get_default_config() -> Dictionary:
	return {
		"challenge_id": "CHALLENGE_006",
		"mechanic": "catch_v1",
		"generation": {"seed": 884422, "rng_version": "2.0"},
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