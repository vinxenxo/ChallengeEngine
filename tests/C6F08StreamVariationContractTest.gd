extends SceneTree

# ============================================================
# C6-F0.8 — Stream Variation Contract Audit Test
# Enforces that VisualLoopRuntime and Generators strictly adhere
# to the RNGStreamRegistry variation key/index mapping definitions.
# ============================================================

const VisualLoopRuntime = preload("res://core/runtime/VisualLoopRuntime.gd")
const VectorFieldGenerator = preload("res://core/runtime/visual/generators/VectorFieldGenerator.gd")
const ParticleFlowGenerator = preload("res://core/runtime/visual/generators/ParticleFlowGenerator.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08StreamVariationContractTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	# 0. Auditoría estricta del RNGStreamRegistry y sus semánticas declaradas
	var registry := RNGStreamRegistry.new()

	var fractal_def = registry.get_definition(registry.STREAM_VISUAL_LOOP_FRACTAL)
	var vector_def = registry.get_definition(registry.STREAM_VISUAL_LOOP_VECTOR_FIELD)
	var particle_def = registry.get_definition(registry.STREAM_VISUAL_LOOP_PARTICLE_FLOW)

	_assert(
		fractal_def != null,
		"Stream 2001 debe estar registrado."
	)

	_assert(
		vector_def != null,
		"Stream 2002 debe estar registrado."
	)

	_assert(
		particle_def != null,
		"Stream 2003 debe estar registrado."
	)

	if fractal_def != null:
		_assert(
			fractal_def.get_allowed_consumers().has("FractalGenerator"),
			"Stream 2001 debe autorizar FractalGenerator."
		)

	if vector_def != null:
		_assert(
			vector_def.get_allowed_consumers().has("VectorFieldGenerator"),
			"Stream 2002 debe autorizar VectorFieldGenerator."
		)
		_assert(
			vector_def.get_index_semantics() == "0=palette_variant, 1=turbulence_variant",
			"Stream 2002 tiene index_semantics incorrectos."
		)

	if particle_def != null:
		_assert(
			particle_def.get_allowed_consumers().has("ParticleFlowGenerator"),
			"Stream 2003 debe autorizar ParticleFlowGenerator."
		)
		_assert(
			particle_def.get_index_semantics() == "0=palette_variant, 1=emission_variant",
			"Stream 2003 tiene index_semantics incorrectos."
		)

	# 1. Auditoría de mapeo de claves en Vector Field (Stream 2002) - Evaluado en frame no cero para evitar sin(0) = 0
	var vf_gen = VectorFieldGenerator.new()
	var vf_state_a = vf_gen.generate_with_variation(15, 60, {"complexity": 2}, {"palette_variant": 0.1, "turbulence_variant": 0.9})
	var vf_state_b = vf_gen.generate_with_variation(15, 60, {"complexity": 2}, {"palette_variant": 0.1, "turbulence_variant": 0.2})
	
	_assert(vf_state_a.has("parameters"), "Vector Field state must have parameters.")
	_assert(vf_state_a["parameters"].has("turbulence"), "Vector Field parameters must include turbulence.")
	_assert(vf_state_a["parameters"]["turbulence"] != vf_state_b["parameters"]["turbulence"], "turbulence_variant must directly impact turbulence output.")

	# 2. Auditoría de mapeo de claves en Particle Flow (Stream 2003)
	var pf_gen = ParticleFlowGenerator.new()
	var pf_state_a = pf_gen.generate_with_variation(0, 60, {"complexity": 2}, {"palette_variant": 0.1, "emission_variant": 0.9})
	var pf_state_b = pf_gen.generate_with_variation(0, 60, {"complexity": 2}, {"palette_variant": 0.1, "emission_variant": 0.1})
	
	_assert(pf_state_a.has("parameters"), "Particle Flow state must have parameters.")
	_assert(pf_state_a["parameters"].has("particle_count"), "Particle Flow parameters must include particle_count.")
	_assert(pf_state_a["parameters"]["particle_count"] != pf_state_b["parameters"]["particle_count"], "emission_variant must directly impact particle_count output.")

	# 3. Auditoría del contrato de construcción en Runtime para Vector Field
	var def = {
		"schema_version": "2.0",
		"content_id": "CONTRACT_AUDIT",
		"content_version": "1.0.0",
		"kind": "visual_loop",
		"subtype": "vector_field",
		"engine_version": "1.0",
		"authoring_version": "1.0",
		"rng_version": "2.0",
		"seed": 42,
		"presentation": {"profile_id": "social_default_v1", "coordinate_space": "2d"},
		"assets": {"family_id": "f1"},
		"audio": {"profile_id": "a1", "enabled": false},
		"provenance": {"author": "system", "timestamp_ms": 1000},
		"content": {
			"domain": "visual_loop",
			"duration": 0.5,
			"fps": 30,
			"frame_count": 15,
			"visual_parameters": {
				"generator": "vector_field",
				"speed": 1.0,
				"complexity": 2,
				"layers": [{"blend_mode": "alpha"}]
			}
		}
	}
	
	var rt = VisualLoopRuntime.new()
	_assert(rt.initialize(def), "Runtime initialization for Vector Field stream mapping failed.")
	rt.next_frame()
	var render_state = rt.get_current_render_state()
	_assert(render_state != null, "Render state must not be null.")
	if render_state != null:
		_assert(render_state.layer_states[0]["generator"] == "vector_field", "Generator type must match.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_STREAM_VARIATION_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_STREAM_VARIATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)