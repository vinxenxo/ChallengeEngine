class_name VisualAuthoringRegistry
extends RefCounted

## C10-A — Strict routing registry.
## No normalization, aliases, or silent fallbacks.

static func supports(domain_family: String, subtype: String) -> bool:
    if domain_family == "visual_loop":
        return VisualLoopAuthoringAdapter.allowed_subtypes().has(subtype)
    if domain_family == "visual_drill":
        return VisualDrillAuthoringAdapter.allowed_subtypes().has(subtype)
    return false
