class_name KeyMechanic
extends ChallengeMechanic

const DETERMINISTIC_LCG = preload("res://core/deterministic/DeterministicLCG.gd")

var target_position: Vector2 = Vector2(540.0, 960.0)
var target_rotation: float = 0.0
var base_speed: float = 8.0
var base_rot_speed: float = 0.05
var tolerance_rotation_deg: float = 4.5
var _rng_index: int = 0

func setup(config: Dictionary) -> void:
	var diff: Dictionary = config.get("difficulty", {})
	var tol: Dictionary = diff.get("tolerance", {})
	tolerance_rotation_deg = float(
		tol.get("rotation_deg", 4.5)
	)

func simulate(
	total_game_frames: int,
	local_seed: int,
	config: Dictionary
) -> SimulationResult:

	setup(config)

	var result: SimulationResult = SimulationResult.new()
	result.tolerance_threshold = deg_to_rad(
		tolerance_rotation_deg
	)

	_rng_index = 0
	var rng_version: String = str(
		config.get("generation", {}).get("rng_version", "1.0")
	)

	var pos: Vector2 = Vector2(540.0, 200.0)

	var speed_var: float
	var rot_var: float
	var rot: float

	if rng_version == "2.0":
		speed_var = DETERMINISTIC_LCG.sample_float_range(local_seed, 10, 0, 0.8, 1.2)
		rot_var = DETERMINISTIC_LCG.sample_float_range(local_seed, 10, 1, 0.7, 1.3)
		rot = DETERMINISTIC_LCG.sample_float_range(local_seed, 10, 2, -PI, PI)
	else:
		speed_var = _sample_legacy_range(local_seed, 0.8, 1.2)
		rot_var = _sample_legacy_range(local_seed, 0.7, 1.3)
		rot = _sample_legacy_range(local_seed, -PI, PI)

	var current_speed: float = base_speed * speed_var
	var current_rot_speed: float = base_rot_speed * rot_var

	for f in range(total_game_frames):
		var snapshot: FrameSnapshot = FrameSnapshot.new()

		pos.y += current_speed
		rot += current_rot_speed

		snapshot.position = pos
		snapshot.rotation = rot
		snapshot.scale = Vector2.ONE
		snapshot.opacity = 1.0

		var angular_distance: float = abs(
			angle_difference(rot, target_rotation)
		)

		var spatial_distance: float = (
			pos.distance_to(target_position)
		)

		snapshot.custom_data = {
			"success_distance": angular_distance,
			"spatial_distance": spatial_distance,
			"velocity": current_speed
		}

		result.frames.append(snapshot)

	result.metadata = {
		"seed_used": local_seed,
		"mechanic": "key",
		"rng_version": rng_version
	}

	return result


func _sample_legacy_range(seed: int, from: float, to: float) -> float:
	var value: float = DETERMINISTIC_LCG.sample_float_range(
		seed,
		0,
		_rng_index,
		from,
		to
	)
	_rng_index += 1
	return value