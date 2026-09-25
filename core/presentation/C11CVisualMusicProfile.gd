class_name C11CVisualMusicProfile
extends RefCounted

## C11-C 2.10.1 — semantic music binding service.
## Presentation/delivery metadata only. It does not consume gameplay frames or answer sheets.

const PROFILE_PATH: String = "res://profiles/presentation/c11c_visual_music_profiles.json"
static var _cached_data: Dictionary = {}

static func _load_data() -> Dictionary:
    if not _cached_data.is_empty():
        return _cached_data
    if not FileAccess.file_exists(PROFILE_PATH):
        return {}
    var parsed = JSON.parse_string(FileAccess.get_file_as_string(PROFILE_PATH))
    if parsed is Dictionary:
        _cached_data = parsed
    return _cached_data

static func binding_for(route: String) -> Dictionary:
    var data := _load_data()
    var bindings: Dictionary = data.get("bindings", {})
    var binding: Variant = bindings.get(route, {})
    return binding.duplicate(true) if binding is Dictionary else {}

static func profile_for(route: String) -> String:
    return str(binding_for(route).get("profile", ""))

static func mode() -> String:
    return str(_load_data().get("mode", ""))

static func metadata_for(route: String) -> Dictionary:
    var data := _load_data()
    var binding := binding_for(route)
    var profile_id := str(binding.get("profile", ""))
    for entry_variant in data.get("profiles", []):
        if entry_variant is Dictionary and str(entry_variant.get("id", "")) == profile_id:
            return {"route": route, "mode": mode(), "binding": binding, "profile": entry_variant.duplicate(true)}
    return {"route": route, "mode": mode(), "binding": binding, "profile": {"id": profile_id}}
