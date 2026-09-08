class_name CanonicalV2Assembler
extends RefCounted

const SCHEMA = preload("res://core/validation/C6FChallengeSchemaValidator.gd")
const POLICY = preload("res://core/authoring/ChallengeAuthoringPolicy.gd")
const DIFFICULTY_RESOLVER = preload("res://core/authoring/DifficultyResolver.gd")

## C6-F0.1.5/0.1.6 — strict Canonical V2 materialization.
## Pure assembly only: no simulation, no RNG consumption, no timeline work.

static func assemble(
	request: ChallengeAuthoringRequest,
	resolution_result: Dictionary,
	adapter_metadata: Dictionary,
	video_profile: Dictionary,
	presentation_profile: PresentationProfile,
	presentation_binding: Dictionary,
	asset_family: Dictionary
) -> Dictionary:
	if request == null:
		return _fail("Authoring request is null.")
	if resolution_result.is_empty():
		return _fail("Difficulty resolution result is unavailable.")
	var parameters: Variant = resolution_result.get("effective_parameters", null)
	if not (parameters is Dictionary):
		return _fail("Difficulty resolution must provide Dictionary 'effective_parameters'.")

	if video_profile.is_empty():
		return _fail("Video profile is unavailable or empty.")
	for key in ["fps", "phases"]:
		if not video_profile.has(key):
			return _fail("Video profile missing required '%s'." % key)
	var phases: Variant = video_profile.get("phases")
	if not (phases is Dictionary):
		return _fail("Video profile 'phases' must be a Dictionary.")
	for key in ["hook_duration", "game_duration", "reveal_duration", "cta_duration"]:
		if not phases.has(key):
			return _fail("Video profile missing required phase '%s'." % key)

	if presentation_profile == null:
		return _fail("Presentation profile is unavailable.")
	var presentation_validation: Dictionary = presentation_profile.validate()
	if not bool(presentation_validation.get("is_valid", false)):
		return _fail("Presentation profile failed validation: %s" % str(presentation_validation.get("errors", [])))
	for key in ["coordinate_space", "secondary_binding"]:
		if not presentation_binding.has(key) or str(presentation_binding.get(key, "")).strip_edges().is_empty():
			return _fail("Presentation binding missing '%s'." % key)
	if str(presentation_binding.get("secondary_binding")) not in ["static_position", "target_position", "target_x", "target_state"]:
		return _fail("Invalid presentation secondary_binding.")

	if asset_family.is_empty():
		return _fail("Asset family is unavailable or empty.")
	for key in ["family_id", "version", "background_path", "target_path", "object_path"]:
		if not asset_family.has(key) or str(asset_family.get(key, "")).strip_edges().is_empty():
			return _fail("Asset family missing required '%s'." % key)
	for key in ["background_path", "target_path", "object_path"]:
		var path := str(asset_family[key])
		if not path.begins_with("res://"):
			return _fail("Asset '%s' must use a res:// path." % key)
		if not ResourceLoader.exists(path):
			return _fail("Asset '%s' does not exist: %s" % [key, path])

	for key in ["rng_version", "mechanic_version"]:
		if not adapter_metadata.has(key) or str(adapter_metadata.get(key, "")).strip_edges().is_empty():
			return _fail("Authoring metadata missing '%s'." % key)
	var rng_version: String = str(adapter_metadata.get("rng_version"))
	if rng_version not in ["1.0", "2.0"]:
		return _fail("Unsupported rng_version '%s'." % rng_version)

	var canonical: Dictionary = {
		"schema_version": POLICY.CANONICAL_SCHEMA_VERSION,
		"version": POLICY.AUTHORING_VERSION,
		"challenge_id": "AUTH_%s_%d" % [request.mechanic_id.to_upper(), request.seed],
		"engine_version": POLICY.ENGINE_VERSION,
		"mechanic": request.mechanic_id,
		"mechanic_version": str(adapter_metadata.get("mechanic_version")),
		"asset_family": str(asset_family.get("family_id")),
		"asset_family_version": str(asset_family.get("version")),
		"theme": presentation_profile.theme_name,
		"simulation": {
			"seed": request.seed,
			"rng_version": rng_version,
			"parameters": parameters.duplicate(true)
		},
		"video": {
			"fps": int(video_profile.get("fps")),
			"hook_duration": float(phases.get("hook_duration")),
			"game_duration": float(phases.get("game_duration")),
			"reveal_duration": float(phases.get("reveal_duration")),
			"cta_duration": float(phases.get("cta_duration"))
		},
		"difficulty": {
			"level": request.level,
			"label": _difficulty_label(parameters, request.level)
		},
		"content": request.get_content(),
		"presentation": {
			"profile_id": presentation_profile.profile_id,
			"profile_version": str(presentation_binding.get("profile_version", POLICY.DEFAULT_PRESENTATION_PROFILE_VERSION)),
			"coordinate_space": str(presentation_binding.get("coordinate_space")),
			"secondary_binding": str(presentation_binding.get("secondary_binding"))
		},
		"assets": {
			"background_path": str(asset_family.get("background_path")),
			"target_path": str(asset_family.get("target_path")),
			"object_path": str(asset_family.get("object_path"))
		}
	}

	var schema_result := SCHEMA.validate_v2(canonical)
	if not bool(schema_result.get("is_valid", false)):
		return _fail("Canonical V2 schema validation failed: %s" % str(schema_result.get("errors", [])))

	return {"success": true, "error": "", "challenge": canonical}

static func _difficulty_label(parameters: Dictionary, level: int) -> String:
	# Preserve the existing deterministic difficulty banding authority.
	return str(DIFFICULTY_RESOLVER.get_band_for_level(level))

static func _fail(message: String) -> Dictionary:
	return {"success": false, "error": message, "challenge": null}
