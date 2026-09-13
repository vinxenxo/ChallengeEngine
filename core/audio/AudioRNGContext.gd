# res://core/audio/AudioRNGContext.gd
class_name AudioRNGContext
extends RefCounted

const MAX_TICK: int = 2147483646
const MAX_SEQUENCE: int = 65535
const MAX_OFFSET: int = 65535

var _master_seed: int
var _registry: RNGStreamRegistry

func _init(seed: int, registry: RNGStreamRegistry):
	_master_seed = seed
	_registry = registry

static func get_deterministic_index(tick: int, sequence: int, offset: int) -> int:
	assert(tick >= 0 and tick <= MAX_TICK, "Tick fuera de rango seguro [0, 2147483646]")
	assert(sequence >= 0 and sequence <= MAX_SEQUENCE, "Sequence fuera de rango [0, 65535]")
	assert(offset >= 0 and offset <= MAX_OFFSET, "Offset fuera de rango [0, 65535]")
	
	return (tick << 32) | (sequence << 16) | offset

func sample_float(stream_id: int, event: AudioEvent, offset: int, consumer_id: String) -> float:
	assert(_registry.is_registered(stream_id), "CRITICAL: Stream no registrado: " + str(stream_id))
	
	var definition = _registry.get_definition(stream_id)
	assert(definition.get_domain() == RNGStreamRegistry.Domain.AUDIO, "CRITICAL: Violación de dominio. El stream no pertenece a AUDIO.")
	assert(_registry.is_consumer_authorized(stream_id, consumer_id), "CRITICAL: Consumidor '" + consumer_id + "' no autorizado.")
	
	var index = AudioRNGContext.get_deterministic_index(event.tick, event.sequence, offset)
	return DeterministicLCG.sample_float(_master_seed, stream_id, index)