# tests/C7A06MultiGeneratorDeterminismTest.gd
extends SceneTree

const AudioGeneratorRegistry = preload(
	"res://core/audio/AudioGeneratorRegistry.gd"
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
const NoiseBurstPCMInterpreter = preload(
	"res://core/audio/renderers/NoiseBurstPCMInterpreter.gd"
)
const ToneBurstGenerator = preload(
	"res://core/audio/generators/ToneBurstGenerator.gd"
)
const ToneBurstPCMInterpreter = preload(
	"res://core/audio/renderers/ToneBurstPCMInterpreter.gd"
)

var failures: Array[String] = []


func _init() -> void:
	print("[C7A06-TEST] Iniciando verificación multi-generador y aislamiento RNG...")
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

	_assert(
		registry.is_registered("noise_burst"),
		"noise_burst debe estar registrado en el registry."
	)
	_assert(
		registry.is_registered("tone_burst"),
		"tone_burst debe mantenerse registrado en el registry."
	)

	var noise_profile := AudioProfile.new(
		"test_noise_profile",
		"noise_burst",
		{
			"amplitude": 0.8,
			"duration_frames": 10,
			"attack_frames": 2,
			"release_frames": 8
		}
	)

	var tone_profile := AudioProfile.new(
		"test_tone_profile",
		"tone_burst",
		{
			"frequency_hz": 440.0,
			"amplitude": 0.5,
			"attack_frames": 5,
			"release_frames": 10
		}
	)

	var event := AudioEvent.new("test_event", 0, 0, {})

	# =========================================================
	# 1. A == A: Misma semilla -> Idéntico resultado (Noise)
	# =========================================================
	var ctx_a1 := AudioRNGContext.new(999, RNGStreamRegistry.new())
	var res_a1 = registry.generate("noise_burst", noise_profile, event, ctx_a1)

	var ctx_a2 := AudioRNGContext.new(999, RNGStreamRegistry.new())
	var res_a2 = registry.generate("noise_burst", noise_profile, event, ctx_a2)

	_assert(res_a1 != null and res_a2 != null, "Generación noise no nula.")
	_assert(
		res_a1.deterministic_parameters["noise_seed"]
		== res_a2.deterministic_parameters["noise_seed"],
		"Misma semilla maestro debe producir idéntico noise_seed."
	)

	var buf_a1 = NoiseBurstPCMInterpreter.render(res_a1)
	var buf_a2 = NoiseBurstPCMInterpreter.render(res_a2)
	_assert(
		buf_a1.get_canonical_hash() == buf_a2.get_canonical_hash(),
		"Misma semilla maestro debe producir hashes PCM idénticos (A == A)."
	)

	# =========================================================
	# 2. A != B: Semilla distinta -> Resultado distinto (Noise)
	# =========================================================
	var ctx_b := AudioRNGContext.new(888, RNGStreamRegistry.new())
	var res_b = registry.generate("noise_burst", noise_profile, event, ctx_b)
	var buf_b = NoiseBurstPCMInterpreter.render(res_b)

	_assert(
		buf_a1.get_canonical_hash() != buf_b.get_canonical_hash(),
		"Semillas distintas deben producir salidas PCM diferentes (A != B)."
	)

	# =========================================================
	# 3. Aislamiento cruzado: ToneBurst no contamina NoiseBurst
	# =========================================================
	var ctx_mixed1 := AudioRNGContext.new(777, RNGStreamRegistry.new())
	var tone_res = registry.generate("tone_burst", tone_profile, event, ctx_mixed1)
	var noise_res_isolated = registry.generate("noise_burst", noise_profile, event, ctx_mixed1)

	var ctx_mixed2 := AudioRNGContext.new(777, RNGStreamRegistry.new())
	var noise_res_standalone = registry.generate("noise_burst", noise_profile, event, ctx_mixed2)

	_assert(tone_res != null, "ToneBurst generado correctamente en contexto mixto.")
	_assert(noise_res_isolated != null, "NoiseBurst generado en contexto mixto.")
	_assert(noise_res_standalone != null, "NoiseBurst generado en contexto standalone.")

	var buf_isolated = NoiseBurstPCMInterpreter.render(noise_res_isolated)
	var buf_standalone = NoiseBurstPCMInterpreter.render(noise_res_standalone)

	_assert(
		buf_isolated.get_canonical_hash() == buf_standalone.get_canonical_hash(),
		"Ejecutar ToneBurst antes no debe alterar el stream RNG ni el resultado de NoiseBurst."
	)


func _conclude() -> void:
	if failures.is_empty():
		print("[C7A06-TEST] RESULTADO GLOBAL: PASS")
		quit(0)
	else:
		push_error(
			"[C7A06-TEST] RESULTADO GLOBAL: FAIL failures=%d"
			% failures.size()
		)
		quit(1)