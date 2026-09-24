# res://core/runtime/visual_drill/generators/PursuitGenerator.gd
class_name PursuitGenerator
extends VisualDrillGenerator

## C11-C.8 / Pursuit mechanic baseline v1.0.
## Runtime consumes an authored uniform cubic B-spline path already parameterized
## by arc length. It does not evaluate spline geometry or invent cognitive events.

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const CENTER := Vector2(270.0, 480.0)

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
    return generate_with_variation(frame_index, total_frames, drill_parameters, {})

func generate_with_variation(frame_index: int, total_frames: int, drill_parameters: Dictionary, variation: Dictionary) -> Dictionary:
    var progress := 0.0 if total_frames <= 1 else clampf(float(frame_index) / float(total_frames - 1), 0.0, 1.0)
    var trajectory: Dictionary = drill_parameters.get("trajectory", {}) if drill_parameters.get("trajectory", {}) is Dictionary else {}
    var task: Dictionary = drill_parameters.get("task", {}) if drill_parameters.get("task", {}) is Dictionary else {}
    var exercise: Dictionary = drill_parameters.get("exercise_parameters", {}) if drill_parameters.get("exercise_parameters", {}) is Dictionary else {}
    var samples: Array = trajectory.get("position_samples_normalized", [])
    if samples.is_empty():
        return _fail_state("Pursuit requires authored arc-length position samples.")

    var sample_index := mini(samples.size() - 1, maxi(0, frame_index))
    var point: Array = samples[sample_index]
    var position := _normalized_body_to_logical(Vector2(float(point[0]), float(point[1])))
    var previous_point := point
    if sample_index > 0:
        previous_point = samples[sample_index - 1]
    var previous := _normalized_body_to_logical(Vector2(float(previous_point[0]), float(previous_point[1])))
    var fps := float(maxi(1, int(drill_parameters.get("fps", 30))))
    var velocity := (position - previous) * fps if sample_index > 0 else Vector2.ZERO
    var speed_factor := 1.0
    var speed_samples: Array = trajectory.get("speed_factor_samples", [])
    if sample_index < speed_samples.size():
        speed_factor = float(speed_samples[sample_index])

    var sizygia_event := _active_sizygia(task.get("sizygia_events", []), frame_index)
    var camouflage_factor := _resolve_camouflage_factor(trajectory.get("camouflage_zones", []), progress)
    var target_radius := clampf(float(trajectory.get("target_radius", 20.0)), 16.0, 24.0)
    var pursuit_variant := clampf(float(variation.get("pursuit_variant", 0.0)), 0.0, 0.999999)

    var target := {
        "id": "t1",
        "x": position.x,
        "y": position.y,
        "radius": target_radius,
        "highlighted": true,
        "status": "active",
        "role": "pursuit_target"
    }

    return {
        "generator_type": "pursuit",
        "progress": progress,
        "stimulus_state": {"type": "pursuit_target", "x": position.x, "y": position.y, "active": true},
        "target_states": [target],
        "distractor_states": [],
        "trajectory_state": {
            "type": "uniform_cubic_bspline",
            "parameterization": "arc_length",
            "position": {"x": position.x, "y": position.y},
            "normalized_position": {"x": float(point[0]), "y": float(point[1])},
            "velocity": {"x": velocity.x, "y": velocity.y},
            "speed_px_per_second": velocity.length(),
            "arc_length_progress": progress,
            "speed_factor": speed_factor,
            "camouflage_contrast": camouflage_factor,
            "sample_index": sample_index
        },
        "task_state": {
            "type": "pursuit",
            "target_id": "t1",
            "sizygia_active": not sizygia_event.is_empty(),
            "sizygia_index": int(sizygia_event.get("index", 0)),
            "sizygia_frame_start": int(sizygia_event.get("frame_start", -1)),
            "sizygia_duration_frames": int(sizygia_event.get("duration_frames", 0)),
            "sizygia_count": int(task.get("sizygia_count", 0)),
            "camouflage_active": camouflage_factor < 0.999,
            "camouflage_contrast": camouflage_factor
        },
        "parameters": {
            "pursuit_variant": pursuit_variant,
            "trajectory_profile": str(trajectory.get("profile", "uniform_cubic_bspline_arc_length_v1")),
            "speed_multiplier": float(exercise.get("speed_multiplier", 1.0)),
            "pacing_mode": str(exercise.get("pacing_mode", "authored_arc_length"))
        }
    }

func _active_sizygia(events_variant: Variant, frame_index: int) -> Dictionary:
    var events: Array = events_variant if events_variant is Array else []
    for event in events:
        if not event is Dictionary:
            continue
        var start := int(event.get("frame_start", -1))
        var duration := int(event.get("duration_frames", 0))
        if frame_index >= start and frame_index < start + duration:
            return event
    return {}

func _resolve_camouflage_factor(zones_variant: Variant, progress: float) -> float:
    var zones: Array = zones_variant if zones_variant is Array else []
    var factor := 1.0
    for zone in zones:
        if not zone is Dictionary:
            continue
        var start := float(zone.get("start_progress", 0.0))
        var end := float(zone.get("end_progress", 0.0))
        if progress >= start and progress <= end:
            var minimum := clampf(float(zone.get("minimum_contrast", 0.15)), 0.05, 1.0)
            var local := clampf((progress - start) / maxf(0.0001, end - start), 0.0, 1.0)
            var envelope := sin(local * PI)
            factor = minf(factor, lerpf(1.0, minimum, envelope))
    return factor

func _normalized_body_to_logical(point: Vector2) -> Vector2:
    return Vector2(
        clampf(point.x, 0.12, 0.88) * BODY_RECT.size.x,
        BODY_RECT.position.y + clampf(point.y, 0.12, 0.88) * BODY_RECT.size.x
    )

func _fail_state(message: String) -> Dictionary:
    return {
        "generator_type": "pursuit",
        "progress": 0.0,
        "stimulus_state": {"type": "pursuit_target", "x": CENTER.x, "y": CENTER.y, "active": false},
        "target_states": [],
        "distractor_states": [],
        "trajectory_state": {},
        "task_state": {"type": "pursuit", "error": message},
        "parameters": {}
    }
