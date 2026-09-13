# core/audio/renderers/ToneBurstPCMInterpreter.gd
class_name ToneBurstPCMInterpreter
extends RefCounted

const SAMPLE_RATE = 44100
const ENGINE_FPS = 60
const SAMPLES_PER_FRAME = 735 # Relación exacta: 44100 / 60

# Renderiza el plan acústico de manera 100% determinista y pura
static func render(result: AudioGenerationResult) -> AudioBuffer:
	assert(result.generator_type == "tone_burst", "ToneBurstPCMInterpreter solo procesa generadores 'tone_burst'")
	
	var freq = float(result.deterministic_parameters["final_frequency"])
	var amp = float(result.deterministic_parameters["amplitude"])
	var attack_frames = int(result.deterministic_parameters["attack_frames"])
	var release_frames = int(result.deterministic_parameters["release_frames"])
	var total_frames = result.duration_frames
	
	# La duración total en muestras debe derivarse de forma entera y estricta
	var total_samples = total_frames * SAMPLES_PER_FRAME
	var attack_samples = attack_frames * SAMPLES_PER_FRAME
	var release_samples = release_frames * SAMPLES_PER_FRAME
	var sustain_samples = total_samples - attack_samples - release_samples
	assert(sustain_samples >= 0, "Duración de ataque y liberación excede la duración total del plan acústico")
	
	var buffer = AudioBuffer.new(SAMPLE_RATE, 1)
	buffer.data.resize(total_samples)
	
	var sample_index = 0
	
	# 1. Fase de Ataque (AR - Attack)
	for i in range(attack_samples):
		var t = float(sample_index) / float(SAMPLE_RATE)
		var wave = sin(2.0 * PI * freq * t)
		var envelope = 0.0
		if attack_samples > 0:
			envelope = float(i) / float(attack_samples)
		buffer.data[sample_index] = wave * amp * envelope
		sample_index += 1
		
	# 2. Fase de Sustain implícito a 1.0
	for i in range(sustain_samples):
		var t = float(sample_index) / float(SAMPLE_RATE)
		var wave = sin(2.0 * PI * freq * t)
		buffer.data[sample_index] = wave * amp * 1.0
		sample_index += 1
		
	# 3. Fase de Relajación (AR - Release)
	for i in range(release_samples):
		var t = float(sample_index) / float(SAMPLE_RATE)
		var wave = sin(2.0 * PI * freq * t)
		var envelope = 1.0
		if release_samples > 0:
			var progress = float(release_samples - i) / float(release_samples)
			envelope = clampf(progress, 0.0, 1.0)
		buffer.data[sample_index] = wave * amp * envelope
		sample_index += 1
		
	return buffer