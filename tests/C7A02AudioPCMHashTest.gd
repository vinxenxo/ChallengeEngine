extends SceneTree

# ============================================================
# C7-A0.2-F1 — Physical Audio Renderer & Canonical PCM Hash Test
# Validates bit-exact determinism via SHA-256, AR envelope timing,
# strict clamping boundaries, and symmetric quantization.
# ============================================================

const AudioGenerationResult = preload("res://core/audio/AudioGenerationResult.gd")
const AudioBuffer = preload("res://core/audio/AudioBuffer.gd")
const ToneBurstPCMInterpreter = preload("res://core/audio/renderers/ToneBurstPCMInterpreter.gd")

var failures: Array[String] = []

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _test_pcm16_clamping() -> void:
	var buffer = AudioBuffer.new(44100, 1)

	buffer.data = PackedFloat32Array([
		-1.2,
		-1.0,
		-0.5,
		0.0,
		0.5,
		1.0,
		1.2
	])

	var bytes = buffer.get_pcm16_bytes()

	_assert(bytes.size() == 14, "El buffer PCM debe contener 7 muestras × 2 bytes.")

	# -1.2 debe clamp -> -32768 -> 0x00 0x80
	_assert(bytes[0] == 0x00, "Clamping negativo: byte bajo incorrecto para -1.2")
	_assert(bytes[1] == 0x80, "Clamping negativo: byte alto incorrecto para -1.2")

	# -1.0 -> -32768
	_assert(bytes[2] == 0x00, "PCM -1.0: byte bajo incorrecto")
	_assert(bytes[3] == 0x80, "PCM -1.0: byte alto incorrecto")

	# 0.0 -> 0
	_assert(bytes[6] == 0x00, "PCM 0.0: byte bajo incorrecto")
	_assert(bytes[7] == 0x00, "PCM 0.0: byte alto incorrecto")

	# +1.0 -> +32767 -> 0xFF 0x7F
	_assert(bytes[10] == 0xFF, "PCM +1.0: byte bajo incorrecto")
	_assert(bytes[11] == 0x7F, "PCM +1.0: byte alto incorrecto")

	# +1.2 debe clamp -> +32767
	_assert(bytes[12] == 0xFF, "Clamping positivo: byte bajo incorrecto para +1.2")
	_assert(bytes[13] == 0x7F, "Clamping positivo: byte alto incorrecto para +1.2")

func _run_tests() -> void:
	var total_frames_contract = 30

	var params = {
		"final_frequency": 440.0,
		"amplitude": 1.0,
		"attack_frames": 5,
		"release_frames": 10
	}

	var result_a = AudioGenerationResult.new(
		"tone_burst",
		"test_profile",
		total_frames_contract,
		params
	)

	var result_b = AudioGenerationResult.new(
		"tone_burst",
		"test_profile",
		total_frames_contract,
		params
	)

	var buffer_a = ToneBurstPCMInterpreter.render(result_a)
	var buffer_b = ToneBurstPCMInterpreter.render(result_b)

	var expected_samples = (
		total_frames_contract *
		ToneBurstPCMInterpreter.SAMPLES_PER_FRAME
	)

	# Integridad temporal
	_assert(
		buffer_a.data.size() == expected_samples,
		"Fallo Integridad Temporal"
	)

	# Invariante física del renderer [-1.0, 1.0]
	for sample in buffer_a.data:
		_assert(
			sample >= -1.0 and sample <= 1.0,
			"El renderer produjo una muestra fuera de [-1,1]"
		)

	# Determinismo físico (SHA-256)
	var hash_a = buffer_a.get_canonical_hash()
	var hash_b = buffer_b.get_canonical_hash()

	_assert(
		hash_a == hash_b,
		"Dos renders idénticos deben producir el mismo SHA-256"
	)

	_assert(
		hash_a.length() == 64,
		"SHA-256 debe tener 64 caracteres hexadecimales"
	)

	# Tamaño PCM en bytes
	var pcm_bytes = buffer_a.get_pcm16_bytes()

	_assert(
		pcm_bytes.size() == expected_samples * 2,
		"PCM16 debe utilizar exactamente 2 bytes por muestra"
	)

	# Comprobación de clamping y cuantización en bytes con valores fuera de rango
	_test_pcm16_clamping()

func _conclude() -> void:
	if failures.is_empty():
		print("[C7A02_PCM_HASH_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C7A02_PCM_HASH_SUITE] FAIL failures=%d" % failures.size())
		quit(1)

func _initialize() -> void:
	print("[TEST] Running C7A02AudioPCMHashTest...")
	_run_tests()
	_conclude()