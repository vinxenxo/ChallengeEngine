# res://tests/C6F4ShadowRuntimeBridgeTest.gd
extends SceneTree

const ChallengeRuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const ChallengeMigrationAdapter = preload("res://core/authoring/ChallengeMigrationAdapter.gd")
const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")
const AssetFamilyRegistry = preload("res://core/authoring/AssetFamilyRegistry.gd")

const MIGRATION_POLICY := {
	"authoring_version": "1.0.0",
	"default_engine_version": "0.1",
	"default_asset_family": "fam_001",
	"default_asset_family_version": "1.0",
	"default_theme": "generic",
	"default_profile_id": "test_master_11s",
	"default_profile_version": "1.0",
	"default_mechanic_version": "1.0",
	"default_difficulty_level": 0
}

func _init() -> void:
	print("[TEST] Running C6F4ShadowRuntimeBridgeTest...")
	var failures: Array[String] = []

	VideoProfileRegistry.clear_cache()
	AssetFamilyRegistry.clear_cache()

	var expected_profiles := {
		"CHALLENGE_001": "f4_legacy_60_h0_g7_r0_c2",
		"CHALLENGE_002": "f4_legacy_60_h3_g7_r0_c0",
		"CHALLENGE_003": "f4_legacy_60_h3_g7_r0_c2",
		"CHALLENGE_004": "f4_legacy_60_h3_g7_r3_c2",
		"CHALLENGE_005": "f4_legacy_60_h0_g7_r0_c0",
		"CHALLENGE_006": "f4_legacy_60_h0_g7_r0_c2",
		"CHALLENGE_007": "f4_legacy_60_h3_g7_r0_c0",
		"CHALLENGE_008": "f4_legacy_60_h3_g7_r0_c2",
		"CHALLENGE_009": "f4_legacy_60_h3_g7_r0_c2"
	}

	for challenge_id in expected_profiles.keys():
		_run_fixture(str(challenge_id), str(expected_profiles[challenge_id]), failures)

	if failures.is_empty():
		print("[C6F4_SHADOW_RUNTIME_BRIDGE_SUITE] PASS")
		quit(0)
		return

	for failure in failures:
		printerr("FAIL: " + failure)
	print("[C6F4_SHADOW_RUNTIME_BRIDGE_SUITE] FAIL count=%d" % failures.size())
	quit(1)

func _run_fixture(challenge_id: String, expected_profile: String, failures: Array[String]) -> void:
	var path := "res://challenges/%s.json" % challenge_id
	var config = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not (config is Dictionary) or config.is_empty():
		failures.append("Unable to read fixture: %s" % path)
		return

	var migration := ChallengeMigrationAdapter.migrate_legacy_v1_to_v2(config, MIGRATION_POLICY)
	if not bool(migration.get("is_valid", false)):
		failures.append("F1.1 migration failed for %s: %s" % [challenge_id, str(migration.get("errors", []))])
		return

	var canonical: Dictionary = migration.get("config", {})
	var video = canonical.get("video", {})
	if not (video is Dictionary):
		failures.append("Migrated video block is not a Dictionary for %s." % challenge_id)
		return

	var adapted := ChallengeRuntimeBridge._build_f3_runtime_input(
		canonical,
		config,
		int(config.get("generation", {}).get("seed", 0))
	)
	if not bool(adapted.get("success", false)):
		failures.append("F4 adaptation failed for %s: %s" % [challenge_id, str(adapted.get("error", ""))])
		return

	var f3_input: Dictionary = adapted.get("config", {})
	if str(f3_input.get("video", "")) != expected_profile:
		failures.append("Unexpected temporal profile for %s: expected=%s actual=%s" % [challenge_id, expected_profile, str(f3_input.get("video", ""))])

	var generation = f3_input.get("generation", {})
	if int(generation.get("seed", -1)) != int(config.get("generation", {}).get("seed", 0)):
		failures.append("Generation seed mismatch for %s." % challenge_id)

	var family_id := str(canonical.get("asset_family", ""))
	if family_id.is_empty():
		failures.append("Migrated asset_family is empty for %s." % challenge_id)
	else:
		var family := AssetFamilyRegistry.get_family(family_id)
		if family.is_empty():
			failures.append("Asset family '%s' does not resolve for %s." % [family_id, challenge_id])

	# The bridge must not mutate the canonical F1.1 temporal block.
	if str(canonical.get("video", {}).get("game_duration", -1)) != str(video.get("game_duration", -2)):
		failures.append("F1.1 canonical video was mutated for %s." % challenge_id)
