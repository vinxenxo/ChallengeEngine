# res://tests/PilotMechanicIsolationTest.gd
extends SceneTree

const REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")
const STRUCTURAL = preload("res://core/deterministic/StructuralRNG.gd")
const COSMETIC = preload("res://core/deterministic/CosmeticRNG.gd")
const MECH_CTX = preload("res://core/deterministic/MechanicRNGContext.gd")
const PRES_CTX = preload("res://core/deterministic/PresentationRNGContext.gd")
const PILOT = preload("res://core/mechanics/pilot/PilotMechanic.gd")
const DETECTOR = preload("res://core/validation/WinningFrameDetector.gd")

const TEST_SEED: int = 314159

func _initialize() -> void:
	var failures: Array[String] = []
	_run_test_p(failures)
	_run_test_q(failures)

	if failures.is_empty():
		print("[PILOT_ISOLATION_SUITE] PASS")
		quit(0)
		return

	for failure in failures:
		push_error(failure)
	print("[PILOT_ISOLATION_SUITE] FAIL count=%d" % failures.size())
	quit(1)

func _make_registry_stack():
	var registry = REGISTRY.new()
	var structural = STRUCTURAL.new(registry)
	var cosmetic = COSMETIC.new(registry)
	return [registry, structural, cosmetic]

func _make_pilot_context(structural: StructuralRNG, registry: RNGStreamRegistry, seed: int):
	return MECH_CTX.create(
		seed,
		"2.0",
		"PilotMechanic",
		[REGISTRY.STREAM_TRAJECTORY, REGISTRY.STREAM_CONTROL],
		structural,
		registry
	)

func _make_presentation_context(cosmetic: CosmeticRNG, registry: RNGStreamRegistry, seed: int):
	return PRES_CTX.create(
		seed,
		"2.0",
		"PilotVisuals",
		[REGISTRY.STREAM_PARTICLES],
		cosmetic,
		registry
	)

func _load_config() -> Dictionary:
	var file: FileAccess = FileAccess.open("res://challenges/CHALLENGE_003.json", FileAccess.READ)
	var json := JSON.new()
	var error := json.parse(file.get_as_text())
	if error != OK or not (json.data is Dictionary):
		return {}
	return json.data

func _simulate(seed: int, config: Dictionary) -> SimulationResult:

	var stack = _make_registry_stack()
	var registry: RNGStreamRegistry = stack[0]
	var structural: StructuralRNG = stack[1]

	var context_result = _make_pilot_context(structural, registry, seed)
	assert(context_result.is_valid)

	var pilot: PilotMechanic = PILOT.new()

	pilot.set_rng_context(context_result.context)
	pilot.setup(config)
	pilot.prepare(420)

	var result: SimulationResult = pilot.simulate(420, seed, config)
	DETECTOR.analyze_and_score(result)
	return result


func _run_test_p(failures: Array[String]) -> void:
	var config: Dictionary = _load_config()
	var first = _make_registry_stack()
	var registry: RNGStreamRegistry = first[0]
	var structural: StructuralRNG = first[1]
	var cosmetic: CosmeticRNG = first[2]

	var pilot_ctx_result = _make_pilot_context(structural, registry, TEST_SEED)
	if not pilot_ctx_result.is_valid:
		failures.append("Test P failed: Pilot context could not be created.")
		return

	var presentation_ctx_result = _make_presentation_context(cosmetic, registry, TEST_SEED)
	if not presentation_ctx_result.is_valid:
		failures.append("Test P failed: Presentation context could not be created.")
		return

	var pilot_a: PilotMechanic = PILOT.new()
	pilot_a.set_rng_context(pilot_ctx_result.context)
	pilot_a.setup(config)
	pilot_a.prepare(420)

	var result_a: SimulationResult = pilot_a.simulate(
		420,
		TEST_SEED,
		config
	)

	DETECTOR.analyze_and_score(result_a)

	# H1/H2/I/J: Presentation work happens independently and in a different order.
	var presentation_context: PresentationRNGContext = presentation_ctx_result.context
	for i in range(500):
		presentation_context.sample_float(REGISTRY.STREAM_PARTICLES, i)
	for i in range(499, -1, -1):
		presentation_context.sample_float(REGISTRY.STREAM_PARTICLES, i)

	var result_b: SimulationResult = _simulate(TEST_SEED, config)
	if not _simulation_results_equal(result_a, result_b):
		failures.append("Test P failed: cosmetic/presentation activity altered SimulationResult.")

func _run_test_q(failures: Array[String]) -> void:
	var config: Dictionary = _load_config()
	var baseline: SimulationResult = _simulate(TEST_SEED, config)

	# Cosmetic mutation must not alter the structural output.
	var stack = _make_registry_stack()
	var presentation_result = _make_presentation_context(stack[2], stack[0], TEST_SEED)
	if not presentation_result.is_valid:
		failures.append("Test Q failed: Presentation context could not be created.")
		return
	for i in range(500):
		presentation_result.context.sample_float_range(REGISTRY.STREAM_PARTICLES, i, -100.0, 100.0)
	var cosmetic_repeat: SimulationResult = _simulate(TEST_SEED, config)
	if baseline.winning_frame != cosmetic_repeat.winning_frame:
		failures.append("Test Q failed: cosmetic mutation changed winning_frame.")
	if baseline.minimum_distance != cosmetic_repeat.minimum_distance:
		failures.append("Test Q failed: cosmetic mutation changed minimum_distance.")

	# Structural mutation: increase trajectory amplitude; output must react.
	var structural_config: Dictionary = config.duplicate(true)
	structural_config["content"] = config["content"].duplicate(true)
	structural_config["content"]["trajectory_amplitude"] = 10.0
	var structural_variant: SimulationResult = _simulate(TEST_SEED, structural_config)
	if baseline.winning_frame == structural_variant.winning_frame and baseline.minimum_distance == structural_variant.minimum_distance:
		failures.append("Test Q failed: structural trajectory mutation produced identical output.")

func _simulation_results_equal(a: SimulationResult, b: SimulationResult) -> bool:
	if a.frames.size() != b.frames.size():
		return false
	if a.winning_frame != b.winning_frame:
		return false
	if a.minimum_distance != b.minimum_distance:
		return false
	if a.score != b.score:
		return false

	for i in range(a.frames.size()):
		var fa: FrameSnapshot = a.frames[i]
		var fb: FrameSnapshot = b.frames[i]
		if fa.position != fb.position:
			return false
		if fa.rotation != fb.rotation:
			return false
		if fa.scale != fb.scale:
			return false
		if fa.opacity != fb.opacity:
			return false
		if fa.custom_data.get("success_distance", INF) != fb.custom_data.get("success_distance", INF):
			return false
		if fa.custom_data.get("velocity", INF) != fb.custom_data.get("velocity", INF):
			return false
		if fa.custom_data.get("target_x", INF) != fb.custom_data.get("target_x", INF):
			return false
		if fa.custom_data.get("base_x", INF) != fb.custom_data.get("base_x", INF):
			return false
		if fa.custom_data.get("trajectory_noise", INF) != fb.custom_data.get("trajectory_noise", INF):
			return false
		if fa.custom_data.get("control_offset", INF) != fb.custom_data.get("control_offset", INF):
			return false

	return true
