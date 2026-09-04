extends SceneTree

func _init():
	print("[TEST] Running C6F2DifficultyMonotonicityTest...")
	
	# Verificamos find_v1: distractor_count debe subir de EASY a EXTREME
	var find_profile = DifficultyProfileRegistry.get_profile("default_find_v1")
	var res_easy = DifficultyResolver.resolve(10, find_profile, {})
	var res_extreme = DifficultyResolver.resolve(90, find_profile, {})
	
	var dist_easy = res_easy.effective_parameters.get("distractor_count", 0)
	var dist_extreme = res_extreme.effective_parameters.get("distractor_count", 0)
	
	if dist_easy >= dist_extreme:
		printerr("FAIL: Monotonicity violation in find_v1.distractor_count (Easy: %d, Extreme: %d)" % [dist_easy, dist_extreme])
		quit(1)
		
	# Verificamos hit_v1: hitbox_radius debe reducirse (hacerse más pequeño) de EASY a EXTREME
	var hit_profile = DifficultyProfileRegistry.get_profile("default_hit_v1")
	var hit_easy = DifficultyResolver.resolve(10, hit_profile, {}).effective_parameters.get("hitbox_radius", 0.0)
	var hit_extreme = DifficultyResolver.resolve(90, hit_profile, {}).effective_parameters.get("hitbox_radius", 0.0)
	
	if hit_easy <= hit_extreme:
		printerr("FAIL: Monotonicity violation in hit_v1.hitbox_radius (Easy: %.1f, Extreme: %.1f)" % [hit_easy, hit_extreme])
		quit(1)
		
	print("[C6F2_DIFFICULTY_MONOTONICITY_SUITE] PASS")
	quit(0)