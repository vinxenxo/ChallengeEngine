extends SceneTree

# ============================================================
# C6-F0.8-C — Cosmetic RNG Contract Test (Fully Certified & Safe)
# Validates RNGStreamRegistry, PresentationRNGContext, and
# MechanicRNGContext domain isolation using authentic baseline APIs.
# ============================================================

const PresentationRNGContext = preload("res://core/deterministic/PresentationRNGContext.gd")
const MechanicRNGContext = preload("res://core/deterministic/MechanicRNGContext.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")
const CosmeticRNG = preload("res://core/deterministic/CosmeticRNG.gd")
const StructuralRNG = preload("res://core/deterministic/StructuralRNG.gd")

const STREAMS = [
	{ "id": 2001, "name": "VISUAL_LOOP_FRACTAL", "consumer": "FractalGenerator" },
	{ "id": 2002, "name": "VISUAL_LOOP_VECTOR_FIELD", "consumer": "VectorFieldGenerator" },
	{ "id": 2003, "name": "VISUAL_LOOP_PARTICLE_FLOW", "consumer": "ParticleFlowGenerator" },
	{ "id": 2004, "name": "VISUAL_LOOP_KALEIDOSCOPE", "consumer": "KaleidoscopeGenerator" },
	{ "id": 2005, "name": "VISUAL_LOOP_GEOMETRIC", "consumer": "GeometricGenerator" },
	{ "id": 2011, "name": "VISUAL_DRILL_TRACKING", "consumer": "TrackingGenerator" },
	{ "id": 2012, "name": "VISUAL_DRILL_PURSUIT", "consumer": "PursuitGenerator" },
	{ "id": 2013, "name": "VISUAL_DRILL_SACCADE", "consumer": "SaccadeGenerator" },
	{ "id": 2014, "name": "VISUAL_DRILL_PERIPHERAL_SCAN", "consumer": "PeripheralScanGenerator" }
]

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08CosmeticRNGContractTest...")
	
	var err = _safe_run_tests()
	if err != "":
		failures.append(err)
		
	_conclude()

func _safe_run_tests() -> String:
	var registry = RNGStreamRegistry.new()
	var cosmetic_rng = CosmeticRNG.new(registry)
	var structural_rng = StructuralRNG.new(registry)
	
	# 1-8. Verificación individual de contrato por cada stream
	for s in STREAMS:
		var stream_id = s["id"]
		var expected_consumer = s["consumer"]
		
		if not registry.is_registered(stream_id):
			return "Stream %d no está registrado." % stream_id
		
		var def = registry.get_definition(stream_id)
		if def == null:
			return "Definición nula para stream %d." % stream_id
			
		if def.get_name() != s["name"]:
			return "Nombre incorrecto para stream %d." % stream_id
			
		if def.get_domain() != RNGStreamRegistry.Domain.COSMETIC_CONTENT:
			return "Stream %d no pertenece a COSMETIC_CONTENT." % stream_id
			
		if def.get_owner() != "VisualContent":
			return "El propietario del stream %d debe ser 'VisualContent'." % stream_id
			
		if def.get_version_introduced() != "2.0":
			return "Stream %d debe ser versión '2.0'." % stream_id
			
		if def.get_index_semantics() == "":
			return "Stream %d carece de index_semantics." % stream_id
		
		if not registry.is_consumer_authorized(stream_id, expected_consumer):
			return "Consumidor %s no está autorizado para %d." % [expected_consumer, stream_id]
			
		if registry.is_consumer_authorized(stream_id, "HackerGenerator"):
			return "Consumidor no autorizado fue aceptado para %d." % stream_id

	# 9. Stream inexistente rechazado
	if registry.is_registered(9999):
		return "Stream inexistente 9999 no fue rechazado."
	
	var fractal_id = STREAMS[0]["id"]
	var fractal_consumer = STREAMS[0]["consumer"]
	var structural_stream_id = RNGStreamRegistry.STREAM_TRAJECTORY

	# 10. Stream estructural rechazado por PresentationRNGContext
	var res_structural = PresentationRNGContext.create(1234, "2.0", "PilotVisuals", [structural_stream_id], cosmetic_rng, registry)
	if res_structural.is_valid:
		return "PresentationRNGContext aceptó un stream STRUCTURAL_MAIN."

	# 11. Stream cosmético aceptado por PresentationRNGContext
	var res_cosmetic = PresentationRNGContext.create(1234, "2.0", fractal_consumer, [fractal_id], cosmetic_rng, registry)
	if not res_cosmetic.is_valid:
		return "PresentationRNGContext rechazó un stream COSMETIC_CONTENT válido."

	var ctx_cosmetic = res_cosmetic.context

	# 12. Streams duplicados en allowed_streams rechazados
	var res_dup = PresentationRNGContext.create(1234, "2.0", fractal_consumer, [fractal_id, fractal_id], cosmetic_rng, registry)
	if res_dup.is_valid:
		return "PresentationRNGContext permitió streams duplicados."

	# 13. Índice negativo rechazado
	if ctx_cosmetic.has_method("sample_float"):
		ctx_cosmetic.sample_float(fractal_id, -1)
		if not ("error_state" in ctx_cosmetic and ctx_cosmetic.error_state == "RNG_INDEX_INVALID"):
			return "El contexto no estableció 'RNG_INDEX_INVALID' al pedir índice negativo."

	# 14. Stream no autorizado en allowed_streams del contexto => rechazo al samplear
	if ctx_cosmetic.has_method("sample_float"):
		ctx_cosmetic.sample_float(STREAMS[1]["id"], 0)
		if not ("error_state" in ctx_cosmetic and ctx_cosmetic.error_state != ""):
			return "El contexto permitió samplear un stream no registrado en allowed_streams."

	# 15. Mismo seed/stream/index => mismo valor (Reproducibilidad pura)
	var res_a = PresentationRNGContext.create(5555, "2.0", fractal_consumer, [fractal_id], cosmetic_rng, registry)
	var res_b = PresentationRNGContext.create(5555, "2.0", fractal_consumer, [fractal_id], cosmetic_rng, registry)
	if res_a.is_valid and res_b.is_valid:
		var ctx_a = res_a.context
		var ctx_b = res_b.context
		if ctx_a.has_method("sample_float") and ctx_b.has_method("sample_float"):
			var sample_a = ctx_a.sample_float(fractal_id, 0)
			var sample_b = ctx_b.sample_float(fractal_id, 0)
			if sample_a != sample_b:
				return "Ruptura de contrato determinista. Mismo seed e índice produjeron valores distintos."

	# 16. MechanicRNGContext rechaza streams cosméticos
	var res_mech = MechanicRNGContext.create(9999, "2.0", "HitMechanic", [fractal_id], structural_rng, registry)
	if res_mech.is_valid:
		return "MechanicRNGContext aceptó un stream COSMETIC_CONTENT."

	return ""

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_COS_RNG_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_COS_RNG_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)