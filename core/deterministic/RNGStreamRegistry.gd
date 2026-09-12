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

# FASE 0.8.0: CATCH V1 Production Streams
const STREAM_CATCH_TARGET_MOTION = 100
const STREAM_CATCH_PURSUER_BIAS = 110
const STREAM_CATCH_INITIAL_PHASE = 120

const STREAM_FIND_SPATIAL_PLACEMENT: int = 130
const STREAM_FIND_TOPOLOGY_GENERATION: int = 140
const STREAM_FIND_SCANNER_TRAJECTORY: int = 150
const STREAM_FIND_TARGET_DRIFT: int = 160

# ==========================================
# FASE 0.8.0: Cosmetic Visual Streams (C6-F0.8-C)
# ==========================================
const STREAM_VISUAL_LOOP_FRACTAL = 2001
const STREAM_VISUAL_LOOP_VECTOR_FIELD = 2002
const STREAM_VISUAL_LOOP_PARTICLE_FLOW = 2003
const STREAM_VISUAL_LOOP_KALEIDOSCOPE = 2004
const STREAM_VISUAL_LOOP_GEOMETRIC = 2005

const STREAM_VISUAL_DRILL_TRACKING = 2011
const STREAM_VISUAL_DRILL_PURSUIT = 2012
const STREAM_VISUAL_DRILL_SACCADE = 2013
const STREAM_VISUAL_DRILL_PERIPHERAL_SCAN = 2014

var _definitions: Dictionary = {}

func _init() -> void:
	_register(STREAM_FIND_SPATIAL_PLACEMENT, "FIND_SPATIAL_PLACEMENT", Domain.STRUCTURAL_SECONDARY, "Target base coordinates", "0=X, 1=Y", "2.0", ["FindMechanic"])
	_register(STREAM_FIND_TOPOLOGY_GENERATION, "FIND_TOPOLOGY_GENERATION", Domain.STRUCTURAL_SECONDARY, "Distractor positions", "2j=X, 2j+1=Y", "2.0", ["FindMechanic"])
	_register(STREAM_FIND_SCANNER_TRAJECTORY, "FIND_SCANNER_TRAJECTORY", Domain.STRUCTURAL_SECONDARY, "Scanner initial phases", "0=phi_x, 1=phi_y", "2.0", ["FindMechanic"])
	_register(STREAM_FIND_TARGET_DRIFT, "FIND_TARGET_DRIFT", Domain.STRUCTURAL_SECONDARY, "Target drift phase", "0=phi_drift", "2.0", ["FindMechanic"])
	
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
	_register(STREAM_HIT_SPEED_VARIANCE, "HIT_SPEED_VARIANCE", Domain.STRUCTURAL_MAIN, "Per-attempt speed variance", "0", "2.0", ["HitMechanic"])
	_register(STREAM_HIT_TRAJECTORY_NOISE, "HIT_TRAJECTORY_NOISE", Domain.STRUCTURAL_MAIN, "Per-frame vertical trajectory noise", "frame", "2.0", ["HitMechanic"])
	_register(STREAM_HIT_TARGET_OFFSET, "HIT_TARGET_OFFSET", Domain.STRUCTURAL_MAIN, "Per-attempt target offset", "0 / 1", "2.0", ["HitMechanic"])

	# CATCH V1 Production Streams
	_register(STREAM_CATCH_TARGET_MOTION, "CATCH_TARGET_MOTION", Domain.STRUCTURAL_SECONDARY, "Per-attempt target velocity variance", "0", "2.0", ["CatchMechanic"])
	_register(STREAM_CATCH_PURSUER_BIAS, "CATCH_PURSUER_BIAS", Domain.STRUCTURAL_SECONDARY, "Per-attempt pursuer velocity bias", "0", "2.0", ["CatchMechanic"])
	_register(STREAM_CATCH_INITIAL_PHASE, "CATCH_INITIAL_PHASE", Domain.STRUCTURAL_SECONDARY, "Per-attempt initial target phase offset", "0", "2.0", ["CatchMechanic"])

	# ==========================================
	# Cosmetic Streams (C6-F0.8-C)
	# Owner attribute is mapped to the 'description' parameter internally.
	# ==========================================
	_register(STREAM_VISUAL_LOOP_FRACTAL, "VISUAL_LOOP_FRACTAL", Domain.COSMETIC_CONTENT, "VisualContent", "0=palette_variant, 1=complexity_variant, 2=phase_offset, 3=rotation_offset", "2.0", ["FractalGenerator"])
	_register(STREAM_VISUAL_LOOP_VECTOR_FIELD, "VISUAL_LOOP_VECTOR_FIELD", Domain.COSMETIC_CONTENT, "VisualContent", "0=palette_variant, 1=turbulence_variant", "2.0", ["VectorFieldGenerator"])
	_register(STREAM_VISUAL_LOOP_PARTICLE_FLOW, "VISUAL_LOOP_PARTICLE_FLOW", Domain.COSMETIC_CONTENT, "VisualContent", "0=palette_variant, 1=emission_variant", "2.0", ["ParticleFlowGenerator"])
	_register(STREAM_VISUAL_LOOP_KALEIDOSCOPE, "VISUAL_LOOP_KALEIDOSCOPE", Domain.COSMETIC_CONTENT, "VisualContent", "0=palette_variant, 1=symmetry_variant", "2.0", ["KaleidoscopeGenerator"])
	_register(STREAM_VISUAL_LOOP_GEOMETRIC, "VISUAL_LOOP_GEOMETRIC", Domain.COSMETIC_CONTENT, "VisualContent", "0=palette_variant, 1=shape_variant", "2.0", ["GeometricGenerator"])

	_register(STREAM_VISUAL_DRILL_TRACKING, "VISUAL_DRILL_TRACKING", Domain.COSMETIC_CONTENT, "VisualContent", "0=tracking_variant", "2.0", ["TrackingGenerator"])
	_register(STREAM_VISUAL_DRILL_PURSUIT, "VISUAL_DRILL_PURSUIT", Domain.COSMETIC_CONTENT, "VisualContent", "0=pursuit_variant", "2.0", ["PursuitGenerator"])
	_register(STREAM_VISUAL_DRILL_SACCADE, "VISUAL_DRILL_SACCADE", Domain.COSMETIC_CONTENT, "VisualContent", "0=saccade_variant", "2.0", ["SaccadeGenerator"])
	_register(STREAM_VISUAL_DRILL_PERIPHERAL_SCAN, "VISUAL_DRILL_PERIPHERAL_SCAN", Domain.COSMETIC_CONTENT, "VisualContent", "0=pattern_variant, 1=amplitude_variant", "2.0", ["PeripheralScanGenerator"])

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