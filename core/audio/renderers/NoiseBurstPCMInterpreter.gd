# core/audio/renderers/NoiseBurstPCMInterpreter.gd
class_name NoiseBurstPCMInterpreter
extends RefCounted

const SAMPLE_RATE = 44100
const ENGINE_FPS = 60
const SAMPLES_PER_FRAME = 735

static func render(result: AudioGenerationResult) -> AudioBuffer:
	assert(
		result.generator_type == "noise_burst",
		"NoiseBurstPCMInterpreter solo procesa generadores 'noise_burst'"
	)

	var amplitude := float(result.deterministic_parameters["amplitude"])
	var attack_frames := int(result.deterministic_parameters["attack_frames"])
	var release_frames := int(result.deterministic_parameters["release_frames"])
	var noise_seed := int(result.deterministic_parameters["noise_seed"])

	var total_frames := result.duration_frames
	var total_samples := total_frames * SAMPLES_PER_FRAME

	var attack_samples := attack_frames * SAMPLES_PER_FRAME
	var release_samples := release_frames * SAMPLES_PER_FRAME
	var sustain_samples := total_samples - attack_samples - release_samples

	assert(amplitude >= 0.0 and amplitude <= 1.0)
	assert(attack_samples >= 0)
	assert(release_samples >= 0)
	assert(sustain_samples >= 0)

	var buffer := AudioBuffer.new(SAMPLE_RATE, 1)
	buffer.data.resize(total_samples)

	var seed_phase := float(noise_seed) / 2147483647.0

	for i in range(total_samples):
		var noise := _noise_sample(i, seed_phase)

		var envelope := 1.0

		if i < attack_samples and attack_samples > 0:
			envelope = float(i) / float(attack_samples)
		elif i >= total_samples - release_samples and release_samples > 0:
			var samples_from_end := total_samples - i
			envelope = float(samples_from_end) / float(release_samples)

		buffer.data[i] = clampf(
			noise * amplitude * envelope,
			-1.0,
			1.0
		)

	return buffer

static func _noise_sample(index: int, seed_phase: float) -> float:
	var x := float(index + 1)
	var value := sin(
		(x + seed_phase) * 12.9898
		+ seed_phase * 78.233
	) * 43758.5453

	var fractional: float = value - floor(value)

	return fractional * 2.0 - 1.0