# res://core/mechanics/find/FindMechanic.gd
class_name FindMechanic
extends ChallengeMechanic

var _rng_context: MechanicRNGContext = null

# Estado estructural congelado en setup()
var _p_base: Vector2 = Vector2.ZERO
var _distractors: Array[Vector2] = []
var _phi_x: float = 0.0
var _phi_y: float = 0.0
var _phi_drift: float = 0.0

func set_rng_context(ctx: MechanicRNGContext) -> void:
	_rng_context = ctx

func requires_temporal_preparation() -> bool:
	return false

func setup(config: Dictionary) -> void:
	_is_setup = false
	_is_prepared = false
	_error_state = "OK"

	# Amnesia por intento
	_p_base = Vector2.ZERO
	_distractors.clear()
	_phi_x = 0.0
	_phi_y = 0.0
	_phi_drift = 0.0

	if _rng_context == null:
		_error_state = "MISSING_RNG_CONTEXT"
		return

	var find_cfg: Dictionary = _get_find_config(config)
	
	var x_min: float = float(find_cfg.get("safe_area_x_min", 0.0))
	var x_max: float = float(find_cfg.get("safe_area_x_max", 1080.0))
	var y_min: float = float(find_cfg.get("safe_area_y_min", 0.0))
	var y_max: float = float(find_cfg.get("safe_area_y_max", 1920.0))
	
	var r_drift: float = float(find_cfg.get("target_drift_radius", 0.0))
	var bx_min: float = x_min + r_drift
	var bx_max: float = x_max - r_drift
	var by_min: float = y_min + r_drift
	var by_max: float = y_max - r_drift

	var has_static_target: bool = find_cfg.has("target_origin")
	var target_base_arr: Array = find_cfg.get("target_origin", [540.0, 960.0])
	var distractor_count: int = int(find_cfg.get("distractor_count", 0))

	if has_static_target:
		var stat_x = float(target_base_arr[0])
		var stat_y = float(target_base_arr[1])
		if stat_x < bx_min or stat_x > bx_max or stat_y < by_min or stat_y > by_max:
			_error_state = "TARGET_BOUNDS_VIOLATION"
			return
		_p_base = Vector2(stat_x, stat_y)
	else:
		var u_x: float = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_FIND_SPATIAL_PLACEMENT, 0, 0.0, 1.0)
		var u_y: float = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_FIND_SPATIAL_PLACEMENT, 1, 0.0, 1.0)
		_p_base = Vector2(lerp(bx_min, bx_max, u_x), lerp(by_min, by_max, u_y))

	for j in range(distractor_count):
		var u_dx: float = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_FIND_TOPOLOGY_GENERATION, 2*j, 0.0, 1.0)
		var u_dy: float = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_FIND_TOPOLOGY_GENERATION, 2*j + 1, 0.0, 1.0)
		_distractors.append(Vector2(lerp(x_min, x_max, u_dx), lerp(y_min, y_max, u_dy)))

	_phi_x = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_FIND_SCANNER_TRAJECTORY, 0, 0.0, 1.0) * TAU
	_phi_y = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_FIND_SCANNER_TRAJECTORY, 1, 0.0, 1.0) * TAU

	if r_drift > 0.0:
		_phi_drift = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_FIND_TARGET_DRIFT, 0, 0.0, 1.0) * TAU

	if _rng_context.error_state != "OK":
		_error_state = _rng_context.error_state
		return

	# C3-F Modelo A: Mecánicas estructurales completan el ciclo temporal en setup
	_is_setup = true
	_is_prepared = true

func _get_find_config(config: Dictionary) -> Dictionary:
	var simulation_cfg: Dictionary = config.get("simulation", {})
	if simulation_cfg is Dictionary:
		var params = simulation_cfg.get("parameters", {})
		if params is Dictionary:
			var v2_find = params.get("find", {})
			if v2_find is Dictionary and not v2_find.is_empty():
				return v2_find.duplicate(true)

	var legacy_difficulty = config.get("difficulty", {})
	if legacy_difficulty is Dictionary:
		var legacy_find = legacy_difficulty.get("find", {})
		if legacy_find is Dictionary:
			return legacy_find.duplicate(true)

	return {}
	
