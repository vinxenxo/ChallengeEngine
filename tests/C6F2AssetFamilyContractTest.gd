# res://tests/C6F2AssetFamilyContractTest.gd
extends SceneTree

const AssetFamilyRegistry = preload("res://core/authoring/AssetFamilyRegistry.gd")
const AssetFamilyValidator = preload("res://core/authoring/AssetFamilyValidator.gd")

func _init():
	print("[TEST] Running C6F2AssetFamilyContractTest...")
	
	AssetFamilyRegistry.clear_cache()
	
	# 1. Valid Registry Load
	var valid_family = AssetFamilyRegistry.get_family("default")
	if valid_family.is_empty():
		printerr("FAIL: Could not load 'default.json' from registry.")
		quit(1)
		
	var valid_errors = AssetFamilyValidator.validate(valid_family)
	if valid_errors.size() > 0:
		printerr("FAIL: Valid asset family rejected: " + str(valid_errors))
		quit(1)
		
	# 2. Boundary Test (Reject Audio/Simulation injection)
	var boundary_violation = valid_family.duplicate(true)
	boundary_violation["audio_profile"] = "chiptune_01" # Simulating architectural bleed
	var err_boundary = AssetFamilyValidator.validate(boundary_violation)
	if err_boundary.size() == 0 or not err_boundary[0].contains("Unknown root field"):
		printerr("FAIL: Validator failed to reject architectural boundary violation (unknown field).")
		quit(1)
		
	# 3. Missing Mandatory Fields Test
	var no_id = valid_family.duplicate(true)
	no_id.erase("family_id")
	var err_no_id = AssetFamilyValidator.validate(no_id)
	if err_no_id.size() == 0 or not err_no_id[0].contains("Missing or invalid 'family_id'"):
		printerr("FAIL: Validator failed to reject missing family_id.")
		quit(1)
		
	var no_version = valid_family.duplicate(true)
	no_version.erase("version")
	var err_no_version = AssetFamilyValidator.validate(no_version)
	if err_no_version.size() == 0 or not err_no_version[0].contains("Missing or invalid 'version'"):
		printerr("FAIL: Validator failed to reject missing version.")
		quit(1)
		
	# 4. Strict Type Test (Themes must be strings)
	var bad_themes = valid_family.duplicate(true)
	bad_themes["themes"] = [123, 456]
	var err_themes = AssetFamilyValidator.validate(bad_themes)
	if err_themes.size() == 0 or not err_themes[0].contains("Theme entry must be a string"):
		printerr("FAIL: Validator failed to reject non-string theme array elements.")
		quit(1)
		
	print("[C6F2_ASSET_FAMILY_CONTRACT_SUITE] PASS")
	quit(0)