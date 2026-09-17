class_name VisualLoopAuthoringAdapter
extends RefCounted

## C10-A.1 — Family adapter for visual_loop.
## Owns only canonical payload shape. All subtype values come from the policy.

static func family_id() -> String:
    return "visual_loop"

static func allowed_subtypes() -> Array[String]:
    return ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]

static func build_payload(request: VisualAuthoringRequest, resolved: Dictionary) -> Dictionary:
    var required := ["seamless", "boundary_tolerance", "blend_mode", "speed", "complexity", "color_palette"]
    for key in required:
        if not resolved.has(key):
            return {"success": false, "errors": ["Visual loop policy missing required parameter '%s'." % key]}

    var frame_count := int(round(request.duration_seconds * float(request.fps)))
    if frame_count < 1:
        return {"success": false, "errors": ["Resolved frame_count must be >= 1."]}

    return {
        "success": true,
        "errors": [],
        "payload": {
            "duration": request.duration_seconds,
            "fps": request.fps,
            "frame_count": frame_count,
            "loop": {
                "seamless": bool(resolved["seamless"]),
                "boundary_tolerance": float(resolved["boundary_tolerance"])
            },
            "visual_parameters": {
                "generator": request.subtype,
                "layers": [
                    {
                        "blend_mode": str(resolved["blend_mode"]),
                        "speed": float(resolved["speed"]),
                        "complexity": int(resolved["complexity"]),
                        "color_palette": str(resolved["color_palette"])
                    }
                ]
            }
        }
    }
