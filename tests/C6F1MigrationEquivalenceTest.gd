# res://tests/C6F1MigrationEquivalenceTest.gd
extends SceneTree

const ADAPTER = preload("res://core/authoring/ChallengeMigrationAdapter.gd")
const SCHEMA = preload("res://core/validation/C6FChallengeSchemaValidator.gd")
const REGISTRY = preload("res://core/mechanics/MechanicRegistry.gd")
const RNG_REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")
const STRUCTURAL_RNG = preload("res://core/deterministic/StructuralRNG.gd")
const RNG_CONTEXT = preload("res://core/deterministic/MechanicRNGContext.gd")

var failures := 0

func _init() -> void:
	var policy := {
		"authoring_version": "1.0.0",
		"default_engine_version": "0.1",
		"default_asset_family": "fam_garage_01",
		"default_asset_family_version": "1.0",
		"default_theme": "generic",
		"default_profile_id": "test_master_11s",
		"default_profile_version": "1.0",
		"default_mechanic_version": "1.0"
	}
	for id in ["001","002","003","004","005","006","007","008","009"]:
		_run_fixture("res://challenges/CHALLENGE_%s.json" % id, policy)
	if failures == 0:
		print("[C6F1_MIGRATION_EQUIVALENCE_SUITE] PASS")
		quit(0)
	else:
		print("[C6F1_MIGRATION_EQUIVALENCE_SUITE] FAIL failures=%d" % failures)
		quit(1)

func _run_fixture(path: String, policy: Dictionary) -> void:
	var original: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	if original.is_empty():
		_fail(path, "Unable to read JSON")
		return
	var migrated = ADAPTER.migrate_legacy_v1_to_v2(original, policy)
	if not migrated.is_valid:
		_fail(path, str(migrated.errors))
		return
	var canonical: Dictionary = migrated.config
	var schema_result := SCHEMA.validate_v2(canonical)
	if not schema_result.is_valid:
		_fail(path, "Canonical schema: %s" % str(schema_result.errors))
		return
	var runtime: Dictionary = ADAPTER.canonical_v2_to_runtime_v1(canonical)
	var expected := _effective_runtime_projection(original)
	var actual := _effective_runtime_projection(runtime)
	if JSON.stringify(expected) != JSON.stringify(actual):
		_fail(path, "Runtime projection differs")
		return
	if not _preserve_explicit_declarative_fields(path, original, canonical):
		return
	if not _compare_simulation(path, original, runtime):
		return

func _effective_runtime_projection(cfg: Dictionary) -> Dictionary:
	# Compare only the declarative inputs actually consumed by the frozen runtime.
	# Authoring/provenance metadata (schema/version/profile/family/theme) is excluded.
	var out := {}
	out["challenge_id"] = str(cfg.get("challenge_id", ""))
	out["mechanic"] = str(cfg.get("mechanic", ""))
	out["generation"] = {
		"seed": int(cfg.get("generation", {}).get("seed", 0)),
		"rng_version": str(cfg.get("generation", {}).get("rng_version", "1.0"))
	}
	var video: Dictionary = cfg.get("video", {})
	out["video"] = {
		"fps": int(video.get("fps", 0)),
		"hook_duration": float(video.get("hook_duration", 0.0)),
		"game_duration": float(video.get("game_duration", 0.0)),
		"reveal_duration": float(video.get("reveal_duration", 0.0)),
		"cta_duration": float(video.get("cta_duration", 0.0))
	}
	out["difficulty"] = cfg.get("difficulty", {})
	out["content"] = cfg.get("content", {})
	# Presentation/assets are deliberately excluded: they are authoring/presentation
	# concerns and must not participate in C3-C5 simulation equivalence.
	return out

