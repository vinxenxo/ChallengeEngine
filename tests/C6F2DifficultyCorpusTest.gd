# res://tests/C6F2DifficultyCorpusTest.gd
extends SceneTree

func _init():
	print("[TEST] Running C6F2DifficultyCorpusTest...")
	
	var mechanics = [
		"key", "parking", "pilot", "parking_v2", 
		"hit_v1", "catch_v1", "find_v1", "choose_v1", "count_v1"
	]
	
	var bands_levels = {
		"EASY": 10,
		"NORMAL": 30,
		"HARD": 60,
		"EXTREME": 90
	}
	
	var total_resolutions = 0
	
	for mech in mechanics:
		var profile_id = "default_" + mech
		var profile = DifficultyProfileRegistry.get_profile(profile_id)
		
		if profile.is_empty():
			printerr("FAIL: Profile not found for mechanic: " + mech)
			quit(1)
			
		# Validar estructura básica del perfil
		if profile.get("mechanic") != mech:
			printerr("FAIL: Mechanic mismatch in profile " + profile_id)
			quit(1)
			
		for band_name in bands_levels:
			var lvl = bands_levels[band_name]
			
			var challenge_mock = {
				"mechanic": mech,
				"difficulty": {
					"level": lvl,
					"overrides": {}
				},
				"simulation": { "parameters": {} }
			}
			
			var result = DifficultyResolver.resolve_for_challenge(challenge_mock, profile)
			if not result.success:
				printerr("FAIL: Resolution failed for %s at band %s. Error: %s" % [mech, band_name, result.error])
				quit(1)
				
			if result.effective_parameters.is_empty():
				printerr("FAIL: Effective parameters empty for %s at band %s" % [mech, band_name])
				quit(1)
				
			total_resolutions += 1
			
	if total_resolutions != 36:
		printerr("FAIL: Expected 36 resolutions, got %d" % total_resolutions)
		quit(1)
		
	print("[C6F2_DIFFICULTY_CORPUS_SUITE] PASS")
	quit(0)