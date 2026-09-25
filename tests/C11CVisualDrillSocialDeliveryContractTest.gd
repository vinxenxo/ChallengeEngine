extends SceneTree

## C11-C 2.10.1 — Visual Drill social sidecar delivery contract.
## Production review runner must emit one .txt sidecar for every generated family/seed.

const RUNNER_SOURCE := "res://tools/prototypes/c11c_bulk/run_c11c_visual_drill_review.ps1"
const GENERATOR_SOURCE := "res://tools/prototypes/c11c_bulk/C11CVisualDrillReviewEnvelopeGenerator.gd"
const FAMILIES := ["tracking", "saccade", "pursuit", "peripheral_scan"]

var failures: Array[String] = []

func _initialize() -> void:
    var runner := FileAccess.get_file_as_string(RUNNER_SOURCE)
    var generator := FileAccess.get_file_as_string(GENERATOR_SOURCE)
    _assert(not runner.is_empty(), "Visual Drill review runner source must be available.")
    _assert(not generator.is_empty(), "Visual Drill envelope generator source must be available.")
    _assert(runner.find("VisualDrill_${family}_seed_${seed}_social.txt") >= 0, "Visual Drill runner must use the canonical social sidecar filename.")
    _assert(runner.find("Write-SocialSidecar") >= 0, "Visual Drill runner must write the social sidecar.")
    _assert(runner.find("Social sidecar was not created") >= 0, "Runner must fail closed when the social sidecar is missing.")
    _assert(runner.find("CTA POSITION: HEADER") >= 0, "Social sidecar must document CTA placement in the Header.")
    _assert(runner.find("FONTS: HEADER=INTER BOLD | FOOTER=NOTO SANS MONO REGULAR") >= 0, "Social sidecar must document the active C11-C font.")
    _assert(runner.find("FAMILY_MUSIC_V3") >= 0, "Visual Drill runner must use family-aware music mode.")
    _assert(runner.find("drill_motion_ambient_v2") < 0, "Visual Drill runner must not retain the superseded global drill ambient profile.")
    _assert(runner.find("global_ambient_master") < 0, "Visual Drill runner must not retain a global ambient master path.")
    _assert(runner.find("FOOTER DURING CTA: VISIBLE") >= 0, "Social metadata must document the CTA footer visibility state.")
    for family in FAMILIES:
        _assert(runner.find("'" + family + "'") >= 0, "Runner must retain explicit social metadata support for %s." % family)
    _assert(generator.find("VisualDrillSeedVariation/2.9.0") >= 0, "Generated authoring artifacts must identify the active 2.9.0 variation engine.")
    if failures.is_empty():
        print("[C11C_VISUAL_DRILL_SOCIAL_DELIVERY_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_VISUAL_DRILL_SOCIAL_DELIVERY_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
