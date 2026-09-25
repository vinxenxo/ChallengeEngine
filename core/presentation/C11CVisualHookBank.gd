class_name C11CVisualHookBank
extends RefCounted

## C11-C 2.11.1 — deterministic presentation/social hook bank.
## Presentation-only. Hooks are editorial copy; they never define gameplay truth.

const PATH: String = "res://profiles/presentation/c11c_visual_hooks.json"
static var _cache: Dictionary = {}

static func _load() -> Dictionary:
    if not _cache.is_empty():
        return _cache
    if not FileAccess.file_exists(PATH):
        return {}
    var parsed = JSON.parse_string(FileAccess.get_file_as_string(PATH))
    if parsed is Dictionary:
        _cache = parsed
    return _cache

static func hook_for(family: String, seed: int) -> String:
    var data := _load()
    var drills: Dictionary = data.get("visual_drills", {})
    var entry_variant: Variant = drills.get(family, {})
    if not entry_variant is Dictionary:
        return ""
    var entry: Dictionary = entry_variant
    var hooks_variant: Variant = entry.get("hooks", [])
    if not hooks_variant is Array or hooks_variant.is_empty():
        return ""
    var hooks: Array = hooks_variant
    var offset := int(entry.get("family_offset", 0))
    var index := posmod(int(seed) + offset, hooks.size())
    return str(hooks[index])

static func hook_index_for(family: String, seed: int) -> int:
    var data := _load()
    var drills: Dictionary = data.get("visual_drills", {})
    var entry_variant: Variant = drills.get(family, {})
    if not entry_variant is Dictionary:
        return -1
    var entry: Dictionary = entry_variant
    var hooks_variant: Variant = entry.get("hooks", [])
    if not hooks_variant is Array or hooks_variant.is_empty():
        return -1
    return posmod(int(seed) + int(entry.get("family_offset", 0)), hooks_variant.size())

static func hook_count_for(family: String) -> int:
    var data := _load()
    var drills: Dictionary = data.get("visual_drills", {})
    var entry_variant: Variant = drills.get(family, {})
    if not entry_variant is Dictionary:
        return 0
    var hooks_variant: Variant = entry_variant.get("hooks", [])
    return hooks_variant.size() if hooks_variant is Array else 0

static func loop_social_hook() -> String:
    var data := _load()
    var loops: Dictionary = data.get("visual_loops", {})
    return str(loops.get("default_social_hook", "¿Puedes notar dónde termina el bucle?"))
