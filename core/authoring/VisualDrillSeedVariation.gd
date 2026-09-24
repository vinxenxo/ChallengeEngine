class_name VisualDrillSeedVariation
extends RefCounted

## C11-C 2.7.0 — Seeded visual-drill authoring variation.
## This stage expands a visual-drill definition deterministically from the content seed.
## It is an authoring transform: no runtime RNG stream is consumed and presentation
## does not calculate or alter mechanics after the envelope has been authored.

const VERSION: String = "2.7.0"
const MASK_31: int = 0x7fffffff

static func apply(subtype: String, seed_value: int, payload: Dictionary) -> Dictionary:
    var result := payload.duplicate(true)
    match subtype:
        "tracking":
            _apply_tracking(seed_value, result)
        "saccade":
            _apply_saccade(seed_value, result)
        _:
            pass
    return result

static func _apply_tracking(seed_value: int, payload: Dictionary) -> void:
    var trajectory_variant: Variant = payload.get("trajectory", {})
    if not trajectory_variant is Dictionary:
        return
    var trajectory: Dictionary = trajectory_variant.duplicate(true)

    var frequency_pairs: Array = [
        [1.0, 2.0],
        [1.0, 3.0],
        [2.0, 3.0],
        [2.0, 4.0],
        [3.0, 1.0],
        [3.0, 2.0],
        [3.0, 4.0],
        [4.0, 1.0],
        [4.0, 3.0]
    ]
    var frequency_pair: Array = frequency_pairs[_index(seed_value, 101, frequency_pairs.size())]

    trajectory["type"] = "lissajous"
    trajectory["profile"] = "lissajous_seeded_v1"
    trajectory["center_x"] = lerpf(254.0, 286.0, _unit(seed_value, 103))
    trajectory["center_y"] = lerpf(456.0, 504.0, _unit(seed_value, 107))
    trajectory["amplitude_x"] = lerpf(138.0, 184.0, _unit(seed_value, 109))
    trajectory["amplitude_y"] = lerpf(184.0, 248.0, _unit(seed_value, 113))
    trajectory["x_frequency"] = float(frequency_pair[0])
    trajectory["y_frequency"] = float(frequency_pair[1])
    trajectory["travel_cycles"] = lerpf(0.54, 1.12, _unit(seed_value, 127))
    trajectory["phase_x"] = lerpf(-PI, PI, _unit(seed_value, 131))
    trajectory["phase_y"] = lerpf(-PI, PI, _unit(seed_value, 137))
    trajectory["motion_speed_multiplier"] = lerpf(0.72, 1.38, _unit(seed_value, 139))
    trajectory["seed_motion_variant"] = _index(seed_value, 149, 1000000)
    trajectory["seed_authoring_version"] = VERSION

    payload["trajectory"] = trajectory
    payload["seed_motion"] = {
        "enabled": true,
        "version": VERSION,
        "seed": int(seed_value),
        "frequency_x": float(trajectory["x_frequency"]),
        "frequency_y": float(trajectory["y_frequency"]),
        "phase_x": float(trajectory["phase_x"]),
        "phase_y": float(trajectory["phase_y"]),
        "amplitude_x": float(trajectory["amplitude_x"]),
        "amplitude_y": float(trajectory["amplitude_y"]),
        "travel_cycles": float(trajectory["travel_cycles"]),
        "motion_speed_multiplier": float(trajectory["motion_speed_multiplier"])
    }


static func _apply_saccade(seed_value: int, payload: Dictionary) -> void:
    var trajectory_variant: Variant = payload.get("trajectory", {})
    if not trajectory_variant is Dictionary:
        return
    var trajectory: Dictionary = trajectory_variant.duplicate(true)

    # All variants are deliberately conservative so every adjacent relocation
    # remains inside the existing 180..300 px jump-distance contract.
    var angle_steps: Array = [
        2.09439510239, # 120°
        2.26892802759, # 130°
        2.39996322973, # golden-angle baseline
        2.53072741539  # 145°
    ]

    trajectory["type"] = "polar_golden_angle"
    trajectory["profile"] = "polar_golden_angle_seeded_v1"
    trajectory["angle_step"] = float(angle_steps[_index(seed_value, 211, angle_steps.size())])
    trajectory["angle_offset"] = lerpf(-PI, PI, _unit(seed_value, 223))
    trajectory["radius_base"] = lerpf(136.0, 144.0, _unit(seed_value, 227))
    trajectory["radius_variation"] = lerpf(14.0, 18.0, _unit(seed_value, 229))
    trajectory["seed_spatial_variant"] = _index(seed_value, 233, 1000000)
    trajectory["seed_authoring_version"] = VERSION

    payload["trajectory"] = trajectory
    payload["seed_motion"] = {
        "enabled": true,
        "family": "saccade",
        "version": VERSION,
        "seed": int(seed_value),
        "angle_step": float(trajectory["angle_step"]),
        "angle_offset": float(trajectory["angle_offset"]),
        "radius_base": float(trajectory["radius_base"]),
        "radius_variation": float(trajectory["radius_variation"])
    }

static func _unit(seed_value: int, salt: int) -> float:
    return float(_seed_mix(seed_value, salt) % 1000000) / 1000000.0

static func _index(seed_value: int, salt: int, size: int) -> int:
    return _seed_mix(seed_value, salt) % maxi(1, size)

static func _seed_mix(seed_value: int, salt: int) -> int:
    var x: int = (int(seed_value) ^ int(salt * 374761393)) & MASK_31
    x = int((x ^ (x >> 13)) * 1274126177) & MASK_31
    x = int((x ^ (x >> 16)) * 2246822519) & MASK_31
    x = int((x ^ (x >> 13)) * 3266489917) & MASK_31
    return int(x ^ (x >> 16)) & MASK_31
