class_name CanonicalV2Assembler
extends RefCounted

# ============================================================
# ChallengeEngineV01_STATELESS
# CanonicalV2Assembler.gd
# F0.1.5 — Strict F1 Canonical V2 Assembler.
#
# PRINCIPLE:
# - Strict enforcement: UNAVAILABLE -> FAIL (Zero magic defaults/fallbacks).
# - Translates authoring intents into normative Canonical V2 documents.
# ============================================================

static func assemble(
	request: ChallengeAuthoringRequest,
	resolution_result: Dictionary,
	adapter_metadata: Dictionary,
	video_profile: Dictionary,
	presentation_profile: PresentationProfile,
	presentation_config: Dictionary,
	asset_family: Dictionary
) -> Dictionary:
	
	# =========================================================
	# 1. STRICT UNAVAILABLE -> FAIL GUARDS (NO DEFAULTS)
	# =========================================================
	if video_profile.is_empty() or not video_profile.has("fps") or not video_profile.has("phases"):
		return {"success": false, "error": "Video profile is unavailable or missing required fps/phases contract."}
	
	var phases = video_profile.get("phases", {})
	if not phases.has("hook_duration") or not phases.has("game_duration") or not phases.has("reveal_duration") or not phases.has("cta_duration"):
		return {"success": false, "error": "Video profile phases contract incomplete."}

	if presentation_profile == null:
		return {"success": false, "error": "Presentation profile is unavailable (null)."}

	if presentation_config.is_empty() or not presentation_config.has("coordinate_space") or not presentation_config.has("secondary_binding"):
		return {"success": false, "error": "Presentation configuration missing coordinate_space or secondary_binding."}

	if asset_family.is_empty():
		return {"success": false, "error": "Asset family is unavailable or empty."}
	
	# Guardias explícitas sin fallbacks para family_id y version
	if not asset_family.has("family_id") or str(asset_family.get("family_id", "")).strip_edges() == "":
		return {"success": false, "error": "Asset family missing mandatory 'family_id'."}
	if not asset_family.has("version") or str(asset_family.get("version", "")).strip_edges() == "":
		return {"success": false, "error": "Asset family missing mandatory 'version'."}

	if not asset_family.has("background_path") or not asset_family.has("target_path") or not asset_family.has("object_path"):
		return {"success": false, "error": "Asset family missing physical paths contract."}

	var bg_path = str(asset_family.get("background_path", ""))
	var tgt_path = str(asset_family.get("target_path", ""))
	var obj_path = str(asset_family.get("object_path", ""))

	if bg_path.is_empty() or tgt_path.is_empty() or obj_path.is_empty():
		return {"success": false, "error": "Asset physical paths are empty strings."}

	if not ResourceLoader.exists(bg_path) or not ResourceLoader.exists(tgt_path) or not ResourceLoader.exists(obj_path):
		return {"success": false, "error": "Asset physical paths do not exist as valid resources on disk."}

	# Guardias estrictas para metadatos del adaptador (engine_version contractual)
	if not adapter_metadata.has("engine_version") or str(adapter_metadata.get("engine_version", "")).strip_edges() == "":
		return {"success": false, "error": "Adapter metadata missing mandatory 'engine_version'."}
	if not adapter_metadata.has("version") or str(adapter_metadata.get("version", "")).strip_edges() == "":
		return {"success": false, "error": "Adapter metadata missing normative 'version'."}
	if not adapter_metadata.has("mechanic_version") or str(adapter_metadata.get("mechanic_version", "")).strip_edges() == "":
		return {"success": false, "error": "Adapter metadata missing 'mechanic_version'."}
	if not adapter_metadata.has("rng_version") or str(adapter_metadata.get("rng_version", "")).strip_edges() == "":
		return {"success": false, "error": "Adapter metadata missing 'rng_version'."}
	if not adapter_metadata.has("difficulty_label") or str(adapter_metadata.get("difficulty_label", "")).strip_edges() == "":
		return {"success": false, "error": "Adapter metadata missing 'difficulty_label'."}

	if not resolution_result.has("effective_parameters") or typeof(resolution_result.get("effective_parameters")) != TYPE_DICTIONARY:
		return {"success": false, "error": "Resolution result missing or invalid 'effective_parameters'."}

	var mechanic_id = request.mechanic_id
	var seed = request.seed
	var level = request.level

	# =========================================================
	# 2. CANONICAL DERIVATION (STRICT F1 SHAPE)
	# =========================================================
	var video_object = {
		"fps": int(video_profile.get("fps")),
		"hook_duration": float(phases.get("hook_duration")),
		"game_duration": float(phases.get("game_duration")),
		"reveal_duration": float(phases.get("reveal_duration")),
		"cta_duration": float(phases.get("cta_duration"))
	}

	var presentation_object = {
		"profile_id": presentation_profile.profile_id,
		"coordinate_space": str(presentation_config.get("coordinate_space")),
		"secondary_binding": str(presentation_config.get("secondary_binding"))
	}

	var assets_object = {
		"background_path": bg_path,
		"target_path": tgt_path,
		"object_path": obj_path
	}

	var content_block = request.get_content()

	# =========================================================
	# 3. DOCUMENT ASSEMBLY
	# =========================================================
	var canonical_v2 = {
		"schema_version": "2.0",
		"version": str(adapter_metadata.get("version")),
		"challenge_id": "CANONICAL_%s_%d" % [mechanic_id.to_upper(), seed],
		"engine_version": str(adapter_metadata.get("engine_version")),
		"mechanic": mechanic_id,
		"mechanic_version": str(adapter_metadata.get("mechanic_version")),
		
		"asset_family": str(asset_family.get("family_id")),
		"asset_family_version": str(asset_family.get("version")),
		
		"theme": presentation_profile.theme_name,
		
		"simulation": {
			"seed": seed,
			"rng_version": str(adapter_metadata.get("rng_version")),
			"parameters": resolution_result.get("effective_parameters")
		},
		
		"video": video_object,
		
		"content": content_block,
		
		"difficulty": {
			"level": level,
			"label": str(adapter_metadata.get("difficulty_label")),
			"profile": request.profile_id,
			"overrides": request.get_overrides()
		},
		
		"presentation": presentation_object,
		
		"assets": assets_object
	}

	return {
		"success": true,
		"error": "",
		"challenge": canonical_v2
	}