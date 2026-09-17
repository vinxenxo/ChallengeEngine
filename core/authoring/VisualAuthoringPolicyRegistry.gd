class_name VisualAuthoringPolicyRegistry
extends RefCounted

## C10-A.1 — Production visual authoring policy registry.
## Loads the 9 product policies from profiles/difficulty/.
## No RNG, runtime, presentation rendering or generator access.

static var _cache: Dictionary = {}

static func policy_id(domain_family: String, subtype: String) -> String:
    return "%s_%s" % [domain_family, subtype]

static func get_policy(domain_family: String, subtype: String) -> Dictionary:
    var id := policy_id(domain_family, subtype)
    if _cache.has(id):
        return _cache[id].duplicate(true)

    var path := "res://profiles/difficulty/%s.json" % id
    if not FileAccess.file_exists(path):
        return {}

    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return {}

    var parsed: Variant = JSON.parse_string(file.get_as_text())
    file.close()
    if not (parsed is Dictionary):
        return {}

    var policy: Dictionary = parsed
    if str(policy.get("domain_family", "")) != domain_family:
        return {}
    if str(policy.get("subtype", "")) != subtype:
        return {}

    _cache[id] = policy.duplicate(true)
    return policy.duplicate(true)

static func clear_cache() -> void:
    _cache.clear()
