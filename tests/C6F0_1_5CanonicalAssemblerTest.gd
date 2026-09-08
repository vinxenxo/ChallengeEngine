extends SceneTree

# ============================================================
# C6-F0.1.5 Canonical V2 Assembler Validation Suite
# ============================================================

const CanonicalV2Assembler = preload("res://core/authoring/CanonicalV2Assembler.gd")
const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const AuthoringMechanicRegistry = preload("res://core/authoring/AuthoringMechanicRegistry.gd")
const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")
const VideoProfileValidator = preload("res://core/authoring/VideoProfileValidator.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")
const AssetFamilyRegistry = preload("res://core/authoring/AssetFamilyRegistry.gd")

var failures: int = 0

func _init() -> void:
	print("[TEST] Running C6F0_1_5CanonicalAssemblerTest...")
	
	AuthoringMechanicRegistry.initialize_defaults()
	
	var request = ChallengeAuthoringRequest.new("pilot", 5, 42, "pilot_default", {"custom_param": 1.0}, {"hook": "Test Hook"})
	var adapter = AuthoringMechanicRegistry.get_adapter("pilot")
	
	var rng_res = adapter.rng_version()
	var video_res = adapter.default_video_profile()
	var pres_res = adapter.default_presentation_profile()
	var asset_res = adapter.required_assets()
	
	var video_profile = VideoProfileRegistry.get_profile(video_res.get("value", "test_master_11s"))
	
	var video_errors = VideoProfileValidator.validate(video_profile)
	_assert(video_errors.is_empty(), "Video profile must pass VideoProfileValidator successfully.")

	var presentation_profile = PresentationProfile.from_challenge({
		"presentation": {
			"profile_id": pres_res.get("value", "social_default_v1")
		},
		"theme": "default_c6"
	})
	var presentation_config = {
		"coordinate_space": "CANVAS_1080X1920",
		"secondary_binding": "target_position"
	}
	
	var asset_family = AssetFamilyRegistry.get_family(asset_res.get("value", "fam_001"))
	
	# 1. Test de Fallo Estricto (UNAVAILABLE -> FAIL) ante asset family sin paths físicos válidos
	var res_fail = CanonicalV2Assembler.assemble(
		request,
		{"effective_parameters": {}},
		{"engine_version": "1.0", "mechanic_version": "1.0", "rng_version": "1.0", "difficulty_label": "hard", "version": "1.0.0"},
		video_profile,
		presentation_profile,
		presentation_config,
		asset_family
	)
	_assert(not res_fail.get("success", true), "Assembler must fail when physical asset paths are missing or invalid.")

	# 2. Cargar asset family con rutas físicas reales estrictas del corpus (CHALLENGE_001.json) sin fallbacks
	var challenge_cfg = _load_json("res://challenges/CHALLENGE_001.json")
	_assert(challenge_cfg.has("assets"), "CHALLENGE_001.json must contain 'assets' block.")
	var real_assets = challenge_cfg.get("assets")
	
	_assert(real_assets.has("background_path"), "CHALLENGE_001.json assets must have background_path")
	_assert(real_assets.has("target_path"), "CHALLENGE_001.json assets must have target_path")
	_assert(real_assets.has("object_path"), "CHALLENGE_001.json assets must have object_path")
	
	var complete_asset_family = asset_family.duplicate(true)
	complete_asset_family["background_path"] = real_assets["background_path"]
	complete_asset_family["target_path"] = real_assets["target_path"]
	complete_asset_family["object_path"] = real_assets["object_path"]

	var resolution_mock = {
		"effective_parameters": {"speed": 12.0}
	}
	var adapter_meta = {
		"engine_version": "1.0",
		"mechanic_version": "1.0",
		"rng_version": str(rng_res.get("value", "1.0")),
		"difficulty_label": "intermediate",
		"version": "1.0.0"
	}

	# 3. Snapshots de Inmutabilidad Profunda
	var req_overrides_snap = request.get_overrides()
	var req_content_snap = request.get_content()
	var resolution_snap = resolution_mock.duplicate(true)
	var adapter_meta_snap = adapter_meta.duplicate(true)
	var video_profile_snap = video_profile.duplicate(true)
	var pres_config_snap = presentation_config.duplicate(true)
	var asset_family_snap = complete_asset_family.duplicate(true)

	var res_success = CanonicalV2Assembler.assemble(
		request,
		resolution_mock,
		adapter_meta,
		video_profile,
		presentation_profile,
		presentation_config,
		complete_asset_family
	)
	
	_assert(res_success.get("success", false), "Assembler must succeed with complete verified contracts: " + str(res_success.get("error", "")))
	var canonical = res_success.get("challenge", {})

	# Verificación de inmutabilidad estricta
	_assert(request.get_overrides() == req_overrides_snap, "Request overrides must not be mutated")
	_assert(request.get_content() == req_content_snap, "Request content must not be mutated")
	_assert(resolution_mock == resolution_snap, "Resolution result must not be mutated")
	_assert(adapter_meta == adapter_meta_snap, "Adapter metadata must not be mutated")
	_assert(video_profile == video_profile_snap, "Video profile must not be mutated")
	_assert(presentation_config == pres_config_snap, "Presentation config must not be mutated")
	_assert(complete_asset_family == asset_family_snap, "Asset family must not be mutated")

	# 4. Validación F1 Normativa Rigurosa contra el Schema Real (challenge_schema.json)
	var schema_dict = _load_json("res://challenge_schema.json")
	_assert(not schema_dict.is_empty(), "challenge_schema.json must be loadable and non-empty.")
	
	_validate_against_schema_f1(canonical, schema_dict)

	# 5. Determinismo Estricto
	var res_success_2 = CanonicalV2Assembler.assemble(
		request, resolution_mock, adapter_meta, video_profile, presentation_profile, presentation_config, complete_asset_family
	)
	var canonical_2 = res_success_2.get("challenge", {})
	_assert(canonical == canonical_2, "Assembler must be strictly deterministic.")

	if failures == 0:
		print("[C6F0_1_5_CANONICAL_ASSEMBLER_SUITE] PASS")
		quit(0)
	else:
		push_error("[C6F0_1_5_CANONICAL_ASSEMBLER_SUITE] FAIL count=%d" % failures)
		quit(1)

