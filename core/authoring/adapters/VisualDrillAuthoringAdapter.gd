class_name VisualDrillAuthoringAdapter
extends RefCounted

## C10-A — Family adapter for visual_drill.
## Preserves the drill's independent root-level parameter contract.

static func family_id() -> String:
    return "visual_drill"

static func allowed_subtypes() -> Array[String]:
    return ["tracking", "pursuit", "saccade", "peripheral_scan"]

static func build_payload(request: VisualAuthoringRequest, resolved: Dictionary) -> Dictionary:
    var p: Dictionary = resolved.duplicate(true)
    var frame_count := int(round(request.duration_seconds * float(request.fps)))

    return {
        "duration": request.duration_seconds,
        "fps": request.fps,
        "frame_count": frame_count,
        "exercise_parameters": {
            "difficulty_tier": request.difficulty_tier,
            "speed_multiplier": float(p.get("speed_multiplier", 1.0)),
            "pacing_mode": str(p.get("pacing_mode", "constant"))
        },
        "stimulus": p.get("stimulus", {"type": "dot", "size": 10.0, "color": "white"}).duplicate(true),
        "targets": p.get("targets", [{"id": 0, "x": 0.0, "y": 0.0, "status": "active"}]).duplicate(true),
        "distractors": p.get("distractors", []).duplicate(true),
        "trajectory": p.get("trajectory", {"pattern": "linear", "speed": 1.0}).duplicate(true),
        "task": p.get("task", {"type": request.subtype}).duplicate(true)
    }
