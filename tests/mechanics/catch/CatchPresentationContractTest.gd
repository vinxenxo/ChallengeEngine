# res://tests/mechanics/catch/CatchPresentationContractTest.gd
class_name CatchPresentationContractTest
extends SceneTree

var failures: int = 0

func _init() -> void:
	print("--- INICIANDO CATCH PRESENTATION CONTRACT SUITE (0.8.1) ---")

	_test_presentation_data_integrity()

	if failures == 0:
		print("[CATCH_PRESENTATION_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		print("[CATCH_PRESENTATION_CONTRACT_SUITE] FAIL - Errores: ", failures)
		quit(1)

func _test_presentation_data_integrity() -> void:
	var config = _get_default_config()
	var reg = RNGStreamRegistry.new()
	var s_rng = StructuralRNG.new(reg)
	
	# Aseguramos un registro temporal para que no falle la creación si se ejecuta suelto
	if not reg.is_registered(100):
		reg._register(100, "T_MOTION", reg.Domain.STRUCTURAL_SECONDARY, "", "0", "2.0", ["CatchMechanic"])
		reg._register(110, "P_BIAS", reg.Domain.STRUCTURAL_SECONDARY, "", "0", "2.0", ["CatchMechanic"])
		reg._register(120, "PHASE", reg.Domain.STRUCTURAL_SECONDARY, "", "0", "2.0", ["CatchMechanic"])

	var ctx = MechanicRNGContext.create(
		884422,
		"2.0",
		"CatchMechanic",
		[100, 110, 120],
		s_rng,
		reg
	)

	var mech = CatchMechanic.new()
	mech.set_rng_context(ctx.context)
	mech.setup(config)
	
	var total_frames = 420
	var res = mech.simulate(total_frames, 884422, config)

	if res == null or res.frames.size() != total_frames:
		print("[FAIL] La simulación no produjo 420 snapshots.")
		failures += 1
		return

	# Recreamos la cinemática analítica de forma independiente para certificar el contenido de cada frame
	var c0 = Vector2(540.0, 1700.0)
	var t0_prime = Vector2(540.0, 400.0) + Vector2(res.metadata["delta_phase_x"], 0.0)
	var v_c = Vector2(0.0, -1.0).normalized() * (6.0 * (1.0 + res.metadata["delta_bias"]))
	var v_t = Vector2(0.0, 1.0).normalized() * (2.5 * (1.0 + res.metadata["delta_target"]))

	var failed_frames = 0
	for f in range(total_frames):
		var snap: FrameSnapshot = res.frames[f]
		var expected_pc = c0 + (v_c * float(f))
		var expected_pt = t0_prime + (v_t * float(f))
		
		if not is_equal_approx(snap.position.x, expected_pc.x) or not is_equal_approx(snap.position.y, expected_pc.y):
			failed_frames += 1
			continue
			
		if not snap.custom_data.has("target_position"):
			failed_frames += 1
			continue
			
		var actual_pt = snap.custom_data["target_position"]
		if not is_equal_approx(actual_pt.x, expected_pt.x) or not is_equal_approx(actual_pt.y, expected_pt.y):
			failed_frames += 1
			continue

	if failed_frames > 0:
		print("[FAIL] Integridad de datos de presentación falló en ", failed_frames, " fotogramas.")
		failures += 1
	else:
		print("[PASS] _test_presentation_data_integrity (420 snapshots verificados)")

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