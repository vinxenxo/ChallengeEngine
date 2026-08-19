extends SceneTree

const REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")
const STRUCTURAL = preload("res://core/deterministic/StructuralRNG.gd")
const COSMETIC = preload("res://core/deterministic/CosmeticRNG.gd")
const MECH_CTX = preload("res://core/deterministic/MechanicRNGContext.gd")
const PRES_CTX = preload("res://core/deterministic/PresentationRNGContext.gd")
const MAESTRO = preload("res://GeneradorMaestro.gd")

# ---------------------------------------------------------
# TEST S: Presentation Execution Harness
# Demuestra reordenación de componentes de Presentation mediante un 
# harness headless. NO demuestra todavía reordenación real del SceneTree.
# ---------------------------------------------------------
class PresentationHarnessComponent:
	var ctx: PresentationRNGContext
	var stream_id: int
	
	func _init(p_ctx: PresentationRNGContext, p_stream_id: int):
		ctx = p_ctx
		stream_id = p_stream_id
		
	func execute(count: int) -> Array[float]:
		var results: Array[float] = []
		for i in range(count):
			results.append(ctx.sample_float(stream_id, i))
		return results

# ---------------------------------------------------------
# TEST T: Direct Structural Stream Mutation Wrapper
# ---------------------------------------------------------
class MutatedStructuralRNG extends StructuralRNG:
	func sample_float(seed: int, stream_id: int, index: int) -> float:
		var base_val = super.sample_float(seed, stream_id, index)
		if stream_id == REGISTRY.STREAM_TRAJECTORY:
			# Mutación normalizada y limpia que preserva el rango [0, 1]
			return 1.0 - base_val
		return base_val

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
func _initialize() -> void:
	var failures: Array[String] = []
	
	var r_pass = _run_test_r(failures)
	if r_pass: print("[R] PASS")
	
	var s_pass = _run_test_s(failures)
	if s_pass: print("[S] PASS")
	
	var t_pass = _run_test_t(failures)
	if t_pass: print("[T] PASS")

	if failures.is_empty() and r_pass and s_pass and t_pass:
		print("[DDI_R1] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[DDI_R1] FAIL count=%d" % failures.size())
		quit(1)

# ---------------------------------------------------------
# IMPLEMENTATION: TEST R
# ---------------------------------------------------------
func _run_test_r(failures: Array[String]) -> bool:
	var registry = REGISTRY.new()
	var structural = STRUCTURAL.new(registry)
	var ctx_res = MECH_CTX.create(314159, "2.0", "PilotMechanic", [REGISTRY.STREAM_TRAJECTORY, REGISTRY.STREAM_CONTROL], structural, registry)
	
	if not ctx_res.is_valid:
		failures.append("Test R Failed: Context invalid")
		return false
		
	var ctx = ctx_res.context
	var frames = 420
	
	# Baseline (Sequential: Traj then Ctrl)
	var traj_baseline: Array[float] = []
	var ctrl_baseline: Array[float] = []
	for i in range(frames): traj_baseline.append(ctx.sample_float(REGISTRY.STREAM_TRAJECTORY, i))
	for i in range(frames): ctrl_baseline.append(ctx.sample_float(REGISTRY.STREAM_CONTROL, i))
		
	# Mut A (Sequential: Ctrl then Traj)
	var ctrl_mut_a: Array[float] = []
	var traj_mut_a: Array[float] = []
	for i in range(frames): ctrl_mut_a.append(ctx.sample_float(REGISTRY.STREAM_CONTROL, i))
	for i in range(frames): traj_mut_a.append(ctx.sample_float(REGISTRY.STREAM_TRAJECTORY, i))
		
	# Mut B (Interleaved)
	var traj_mut_b: Array[float] = []
	var ctrl_mut_b: Array[float] = []
	for i in range(frames):
		traj_mut_b.append(ctx.sample_float(REGISTRY.STREAM_TRAJECTORY, i))
		ctrl_mut_b.append(ctx.sample_float(REGISTRY.STREAM_CONTROL, i))

	# Validations
	var r_valid = true
	for i in range(frames):
		if traj_baseline[i] != traj_mut_a[i] or traj_baseline[i] != traj_mut_b[i]:
			failures.append("Test R Failed: TRAJECTORY stream independence violated at index %d" % i)
			r_valid = false
			break
		if ctrl_baseline[i] != ctrl_mut_a[i] or ctrl_baseline[i] != ctrl_mut_b[i]:
			failures.append("Test R Failed: CONTROL stream independence violated at index %d" % i)
			r_valid = false
			break

	return r_valid

