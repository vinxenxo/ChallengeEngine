class_name RNGStreamRegistry
extends RefCounted

enum Domain {
	STRUCTURAL_MAIN = 0,
	STRUCTURAL_SECONDARY = 1,
	PRESENTATION = 2,
	COSMETIC_CONTENT = 3
}

const STREAM_TRAJECTORY: int = 10
const STREAM_CONTROL: int = 20
const STREAM_PARTICLES: int = 1010

var _definitions: Dictionary = {}

func _init() -> void:
	_register(STREAM_TRAJECTORY, "TRAJECTORY", Domain.STRUCTURAL_MAIN, "SimulationCore", "frame", "2.0", ["PilotMechanic"])
	_register(STREAM_CONTROL, "CONTROL", Domain.STRUCTURAL_MAIN, "SimulationCore", "frame", "2.0", ["PilotMechanic"])
	_register(STREAM_PARTICLES, "PARTICLES", Domain.PRESENTATION, "PresentationCore", "entity_id", "2.0", ["PilotVisuals"])

func _register(p_id: int, p_name: String, p_domain: Domain, p_owner: String, p_semantics: String, p_version: String, p_consumers: Array[String]) -> void:
	_definitions[p_id] = RNGStreamDefinition.new(
		p_id,
		p_name,
		p_domain,
		p_owner,
		p_semantics,
		p_version,
		p_consumers
	)

func is_registered(stream_id: int) -> bool:
	return _definitions.has(stream_id)

func get_definition(stream_id: int) -> RNGStreamDefinition:
	if is_registered(stream_id):
		return _definitions[stream_id]
	return null

func is_consumer_authorized(stream_id: int, consumer_id: String) -> bool:
	var definition: RNGStreamDefinition = get_definition(stream_id)
	if definition == null:
		return false
	return consumer_id in definition.get_allowed_consumers()
