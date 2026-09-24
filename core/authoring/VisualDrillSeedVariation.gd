class_name VisualDrillSeedVariation
extends RefCounted

## C11-C 2.7.0 — Seeded visual-drill authoring variation.
## This stage expands a visual-drill definition deterministically from the content seed.
## It is an authoring transform: no runtime RNG stream is consumed and presentation
## does not calculate or alter mechanics after the envelope has been authored.

const VERSION: String = "2.8.0"
const MASK_31: int = 0x7fffffff

static func apply(subtype: String, seed_value: int, payload: Dictionary) -> Dictionary:
    var result := payload.duplicate(true)
    match subtype:
        "tracking":
            _apply_tracking(seed_value, result)
        "saccade":
            _apply_saccade(seed_value, result)
        "pursuit":
            _apply_pursuit(seed_value, result)
        "peripheral_scan":
            _apply_peripheral_scan(seed_value, result)
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



static func _apply_pursuit(seed_value: int, payload: Dictionary) -> void:
    var trajectory_variant: Variant = payload.get("trajectory", {})
    if not trajectory_variant is Dictionary:
        return
    var trajectory: Dictionary = trajectory_variant.duplicate(true)
    var task_variant: Variant = payload.get("task", {})
    var task: Dictionary = task_variant.duplicate(true) if task_variant is Dictionary else {}
    var exercise_variant: Variant = payload.get("exercise_parameters", {})
    var exercise: Dictionary = exercise_variant.duplicate(true) if exercise_variant is Dictionary else {}

    var point_count := 6
    var control_points: Array = []
    var orbit_phase := lerpf(-0.35, 0.35, _unit(seed_value, 503))
    var base_rx := lerpf(0.235, 0.295, _unit(seed_value, 509))
    var base_ry := lerpf(0.250, 0.315, _unit(seed_value, 521))
    for i in range(point_count):
        var angle := TAU * float(i) / float(point_count) + orbit_phase
        var radial_x := lerpf(0.88, 1.10, _unit(seed_value, 530 + i))
        var radial_y := lerpf(0.88, 1.10, _unit(seed_value, 540 + i))
        var x := 0.5 + cos(angle) * base_rx * radial_x + sin(angle * 2.0 + orbit_phase) * 0.028
        var y := 0.5 + sin(angle) * base_ry * radial_y + cos(angle * 3.0 - orbit_phase) * 0.022
        control_points.append([clampf(x, 0.16, 0.84), clampf(y, 0.14, 0.86)])

    var lut: Array = []
    var samples_per_segment := 48
    var previous := _bspline_point(control_points, 0, 0.0)
    var cumulative := 0.0
    lut.append({"distance": 0.0, "x": previous.x, "y": previous.y})
    for segment in range(point_count):
        for j in range(1, samples_per_segment + 1):
            var u := float(j) / float(samples_per_segment)
            var current := _bspline_point(control_points, segment, u)
            cumulative += previous.distance_to(current)
            lut.append({"distance": cumulative, "x": current.x, "y": current.y})
            previous = current

    if cumulative <= 0.000001:
        return
    for sample in lut:
        sample["distance"] = float(sample["distance"]) / cumulative

    var frame_count := int(payload.get("frame_count", 510))
    var position_samples: Array = []
    var speed_samples: Array = []
    var raw_distances: Array = []
    var speed_amplitude := lerpf(0.028, 0.065, _unit(seed_value, 601))
    var speed_frequency := 1 + _index(seed_value, 607, 2)
    var speed_phase := lerpf(-PI, PI, _unit(seed_value, 613))
    var difficulty_speed := clampf(float(exercise.get("speed_multiplier", 1.0)), 0.75, 1.5)
    var cumulative_distance := 0.0
    for frame in range(maxi(1, frame_count)):
        var progress := 0.0 if frame_count <= 1 else float(frame) / float(frame_count - 1)
        var speed_factor := difficulty_speed * (1.0 + speed_amplitude * sin(TAU * float(speed_frequency) * progress + speed_phase))
        speed_samples.append(speed_factor)
        raw_distances.append(cumulative_distance)
        cumulative_distance += speed_factor / float(maxi(1, frame_count - 1))

    for frame in range(maxi(1, frame_count)):
        var distance_fraction := fposmod(float(raw_distances[frame]), 1.0)
        var point := _sample_lut(lut, distance_fraction)
        position_samples.append([point.x, point.y])

    var difficulty_tier := int(exercise.get("difficulty_tier", 2))
    var sizygia_min := 2
    var sizygia_max := 3
    match difficulty_tier:
        1:
            sizygia_min = 2; sizygia_max = 3
        2:
            sizygia_min = 3; sizygia_max = 5
        3:
            sizygia_min = 4; sizygia_max = 5
        4:
            sizygia_min = 5; sizygia_max = 7
        _:
            sizygia_min = 6; sizygia_max = 8
    var sizygia_count := sizygia_min + _index(seed_value, 409, sizygia_max - sizygia_min + 1)
    var sizygia_events: Array = []
    var previous_start := -1000
    var span_start := int(round(float(frame_count) * 0.14))
    var span_end := int(round(float(frame_count) * 0.86))
    for i in range(sizygia_count):
        var base_fraction := 0.0 if sizygia_count <= 1 else float(i) / float(sizygia_count - 1)
        var jitter := lerpf(-0.035, 0.035, _unit(seed_value, 420 + i))
        var event_fraction := clampf(0.14 + base_fraction * 0.72 + jitter, 0.10, 0.90)
        var start_frame := int(round(lerpf(float(span_start), float(span_end), event_fraction)))
        if start_frame - previous_start < 30:
            start_frame = previous_start + 30
        start_frame = mini(frame_count - 6, start_frame)
        previous_start = start_frame
        var duration_frames := 5 + _index(seed_value, 470 + i, 2)
        sizygia_events.append({
            "index": i + 1,
            "frame_start": start_frame,
            "duration_frames": duration_frames,
            "duration_ms": duration_frames * 1000.0 / 30.0
        })

    var camouflage_zones: Array = []
    var zone_count := 1 + _index(seed_value, 661, 2)
    for i in range(zone_count):
        var start := 0.28 + float(i) * 0.28 + lerpf(-0.025, 0.025, _unit(seed_value, 670 + i))
        camouflage_zones.append({
            "start_progress": clampf(start, 0.08, 0.82),
            "end_progress": clampf(start + lerpf(0.055, 0.09, _unit(seed_value, 680 + i)), 0.12, 0.94),
            "minimum_contrast": lerpf(0.05, 0.16, _unit(seed_value, 690 + i))
        })

    trajectory["type"] = "uniform_cubic_bspline"
    trajectory["profile"] = "uniform_cubic_bspline_arc_length_v1"
    trajectory["coordinate_space"] = "normalized_body_0_1"
    trajectory["control_points_normalized"] = control_points
    trajectory["arc_length_lut"] = lut
    trajectory["arc_length_parameterized"] = true
    trajectory["closed_path"] = true
    trajectory["position_samples_normalized"] = position_samples
    trajectory["speed_factor_samples"] = speed_samples
    trajectory["speed_modulation_amplitude"] = speed_amplitude
    trajectory["speed_modulation_frequency"] = speed_frequency
    trajectory["speed_modulation_phase"] = speed_phase
    trajectory["camouflage_zones"] = camouflage_zones
    trajectory["target_radius"] = lerpf(18.0, 23.0, _unit(seed_value, 703))
    trajectory["seed_motion_variant"] = _index(seed_value, 709, 1000000)
    trajectory["seed_authoring_version"] = VERSION

    task["type"] = "pursuit"
    task["target_id"] = "t1"
    task["sizygia_count"] = sizygia_count
    task["sizygia_duration_frames_min"] = 5
    task["sizygia_duration_frames_max"] = 6
    task["sizygia_events"] = sizygia_events
    task["camouflage_zones"] = camouflage_zones
    var sizygia_frame_starts: Array = []
    for event in sizygia_events:
        if event is Dictionary:
            sizygia_frame_starts.append(int(event.get("frame_start", -1)))
    task["answer_sheet"] = {"sizygia_count": sizygia_count, "event_frame_starts": sizygia_frame_starts}

    exercise["generator"] = "pursuit"
    exercise["pacing_mode"] = "authored_arc_length"
    payload["exercise_parameters"] = exercise
    payload["trajectory"] = trajectory
    payload["task"] = task
    payload["seed_motion"] = {
        "enabled": true,
        "family": "pursuit",
        "version": VERSION,
        "seed": int(seed_value),
        "control_points_count": point_count,
        "sizygia_count": sizygia_count,
        "speed_modulation_amplitude": speed_amplitude,
        "speed_modulation_frequency": speed_frequency,
        "difficulty_speed_multiplier": difficulty_speed
    }

