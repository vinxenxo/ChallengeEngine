# res://tests/C7A01AudioDeterminismTest.gd
extends SceneTree

# ============================================================
# C7-A0.1-F1 — Audio Procedural Determinism & Isolation Test
# Validates determinism, stateless RNG, capability boundaries,
# index injectivity, and simulation non-contamination.
# ============================================================

const AudioRNGContext = preload("res://core/audio/AudioRNGContext.gd")
const AudioEvent = preload("res://core/audio/AudioEvent.gd")
const AudioProfile = preload("res://core/audio/AudioProfile.gd")
const AudioGenerationResult = preload("res://core/audio/AudioGenerationResult.gd")
const ToneBurstGenerator = preload("res://core/audio/generators/ToneBurstGenerator.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")
const ChallengeExecutionPipeline = preload("res://core/execution/ChallengeExecutionPipeline.gd")

const BASE_SEED = 12345
const ALT_SEED = 54321
const CONSUMER = "ToneBurstGenerator"

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C7A01AudioDeterminismTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _create_test_profile() -> AudioProfile:
	return AudioProfile.new("test_success_burst", "tone_burst", {
		"frequency_hz": 440.0, "amplitude": 0.8, "attack_frames": 48, "release_frames": 960
	})

func _create_test_event(tick: int, seq: int) -> AudioEvent:
	return AudioEvent.new("success_reveal", tick, seq, {"pitch_ratio": 1.5})

func _get_canonical_v2_fixture() -> Dictionary:
	var path = "res://challenges/CHALLENGE_004.json"
	var file = FileAccess.open(path, FileAccess.READ)
	var text = file.get_as_text()
	file.close()
	var dict = JSON.parse_string(text)
	
	# Preservar exactamente la configuración semántica de generación del fixture original
	if not dict.has("simulation"):
		if dict.has("generation"):
			dict["simulation"] = dict["generation"].duplicate(true)
		else:
			dict["simulation"] = {
				"seed": BASE_SEED,
				"rng_version": "2.0"
			}
	return dict

func _run_tests() -> void:
	# --- Prueba A: Determinismo semántico directo ---
	var registry_a = RNGStreamRegistry.new()
	var registry_b = RNGStreamRegistry.new()
	var ctx_a = AudioRNGContext.new(BASE_SEED, registry_a)
	var ctx_b = AudioRNGContext.new(BASE_SEED, registry_b)
	
	var generator = ToneBurstGenerator.new()
	var profile = _create_test_profile()
	var event = _create_test_event(100, 0)
	
	var result_a = generator.generate(profile, event, ctx_a)
	var result_b = generator.generate(profile, event, ctx_b)
	_assert(result_a.is_equal(result_b), "Fallo Determinismo: Entradas idénticas deben producir campos semánticos idénticos.")

	# --- Prueba C: Denegación de Capacidad usando Constantes y APIs Reales ---
	var registry_c = RNGStreamRegistry.new()
	var pitch_def = registry_c.get_definition(RNGStreamRegistry.STREAM_AUDIO_PITCH)
	_assert(pitch_def.get_domain() == RNGStreamRegistry.Domain.AUDIO, "Fallo Dominio: Pitch debe pertenecer estrictamente a DOMAIN_AUDIO.")
	_assert(not registry_c.is_consumer_authorized(RNGStreamRegistry.STREAM_AUDIO_PITCH, "VisualLoopRenderer"), "Fallo Capability: Visual Renderer NO debe tener acceso a streams de Audio.")
	_assert(not registry_c.is_consumer_authorized(RNGStreamRegistry.STREAM_VISUAL_LOOP_FRACTAL, CONSUMER), "Fallo Capability: Audio Generator NO debe tener acceso a streams Visuales.")

	# --- Prueba D: Variación Semántica ---
	var registry_d = RNGStreamRegistry.new()
	var result_base = generator.generate(_create_test_profile(), _create_test_event(100, 0), AudioRNGContext.new(BASE_SEED, registry_d))
	var result_alt = generator.generate(_create_test_profile(), _create_test_event(100, 0), AudioRNGContext.new(ALT_SEED, registry_d))
	_assert(not result_base.is_equal(result_alt), "Fallo Variación: Semillas distintas deben generar divergencia semántica en los parámetros.")

	# --- Prueba E: Aislamiento Real del SimulationResult (Clase RefCounted real) ---
	var canonical = _get_canonical_v2_fixture()
	
	var execution_a = ChallengeExecutionPipeline.execute(canonical)
	_assert(execution_a.get("success", false), "Fallo Pipeline A: " + str(execution_a.get("error", "")))
	var sim_result_a = execution_a.get("simulation_result")
	
	var registry_e = RNGStreamRegistry.new()
	var audio_ctx_e = AudioRNGContext.new(BASE_SEED, registry_e)
	var gen_e = ToneBurstGenerator.new()
	for i in range(150):
		gen_e.generate(_create_test_profile(), _create_test_event(i, 0), audio_ctx_e)
		
	var execution_b = ChallengeExecutionPipeline.execute(canonical)
	_assert(execution_b.get("success", false), "Fallo Pipeline B: " + str(execution_b.get("error", "")))
	var sim_result_b = execution_b.get("simulation_result")
	
	_assert(sim_result_a.score == sim_result_b.score, "Fallo Aislamiento: La presencia de Audio alteró el score de simulación.")
	_assert(sim_result_a.winning_frame == sim_result_b.winning_frame, "Fallo Aislamiento: La presencia de Audio alteró el winning_frame.")
	_assert(sim_result_a.minimum_distance == sim_result_b.minimum_distance, "Fallo Aislamiento: La presencia de Audio alteró minimum_distance.")
	_assert(sim_result_a.frames.size() == sim_result_b.frames.size(), "Fallo Aislamiento: La presencia de Audio alteró la longitud de frames.")

	# --- Prueba F: Inyectividad Matemática del Índice y Límites LCG ---
	var i1 = AudioRNGContext.get_deterministic_index(0, 0, 0)
	var i2 = AudioRNGContext.get_deterministic_index(0, 0, 1)
	var i3 = AudioRNGContext.get_deterministic_index(0, 1, 0)
	var i4 = AudioRNGContext.get_deterministic_index(1, 0, 0)
	var i5 = AudioRNGContext.get_deterministic_index(AudioRNGContext.MAX_TICK, 0, 0)
	var i6 = AudioRNGContext.get_deterministic_index(0, AudioRNGContext.MAX_SEQUENCE, 0)
	var i7 = AudioRNGContext.get_deterministic_index(0, 0, AudioRNGContext.MAX_OFFSET)
	var i8 = AudioRNGContext.get_deterministic_index(AudioRNGContext.MAX_TICK, AudioRNGContext.MAX_SEQUENCE, AudioRNGContext.MAX_OFFSET)
	
	var indices = [i1, i2, i3, i4, i5, i6, i7, i8]
	var unique_indices = {}
	for val in indices:
		_assert(not unique_indices.has(val), "Fallo Inyectividad: Colisión de índice detectada para el valor index: " + str(val))
		unique_indices[val] = true
		
	_assert((i8 + 1) < 9223372036854775807, "Fallo Desbordamiento LCG: El índice máximo empaquetado debe dejar espacio libre para index + 1.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C7A01_AUDIO_DETERMINISM_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C7A01_AUDIO_DETERMINISM_SUITE] FAIL failures=%d" % failures.size())
		quit(1)