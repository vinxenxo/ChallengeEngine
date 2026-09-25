extends SceneTree

## C11-C 2.13.1 — robust seed uniqueness contract.

var failures: Array[String] = []
const COMMON := "res://tools/prototypes/c11c_bulk/C11CProductionBatchCommon.ps1"

func _initialize() -> void:
    var s := FileAccess.get_file_as_string(COMMON)
    _assert(not s.is_empty(), "Production batch common script must exist.")
    var grammar_tokens := [
        "harmonic_membrane", "radial_bloom", "astrolabe", "swarm",
        "dipole_field", "interference_plane", "dendritic_tunnel", "gear_train",
        "vortex", "vortex_field", "parametric_ribbon", "spiral_fractal",
        "polygon_orrery", "collision_cloud", "saddle_field", "lattice_wave",
        "fractal_filigree", "origami_mandala", "organic_pulse", "quadrupole_field",
        "orbital_wave", "nested_worlds", "celestial_chart", "magnetic_filament_cloud",
        "gravitational_lens", "topographic_basin", "scalar_potential"
    ]
    for grammar in grammar_tokens:
        _assert(s.find("Grammar='" + grammar + "'") >= 0, "Weekly schedule must contain " + grammar + ".")
    _assert(s.find("$Schedule.Count") >= 0 and s.find("$Seeds.Count") >= 0, "Batch runner must validate schedule/seed cardinality.")
    _assert(s.find("Sort-Object -Unique") >= 0 and s.find("Batch seeds must be unique.") >= 0, "Batch runner must reject repeated seeds.")
    _assert(s.find("unique_video_keys") >= 0, "Batch manifest must expose unique video keys.")
    _assert(s.find("artifacts\\production\\audiovisual") >= 0, "Batch must publish through the protected production audiovisual tree.")
    _assert(s.find("run_c11c_production.ps1") >= 0, "Batch must invoke the canonical production launcher.")
    _assert(s.find("-Family $item.Production -Seed $seed -Grammar $item.Grammar") >= 0, "Batch must pass family, seed and technical grammar to production.")
    if failures.is_empty():
        print("[C11C_PRODUCTION_BATCH_SCHEDULE_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for f in failures: push_error(f)
        print("[C11C_PRODUCTION_BATCH_SCHEDULE_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition: failures.append(message)
