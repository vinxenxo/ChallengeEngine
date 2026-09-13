# res://tests/C6F2DeterminismTest.gd
extends SceneTree

func _init():
	print("[TEST] Running C6F2DeterminismTest...")
	
	var challenge_mock = {
		"mechanic": "test_mech",
		"difficulty": {
			"level": 75,
			"overrides": { "speed": 10.5 }
		},
		"simulation": { "parameters": {} } # Vacío, fuerza la resolución
	}
	
	var profile_mock = {
		"mechanic": "test_mech",
		"allowed_parameters": ["speed", "count"],
		"constraints": {
			"speed": {"type": "float", "min": 1.0, "max": 20.0},
			"count": {"type": "int", "min": 0, "max": 999}
		},
		"base_parameters": { "count": 5 },
		"scaling": {
			"EXTREME": { "count": 100 }
		}
	}
	
	# Simular inyección en Registry
	DifficultyProfileRegistry._cache["test_profile"] = profile_mock
	
	# 1. Primera pasada (Cache Hit simulado)
	var result_A = DifficultyResolver.resolve_for_challenge(challenge_mock, DifficultyProfileRegistry.get_profile("test_profile"))
	if not result_A.success:
		printerr("FAIL: First resolution failed: " + result_A.error)
		quit(1)
		
	var serialized_A: String = JSON.stringify(result_A.effective_parameters)
	
	# 2. Limpiar caché, forzar recarga (simulada aquí re-inyectando para no depender de I/O en el test unitario)
	DifficultyProfileRegistry.clear_cache()
	DifficultyProfileRegistry._cache["test_profile"] = profile_mock.duplicate(true)
	
	# 3. Segunda pasada (Cache Miss simulado)
	var result_B = DifficultyResolver.resolve_for_challenge(challenge_mock, DifficultyProfileRegistry.get_profile("test_profile"))
	if not result_B.success:
		printerr("FAIL: Second resolution failed: " + result_B.error)
		quit(1)
		
	var serialized_B: String = JSON.stringify(result_B.effective_parameters)
	
	# 4. Verificación de Identidad Serializada y Semántica
	if serialized_A != serialized_B:
		printerr("FAIL: Determinism broken. Results differ between cache states.")
		quit(1)
		
	if result_B.effective_parameters.get("count") != 100:
		printerr("FAIL: Semantic mapping for 'count' failed.")
		quit(1)
		
	if result_B.effective_parameters.get("speed") != 10.5:
		printerr("FAIL: Semantic mapping for 'speed' failed.")
		quit(1)
		
	# 5. Verificación de Precedencia Absoluta (Bypass si simulation.parameters está lleno)
	var challenge_precedence = challenge_mock.duplicate(true)
	challenge_precedence["simulation"]["parameters"] = {"speed": 99.9, "count": 1} # Explícito manual
	
	var result_C = DifficultyResolver.resolve_for_challenge(challenge_precedence, profile_mock)
	if result_C.effective_parameters.get("speed") != 99.9:
		printerr("FAIL: Runtime integration precedence violated! Did not respect existing simulation.parameters")
		quit(1)
		
	print("[C6F2_DETERMINISM_SUITE] PASS")
	quit(0)