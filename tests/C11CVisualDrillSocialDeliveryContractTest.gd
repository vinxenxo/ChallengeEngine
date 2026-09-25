extends SceneTree

## C11-C 2.11.1 — Visual Drill social sidecar delivery contract.
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
    _assert(runner.find("cta_position") >= 0 or runner.find("CTA POSITION: HEADER") >= 0, "Runner manifest must preserve CTA placement metadata.")
    _assert(runner.find("typography") >= 0 and runner.find("Inter Bold") >= 0 and runner.find("Noto Sans Mono Regular") >= 0, "Runner manifest must preserve active C11-C typography metadata.")
    _assert(runner.find("c11c_visual_hooks.json") >= 0, "Visual Drill runner must consume the canonical hook bank.")
    _assert(runner.find("hook_index") >= 0, "Visual Drill manifest must expose deterministic hook selection metadata.")
    _assert(runner.find("#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying") >= 0, "Visual Drill sidecar must include the four fixed hashtags.")
    _assert(runner.find("**$display**") >= 0, "Visual Drill social copy must use the new markdown-friendly format.")
    _assert(runner.find("FAMILY_MUSIC_V4") >= 0, "Visual Drill runner must use family-aware music mode.")
    _assert(runner.find("audio ambient") < 0, "Visual Drill runner must not hard-code an old single ambient public copy.")
    _assert(runner.find("drill_motion_ambient_v2") < 0, "Visual Drill runner must not retain the superseded global drill ambient profile.")
    _assert(runner.find("global_ambient_master") < 0, "Visual Drill runner must not retain a global ambient master path.")
    _assert(runner.find("footer_during_cta") >= 0 or runner.find("FOOTER DURING CTA: VISIBLE") >= 0, "Visual Drill manifest must document footer visibility during CTA.")
    for family in FAMILIES:
        _assert(runner.find("'" + family + "'") >= 0, "Runner must retain explicit social metadata support for %s." % family)
    _assert(generator.find("VisualDrillSeedVariation/2.9.0") >= 0, "Generated authoring artifacts must identify the active variation engine.")
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