func calculate_frame(f: int, config: Dictionary) -> Dictionary:
	var find_cfg: Dictionary = _get_find_config(config)
	var c_x: float = float(find_cfg.get("scanner_cx", 540.0))
	var c_y: float = float(find_cfg.get("scanner_cy", 960.0))
	var a_x: float = float(find_cfg.get("scanner_ax", 400.0))
	var a_y: float = float(find_cfg.get("scanner_ay", 800.0))
	var w_x: float = float(find_cfg.get("scanner_wx", 0.01))
	var w_y: float = float(find_cfg.get("scanner_wy", 0.015))
	
	var r_drift: float = float(find_cfg.get("target_drift_radius", 0.0))
	var w_drift: float = float(find_cfg.get("target_drift_frequency", 0.0))

	var time: float = float(f)
	var p_scan: Vector2 = Vector2(
		c_x + a_x * sin(w_x * time + _phi_x),
		c_y + a_y * sin(w_y * time + _phi_y)
	)
	var p_target: Vector2 = Vector2(
		_p_base.x + r_drift * cos(w_drift * time + _phi_drift),
		_p_base.y + r_drift * sin(w_drift * time + _phi_drift)
	)
	return {
		"p_scan": p_scan,
		"p_target": p_target
	}

func simulate(total_frames: int, _initial_seed: int, config: Dictionary) -> SimulationResult:
	if not _is_setup or _error_state != "OK" or not _is_prepared:
		var err = SimulationResult.new()
		err.winning_frame = -1
		err.metadata["error"] = _error_state
		return err

	var find_cfg: Dictionary = _get_find_config(config)
	var capture_radius: float = float(find_cfg.get("capture_radius", 100.0))

	var frames: Array[FrameSnapshot] = []
	var min_dist_target: float = INF
	var winning_frame: int = -1
	
	var in_false_positive_episode: bool = false
	var close_call_episodes: int = 0

	for f in range(total_frames):
		var frame_math = calculate_frame(f, config)
		var p_scan: Vector2 = frame_math["p_scan"]
		var p_target: Vector2 = frame_math["p_target"]

		var d_t: float = p_scan.distance_to(p_target)
		
		if d_t < min_dist_target:
			min_dist_target = d_t
			winning_frame = f

		var is_in_target: bool = (d_t <= capture_radius)
		var is_in_distractor: bool = false
		
		for distractor in _distractors:
			if p_scan.distance_to(distractor) <= capture_radius:
				is_in_distractor = true
				break
				
		var current_is_false_positive: bool = is_in_distractor and not is_in_target
		
		if current_is_false_positive and not in_false_positive_episode:
			close_call_episodes += 1
			in_false_positive_episode = true
		elif not current_is_false_positive:
			in_false_positive_episode = false

		var snap: FrameSnapshot = FrameSnapshot.new()
		snap.position = p_scan
		snap.rotation = 0.0
		snap.scale = Vector2.ONE
		snap.opacity = 1.0
		snap.custom_data = {
			"target_position": p_target
		}
		frames.append(snap)

	var captured: bool = min_dist_target <= capture_radius
	var score: float = clampf(1.0 - (min_dist_target / capture_radius), 0.0, 1.0)

	var result: SimulationResult = SimulationResult.new()
	result.frames = frames
	result.is_self_scored = true
	result.winning_frame = winning_frame
	result.minimum_distance = min_dist_target
	result.score = score
	result.tolerance_threshold = capture_radius
	
	result.metadata = {
		"captured": captured,
		"close_calls": close_call_episodes,
		"distractor_topology": _distractors.duplicate(),
		"target_base_position": _p_base
	}
	return result
