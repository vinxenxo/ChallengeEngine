# res://core/runtime/visual_drill/generators/PeripheralScanGenerator.gd
class_name PeripheralScanGenerator
extends VisualDrillGenerator

## C11-C.9 / Peripheral Scan mechanic baseline v1.0.
## Runtime consumes the authored polar schedule and emits only the current
## central-anchor state plus active peripheral event state.

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const CENTER := Vector2(270.0, 480.0)

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
    return generate_with_variation(frame_index, total_frames, drill_parameters, {})

func generate_with_variation(frame_index: int, total_frames: int, drill_parameters: Dictionary, variation: Dictionary) -> Dictionary:
    var progress := 0.0 if total_frames <= 1 else clampf(float(frame_index) / float(total_frames - 1), 0.0, 1.0)
    var trajectory: Dictionary = drill_parameters.get("trajectory", {}) if drill_parameters.get("trajectory", {}) is Dictionary else {}
    var task: Dictionary = drill_parameters.get("task", {}) if drill_parameters.get("task", {}) is Dictionary else {}
    var exercise: Dictionary = drill_parameters.get("exercise_parameters", {}) if drill_parameters.get("exercise_parameters", {}) is Dictionary else {}
    var fps := maxi(1, int(drill_parameters.get("fps", 30)))

    var anchor_sequence: Array = task.get("anchor_sequence", ["TRIANGLE", "CIRCLE", "SQUARE"])
    var anchor_interval := maxi(1, int(task.get("anchor_interval_frames", 80)))
    var anchor_index := int(floor(float(frame_index) / float(anchor_interval))) % maxi(1, anchor_sequence.size())
    var anchor_shape := str(anchor_sequence[anchor_index]) if not anchor_sequence.is_empty() else "CIRCLE"

    var active_events: Array = []
    var authored_events: Array = task.get("events", [])
    for event in authored_events:
        if not event is Dictionary:
            continue
        var start := int(event.get("frame_start", -1))
        var duration := int(event.get("duration_frames", 0))
        if frame_index < start or frame_index >= start + duration:
            continue
        var local_frame := frame_index - start
        var pulse := _pulse_strength(str(event.get("kind", "distractor")), local_frame, duration)
        if pulse <= 0.001:
            continue
        var active: Dictionary = event.duplicate(true)
        active["local_frame"] = local_frame
        active["pulse_strength"] = pulse
        active["pulse_index"] = 2 if str(event.get("kind", "distractor")) == "threat" and local_frame >= int(duration * 0.5) else 1
        active_events.append(active)

    var pattern_variant := clampf(float(variation.get("pattern_variant", 0.0)), 0.0, 0.999999)
    var amplitude_variant := clampf(float(variation.get("amplitude_variant", 0.0)), 0.0, 0.999999)
    var central_anchor := {
        "x": CENTER.x,
        "y": CENTER.y,
        "shape": anchor_shape,
        "shape_index": anchor_index,
        "sequence_length": anchor_sequence.size()
    }

    var primary_target := {
        "id": "central_anchor",
        "x": CENTER.x,
        "y": CENTER.y,
        "radius": 24.0,
        "highlighted": true,
        "status": "active",
        "role": "fixation_anchor"
    }

    return {
        "generator_type": "peripheral_scan",
        "progress": progress,
        "stimulus_state": {"type": "central_fixation_anchor", "x": CENTER.x, "y": CENTER.y, "active": true},
        "target_states": [primary_target],
        "distractor_states": [],
        "trajectory_state": {
            "type": "polar_logistic_orbits",
            "center": {"x": CENTER.x, "y": CENTER.y},
            "ring_radii_normalized": trajectory.get("ring_radii_normalized", [0.245, 0.355, 0.450]),
            "active_events": active_events
        },
        "task_state": {
            "type": "peripheral_scan",
            "anchor_fixed": true,
            "anchor_state": central_anchor,
            "active_events": active_events,
            "threat_count": int(task.get("threat_count", 0)),
            "distractor_count": int(task.get("distractor_count", 0)),
            "answer_sheet": task.get("answer_sheet", {}),
            "fps": fps
        },
        "parameters": {
            "pattern_variant": pattern_variant,
            "amplitude_variant": amplitude_variant,
            "speed_multiplier": float(exercise.get("speed_multiplier", 1.0)),
            "pacing_mode": str(exercise.get("pacing_mode", "authored_polar_schedule"))
        }
    }

func _pulse_strength(kind: String, local_frame: int, duration_frames: int) -> float:
    var duration := float(maxi(1, duration_frames))
    var x := float(local_frame)
    if kind == "threat":
        var c1 := duration * 0.24
        var c2 := duration * 0.66
        var sigma := maxf(1.0, duration * 0.12)
        return maxf(exp(-pow((x - c1) / sigma, 2.0)), exp(-pow((x - c2) / sigma, 2.0)))
    var c := duration * 0.48
    var sigma_single := maxf(1.0, duration * 0.18)
    return exp(-pow((x - c) / sigma_single, 2.0))
