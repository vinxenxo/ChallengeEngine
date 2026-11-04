extends SceneTree

## Materializes a D-owned semantic Challenge payload from frozen C11-C runtime outputs.
## Default path: review-only source-timebase payload/descriptor and exit.
## Explicit --e4a-config test path: may render isolated off-screen SubViewport PNGs under
## artifacts/tests only, including alpha-composition over supplied, hash-pinned sample frames.
## Neither path emits production renderer input, dispatches D9.10, or writes production media.
const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const PresentationBinder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const C11CVisualEditorialLayerClass = preload("res://core/presentation/C11CVisualEditorialLayer.gd")
const ChallengeEditorialAdapter = preload("res://tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd")
const ChallengePath := "res://challenges/CHALLENGE_004.json"
const ManifestPath := "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const ContractPath := "res://definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json"
const FrozenManifestSha := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const ChallengeSha := "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
const ChallengeEditorialAdapterSha := "d17568882eb63ba2eb48649cb9cd46edafe122d72c0c5ed29275e79b8d6d5846"
const E4AApprovalPath := "res://definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json"
const E4AApprovalSha := "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"
const D15LayoutPath := "res://docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md"
const D15LayoutSha := "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461"
const D11MappingPath := "res://docs/current/d/D1.1_CHALLENGE_VISUAL_EDITORIAL_MAPPING_V1.0.md"
const D11MappingSha := "7060e72c6b32c31a3f1eb9f7bd242e9dbb3c792aecc2728f67ee86403af06e84"
const D17MappingPath := "res://docs/current/d/D1.7_CHALLENGE_VISUAL_EDITORIAL_DECLARATIVE_MAPPING.md"
const D17MappingSha := "283a659af9c9d8c482355ef77fedd0ccc7bfc7461b60b867ecc1a9ac3a60950a"
const E4AProposalPath := "res://docs/history/c11d/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_PROPOSAL_20261103_V1.md"
const E4AProposalSha := "a1151999003b890abedb5d3b73382d1861d8ef3a56b0768a10fe480cfa841405"
const E4APixelReportSchema := "C11E-E4A-CHALLENGE-PIXEL-RENDER-REPORT-V1"
const E4ADCompositorConfigSchema := "C11E-E4A-D-GODOT-COMPOSITOR-PIXEL-TEST-CONFIG-V1"
const E4ADCompositorReportSchema := "C11E-E4A-D-GODOT-COMPOSITOR-REAL-BODY-PIXEL-REPORT-V1"
const OutputSchema := "C11-D-D9-CHALLENGE-VISUAL-PAYLOAD-PREVIEW-V1"
const SourcePins := {
    "challenges/CHALLENGE_004.json": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "core/execution/ChallengeRuntimeBridge.gd": "c53f04df064b3697f8dd02cd779f8ef002a4e3e2d40fa0e01aa7d9b1a80a8191",
    "core/execution/ChallengeTimelineBuilder.gd": "35a47ad126a2e11577933a03b251f47732e580693e5c08e45d3b6af047c8c9af",
    "core/presentation/ChallengePresentationBinder.gd": "755ecfc9cc6e1ee51738938583217ab8a470c1a1f290bb107e91e19990d74b47",
    "core/presentation/PresentationProfile.gd": "187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24",
    "core/mechanics/parking/ParkingMechanicV2.gd": "c78dbc1adcc95ad4981f3c704c69630edc54c25473c479f10bb154efe6f105cd",
    "core/data/FrameSnapshot.gd": "61060d0937063400447cd5f2513265cb82d8e38017f5bd097c2870da03967180",
    "assets/c6/garage_background.svg": "c9d8acdae725ca7726fc8ad23a046e4aac4d9e454b45db40d2c770732b31ab1e",
    "assets/c6/car.svg": "93a6f78d9654f7917ab2287800858a937e9c68c458cc60bf417d6f2b98c1a96d",
    "assets/c6/parking_target.svg": "ec2dcafd7dfc99ff501eb2d93b93906680a30c48cf0741807cbbdd915a18cfb3"
}

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var manifest_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ManifestPath)
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != FrozenManifestSha:
        _fail("Frozen C11-C manifest hash mismatch.")
        return
    var source_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ChallengePath)
    if source_bytes.is_empty() or _sha256_bytes(source_bytes) != ChallengeSha:
        _fail("CHALLENGE_004 source bytes/hash mismatch.")
        return
    for rel_path: String in SourcePins.keys():
        var bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://" + rel_path)
        if bytes.is_empty() or _sha256_bytes(bytes) != str(SourcePins[rel_path]):
            _fail("Pinned C11-C source or physical asset hash mismatch: %s" % rel_path)
            return
    var adapter_bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd")
    if adapter_bytes.is_empty() or _sha256_bytes(adapter_bytes) != ChallengeEditorialAdapterSha:
        _fail("D-owned Challenge editorial adapter source pin mismatch.")
        return

    var source_value: Variant = JSON.parse_string(source_bytes.get_string_from_utf8())
    if not (source_value is Dictionary):
        _fail("Canonical Challenge source is not a JSON object.")
        return
    var source: Dictionary = source_value
    if str(source.get("challenge_id", "")) != "CHALLENGE_004" or str(source.get("mechanic", "")) != "parking_v2":
        _fail("Challenge identity changed.")
        return
    if not _contract_guard():
        _fail("Visual payload contract or governance locks changed.")
        return

    var first_result: Dictionary = RuntimeBridge.run_effective_pipeline(source)
    if not bool(first_result.get("success", false)):
        _fail("First frozen runtime invocation failed: %s" % str(first_result.get("error", "unknown")))
        return
    var second_result: Dictionary = RuntimeBridge.run_effective_pipeline(source)
    if not bool(second_result.get("success", false)):
        _fail("Repeated frozen runtime invocation failed.")
        return
    var first_context: Variant = first_result.get("context", null)
    var second_context: Variant = second_result.get("context", null)
    if first_context == null or second_context == null:
        _fail("Frozen runtime returned incomplete context.")
        return

    var first_payload_result: Dictionary = _build_payload(source, first_context)
    if not bool(first_payload_result.get("success", false)):
        _fail("First Challenge visual payload build failed: %s" % str(first_payload_result.get("error", "unknown")))
        return
    var second_payload_result: Dictionary = _build_payload(source, second_context)
    if not bool(second_payload_result.get("success", false)):
        _fail("Repeated Challenge visual payload build failed: %s" % str(second_payload_result.get("error", "unknown")))
        return

    var first_payload_hash: String = str(first_payload_result.get("payload_sha256", ""))
    var second_payload_hash: String = str(second_payload_result.get("payload_sha256", ""))
    var first_frame_hash: String = str(first_payload_result.get("frame_signature_sha256", ""))
    var second_frame_hash: String = str(second_payload_result.get("frame_signature_sha256", ""))
    var repeated_equal: bool = first_payload_hash == second_payload_hash and first_frame_hash == second_frame_hash
    if not repeated_equal:
        _fail("Repeated runtime did not produce identical visual payload/frame signatures.")
        return

    var payload: Dictionary = first_payload_result["payload"]
    var assets: Array = first_payload_result["asset_nodes"]
    var timeline: Dictionary = first_payload_result["source_timeline"]
    var frame_records_hash: String = str(first_payload_result["frame_records_sha256"])
    var model_hash: String = str(first_payload_result["render_model_sha256"])
    var inv: Dictionary = first_payload_result["simulation_invariance"]
    if not bool(inv.get("simulation_invariance", false)):
        _fail("Presentation rebind changed simulation frames or metrics.")
        return
    if not _validate_payload_in_memory(payload, assets, first_payload_hash, timeline, frame_records_hash):
        _fail("Materialized visual payload failed invariant checks.")
        return

    var e4a_config_path: String = _cmdline_value("--e4a-config")
    if not e4a_config_path.is_empty():
        print("E4A3_GODOT_START rendering=ENABLED headless=false")
        var e4a_result: Dictionary = await _run_e4a_pixel_test(payload, timeline, first_payload_hash, frame_records_hash, e4a_config_path)
        if not bool(e4a_result.get("success", false)):
            _fail("E4A isolated pixel test failed: %s" % str(e4a_result.get("error", "unknown")))
            return
        var e4a_report: Dictionary = e4a_result.get("report", {})
        if str(e4a_report.get("schema", "")) == E4ADCompositorReportSchema:
            print("C11E E4A D-OWNED GODOT REAL-BODY COMPOSITOR PASS | variants=3/3 | real_delivery_frames=6/6 | pixel_pngs=18/18 | comparisons=12/12 | gameplay_body_pixel_identity=PASS | hook_editorial_overlap=false | shared_header_fit=PASS | visual_placement=UNAPPROVED | production_dispatch=false | production_media=false | D4.8=BLOCKED | D9.10=PREPARE_ONLY | release_authority=NONE")
        else:
            print("C11E E4A CHALLENGE EDITORIAL PIXEL RENDER PASS | variants=3/3 | source_frames=420/420 | text_regions=HEADER+FOOTER | phase_windows=HOOK+CTA | challenge_overlay=BLOCKED_GEOMETRY_UNRESOLVED | language=METADATA_ONLY | fixture_body_pixels_unchanged=true | gameplay_body_pixel_identity=NOT_TESTED | production_dispatch=false | production_media=false | D4.8=BLOCKED | D9.10=PREPARE_ONLY | release_authority=NONE")
        print("C11E E4A CHALLENGE EDITORIAL PIXEL RENDER SUMMARY=" + JSON.stringify(_stable_value(e4a_report)))
        quit(0)
        return

    var source_lineage: Array[Dictionary] = []
    source_lineage.append({"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": FrozenManifestSha})
    for rel_path: String in SourcePins.keys():
        source_lineage.append({"path": rel_path, "sha256": str(SourcePins[rel_path])})
    # Include the dynamically hashed input contract itself in the emitted lineage.
    # It is intentionally not self-pinned inside its own JSON document.
    var contract_lineage_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ContractPath)
    if contract_lineage_bytes.is_empty():
        _fail("Visual payload contract unavailable for source lineage.")
        return
    source_lineage.append({"path": "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json", "sha256": _sha256_bytes(contract_lineage_bytes)})
    source_lineage.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return str(a.get("path", "")) < str(b.get("path", "")))

    var report: Dictionary = {
        "schema": OutputSchema,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FrozenManifestSha,
        "challenge_source_sha256": ChallengeSha,
        "payload_sha256": first_payload_hash,
        "payload_identity": {
            "challenge_id": "CHALLENGE_004",
            "mechanic": "parking_v2",
            "mechanic_version": "2.0",
            "presentation_profile_id": "social_default_v1",
            "coordinate_space": "CANVAS_1080X1920",
            "materialization": "IN_MEMORY_ONLY_SOURCE_TIMEBASE"
        },
        "asset_nodes": assets,
        "source_timeline": timeline,
        "animation": {
            "frame_source": "SimulationResult.frames",
            "source_fps": 60,
            "game_frame_count": 420,
            "frame_record_count": 420,
            "frame_records_sha256": frame_records_hash,
            "snapshot_fields_included": ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"],
            "simulation_telemetry_included": false,
            "winning_frame_sampling_used": false,
            "delivery_resampling": "UNRESOLVED_NOT_APPLIED"
        },
        "presentation": {
            "render_model_sha256": model_hash,
            "profile_source_canvas": {"width": 540, "height": 960},
            "profile_master_output": {"width": 1080, "height": 1920},
            "source_coordinate_space": "CANVAS_1080X1920",
            "coordinate_projection": "UNRESOLVED_NOT_APPLIED"
        },
        "determinism": {
            "runtime_repeat_equal": true,
            "payload_repeat_equal": first_payload_hash == second_payload_hash,
            "frame_signature_repeat_equal": first_frame_hash == second_frame_hash,
            "simulation_invariance": true
        },
        "execution_boundary": {
            "mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY",
            "payload_written": false,
            "media_output_created": false,
            "renderer_native_input_emitted": false,
            "renderer_dispatch_invoked": false,
            "renderer_activation": false,
            "c11c_source_mutation": false,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "output_artifact_path": null
        },
        "source_lineage": source_lineage
    }
    print("C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW PASS | payload=1/1 | assets=3/3 | game_frames=420/420@60FPS | deterministic=2/2 | coordinate_projection=UNRESOLVED_NOT_APPLIED | delivery_resampling=UNRESOLVED_NOT_APPLIED | telemetry=NOT_BOUND | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    print("C11-D CHALLENGE VISUAL PAYLOAD PREVIEW SUMMARY=" + JSON.stringify(report))
    quit(0)

func _cmdline_value(option_name: String) -> String:
    var args: PackedStringArray = OS.get_cmdline_user_args()
    for index: int in range(args.size()):
        if str(args[index]) == option_name and index + 1 < args.size():
            return str(args[index + 1])
        if str(args[index]).begins_with(option_name + "="):
            return str(args[index]).substr(option_name.length() + 1)
    return ""

func _run_e4a_pixel_test(base_payload: Dictionary, timeline: Dictionary, payload_sha: String, frame_records_sha: String, config_path: String) -> Dictionary:
    var config_bytes: PackedByteArray = FileAccess.get_file_as_bytes(config_path)
    if config_bytes.is_empty():
        return {"success": false, "error": "E4A pixel-test config is missing or empty."}
    var config_value: Variant = JSON.parse_string(config_bytes.get_string_from_utf8())
    if not (config_value is Dictionary):
        return {"success": false, "error": "E4A pixel-test config must be a JSON object."}
    var config: Dictionary = config_value
    var config_schema: String = str(config.get("schema", ""))
    var real_background_mode: bool = config_schema == E4ADCompositorConfigSchema
    if config_schema != "C11E-E4A-CHALLENGE-PIXEL-TEST-CONFIG-V1" and not real_background_mode:
        return {"success": false, "error": "Unsupported E4A pixel-test config schema."}

    var approval_bytes: PackedByteArray = FileAccess.get_file_as_bytes(E4AApprovalPath)
    if approval_bytes.is_empty() or _sha256_bytes(approval_bytes) != E4AApprovalSha:
        return {"success": false, "error": "Approved E4A policy hash mismatch."}
    var approval_value: Variant = JSON.parse_string(approval_bytes.get_string_from_utf8())
    if not (approval_value is Dictionary):
        return {"success": false, "error": "Approved E4A policy is invalid JSON."}
    var approval: Dictionary = approval_value
    if str(approval.get("schema", "")) != "C11E-E4A-CHALLENGE-EDITORIAL-PRESENTATION-POLICY-APPROVAL-V1":
        return {"success": false, "error": "Approved E4A policy schema mismatch."}
    if str(approval.get("status", "")) != "APPROVED_BY_OPERATOR_FOR_CHALLENGE_SEMANTIC_MAPPING":
        return {"success": false, "error": "E4A policy is not operator-approved."}
    if str(approval.get("render_test_authorization", {}).get("isolated_e4a_test_rendering", "")) != "AUTHORIZED_BY_OPERATOR_CURRENT_INSTRUCTION":
        return {"success": false, "error": "Isolated E4A rendering authorization is absent."}
    if str(approval.get("render_test_authorization", {}).get("production_renderer", "")) != "NOT_AUTHORIZED" or str(approval.get("render_test_authorization", {}).get("production_dispatch", "")) != "NOT_AUTHORIZED":
        return {"success": false, "error": "Policy unexpectedly authorizes production renderer/dispatch."}

    var supporting_pins: Dictionary = {
        D11MappingPath: D11MappingSha,
        D17MappingPath: D17MappingSha,
        E4AProposalPath: E4AProposalSha
    }
    for supporting_path: String in supporting_pins.keys():
        var supporting_bytes: PackedByteArray = FileAccess.get_file_as_bytes(supporting_path)
        if supporting_bytes.is_empty() or _sha256_bytes(supporting_bytes) != str(supporting_pins[supporting_path]):
            return {"success": false, "error": "E4A source policy/precedent pin mismatch: %s" % supporting_path}

    var layout_bytes: PackedByteArray = FileAccess.get_file_as_bytes(D15LayoutPath)
    if layout_bytes.is_empty() or _sha256_bytes(layout_bytes) != D15LayoutSha:
        return {"success": false, "error": "D1.5 layout contract hash mismatch."}
    var layout_text: String = layout_bytes.get_string_from_utf8()
    if not layout_text.contains("Logical width: 540") or not layout_text.contains("Logical height: 960"):
        return {"success": false, "error": "D1.5 logical frame dimensions are not the reviewed 540x960 contract."}
    if not layout_text.contains("Rect2(0, 0, 540, 144)") or not layout_text.contains("Rect2(0, 144, 540, 672)") or not layout_text.contains("Rect2(0, 816, 540, 144)"):
        return {"success": false, "error": "D1.5 canonical region rectangles do not match the approved layout contract."}
    var header_rect := Rect2(0, 0, 540, 144)
    var body_rect := Rect2(0, 144, 540, 672)
    var footer_rect := Rect2(0, 816, 540, 144)

    var variants_value: Variant = config.get("variants", null)
    if not (variants_value is Array) or variants_value.size() != 3:
        return {"success": false, "error": "E4A pixel test requires exactly three canonical E1 variants A/B/C."}
    var variants: Dictionary = {}
    for variant_value: Variant in variants_value:
        if not (variant_value is Dictionary):
            return {"success": false, "error": "E4A variant entry must be an object."}
        var variant: Dictionary = variant_value
        var variant_id: String = str(variant.get("id", ""))
        if not ["A", "B", "C"].has(variant_id) or variants.has(variant_id):
            return {"success": false, "error": "E4A variant id is invalid or duplicated."}
        var intent_value: Variant = variant.get("intent", null)
        if not (intent_value is Dictionary):
            return {"success": false, "error": "E4A variant is missing its shared E1 service intent."}
        var intent: Dictionary = intent_value
        if not _validate_e4a_intent(intent, variant_id):
            return {"success": false, "error": "E1 intent validation failed for variant %s." % variant_id}
        variants[variant_id] = intent
    if variants.size() != 3:
        return {"success": false, "error": "E4A A/B/C canonical intents are incomplete."}

    var intent_a: Dictionary = variants["A"]
    var intent_b: Dictionary = variants["B"]
    var intent_c: Dictionary = variants["C"]
    if intent_b.get("editorial", {}).get("title") != intent_c.get("editorial", {}).get("title") or intent_b.get("editorial", {}).get("subtitle") != intent_c.get("editorial", {}).get("subtitle") or intent_b.get("editorial", {}).get("call_to_action") != intent_c.get("editorial", {}).get("call_to_action"):
        return {"success": false, "error": "Variant C must preserve all three visual text fields from B."}
    if intent_b.get("editorial", {}).get("language") == intent_c.get("editorial", {}).get("language"):
        return {"success": false, "error": "Variant C must change only the metadata language relative to B's visual text."}
    if intent_b.get("editorial", {}).get("player_name") in ["", "UNKNOWN"] or intent_b.get("editorial", {}).get("challenge_label") in ["", "UNKNOWN"]:
        return {"success": false, "error": "Variant B must include Challenge-only fields to prove fail-closed geometry handling."}
    if intent_b.get("editorial", {}).get("title") in ["", "UNKNOWN"] or intent_b.get("editorial", {}).get("subtitle") in ["", "UNKNOWN"] or intent_b.get("editorial", {}).get("call_to_action") in ["", "UNKNOWN"]:
        return {"success": false, "error": "Variant B must contain non-empty text in HEADER and FOOTER."}
    if intent_b.get("editorial", {}).get("language") != "es" or intent_c.get("editorial", {}).get("language") != "en":
        return {"success": false, "error": "B/C language control values must be canonical es/en metadata."}
    if intent_c.get("editorial", {}).get("player_name") != "UNKNOWN" or intent_c.get("editorial", {}).get("challenge_label") != "UNKNOWN":
        return {"success": false, "error": "Variant C must omit Challenge overlay values while preserving other text."}
    if intent_a.get("editorial", {}).get("title") != "UNKNOWN" or intent_a.get("editorial", {}).get("subtitle") != "UNKNOWN" or intent_a.get("editorial", {}).get("call_to_action") != "UNKNOWN" or intent_a.get("editorial", {}).get("language") != "UNKNOWN" or intent_a.get("editorial", {}).get("player_name") != "UNKNOWN" or intent_a.get("editorial", {}).get("challenge_label") != "UNKNOWN":
        return {"success": false, "error": "Variant A must provide the canonical empty-value control for all six fields."}

    var adapter_contract: Dictionary = _validate_shared_editorial_adapter_contract(intent_b, intent_a, timeline)
    if not bool(adapter_contract.get("success", false)):
        return {"success": false, "error": "Shared editorial adapter contract failed: %s" % str(adapter_contract.get("error", "unknown"))}
    var challenge_source_value: Variant = JSON.parse_string(FileAccess.get_file_as_string(ChallengePath))
    if not (challenge_source_value is Dictionary):
        return {"success": false, "error": "Canonical Challenge source could not be re-read for its native hook content."}
    var native_hook_text: String = str(challenge_source_value.get("content", {}).get("hook", "")).strip_edges()
    if native_hook_text.is_empty():
        return {"success": false, "error": "Canonical Challenge hook text is empty; cannot recompose HEADER."}

    var output_dir: String = str(config.get("output_dir", "" )).replace("\\", "/").simplify_path()
    var project_root: String = ProjectSettings.globalize_path("res://").replace("\\", "/").trim_suffix("/")
    var output_suffix: String = "artifacts/tests/c11e/e4a_d_compositor_pixel_review/" if real_background_mode else "artifacts/tests/c11e/e4a_pixel_review/"
    var allowed_prefix: String = (project_root + "/" + output_suffix).to_lower()
    if output_dir.is_empty() or not output_dir.to_lower().begins_with(allowed_prefix):
        return {"success": false, "error": "E4A pixel evidence output escaped its test-only artifacts root."}
    var mkdir_error: int = DirAccess.make_dir_recursive_absolute(output_dir)
    if mkdir_error != OK and mkdir_error != ERR_ALREADY_EXISTS:
        return {"success": false, "error": "Cannot create E4A pixel evidence folder: %d" % mkdir_error}

    var composition_by_variant: Dictionary = {}
    var intent_by_variant: Dictionary = {}
    for variant_id: String in ["A", "B", "C"]:
        var intent: Dictionary = variants[variant_id]
        intent_by_variant[variant_id] = intent
        var composition_result: Dictionary = _build_e4a_editorial_composition(intent.get("editorial", {}), timeline, approval, payload_sha, frame_records_sha, intent)
        if not bool(composition_result.get("success", false)):
            return {"success": false, "error": "Editorial composition %s: %s" % [variant_id, str(composition_result.get("error", "unknown"))]}
        var composed_payload: Dictionary = base_payload.duplicate(true)
        composed_payload["editorial_visual_composition"] = composition_result["composition"]
        composed_payload["editorial_visual_composition_sha256"] = composition_result["composition_sha256"]
        if str(composed_payload.get("animation", {}).get("frame_records_sha256", "")) != frame_records_sha or int(composed_payload.get("animation", {}).get("frame_records", []).size()) != 420:
            return {"success": false, "error": "Editorial composition mutated or detached the canonical 420-frame source payload."}
        if _contains_key(composed_payload, "custom_data") or _contains_key(composed_payload, "winning_frame") or _contains_key(composed_payload, "close_calls"):
            return {"success": false, "error": "Protected gameplay/custom_data field entered E4A editorial composition."}
        composition_by_variant[variant_id] = composition_result["composition"]

    var samples: Array[Dictionary] = []
    var backgrounds_by_label: Dictionary = {}
    if real_background_mode:
        var base_frames_value: Variant = config.get("base_frames", null)
        if not (base_frames_value is Array) or base_frames_value.size() != 6:
            return {"success": false, "error": "Real-body compositor mode requires exactly six extracted C11-C background frames."}
        var expected_sample_rows: Array[Dictionary] = [
            {"label": "hook_first", "phase": "HOOK", "delivery_frame": 0},
            {"label": "hook_last", "phase": "HOOK", "delivery_frame": 89},
            {"label": "game_first", "phase": "GAME", "delivery_frame": 90},
            {"label": "reveal_first", "phase": "REVEAL", "delivery_frame": 300},
            {"label": "cta_first", "phase": "CTA", "delivery_frame": 390},
            {"label": "cta_last", "phase": "CTA", "delivery_frame": 449}
        ]
        var base_prefix: String = (output_dir + "/base_frames/").to_lower()
        var source_fps: int = int(timeline.get("fps", 0))
        if source_fps != 60:
            return {"success": false, "error": "Pinned Challenge source timebase is not 60 FPS."}
        for expected_row: Dictionary in expected_sample_rows:
            var matched: Dictionary = {}
            var match_count: int = 0
            for base_frame_value: Variant in base_frames_value:
                if not (base_frame_value is Dictionary): continue
                var candidate: Dictionary = base_frame_value
                if str(candidate.get("label", "")) == str(expected_row["label"]):
                    matched = candidate
                    match_count += 1
            if match_count != 1:
                return {"success": false, "error": "Missing or duplicated real source sample: %s" % str(expected_row["label"])}
            var label: String = str(expected_row["label"])
            var phase: String = str(expected_row["phase"])
            var delivery_frame: int = int(expected_row["delivery_frame"])
            var source_frame: int = int(round(float(delivery_frame) * float(source_fps) / 30.0))
            if str(matched.get("phase", "")) != phase or int(matched.get("delivery_frame", -1)) != delivery_frame or int(matched.get("source_frame", -1)) != source_frame:
                return {"success": false, "error": "Real sample mapping mismatch for %s." % label}
            var phase_segment: Dictionary = _phase_segment(timeline, phase)
            if phase_segment.is_empty() or source_frame < int(phase_segment["start_frame"]) or source_frame >= int(phase_segment["end_frame"]):
                return {"success": false, "error": "Real sample falls outside its canonical source-time phase: %s" % label}
            var background_path: String = str(matched.get("path", "")).replace("\\", "/").simplify_path()
            if background_path.is_empty() or not background_path.to_lower().begins_with(base_prefix):
                return {"success": false, "error": "Real source frame escaped the run's base_frames directory: %s" % label}
            var background_bytes: PackedByteArray = FileAccess.get_file_as_bytes(background_path)
            if background_bytes.is_empty() or _sha256_bytes(background_bytes) != str(matched.get("sha256", "")):
                return {"success": false, "error": "Real source frame SHA-256 mismatch: %s" % label}
            var background_image := Image.new()
            if background_image.load(background_path) != OK or background_image.get_width() != 720 or background_image.get_height() != 1280:
                return {"success": false, "error": "Real source frame must decode as 720x1280 PNG: %s" % label}
            backgrounds_by_label[label] = {"path": background_path, "sha256": _sha256_bytes(background_bytes), "delivery_frame": delivery_frame, "source_frame": source_frame}
            samples.append({"label": label, "phase": phase, "source_frame": source_frame, "delivery_frame": delivery_frame, "background_sha256": _sha256_bytes(background_bytes)})
    else:
        for sample_spec: Dictionary in [
            {"label": "hook_first", "phase": "HOOK", "edge": "FIRST"},
            {"label": "hook_last", "phase": "HOOK", "edge": "LAST"},
            {"label": "game_first", "phase": "GAME", "edge": "FIRST"},
            {"label": "reveal_first", "phase": "REVEAL", "edge": "FIRST"},
            {"label": "cta_first", "phase": "CTA", "edge": "FIRST"},
            {"label": "cta_last", "phase": "CTA", "edge": "LAST"}
        ]:
            var phase_segment: Dictionary = _phase_segment(timeline, str(sample_spec["phase"]))
            if phase_segment.is_empty():
                return {"success": false, "error": "Cannot resolve source phase for pixel fixture: %s" % str(sample_spec["phase"])}
            var sample_frame: int = int(phase_segment["start_frame"])
            if str(sample_spec["edge"]) == "LAST": sample_frame = int(phase_segment["end_frame"]) - 1
            samples.append({"label": str(sample_spec["label"]), "phase": str(sample_spec["phase"]), "source_frame": sample_frame})

    var pixel_header_rect: Rect2 = Rect2(0, 0, 720, 192) if real_background_mode else header_rect
    var pixel_body_rect: Rect2 = Rect2(0, 192, 720, 896) if real_background_mode else body_rect
    var pixel_footer_rect: Rect2 = Rect2(0, 1088, 720, 192) if real_background_mode else footer_rect
    var image_paths: Dictionary = {"A": {}, "B": {}, "C": {}}
    var header_layout_by_variant: Dictionary = {"A": {}, "B": {}, "C": {}}
    for variant_id: String in ["A", "B", "C"]:
        var composition: Dictionary = composition_by_variant[variant_id]
        for sample: Dictionary in samples:
            var label: String = str(sample["label"])
            var image_path: String = output_dir.path_join("%s_%s.png" % [variant_id, label])
            var background_path: String = str(backgrounds_by_label.get(label, {}).get("path", "")) if real_background_mode else ""
            var show_hook_countdown: bool = bool(composition.get("presentation_options", {}).get("show_hook_countdown", true))
            print("E4A3_VIEWPORT_BEGIN=%s/%s" % [variant_id, label])
            var render_result: Dictionary = await _render_e4a_pixel_surface(composition.get("fields", []), int(sample["source_frame"]), int(timeline.get("total_frames", 0)), pixel_header_rect, pixel_body_rect, pixel_footer_rect, image_path, background_path, native_hook_text, show_hook_countdown)
            if not bool(render_result.get("success", false)):
                return {"success": false, "error": "Pixel render %s/%s: %s" % [variant_id, label, str(render_result.get("error", "unknown"))]}
            image_paths[variant_id][label] = image_path
            if bool(render_result.get("header_layout", {}).get("header_active", false)):
                header_layout_by_variant[variant_id][label] = render_result.get("header_layout", {})
            print("E4A3_VIEWPORT_DONE=%s/%s" % [variant_id, label])

    var comparisons: Array[Dictionary] = []
    for label: String in ["hook_first", "hook_last"]:
        var comparison: Dictionary = _compare_e4a_images(image_paths["A"][label], image_paths["B"][label], pixel_header_rect)
        comparison["comparison"] = "A_TO_B_%s_HEADER_ONLY" % label.to_upper()
        if int(comparison.get("changed_pixels", 0)) <= 0 or int(comparison.get("changed_pixels_outside_region", -1)) != 0:
            return {"success": false, "error": "A/B header pixel comparison escaped HEADER or showed no visible title/subtitle change: %s" % label}
        comparisons.append(comparison)
    for label: String in ["game_first", "reveal_first"]:
        var comparison: Dictionary = _compare_e4a_images(image_paths["A"][label], image_paths["B"][label], Rect2())
        comparison["comparison"] = "A_TO_B_%s_PIXEL_IDENTICAL" % label.to_upper()
        if int(comparison.get("changed_pixels", -1)) != 0:
            return {"success": false, "error": "Header/CTA text leaked outside approved source-timebase windows: %s" % label}
        comparisons.append(comparison)
    for label: String in ["cta_first", "cta_last"]:
        var comparison: Dictionary = _compare_e4a_images(image_paths["A"][label], image_paths["B"][label], pixel_footer_rect)
        comparison["comparison"] = "A_TO_B_%s_FOOTER_ONLY" % label.to_upper()
        if int(comparison.get("changed_pixels", 0)) <= 0 or int(comparison.get("changed_pixels_outside_region", -1)) != 0:
            return {"success": false, "error": "A/B CTA pixel comparison escaped FOOTER or showed no visible CTA change: %s" % label}
        comparisons.append(comparison)
    for label: String in ["hook_first", "hook_last", "game_first", "reveal_first", "cta_first", "cta_last"]:
        var comparison: Dictionary = _compare_e4a_images(image_paths["B"][label], image_paths["C"][label], Rect2())
        comparison["comparison"] = "B_TO_C_%s_METADATA_AND_BLOCKED_FIELDS_NO_PIXELS" % label.to_upper()
        if int(comparison.get("changed_pixels", -1)) != 0:
            return {"success": false, "error": "Metadata-only language or unresolved Challenge overlay changed pixels: %s" % label}
        comparisons.append(comparison)

    var lineage := [
        {"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": FrozenManifestSha},
        {"path": "challenges/CHALLENGE_004.json", "sha256": ChallengeSha},
        {"path": "definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json", "sha256": E4AApprovalSha},
        {"path": "docs/current/d/D1.1_CHALLENGE_VISUAL_EDITORIAL_MAPPING_V1.0.md", "sha256": D11MappingSha},
        {"path": "docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md", "sha256": D15LayoutSha},
        {"path": "docs/current/d/D1.7_CHALLENGE_VISUAL_EDITORIAL_DECLARATIVE_MAPPING.md", "sha256": D17MappingSha},
        {"path": "docs/history/c11d/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_PROPOSAL_20261103_V1.md", "sha256": E4AProposalSha},
        {"path": "tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd", "sha256": _sha256_bytes(FileAccess.get_file_as_bytes("res://tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd"))},
        {"path": "tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd", "sha256": ChallengeEditorialAdapterSha},
        {"path": "tools/c11d/d9/c11e_e4a_challenge_pixel_review.py", "sha256": _sha256_bytes(FileAccess.get_file_as_bytes("res://tools/c11d/d9/c11e_e4a_challenge_pixel_review.py"))}
    ]
    var report: Dictionary = {
        "schema": E4ADCompositorReportSchema if real_background_mode else E4APixelReportSchema,
        "schema_version": "1.0",
        "status": "PASS_ISOLATED_D_OWNED_GODOT_LAYER_REAL_BODY_PIXEL_PROOF_TEST_ONLY" if real_background_mode else "PASS_ISOLATED_EDITORIAL_PIXEL_PROOF_TEST_ONLY",
        "scope": "CHALLENGE_004_D_OWNED_GODOT_SUBVIEWPORT_LAYER_ALPHA_COMPOSITED_OVER_REAL_C11C_REVIEW_FRAMES" if real_background_mode else "CHALLENGE_004_FIXED_FIXTURE_SOURCE_TIMEBASE_OFFSCREEN_SUBVIEWPORT",
        "frozen_c11c_manifest_sha256": FrozenManifestSha,
        "challenge_source_sha256": ChallengeSha,
        "base_payload_sha256": payload_sha,
        "game_frame_records_sha256": frame_records_sha,
        "game_frame_record_count": 420,
        "source_timeline": timeline,
        "logical_canvas": {"width": 540, "height": 960, "coordinate_space": "D1.5_LOGICAL_FRAME"},
        "delivery_canvas": {"width": 720, "height": 1280, "scale_from_logical": "4/3", "mode": "TEST_ONLY_ALPHA_COMPOSITE" if real_background_mode else "LOGICAL_FIXTURE"},
        "regions": {
            "HEADER": {"x": 0, "y": 0, "width": 720 if real_background_mode else 540, "height": 192 if real_background_mode else 144},
            "BODY": {"x": 0, "y": 192 if real_background_mode else 144, "width": 720 if real_background_mode else 540, "height": 896 if real_background_mode else 672},
            "FOOTER": {"x": 0, "y": 1088 if real_background_mode else 816, "width": 720 if real_background_mode else 540, "height": 192 if real_background_mode else 144}
        },
        "layout_fixture": "C11C_SHARED_EDITORIAL_LAYER_LOGICAL_540X960_SCALED_4_3; OPAQUE_HEADER_RECOMPOSES_NATIVE_CHALLENGE_HOOK_PLUS_OPTIONAL_TITLE_SUBTITLE; FOOTER_BACKDROP_REPLACES_NATIVE_CTA_WHEN_D_CTA_ACTIVE; VISUAL_PLACEMENT_UNAPPROVED",
        "rendered_scene": "C11E_D_ADAPTER_TO_C11C_VISUAL_EDITORIAL_LAYER_OVER_REAL_C11C_FRAME_TEST_ONLY" if real_background_mode else "C11E_D_ADAPTER_TO_C11C_VISUAL_EDITORIAL_LAYER_FIXTURE_ONLY",
        "base_frame_inputs": backgrounds_by_label if real_background_mode else {},
        "variants": {
            "A": {"request_id": intent_a.get("request", {}).get("request_id", ""), "request_hash": intent_a.get("identity", {}).get("request_hash", ""), "editorial_hash": intent_a.get("identity", {}).get("editorial_hash", ""), "composition_sha256": _sha256_text(JSON.stringify(_stable_value(composition_by_variant["A"])))} ,
            "B": {"request_id": intent_b.get("request", {}).get("request_id", ""), "request_hash": intent_b.get("identity", {}).get("request_hash", ""), "editorial_hash": intent_b.get("identity", {}).get("editorial_hash", ""), "composition_sha256": _sha256_text(JSON.stringify(_stable_value(composition_by_variant["B"])))} ,
            "C": {"request_id": intent_c.get("request", {}).get("request_id", ""), "request_hash": intent_c.get("identity", {}).get("request_hash", ""), "editorial_hash": intent_c.get("identity", {}).get("editorial_hash", ""), "composition_sha256": _sha256_text(JSON.stringify(_stable_value(composition_by_variant["C"])))}
        },
        "field_dispositions": composition_by_variant["B"].get("fields", []),
        "shared_visual_consumer": {"adapter": "C11EChallengeEditorialPresentationAdapter", "layer": "C11CVisualEditorialLayer.apply_render_model", "header_native_hook_recomposed_once": true, "header_native_hook_owner": "D_C11C_SHARED_HEADER_WHEN_EDITORIAL_ACTIVE", "footer_native_cta_owner": "D_C11C_SHARED_FOOTER_WHEN_EDITORIAL_CTA_PRESENT", "hook_countdown_option_off": "MODEL_ONLY_NOT_ERASURE_OF_BAKED_C11C_BASE_FRAME_PIXELS", "option_contract_probe": adapter_contract},
        "header_layout_diagnostics": header_layout_by_variant,
        "pixel_comparisons": comparisons,
        "pixel_artifacts": [],
        "invariants": {
            "source_payload_unchanged": true,
            "source_game_frame_records_unchanged": true,
            "simulation_truth_mutation": false,
            "winning_frame_sampling_used": false,
            "close_calls_used": false,
            "frame_snapshot_custom_data_serialized": false,
            "language_pixel_effect": false,
            "challenge_overlay_pixel_effect": false,
            "fixture_body_pixel_effect": false,
            "real_gameplay_body_rasterized": real_background_mode,
            "gameplay_body_pixel_identity": "PASS_AT_SIX_REAL_DELIVERY_SAMPLES" if real_background_mode else "NOT_TESTED_GAMEPLAY_NOT_RASTERIZED_IN_THIS_EDITORIAL_LAYER_FIXTURE",
            "delivery_resampling": "BASE_VIDEO_ALREADY_NORMALIZED_TEST_ONLY_30FPS" if real_background_mode else "NOT_APPLIED",
            "production_audio_or_music": false
        },
        "execution_boundary": {
            "mode": "ISOLATED_E4A_TEST_PIXEL_RENDERING_ONLY",
            "offscreen_subviewport_rendered": true,
            "test_pixel_artifacts_created": true,
            "production_renderer_activation": false,
            "production_dispatch_invoked": false,
            "production_media_created": false,
            "c11c_source_mutation": false,
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "d9_14": "BLOCKED",
            "d9_16": "BLOCKED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED_FOR_PROMOTION",
            "release_authority": "NONE"
        },
        "source_lineage": lineage
    }
    for variant_id: String in ["A", "B", "C"]:
        for sample: Dictionary in samples:
            var image_path: String = str(image_paths[variant_id][str(sample["label"])])
            var artifact: Dictionary = {"variant": variant_id, "sample": str(sample["label"]), "phase": str(sample["phase"]), "source_frame": int(sample["source_frame"]), "path": image_path.replace("\\", "/").trim_prefix(project_root + "/"), "sha256": _sha256_bytes(FileAccess.get_file_as_bytes(image_path)), "width": 720 if real_background_mode else 540, "height": 1280 if real_background_mode else 960}
            if real_background_mode:
                artifact["delivery_frame"] = int(sample.get("delivery_frame", -1))
                artifact["base_frame_sha256"] = str(sample.get("background_sha256", ""))
            report["pixel_artifacts"].append(artifact)
    if real_background_mode:
        report["test_only_visual_layout_disposition"] = {
            "pixel_region_confinement_proven": true,
            "d_owned_godot_layer_alpha_composited_over_real_c11c_gameplay": true,
            "visual_placement_approved": false,
            "d1_5_safe_area_and_generic_typography": "UNKNOWN",
            "existing_c11c_hook_content_overlap_observed": false,
            "native_challenge_hook_recomposed_into_shared_header": true,
            "header_three_line_fit_contract": "PASS_FOR_RENDERED_B_VARIANT_HOOK_SAMPLES",
            "header_layout_diagnostics": header_layout_by_variant.get("B", {}),
            "production_compositor_layout_acceptance": "NOT_GRANTED"
        }
        report["execution_boundary"] = {
            "mode": "ISOLATED_E4A_D_OWNED_GODOT_COMPOSITOR_TEST_ONLY",
            "offscreen_subviewport_rendered": true,
            "real_c11c_delivery_frames_used_as_background": true,
            "test_pixel_artifacts_created": true,
            "production_renderer_activation": false,
            "production_dispatch_invoked": false,
            "production_media_created": false,
            "c11c_source_mutation": false,
            "d4_8": "BLOCKED", "d9_10": "PREPARE_ONLY", "release_authority": "NONE"
        }
    var report_name: String = "C11E_E4A_D_COMPOSITOR_PIXEL_REPORT.json" if real_background_mode else "C11E_E4A_PIXEL_RENDER_REPORT.json"
    var report_path: String = output_dir.path_join(report_name)
    var report_file := FileAccess.open(report_path, FileAccess.WRITE)
    if report_file == null:
        return {"success": false, "error": "Cannot write E4A pixel report."}
    report_file.store_string(JSON.stringify(_stable_value(report), "\t", true) + "\n")
    report_file.close()
    return {"success": true, "report": report, "report_path": report_path}

func _validate_e4a_intent(intent: Dictionary, variant_id: String) -> bool:
    if str(intent.get("schema", "")) != "C11-E-PRODUCTION-INTENT-V1" or str(intent.get("status", "")) != "PREPARED_E1_NOT_DISPATCHED": return false
    if str(intent.get("service_version", "")) != "0.2.0-E3.2": return false
    var request: Dictionary = intent.get("request", {})
    var selection: Dictionary = request.get("selection", {})
    if str(request.get("content_type", "")) != "challenges" or str(selection.get("content_type", "")) != "challenges": return false
    if str(selection.get("variant_id", "")) != "CHALLENGE_004" or str(selection.get("family_id", "")) != "parking_v2": return false
    if str(intent.get("delivery", {}).get("resolved_profile_id", "")) != "REVIEW_720" or str(intent.get("delivery", {}).get("presentation_profile_id", "")) != "social_default_v1": return false
    if intent.get("delivery", {}).get("audio_enabled") != false: return false
    if int(intent.get("seed_domains", {}).get("gameplay", {}).get("value", -1)) != 314159 or int(intent.get("seed_domains", {}).get("music", {}).get("value", -1)) != 840001: return false
    if intent.get("seed_domains", {}).get("independent_domains") != true or intent.get("output", {}).get("created") != false: return false
    if str(request.get("mode", "")) != "REVIEW" or str(intent.get("request_origin", "")) != "TEST": return false
    var consumption_value: Variant = intent.get("editorial_field_consumption", null)
    if not (consumption_value is Dictionary): return false
    var consumption: Dictionary = consumption_value
    var consumption_keys: Array = consumption.keys()
    consumption_keys.sort()
    var expected_consumption_keys := ["call_to_action", "challenge_label", "language", "player_name", "subtitle", "title"]
    if consumption_keys != expected_consumption_keys: return false
    for field_name: Variant in consumption.keys():
        if str(consumption[field_name].get("consumer_status", "")) != "NOT_CONSUMED_E1": return false
    var boundary: Dictionary = intent.get("execution_boundary", {})
    if boundary.get("dispatch_authorized") != false or boundary.get("renderer_input_emitted") != false or boundary.get("renderer_dispatch_invoked") != false or boundary.get("renderer_activation") != false or boundary.get("production_execution") != false or boundary.get("media_created") != false or boundary.get("release_authority") != "NONE" or boundary.get("d4_8") != "BLOCKED": return false
    var presentation_options: Variant = request.get("presentation_options", null)
    if request.has("presentation_options"):
        if not (presentation_options is Dictionary) or presentation_options.size() != 1 or not presentation_options.has("show_hook_countdown") or typeof(presentation_options.get("show_hook_countdown")) != TYPE_BOOL:
            return false
    var editorial: Dictionary = intent.get("editorial", {})
    var expected_fields := ["title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"]
    var actual_fields: Array = editorial.keys()
    actual_fields.sort()
    expected_fields.sort()
    if actual_fields != expected_fields: return false
    var identity: Dictionary = intent.get("identity", {})
    for key: String in ["request_hash", "editorial_hash", "plan_hash", "intent_hash"]:
        if str(identity.get(key, "")).length() != 64: return false
    return true

func _validate_shared_editorial_adapter_contract(intent_on: Dictionary, empty_intent: Dictionary, timeline: Dictionary) -> Dictionary:
    var hook_content := {"hook": "NATIVE CHALLENGE HOOK", "ui_fps": 60, "ui_state_frame": 0, "absolute_frame": 0, "winning_frame": -1, "timeline": null}
    var native_hook_model: Dictionary = PresentationBinder.build_frame_render_model("HOOK", hook_content, null)
    var on_result: Dictionary = ChallengeEditorialAdapter.adapt_native_challenge_render_model(native_hook_model, intent_on)
    if not bool(on_result.get("success", false)):
        return {"success": false, "error": "Default/ON Challenge option was rejected."}
    if on_result.get("render_model", {}).get("show_hook") != true or on_result.get("render_model", {}).get("countdown_visible") != true:
        return {"success": false, "error": "Default/ON must preserve native C hook and countdown."}
    var off_intent := intent_on.duplicate(true)
    var off_request: Dictionary = off_intent.get("request", {}).duplicate(true)
    off_request["presentation_options"] = {"show_hook_countdown": false}
    off_intent["request"] = off_request
    var off_result: Dictionary = ChallengeEditorialAdapter.adapt_native_challenge_render_model(native_hook_model, off_intent)
    if not bool(off_result.get("success", false)):
        return {"success": false, "error": "Explicit OFF Challenge option was rejected."}
    var off_model: Dictionary = off_result.get("render_model", {})
    if off_model.get("show_hook") != false or off_model.get("countdown_visible") != false or off_model.get("countdown_value") != "":
        return {"success": false, "error": "Explicit OFF must suppress native hook/countdown model visibility."}
    if native_hook_model.get("show_hook") != true or native_hook_model.get("countdown_visible") != true:
        return {"success": false, "error": "Adapter mutated the C binder's input render model."}
    var legacy_result: Dictionary = ChallengeEditorialAdapter.resolve_hook_countdown_option(empty_intent)
    if not bool(legacy_result.get("success", false)) or legacy_result.get("show_hook_countdown") != true:
        return {"success": false, "error": "Legacy E1 Challenge intent must default ON."}

    var native_cta_model: Dictionary = PresentationBinder.build_frame_render_model("CTA", hook_content, null)
    var cta_owner_result: Dictionary = ChallengeEditorialAdapter.adapt_native_challenge_render_model(native_cta_model, intent_on, {"footer_active": true})
    if not bool(cta_owner_result.get("success", false)) or cta_owner_result.get("render_model", {}).get("cta_visible") != false or str(cta_owner_result.get("native_cta_owner", "")) != "D_C11C_SHARED_FOOTER":
        return {"success": false, "error": "D editorial CTA must become the single footer owner only when D CTA is active."}
    var native_cta_unchanged: Dictionary = ChallengeEditorialAdapter.adapt_native_challenge_render_model(native_cta_model, intent_on)
    if not bool(native_cta_unchanged.get("success", false)) or native_cta_unchanged.get("render_model", {}).get("cta_visible") != true or native_cta_model.get("cta_visible") != true:
        return {"success": false, "error": "Native Challenge CTA must remain owner when D CTA is empty."}

    var loop_intent := intent_on.duplicate(true)
    var loop_request: Dictionary = loop_intent.get("request", {}).duplicate(true)
    loop_request["content_type"] = "visual_loops"
    loop_intent["request"] = loop_request
    if bool(ChallengeEditorialAdapter.resolve_hook_countdown_option(loop_intent).get("success", true)):
        return {"success": false, "error": "Challenge-only option leaked into Loop."}

    var hook_segment: Dictionary = _phase_segment(timeline, "HOOK")
    var cta_segment: Dictionary = _phase_segment(timeline, "CTA")
    if hook_segment.is_empty() or cta_segment.is_empty():
        return {"success": false, "error": "Cannot resolve source phase windows for editorial arrangement probes."}
    var hook_frame: int = int(hook_segment.get("start_frame", -1))
    var cta_frame: int = int(cta_segment.get("start_frame", -1))
    var total_frames: int = int(timeline.get("total_frames", 0))

    var empty_rows: Array[Dictionary] = _build_adapter_probe_fields("", "", "", timeline)
    var empty_probe: Dictionary = ChallengeEditorialAdapter.build_shared_editorial_model(empty_rows, hook_frame, total_frames)
    if not bool(empty_probe.get("success", false)) or bool(empty_probe.get("header_active", true)) or bool(empty_probe.get("footer_active", true)):
        return {"success": false, "error": "All-empty editorial arrangement must produce no visible regions."}

    var title_rows: Array[Dictionary] = _build_adapter_probe_fields("TITLE ONLY", "", "", timeline)
    var title_probe: Dictionary = ChallengeEditorialAdapter.build_shared_editorial_model(title_rows, hook_frame, total_frames, 314159, "NATIVE CHALLENGE HOOK", true)
    if not bool(title_probe.get("success", false)) or not bool(title_probe.get("header_active", false)) or bool(title_probe.get("footer_active", true)):
        return {"success": false, "error": "Title-only editorial arrangement did not isolate HEADER."}
    if not bool(title_probe.get("header_native_hook_migrated", false)) or bool(title_probe.get("native_hook_overlap", true)):
        return {"success": false, "error": "Title-only arrangement did not recompose native HOOK exactly once."}
    if str(title_probe.get("render_model", {}).get("editorial", {}).get("header", {}).get("line_1", "")) != "NATIVE CHALLENGE HOOK":
        return {"success": false, "error": "Native Challenge hook is not the primary C11C shared-header line."}

    var subtitle_rows: Array[Dictionary] = _build_adapter_probe_fields("", "SUBTITLE ONLY", "", timeline)
    var subtitle_probe: Dictionary = ChallengeEditorialAdapter.build_shared_editorial_model(subtitle_rows, hook_frame, total_frames, 314159, "NATIVE CHALLENGE HOOK", true)
    if not bool(subtitle_probe.get("success", false)) or not bool(subtitle_probe.get("header_active", false)) or bool(subtitle_probe.get("footer_active", true)):
        return {"success": false, "error": "Subtitle-only editorial arrangement did not isolate HEADER."}

    var combined_rows: Array[Dictionary] = _build_adapter_probe_fields("TITLE + HOOK", "SUBTITLE", "", timeline)
    var combined_probe: Dictionary = ChallengeEditorialAdapter.build_shared_editorial_model(combined_rows, hook_frame, total_frames, 314159, "NATIVE CHALLENGE HOOK", true)
    if not bool(combined_probe.get("success", false)) or not bool(combined_probe.get("header_native_hook_migrated", false)):
        return {"success": false, "error": "Combined title/subtitle did not migrate the native hook into the shared header."}
    var combined_header: Dictionary = combined_probe.get("render_model", {}).get("editorial", {}).get("header", {})
    if str(combined_header.get("line_1", "")) != "NATIVE CHALLENGE HOOK" or str(combined_header.get("line_2", "")) != "TITLE + HOOK · SUBTITLE":
        return {"success": false, "error": "Three-line header content order is not hook/title/subtitle."}
    var combined_adapted: Dictionary = ChallengeEditorialAdapter.adapt_native_challenge_render_model(native_hook_model, intent_on, combined_probe)
    if not bool(combined_adapted.get("success", false)) or combined_adapted.get("render_model", {}).get("show_hook") != false or combined_adapted.get("render_model", {}).get("countdown_visible") != true:
        return {"success": false, "error": "Hook must be migrated once while the body countdown remains visible when ON."}
    var off_shared_probe: Dictionary = ChallengeEditorialAdapter.build_shared_editorial_model(combined_rows, hook_frame, total_frames, 314159, "NATIVE CHALLENGE HOOK", false)
    if not bool(off_shared_probe.get("success", false)) or bool(off_shared_probe.get("header_native_hook_migrated", true)):
        return {"success": false, "error": "Explicit OFF must omit native hook from the shared header."}
    var off_shared_header: Dictionary = off_shared_probe.get("render_model", {}).get("editorial", {}).get("header", {})
    if str(off_shared_header.get("line_1", "")) != "TITLE + HOOK" or str(off_shared_header.get("line_2", "")) != "SUBTITLE":
        return {"success": false, "error": "Explicit OFF must retain editorial title/subtitle without native hook."}

    var cta_rows: Array[Dictionary] = _build_adapter_probe_fields("", "", "CTA ONLY", timeline)
    var cta_probe: Dictionary = ChallengeEditorialAdapter.build_shared_editorial_model(cta_rows, cta_frame, total_frames)
    if not bool(cta_probe.get("success", false)) or bool(cta_probe.get("header_active", true)) or not bool(cta_probe.get("footer_active", false)):
        return {"success": false, "error": "CTA-only editorial arrangement did not isolate FOOTER."}

    var blocked_rows: Array[Dictionary] = _build_adapter_probe_fields("", "", "", timeline)
    for row_index in range(blocked_rows.size()):
        if str(blocked_rows[row_index].get("field", "")) == "player_name":
            blocked_rows[row_index]["disposition"] = "READY_FOR_ISOLATED_TEST_PIXEL_DRAW"
            blocked_rows[row_index]["effective_value"] = "BLOCKED PLAYER"
            blocked_rows[row_index]["source_frame_ranges"] = [{"start_frame": hook_frame, "end_frame": int(hook_segment.get("end_frame", 0))}]
    var blocked_probe: Dictionary = ChallengeEditorialAdapter.build_shared_editorial_model(blocked_rows, hook_frame, total_frames)
    if bool(blocked_probe.get("success", true)):
        return {"success": false, "error": "CHALLENGE_OVERLAY player_name escaped its unresolved geometry block."}

    return {"success": true, "cases": {"challenge_default_on": true, "challenge_explicit_off": true, "legacy_intent_default_on": true, "loop_rejected": true, "c_render_model_immutable": true, "single_cta_owner_when_populated": true, "native_cta_owner_when_d_empty": true, "empty_fields_omitted": true, "title_only_header": true, "subtitle_only_header": true, "hook_title_subtitle_single_shared_header": true, "hook_countdown_on_preserves_countdown_only": true, "hook_countdown_off_omits_hook_from_shared_header": true, "cta_only_footer": true, "challenge_overlay_blocked": true}}

func _build_adapter_probe_fields(title_value: String, subtitle_value: String, cta_value: String, timeline: Dictionary) -> Array[Dictionary]:
    var hook_segment: Dictionary = _phase_segment(timeline, "HOOK")
    var cta_segment: Dictionary = _phase_segment(timeline, "CTA")
    var rows: Array[Dictionary] = []
    var title_disposition: String = "OMITTED_EMPTY" if title_value.strip_edges().is_empty() else "READY_FOR_ISOLATED_TEST_PIXEL_DRAW"
    var subtitle_disposition: String = "OMITTED_EMPTY" if subtitle_value.strip_edges().is_empty() else "READY_FOR_ISOLATED_TEST_PIXEL_DRAW"
    var cta_disposition: String = "OMITTED_EMPTY" if cta_value.strip_edges().is_empty() else "READY_FOR_ISOLATED_TEST_PIXEL_DRAW"
    rows.append({"field": "title", "region": "HEADER", "disposition": title_disposition, "effective_value": title_value, "source_frame_ranges": [{"start_frame": int(hook_segment.get("start_frame", 0)), "end_frame": int(hook_segment.get("end_frame", 0))}]})
    rows.append({"field": "subtitle", "region": "HEADER", "disposition": subtitle_disposition, "effective_value": subtitle_value, "source_frame_ranges": [{"start_frame": int(hook_segment.get("start_frame", 0)), "end_frame": int(hook_segment.get("end_frame", 0))}]})
    rows.append({"field": "player_name", "region": "CHALLENGE_OVERLAY", "disposition": "BLOCKED_GEOMETRY_UNRESOLVED", "effective_value": "", "source_frame_ranges": []})
    rows.append({"field": "challenge_label", "region": "CHALLENGE_OVERLAY", "disposition": "BLOCKED_GEOMETRY_UNRESOLVED", "effective_value": "", "source_frame_ranges": []})
    rows.append({"field": "call_to_action", "region": "FOOTER", "disposition": cta_disposition, "effective_value": cta_value, "source_frame_ranges": [{"start_frame": int(cta_segment.get("start_frame", 0)), "end_frame": int(cta_segment.get("end_frame", 0))}]})
    rows.append({"field": "language", "region": "METADATA", "disposition": "METADATA_ONLY", "effective_value": "es", "source_frame_ranges": []})
    return rows

func _build_e4a_editorial_composition(editorial: Dictionary, timeline: Dictionary, approval: Dictionary, payload_sha: String, frame_records_sha: String, intent: Dictionary) -> Dictionary:
    var expected_fields := ["title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"]
    var actual_fields: Array = editorial.keys()
    actual_fields.sort()
    expected_fields.sort()
    if actual_fields != expected_fields:
        return {"success": false, "error": "D9.9 effective editorial field allowlist mismatch."}
    var policy_fields_value: Variant = approval.get("fields", null)
    if not (policy_fields_value is Array) or policy_fields_value.size() != 6:
        return {"success": false, "error": "Approved policy field matrix must contain six entries."}
    var field_rows: Array[Dictionary] = []
    var seen: Dictionary = {}
    for row_value: Variant in policy_fields_value:
        if not (row_value is Dictionary): return {"success": false, "error": "Malformed approved policy field row."}
        var row: Dictionary = row_value
        var field: String = str(row.get("field", ""))
        if not expected_fields.has(field) or seen.has(field): return {"success": false, "error": "Unknown or duplicate policy field: %s" % field}
        seen[field] = true
        var value: String = str(editorial.get(field, "UNKNOWN"))
        var clean_value: String = value.strip_edges()
        var windows_value: Variant = row.get("source_phase_windows", [])
        if not (windows_value is Array): return {"success": false, "error": "Phase-window policy must be an array for %s." % field}
        var windows: Array = windows_value
        var frame_ranges: Array[Dictionary] = []
        for phase_value: Variant in windows:
            var segment: Dictionary = _phase_segment(timeline, str(phase_value))
            if segment.is_empty(): return {"success": false, "error": "Approved phase missing from source timeline: %s/%s" % [field, str(phase_value)]}
            frame_ranges.append({"phase": str(phase_value), "start_frame": int(segment["start_frame"]), "end_frame": int(segment["end_frame"]), "timebase": "SOURCE_60FPS_HALF_OPEN"})
        var kind: String = str(row.get("kind", ""))
        var region: String = str(row.get("region", ""))
        var disposition: String = ""
        var region_rect: Dictionary = {}
        if clean_value.is_empty() or clean_value == "UNKNOWN":
            disposition = "OMITTED_EMPTY"
        elif kind == "metadata_only":
            disposition = "METADATA_ONLY"
        elif region == "CHALLENGE_OVERLAY":
            disposition = "BLOCKED_GEOMETRY_UNRESOLVED"
        elif region == "HEADER":
            disposition = "READY_FOR_ISOLATED_TEST_PIXEL_DRAW"
            region_rect = {"x": 0, "y": 0, "width": 540, "height": 144}
        elif region == "FOOTER":
            disposition = "READY_FOR_ISOLATED_TEST_PIXEL_DRAW"
            region_rect = {"x": 0, "y": 816, "width": 540, "height": 144}
        else:
            return {"success": false, "error": "Unsupported or unresolved semantic region: %s" % region}
        field_rows.append({
            "field": field,
            "kind": kind,
            "region": region,
            "effective_value": clean_value if disposition != "OMITTED_EMPTY" else "",
            "value_sha256": _sha256_text(clean_value),
            "source_phase_windows": windows,
            "source_frame_ranges": frame_ranges,
            "region_rect": region_rect,
            "disposition": disposition,
            "policy_sha256": E4AApprovalSha,
            "layout_contract_sha256": D15LayoutSha
        })
    if seen.size() != 6:
        return {"success": false, "error": "Approved policy does not cover all six Challenge fields."}
    var option_result: Dictionary = ChallengeEditorialAdapter.resolve_hook_countdown_option(intent)
    if not bool(option_result.get("success", false)):
        return {"success": false, "error": str(option_result.get("error", "E1 Challenge visibility option failed."))}
    var composition: Dictionary = {
        "schema": "C11E-E4A-CHALLENGE-EDITORIAL-VISUAL-COMPOSITION-V1",
        "status": "IN_MEMORY_D_ONLY_COMPOSITION_FOR_ISOLATED_PIXEL_TEST",
        "payload_sha256": payload_sha,
        "game_frame_records_sha256": frame_records_sha,
        "challenge_id": "CHALLENGE_004",
        "presentation_profile_id": "social_default_v1",
        "source_fps": int(timeline.get("fps", 0)),
        "source_total_frames": int(timeline.get("total_frames", 0)),
        "fields": field_rows,
        "presentation_options": {"show_hook_countdown": bool(option_result.get("show_hook_countdown", true)), "source": str(option_result.get("source", ""))},
        "native_content_policy": "C11C_HOOK_COUNTDOWN_RETAINED_WHEN_ON; OFF_APPLIES_TO_LIVE_RENDER_MODEL_ONLY_NOT_BAKED_BASE_FRAME_PIXELS",
        "policy_sha256": E4AApprovalSha,
        "layout_contract_sha256": D15LayoutSha,
        "delivery_resampling": "NOT_APPLIED",
        "renderer_input_emitted": false,
        "production_dispatch": false,
        "release_authority": "NONE"
    }
    return {"success": true, "composition": composition, "composition_sha256": _sha256_text(JSON.stringify(_stable_value(composition)))}

func _phase_segment(timeline: Dictionary, phase_name: String) -> Dictionary:
    var segments: Variant = timeline.get("phase_segments", [])
    if not (segments is Array): return {}
    var found: Dictionary = {}
    var matches: int = 0
    for segment_value: Variant in segments:
        if not (segment_value is Dictionary): continue
        var segment: Dictionary = segment_value
        if str(segment.get("phase", "")) == phase_name:
            matches += 1
            found = segment
    if matches != 1: return {}
    var start_frame: int = int(found.get("start_frame", -1))
    var end_frame: int = int(found.get("end_frame", -1))
    if start_frame < 0 or end_frame <= start_frame or end_frame > int(timeline.get("total_frames", 0)): return {}
    return found

func _render_e4a_pixel_surface(fields: Array, source_frame: int, source_frame_count: int, header_rect: Rect2, body_rect: Rect2, footer_rect: Rect2, output_path: String, base_background_path: String = "", native_hook_text: String = "", show_hook_countdown: bool = true) -> Dictionary:
    var real_background_mode: bool = not base_background_path.is_empty()
    var target_size: Vector2i = Vector2i(720, 1280) if real_background_mode else Vector2i(540, 960)
    var shared_model_result: Dictionary = ChallengeEditorialAdapter.build_shared_editorial_model(fields, source_frame, source_frame_count, 314159, native_hook_text, show_hook_countdown)
    if not bool(shared_model_result.get("success", false)):
        return {"success": false, "error": "D editorial adapter rejected composition: %s" % str(shared_model_result.get("error", "unknown"))}

    var viewport := SubViewport.new()
    viewport.size = target_size
    viewport.disable_3d = true
    viewport.transparent_bg = real_background_mode
    viewport.render_target_clear_mode = SubViewport.CLEAR_MODE_ALWAYS
    viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
    get_root().add_child(viewport)

    var canvas := Control.new()
    canvas.position = Vector2.ZERO
    canvas.size = Vector2(target_size)
    canvas.clip_contents = true
    viewport.add_child(canvas)
    if not real_background_mode:
        var background := ColorRect.new()
        background.position = Vector2.ZERO
        background.size = Vector2(540, 960)
        background.color = Color(0.055, 0.070, 0.090, 1.0)
        canvas.add_child(background)
        var header_background := ColorRect.new()
        header_background.position = header_rect.position
        header_background.size = header_rect.size
        header_background.color = Color(0.10, 0.13, 0.17, 1.0)
        canvas.add_child(header_background)
        var body_background := ColorRect.new()
        body_background.position = body_rect.position
        body_background.size = body_rect.size
        body_background.color = Color(0.075, 0.095, 0.12, 1.0)
        canvas.add_child(body_background)
        var footer_background := ColorRect.new()
        footer_background.position = footer_rect.position
        footer_background.size = footer_rect.size
        footer_background.color = Color(0.10, 0.13, 0.17, 1.0)
        canvas.add_child(footer_background)

    var frame_scene := load("res://core/presentation/UnifiedSocialFrame.tscn") as PackedScene
    if frame_scene == null:
        viewport.queue_free()
        return {"success": false, "error": "Cannot load the canonical UnifiedSocialFrame scene."}
    var frame := frame_scene.instantiate() as UnifiedSocialFrame
    if frame == null:
        viewport.queue_free()
        return {"success": false, "error": "UnifiedSocialFrame scene did not instantiate."}
    frame.position = Vector2.ZERO
    frame.scale = Vector2(4.0 / 3.0, 4.0 / 3.0) if real_background_mode else Vector2.ONE
    canvas.add_child(frame)
    print("E4A_SHARED_LAYER_WAIT_FRAME_READY")
    await process_frame

    var shared_layer: RefCounted = C11CVisualEditorialLayerClass.new()
    var layer_result: Dictionary = ChallengeEditorialAdapter.apply_to_shared_layer(frame, shared_layer, shared_model_result)
    if not bool(layer_result.get("success", false)):
        viewport.queue_free()
        await process_frame
        return {"success": false, "error": str(layer_result.get("error", "C11C shared layer failed."))}
    var header_layout: Dictionary = ChallengeEditorialAdapter.get_header_layout_diagnostics(frame, shared_model_result)
    if not bool(header_layout.get("success", false)):
        viewport.queue_free()
        await process_frame
        return {"success": false, "error": str(header_layout.get("error", "C11C shared header did not satisfy its fit contract."))}

    print("E4A_SHARED_LAYER_WAIT_PROCESS_FRAME")
    await process_frame
    print("E4A_SHARED_LAYER_WAIT_FRAME_POST_DRAW")
    print("E4A3_VIEWPORT_WAIT_FRAME_POST_DRAW")
    await RenderingServer.frame_post_draw
    print("E4A_SHARED_LAYER_FRAME_POST_DRAW_OK")
    print("E4A3_VIEWPORT_FRAME_POST_DRAW_OK")
    var texture: Texture2D = viewport.get_texture()
    if texture == null:
        viewport.queue_free()
        await process_frame
        return {"success": false, "error": "Offscreen SubViewport returned no texture."}
    var image: Image = texture.get_image()
    if image == null or image.is_empty() or image.get_width() != target_size.x or image.get_height() != target_size.y:
        viewport.queue_free()
        await process_frame
        return {"success": false, "error": "C11C shared-layer image is empty or has the wrong dimensions."}

    var final_image: Image = image
    if real_background_mode:
        var base_image := Image.new()
        var base_load_error: int = base_image.load(base_background_path)
        if base_load_error != OK or base_image.is_empty() or base_image.get_width() != 720 or base_image.get_height() != 1280:
            viewport.queue_free()
            await process_frame
            return {"success": false, "error": "Cannot load the pinned 720x1280 real C11-C base frame: %s" % base_background_path}
        if base_image.get_format() != Image.FORMAT_RGBA8:
            base_image.convert(Image.FORMAT_RGBA8)
        if image.get_format() != Image.FORMAT_RGBA8:
            image.convert(Image.FORMAT_RGBA8)
        base_image.blend_rect(image, Rect2i(0, 0, 720, 1280), Vector2i.ZERO)
        final_image = base_image

    var save_error: int = final_image.save_png(output_path)
    viewport.queue_free()
    await process_frame
    if save_error != OK:
        return {"success": false, "error": "Cannot save shared-layer test PNG: %s (error %d)" % [output_path, save_error]}
    return {"success": true, "width": target_size.x, "height": target_size.y, "shared_consumer": "C11CVisualEditorialLayer", "d_adapter_schema": str(shared_model_result.get("schema", "")), "alpha_composited_over_real_background": real_background_mode, "native_cta_owner": str(shared_model_result.get("native_cta_owner", "")), "header_layout": header_layout, "visual_placement": "UNAPPROVED_TEST_ONLY"}

func _compare_e4a_images(path_a: String, path_b: String, allowed_rect: Rect2) -> Dictionary:
    var image_a := Image.new()
    var image_b := Image.new()
    if image_a.load(path_a) != OK or image_b.load(path_b) != OK:
        return {"success": false, "error": "Cannot reload pixel evidence images."}
    if image_a.get_width() != image_b.get_width() or image_a.get_height() != image_b.get_height():
        return {"success": false, "error": "Pixel evidence dimensions mismatch."}
    var image_width: int = image_a.get_width()
    var image_height: int = image_a.get_height()
    var changed: int = 0
    var inside: int = 0
    var outside: int = 0
    for y: int in range(image_height):
        for x: int in range(image_width):
            if image_a.get_pixel(x, y) != image_b.get_pixel(x, y):
                changed += 1
                if not allowed_rect.has_area() or not allowed_rect.has_point(Vector2(x + 0.5, y + 0.5)):
                    outside += 1
                else:
                    inside += 1
    return {"success": true, "width": image_width, "height": image_height, "changed_pixels": changed, "changed_pixels_inside_region": inside, "changed_pixels_outside_region": outside, "allowed_region": _stable_value(allowed_rect)}

func _build_payload(source: Dictionary, context: Variant) -> Dictionary:
    if context == null or context.simulation_result == null or context.timeline == null or context.presentation_binding == null:
        return {"success": false, "error": "Incomplete runtime context."}
    var sim: Variant = context.simulation_result
    var timeline_obj: Variant = context.timeline
    if str(sim.error_state) != "OK" or sim.frames.size() != 420 or int(timeline_obj.fps) != 60 or int(timeline_obj.total_frames) != 900:
        return {"success": false, "error": "Runtime timeline/simulation frame count mismatch."}
    var before_signature: String = _frame_signature_sha256(sim)
    if before_signature.is_empty():
        return {"success": false, "error": "Simulation frame signature is invalid."}
    var before_winning: int = int(sim.winning_frame)
    var before_score: float = float(sim.score)
    var before_distance: float = float(sim.minimum_distance)
    var before_tolerance: float = float(sim.tolerance_threshold)

    var canonical: Dictionary = context.canonical_v2.duplicate(true)
    var d_presentation: Dictionary = canonical.get("presentation", {}).duplicate(true)
    d_presentation["profile_id"] = "social_default_v1"
    canonical["presentation"] = d_presentation
    var d_binding: Variant = PresentationBinder.bind(canonical, timeline_obj, sim)
    if d_binding == null or not bool(d_binding.success) or d_binding.presentation_profile == null:
        return {"success": false, "error": "D presentation binding failed: %s" % str(d_binding.error if d_binding != null else "null binding")}
    if str(d_binding.presentation_profile.profile_id) != "social_default_v1":
        return {"success": false, "error": "D presentation profile identity mismatch."}

    var render_model: Dictionary = d_binding.presentation_render_model
    var render_model_hash: String = _sha256_text(JSON.stringify(_stable_value(render_model)))
    var source_assets: Dictionary = source.get("assets", {})
    var bound_assets: Dictionary = d_binding.physical_assets
    if bound_assets.get("background_path", "") != source_assets.get("background_path", "") or bound_assets.get("object_path", "") != source_assets.get("object_path", "") or bound_assets.get("target_path", "") != source_assets.get("target_path", ""):
        return {"success": false, "error": "D presentation binding changed canonical asset paths."}

    var visual_cfg: Dictionary = source.get("presentation", {}).get("visual", {})
    var parking_cfg: Dictionary = source.get("difficulty", {}).get("parking", {})
    var asset_nodes: Array[Dictionary] = []
    var asset_specs: Array[Dictionary] = [
        {"role": "BACKGROUND", "path": str(bound_assets.get("background_path", "")), "rel": "assets/c6/garage_background.svg", "binding_source": "CanonicalV2.assets.background_path", "transform": {"policy": "INTRINSIC_SOURCE_ASSET", "projection_applied": false}},
        {"role": "ANIMATED_OBJECT", "path": str(bound_assets.get("object_path", "")), "rel": "assets/c6/car.svg", "binding_source": "CanonicalV2.assets.object_path", "transform": {"policy": "PRESERVE_SIMULATION_FRAME_TRANSFORMS_AND_DECLARED_PRESENTATION_METADATA_SEPARATELY", "declared_scale": float(visual_cfg.get("object_scale", 0.85)), "declared_offset": visual_cfg.get("object_offset", [0.0, 0.0]), "projection_applied": false}},
        {"role": "TARGET", "path": str(bound_assets.get("target_path", "")), "rel": "assets/c6/parking_target.svg", "binding_source": "CanonicalV2.assets.target_path", "transform": {"policy": "PRESERVE_CANONICAL_STATIC_TARGET_METADATA_SEPARATELY", "position_source": "CHALLENGE_004.difficulty.parking.target_position", "declared_position": parking_cfg.get("target_position", []), "declared_scale": float(visual_cfg.get("target_scale", 0.85)), "declared_offset": visual_cfg.get("target_offset", [0.0, 0.0]), "projection_applied": false}}
    ]
    for spec: Dictionary in asset_specs:
        var path: String = str(spec.get("path", ""))
        var bytes: PackedByteArray = FileAccess.get_file_as_bytes(path)
        if path.is_empty() or bytes.is_empty():
            return {"success": false, "error": "Physical asset missing/unreadable: %s" % path}
        var loaded_resource: Resource = ResourceLoader.load(path) as Resource
        if loaded_resource == null or not (loaded_resource is Texture2D):
            return {"success": false, "error": "Physical asset did not load as Texture2D: %s" % path}
        var texture: Texture2D = loaded_resource as Texture2D
        var expected_sizes: Dictionary = {"BACKGROUND": [1080, 1920], "ANIMATED_OBJECT": [160, 320], "TARGET": [200, 400]}
        var expected_size: Array = expected_sizes.get(str(spec.get("role", "")), [])
        if expected_size.size() != 2 or int(texture.get_width()) != int(expected_size[0]) or int(texture.get_height()) != int(expected_size[1]):
            return {"success": false, "error": "Loaded asset intrinsic size changed: %s" % path}
        var asset_node: Dictionary = {
            "role": str(spec.get("role", "")),
            "resource_path": path,
            "sha256": _sha256_bytes(bytes),
            "resource_loaded_as_texture2d": true,
            "intrinsic_width": int(texture.get_width()),
            "intrinsic_height": int(texture.get_height()),
            "binding_source": str(spec.get("binding_source", "")),
            "declared_transform": spec.get("transform", {})
        }
        asset_nodes.append(asset_node)

    var game_records: Array[Dictionary] = []
    for index: int in range(sim.frames.size()):
        var frame: Variant = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            return {"success": false, "error": "Invalid simulation visual snapshot at GAME index %d." % index}
        game_records.append({
            "source_game_frame_index": index,
            "position": {"x": float(frame.position.x), "y": float(frame.position.y)},
            "rotation_radians": float(frame.rotation),
            "scale": {"x": float(frame.scale.x), "y": float(frame.scale.y)},
            "opacity": float(frame.opacity),
            "texture_index": int(frame.texture_index),
            "variant_id": int(frame.variant_id)
        })
    if game_records.size() != 420:
        return {"success": false, "error": "Visual frame payload did not preserve all 420 GAME snapshots."}

    var phase_segments: Array[Dictionary] = []
    var boundary: int = 0
    var phase_data: Array[Dictionary] = [
        {"phase": "HOOK", "frame_count": int(timeline_obj.hook_frames)},
        {"phase": "GAME", "frame_count": int(timeline_obj.game_frames)},
        {"phase": "REVEAL", "frame_count": int(timeline_obj.reveal_frames)},
        {"phase": "CTA", "frame_count": int(timeline_obj.cta_frames)}
    ]
    for phase: Dictionary in phase_data:
        var count: int = int(phase.get("frame_count", 0))
        phase_segments.append({"phase": str(phase.get("phase", "")), "start_frame": boundary, "end_frame": boundary + count, "frame_count": count})
        boundary += count
    if boundary != 900:
        return {"success": false, "error": "Source phase ranges do not sum to 900 frames."}

    var frames_hash: String = _sha256_text(JSON.stringify(_stable_value(game_records)))
    var payload: Dictionary = {
        "schema": OutputSchema,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
        "identity": {"challenge_id": "CHALLENGE_004", "mechanic": "parking_v2", "mechanic_version": "2.0", "presentation_profile_id": "social_default_v1", "coordinate_space": str(source.get("presentation", {}).get("coordinate_space", "")), "materialization": "IN_MEMORY_ONLY_SOURCE_TIMEBASE"},
        "asset_nodes": asset_nodes,
        "presentation_render_model": _stable_value(render_model),
        "presentation_render_model_sha256": render_model_hash,
        "timeline": {"fps": int(timeline_obj.fps), "total_frames": int(timeline_obj.total_frames), "duration_seconds": float(timeline_obj.total_frames) / float(timeline_obj.fps), "phase_order": ["HOOK", "GAME", "REVEAL", "CTA"], "phase_segments": phase_segments},
        "animation": {"frame_source": "SimulationResult.frames", "source_fps": int(timeline_obj.fps), "game_frame_count": int(sim.frames.size()), "frame_records": game_records, "frame_records_sha256": frames_hash, "fields_included": ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"], "telemetry_included": false, "winning_frame_sampling_used": false, "delivery_resampling": "UNRESOLVED_NOT_APPLIED"},
        "source_coordinate_space": str(source.get("presentation", {}).get("coordinate_space", "")),
        "profile_source_canvas": {"width": int(d_binding.presentation_profile.source_canvas_size.x), "height": int(d_binding.presentation_profile.source_canvas_size.y)},
        "profile_master_output": {"width": int(d_binding.presentation_profile.master_output_size.x), "height": int(d_binding.presentation_profile.master_output_size.y)},
        "coordinate_projection": "UNRESOLVED_NOT_APPLIED",
        "editorial_visibility": "NOT_APPLIED_BY_THIS_PAYLOAD_PREVIEW",
        "execution_boundary": {"payload_written": false, "media_output_created": false, "renderer_native_input_emitted": false, "renderer_dispatch_invoked": false, "renderer_activation": false, "c11c_source_mutation": false, "d4_8": "BLOCKED", "release_authority": "NONE", "output_artifact_path": null}
    }
    var payload_sha: String = _sha256_text(JSON.stringify(_stable_value(payload)))

    var after_signature: String = _frame_signature_sha256(sim)
    var invariance: bool = before_signature == after_signature and int(sim.winning_frame) == before_winning and is_equal_approx(float(sim.score), before_score) and is_equal_approx(float(sim.minimum_distance), before_distance) and is_equal_approx(float(sim.tolerance_threshold), before_tolerance) and sim.frames.size() == 420
    if not invariance:
        return {"success": false, "error": "Simulation invariance check failed during payload materialization."}
    return {
        "success": true,
        "payload": payload,
        "payload_sha256": payload_sha,
        "asset_nodes": asset_nodes,
        "source_timeline": {"fps": int(timeline_obj.fps), "total_frames": int(timeline_obj.total_frames), "duration_seconds": float(timeline_obj.total_frames) / float(timeline_obj.fps), "phase_order": ["HOOK", "GAME", "REVEAL", "CTA"], "phase_segments": phase_segments},
        "frame_records_sha256": frames_hash,
        "render_model_sha256": render_model_hash,
        "frame_signature_sha256": after_signature,
        "simulation_invariance": {"simulation_invariance": invariance, "winning_frame_sampling_used": false}
    }

func _validate_payload_in_memory(payload: Dictionary, assets: Array, payload_hash: String, timeline: Dictionary, frames_hash: String) -> bool:
    if str(payload.get("schema", "")) != OutputSchema or str(payload.get("status", "")) != "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT":
        return false
    if assets.size() != 3 or int(payload.get("animation", {}).get("frame_records", []).size()) != 420:
        return false
    if payload_hash.length() != 64 or frames_hash.length() != 64:
        return false
    if int(timeline.get("fps", 0)) != 60 or int(timeline.get("total_frames", 0)) != 900 or float(timeline.get("duration_seconds", 0.0)) != 15.0:
        return false
    if str(payload.get("coordinate_projection", "")) != "UNRESOLVED_NOT_APPLIED" or str(payload.get("animation", {}).get("delivery_resampling", "")) != "UNRESOLVED_NOT_APPLIED":
        return false
    if bool(payload.get("animation", {}).get("telemetry_included", true)) or bool(payload.get("animation", {}).get("winning_frame_sampling_used", true)):
        return false
    if _contains_key(payload, "winning_frame") or _contains_key(payload, "close_calls") or _contains_key(payload, "minimum_distance") or _contains_key(payload, "score") or _contains_key(payload, "custom_data"):
        return false
    var roles: Dictionary = {}
    var expected_paths: Dictionary = {"BACKGROUND": "res://assets/c6/garage_background.svg", "ANIMATED_OBJECT": "res://assets/c6/car.svg", "TARGET": "res://assets/c6/parking_target.svg"}
    for node: Dictionary in assets:
        var role: String = str(node.get("role", ""))
        if roles.has(role) or not bool(node.get("resource_loaded_as_texture2d", false)):
            return false
        if str(node.get("resource_path", "")) != str(expected_paths.get(role, "")):
            return false
        roles[role] = true
    return roles.has("BACKGROUND") and roles.has("ANIMATED_OBJECT") and roles.has("TARGET")

func _contract_guard() -> bool:
    var bytes: PackedByteArray = FileAccess.get_file_as_bytes(ContractPath)
    if bytes.is_empty(): return false
    var value: Variant = JSON.parse_string(bytes.get_string_from_utf8())
    if not (value is Dictionary): return false
    var contract: Dictionary = value
    if str(contract.get("schema", "")) != "C11-D-D9-RENDERER-CHALLENGE-VISUAL-PAYLOAD-PREVIEW-CONTRACT-V1": return false
    if str(contract.get("status", "")) != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN": return false
    if str(contract.get("source_authority", {}).get("frozen_manifest_sha256", "")) != FrozenManifestSha: return false
    if str(contract.get("source_authority", {}).get("challenge_source_sha256", "")) != ChallengeSha: return false
    var pins_value: Variant = contract.get("pinned_sources", [])
    if not (pins_value is Array) or pins_value.size() != SourcePins.size(): return false
    var declared_pins: Dictionary = {}
    for pin_value: Variant in pins_value:
        if not (pin_value is Dictionary): return false
        var pin: Dictionary = pin_value
        declared_pins[str(pin.get("path", ""))] = str(pin.get("sha256", ""))
    if declared_pins != SourcePins: return false
    var locks: Dictionary = contract.get("governance_locks", {})
    return str(locks.get("source_adapter_mode", "")) == "PREPARE_ONLY" and str(locks.get("d4_8", "")) == "BLOCKED" and str(locks.get("release_authority", "")) == "NONE" and locks.get("renderer_baseline_approved") == false and locks.get("renderer_baseline_frozen") == false

func _contains_key(value: Variant, forbidden: String) -> bool:
    if value is Dictionary:
        for key: Variant in value.keys():
            if str(key).to_lower() == forbidden.to_lower(): return true
            if _contains_key(value[key], forbidden): return true
    elif value is Array:
        for item: Variant in value:
            if _contains_key(item, forbidden): return true
    return false

func _frame_signature_sha256(sim: Variant) -> String:
    var parts := PackedStringArray()
    for index: int in range(sim.frames.size()):
        var frame: Variant = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot(): return ""
        # Fingerprint only explicit visual snapshot fields. Never inspect, enumerate, or serialize FrameSnapshot.custom_data.
        parts.append("%d|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%d" % [index, frame.position.x, frame.position.y, frame.rotation, frame.scale.x, frame.scale.y, frame.opacity, float(frame.texture_index), int(frame.variant_id)])
    return _sha256_text("\n".join(parts))

func _stable_value(value: Variant) -> Variant:
    if value is Dictionary:
        var output: Dictionary = {}
        var keys: Array = value.keys()
        keys.sort_custom(func(a: Variant, b: Variant) -> bool: return str(a) < str(b))
        for key: Variant in keys: output[str(key)] = _stable_value(value[key])
        return output
    if value is Array:
        var output_array: Array = []
        for item: Variant in value: output_array.append(_stable_value(item))
        return output_array
    if value is Vector2: return {"$type": "Vector2", "x": value.x, "y": value.y}
    if value is Vector2i: return {"$type": "Vector2i", "x": value.x, "y": value.y}
    if value is Vector3: return {"$type": "Vector3", "x": value.x, "y": value.y, "z": value.z}
    if value is Color: return {"$type": "Color", "r": value.r, "g": value.g, "b": value.b, "a": value.a}
    if value is Rect2: return {"$type": "Rect2", "position": _stable_value(value.position), "size": _stable_value(value.size)}
    if value is String or value is StringName or value is int or value is float or value is bool or value == null: return value
    return str(value)

func _sha256_text(value: String) -> String:
    return _sha256_bytes(value.to_utf8_buffer())

func _sha256_bytes(bytes: PackedByteArray) -> String:
    if bytes.is_empty(): return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    var context := HashingContext.new()
    context.start(HashingContext.HASH_SHA256)
    context.update(bytes)
    return context.finish().hex_encode()

func _fail(message: String) -> void:
    printerr("C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW FAIL | %s" % message)
    quit(1)
