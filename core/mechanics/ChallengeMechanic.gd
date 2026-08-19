class_name ChallengeMechanic
extends RefCounted

## Configura los parámetros iniciales de la mecánica
func setup(_config: Dictionary) -> void:
	pass

## Recibe una capability RNG V2.0 cuando la mecánica la requiere.
## Las mecánicas V1.0 no tienen que sobrescribir este método.
func set_rng_context(_context: MechanicRNGContext) -> void:
	pass

## Ejecuta la simulación determinista en CPU
func simulate(_total_game_frames: int, _local_seed: int, _config: Dictionary) -> SimulationResult:
	push_error("ChallengeMechanic.simulate() debe ser implementado por subclases.")
	return null
