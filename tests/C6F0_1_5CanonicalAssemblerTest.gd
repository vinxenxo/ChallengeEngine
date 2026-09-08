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
	
	# Validación soberana obligatoria del perfil de vídeo mediante VideoProfileValidator
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

	# 2. Cargar asset family enriquecida con rutas físicas reales extraídas del corpus (CHALLENGE_001.json)
	var challenge_cfg = _load_json("res://challenges/CHALLENGE_001.json")
	var real_assets = challenge_cfg.get("assets", {})
	
	var complete_asset_family = asset_family.duplicate(true)
	complete_asset_family["background_path"] = real_assets.get("background_path", "res://assets/backgrounds/background_default.png")
	complete_asset_family["target_path"] = real_assets.get("target_path", "res://assets/targets/target_default.png")
	complete_asset_family["object_path"] = real_assets.get("object_path", "res://assets/objects/object_default.png")

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

	# 3. Snapshots de Inmutabilidad Profunda antes de la asamblea
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

	# Verificación de inmutabilidad estricta (igualdad profunda post-asamblea)
	_assert(request.get_overrides() == req_overrides_snap, "Request overrides must not be mutated")
	_assert(request.get_content() == req_content_snap, "Request content must not be mutated")
	_assert(resolution_mock == resolution_snap, "Resolution result must not be mutated")
	_assert(adapter_meta == adapter_meta_snap, "Adapter metadata must not be mutated")
	_assert(video_profile == video_profile_snap, "Video profile must not be mutated")
	_assert(presentation_config == pres_config_snap, "Presentation config must not be mutated")
	_assert(complete_asset_family == asset_family_snap, "Asset family must not be mutated")

	# 4. Validación de Estructura Normativa F1 Exacta
	_assert(canonical.get("schema_version") == "2.0", "schema_version must be 2.0")
	_assert(canonical.get("version") == "1.0.0", "version must match metadata")
	_assert(canonical.get("engine_version") == "1.0", "engine_version must match contract")
	_assert(canonical.has("challenge_id"), "challenge_id required")
	_assert(canonical.get("mechanic") == "pilot", "mechanic required")
	_assert(canonical.has("mechanic_version"), "mechanic_version required")
	_assert(canonical.has("asset_family"), "asset_family required")
	_assert(canonical.has("asset_family_version"), "asset_family_version required")
	_assert(canonical.has("theme"), "theme required")
	_assert(canonical.has("simulation"), "simulation required")
	
	# Validación estructura exacta de vídeo F1 (aplanada, sin profile_id, sin phases)
	var video_block = canonical.get("video", {})
	_assert(typeof(video_block) == TYPE_DICTIONARY, "video must be dictionary")
	_assert(video_block.has("fps"), "video must have fps")
	_assert(video_block.has("hook_duration"), "video must have hook_duration")
	_assert(video_block.has("game_duration"), "video must have game_duration")
	_assert(video_block.has("reveal_duration"), "video must have reveal_duration")
	_assert(video_block.has("cta_duration"), "video must have cta_duration")
	_assert(not video_block.has("profile_id"), "video must NOT have profile_id in F1 normative schema")
	_assert(not video_block.has("phases"), "video must NOT have phases in F1 normative schema")

	# Validación estructura exacta de presentation F1
	var pres_block = canonical.get("presentation", {})
	_assert(typeof(pres_block) == TYPE_DICTIONARY, "presentation must be dictionary")
	_assert(pres_block.has("profile_id"), "presentation must have profile_id")
	_assert(pres_block.has("coordinate_space"), "presentation must have coordinate_space")
	_assert(pres_block.has("secondary_binding"), "presentation must have secondary_binding")

	# Validación estructura exacta de assets F1
	var assets_block = canonical.get("assets", {})
	_assert(typeof(assets_block) == TYPE_DICTIONARY, "assets must be dictionary")
	_assert(assets_block.has("background_path"), "assets must have background_path")
	_assert(assets_block.has("target_path"), "assets must have target_path")
	_assert(assets_block.has("object_path"), "assets must have object_path")

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