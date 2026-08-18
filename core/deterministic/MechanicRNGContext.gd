class_name MechanicRNGContext
extends RefCounted

class CreationResult:
	var is_valid: bool = false
	var context = null # Evita autorreferencia tipada estricta para prevenir problemas del parser
	var error_code: String = "OK"

var _seed: int
var _rng_version: String
var _consumer_id: String
var _allowed_streams: Array[int]
var _rng: StructuralRNG
var error_state: String = "OK"

func _init(seed: int, rng_version: String, consumer_id: String, allowed_streams: Array[int], rng: StructuralRNG) -> void:
	_seed = seed
	_rng_version = rng_version
	_consumer_id = consumer_id
	_allowed_streams = allowed_streams.duplicate()
	_rng = rng

static func create(seed: int, rng_version: String, consumer_id: String, allowed_streams: Array[int], rng: StructuralRNG, registry: RNGStreamRegistry) -> CreationResult:
	var result = CreationResult.new()
	
	if rng_version != "2.0":
		result.error_code = "RNG_VERSION_UNSUPPORTED"
		return result

	var seen: Dictionary = {}
	for s_id in allowed_streams:
		if seen.has(s_id):
			result.error_code = "RNG_CONTEXT_INVALID"
			return result
		seen[s_id] = true

	for stream_id in allowed_streams:
		var def: RNGStreamDefinition = registry.get_definition(stream_id)
		if def == null:
			result.error_code = "RNG_CONTEXT_INVALID"
			return result
		if def.get_domain() != RNGStreamRegistry.Domain.STRUCTURAL_MAIN and def.get_domain() != RNGStreamRegistry.Domain.STRUCTURAL_SECONDARY:
			result.error_code = "RNG_CONTEXT_INVALID"
			return result
		if not registry.is_consumer_authorized(stream_id, consumer_id):
			result.error_code = "RNG_CONTEXT_INVALID"
			return result

	result.is_valid = true
	result.context = MechanicRNGContext.new(seed, rng_version, consumer_id, allowed_streams, rng)
	return result

func sample_float(stream_id: int, index: int) -> float:
	if index < 0:
		error_state = "RNG_INDEX_INVALID"
		push_error(error_state)
		return NAN
	if not stream_id in _allowed_streams:
		error_state = "RNG_CONSUMER_NOT_AUTHORIZED"
		push_error(error_state)
		return NAN
	return _rng.sample_float(_seed, stream_id, index)

func sample_integer(stream_id: int, index: int) -> int:
	if index < 0:
		error_state = "RNG_INDEX_INVALID"
		push_error(error_state)
		return -1
	if not stream_id in _allowed_streams:
		error_state = "RNG_CONSUMER_NOT_AUTHORIZED"
		push_error(error_state)
		return -1
	return _rng.sample_integer(_seed, stream_id, index)

func sample_float_range(stream_id: int, index: int, min_val: float, max_val: float) -> float:
	if index < 0:
		error_state = "RNG_INDEX_INVALID"
		push_error(error_state)
		return NAN
	if not stream_id in _allowed_streams:
		error_state = "RNG_CONSUMER_NOT_AUTHORIZED"
		push_error(error_state)
		return NAN
	return _rng.sample_float_range(_seed, stream_id, index, min_val, max_val)