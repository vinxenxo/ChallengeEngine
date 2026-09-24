extends SceneTree

const RendererSource = "res://core/presentation/rendering/PursuitRenderer.gd"
const TargetSource = "res://core/presentation/rendering/PursuitTargetLayer.gd"
const ShaderSource = "res://core/presentation/rendering/shaders/pursuit_dof.gdshader"

var failures: Array[String] = []

const EnvironmentSource = "res://core/presentation/rendering/C11CDrillEnvironment.gd"

func _initialize() -> void:
    _check_source_contracts()
    _conclude()

func _check_source_contracts() -> void:
    var renderer := FileAccess.get_file_as_string(RendererSource)
    var target := FileAccess.get_file_as_string(TargetSource)
    var shader := FileAccess.get_file_as_string(ShaderSource)
    _assert(renderer.find("PursuitTargetLayerClass") >= 0, "Pursuit must use a dedicated perceptual target layer.")
    _assert(renderer.find("DOF_SHADER") >= 0, "Pursuit must include the radial focus layer.")
    _assert(renderer.find("position_samples_normalized") < 0, "Renderer must not recompute or read raw authored position samples directly; it consumes runtime state only.")
    _assert(target.find("Euler") >= 0 or target.find("ring") >= 0, "Pursuit target must expose internal ring geometry.")
    _assert(shader.find("screen_texture") >= 0, "Pursuit radial DOF must use a screen-texture filter.")
    _assert(renderer.find("_hash01") >= 0, "Pursuit background must be deterministic from the seed.")
    _assert(target.find("sizygia_active") >= 0, "Target layer must react to authored sizygia state.")

    _assert(FileAccess.file_exists(EnvironmentSource), "Shared C11-C drill environment must be present.")

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C11C_PURSUIT_PRESENTATION_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_PURSUIT_PRESENTATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
