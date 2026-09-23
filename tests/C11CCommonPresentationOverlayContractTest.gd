extends SceneTree

## C11-C 2.2.2 common presentation contract. Source-level smoke contract for all five loops.

var failures: Array[String] = []

func _initialize() -> void:
    var family_files := [
        "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd",
        "res://tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd",
        "res://tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.gd",
        "res://tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.gd",
        "res://tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.gd"
    ]

    for path in family_files:
        var source := FileAccess.get_file_as_string(path)
        _assert(source.find("C11CVisualEditorialLayer.gd") >= 0, path + " must use the shared editorial layer.")
        _assert(source.find('"matrix_enabled": true') >= 0, path + " must enable the common Matrix presentation.")
        _assert(source.find("_mount_editorial(frame)") >= 0, path + " must mount the shared editorial layer.")
        _assert(source.find("_header_animator") < 0 and source.find("_header_math") < 0 and source.find("_header_hook") < 0, path + " must not keep duplicate header animation state.")

    var road_source := FileAccess.get_file_as_string("res://tools/prototypes/c11c_living_particles_v1/LivingParticlesTronRoad.gd")
    _assert(road_source.find("VANISHING_POINT") >= 0, "Living Particles Tron road must define a perspective vanishing point.")
    _assert(road_source.find("_travel") >= 0, "Living Particles Tron road must animate forward travel.")
    var layer_source := FileAccess.get_file_as_string("res://core/presentation/C11CVisualEditorialLayer.gd")
    _assert(layer_source.find("const HEADER_FONT_SIZE := 23") >= 0, "Shared header font must be 23 logical px in C11-C 2.2.2.")
    _assert(layer_source.find("const HEADER_MAX_WIDTH := CONTENT_WIDTH") >= 0, "Header width must stay inside the shared content margins.")
    var particle_source := FileAccess.get_file_as_string("res://tools/prototypes/c11c_living_particles_v1/LivingParticlesRenderer.gd")
    _assert(particle_source.find("LivingParticlesBackground") >= 0, "Living Particles must own a separate Body background beneath the Tron road.")
    var shader_source := FileAccess.get_file_as_string("res://tools/prototypes/c11c_living_particles_v1/LivingParticles.gdshader")
    _assert(shader_source.find("particle_alpha") >= 0, "Particle shader must composite transparently over the Tron road.")
    var reviewer_source := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_visual_drill_review.ps1")
    _assert(reviewer_source.find("C11CVisualDrillReviewEnvelopeGenerator.gd") >= 0, "Drill reviewer must generate envelopes for requested seeds.")
    _assert(reviewer_source.find("MATRIX HEADER TRANSITION: ON") >= 0, "Drill review metadata must report Matrix ON.")
    _assert(reviewer_source.find("[switch]$Smoke") >= 0, "Drill reviewer must expose a single-seed smoke mode.")

    if failures.is_empty():
        print("[C11C_COMMON_PRESENTATION_OVERLAY_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_COMMON_PRESENTATION_OVERLAY_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
