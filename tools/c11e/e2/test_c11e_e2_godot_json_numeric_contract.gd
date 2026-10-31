extends SceneTree

const E2Script = preload("res://tools/c11e/e2/C11EChallenge001E2.gd")
const EXPECTED_MANIFEST_SHA := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const EXPECTED_CHALLENGE_SHA := "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea"

func _initialize() -> void:
	# Round-trip a complete, valid E2 sidecar through Godot's actual JSON parser.
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
			"gameplay": {"field": "request.seed", "value": 193847},
			"music": {"field": "request.music_seed", "value": 840001}
		}
	}
	var parsed: Variant = JSON.parse_string(JSON.stringify(valid_sidecar))
	if not (parsed is Dictionary):
		_fail("JSON.parse_string did not return a Dictionary")
		return
	var parsed_sidecar: Dictionary = parsed
	var gameplay_value: Variant = parsed_sidecar["seed_domains"]["gameplay"]["value"]
	var music_value: Variant = parsed_sidecar["seed_domains"]["music"]["value"]
	if typeof(gameplay_value) != TYPE_FLOAT or typeof(music_value) != TYPE_FLOAT:
		_fail("Godot JSON number typing differs from the reviewed runtime contract")
		return
	var validator: Object = E2Script.new()
	if not validator.has_method("_validate_c11e_sidecar"):
		validator.free()
		_fail("E2 sidecar validator method was not exposed by the loaded script")
		return
	if not bool(validator.call("_validate_c11e_sidecar", parsed_sidecar)):
		validator.free()
		_fail("complete JSON-decoded E2 sidecar was rejected")
		return
	if not E2Script.is_positive_integral_seed(193847):
		validator.free()
		_fail("native integer gameplay seed was rejected")
		return
	if not E2Script.is_positive_integral_seed(2147483646.0):
		validator.free()
		_fail("maximum allowed seed was rejected")
		return
	var invalid_values: Array = [0, -1, 1.5, "193847", true, 2147483647.0, NAN, INF]
	for seed_name: String in ["gameplay", "music"]:
		for candidate: Variant in invalid_values:
			var candidate_sidecar: Dictionary = parsed_sidecar.duplicate(true)
			var domains: Dictionary = candidate_sidecar["seed_domains"]
			var seed_record: Dictionary = domains[seed_name]
			seed_record["value"] = candidate
			if bool(validator.call("_validate_c11e_sidecar", candidate_sidecar)):
				validator.free()
				_fail("invalid " + seed_name + " seed was accepted: " + str(candidate))
				return
	validator.free()
	print("C11E_E2_GODOT_JSON_NUMERIC_CONTRACT=PASS")
	print("JSON_GAMEPLAY_TYPE=" + type_string(typeof(gameplay_value)))
	print("JSON_MUSIC_TYPE=" + type_string(typeof(music_value)))
	print("FULL_SIDECAR_VALIDATION=PASS")
	quit(0)

func _fail(message: String) -> void:
	push_error("[C11E_E2_JSON_NUMERIC] " + message)
	quit(1)