func _preserve_explicit_declarative_fields(path: String, original: Dictionary, canonical: Dictionary) -> bool:
	# Verify explicitly authored fields survive migration. This is separate from
	# runtime equivalence because canonical V2 may legitimately add structural
	# defaults required by its own schema.
	for root_key in ["asset_family", "asset_family_version", "theme", "engine_version", "mechanic_version"]:
		if original.has(root_key) and str(canonical.get(root_key, "")) != str(original[root_key]):
			return _fail(path, "Explicit field '%s' changed during migration" % root_key)
	var original_content: Dictionary = original.get("content", {})
	var canonical_content: Dictionary = canonical.get("content", {})
	for key in ["hook", "reveal", "cta"]:
		if original_content.has(key) and canonical_content.get(key) != original_content[key]:
			return _fail(path, "Explicit content '%s' changed during migration" % key)
	var original_presentation: Dictionary = original.get("presentation", {})
	var canonical_presentation: Dictionary = canonical.get("presentation", {})
	for key in ["coordinate_space", "secondary_binding", "static_target_position", "visual", "ui"]:
		if original_presentation.has(key) and canonical_presentation.get(key) != original_presentation[key]:
			return _fail(path, "Explicit presentation '%s' changed during migration" % key)
	return true

func _compare_simulation(path: String, a: Dictionary, b: Dictionary) -> bool:
	var mechanic_id := str(a.get("mechanic", ""))
	var fps := int(a.get("video", {}).get("fps", 60))
	var game_frames := int(round(float(a.get("video", {}).get("game_duration", 7.0)) * fps))
	var seed := int(a.get("generation", {}).get("seed", 0))
	var rng_version := str(a.get("generation", {}).get("rng_version", "1.0"))
	var ra = _simulate_one(mechanic_id, game_frames, seed, rng_version, a)
	var rb = _simulate_one(mechanic_id, game_frames, seed, rng_version, b)
	if ra == null or rb == null:
		return _fail(path, "Simulation setup unsupported/failed")
	if ra.winning_frame != rb.winning_frame:
		return _fail(path, "winning_frame changed: %d != %d" % [ra.winning_frame, rb.winning_frame])
	if ra.frames.size() != rb.frames.size():
		return _fail(path, "frame count changed")
	for i in range(ra.frames.size()):
		var fa: FrameSnapshot = ra.frames[i]
		var fb: FrameSnapshot = rb.frames[i]
		if not fa.position.is_equal_approx(fb.position) or not is_equal_approx(fa.rotation, fb.rotation) or not is_equal_approx(fa.opacity, fb.opacity):
			return _fail(path, "frame %d changed" % i)
	return true

func _simulate_one(mechanic_id: String, game_frames: int, seed: int, rng_version: String, cfg: Dictionary):
	var mechanic = REGISTRY.create_mechanic(mechanic_id)
	if mechanic == null: return null
	if rng_version == "2.0":
		var registry = RNG_REGISTRY.new()
		var structural = STRUCTURAL_RNG.new(registry)
		var streams: Array[int] = []
		var consumer := ""
		match mechanic_id:
			"pilot": streams = [10,20]; consumer = "PilotMechanic"
			"parking_v2": streams = [30,40,50,60]; consumer = "ParkingMechanic"
			"hit_v1": streams = [70,80,90]; consumer = "HitMechanic"
			"catch_v1": streams = [100,110,120]; consumer = "CatchMechanic"
			"find_v1": streams = [130,140,150,160]; consumer = "FindMechanic"
			_: streams = []
		if not streams.is_empty():
			var created = RNG_CONTEXT.create(seed, rng_version, consumer, streams, structural, registry)
			if not created.is_valid: return null
			mechanic.set_rng_context(created.context)
	mechanic.setup(cfg)
	if mechanic_id in ["pilot", "parking_v2", "hit_v1", "catch_v1", "find_v1", "choose_v1", "count_v1"]:
		mechanic.prepare(game_frames)
	else:
		mechanic.setup(cfg)
	return mechanic.simulate(game_frames, seed, cfg)

func _fail(path: String, message: String) -> bool:
	failures += 1
	print("[C6F1] FAIL %s -> %s" % [path, message])
	return false