func _validate_against_schema_f1(data: Dictionary, schema: Dictionary) -> void:
	var required_props = schema.get("required", [])
	var properties = schema.get("properties", {})
	
	# Verificar propiedades requeridas a nivel de raíz según F1
	for prop in required_props:
		_assert(data.has(prop), "Schema F1 validation failed: missing required root property '%s'" % prop)
		
	# Verificar tipos y propiedades adicionales (additionalProperties: false enforcement)
	for key in data.keys():
		_assert(properties.has(key), "Schema F1 validation failed: property '%s' is not defined in challenge_schema.json (additionalProperties violation)" % key)
		
		var prop_schema = properties.get(key, {})
		var expected_type = prop_schema.get("type", "")
		var val = data[key]
		
		if expected_type == "string":
			_assert(typeof(val) == TYPE_STRING, "Schema F1 type error for '%s': expected string" % key)
		elif expected_type == "object":
			_assert(typeof(val) == TYPE_DICTIONARY, "Schema F1 type error for '%s': expected object/dictionary" % key)
			
			# Validación recursiva de sub-objetos normativos (video, presentation, assets, simulation, difficulty, content)
			var sub_required = prop_schema.get("required", [])
			var sub_properties = prop_schema.get("properties", {})
			
			for sub_req in sub_required:
				_assert(val.has(sub_req), "Schema F1 sub-object validation failed: '%s' missing required property '%s'" % [key, sub_req])
				
			for sub_key in val.keys():
				_assert(sub_properties.has(sub_key), "Schema F1 sub-object validation failed: '%s.%s' is not defined in schema" % [key, sub_key])
				
				var sub_prop_schema = sub_properties.get(sub_key, {})
				var sub_expected_type = sub_prop_schema.get("type", "")
				var sub_val = val[sub_key]
				
				if sub_expected_type == "string":
					_assert(typeof(sub_val) == TYPE_STRING, "Schema F1 type error for '%s.%s': expected string" % [key, sub_key])
				elif sub_expected_type == "integer" or sub_expected_type == "number":
					_assert(typeof(sub_val) == TYPE_INT or typeof(sub_val) == TYPE_FLOAT, "Schema F1 type error for '%s.%s': expected number/integer" % [key, sub_key])
				elif sub_expected_type == "object":
					_assert(typeof(sub_val) == TYPE_DICTIONARY, "Schema F1 type error for '%s.%s': expected object" % [key, sub_key])

func _load_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		return parsed
	return {}

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		print("[ASSEMBLER-TEST-FAIL] " + message)