# res://tests/C6F2VideoProfileContractTest.gd
extends SceneTree

const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")
const VideoProfileValidator = preload("res://core/authoring/VideoProfileValidator.gd")

func _init():
	print("[TEST] Running C6F2VideoProfileContractTest...")
	
	VideoProfileRegistry.clear_cache()
	
	# 1. Registry Load & Valid Schema
	var valid_profile = VideoProfileRegistry.get_profile("standard_8s")
	if valid_profile.is_empty():
		printerr("FAIL: Could not load 'standard_8s.json' from registry.")
		quit(1)
		
	var valid_errors = VideoProfileValidator.validate(valid_profile)
	if valid_errors.size() > 0:
		printerr("FAIL: Valid profile rejected: " + str(valid_errors))
		quit(1)
		
	# 2. Strict Root Fields Test
	var invalid_root = valid_profile.duplicate(true)
	invalid_root["rng_version"] = "2.0"
	var err_root = VideoProfileValidator.validate(invalid_root)
	if err_root.size() == 0 or not err_root[0].contains("Unknown root field"):
		printerr("FAIL: Validator failed to reject unknown root field.")
		quit(1)
		
	# 3. Strict Phase Fields Test
	var invalid_phase = valid_profile.duplicate(true)
	invalid_phase["phases"]["extra_time"] = 5.0
	var err_phase = VideoProfileValidator.validate(invalid_phase)
	if err_phase.size() == 0 or not err_phase[0].contains("Unknown phase field"):
		printerr("FAIL: Validator failed to reject unknown phase field.")
		quit(1)
		
	# 4. Mandatory Game Duration Check
	var no_game = valid_profile.duplicate(true)
	no_game["phases"]["game_duration"] = 0.0
	var err_no_game = VideoProfileValidator.validate(no_game)
	if err_no_game.size() == 0 or not err_no_game[0].contains("must be a number > 0"):
		printerr("FAIL: Validator failed to reject zero game_duration.")
		quit(1)
		
	# 5. Zero-Duration Omission Check (Allowed for non-game)
	var zero_hook = valid_profile.duplicate(true)
	zero_hook["phases"]["hook_duration"] = 0.0
	zero_hook["phases"]["reveal_duration"] = 0.0
	var err_zero_opt = VideoProfileValidator.validate(zero_hook)
	if err_zero_opt.size() > 0:
		printerr("FAIL: Validator incorrectly rejected valid 0.0 duration for optional phases.")
		quit(1)
		
	# 6. FPS Check
	var bad_fps = valid_profile.duplicate(true)
	bad_fps["fps"] = 0
	var err_fps = VideoProfileValidator.validate(bad_fps)
	if err_fps.size() == 0 or not err_fps[0].contains("integer > 0"):
		printerr("FAIL: Validator failed to reject invalid FPS.")
		quit(1)
		
	print("[C6F2_VIDEO_PROFILE_CONTRACT_SUITE] PASS")
	quit(0)