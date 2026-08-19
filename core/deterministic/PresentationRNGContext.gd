class_name PresentationRNGContext
extends RefCounted

class CreationResult:
	var is_valid: bool = false
	var context = null
	var error_code: String = "OK"

var _seed: int
var _rng_version: String
var _consumer_id: String
var _allowed_streams: Array[int]
var _rng: CosmeticRNG
var error_state: String = "OK"

func _init(seed: int, rng_version: String, consumer_id: String, allowed_streams: Array[int], rng: CosmeticRNG) -> void:
	_seed = seed
	_rng_version = rng_version
	_consumer_id = consumer_id
	_allowed_streams = allowed_streams.duplicate()
	_rng = rng

static func create(seed: int, rng_version: String, consumer_id: String, allowed_streams: Array[int], rng: CosmeticRNG, registry: RNGStreamRegistry) -> CreationResult:
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
		if def.get_domain() != RNGStreamRegistry.Domain.PRESENTATION and def.get_domain() != RNGStreamRegistry.Domain.COSMETIC_CONTENT:
			result.error_code = "RNG_CONTEXT_INVALID"
			return result
		if not registry.is_consumer_authorized(stream_id, consumer_id):
			result.error_code = "RNG_CONTEXT_INVALID"
			return result

	result.is_valid = true
	result.context = PresentationRNGContext.new(seed, rng_version, consumer_id, allowed_streams, rng)
	return result

func sample_float(stream_id: int, index: int) -> float:
	if index < 0:
		error_state = "RNG_INDEX_INVALID"
		return NAN
	if not stream_id in _allowed_streams:
		error_state = "RNG_CONSUMER_NOT_AUTHORIZED"
		return NAN

	var val = _rng.sample_float(_seed, stream_id, index)
	if _rng.last_error != "OK":
		error_state = _rng.last_error
		return NAN

	error_state = "OK"
	return val

func sample_integer(stream_id: int, index: int) -> int:
	if index < 0:
		error_state = "RNG_INDEX_INVALID"
		return -1
	if not stream_id in _allowed_streams:
		error_state = "RNG_CONSUMER_NOT_AUTHORIZED"
		return -1

	var val = _rng.sample_integer(_seed, stream_id, index)
	if _rng.last_error != "OK":
		error_state = _rng.last_error
		return -1

	error_state = "OK"
	return val

func sample_float_range(stream_id: int, index: int, min_val: float, max_val: float) -> float:
	if index < 0:
		error_state = "RNG_INDEX_INVALID"
		return NAN
	if not stream_id in _allowed_streams:
		error_state = "RNG_CONSUMER_NOT_AUTHORIZED"
		return NAN

	var val = _rng.sample_float_range(_seed, stream_id, index, min_val, max_val)
	if _rng.last_error != "OK":
		error_state = _rng.last_error
		return NAN

	error_state = "OK"
	return val