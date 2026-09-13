# core/audio/AudioGeneratorRegistry.gd
class_name AudioGeneratorRegistry
extends RefCounted

const ToneBurstGenerator = preload("res://core/audio/generators/ToneBurstGenerator.gd")
const NoiseBurstGenerator = preload(
	"res://core/audio/generators/NoiseBurstGenerator.gd"
)

var _registry: Dictionary = {}

func _init() -> void:
	_register_default_generators()

func _register_default_generators() -> void:
	register_generator("tone_burst", ToneBurstGenerator.new())
	register_generator("noise_burst", NoiseBurstGenerator.new())

func register_generator(generator_type: String, generator_instance: RefCounted) -> bool:
	var key := generator_type.strip_edges()

	if key.is_empty():
		push_error("[AUDIO_REGISTRY] generator_type vacío.")
		return false

	if generator_instance == null:
		push_error(
			"[AUDIO_REGISTRY] No se puede registrar '%s': instancia nula."
			% key
		)
		return false

	if not generator_instance.has_method("generate"):
		push_error(
			"[AUDIO_REGISTRY] El generador '%s' no expone generate()."
			% key
		)
		return false

	_registry[key] = generator_instance
	return true

func is_registered(generator_type: String) -> bool:
	return _registry.has(generator_type)

func generate(
	generator_type: String,
	profile: AudioProfile,
	event: AudioEvent,
	rng_context: AudioRNGContext
) -> AudioGenerationResult:
	var key := generator_type.strip_edges()

	if key.is_empty():
		push_error("[AUDIO_REGISTRY] generator_type vacío.")
		return null

	if not _registry.has(key):
		push_error(
			"[AUDIO_REGISTRY] Fail-closed: generator_type no registrado '%s'."
			% key
		)
		return null

	var generator: RefCounted = _registry[key]

	if not generator.has_method("generate"):
		push_error(
			"[AUDIO_REGISTRY] Fail-closed: '%s' no tiene generate()."
			% key
		)
		return null

	return generator.generate(profile, event, rng_context)