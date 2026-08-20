class_name RNGStreamRegistry
extends RefCounted

enum Domain {
	STRUCTURAL_MAIN,
	STRUCTURAL_SECONDARY,
	PRESENTATION,
	COSMETIC_CONTENT
}

const STREAM_TRAJECTORY = 10
const STREAM_CONTROL = 20
const STREAM_PARTICLES = 1010

# FASE 0.3.2: Parking V2 Production Streams
const STREAM_PARKING_DODGE = 30
const STREAM_PARKING_SAVE = 40
const STREAM_PARKING_OVERSHOOT = 50
const STREAM_PARKING_STEERING = 60

# FASE 0.6.0: HIT V1 Production Streams
const STREAM_HIT_SPEED_VARIANCE = 70
const STREAM_HIT_TRAJECTORY_NOISE = 80
const STREAM_HIT_TARGET_OFFSET = 90

var _definitions: Dictionary = {}

func _init() -> void:
	# Legacy / Pilot Streams
	_register(STREAM_TRAJECTORY, "TRAJECTORY", Domain.STRUCTURAL_MAIN, "Main spatial generation", "frame", "2.0", ["PilotMechanic"])
	_register(STREAM_CONTROL, "CONTROL", Domain.STRUCTURAL_MAIN, "Logic flow generation", "frame", "2.0", ["PilotMechanic"])
	_register(STREAM_PARTICLES, "PARTICLES", Domain.PRESENTATION, "Visual particles", "frame", "2.0", ["PilotVisuals"])

	# Parking V2 Production Streams
	_register(STREAM_PARKING_DODGE, "PARKING_DODGE_OFFSET", Domain.STRUCTURAL_MAIN, "Dodge generation parameter", "0", "2.0", ["ParkingMechanic"])
	_register(STREAM_PARKING_SAVE, "PARKING_SAVE_OFFSET", Domain.STRUCTURAL_MAIN, "Save generation parameter", "0", "2.0", ["ParkingMechanic"])
	_register(STREAM_PARKING_OVERSHOOT, "PARKING_OVERSHOOT", Domain.STRUCTURAL_MAIN, "Overshoot generation parameter", "0", "2.0", ["ParkingMechanic"])
	_register(STREAM_PARKING_STEERING, "PARKING_STEERING_NOISE", Domain.STRUCTURAL_MAIN, "Steering noise (x/y)", "frame*2 / frame*2+1", "2.0", ["ParkingMechanic"])

	# HIT V1 Production Streams
	_register(
		STREAM_HIT_SPEED_VARIANCE, 
		"HIT_SPEED_VARIANCE", 
		Domain.STRUCTURAL_MAIN, 
		"Per-attempt speed variance", 
		"0", 
		"2.0", 
		["HitMechanic"]
	)
	_register(
		STREAM_HIT_TRAJECTORY_NOISE, 
		"HIT_TRAJECTORY_NOISE", 
		Domain.STRUCTURAL_MAIN, 
		"Per-frame vertical trajectory noise", 
		"frame", 
		"2.0", 
		["HitMechanic"]
	)
	_register(
		STREAM_HIT_TARGET_OFFSET, 
		"HIT_TARGET_OFFSET", 
		Domain.STRUCTURAL_MAIN, 
		"Per-attempt target offset", 
		"0 / 1", 
		"2.0", 
		["HitMechanic"]
	)

func _register(id: int, name: String, domain: Domain, description: String, index_semantics: String, version_introduced: String, allowed_consumers: Array[String]) -> void:
	_definitions[id] = RNGStreamDefinition.new(id, name, domain, description, index_semantics, version_introduced, allowed_consumers)

func is_registered(stream_id: int) -> bool:
	return _definitions.has(stream_id)

func get_definition(stream_id: int) -> RNGStreamDefinition:
	return _definitions.get(stream_id, null)

func is_consumer_authorized(stream_id: int, consumer_id: String) -> bool:
	if not is_registered(stream_id):
		return false
	return _definitions[stream_id].get_allowed_consumers().has(consumer_id)