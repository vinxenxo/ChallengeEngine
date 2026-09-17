class_name VisualDrillAuthoringAdapter
extends RefCounted

## C10-A.1 — Family adapter for visual_drill.
## Preserves the frozen canonical drill payload shape.
## The canonical corpus currently uses arrays/objects for concrete stimulus state.

static func family_id() -> String:
    return "visual_drill"

static func allowed_subtypes() -> Array[String]:
    return ["tracking", "pursuit", "saccade", "peripheral_scan"]

static func build_payload(request: VisualAuthoringRequest, resolved: Dictionary) -> Dictionary:
    var required := ["speed_multiplier", "pacing_mode", "stimulus", "targets", "distractors", "trajectory", "task"]
    for key in required:
        if not resolved.has(key):
            return {"success": false, "errors": ["Visual drill policy missing required parameter '%s'." % key]}

    if not (resolved["stimulus"] is Dictionary):
        return {"success": false, "errors": ["Visual drill stimulus policy must be a Dictionary."]}
    if not (resolved["targets"] is Array):
        return {"success": false, "errors": ["Visual drill targets policy must be an Array."]}
    if not (resolved["distractors"] is Array):
        return {"success": false, "errors": ["Visual drill distractors policy must be an Array."]}
    if not (resolved["trajectory"] is Dictionary):
        return {"success": false, "errors": ["Visual drill trajectory policy must be a Dictionary."]}
    if not (resolved["task"] is Dictionary):
        return {"success": false, "errors": ["Visual drill task policy must be a Dictionary."]}

    var task: Dictionary = resolved["task"].duplicate(true)
    if str(task.get("type", "")) != request.subtype:
        return {"success": false, "errors": ["Visual drill task.type must match request subtype."]}

    var frame_count := int(round(request.duration_seconds * float(request.fps)))
    if frame_count < 1:
        return {"success": false, "errors": ["Resolved frame_count must be >= 1."]}

    var exercise := {
        "generator": request.subtype,
        "difficulty_tier": request.difficulty_tier,
        "speed_multiplier": float(resolved["speed_multiplier"]),
        "pacing_mode": str(resolved["pacing_mode"])
    }

    return {
        "success": true,
        "errors": [],
        "payload": {
            "duration": request.duration_seconds,
            "fps": request.fps,
            "frame_count": frame_count,
            "exercise_parameters": exercise,
            "stimulus": resolved["stimulus"].duplicate(true),
            "targets": resolved["targets"].duplicate(true),
            "distractors": resolved["distractors"].duplicate(true),
            "trajectory": resolved["trajectory"].duplicate(true),
            "task": task
        }
    }
