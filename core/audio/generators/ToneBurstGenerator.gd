class_name ToneBurstGenerator
extends RefCounted

const CONSUMER_ID = "ToneBurstGenerator"
const OFFSET_PRIMARY_PITCH = 0

func generate(profile: AudioProfile, event: AudioEvent, rng_context: AudioRNGContext) -> AudioGenerationResult:
	_validate_schema(profile.parameters)
	
	var payload_ratio = 1.0
	if event.dynamic_payload.has("pitch_ratio"):
		var val = event.dynamic_payload["pitch_ratio"]
		assert(typeof(val) in [TYPE_INT, TYPE_FLOAT], "pitch_ratio debe ser numérico")
		payload_ratio = float(val)
		assert(payload_ratio > 0.0, "pitch_ratio debe ser estrictamente positivo")
	
	var random_modulation = rng_context.sample_float(RNGStreamRegistry.STREAM_AUDIO_PITCH, event, OFFSET_PRIMARY_PITCH, CONSUMER_ID) * 0.1
	
	var base_freq = float(profile.parameters["frequency_hz"])
	var final_freq = base_freq * payload_ratio * (1.0 + random_modulation)
	
	var frames = int(profile.parameters["attack_frames"]) + int(profile.parameters["release_frames"])
	
	return AudioGenerationResult.new(
		profile.generator_type,
		profile.profile_id,
		frames,
		{
			"final_frequency": final_freq,
			"amplitude": float(profile.parameters["amplitude"]),
			"attack_frames": int(profile.parameters["attack_frames"]),
			"release_frames": int(profile.parameters["release_frames"])
		}
	)

func _validate_schema(params: Dictionary):
	assert(params.has("frequency_hz") and typeof(params["frequency_hz"]) in [TYPE_INT, TYPE_FLOAT], "frequency_hz ausente/inválido")
	assert(float(params["frequency_hz"]) > 0.0, "frequency_hz debe ser > 0")
	
	assert(params.has("amplitude") and typeof(params["amplitude"]) in [TYPE_INT, TYPE_FLOAT], "amplitude ausente/inválido")
	var amp = float(params["amplitude"])
	assert(amp >= 0.0 and amp <= 1.0, "amplitude debe estar en rango [0.0, 1.0]")
	
	assert(params.has("attack_frames") and typeof(params["attack_frames"]) == TYPE_INT, "attack_frames ausente/inválido")
	assert(int(params["attack_frames"]) >= 0, "attack_frames no puede ser negativo")
	
	assert(params.has("release_frames") and typeof(params["release_frames"]) == TYPE_INT, "release_frames ausente/inválido")
	assert(int(params["release_frames"]) >= 0, "release_frames no puede ser negativo")