class_name VisualLoopAuthoringAdapter
extends RefCounted

## C10-A — Family adapter for visual_loop.
## Subtype policy remains data/configuration; this class owns only canonical shape.

static func family_id() -> String:
    return "visual_loop"

static func allowed_subtypes() -> Array[String]:
    return ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]

static func build_payload(request: VisualAuthoringRequest, resolved: Dictionary) -> Dictionary:
    var p: Dictionary = resolved.duplicate(true)
    var frame_count := int(round(request.duration_seconds * float(request.fps)))

    return {
        "duration": request.duration_seconds,
        "fps": request.fps,
        "frame_count": frame_count,
        "loop": {
            "seamless": bool(p.get("seamless", true)),
            "boundary_tolerance": float(p.get("boundary_tolerance", 0.01))
        },
        "visual_parameters": {
            "generator": request.subtype,
            "layers": [
                {
                    "blend_mode": str(p.get("blend_mode", "normal")),
                    "speed": float(p.get("speed", 1.0)),
                    "complexity": int(p.get("complexity", 1)),
                    "color_palette": str(p.get("color_palette", "default"))
                }
            ]
        }
    }
