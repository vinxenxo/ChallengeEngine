# res://tests/DeterministicLCGStatelessTest.gd
extends SceneTree

const RNG = preload("res://core/deterministic/DeterministicLCG.gd")
const KEY_MECHANIC = preload("res://core/mechanics/key/KeyMechanic.gd")
const PARKING_MECHANIC = preload("res://core/mechanics/parking/ParkingMechanic.gd")
const DETECTOR = preload("res://core/validation/WinningFrameDetector.gd")
const RESOLVER = preload("res://core/simulation/SimulationMetricsResolver.gd")
const VALIDATOR = preload("res://core/validation/ChallengeValidator.gd")

func _initialize() -> void:
	var failures: Array[String] = []
	_run_rng_tests(failures)
	_run_regression_tests(failures)

	if failures.is_empty():
		print("[RNG_TEST_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[RNG_TEST_SUITE] FAIL count=%d" % failures.size())
		quit(1)


func _run_rng_tests(failures: Array[String]) -> void:
	# Test A — exact legacy sequence equivalence, 10,000 samples.
	var legacy_state: int = 193847
	for i in range(10000):
		legacy_state = ((legacy_state * RNG.MULTIPLIER) + RNG.INCREMENT) & RNG.MASK_31
		var stateless_value: int = RNG.sample_integer(193847, 0, i)
		if stateless_value != legacy_state:
			failures.append("Test A failed at index %d: legacy=%d stateless=%d" % [i, legacy_state, stateless_value])
			break

	# Test B — repeated referentially identical samples.
	var repeated_value: float = RNG.sample_float(987654, 10, 5)
	for _i in range(100):
		if RNG.sample_float(987654, 10, 5) != repeated_value:
			failures.append("Test B failed: repeated sample changed.")
			break

	# Test C — call order cannot affect explicit indices.
	var ordered: Dictionary = {}
	for index in [2, 5, 9]:
		ordered[index] = RNG.sample_integer(987654, 10, index)
	for index in [5, 2, 9]:
		if RNG.sample_integer(987654, 10, index) != ordered[index]:
			failures.append("Test C failed for index %d." % index)
			break

	# Test D — stream 20 calls cannot alter stream 10.
	var baseline: Array[int] = []
	for index in range(100):
		baseline.append(RNG.sample_integer(987654, 10, index))
	for index in range(100):
		RNG.sample_integer(987654, 20, index * 17)
	for index in range(100):
		if RNG.sample_integer(987654, 10, index) != baseline[index]:
			failures.append("Test D failed for stream 10 index %d." % index)
			break

	# Test E — the RNG implementation must not declare mutable instance state.
	var rng_source: String = FileAccess.get_file_as_string("res://core/deterministic/DeterministicLCG.gd")
	for line in rng_source.split("\n"):
		var trimmed: String = line.strip_edges()
		if not line.begins_with("\t") and not line.begins_with(" ") and (trimmed.begins_with("var ") or trimmed.begins_with("var\t")):
			failures.append("Test E failed: mutable class/module variable found: %s" % trimmed)
			break


func _run_regression_tests(failures: Array[String]) -> void:
	var key_config: Dictionary = _load_json("res://challenges/CHALLENGE_001.json")
	var key: ChallengeMechanic = KEY_MECHANIC.new()
	var key_result: SimulationResult = key.simulate(420, 126048932, key_config)
	
	# C4-C1: Inyección de la capa de métricas derivada
	RESOLVER.resolve_metrics(key_result)
	DETECTOR.analyze_and_score(key_result)
	var key_validation: ValidationResult = VALIDATOR.validate(key_result, 120, 420)

	if key_result.winning_frame != 342:
		failures.append("Test F failed: CHALLENGE_001 winning_frame=%d" % key_result.winning_frame)
	if not is_equal_approx(key_result.minimum_distance, 0.000230040647936747):
		failures.append("Test F failed: CHALLENGE_001 minimum_distance=%s" % key_result.minimum_distance)
	if not is_equal_approx(key_result.score, 0.638380059088502):
		failures.append("Test F failed: CHALLENGE_001 score=%s" % key_result.score)
	if not key_validation.is_valid:
		failures.append("Test F failed: CHALLENGE_001 validation rejected: %s" % key_validation.errors)

	var parking_config: Dictionary = _load_json("res://challenges/CHALLENGE_002.json")
	var parking: ChallengeMechanic = PARKING_MECHANIC.new()
	var parking_result: SimulationResult = parking.simulate(420, 987654, parking_config)
	
	# C4-C1: Inyección de la capa de métricas derivada
	RESOLVER.resolve_metrics(parking_result)
	DETECTOR.analyze_and_score(parking_result)
	var parking_validation: ValidationResult = VALIDATOR.validate(parking_result, 120, 420)

	if parking_result.winning_frame != 395:
		failures.append("Test G failed: CHALLENGE_002 winning_frame=%d" % parking_result.winning_frame)
	if not is_equal_approx(parking_result.metadata.get("dodge_offset", 0.0), -95.0478103361315):
		failures.append("Test G failed: dodge_offset=%s" % parking_result.metadata.get("dodge_offset"))
	if not is_equal_approx(parking_result.metadata.get("save_offset", 0.0), 23.9687795163918):
		failures.append("Test G failed: save_offset=%s" % parking_result.metadata.get("save_offset"))
	if not is_equal_approx(parking_result.metadata.get("overshoot_dist", 0.0), 67.4236544163076):
		failures.append("Test G failed: overshoot_dist=%s" % parking_result.metadata.get("overshoot_dist"))
	if not parking_validation.is_valid:
		failures.append("Test G failed: CHALLENGE_002 validation rejected: %s" % parking_validation.errors)


func _load_json(path: String) -> Dictionary:
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	var json: JSON = JSON.new()
	var error: Error = json.parse(file.get_as_text())
	if error != OK or not (json.data is Dictionary):
		return {}
	return json.data