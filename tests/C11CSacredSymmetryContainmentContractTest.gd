extends SceneTree

## C11-C 2.16.0 — Sacred Symmetry Body containment contract.
var failures: Array[String] = []

func _initialize() -> void:
    var shader := FileAccess.get_file_as_string("res://tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetry.gdshader")
    _assert(shader.find("GEOMETRY_CONTAINMENT_SCALE = 0.98") >= 0, "Sacred Symmetry containment scale must be 0.98 in the balanced full-frame regime.")
    _assert(shader.find("clamp(macro_scale, 0.84, 1.02)") >= 0, "Sacred Symmetry macro scale must stay inside the Body safe range.")
    _assert(shader.find("p.x *= BODY_ASPECT") >= 0, "Sacred Symmetry Body aspect correction must avoid horizontal deformation.")
    _assert(shader.find("0.405 * ring_scale") >= 0, "Sacred Symmetry outer ring must remain inside the Body.")
    _assert(shader.find("grammar_scale = 1.10") >= 0, "Astrolabe must receive the targeted larger optical footprint.")
    _assert(shader.find("geometry_scale = clamp(geometry_scale, 0.88, 1.10)") >= 0, "Sacred Symmetry must allow a larger contained optical footprint.")
    var renderer := FileAccess.get_file_as_string("res://tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryRenderer.gd")
    _assert(renderer.find("BODY_RECT") >= 0, "Sacred Symmetry renderer must retain the canonical Body rectangle.")
    if failures.is_empty():
        print("[C11C_SACRED_SYMMETRY_CONTAINMENT_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for f in failures: push_error(f)
    print("[C11C_SACRED_SYMMETRY_CONTAINMENT_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition: failures.append(message)
