# tests/C7A05AudioGeneratorRegistryTest.gd
extends SceneTree

const AudioGeneratorRegistry = preload(
	"res://core/audio/AudioGeneratorRegistry.gd"
)
const ToneBurstGenerator = preload(
	"res://core/audio/generators/ToneBurstGenerator.gd"
)
const AudioProfileAdapter = preload(
	"res://core/audio/AudioProfileAdapter.gd"
)
const AudioProfile = preload(
	"res://core/audio/AudioProfile.gd"
)
const AudioEvent = preload(
	"res://core/audio/AudioEvent.gd"
)
const AudioRNGContext = preload(
	"res://core/audio/AudioRNGContext.gd"
)
const RNGStreamRegistry = preload(
	"res://core/deterministic/RNGStreamRegistry.gd"
)
const ToneBurstPCMInterpreter = preload(
	"res://core/audio/renderers/ToneBurstPCMInterpreter.gd"
)

var failures: Array[String] = []


func _init() -> void:
	print("[C7A05-TEST] Iniciando verificación estricta de AudioGeneratorRegistry...")

	_run_tests()
	_conclude()


func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
		print("[FAIL] " + message)
	else:
		print("[PASS] " + message)


func _run_tests() -> void:
	var registry := AudioGeneratorRegistry.new()

	# =========================================================
	# 1. Registro obligatorio
	# =========================================================
	_assert(
		registry.is_registered("tone_burst"),
		"tone_burst debe estar registrado por defecto."
	)

	# =========================================================
	# 2. Resolver un AudioProfile REAL de producción
	# =========================================================
	var valid_profile: AudioProfile = (
		AudioProfileAdapter.from_authoring_profile(
			"c7_test_profile",
			"countdown_tick"
		)
	)

	_assert(
		valid_profile != null,
		"AudioProfileAdapter debe resolver c7_test_profile/countdown_tick."
	)

	if valid_profile == null:
		return

	_assert(
		valid_profile.generator_type == "tone_burst",
		"El perfil resuelto debe declarar generator_type=tone_burst."
	)

	# =========================================================
	# 3. Evento real compatible con el perfil
	# =========================================================
	var valid_event := AudioEvent.new(
		"countdown_tick",
		0,
		0,
		{}
	)

	# =========================================================
	# 4. Unknown generator -> FAIL-CLOSED
	# =========================================================
	var unknown_rng_context := AudioRNGContext.new(
		12345,
		RNGStreamRegistry.new()
	)

	var unknown_result = registry.generate(
		"unknown_type",
		valid_profile,
		valid_event,
		unknown_rng_context
	)

	_assert(
		unknown_result == null,
		"generator_type desconocido debe devolver null (FAIL-CLOSED)."
	)

	# =========================================================
	# 5. Generación directa del generador
	# =========================================================
	var direct_rng_context := AudioRNGContext.new(
		12345,
		RNGStreamRegistry.new()
	)

	var direct_generator := ToneBurstGenerator.new()

	var direct_result = direct_generator.generate(
		valid_profile,
		valid_event,
		direct_rng_context
	)

	_assert(
		direct_result != null,
		"ToneBurstGenerator directo debe generar un AudioGenerationResult."
	)

	if direct_result == null:
		return

	# =========================================================
	# 6. Generación mediante registry
	# =========================================================
	var registry_rng_context := AudioRNGContext.new(
		12345,
		RNGStreamRegistry.new()
	)

	var registry_result = registry.generate(
		"tone_burst",
		valid_profile,
		valid_event,
		registry_rng_context
	)

	_assert(
		registry_result != null,
		"AudioGeneratorRegistry debe generar mediante tone_burst."
	)

	if registry_result == null:
		return

	# =========================================================
	# 7. Paridad semántica básica
	# =========================================================
	_assert(
		direct_result.generator_type == registry_result.generator_type,
		"generator_type debe coincidir entre generación directa y registry."
	)

	_assert(
		direct_result.profile_id == registry_result.profile_id,
		"profile_id debe coincidir entre generación directa y registry."
	)

	_assert(
		direct_result.duration_frames == registry_result.duration_frames,
		"duration_frames debe coincidir entre generación directa y registry."
	)

	_assert(
		direct_result.deterministic_parameters
		== registry_result.deterministic_parameters,
		"deterministic_parameters debe coincidir entre generación directa y registry."
	)

	# =========================================================
	# 8. Paridad física del resultado interpretado
	# =========================================================
	var direct_buffer = ToneBurstPCMInterpreter.render(
		direct_result
	)

	var registry_buffer = ToneBurstPCMInterpreter.render(
		registry_result
	)

	_assert(
		direct_buffer != null,
		"El resultado directo debe poder interpretarse a PCM."
	)

	_assert(
		registry_buffer != null,
		"El resultado del registry debe poder interpretarse a PCM."
	)

	if direct_buffer == null or registry_buffer == null:
		return

	_assert(
		direct_buffer.get_canonical_hash()
		== registry_buffer.get_canonical_hash(),
		"Registry y generación directa deben producir PCM bit-exact equivalente."
	)


func _conclude() -> void:
	if failures.is_empty():
		print("[C7A05-TEST] RESULTADO GLOBAL: PASS")
		quit(0)
	else:
		push_error(
			"[C7A05-TEST] RESULTADO GLOBAL: FAIL failures=%d"
			% failures.size()
		)
		quit(1)