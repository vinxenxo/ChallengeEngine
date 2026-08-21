class_name FindMechanicIsolationTest
extends SceneTree

var failures: int = 0

func _init() -> void:
	print("--- INICIANDO FIND V1 ISOLATION SUITE (1.0.0-D RIGOROUS) ---")
	
	_test_full_spectrum_determinism()
	_test_close_call_episodic_logic()
	_test_pure_structural_isolation()

	if failures == 0:
		print("[FIND_V1_ISOLATION_SUITE] PASS")
		quit(0)
	else:
		print("[FIND_V1_ISOLATION_SUITE] FAIL - Errores: ", failures)
		quit(1)

func _get_test_config() -> Dictionary:
	return {
		"challenge_id": "FIND_TEST_001",
		"mechanic": "find_v1",
		"generation": {"seed": 998877, "rng_version": "2.0"},
		"difficulty": {
			"find": {
				"safe_area_x_min": 100.0,
				"safe_area_x_max": 980.0,
				"safe_area_y_min": 100.0,
				"safe_area_y_max": 1820.0,
				"scanner_cx": 540.0,
				"scanner_cy": 960.0,
				"scanner_ax": 300.0,
				"scanner_ay": 700.0,
				"scanner_wx": 0.02,
				"scanner_wy": 0.03,
				"capture_radius": 80.0,
				# Configuración que activa simultáneamente los 4 streams (130, 140, 150, 160)
				"distractor_count": 2,
				"target_drift_radius": 40.0,
				"target_drift_frequency": 0.015
			}
		}
	}

func _setup_registry() -> RNGStreamRegistry:
	var reg = RNGStreamRegistry.new()
	reg._register(130, "FIND_SPATIAL_PLACEMENT", reg.Domain.STRUCTURAL_SECONDARY, "", "0,1", "2.0", ["FindMechanic"])
	reg._register(140, "FIND_TOPOLOGY_GENERATION", reg.Domain.STRUCTURAL_SECONDARY, "", "2j,2j+1", "2.0", ["FindMechanic"])
	reg._register(150, "FIND_SCANNER_TRAJECTORY", reg.Domain.STRUCTURAL_SECONDARY, "", "0,1", "2.0", ["FindMechanic"])
	reg._register(160, "FIND_TARGET_DRIFT", reg.Domain.STRUCTURAL_SECONDARY, "", "0", "2.0", ["FindMechanic"])
	return reg

func _test_full_spectrum_determinism() -> void:
	var cfg = _get_test_config()
	var total_frames = 120
	var seed_val = 884422
	
	var reg1 = _setup_registry()
	var ctx1 = MechanicRNGContext.create(seed_val, "2.0", "FindMechanic", [130, 140, 150, 160], StructuralRNG.new(reg1), reg1)
	var mech1 = FindMechanic.new()
	mech1.set_rng_context(ctx1.context)
	mech1.setup(cfg)
	var res1 = mech1.simulate(total_frames, seed_val, cfg)
	
	var reg2 = _setup_registry()
	var ctx2 = MechanicRNGContext.create(seed_val, "2.0", "FindMechanic", [130, 140, 150, 160], StructuralRNG.new(reg2), reg2)
	var mech2 = FindMechanic.new()
	mech2.set_rng_context(ctx2.context)
	mech2.setup(cfg)
	var res2 = mech2.simulate(total_frames, seed_val, cfg)
	
	if res1.winning_frame != res2.winning_frame or \
	   not is_equal_approx(res1.score, res2.score) or \
	   not is_equal_approx(res1.minimum_distance, res2.minimum_distance) or \
	   res1.metadata["close_calls"] != res2.metadata["close_calls"] or \
	   res1.frames.size() != res2.frames.size():
		print("[FAIL] Determinismo roto: Resúmenes o close_calls divergen.")
		failures += 1
		return

	var d1: Array = res1.metadata["distractor_topology"]
	var d2: Array = res2.metadata["distractor_topology"]
	if d1.size() != d2.size() or not d1[0].is_equal_approx(d2[0]) or not d1[1].is_equal_approx(d2[1]):
		print("[FAIL] Determinismo roto en topología de distractores.")
		failures += 1
		return

	if not res1.metadata["target_base_position"].is_equal_approx(res2.metadata["target_base_position"]):
		print("[FAIL] Determinismo roto en spatial placement del target.")
		failures += 1
		return

	for f in range(total_frames):
		var s1 = res1.frames[f]
		var s2 = res2.frames[f]
		if not s1.position.is_equal_approx(s2.position) or not s1.custom_data["target_position"].is_equal_approx(s2.custom_data["target_position"]):
			print("[FAIL] Determinismo roto en fotograma ", f)
			failures += 1
			return

	print("[PASS] _test_full_spectrum_determinism (130, 140, 150, 160 fully validated)")

