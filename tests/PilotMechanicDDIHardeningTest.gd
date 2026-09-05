extends SceneTree

const REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")
const STRUCTURAL = preload("res://core/deterministic/StructuralRNG.gd")
const COSMETIC = preload("res://core/deterministic/CosmeticRNG.gd")
const MECH_CTX = preload("res://core/deterministic/MechanicRNGContext.gd")
const PRES_CTX = preload("res://core/deterministic/PresentationRNGContext.gd")
const MECHANIC_REGISTRY = preload("res://core/mechanics/MechanicRegistry.gd")

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

	# Each scenario owns its own presentation RNG capability. The test must
	# not depend on GeneradorMaestro's removed legacy orchestration.	
	var registry_a = REGISTRY.new()
	var cosmetic_a = COSMETIC.new(registry_a)
	registry_a._register(1020, "CAMERA", REGISTRY.Domain.PRESENTATION, "Test", "frame", "2.0", ["Camera"])
	registry_a._register(1030, "SPRITE", REGISTRY.Domain.PRESENTATION, "Test", "entity", "2.0", ["Sprite"])

	var cam_ctx_a = PRES_CTX.create(314159, "2.0", "Camera", [1020], cosmetic_a, registry_a).context
	var spr_ctx_a = PRES_CTX.create(314159, "2.0", "Sprite", [1030], cosmetic_a, registry_a).context
	var prt_ctx_a = PRES_CTX.create(314159, "2.0", "PilotVisuals", [1010], cosmetic_a, registry_a).context

	var cam_a = PresentationHarnessComponent.new(cam_ctx_a, 1020).execute(100)
	var spr_a = PresentationHarnessComponent.new(spr_ctx_a, 1030).execute(100)
	var prt_a = PresentationHarnessComponent.new(prt_ctx_a, 1010).execute(100)
	var sim_a = _run_pilot_simulation(config)

	# Reordered presentation consumption must not affect any presentation stream.
	var registry_b = REGISTRY.new()
	var cosmetic_b = COSMETIC.new(registry_b)
	registry_b._register(1020, "CAMERA", REGISTRY.Domain.PRESENTATION, "Test", "frame", "2.0", ["Camera"])
	registry_b._register(1030, "SPRITE", REGISTRY.Domain.PRESENTATION, "Test", "entity", "2.0", ["Sprite"])

	var prt_ctx_b = PRES_CTX.create(314159, "2.0", "PilotVisuals", [1010], cosmetic_b, registry_b).context
	var cam_ctx_b = PRES_CTX.create(314159, "2.0", "Camera", [1020], cosmetic_b, registry_b).context
	var spr_ctx_b = PRES_CTX.create(314159, "2.0", "Sprite", [1030], cosmetic_b, registry_b).context

	var prt_b = PresentationHarnessComponent.new(prt_ctx_b, 1010).execute(100)
	var cam_b = PresentationHarnessComponent.new(cam_ctx_b, 1020).execute(100)
	var spr_b = PresentationHarnessComponent.new(spr_ctx_b, 1030).execute(100)
	var sim_b = _run_pilot_simulation(config)

	if sim_a == null or sim_b == null:
		failures.append("Test S Failed: Pilot simulation helper returned null.")
		return false

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

	# Baseline Pilot simulation with the certified structural RNG.
	var sim_base = _run_pilot_simulation(config)
	# Mutated Pilot simulation with an injected StructuralRNG test double.
	var mutated_registry = REGISTRY.new()
	var mutated_structural = MutatedStructuralRNG.new(mutated_registry)
	var sim_mut = _run_pilot_simulation(config, mutated_structural, mutated_registry)

	if sim_base == null or sim_mut == null:
		failures.append("Test T Failed: Pilot simulation helper returned null.")
		return false

	# Simulation truth is evaluated by the frame snapshots here.
	# winning_frame / minimum_distance / score are not computed by
	# PilotMechanic.simulate(); they are resolved later by the analysis/
	# validation layers. Therefore this DDI test must not demand a macro
	# change in those fields at this stage.

	# The structural mutation MUST produce an observable trajectory effect,
	# while CONTROL remains isolated and byte-for-byte equivalent.
	var trajectory_changed := false
	var position_changed := false
	var frames_count = sim_base.frames.size()

	if frames_count != sim_mut.frames.size():
		failures.append("Test T Failed: structural mutation changed frame cardinality.")
		t_valid = false
		return t_valid

	for i in range(frames_count):
		var snap_base = sim_base.frames[i]
		var snap_mut = sim_mut.frames[i]

		# Control offset DEBE ser idéntico.
		if snap_base.custom_data.get("control_offset", 0.0) != snap_mut.custom_data.get("control_offset", 0.0):
			failures.append("Test T Failed: control_offset mutated at frame %d when it should be isolated." % i)
			t_valid = false
			break

		# Structural TRAJECTORY stream must alter the trajectory payload.
		if snap_base.custom_data.get("trajectory_noise", 0.0) != snap_mut.custom_data.get("trajectory_noise", 0.0):
			trajectory_changed = true

		if snap_base.position != snap_mut.position:
			position_changed = true

	if not trajectory_changed:
		failures.append("Test T Failed: TRAJECTORY stream mutation produced no trajectory_noise change.")
		t_valid = false

	if not position_changed:
		failures.append("Test T Failed: structural trajectory mutation produced no position change.")
		t_valid = false

	return t_valid

# ---------------------------------------------------------
# PILOT TEST HARNESS
# ---------------------------------------------------------
func _run_pilot_simulation(config: Dictionary, structural_override = null, registry_override = null) -> SimulationResult:
	var registry = REGISTRY.new() if registry_override == null else registry_override
	var structural = STRUCTURAL.new(registry) if structural_override == null else structural_override
	var seed: int = int(config.get("generation", {}).get("seed", 314159))
	var context_result = MECH_CTX.create(
		seed,
		"2.0",
		"PilotMechanic",
		[REGISTRY.STREAM_TRAJECTORY, REGISTRY.STREAM_CONTROL],
		structural,
		registry
	)
	if not context_result.is_valid:
		return null

	var mechanic: ChallengeMechanic = MECHANIC_REGISTRY.create_mechanic("pilot")
	if mechanic == null:
		return null

	mechanic.set_rng_context(context_result.context)
	mechanic.setup(config)
	if not mechanic._is_setup or mechanic._error_state != "OK":
		return null

	var timeline := VideoTimeline.new(config.get("video", {}))
	mechanic.prepare(timeline.game_frames)
	if not mechanic._is_prepared or mechanic._error_state != "OK":
		return null

	return mechanic.simulate(timeline.game_frames, seed, config)
