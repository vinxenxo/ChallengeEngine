# res://tests/C6F0_1_6AuthoringPipelineTest.gd
extends SceneTree

const ChallengeGenerator = preload("res://core/authoring/ChallengeGenerator.gd")
const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const Schema = preload("res://core/validation/C6FChallengeSchemaValidator.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F0_1_6AuthoringPipelineTest...")
	_run()
	if failures.is_empty():
		print("[C6F0_1_6_AUTHORING_PIPELINE_SUITE] PASS")
		quit(0)
		return
	for failure in failures:
		printerr("FAIL: " + failure)
	print("[C6F0_1_6_AUTHORING_PIPELINE_SUITE] FAIL count=%d" % failures.size())
	quit(1)

func _run() -> void:
	var result := ChallengeAuthoringRequest.create_from_dictionary({
		"mechanic": "pilot",
		"level": 3,
		"seed": 1337,
		"profile": "default_pilot",
		"overrides": {},
		"content": {
			"hook": "Pilot Pipeline Hook",
			"reveal": "Pilot Pipeline Reveal",
			"cta": "Pilot Pipeline CTA"
		}
	})
	_assert(bool(result.get("success", false)), "Request creation failed: %s" % str(result.get("errors", [])))
	if not bool(result.get("success", false)):
		return

	var request: ChallengeAuthoringRequest = result.get("request")
	var normative := ChallengeGenerator.generate_normative(request)
	_assert(bool(normative.get("success", false)), "Normative authoring generation failed: %s" % str(normative.get("error", "")))
	if not bool(normative.get("success", false)):
		return

	var canonical: Dictionary = normative.get("challenge", {})
	_assert(canonical.get("schema_version") == "2.0", "Normative schema_version must be 2.0.")
	_assert(canonical.get("mechanic") == "pilot", "Normative mechanic mismatch.")
	var schema := Schema.validate_v2(canonical)
	_assert(bool(schema.get("is_valid", false)), "Normative Canonical V2 failed schema validation: %s" % str(schema.get("errors", [])))
	_assert(canonical.get("content", {}).get("hook") == "Pilot Pipeline Hook", "Hook content lost in normative pipeline.")
	_assert(canonical.get("content", {}).get("reveal") == "Pilot Pipeline Reveal", "Reveal content lost in normative pipeline.")
	_assert(canonical.get("content", {}).get("cta") == "Pilot Pipeline CTA", "CTA content lost in normative pipeline.")

	# Legacy path remains a separately tested transport DTO. This test only checks
	# that adding the normative path does not replace it.
	var legacy := ChallengeGenerator.generate(request)
	_assert(bool(legacy.get("success", false)), "Legacy generate() was changed/broken by F0.1.6.")	
	if bool(legacy.get("success", false)):
		var legacy_challenge: Dictionary = legacy.get("challenge", {})
		_assert(typeof(legacy_challenge.get("video")) == TYPE_STRING, "Legacy DTO video field must remain a String.")

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
