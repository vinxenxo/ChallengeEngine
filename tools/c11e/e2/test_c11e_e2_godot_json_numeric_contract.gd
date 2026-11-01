extends SceneTree

const Validator = preload("res://tools/c11e/e2/C11EE2SidecarValidator.gd")
const RESULT_SCHEMA := "C11E-E2-GODOT-JSON-NUMERIC-TEST-RESULT-V1"
const EXPECTED_MANIFEST_SHA := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const EXPECTED_CHALLENGE_SHA := "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea"

func _initialize() -> void:
	call_deferred("_run_contract")

func _run_contract() -> void:
	var result_path := _get_result_path()
	var result: Dictionary = {
		"schema": RESULT_SCHEMA,
		"status": "FAILED",
		"failure": "not_started",
		"json_gameplay_type": "NOT_READ",
		"json_music_type": "NOT_READ",
		"full_sidecar_validation": false,
		"numeric_cases_passed": 0,
		"numeric_cases_expected": 30
	}
	if result_path.is_empty():
		_fail(result, "Missing --result-json=<absolute-path>", "")
		return

	var valid_sidecar: Dictionary = {
		"schema": "C11E-CHALLENGE-EDITORIAL-SIDECAR-V1",
		"schema_version": "1.0",
		"content_type": "challenges",
		"challenge_id": "CHALLENGE_001",
		"editorial": {"title": "E2 JSON NUMERIC TEST"},
		"visual_target": {
			"slot_id": "header.editorial_title",
			"region": "HEADER",
			"semantic_separation": "TITLE_IS_NOT_HOOK_CTA_OR_GAMEPLAY",
			"visibility": "ALL_CHALLENGE_FRAMES",
			"bounds_logical_540x960": {"x": 24, "y": 24, "width": 496, "height": 104}
		},
		"execution_boundary": {
			"renderer_input_is_e2_test_only": true,
			"release_authority": "NONE",
			"baseline_promotion": false,
			"audio_enabled": false
		},
		"source_identity": {
			"c11c_manifest_sha256": EXPECTED_MANIFEST_SHA,
			"challenge_source_sha256": EXPECTED_CHALLENGE_SHA
		},
		"seed_domains": {
			"independent_domains": true,
			"gameplay": {"field": "request.seed", "value": 193847.0},
			"music": {"field": "request.music_seed", "value": 840001.0}
		}
	}

	var json_text := JSON.stringify(valid_sidecar)
	var parsed: Variant = JSON.parse_string(json_text)
	if typeof(parsed) != TYPE_DICTIONARY:
		_fail(result, "JSON.parse_string did not return a Dictionary", result_path)
		return
	var parsed_sidecar: Dictionary = parsed
	var seed_domains: Dictionary = parsed_sidecar["seed_domains"]
	var gameplay: Dictionary = seed_domains["gameplay"]
	var music: Dictionary = seed_domains["music"]
	var gameplay_value: Variant = gameplay["value"]
	var music_value: Variant = music["value"]
	result["json_gameplay_type"] = type_string(typeof(gameplay_value))
	result["json_music_type"] = type_string(typeof(music_value))
	if typeof(gameplay_value) != TYPE_FLOAT or typeof(music_value) != TYPE_FLOAT:
		_fail(result, "JSON round-trip did not exercise floating-point seed Variants", result_path)
		return

	if not Validator.validate(parsed_sidecar):
		_fail(result, "Production sidecar validator rejected a complete JSON-decoded valid sidecar", result_path)
		return
	result["full_sidecar_validation"] = true

	var valid_values: Array = [1, 193847, 2147483646, 1.0, 193847.0, 2147483646.0]
	for candidate: Variant in valid_values:
		if not Validator.is_positive_integral_seed(candidate):
			_fail(result, "Valid integer seed rejected: " + str(candidate), result_path)
			return
		result["numeric_cases_passed"] = int(result["numeric_cases_passed"]) + 1

	var invalid_values: Array = [0, -1, 1.5, "193847", true, 2147483647.0, NAN, INF, -INF, null, [], {}]
	for seed_name: String in ["gameplay", "music"]:
		for candidate: Variant in invalid_values:
			var candidate_sidecar: Dictionary = parsed_sidecar.duplicate(true)
			var domains: Dictionary = candidate_sidecar["seed_domains"]
			var seed_record: Dictionary = domains[seed_name]
			seed_record["value"] = candidate
			if Validator.validate(candidate_sidecar):
				_fail(result, "Invalid " + seed_name + " seed accepted: " + str(candidate), result_path)
				return
			result["numeric_cases_passed"] = int(result["numeric_cases_passed"]) + 1

	result["numeric_cases_expected"] = 30
	if int(result["numeric_cases_passed"]) != 30:
		_fail(result, "Numeric test case denominator mismatch", result_path)
		return
	result["status"] = "PASS"
	result["failure"] = null
	if not _write_result(result_path, result):
		push_error("[C11E_E2_JSON_NUMERIC] PASS result could not be persisted.")
		quit(1)
		return
	print("C11E_E2_GODOT_JSON_NUMERIC_CONTRACT=PASS")
	print("JSON_GAMEPLAY_TYPE=" + str(result["json_gameplay_type"]))
	print("JSON_MUSIC_TYPE=" + str(result["json_music_type"]))
	print("FULL_SIDECAR_VALIDATION=PASS")
	print("NUMERIC_CASES=30/30")
	quit(0)

func _get_result_path() -> String:
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--result-json="):
			return arg.substr("--result-json=".length()).replace("\\", "/")
	return ""

func _write_result(path: String, result: Dictionary) -> bool:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("[C11E_E2_JSON_NUMERIC] Cannot create structured result: " + path)
		return false
	file.store_string(JSON.stringify(result, "\t"))
	file.flush()
	file.close()
	return true

func _fail(result: Dictionary, reason: String, result_path: String) -> void:
	result["status"] = "FAILED"
	result["failure"] = reason
	if not result_path.is_empty():
		_write_result(result_path, result)
	push_error("[C11E_E2_JSON_NUMERIC] " + reason)
	quit(1)