static func _apply_peripheral_scan(seed_value: int, payload: Dictionary) -> void:
    var trajectory_variant: Variant = payload.get("trajectory", {})
    var task_variant: Variant = payload.get("task", {})
    var exercise_variant: Variant = payload.get("exercise_parameters", {})
    var trajectory: Dictionary = trajectory_variant.duplicate(true) if trajectory_variant is Dictionary else {}
    var task: Dictionary = task_variant.duplicate(true) if task_variant is Dictionary else {}
    var exercise: Dictionary = exercise_variant.duplicate(true) if exercise_variant is Dictionary else {}
    var frame_count := int(payload.get("frame_count", 510))
    var fps := int(payload.get("fps", 30))
    var tier := int(exercise.get("difficulty_tier", 2))

    var event_count := 8
    match tier:
        1: event_count = 9
        2: event_count = 12
        3: event_count = 14
        4: event_count = 16
        _: event_count = 18

    var rings := [0.245, 0.355, 0.450]
    var logistic_x := lerpf(0.12, 0.88, _unit(seed_value, 811))
    var logistic_r := lerpf(3.86, 3.98, _unit(seed_value, 817))
    var events: Array = []
    var threat_count := 0
    var distractor_count := 0
    var last_start := -1000
    for i in range(event_count):
        logistic_x = logistic_r * logistic_x * (1.0 - logistic_x)
        var angle := logistic_x * TAU
        var ring_index := _index(seed_value, 820 + i, rings.size())
        var kind := "threat" if (_index(seed_value, 850 + i, 100) < 48) else "distractor"
        if i == event_count - 1 and threat_count == 0:
            kind = "threat"
        if kind == "threat": threat_count += 1
        else: distractor_count += 1
        var base_fraction := 0.0 if event_count <= 1 else float(i) / float(event_count - 1)
        var jitter := lerpf(-0.018, 0.018, _unit(seed_value, 870 + i))
        var fraction := clampf(0.10 + base_fraction * 0.80 + jitter, 0.08, 0.94)
        var start_frame := int(round(fraction * float(maxi(1, frame_count - 1))))
        # Hard tiers may deliberately create a pair at the same onset; others keep
        # a minimum gap so the peripheral field remains legible.
        var allow_overlap := tier >= 4 and i > 0 and (i % 5 == 0)
        if not allow_overlap and start_frame - last_start < 14:
            start_frame = last_start + 14
        start_frame = mini(frame_count - 12, start_frame)
        last_start = start_frame
        var duration_frames := 6 + _index(seed_value, 900 + i, 13)
        events.append({
            "id": "e%d" % (i + 1),
            "kind": kind,
            "ring_index": ring_index,
            "radius_norm": rings[ring_index],
            "angle_rad": angle,
            "angle_deg": rad_to_deg(angle),
            "frame_start": start_frame,
            "duration_frames": duration_frames,
            "duration_ms": duration_frames * 1000.0 / float(maxi(1, fps)),
            "pulse_pattern": "double" if kind == "threat" else "single",
            "simultaneous_allowed": allow_overlap
        })

    var anchor_interval := 75 + _index(seed_value, 931, 16)
    var anchor_sequence := ["TRIANGLE", "CIRCLE", "SQUARE"]
    trajectory["type"] = "polar_logistic_orbits"
    trajectory["profile"] = "polar_logistic_orbits_seeded_v1"
    trajectory["coordinate_space"] = "normalized_body_0_1_min_dimension"
    trajectory["center_normalized"] = [0.5, 0.5]
    trajectory["ring_radii_normalized"] = rings
    trajectory["logistic_parameter"] = logistic_r
    trajectory["seed_authoring_version"] = VERSION

    task["type"] = "peripheral_scan"
    task["target_id"] = "central_anchor"
    task["anchor_fixed"] = true
    task["anchor_sequence"] = anchor_sequence
    task["anchor_interval_frames"] = anchor_interval
    task["events"] = events
    task["threat_count"] = threat_count
    task["distractor_count"] = distractor_count
    var threat_frame_starts: Array = []
    var distractor_frame_starts: Array = []
    for event in events:
        if not event is Dictionary:
            continue
        if str(event.get("kind", "")) == "threat":
            threat_frame_starts.append(int(event.get("frame_start", -1)))
        else:
            distractor_frame_starts.append(int(event.get("frame_start", -1)))
    task["answer_sheet"] = {
        "threat_count": threat_count,
        "distractor_count": distractor_count,
        "threat_frame_starts": threat_frame_starts,
        "distractor_frame_starts": distractor_frame_starts
    }

    exercise["generator"] = "peripheral_scan"
    exercise["pacing_mode"] = "authored_polar_schedule"
    payload["exercise_parameters"] = exercise
    payload["trajectory"] = trajectory
    payload["task"] = task
    payload["seed_motion"] = {
        "enabled": true,
        "family": "peripheral_scan",
        "version": VERSION,
        "seed": int(seed_value),
        "threat_count": threat_count,
        "distractor_count": distractor_count,
        "logistic_parameter": logistic_r,
        "anchor_interval_frames": anchor_interval
    }

