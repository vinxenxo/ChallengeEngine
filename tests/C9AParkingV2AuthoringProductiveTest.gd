# res://tests/C9AParkingV2AuthoringProductiveTest.gd
extends SceneTree

const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const ChallengeGenerator = preload("res://core/authoring/ChallengeGenerator.gd")
const Schema = preload("res://core/validation/C6FChallengeSchemaValidator.gd")

func _initialize() -> void:
	print("[TEST] Running C9AParkingV2AuthoringProductiveTest...")

	var request_result := ChallengeAuthoringRequest.create_from_dictionary({
		"mechanic": "parking_v2",
		"level": 3,
		"seed": 314159,
		"profile": "default_parking_v2",
		"overrides": {},
		"content": {
			"hook": "¡SOLO EL 1% APARCA SIN ROZAR!",
			"reveal": "",
			"cta": "¿Lo has clavado?"
		}
	})

	if not bool(request_result.get("success", false)):
		printerr("FAIL: request creation failed: %s" % str(request_result.get("errors", [])))
		quit(1)
		return

	var result := ChallengeGenerator.generate_normative(request_result.get("request"))
	if not bool(result.get("success", false)):
		printerr("FAIL: parking_v2 normative generation failed: %s" % str(result.get("error", "")))
		quit(1)
		return

	var challenge: Dictionary = result.get("challenge", {})
	var schema := Schema.validate_v2(challenge)
	if not bool(schema.get("is_valid", false)):
		printerr("FAIL: generated Canonical V2 schema invalid: %s" % str(schema.get("errors", [])))
		quit(1)
		return

	if challenge.get("mechanic") != "parking_v2":
		printerr("FAIL: mechanic mismatch.")
		quit(1)
		return

	if challenge.get("mechanic_version") != "2.0":
		printerr("FAIL: mechanic_version mismatch: %s" % str(challenge.get("mechanic_version")))
		quit(1)
		return

	if challenge.get("asset_family") != "fam_garage_01":
		printerr("FAIL: asset family mismatch.")
		quit(1)
		return

	var simulation: Dictionary = challenge.get("simulation", {})
	if simulation.get("rng_version") != "2.0":
		printerr("FAIL: rng_version mismatch.")
		quit(1)
		return

	var parameters: Dictionary = simulation.get("parameters", {})
	var parking: Dictionary = parameters.get("parking", {})
	var tolerance: Dictionary = parameters.get("tolerance", {})

	if parking.get("max_speed_px") != 12.0:
		printerr("FAIL: max_speed_px mismatch.")
		quit(1)
		return
	if parking.get("target_angle_deg") != 0.0:
		printerr("FAIL: target_angle_deg mismatch.")
		quit(1)
		return
	if tolerance.get("distance_px") != 50.0:
		printerr("FAIL: expected EASY scaling was not resolved at level 3.")
		quit(1)
		return
	if tolerance.get("angle_deg") != 30.0:
		printerr("FAIL: tolerance.angle_deg mismatch.")
		quit(1)
		return
	if parking.get("steering_noise") != 0.0:
		printerr("FAIL: steering_noise mismatch.")
		quit(1)
		return

	if challenge.get("video", {}).get("fps", -1) != 60:
		printerr("FAIL: video fps mismatch.")
		quit(1)
		return
	if challenge.get("video", {}).get("game_duration", -1.0) != 7.0:
		printerr("FAIL: game duration mismatch.")
		quit(1)
		return

	print("[C9A_PARKING_V2_AUTHORING] PASS")
	quit(0)
