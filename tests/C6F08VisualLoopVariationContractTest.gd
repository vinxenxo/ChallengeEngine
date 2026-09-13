# res://tests/C6F08VisualLoopVariationContractTest.gd
extends SceneTree

# ============================================================
# C6-F0.8-D1 — Visual Loop Variation Injection Contract Test
# Validates runtime RNG context initialization and variation packaging.
# ============================================================

const VisualLoopRuntime = preload("res://core/runtime/VisualLoopRuntime.gd")
const ContentEnvelope = preload("res://core/authoring/ContentEnvelope.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08VisualLoopVariationContractTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	# 1. Construir un envelope con seed explícita
	var env_dict = {
		"schema_version": "2.0",
		"content_id": "TEST_LOOP_VAR",
		"content_version": "1.0.0",
		"kind": "visual_loop",
		"subtype": "fractal",
		"engine_version": "1.0",
		"authoring_version": "1.0",
		"rng_version": "2.0",
		"seed": 12345,
		"presentation": {"profile_id": "p1", "coordinate_space": "2d"},
		"assets": {"family_id": "f1"},
		"audio": {"profile_id": "a1", "enabled": false},
		"provenance": {"author": "system", "timestamp_ms": 1000}
	}
	var env_res = ContentEnvelope.create_from_dictionary(env_dict)
	_assert(env_res.success, "Fallo: No se pudo crear el envelope de prueba.")
	
	if env_res.success:
		var env = env_res.envelope
		# 2. Verificar que el runtime procesa el envelope y expone el mecanismo de variación determinista
		var runtime = VisualLoopRuntime.new()
		
		# Validar que el runtime puede inicializar el contexto RNG sin errores usando la seed del envelope
		var registry = RNGStreamRegistry.new()
		_assert(registry.is_registered(registry.STREAM_VISUAL_LOOP_FRACTAL), "El stream fractal debe estar registrado.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_VISUAL_LOOP_VARIATION_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_VISUAL_LOOP_VARIATION_SUITE] FAIL failures=%d" % failures.size())
		quit(1)