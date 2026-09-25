extends SceneTree

## C11-C 2.11.0 — canonical technical/artistic/production family nomenclature contract.

const CATALOG_PATH := "res://profiles/presentation/c11c_visual_family_catalog.json"
const EXPECTED := {
    "geometric": ["Geometric Waves", "c11c_geometric_waves_v1"],
    "fractal": ["Fractal Bloom", "c11c_fractal_bloom_v1"],
    "kaleidoscope": ["Sacred Symmetry", "c11c_sacred_symmetry_v1"],
    "particle_flow": ["Living Particles", "c11c_living_particles_v1"],
    "vector_field": ["Invisible Forces", "c11c_invisible_forces_v1"]
}

var failures: Array[String] = []

func _initialize() -> void:
    _assert(FileAccess.file_exists(CATALOG_PATH), "Canonical Visual Loop family catalog must exist.")
    var data = JSON.parse_string(FileAccess.get_file_as_string(CATALOG_PATH))
    _assert(data is Dictionary, "Visual Loop family catalog must be valid JSON.")
    if not data is Dictionary:
        _conclude()
        return
    var families: Array = data.get("families", [])
    _assert(families.size() == 5, "Exactly five canonical Visual Loop families must be recorded.")
    var seen: Dictionary = {}
    for entry_variant in families:
        if not entry_variant is Dictionary:
            _assert(false, "Catalog entries must be dictionaries.")
            continue
        var entry: Dictionary = entry_variant
        var technical_id := str(entry.get("technical_id", ""))
        seen[technical_id] = true
        _assert(EXPECTED.has(technical_id), "Unexpected Visual Loop technical_id: %s" % technical_id)
        if EXPECTED.has(technical_id):
            _assert(str(entry.get("artistic_name", "")) == str(EXPECTED[technical_id][0]), "%s artistic name mismatch." % technical_id)
            _assert(str(entry.get("production_id", "")) == str(EXPECTED[technical_id][1]), "%s production id mismatch." % technical_id)
    _assert(seen.size() == 5, "Visual Loop technical IDs must be unique.")
    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C11C_VISUAL_FAMILY_NOMENCLATURE_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_VISUAL_FAMILY_NOMENCLATURE_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