# ---------------------------------------------------------
# IMPLEMENTATION: TEST S
# ---------------------------------------------------------
func _run_test_s(failures: Array[String]) -> bool:
	var config_text = FileAccess.get_file_as_string("res://challenges/CHALLENGE_003.json")
	if config_text.is_empty():
		failures.append("Test S Failed: Could not load CHALLENGE_003.json")
		return false
	
	var config = JSON.parse_string(config_text)
	var s_valid = true
	
	# Arrays estrictamente tipados para evitar el SCRIPT ERROR de Godot 4.7
	var cam_consumers: Array[String] = ["Camera"]
	var spr_consumers: Array[String] = ["Sprite"]

	# Escenario A (Pilot -> Cam -> Sprite -> Particles)
	var maestro_a = MAESTRO.new()
	maestro_a.config_cache = config
	maestro_a.timeline = VideoTimeline.new(config.get("video", {}))
	maestro_a.initialize_rng_infrastructure()
	
	# Register conceptual presentation streams
	maestro_a.rng_registry._register(1020, "CAMERA", REGISTRY.Domain.PRESENTATION, "Test", "frame", "2.0", cam_consumers)
	maestro_a.rng_registry._register(1030, "SPRITE", REGISTRY.Domain.PRESENTATION, "Test", "entity", "2.0", spr_consumers)
	
	var sim_a = maestro_a.run_validation_pipeline()["result"]
	
	var cam_ctx_a = PRES_CTX.create(314159, "2.0", "Camera", [1020], maestro_a.cosmetic_rng, maestro_a.rng_registry).context
	var spr_ctx_a = PRES_CTX.create(314159, "2.0", "Sprite", [1030], maestro_a.cosmetic_rng, maestro_a.rng_registry).context
	var prt_ctx_a = PRES_CTX.create(314159, "2.0", "PilotVisuals", [1010], maestro_a.cosmetic_rng, maestro_a.rng_registry).context
	
	var cam_a = PresentationHarnessComponent.new(cam_ctx_a, 1020).execute(100)
	var spr_a = PresentationHarnessComponent.new(spr_ctx_a, 1030).execute(100)
	var prt_a = PresentationHarnessComponent.new(prt_ctx_a, 1010).execute(100)

	# Escenario B (Particles -> Cam -> Sprite -> Pilot)
	var maestro_b = MAESTRO.new()
	maestro_b.config_cache = config
	maestro_b.timeline = VideoTimeline.new(config.get("video", {}))
	maestro_b.initialize_rng_infrastructure()
	
	maestro_b.rng_registry._register(1020, "CAMERA", REGISTRY.Domain.PRESENTATION, "Test", "frame", "2.0", cam_consumers)
	maestro_b.rng_registry._register(1030, "SPRITE", REGISTRY.Domain.PRESENTATION, "Test", "entity", "2.0", spr_consumers)

	var prt_ctx_b = PRES_CTX.create(314159, "2.0", "PilotVisuals", [1010], maestro_b.cosmetic_rng, maestro_b.rng_registry).context
	var cam_ctx_b = PRES_CTX.create(314159, "2.0", "Camera", [1020], maestro_b.cosmetic_rng, maestro_b.rng_registry).context
	var spr_ctx_b = PRES_CTX.create(314159, "2.0", "Sprite", [1030], maestro_b.cosmetic_rng, maestro_b.rng_registry).context

	var prt_b = PresentationHarnessComponent.new(prt_ctx_b, 1010).execute(100)
	var cam_b = PresentationHarnessComponent.new(cam_ctx_b, 1020).execute(100)
	var spr_b = PresentationHarnessComponent.new(spr_ctx_b, 1030).execute(100)
	
	var sim_b = maestro_b.run_validation_pipeline()["result"]

	# Asserts
	if sim_a.winning_frame != sim_b.winning_frame:
		failures.append("Test S Failed: SimulationResult winning_frame differs upon reordering.")
		s_valid = false
		
	for i in range(100):
		if cam_a[i] != cam_b[i]:
			failures.append("Test S Failed: Camera component index %d altered by execution order." % i)
			s_valid = false
			break
		if spr_a[i] != spr_b[i]:
			failures.append("Test S Failed: Sprite component index %d altered by execution order." % i)
			s_valid = false
			break
		if prt_a[i] != prt_b[i]:
			failures.append("Test S Failed: Particle component index %d altered by execution order." % i)
			s_valid = false
			break
	
	# Clean up Node2D leaks
	maestro_a.free()
	maestro_b.free()
	
	return s_valid

