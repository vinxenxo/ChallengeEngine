# res://tests/C6F08PeripheralScanPilotTest.gd
extends SceneTree

# ============================================================
# C6-F0.8-E1 — Peripheral Scan Pilot & Runtime Contract Test
# Validates Stream 2014 binding, determinism, and variation injection.
# ============================================================

const VisualDrillRuntime = preload("res://core/runtime/VisualDrillRuntime.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08PeripheralScanPilotTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	# 0. Auditoría de registro Stream 2014
	var registry := RNGStreamRegistry.new()
	var drill_def = registry.get_definition(registry.STREAM_VISUAL_DRILL_PERIPHERAL_SCAN)
	_assert(drill_def != null, "Stream 2014 (Peripheral Scan) debe estar registrado.")
	if drill_def != null:
		_assert(drill_def.get_allowed_consumers().has("PeripheralScanGenerator"), "Stream 2014 debe autorizar PeripheralScanGenerator.")
		var semantics = drill_def.get_index_semantics()
		_assert("pattern_variant" in semantics and "amplitude_variant" in semantics, "Stream 2014 debe declarar semánticas para pattern_variant y amplitude_variant.")

	# 1. Definición Mock para Runtime
	var definition = {
		"schema_version": "2.0",
		"content_id": "PERIPHERAL_SCAN_PILOT",
		"content_version": "1.0.0",
		"kind": "visual_drill",
		"subtype": "peripheral_scan",
		"engine_version": "1.0",
		"authoring_version": "1.0",
		"rng_version": "2.0",
		"seed": 12345,
		"presentation": {"profile_id": "social_default_v1", "coordinate_space": "2d"},
		"assets": {"family_id": "f1"},
		"audio": {"profile_id": "a1", "enabled": false},
		"provenance": {"author": "system", "timestamp_ms": 1000},
		"payload": {
			"domain": "visual_drill",
			"duration": 0.5,
			"fps": 30,
			"frame_count": 15,
			"exercise_parameters": {},
			"stimulus": {"x": 10.0, "y": 20.0, "active": true},
			"targets": [],
			"distractors": [],
			"trajectory": {},
			"task": {}
		}
	}

	var rt1 = VisualDrillRuntime.new()
	_assert(rt1.initialize(definition), "VisualDrillRuntime debe inicializarse correctamente para peripheral_scan.")
	
	var frame1 = rt1.next_frame()
	_assert(not frame1.is_empty(), "Runtime debe entregar frames válidos.")
	
	var payload1 = frame1.get("payload", {})
	_assert(payload1.has("parameters"), "Payload debe contener los parámetros generados por variación.")
	if payload1.has("parameters"):
		_assert(payload1["parameters"].has("pattern_variant"), "Debe incluir pattern_variant del Stream 2014.")
		_assert(payload1["parameters"].has("amplitude_variant"), "Debe incluir amplitude_variant del Stream 2014.")

	# 2. Prueba de Determinismo (Misma seed -> Misma salida exacta)
	var rt2 = VisualDrillRuntime.new()
	_assert(rt2.initialize(definition), "Runtime 2 debe inicializarse.")
	var frame2 = rt2.next_frame()
	
	_assert(str(frame1) == str(frame2), "Determinismo Estricto: Mismas semillas deben producir idénticos frames de drill.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_PERIPHERAL_SCAN_PILOT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_PERIPHERAL_SCAN_PILOT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)