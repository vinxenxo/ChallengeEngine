class_name NoiseBurstGenerator
extends RefCounted

const CONSUMER_ID = "NoiseBurstGenerator"
const OFFSET_NOISE_SEED = 0

func generate(
	profile: AudioProfile,
	event: AudioEvent,
	rng_context: AudioRNGContext
) -> AudioGenerationResult:
	assert(profile != null, "profile no puede ser null")
	assert(event != null, "event no puede ser null")
	assert(rng_context != null, "rng_context no puede ser null")

	_validate_schema(profile.parameters)

	var seed_float := rng_context.sample_float(
		RNGStreamRegistry.STREAM_AUDIO_NOISE,
		event,
		OFFSET_NOISE_SEED,
		CONSUMER_ID
	)

	var noise_seed := int(seed_float * 2147483647.0)

	var duration_frames: int = int(profile.parameters["duration_frames"])
	var amplitude: float = float(profile.parameters["amplitude"])
	var attack_frames: int = int(profile.parameters["attack_frames"])
	var release_frames: int = int(profile.parameters["release_frames"])

	assert(
		attack_frames + release_frames <= duration_frames,
		"attack_frames + release_frames no puede exceder duration_frames"
	)

	return AudioGenerationResult.new(
		profile.generator_type,
		profile.profile_id,
		duration_frames,
		{
			"amplitude": amplitude,
			"attack_frames": attack_frames,
			"release_frames": release_frames,
			"noise_seed": noise_seed
		}
	)

func _validate_schema(params: Dictionary) -> void:
	assert(
		params.has("amplitude")
		and typeof(params["amplitude"]) in [TYPE_INT, TYPE_FLOAT],
		"amplitude ausente/inválido"
	)

	var amplitude := float(params["amplitude"])

	assert(
		amplitude >= 0.0 and amplitude <= 1.0,
		"amplitude debe estar en rango [0.0, 1.0]"
	)

	assert(
		params.has("duration_frames")
		and typeof(params["duration_frames"]) == TYPE_INT,
		"duration_frames ausente/inválido"
	)

	assert(
		int(params["duration_frames"]) > 0,
		"duration_frames debe ser > 0"
	)

	assert(
		params.has("attack_frames")
		and typeof(params["attack_frames"]) == TYPE_INT,
		"attack_frames ausente/inválido"
	)

	assert(
		int(params["attack_frames"]) >= 0,
		"attack_frames no puede ser negativo"
	)

	assert(
		params.has("release_frames")
		and typeof(params["release_frames"]) == TYPE_INT,
		"release_frames ausente/inválido"
	)

	assert(
		int(params["release_frames"]) >= 0,
		"release_frames no puede ser negativo"
	)