func _test_close_call_episodic_logic() -> void:
	var cfg = _get_test_config()
	var reg = _setup_registry()
	var ctx = MechanicRNGContext.create(1111, "2.0", "FindMechanic", [130, 140, 150, 160], StructuralRNG.new(reg), reg)
	
	var mech = FindMechanic.new()
	mech.set_rng_context(ctx.context)
	mech.setup(cfg)
	
	var math_10 = mech.calculate_frame(10, cfg)
	var math_20 = mech.calculate_frame(20, cfg)

	# CORREGIDO: Estas líneas ahora tienen la indentación correcta
	mech._distractors.clear()
	mech._distractors.append(math_10["p_scan"] as Vector2)
	mech._distractors.append(math_20["p_scan"] as Vector2)
	
	var capture_radius = 80.0
	var close_call_episodes = 0
	var in_false_positive_episode = false
	
	for f in range(30):
		var math_f = mech.calculate_frame(f, cfg)
		var p_scan = math_f["p_scan"]
		var p_target = math_f["p_target"]
		
		var d_t = p_scan.distance_to(p_target)
		var is_in_target = (d_t <= capture_radius)
		var is_in_distractor = false
		
		for distractor in mech._distractors:
			if p_scan.distance_to(distractor) <= capture_radius:
				is_in_distractor = true
				break
				
		var current_is_false_positive = is_in_distractor and not is_in_target
		
		if current_is_false_positive and not in_false_positive_episode:
			close_call_episodes += 1
			in_false_positive_episode = true
		elif not current_is_false_positive:
			in_false_positive_episode = false
			
	if close_call_episodes != 2:
		print("[FAIL] Lógica episódica de close_calls incorrecta. Esperados: 2, Obtenidos: ", close_call_episodes)
		failures += 1
	else:
		print("[PASS] _test_close_call_episodic_logic")
     
     
func _test_pure_structural_isolation() -> void:
	var cfg = _get_test_config()
	var reg = _setup_registry()
	
	var s_rng = StructuralRNG.new(reg)
	var ctx = MechanicRNGContext.create(5555, "2.0", "FindMechanic", [130, 140, 150, 160], s_rng, reg)
	
	var mech = FindMechanic.new()
	mech.set_rng_context(ctx.context)
	mech.setup(cfg)
	
	var base_p_before = mech._p_base
	var phi_x_before = mech._phi_x
	var phi_y_before = mech._phi_y
	var phi_drift_before = mech._phi_drift
	var distractors_before = mech._distractors.duplicate()
	
	mech._rng_context = null
	
	var frame_10_a = mech.calculate_frame(10, cfg)
	var frame_10_b = mech.calculate_frame(10, cfg)
	
	if not frame_10_a["p_scan"].is_equal_approx(frame_10_b["p_scan"]) or \
	   not frame_10_a["p_target"].is_equal_approx(frame_10_b["p_target"]) or \
	   mech._p_base != base_p_before or \
	   mech._phi_x != phi_x_before or \
	   mech._phi_y != phi_y_before or \
	   mech._phi_drift != phi_drift_before or \
	   mech._distractors.size() != distractors_before.size():
		print("[FAIL] calculate_frame no es puro o mutó estado estructural.")
		failures += 1
	else:
		print("[PASS] _test_pure_structural_isolation (Zero RNG & zero mutation verified)")