extends SceneTree

# ============================================================
# C6-F0.8-B — Content Definition Determinism Test
# Validates ContentEnvelope's handling of seed and rng_version.
# ============================================================

const ContentEnvelope = preload("res://core/authoring/ContentEnvelope.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08ContentDefinitionDeterminismTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _get_valid_base_envelope() -> Dictionary:
	return {
		"schema_version": "2.0",
		"content_id": "TEST_FRACTAL_01",
		"content_version": "1.0.0",
		"kind": "visual_loop",
		"subtype": "fractal_journey",
		"engine_version": "1.0",
		"authoring_version": "1.0",
		"presentation": {"profile_id": "p1", "coordinate_space": "2d"},
		"assets": {"family_id": "f1"},
		"audio": {"profile_id": "a1", "enabled": false},
		"provenance": {"author": "system", "timestamp_ms": 1000}
	}

func _run_tests() -> void:
	# 1. Defaults: Envelopes antiguos deben adoptar "2.0" y 0
	var dict_legacy = _get_valid_base_envelope()
	var res_legacy = ContentEnvelope.create_from_dictionary(dict_legacy)
	_assert(res_legacy.success, "Fallo: Envelope legacy válido fue rechazado.")
	if res_legacy.success:
		var env = res_legacy.envelope
		_assert(env.rng_version == "2.0", "Fallo: Default rng_version incorrecto (esperado '2.0').")
		_assert(env.seed == 0, "Fallo: Default seed incorrecto (esperado 0).")

	# 2. Explícito: Envelopes nuevos con seed y rng_version deben procesarlos
	var dict_new = _get_valid_base_envelope()
	dict_new["rng_version"] = "2.0"
	dict_new["seed"] = 88889999
	var res_new = ContentEnvelope.create_from_dictionary(dict_new)
	_assert(res_new.success, "Fallo: Envelope nuevo con rng/seed válido fue rechazado.")
	if res_new.success:
		var env = res_new.envelope
		_assert(env.rng_version == "2.0", "Fallo: rng_version no se asignó correctamente.")
		_assert(env.seed == 88889999, "Fallo: seed no se asignó correctamente.")

		# 3. Serialización: to_dictionary debe conservar estos campos
		var out_dict = env.to_dictionary()
		_assert(out_dict.has("rng_version") and out_dict["rng_version"] == "2.0", "Fallo: to_dictionary omitió/alteró rng_version.")
		_assert(out_dict.has("seed") and out_dict["seed"] == 88889999, "Fallo: to_dictionary omitió/alteró seed.")

	# 4. Rechazo: rng_version incompatible (ej. "1.0")
	var dict_bad_rng = _get_valid_base_envelope()
	dict_bad_rng["rng_version"] = "1.0"
	var res_bad_rng = ContentEnvelope.create_from_dictionary(dict_bad_rng)
	_assert(not res_bad_rng.success, "Fallo: Envelope aceptó un rng_version incompatible ('1.0').")

	# 5. Rechazo: seed de tipo incorrecto (ej. string o float)
	var dict_bad_seed = _get_valid_base_envelope()
	dict_bad_seed["seed"] = "bad_seed"
	var res_bad_seed = ContentEnvelope.create_from_dictionary(dict_bad_seed)
	_assert(not res_bad_seed.success, "Fallo: Envelope aceptó un seed de tipo String.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_CONTENT_DEF_DETERMINISM_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_CONTENT_DEF_DETERMINISM_SUITE] FAIL failures=%d" % failures.size())
		quit(1)