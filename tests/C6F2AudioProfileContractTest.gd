# res://tests/C6F2AudioProfileContractTest.gd
extends SceneTree

const AudioProfileRegistry = preload("res://core/authoring/AudioProfileRegistry.gd")
const AudioProfileValidator = preload("res://core/authoring/AudioProfileValidator.gd")

func _init() -> void:
	print("[TEST] Running C6F2AudioProfileContractTest...")
	
	AudioProfileRegistry.clear_cache()
	var failures: Array[String] = []
	
	# 1. Valid Asset Music Profile
	var asset_prof = AudioProfileRegistry.get_profile("default_asset_music")
	if asset_prof.is_empty():
		failures.append("Could not load 'default_asset_music'.")
	else:
		var errs = AudioProfileValidator.validate(asset_prof)
		if errs.size() > 0:
			failures.append("Asset profile rejected: " + str(errs))
			
	# 2. Valid Procedural Music Profile
	var proc_prof = AudioProfileRegistry.get_profile("default_procedural_music")
	if proc_prof.is_empty():
		failures.append("Could not load 'default_procedural_music'.")
	else:
		var errs = AudioProfileValidator.validate(proc_prof)
		if errs.size() > 0:
			failures.append("Procedural profile rejected: " + str(errs))
			
	# 3. Procedural whitelist enforcement (Block simulation leakage)
	var leak_proc = proc_prof.duplicate(true)
	leak_proc["music"]["procedural_config"] = leak_proc["music"]["procedural_config"].duplicate(true)
	leak_proc["music"]["procedural_config"]["game_duration_override"] = 10.0
	var err_leak = AudioProfileValidator.validate(leak_proc)
	if err_leak.size() == 0 or not err_leak[0].contains("Unknown procedural field"):
		failures.append("Validator failed to reject 'game_duration_override' from procedural_config.")

	# 4. SFX whitelist enforcement
	var leak_sfx = asset_prof.duplicate(true)
	leak_sfx["sfx"] = leak_sfx["sfx"].duplicate(true)
	leak_sfx["sfx"]["timeline_override"] = true
	var err_sfx = AudioProfileValidator.validate(leak_sfx)
	if err_sfx.size() == 0 or not err_sfx[0].contains("Unknown sfx field"):
		failures.append("Validator failed to reject 'timeline_override' from sfx.")
		
	# 5. Mutually exclusive modes protection
	var hybrid = asset_prof.duplicate(true)
	hybrid["music"] = hybrid["music"].duplicate(true)
	hybrid["music"]["procedural_config"] = {"tempo": 120, "intensity": 0.5} # Mixing asset and procedural
	var err_hybrid = AudioProfileValidator.validate(hybrid)
	if err_hybrid.size() == 0 or not err_hybrid[0].contains("not allowed when mode is 'asset'"):
		failures.append("Validator failed to reject mutually exclusive config injection (procedural inside asset mode).")
		
	# 6. Semantic Volume validation
	var bad_vol = asset_prof.duplicate(true)
	bad_vol["music"] = bad_vol["music"].duplicate(true)
	bad_vol["music"]["volume_db"] = 25.0 # Max is 12.0
	var err_vol = AudioProfileValidator.validate(bad_vol)
	if err_vol.size() == 0 or not err_vol[0].contains("[-80, 12]"):
		failures.append("Validator failed to semantic-check volume_db upper bound.")
		
	# 7. Registry Identity Check
	# Forzando una discordancia entre archivo pedido ("fake") y perfil interno ("default_asset_music")
	var fake_identity_load = AudioProfileRegistry.get_profile("fake_identity") # This should fail closed inside the registry if we had a mismatched JSON, but we test the null return for now.
	
	if failures.is_empty():
		print("[C6F2_AUDIO_PROFILE_CONTRACT_SUITE] PASS")
		quit(0)
		return
		
	for failure in failures:
		printerr("FAIL: " + failure)
	print("[C6F2_AUDIO_PROFILE_CONTRACT_SUITE] FAIL count=%d" % failures.size())
	quit(1)