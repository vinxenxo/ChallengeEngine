# tests/audio/C7A02AudioPCMHashTest.gd
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

func _initialize() -> void:
	print("[TEST] Running C7A02AudioPCMHashTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	# 1. Configuración de prueba con amplitud superior a 1.0 para probar clamping
	var params = {
		"final_frequency": 440.0,
		"amplitude": 1.2, # Supera el rango normalizado para probar el clamping defensivo
		"attack_frames": 5,
		"release_frames": 10
	}
	var total_frames_contract = 30
	var result_a = AudioGenerationResult.new("tone_burst", "test_profile", total_frames_contract, params)
	var result_b = AudioGenerationResult.new("tone_burst", "test_profile", total_frames_contract, params)
	
	# 2. Renderizado físico puro
	var buffer_a = ToneBurstPCMInterpreter.render(result_a)
	var buffer_b = ToneBurstPCMInterpreter.render(result_b)
	
	# 3. Certificación de integridad temporal estricta derivada del contrato
	var expected_samples = total_frames_contract * ToneBurstPCMInterpreter.SAMPLES_PER_FRAME
	_assert(buffer_a.data.size() == expected_samples, "Fallo Integridad Temporal: El número de muestras no coincide con el contrato de frames.")
	
	# 4. Certificación de determinismo bit-a-bit mediante Hash SHA-256 canónico
	var hash_a = buffer_a.get_canonical_hash()
	var hash_b = buffer_b.get_canonical_hash()
	_assert(hash_a == hash_b, "Fallo PCM Bit-Exact: Dos renders del mismo plan deben arrojar idéntico hash SHA-256.")
	_assert(hash_a.length() == 64, "Fallo Hash: El hash canónico debe ser una cadena SHA-256 de 64 caracteres.")
	
	# 5. Validación rigurosa de Clamping y Cuantización Simétrica PCM16
	var pcm_bytes = buffer_a.get_pcm16_bytes()
	_assert(pcm_bytes.size() == expected_samples * 2, "Fallo de Bytes: El tamaño del PackedByteArray PCM16 debe ser exactamente el doble de muestras.")
	
	# Comprobación de que ningún valor crudo flotante supera los límites lógicos [-1.0, 1.0] tras el render
	for sample in buffer_a.data:
		_assert(sample >= -1.0 and sample <= 1.0, "Fallo Clamping Físico: El buffer contiene muestras fuera del rango normalizado tras aplicar amplitud.")