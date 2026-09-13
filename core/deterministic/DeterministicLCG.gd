# res://core/deterministic/DeterministicLCG.gd
class_name DeterministicLCG
extends RefCounted

## Deterministic 31-bit LCG exposed as a stateless sampling API.
##
## RNG v1.0 compatibility is represented by stream_id=0 and a sequential
## index. RNG v2.0 uses semantic streams with explicit indices.

const MASK_31: int = 0x7fffffff
const MULTIPLIER: int = 1103515245
const INCREMENT: int = 12345
const NORMALIZER: float = 2147483647.0
const STREAM_MIXER: int = 2654435761

## Returns the LCG state corresponding to the requested zero-based sample.
## index=0 is exactly one nexti() transition from the supplied seed.
static func sample_integer(seed: int, stream_id: int, index: int) -> int:
	if index < 0:
		return 0

	var stream_seed: int = _derive_stream_seed(seed, stream_id)
	return _advance(stream_seed, index + 1)

static func sample_float(seed: int, stream_id: int, index: int) -> float:
	return float(sample_integer(seed, stream_id, index)) / NORMALIZER

static func sample_float_range(
	seed: int,
	stream_id: int,
	index: int,
	min_val: float,
	max_val: float
) -> float:
	return min_val + sample_float(seed, stream_id, index) * (max_val - min_val)

## Derives a deterministic initial state for a semantic stream.
## stream_id=0 is deliberately the historical seed so RNG v1.0 remains exact.
static func _derive_stream_seed(seed: int, stream_id: int) -> int:
	var normalized_seed: int = seed & MASK_31
	if stream_id == 0:
		return normalized_seed

	var normalized_stream: int = stream_id & MASK_31
	return (normalized_seed + normalized_stream * STREAM_MIXER) & MASK_31

## Applies n LCG transitions using affine exponentiation by squaring.
## The recurrence x' = MULTIPLIER*x + INCREMENT (mod 2^31) is composed
## without mutable generator state, so the result depends only on the inputs.
static func _advance(seed: int, steps: int) -> int:
	var result_multiplier: int = 1
	var result_increment: int = 0
	var current_multiplier: int = MULTIPLIER & MASK_31
	var current_increment: int = INCREMENT & MASK_31
	var remaining: int = steps

	while remaining > 0:
		if (remaining & 1) != 0:
			result_increment = (
				result_multiplier * current_increment
				+ result_increment
			) & MASK_31
			result_multiplier = (
				result_multiplier * current_multiplier
			) & MASK_31

		current_increment = (
			current_multiplier * current_increment
			+ current_increment
		) & MASK_31
		current_multiplier = (
			current_multiplier * current_multiplier
		) & MASK_31

		remaining >>= 1

	return (result_multiplier * (seed & MASK_31) + result_increment) & MASK_31
