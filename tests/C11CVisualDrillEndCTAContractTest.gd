extends SceneTree

## C11-C 2.7.2 — Visual Drill terminal CTA contract.
## Reuses the historical Challenge CTAComponent through the shared presentation UI.
## The phase is presentation-only and is appended after the canonical gameplay stream.

const Binder = preload("res://core/presentation/VisualDrillPresentationBinder.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")
const PresentationUI = preload("res://core/presentation/PresentationUI.gd")
const PhaseLogic = preload("res://core/presentation/VisualDrillPresentationPhaseLogic.gd")
const CTAComponent = preload("res://core/presentation/components/CTAComponent.gd")

var failures: Array[String] = []

func _initialize() -> void:
    _test_phase_boundaries()
    _test_all_families_bind_terminal_cta()
    await _test_shared_cta_component_path()
    _test_legacy_challenge_cta_path_is_preserved()
    _test_cta_component_instantiable()
    if failures.is_empty():
        print("[C11C_VISUAL_DRILL_END_CTA_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_VISUAL_DRILL_END_CTA_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)

func _test_phase_boundaries() -> void:
    _assert(PhaseLogic.countdown_frames(30) == 90, "Countdown must remain 90 frames at 30 FPS.")
    _assert(PhaseLogic.end_cta_frames(30) == 90, "End CTA must be 90 frames at 30 FPS.")
    _assert(PhaseLogic.total_presentation_frames(630, 30) == 810, "Tracking total must be 810 frames after adding the 3s end CTA.")
    _assert(PhaseLogic.total_presentation_frames(510, 30) == 690, "Saccade/default total must be 690 frames after adding the 3s end CTA.")
    _assert(PhaseLogic.phase_for_frame(89, 630, 30) == "PRE_ROLL", "Frame 89 must remain the final countdown frame.")
    _assert(PhaseLogic.phase_for_frame(90, 630, 30) == "GAME", "Frame 90 must begin gameplay.")
    _assert(PhaseLogic.phase_for_frame(719, 630, 30) == "GAME", "Tracking frame 719 must remain gameplay.")
    _assert(PhaseLogic.phase_for_frame(720, 630, 30) == "END_CTA", "Tracking frame 720 must begin end CTA.")
    _assert(PhaseLogic.phase_for_frame(809, 630, 30) == "END_CTA", "Tracking frame 809 must remain final CTA.")
    _assert(PhaseLogic.phase_for_frame(810, 630, 30) == "DONE", "Frame 810 must be outside the presentation envelope.")

func _test_all_families_bind_terminal_cta() -> void:
    var profile := PresentationProfile.new()
    var binder := Binder.new()
    if binder == null or not binder.has_method("bind_frame"):
        _assert(false, "VisualDrillPresentationBinder failed to instantiate; dependent parse errors must not be reported as PASS.")
        return
    binder.set_definition_context({
        "kind": "visual_drill",
        "seed": 5409,
        "payload": {
            "duration": 17.0,
            "fps": 30,
            "frame_count": 510,
            "exercise_parameters": {"difficulty_tier": 2, "speed_multiplier": 1.0}
        }
    })
    for family in ["tracking", "saccade", "pursuit", "peripheral_scan"]:
        var frame := {
            "frame_index": 509,
            "payload": {
                "generator_type": family,
                "parameters": {
                    "tracking_variant": 0.16,
                    "saccade_variant": 0.74
                },
                "target_states": [],
                "distractor_states": [],
                "trajectory_state": {},
                "task_state": {}
            }
        }
        var model: Dictionary = binder.bind_frame(frame, profile, "END_CTA", 600, 30, 690)
        _assert(bool(model.get("cta_visible", false)), "%s end CTA must be visible." % family)
        _assert(str(model.get("cta_main", "")) == "¿LO CONSEGUISTE?", "%s end CTA main mismatch." % family)
        _assert(str(model.get("cta_sub", "")) == "¿HASTA DÓNDE LLEGASTE?", "%s end CTA sub mismatch." % family)
        _assert(bool(model.get("cta_animated", false)), "%s end CTA must use presentation animation." % family)

func _test_shared_cta_component_path() -> void:
    var profile := PresentationProfile.new()
    var root := Control.new()
    root.size = Vector2(540.0, 960.0)
    get_root().add_child(root)
    var frame_scene: PackedScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
    var unified: UnifiedSocialFrame = frame_scene.instantiate() as UnifiedSocialFrame
    _assert(unified != null, "UnifiedSocialFrame must instantiate for the shared CTA path.")
    if unified == null:
        root.queue_free()
        await process_frame
        return
    root.add_child(unified)
    # UnifiedSocialFrame exposes its mount points through @onready members.
    # Wait one frame so _ready() has completed before PresentationUI resolves them.
    await process_frame
    var ui := PresentationUI.new(unified, "default_c6", profile, true)
    var footer_region: Control = unified.get_footer_content_root().get_parent() as Control
    _assert(footer_region != null, "Visual Drill shared footer region must be discoverable as a Control parent.")
    _assert(ui != null, "PresentationUI must instantiate for the shared UnifiedSocialFrame path.")
    if ui == null:
        root.queue_free()
        await process_frame
        return
    var binder := Binder.new()
    if binder == null or not binder.has_method("bind_frame"):
        _assert(false, "VisualDrillPresentationBinder failed to instantiate in shared UI path.")
        root.queue_free()
        await process_frame
        return
    binder.set_definition_context({
        "kind": "visual_drill",
        "seed": 5409,
        "payload": {"duration": 17.0, "fps": 30, "frame_count": 510, "exercise_parameters": {"difficulty_tier": 2}}
    })
    var model: Dictionary = binder.bind_frame({"payload": {"generator_type": "pursuit", "parameters": {}}}, profile, "END_CTA", 600, 30, 690)
    ui.apply_render_model(model)
    _assert(ui.cta != null, "Visual Drill end CTA must reuse CTAComponent.")
    if ui.cta == null:
        root.queue_free()
        await process_frame
        return
    _assert(ui.cta.visible, "Shared CTAComponent must become visible for END_CTA.")
    _assert(ui.cta.get_parent() == unified.get_header_content_root(), "Visual Drill END_CTA CTAComponent must be mounted in the HEADER.")
    _assert(ui.cta.get_parent() != unified.get_footer_content_root(), "Visual Drill END_CTA CTAComponent must not be mounted in the FOOTER.")
    _assert(footer_region != null and footer_region.visible, "Visual Drill END_CTA must keep the FooterRegion visible so telemetry text remains visible and no stale CTA surface is shown.")
    _assert(ui.cta.label_main.text == "¿LO CONSEGUISTE?", "Shared CTAComponent main label mismatch.")
    _assert(ui.cta.label_sub.text == "¿HASTA DÓNDE LLEGASTE?", "Shared CTAComponent sub label mismatch.")
    _assert(ui.cta.scale.x < 1.0, "Shared CTAComponent should be in its terminal entry animation path.")
    root.queue_free()
    await process_frame
func _test_legacy_challenge_cta_path_is_preserved() -> void:
    var source := FileAccess.get_file_as_string("res://core/presentation/PresentationUI.gd")
    _assert(source.find("if not use_c11c_shared_social_editorial") >= 0, "PresentationUI must preserve the legacy Challenge CTA path.")
    _assert(source.find("cta = CTAComponent.new()") >= 0, "PresentationUI must continue to instantiate the shared CTAComponent.")
    _assert(source.find("c11c_shared_footer_region.visible = true") >= 0, "PresentationUI must keep the shared Visual Drill FooterRegion visible during END_CTA.")

func _test_cta_component_instantiable() -> void:
    var cta = CTAComponent.new()
    _assert(cta != null and is_instance_valid(cta), "CTAComponent must instantiate without script errors.")
    if cta != null and is_instance_valid(cta):
        cta.free()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
