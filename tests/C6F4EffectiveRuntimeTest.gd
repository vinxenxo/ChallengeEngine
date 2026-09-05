extends SceneTree

const ChallengeRuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const ChallengeLegacyRuntimeOracle = preload("res://core/execution/ChallengeLegacyRuntimeOracle.gd")
const ChallengeRuntimeContext = preload("res://core/execution/ChallengeRuntimeContext.gd")

func _init() -> void:
	print("[TEST] Running C6F4EffectiveRuntimeTest...")
	var failures: Array[String] = []

	var generator_source := FileAccess.get_file_as_string("res://GeneradorMaestro.gd")
	if generator_source.contains("func run_validation_pipeline"):
		failures.append("GeneradorMaestro still owns run_validation_pipeline().")
	if generator_source.contains("register_profile("):
		failures.append("GeneradorMaestro contains forbidden dynamic VideoProfile registration.")
	if generator_source.contains("RNGStreamRegistry"):
		failures.append("GeneradorMaestro still owns RNG infrastructure wiring.")
	if not generator_source.contains("ChallengeRuntimeBridge.run_effective_pipeline"):
		failures.append("GeneradorMaestro does not use the effective C6 runtime entry point.")
	if not generator_source.contains("ChallengeLegacyRuntimeOracle.run"):
		failures.append("GeneradorMaestro does not invoke the independent legacy oracle.")

	for index in range(1, 10):
		_run_fixture("CHALLENGE_%03d" % index, failures)

	if failures.is_empty():
		print("[C6F4_EFFECTIVE_RUNTIME_SUITE] PASS")
		quit(0)
		return

	for failure in failures:
		printerr("FAIL: " + failure)
	print("[C6F4_EFFECTIVE_RUNTIME_SUITE] FAIL count=%d" % failures.size())
	quit(1)

func _run_fixture(challenge_id: String, failures: Array[String]) -> void:
	var path := "res://challenges/%s.json" % challenge_id
	var config = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not (config is Dictionary) or config.is_empty():
		failures.append("Unable to read fixture: %s" % path)
		return

	var effective := ChallengeRuntimeBridge.run_effective_pipeline(config)
	if not bool(effective.get("success", false)):
		failures.append("Effective runtime failed for %s: %s" % [challenge_id, str(effective.get("error", ""))])
		return

	var context: ChallengeRuntimeContext = effective.get("context")
	if context == null or context.simulation_result == null or context.timeline == null or context.presentation_binding == null:
		failures.append("Effective runtime returned incomplete context for %s." % challenge_id)
		return

	var validation: ValidationResult = effective.get("validation")
	if validation == null or not validation.is_valid:
		failures.append("Effective runtime returned invalid validation for %s." % challenge_id)
		return

	var oracle := ChallengeLegacyRuntimeOracle.run(config)
	if not bool(oracle.get("valid", false)):
		failures.append("Legacy oracle failed for %s: %s" % [challenge_id, str(oracle.get("message", ""))])
		return

	var equivalence := ChallengeRuntimeBridge.verify_equivalence(
		oracle.get("timeline"),
		oracle.get("result"),
		context
	)
	if not bool(equivalence.get("success", false)):
		failures.append("Effective/oracle equivalence failed for %s: %s" % [challenge_id, str(equivalence.get("failures", []))])
