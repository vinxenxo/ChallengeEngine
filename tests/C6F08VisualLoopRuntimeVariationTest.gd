# res://tests/C6F08VisualLoopRuntimeVariationTest.gd
extends SceneTree

# ============================================================
# C6-F0.8-D2-B — VisualLoopRuntime Variation Injection E2E Test
# Validates strict integration of PresentationRNGContext into Runtime.
# ============================================================

const ContentEnvelope = preload("res://core/authoring/ContentEnvelope.gd")
const VisualLoopRuntime = preload("res://core/runtime/VisualLoopRuntime.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08VisualLoopRuntimeVariationTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	var env_dict_a = {
		"schema_version": "2.0",
		"content_id": "TEST_LOOP_RUNTIME_A",
		"content_version": "1.0.0",
		"kind": "visual_loop",
		"subtype": "fractal",
		"engine_version": "1.0",
		"authoring_version": "1.0",
		"rng_version": "2.0",
		"seed": 12345,
		"presentation": {"profile_id": "social_default_v1", "coordinate_space": "2d"},
		"assets": {"family_id": "f1"},
		"audio": {"profile_id": "a1", "enabled": false},
		"provenance": {"author": "system", "timestamp_ms": 1000}
	}

	var env_dict_b = env_dict_a.duplicate(true)
	env_dict_b["seed"] = 99999
	env_dict_b["content_id"] = "TEST_LOOP_RUNTIME_B"

	var env_dict_a2 = env_dict_a.duplicate(true)
	env_dict_a2["content_id"] = "TEST_LOOP_RUNTIME_A2"

	var env_res_a = ContentEnvelope.create_from_dictionary(env_dict_a)
	var env_res_b = ContentEnvelope.create_from_dictionary(env_dict_b)
	var env_res_a2 = ContentEnvelope.create_from_dictionary(env_dict_a2)

	if not env_res_a.success:
		print("Envelope A errors: ", env_res_a.errors)
		_assert(false, "Fallo: Creación Envelope A.")

	if not env_res_b.success:
		print("Envelope B errors: ", env_res_b.errors)
		_assert(false, "Fallo: Creación Envelope B.")

	if not env_res_a2.success:
		print("Envelope A2 errors: ", env_res_a2.errors)
		_assert(false, "Fallo: Creación Envelope A2.")

	if not failures.is_empty():
		return

	var runtime_definition_a: Dictionary = env_res_a.envelope.to_dictionary()
	runtime_definition_a["payload"] = {
		"duration": 1.0,
		"fps": 60,
		"frame_count": 60,
		"visual_parameters": {
			"generator": "fractal",
			"speed": 1.0,
			"complexity": 3,
			"layers": [{"blend_mode": "alpha"}]
		}
	}

	var runtime_definition_b: Dictionary = env_res_b.envelope.to_dictionary()
	runtime_definition_b["payload"] = {
		"duration": 1.0,
		"fps": 60,
		"frame_count": 60,
		"visual_parameters": {
			"generator": "fractal",
			"speed": 1.0,
			"complexity": 3,
			"layers": [{"blend_mode": "alpha"}]
		}
	}

	var runtime_definition_a2: Dictionary = env_res_a2.envelope.to_dictionary()
	runtime_definition_a2["payload"] = {
		"duration": 1.0,
		"fps": 60,
		"frame_count": 60,
		"visual_parameters": {
			"generator": "fractal",
			"speed": 1.0,
			"complexity": 3,
			"layers": [{"blend_mode": "alpha"}]
		}
	}

	var rt_a = VisualLoopRuntime.new()
	var rt_b = VisualLoopRuntime.new()
	var rt_a2 = VisualLoopRuntime.new()

	_assert(
		rt_a.initialize(runtime_definition_a),
		"Runtime A initialization failed."
	)

	_assert(
		rt_b.initialize(runtime_definition_b),
		"Runtime B initialization failed."
	)

	_assert(
		rt_a2.initialize(runtime_definition_a2),
		"Runtime A2 initialization failed."
	)

	if not failures.is_empty():
		return

	rt_a.next_frame()
	rt_a2.next_frame()
	rt_b.next_frame()

	var f_state_a_next = rt_a.get_current_render_state()
	var f_state_a2_next = rt_a2.get_current_render_state()
	var f_state_b_next = rt_b.get_current_render_state()

	_assert(f_state_a_next != null and f_state_a2_next != null and f_state_b_next != null, "Render states must not be null.")

	if f_state_a_next != null and f_state_a2_next != null and f_state_b_next != null:
		var layer_a = f_state_a_next.layer_states[0]
		var layer_a2 = f_state_a2_next.layer_states[0]
		var layer_b = f_state_b_next.layer_states[0]
		
		_assert(layer_a.has("generator"), "Fallo Baseline: Logical Layer State carece de 'generator'.")
		_assert(layer_a.has("parameters"), "Fallo Baseline: Logical Layer State carece de 'parameters'.")
		_assert(layer_a["generator"] == "fractal", "Fallo Baseline: El generator debe seguir siendo fractal.")

		var rot_a = layer_a["parameters"]["rotation"]
		var rot_a2 = layer_a2["parameters"]["rotation"]
		_assert(rot_a == rot_a2, "Misma seed debe producir idéntica rotación.")

		var rot_b = layer_b["parameters"]["rotation"]
		_assert(rot_a != rot_b, "Seeds diferentes deben producir diferente variación.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_VISUAL_LOOP_RUNTIME_VARIATION_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_VISUAL_LOOP_RUNTIME_VARIATION_SUITE] FAIL failures=%d" % failures.size())
		quit(1)