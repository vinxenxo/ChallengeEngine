extends SceneTree

# ============================================================
# C6-F0.8-D2-A — Fractal Pilot Vertical Slice Test (Generator + Variation)
# Validates invariants: Purity, Variation, Seed Determinism, Loop Closure.
# ============================================================

const ContentEnvelope = preload("res://core/authoring/ContentEnvelope.gd")
const CosmeticRNG = preload("res://core/deterministic/CosmeticRNG.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")
const PresentationRNGContext = preload("res://core/deterministic/PresentationRNGContext.gd")
const FractalGenerator = preload("res://core/runtime/visual/generators/FractalGenerator.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08FractalPilotTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _create_variation_from_seed(seed_val: int) -> Dictionary:
	var registry := RNGStreamRegistry.new()
	var cosmetic_rng := CosmeticRNG.new(registry)

	var stream_id := registry.STREAM_VISUAL_LOOP_FRACTAL
	var streams: Array[int] = [stream_id]

	var consumer_id := "FractalGenerator"

	_assert(
		registry.is_consumer_authorized(stream_id, consumer_id),
		"Fallo Registry: stream 2001 debe autorizar a FractalGenerator."
	)

	var creation := PresentationRNGContext.create(
		seed_val,
		"2.0",
		consumer_id,
		streams,
		cosmetic_rng,
		registry
	)

	_assert(
		creation.is_valid,
		"Fallo RNG Context: no se pudo crear PresentationRNGContext. error=%s"
		% creation.error_code
	)

	if not creation.is_valid:
		return {
			"palette_variant": 0.0,
			"complexity_variant": 0.5,
			"phase_offset": 0.0,
			"rotation_offset": 0.0
		}

	var ctx: PresentationRNGContext = creation.context

	return {
		"palette_variant": ctx.sample_float(stream_id, 0),
		"complexity_variant": ctx.sample_float(stream_id, 1),
		"phase_offset": ctx.sample_float(stream_id, 2),
		"rotation_offset": ctx.sample_float(stream_id, 3)
	}

func _run_tests() -> void:
	var generator = FractalGenerator.new()
	var layer_params = {"blend_mode": "add", "speed": 1.0, "complexity": 3, "color_palette": "neon"}
	
	# --- Invariante 1: PUREZA ---
	var var_a = {"palette_variant": 0.5, "complexity_variant": 0.5, "phase_offset": 0.0, "rotation_offset": 0.0}
	var state_pure_1 = generator.generate_with_variation(10, 60, layer_params, var_a)
	var state_pure_2 = generator.generate_with_variation(10, 60, layer_params, var_a)
	_assert(state_pure_1["parameters"]["rotation"] == state_pure_2["parameters"]["rotation"], "Fallo Pureza: Mismos inputs produjeron distintos outputs.")

	# --- Invariante 2: VARIACIÓN ---
	var var_b = {"palette_variant": 0.5, "complexity_variant": 0.5, "phase_offset": 0.0, "rotation_offset": 0.8}
	var state_var = generator.generate_with_variation(10, 60, layer_params, var_b)
	_assert(state_pure_1["parameters"]["rotation"] != state_var["parameters"]["rotation"], "Fallo Variación: Distinta variation dict no alteró el estado lógico.")

	# --- Invariante 3: SEED DETERMINISM ---
	var var_seed_1a = _create_variation_from_seed(4040)
	var var_seed_1b = _create_variation_from_seed(4040)
	var var_seed_2 = _create_variation_from_seed(9090)
	
	var state_seed_1a = generator.generate_with_variation(30, 60, layer_params, var_seed_1a)
	var state_seed_1b = generator.generate_with_variation(30, 60, layer_params, var_seed_1b)
	var state_seed_2 = generator.generate_with_variation(30, 60, layer_params, var_seed_2)
	
	_assert(state_seed_1a["parameters"]["rotation"] == state_seed_1b["parameters"]["rotation"], "Fallo Seed Determinism: Misma semilla produjo diferentes resultados.")
	_assert(state_seed_1a["parameters"]["rotation"] != state_seed_2["parameters"]["rotation"], "Fallo Seed Determinism: Diferentes semillas produjeron mismo resultado.")

	# --- Invariante 4: LOOP CLOSURE ---
	var state_start = generator.generate_with_variation(0, 60, layer_params, var_seed_1a)
	var state_end = generator.generate_with_variation(60, 60, layer_params, var_seed_1a)
	
	var rot_diff = abs(state_start["parameters"]["rotation"] - state_end["parameters"]["rotation"])
	_assert(rot_diff < 0.0001, "Fallo Loop Closure: El frame 0 no coincide geométricamente con el frame 60 (rot_diff=%f)." % rot_diff)

	_assert(state_start.has("generator") and state_start["generator"] == "fractal", "Fallo Baseline: Falta key 'generator'.")
	_assert(state_start.has("parameters"), "Fallo Baseline: Falta bloque 'parameters'.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_FRACTAL_PILOT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_FRACTAL_PILOT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)