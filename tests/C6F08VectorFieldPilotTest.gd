extends SceneTree

# ============================================================
# C6-F0.8-D4 — Vector Field Pilot Determinism Test
# Validates determinism, variation injection, and loop closure.
# ============================================================

const VectorFieldGenerator = preload("res://core/runtime/visual/generators/VectorFieldGenerator.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08VectorFieldPilotTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	var gen := VectorFieldGenerator.new()
	var layer_params := {"speed": 1.0, "complexity": 3}
	
	# Variación 1
	var var_a := {
		"palette_variant": 0.2,
		"complexity_variant": 0.8,
		"phase_offset": 0.25,
		"rotation_offset": 0.1
	}
	
	# Variación 2 (diferente offset)
	var var_b := var_a.duplicate(true)
	var_b["rotation_offset"] = 0.5
	
	# 1. Determinismo Estricto
	var s_a1 = gen.generate_with_variation(0, 60, layer_params, var_a)
	var s_a2 = gen.generate_with_variation(0, 60, layer_params, var_a)
	_assert(str(s_a1) == str(s_a2), "Fallo Determinismo: Mismos parámetros deben dar misma salida exacta.")
	
	# 2. Diferenciación Cosmética
	var s_b = gen.generate_with_variation(0, 60, layer_params, var_b)
	_assert(str(s_a1) != str(s_b), "Fallo Variación: Diferente variación debe producir distinto estado.")
	_assert(s_a1["parameters"]["global_rotation"] != s_b["parameters"]["global_rotation"], "Rotación global debe divergir.")
	
	# 3. Loop Closure Absoluto (Frame 0 == Frame 60)
	# Vector field math uses fposmod on flow_angle.
	var frame_0 = gen.generate_with_variation(0, 60, layer_params, var_a)
	var frame_60 = gen.generate_with_variation(60, 60, layer_params, var_a)
	
	var ang_0: float = frame_0["parameters"]["flow_angle"]
	var ang_60: float = frame_60["parameters"]["flow_angle"]
	
	# El ángulo usa fposmod(1.0, 1.0) que envuelve a 0.0. Evaluamos usando tolerancias.
	var diff = abs(sin(ang_0) - sin(ang_60))
	_assert(diff < 0.0001, "Fallo Cierre Loop: Frame 0 y Total Frames deben generar matemática visual equivalente.")
	
	# 4. Compatibilidad Legacy (Vacío)
	var s_legacy = gen.generate(0, 60, layer_params)
	_assert(s_legacy["parameters"].has("flow_angle"), "Fallback legacy debe seguir generando flow_angle.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_VECTOR_FIELD_PILOT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_VECTOR_FIELD_PILOT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)