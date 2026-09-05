extends SceneTree

const AuthoringMechanicRegistry = preload(
	"res://core/authoring/AuthoringMechanicRegistry.gd"
)

const ChallengeAuthoringRequest = preload(
	"res://core/authoring/ChallengeAuthoringRequest.gd"
)

const ChallengeGenerator = preload(
	"res://core/authoring/ChallengeGenerator.gd"
)

const VideoProfileRegistry = preload(
	"res://core/authoring/VideoProfileRegistry.gd"
)

const AssetFamilyRegistry = preload(
	"res://core/authoring/AssetFamilyRegistry.gd"
)


func _init() -> void:
	print(
		"[TEST] Running C6F2ProductiveGeneratorTest..."
	)

	AuthoringMechanicRegistry.clear_registry()
	AuthoringMechanicRegistry.initialize_defaults()

	VideoProfileRegistry.clear_cache()
	AssetFamilyRegistry.clear_cache()

	var failures: Array[String] = []

	# =========================================================
	# 1. PILOT — PRODUCTIVE GENERATION
	# =========================================================

	var pilot_request_result := (
		ChallengeAuthoringRequest.create_from_dictionary(
			{
				"mechanic": "pilot",
				"level": 50,
				"seed": 472819,
				"profile": "default_pilot",
				"overrides": {}
			}
		)
	)

	if not bool(
		pilot_request_result.get("success", false)
	):
		failures.append(
			"Pilot authoring request rejected: %s"
			% str(
				pilot_request_result.get(
					"errors",
					[]
				)
			)
		)
	else:
		var pilot_request = (
			pilot_request_result.get("request")
		)

		var pilot_result := (
			ChallengeGenerator.generate(
				pilot_request
			)
		)

		if not bool(
			pilot_result.get("success", false)
		):
			failures.append(
				"Pilot productive generation failed: %s"
				% str(
					pilot_result.get(
						"error",
						"unknown error"
					)
				)
			)
		else:
			if pilot_result.get("stage") != "assembly":
				failures.append(
					"Pilot generation did not finish at assembly."
				)

			var challenge = (
				pilot_result.get("challenge")
			)

			if typeof(challenge) != TYPE_DICTIONARY:
				failures.append(
					"Pilot generation did not return a Dictionary."
				)
			else:
				# Required established V2 fields.
				for key in [
					"schema_version",
					"challenge_id",
					"mechanic",
					"generation",
					"simulation",
					"difficulty",
					"video",
					"presentation",
					"asset_family",
					"asset_family_version",
					"theme"
				]:
					if not challenge.has(key):
						failures.append(
							"Pilot V2 missing required field '%s'."
							% key
						)

				if challenge.get("schema_version") != "2.0":
					failures.append(
						"Unexpected V2 schema_version: %s"
						% str(
							challenge.get(
								"schema_version"
							)
						)
					)

				if challenge.get("mechanic") != "pilot":
					failures.append(
						"Pilot V2 mechanic mismatch."
					)

				if challenge.get("video") != (
					"test_master_11s"
				):
					failures.append(
						"Pilot V2 video binding mismatch."
					)

				if challenge.get("presentation") != (
					"social_default_v1"
				):
					failures.append(
						"Pilot V2 presentation binding mismatch."
					)

				if challenge.get("asset_family") != (
					"fam_001"
				):
					failures.append(
						"Pilot V2 asset family binding mismatch."
					)

				if challenge.get("asset_family_version") != (
					"1.0"
				):
					failures.append(
						"Pilot V2 asset family version mismatch."
					)

				var generation = challenge.get(
					"generation",
					{}
				)

				if generation.get("seed") != 472819:
					failures.append(
						"Pilot generation seed mismatch."
					)

				if generation.get("rng_version") != "2.0":
					failures.append(
						"Pilot generation RNG version mismatch."
					)

				var simulation = challenge.get(
					"simulation",
					{}
				)

				if simulation.get("seed") != 472819:
					failures.append(
						"Pilot simulation seed mismatch."
					)

				if simulation.get("rng_version") != "2.0":
					failures.append(
						"Pilot simulation RNG version mismatch."
					)

				var difficulty = challenge.get(
					"difficulty",
					{}
				)

				if difficulty.get("level") != 50:
					failures.append(
						"Pilot difficulty level mismatch."
					)

				if difficulty.get("profile") != (
					"default_pilot"
				):
					failures.append(
						"Pilot difficulty profile mismatch."
					)

	# =========================================================
	# 2. HIT — FAIL CLOSED
	# =========================================================

	var hit_request_result := (
		ChallengeAuthoringRequest.create_from_dictionary(
			{
				"mechanic": "hit_v1",
				"level": 50,
				"seed": 472820,
				"profile": "default_hit_v1",
				"overrides": {}
			}
		)
	)

	if not bool(
		hit_request_result.get("success", false)
	):
		failures.append(
			"Hit authoring request unexpectedly rejected."
		)
	else:
		var hit_request = (
			hit_request_result.get("request")
		)

		var hit_result := (
			ChallengeGenerator.generate(
				hit_request
			)
		)

		if bool(hit_result.get("success", false)):
			failures.append(
				"Hit generation succeeded despite "
				+ "incomplete metadata."
			)

		if hit_result.get("stage") != (
			"metadata_validation"
		):
			failures.append(
				"Hit expected metadata_validation failure, got '%s'."
				% str(
					hit_result.get(
						"stage",
						""
					)
				)
			)

		if not str(
			hit_result.get(
				"error",
				""
			)
		).contains("Metadata unavailable"):
			failures.append(
				"Hit did not fail through the expected "
				+ "Metadata unavailable path: %s"
				% str(
					hit_result.get(
						"error",
						""
					)
				)
			)

		if hit_result.get("challenge") != null:
			failures.append(
				"Hit fail-closed generation returned "
				+ "a non-null challenge."
			)

	# =========================================================
	# FINAL
	# =========================================================

	if failures.is_empty():
		print(
			"[C6F2_PRODUCTIVE_GENERATOR_SUITE] PASS"
		)
		quit(0)
		return

	for failure in failures:
		printerr("FAIL: " + failure)

	print(
		"[C6F2_PRODUCTIVE_GENERATOR_SUITE] "
		+ "FAIL count=%d"
		% failures.size()
	)

	quit(1)