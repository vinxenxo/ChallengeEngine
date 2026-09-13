# res://tests/C6F4CanonicalV2CountTest.gd
extends SceneTree

# ============================================================
# C6-F4.4 Phase 7: Canonical V2 CountMechanic Test
# ============================================================

func _init() -> void:
	print("[TEST] Running C6F4CanonicalV2CountTest...")

	var challenge_file = FileAccess.open("res://challenges/CHALLENGE_009.json", FileAccess.READ)
	if challenge_file == null:
		push_error("No se encontro CHALLENGE_009.json")
		quit(1)
		return

	var v1_config = JSON.parse_string(challenge_file.get_as_text())
	if not (v1_config is Dictionary) or v1_config.is_empty():
		push_error("CHALLENGE_009.json invalido.")
		quit(1)
		return

	# 1. Legacy Oracle
	print("[TEST] 1. Ejecutando Oracle Legacy...")
	var oracle_result = ChallengeLegacyRuntimeOracle.run(v1_config)
	if not bool(oracle_result.get("valid", false)):
		push_error("Legacy Oracle fallo: " + str(oracle_result.get("error_code", "")) + " " + str(oracle_result.get("message", "")))
		quit(1)
		return

	var legacy_sim: SimulationResult = oracle_result.get("result")
	if legacy_sim == null:
		push_error("Legacy Oracle no devolvio SimulationResult.")
		quit(1)
		return

	# 2. V1 -> Canonical V2
	print("[TEST] 2. Migrando V1 -> V2...")
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

	var canonical_v2: Dictionary = mig_res.get("config", {}).duplicate(true)
	if canonical_v2.is_empty():
		push_error("La migracion devolvio un config vacio.")
		quit(1)
		return

	# 3. Remove all legacy inputs and preserve the authoritative seed.
	print("[TEST] 3. Stripping legacy y fijando seed V2...")
	var generation_cfg: Dictionary = v1_config.get("generation", {})
	var effective_seed: int = int(generation_cfg.get("seed", 12345))

	canonical_v2.erase("difficulty")
	canonical_v2.erase("content")
	canonical_v2.erase("generation")

	if not canonical_v2.has("simulation"):
		canonical_v2["simulation"] = {}
	canonical_v2["simulation"]["seed"] = effective_seed

	if not canonical_v2.has("simulation") or not (canonical_v2["simulation"] is Dictionary):
		push_error("Canonical V2 no contiene simulation.")
		quit(1)
		return

	if not canonical_v2["simulation"].has("parameters"):
		push_error("Canonical V2 no contiene simulation.parameters.")
		quit(1)
		return

	if not canonical_v2["simulation"]["parameters"].has("count") and not canonical_v2["simulation"]["parameters"].has("min_value"):
		push_error("Canonical V2 no contiene parametros de COUNT.")
		quit(1)
		return

	# 4. Native V2 execution.
	print("[TEST] 4. Ejecutando Pipeline V2...")
	var exec_res = ChallengeExecutionPipeline.execute(canonical_v2)
	if not bool(exec_res.get("success", false)):
		push_error("ExecutionPipeline fallo con Canonical V2 puro: " + str(exec_res.get("error", "")))
		quit(1)
		return

	var v2_sim: SimulationResult = exec_res.get("simulation_result")
	if v2_sim == null:
		push_error("ExecutionPipeline no devolvio SimulationResult.")
		quit(1)
		return

	# 5. Core equivalence.
	print("[TEST] 5. Comprobando equivalencia...")
	if legacy_sim.winning_frame != v2_sim.winning_frame:
		push_error("Mismatch winning_frame: %d vs %d" % [legacy_sim.winning_frame, v2_sim.winning_frame])
		quit(1)
		return

	if legacy_sim.frames.size() != v2_sim.frames.size():
		push_error("Mismatch frames: %d vs %d" % [legacy_sim.frames.size(), v2_sim.frames.size()])
		quit(1)
		return

	if abs(legacy_sim.score - v2_sim.score) > 0.000001:
		push_error("Mismatch score: %s vs %s" % [str(legacy_sim.score), str(v2_sim.score)])
		quit(1)
		return

	if abs(legacy_sim.minimum_distance - v2_sim.minimum_distance) > 0.000001:
		push_error("Mismatch minimum_distance: %s vs %s" % [str(legacy_sim.minimum_distance), str(v2_sim.minimum_distance)])
		quit(1)
		return

	for key in ["target_count", "min_value", "max_value", "close_calls", "rng_version"]:
		var legacy_value = legacy_sim.metadata.get(key)
		var v2_value = v2_sim.metadata.get(key)
		if str(legacy_value) != str(v2_value):
			push_error("Mismatch metadata[%s]: %s vs %s" % [key, str(legacy_value), str(v2_value)])
			quit(1)
			return

	# COUNT is discrete: custom_data is part of the equivalence contract.
	print("[TEST] 5.1 Comparando custom_data fotograma a fotograma...")
	for i in range(legacy_sim.frames.size()):
		var lf: FrameSnapshot = legacy_sim.frames[i]
		var vf: FrameSnapshot = v2_sim.frames[i]

		if lf.position.distance_to(vf.position) > 0.000001:
			push_error("Position mismatch at frame %d" % i)
			quit(1)
			return

		if JSON.stringify(lf.custom_data) != JSON.stringify(vf.custom_data):
			push_error("Custom data mismatch at frame %d: Legacy %s vs V2 %s" % [i, JSON.stringify(lf.custom_data), JSON.stringify(vf.custom_data)])
			quit(1)
			return

	print("[C6F4_CANONICAL_V2_COUNT_SUITE] PASS")
	quit(0)