# ---------------------------------------------------------
# IMPLEMENTATION: TEST T
# ---------------------------------------------------------
func _run_test_t(failures: Array[String]) -> bool:
	var config_text = FileAccess.get_file_as_string("res://challenges/CHALLENGE_003.json")
	if config_text.is_empty():
		failures.append("Test T Failed: Could not load CHALLENGE_003.json")
		return false
		
	var config = JSON.parse_string(config_text)
	var t_valid = true

	# Baseline Execution
	var maestro_base = MAESTRO.new()
	maestro_base.config_cache = config
	maestro_base.timeline = VideoTimeline.new(config.get("video", {}))
	maestro_base.initialize_rng_infrastructure()
	
	var val_base = maestro_base.run_validation_pipeline()
	var sim_base = val_base["result"]
	var result_base = val_base["validation"]

	# Mutated Execution
	var maestro_mut = MAESTRO.new()
	maestro_mut.config_cache = config
	maestro_mut.timeline = VideoTimeline.new(config.get("video", {}))
	maestro_mut.initialize_rng_infrastructure()
	
	# Inyectamos el StructuralRNG modificado
	maestro_mut.structural_rng = MutatedStructuralRNG.new(maestro_mut.rng_registry)
	
	var val_mut = maestro_mut.run_validation_pipeline()
	var sim_mut = val_mut["result"]
	var result_mut = val_mut["validation"]

	# Asserts Macro
	var macro_changed = (result_base.absolute_winning_frame != result_mut.absolute_winning_frame) or \
						(result_base.minimum_distance != result_mut.minimum_distance) or \
						(result_base.score != result_mut.score)
						
	if not macro_changed:
		failures.append("Test T Failed: Structural stream mutation did not alter winning_frame, min_dist, or score.")
		t_valid = false

	# Asserts Internos por Frame
	var frames_count = sim_base.frames.size()
	for i in range(frames_count):
		var snap_base = sim_base.frames[i]
		var snap_mut = sim_mut.frames[i]
		
		# Control offset DEBE ser idéntico
		if snap_base.custom_data.get("control_offset", 0.0) != snap_mut.custom_data.get("control_offset", 0.0):
			failures.append("Test T Failed: control_offset mutated at frame %d when it should be isolated." % i)
			t_valid = false
			break
			
		# Trajectory noise DEBE ser diferente (asumiendo que 1.0 - x no es igual a x en la mayoría de valores no-0.5)
		if snap_base.custom_data.get("trajectory_noise", 0.0) == snap_mut.custom_data.get("trajectory_noise", 0.0):
			# Salvedad matemática: si el sample fue exactamente 0.5, 1.0 - 0.5 = 0.5, por lo que no cambiará.
			if abs(snap_base.custom_data.get("trajectory_noise", 0.0)) > 0.0001: 
				failures.append("Test T Failed: trajectory_noise did not react to stream mutation at frame %d." % i)
				t_valid = false
				break
				
	# Clean up Node2D leaks
	maestro_base.free()
	maestro_mut.free()

	return t_valid