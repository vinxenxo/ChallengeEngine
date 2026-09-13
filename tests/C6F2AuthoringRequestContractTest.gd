# res://tests/C6F2AuthoringRequestContractTest.gd
extends SceneTree

func _init():
	print("[TEST] Running C6F2AuthoringRequestContractTest...")
	
	# 1. Valid request creation and schema compliance
	var valid_dict = {
		"mechanic": "find_v1",
		"level": 82,
		"seed": 472819,
		"profile": "default_find_v1",
		"overrides": { "capture_radius": 25.0 }
	}
	
	var res = ChallengeAuthoringRequest.create_from_dictionary(valid_dict)
	if not res.success:
		printerr("FAIL: Valid request rejected. Errors: " + str(res.errors))
		quit(1)
		
	var req: ChallengeAuthoringRequest = res.request
	if req.mechanic_id != "find_v1" or req.level != 82 or req.seed != 472819 or req.profile_id != "default_find_v1":
		printerr("FAIL: Request properties improperly mapped.")
		quit(1)
		
	# 2. Immutability / Deep-copy safety check
	var extracted_overrides = req.get_overrides()
	extracted_overrides["capture_radius"] = 999.0
	var clean_overrides = req.get_overrides()
	if clean_overrides["capture_radius"] == 999.0:
		printerr("FAIL: Request overrides lack deep-copy protection (mutation safety breached).")
		quit(1)
		
	# 3. Invalid mechanic test
	var invalid_mech_dict = valid_dict.duplicate(true)
	invalid_mech_dict["mechanic"] = "unknown_mech"
	var req_inv_mech = ChallengeAuthoringRequest.create_from_dictionary(invalid_mech_dict).request
	var errors_mech = ChallengeAuthoringRequestValidator.validate(req_inv_mech)
	if errors_mech.is_empty():
		printerr("FAIL: Validator failed to catch unregistered mechanic.")
		quit(1)
		
	# 4. Invalid level bounds test (Level 0 rejection)
	var invalid_lvl_dict = valid_dict.duplicate(true)
	invalid_lvl_dict["level"] = 0
	var res_inv_lvl = ChallengeAuthoringRequest.create_from_dictionary(invalid_lvl_dict)
	if res_inv_lvl.success:
		printerr("FAIL: Level 0 accepted by creator schema.")
		quit(1)
		
	invalid_lvl_dict["level"] = 101
	res_inv_lvl = ChallengeAuthoringRequest.create_from_dictionary(invalid_lvl_dict)
	if res_inv_lvl.success:
		printerr("FAIL: Level 101 accepted by creator schema.")
		quit(1)
		
	# 5. Profile/Mechanic mismatch test
	var mismatch_dict = valid_dict.duplicate(true)
	mismatch_dict["mechanic"] = "hit_v1" # Perfil es find_v1
	var req_mismatch = ChallengeAuthoringRequest.create_from_dictionary(mismatch_dict).request
	var errors_mismatch = ChallengeAuthoringRequestValidator.validate(req_mismatch)
	if errors_mismatch.is_empty():
		printerr("FAIL: Validator failed to catch profile/mechanic mismatch.")
		quit(1)
		
	# 6. Invalid override (firewall violation) test
	var invalid_override_dict = valid_dict.duplicate(true)
	invalid_override_dict["overrides"] = { "illegal_parameter": 123.0 }
	var req_invalid_override = ChallengeAuthoringRequest.create_from_dictionary(invalid_override_dict).request
	var errors_override = ChallengeAuthoringRequestValidator.validate(req_invalid_override)
	if errors_override.is_empty():
		printerr("FAIL: Validator failed to catch unauthorized override keys.")
		quit(1)
		
	print("[C6F2_AUTHORING_REQUEST_SUITE] PASS")
	quit(0)