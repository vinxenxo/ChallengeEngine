# res://tests/C6F4CanonicalV2ChooseTest.gd
extends SceneTree

# ============================================================
# C6-F4.4 Phase 6: Canonical V2 ChooseMechanic Test (ROBUST)
# ============================================================

func _init() -> void:
	print("[TEST] Running C6F4CanonicalV2ChooseTest...")
	
	var challenge_file = FileAccess.open("res://challenges/CHALLENGE_008.json", FileAccess.READ)
	if challenge_file == null:
		push_error("No se encontró CHALLENGE_008.json")
		quit(1)
		return
		
	var v1_config = JSON.parse_string(challenge_file.get_as_text())
	
	# 1. Oracle Legacy
	print("[TEST] 1. Ejecutando Oracle Legacy...")
	var ChallengeLegacyRuntimeOracle = load("res://core/execution/ChallengeLegacyRuntimeOracle.gd")
	var oracle_result = ChallengeLegacyRuntimeOracle.run(v1_config)
	if not bool(oracle_result.get("valid", false)):
		push_error(
			"Legacy Oracle falló: "
			+ str(oracle_result.get("error_code", ""))
			+ " "
			+ str(oracle_result.get("message", ""))
		)
		quit(1)
		return
		
	var legacy_sim: SimulationResult = oracle_result.get("result")
	if legacy_sim == null:
		push_error("Legacy Oracle no devolvió SimulationResult.")
		quit(1)
		return
	print("[TEST] 1. Oracle Legacy OK. Winning frame: ", legacy_sim.winning_frame)
	
	# 2. Migración V1 -> Canonical V2
	print("[TEST] 2. Migrando V1 -> V2...")
	var ChallengeMigrationAdapter = load("res://core/authoring/ChallengeMigrationAdapter.gd")
	const MIGRATION_POLICY := {
		"authoring_version": "1.0.0",
		"default_engine_version": "0.1",
		"default_asset_family": "fam_001",
		"default_asset_family_version": "1.0",
		"default_theme": "generic",
		"default_profile_id": "test_master_11s",
		"default_profile_version": "1.0",
		"default_mechanic_version": "1.0",
		"default_difficulty_level": 0
	}
	var mig_res = ChallengeMigrationAdapter.migrate_legacy_v1_to_v2(v1_config, MIGRATION_POLICY)
	
	if not bool(mig_res.get("is_valid", false)):
		push_error("La migracion F1.1 fallo: " + str(mig_res.get("errors", [])))
		quit(1)
		return
		
	var canonical_v2 = mig_res.get("config", {}).duplicate(true)
	if canonical_v2.is_empty():
		push_error("La migracion devolvio un config vacio.")
		quit(1)
		return
	
	# 3. STRIP AGRESIVO Y SETUP NATIVO
	print("[TEST] 3. Stripping de variables legacy y Setup Nativo...")
	var generation_cfg = v1_config.get("generation", {})
	var effective_seed = int(generation_cfg.get("seed", 12345))
	
	canonical_v2.erase("difficulty")
	canonical_v2.erase("content")
	canonical_v2.erase("generation")
	
	# El Bridge en producción hace esto explícitamente para mecánicas V2 nativas
	if not canonical_v2.has("simulation"):
		canonical_v2["simulation"] = {}
	canonical_v2["simulation"]["seed"] = effective_seed
	
	# 4. F3.1 Execution 
	print("[TEST] 4. Ejecutando Pipeline V2...")
	var ChallengeExecutionPipeline = load("res://core/execution/ChallengeExecutionPipeline.gd")
	var exec_res = ChallengeExecutionPipeline.execute(canonical_v2)
	
	if not exec_res.success:
		push_error("ExecutionPipeline falló con Canonical V2 puro: " + str(exec_res.error))
		quit(1)
		return
		
	var v2_sim = exec_res.simulation_result
	print("[TEST] 4. Pipeline V2 OK. Winning frame: ", v2_sim.winning_frame)
	
	# 5. Equivalence Gate Endurecido
	print("[TEST] 5. Comprobando Equivalence Gate...")
	if legacy_sim.winning_frame != v2_sim.winning_frame:
		push_error("Mismatch winning_frame: Legacy %d vs V2 %d" % [legacy_sim.winning_frame, v2_sim.winning_frame])
		quit(1)
		return
		
	if legacy_sim.frames.size() != v2_sim.frames.size():
		push_error("Mismatch frames size: Legacy %d vs V2 %d" % [legacy_sim.frames.size(), v2_sim.frames.size()])
		quit(1)
		return
		
	if abs(legacy_sim.score - v2_sim.score) > 0.001:
		push_error("Mismatch score: %s vs %s" % [str(legacy_sim.score), str(v2_sim.score)])
		quit(1)
		return
		
	if abs(legacy_sim.minimum_distance - v2_sim.minimum_distance) > 0.001:
		push_error("Mismatch min_distance: %s vs %s" % [str(legacy_sim.minimum_distance), str(v2_sim.minimum_distance)])
		quit(1)
		return
		
	for key in ["close_calls", "rng_version"]:
		var legacy_val = legacy_sim.metadata.get(key)
		var v2_val = v2_sim.metadata.get(key)
		if str(legacy_val) != str(v2_val):
			push_error("Mismatch metadata[%s]: Legacy %s vs V2 %s" % [key, str(legacy_val), str(v2_val)])
			quit(1)
			return
		
	print("[TEST] 5.3 Comparando fotogramas y lógicas discretas...")
	for i in range(legacy_sim.frames.size()):
		var lf = legacy_sim.frames[i]
		var vf = v2_sim.frames[i]
		
		if lf.position.distance_to(vf.position) > 0.001:
			push_error("Positional determinism failed at frame %d" % i)
			quit(1)
			return
			
		var lf_cd_str = JSON.stringify(lf.custom_data)
		var vf_cd_str = JSON.stringify(vf.custom_data)
		if lf_cd_str != vf_cd_str:
			push_error("Custom data mismatch at frame %d: Legacy %s vs V2 %s" % [i, lf_cd_str, vf_cd_str])
			quit(1)
			return
			
	print("[C6F4_CANONICAL_V2_CHOOSE_SUITE] PASS")
	quit(0)