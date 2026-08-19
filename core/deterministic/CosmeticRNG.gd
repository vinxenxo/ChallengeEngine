class_name CosmeticRNG
extends RefCounted

var _registry: RNGStreamRegistry
var last_error: String = "OK"

func _init(registry: RNGStreamRegistry) -> void:
	_registry = registry

func validate_stream(stream_id: int) -> String:
	if not _registry.is_registered(stream_id):
		return "RNG_STREAM_UNREGISTERED"
	var def = _registry.get_definition(stream_id)
	if def.get_domain() != RNGStreamRegistry.Domain.PRESENTATION and def.get_domain() != RNGStreamRegistry.Domain.COSMETIC_CONTENT:
		return "RNG_DOMAIN_VIOLATION"
	return "OK"

func sample_float(seed: int, stream_id: int, index: int) -> float:
	last_error = validate_stream(stream_id)
	if last_error != "OK":
		return NAN
	last_error = "OK"
	return DeterministicLCG.sample_float(seed, stream_id, index)

func sample_integer(seed: int, stream_id: int, index: int) -> int:
	last_error = validate_stream(stream_id)
	if last_error != "OK":
		return -1
	last_error = "OK"
	return DeterministicLCG.sample_integer(seed, stream_id, index)

func sample_float_range(seed: int, stream_id: int, index: int, min_val: float, max_val: float) -> float:
	last_error = validate_stream(stream_id)
	if last_error != "OK":
		return NAN
	last_error = "OK"
	return DeterministicLCG.sample_float_range(seed, stream_id, index, min_val, max_val)