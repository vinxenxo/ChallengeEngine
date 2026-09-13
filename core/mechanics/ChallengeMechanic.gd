# res://core/mechanics/ChallengeMechanic.gd
class_name ChallengeMechanic
extends RefCounted

# Unified lifecycle state (C3-T1)
var _is_setup: bool = false
var _is_prepared: bool = false
var _error_state: String = "OK"

## Configura los parámetros iniciales de la mecánica
func setup(_config: Dictionary) -> void:
	pass

# Hook virtual para consulta de capabilities de preparación temporal
func requires_temporal_preparation() -> bool:
	return false

# Hook virtual para preparación de estado temporal indexado por frame (C3-T)
func prepare(_total_frames: int) -> void:
	pass

## Recibe una capability RNG V2.0 cuando la mecánica la requiere.
## Las mecánicas V1.0 no tienen que sobrescribir este método.
func set_rng_context(_context: MechanicRNGContext) -> void:
	pass

## Ejecuta la simulación determinista en CPU
func simulate(_total_game_frames: int, _local_seed: int, _config: Dictionary) -> SimulationResult:
	push_error("ChallengeMechanic.simulate() debe ser implementado por subclases.")
	return null