static func _bspline_point(control_points: Array, segment: int, u: float) -> Vector2:
    var count := control_points.size()
    var p0 := _cp(control_points, segment % count)
    var p1 := _cp(control_points, (segment + 1) % count)
    var p2 := _cp(control_points, (segment + 2) % count)
    var p3 := _cp(control_points, (segment + 3) % count)
    var u2 := u * u
    var u3 := u2 * u
    var b0 := (-u3 + 3.0 * u2 - 3.0 * u + 1.0) / 6.0
    var b1 := (3.0 * u3 - 6.0 * u2 + 4.0) / 6.0
    var b2 := (-3.0 * u3 + 3.0 * u2 + 3.0 * u + 1.0) / 6.0
    var b3 := u3 / 6.0
    return p0 * b0 + p1 * b1 + p2 * b2 + p3 * b3

static func _cp(control_points: Array, index: int) -> Vector2:
    var point: Array = control_points[index]
    return Vector2(float(point[0]), float(point[1]))

static func _sample_lut(lut: Array, distance_fraction: float) -> Vector2:
    if lut.is_empty():
        return Vector2(0.5, 0.5)
    var target := clampf(distance_fraction, 0.0, 1.0)
    var lo := 0
    var hi := lut.size() - 1
    while lo < hi:
        var mid := int(floor(float(lo + hi) * 0.5))
        if float(lut[mid].get("distance", 0.0)) < target:
            lo = mid + 1
        else:
            hi = mid
    var i := maxi(0, lo - 1)
    var a: Dictionary = lut[i]
    var b: Dictionary = lut[mini(lut.size() - 1, i + 1)]
    var da := float(a.get("distance", 0.0))
    var db := float(b.get("distance", da + 0.000001))
    var t := 0.0 if is_equal_approx(da, db) else clampf((target - da) / (db - da), 0.0, 1.0)
    return Vector2(lerpf(float(a.get("x", 0.5)), float(b.get("x", 0.5)), t), lerpf(float(a.get("y", 0.5)), float(b.get("y", 0.5)), t))

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
