extends RefCounted

## E4A.6 D-only live Challenge consumer.
## The native C SocialUIBinder remains the only full PresentationUI binder.
## This consumer is optional, activated only by --c11e-editorial-envelope=<path>.
## It mounts the existing C11C shared editorial layer once and thereafter
## applies only the approved header/footer model plus three targeted visibility
## overrides. It does not change phase timing, mechanics, seeds, or C11-C APIs.

const ChallengeEditorialAdapter = preload("res://tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd")
const SharedLayerScript = preload("res://core/presentation/C11CVisualEditorialLayer.gd")
const EnvelopeSchema := "C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1"
const ApprovedPolicyPath := "res://definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json"
const ApprovedPolicySha := "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"
const LayoutContractPath := "res://docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md"
const LayoutContractSha := "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461"
const ExpectedFields := ["title", "subtitle", "player_name", "challenge_label", "call_to_action", "language"]
const ExpectedWindows := {
    "title": ["HOOK"],
    "subtitle": ["HOOK"],
    "player_name": ["HOOK", "GAME"],
    "challenge_label": ["HOOK", "GAME"],
    "call_to_action": ["CTA"],
    "language": []
}
const ExpectedRegions := {
    "title": "HEADER",
    "subtitle": "HEADER",
    "player_name": "CHALLENGE_OVERLAY",
    "challenge_label": "CHALLENGE_OVERLAY",
    "call_to_action": "FOOTER",
    "language": "METADATA"
}

var _envelope: Dictionary = {}
var _intent: Dictionary = {}
var _field_rows: Array = []
var _presentation_ui: PresentationUI = null
var _frame: UnifiedSocialFrame = null
var _timeline: VideoTimeline = null
var _layer: RefCounted = null
var _enabled: bool = false
var _mounted: bool = false
var _failed: bool = false
var _last_error: String = ""
var _mount_count: int = 0
var _frame_count: int = 0
var _header_owner_frames: int = 0
var _footer_owner_frames: int = 0
var _native_cta_owner_frames: int = 0
var _envelope_sha256: String = ""

func configure_from_file(
    envelope_path: String,
    challenge_config: Dictionary,
    timeline: VideoTimeline,
    presentation_ui: PresentationUI,
    frame: UnifiedSocialFrame
) -> Dictionary:
    if envelope_path.strip_edges().is_empty():
        return {"success": true, "enabled": false, "reason": "NO_D_ENVELOPE_ARGUMENT"}
    if not FileAccess.file_exists(envelope_path):
        return _fail("D editorial envelope file does not exist: %s" % envelope_path)
    var file := FileAccess.open(envelope_path, FileAccess.READ)
    if file == null:
        return _fail("D editorial envelope cannot be opened: %s" % envelope_path)
    var raw_bytes: PackedByteArray = file.get_buffer(file.get_length())
    file.close()
    if raw_bytes.is_empty():
        return _fail("D editorial envelope is empty.")
    var raw_sha256 := _sha256_bytes(raw_bytes)
    var sidecar_path := envelope_path + ".sha256"
    if not FileAccess.file_exists(sidecar_path):
        return _fail("D editorial envelope SHA-256 sidecar is missing.")
    var sidecar := FileAccess.open(sidecar_path, FileAccess.READ)
    if sidecar == null:
        return _fail("D editorial envelope SHA-256 sidecar cannot be opened.")
    var sidecar_text := sidecar.get_as_text().strip_edges()
    sidecar.close()
    var expected_sha256 := sidecar_text.substr(0, 64).to_lower()
    if not _is_sha256(expected_sha256) or expected_sha256 != raw_sha256:
        return _fail("D editorial envelope SHA-256 sidecar mismatch.")
    var parsed: Variant = JSON.parse_string(raw_bytes.get_string_from_utf8())
    if not (parsed is Dictionary):
        return _fail("D editorial envelope must be a JSON object.")
    var validation: Dictionary = validate_envelope(parsed, challenge_config, timeline)
    if not bool(validation.get("success", false)):
        return _fail(str(validation.get("error", "D editorial envelope validation failed.")))
    if presentation_ui == null or frame == null or timeline == null:
        return _fail("D live consumer requires PresentationUI, UnifiedSocialFrame and VideoTimeline.")
    if presentation_ui.hook_label == null or presentation_ui.countdown == null or presentation_ui.cta == null:
        return _fail("Native Challenge Hook/Countdown/CTA components are incomplete.")
    _envelope = parsed
    _intent = parsed.get("e1_intent", {})
    _field_rows = parsed.get("fields", [])
    _presentation_ui = presentation_ui
    _frame = frame
    _timeline = timeline
    _envelope_sha256 = raw_sha256
    _enabled = true
    return {
        "success": true,
        "enabled": true,
        "envelope_sha256": _envelope_sha256,
        "intent_hash": str(parsed.get("intent_hash", "")),
        "source_fps": int(parsed.get("source_timebase", {}).get("fps", 0)),
        "source_frames": int(parsed.get("source_timebase", {}).get("total_frames", 0))
    }

func validate_envelope(
    envelope: Dictionary,
    challenge_config: Dictionary,
    timeline: VideoTimeline
) -> Dictionary:
    if timeline == null:
        return {"success": false, "error": "VideoTimeline is required to validate the D envelope."}
    if str(envelope.get("schema", "")) != EnvelopeSchema or str(envelope.get("schema_version", "")) != "1.0":
        return {"success": false, "error": "D editorial envelope schema/version mismatch."}
    if str(envelope.get("status", "")) != "PREPARED_E1_NOT_DISPATCHED":
        return {"success": false, "error": "D editorial envelope crossed the E1 preparation boundary."}
    if str(envelope.get("content_type", "")) != "challenges":
        return {"success": false, "error": "D live editorial consumer is Challenge-only."}
    var challenge_id := str(challenge_config.get("challenge_id", challenge_config.get("id", "")))
    if challenge_id.is_empty() or str(envelope.get("challenge_id", "")) != challenge_id:
        return {"success": false, "error": "D envelope Challenge identity does not match the loaded canonical Challenge."}
    var intent_value: Variant = envelope.get("e1_intent", null)
    if not (intent_value is Dictionary):
        return {"success": false, "error": "D envelope is missing the sealed E1 intent."}
    var intent: Dictionary = intent_value
    if str(intent.get("schema", "")) != "C11-E-PRODUCTION-INTENT-V1" or str(intent.get("status", "")) != "PREPARED_E1_NOT_DISPATCHED":
        return {"success": false, "error": "Nested E1 intent is not sealed and preparation-only."}
    var request_value: Variant = intent.get("request", null)
    if not (request_value is Dictionary):
        return {"success": false, "error": "Nested E1 request is missing."}
    var request: Dictionary = request_value
    var selection_value: Variant = request.get("selection", null)
    if not (selection_value is Dictionary):
        return {"success": false, "error": "Nested E1 Challenge selector is missing."}
    var selection: Dictionary = selection_value
    if str(request.get("content_type", "")) != "challenges" or str(selection.get("content_type", "")) != "challenges" or str(selection.get("variant_id", "")) != challenge_id:
        return {"success": false, "error": "Nested E1 selector identity does not match this Challenge."}
    var identity_value: Variant = intent.get("identity", null)
    if not (identity_value is Dictionary):
        return {"success": false, "error": "Nested E1 intent identity is missing."}
    var identity: Dictionary = identity_value
    var intent_hash := str(identity.get("intent_hash", ""))
    if not _is_sha256(intent_hash) or str(envelope.get("intent_hash", "")) != intent_hash:
        return {"success": false, "error": "Nested E1 intent hash mismatch."}
    if str(envelope.get("request_id", "")) != str(request.get("request_id", "")):
        return {"success": false, "error": "Envelope request identity mismatch."}
    var option_result: Dictionary = ChallengeEditorialAdapter.resolve_hook_countdown_option(intent)
    if not bool(option_result.get("success", false)):
        return {"success": false, "error": "E1 Challenge presentation option rejected: %s" % str(option_result.get("error", "unknown"))}
    var option_value: Variant = envelope.get("presentation_options", null)
    if not (option_value is Dictionary) or option_value.size() != 1 or typeof(option_value.get("show_hook_countdown")) != TYPE_BOOL:
        return {"success": false, "error": "Envelope presentation option is invalid."}
    if bool(option_value.get("show_hook_countdown")) != bool(option_result.get("show_hook_countdown", true)):
        return {"success": false, "error": "Envelope presentation option differs from sealed E1 intent."}

    var timebase_value: Variant = envelope.get("source_timebase", null)
    if not (timebase_value is Dictionary):
        return {"success": false, "error": "D envelope source timebase is missing."}
    var timebase: Dictionary = timebase_value
    if int(timebase.get("fps", -1)) != timeline.fps or int(timebase.get("total_frames", -1)) != timeline.total_frames:
        return {"success": false, "error": "D envelope FPS/frame count differs from the active native Challenge timeline."}
    if str(timebase.get("kind", "")) != "SOURCE_FRAME_INDEX":
        return {"success": false, "error": "D envelope is not bound to the source frame index."}

    var expected_phase_ranges: Array[Dictionary] = _expected_phase_ranges(timeline)
    var phase_ranges_value: Variant = envelope.get("source_phase_ranges", null)
    if not (phase_ranges_value is Array) or phase_ranges_value.size() != expected_phase_ranges.size():
        return {"success": false, "error": "D envelope phase range set is incomplete."}
    for index in range(expected_phase_ranges.size()):
        var actual_value: Variant = phase_ranges_value[index]
        if not (actual_value is Dictionary):
            return {"success": false, "error": "D envelope phase range row is malformed."}
        var actual: Dictionary = actual_value
        var expected: Dictionary = expected_phase_ranges[index]
        if str(actual.get("phase", "")) != str(expected["phase"]) or int(actual.get("start_frame", -1)) != int(expected["start_frame"]) or int(actual.get("end_frame", -1)) != int(expected["end_frame"]) or str(actual.get("timebase", "")) != "SOURCE_FPS_HALF_OPEN":
            return {"success": false, "error": "D envelope phase range differs from native timeline: %s" % str(expected["phase"])}

    if str(envelope.get("policy_sha256", "")) != ApprovedPolicySha or str(envelope.get("layout_contract_sha256", "")) != LayoutContractSha:
        return {"success": false, "error": "D envelope approved policy/layout identity mismatch."}
    var policy_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ApprovedPolicyPath)
    var layout_bytes: PackedByteArray = FileAccess.get_file_as_bytes(LayoutContractPath)
    if policy_bytes.is_empty() or _sha256_bytes(policy_bytes) != ApprovedPolicySha:
        return {"success": false, "error": "Live E4A approval policy file hash mismatch."}
    if layout_bytes.is_empty() or _sha256_bytes(layout_bytes) != LayoutContractSha:
        return {"success": false, "error": "Live D1.5 layout contract file hash mismatch."}

    var fields_value: Variant = envelope.get("fields", null)
    if not (fields_value is Array) or fields_value.size() != ExpectedFields.size():
        return {"success": false, "error": "D envelope must contain exactly six approved editorial rows."}
    var seen: Dictionary = {}
    for field_value: Variant in fields_value:
        if not (field_value is Dictionary):
            return {"success": false, "error": "D envelope editorial field row is malformed."}
        var field: Dictionary = field_value
        var name := str(field.get("field", ""))
        if not ExpectedFields.has(name) or seen.has(name):
            return {"success": false, "error": "D envelope field allowlist contains an unknown or duplicate field."}
        seen[name] = true
        if str(field.get("region", "")) != str(ExpectedRegions[name]):
            return {"success": false, "error": "D envelope field region differs from approved policy: %s" % name}
        var windows_value: Variant = field.get("source_phase_windows", null)
        if not (windows_value is Array) or windows_value != ExpectedWindows[name]:
            return {"success": false, "error": "D envelope source phase window differs from approved policy: %s" % name}
        if str(field.get("policy_sha256", "")) != ApprovedPolicySha or str(field.get("layout_contract_sha256", "")) != LayoutContractSha:
            return {"success": false, "error": "D envelope per-field policy/layout pin mismatch: %s" % name}
        var effective_value := str(field.get("effective_value", ""))
        if str(field.get("value_sha256", "")) != _sha256_text(effective_value):
            return {"success": false, "error": "D envelope effective value hash mismatch: %s" % name}
        var expected_ranges: Array = []
        for phase_name: String in ExpectedWindows[name]:
            for phase_value: Variant in expected_phase_ranges:
                if str(phase_value.get("phase", "")) == phase_name:
                    expected_ranges.append({
                        "phase": phase_name,
                        "start_frame": int(phase_value.get("start_frame", -1)),
                        "end_frame": int(phase_value.get("end_frame", -1)),
                        "timebase": "SOURCE_FPS_HALF_OPEN"
                    })
        var ranges_value: Variant = field.get("source_frame_ranges", null)
        if not _source_frame_ranges_match(ranges_value, expected_ranges):
            return {
                "success": false,
                "error": "D envelope field source frame ranges do not match approved phase windows: %s expected=%s actual=%s" % [name, JSON.stringify(expected_ranges), JSON.stringify(ranges_value)]
            }
        var disposition := str(field.get("disposition", ""))
        if disposition == "READY_FOR_ISOLATED_TEST_PIXEL_DRAW":
            if effective_value.strip_edges().is_empty() or not ["HEADER", "FOOTER"].has(str(ExpectedRegions[name])):
                return {"success": false, "error": "Renderable D field is empty or outside approved regions: %s" % name}
        elif disposition == "BLOCKED_GEOMETRY_UNRESOLVED":
            if not ["player_name", "challenge_label"].has(name):
                return {"success": false, "error": "Only Challenge overlay fields may remain geometry-blocked."}
        elif disposition == "METADATA_ONLY":
            if name != "language":
                return {"success": false, "error": "Only language may be metadata-only."}
        elif disposition == "OMITTED_EMPTY":
            if not effective_value.is_empty():
                return {"success": false, "error": "Omitted D field contains a visual value: %s" % name}
        else:
            return {"success": false, "error": "Unsupported D field disposition: %s" % name}
    if seen.size() != ExpectedFields.size():
        return {"success": false, "error": "D envelope does not cover the exact six-field allowlist."}

    var governance_value: Variant = envelope.get("governance", null)
    if not (governance_value is Dictionary):
        return {"success": false, "error": "D envelope governance boundary is missing."}
    var governance: Dictionary = governance_value
    if governance.get("renderer_input_emitted") != false or governance.get("production_dispatch") != false or governance.get("media_created") != false:
        return {"success": false, "error": "D envelope crossed renderer/dispatch/media boundary."}
    if str(governance.get("release_authority", "")) != "NONE" or str(governance.get("d4_8", "")) != "BLOCKED" or str(governance.get("d9_10", "")) != "PREPARE_ONLY":
        return {"success": false, "error": "D envelope governance locks are inconsistent."}
    return {"success": true, "error": ""}


func _source_frame_ranges_match(actual_value: Variant, expected_ranges: Array) -> bool:
    # JSON.parse_string() yields Variants while native timeline rows are typed
    # Dictionaries. Compare the approved schema fields explicitly instead of
    # relying on opaque Array/Dictionary Variant equality. Numeric frame values
    # are normalized to int; no range, phase, or timebase is widened.
    if not (actual_value is Array):
        return false
    var actual_ranges: Array = actual_value
    if actual_ranges.size() != expected_ranges.size():
        return false
    for index in range(expected_ranges.size()):
        var actual_row_value: Variant = actual_ranges[index]
        if not (actual_row_value is Dictionary):
            return false
        var actual_row: Dictionary = actual_row_value
        var expected_row: Dictionary = expected_ranges[index]
        if str(actual_row.get("phase", "")) != str(expected_row.get("phase", "")):
            return false
        if int(actual_row.get("start_frame", -1)) != int(expected_row.get("start_frame", -2)):
            return false
        if int(actual_row.get("end_frame", -1)) != int(expected_row.get("end_frame", -2)):
            return false
        if str(actual_row.get("timebase", "")) != "SOURCE_FPS_HALF_OPEN":
            return false
    return true

func apply_after_native_bind(native_render_model: Dictionary, absolute_source_frame: int) -> Dictionary:
    if not _enabled:
        return {"success": true, "enabled": false}
    if _failed:
        return {"success": false, "error": _last_error}
    if absolute_source_frame < 0 or absolute_source_frame >= int(_envelope.get("source_timebase", {}).get("total_frames", 0)):
        return _fail("D consumer received an out-of-range native source frame.")
    var option_result: Dictionary = ChallengeEditorialAdapter.resolve_hook_countdown_option(_intent)
    if not bool(option_result.get("success", false)):
        return _fail("E1 presentation option became invalid after initialization.")
    var shared_model_result: Dictionary = ChallengeEditorialAdapter.build_shared_editorial_model(
        _field_rows,
        absolute_source_frame,
        int(_envelope.get("source_timebase", {}).get("total_frames", 0)),
        314159,
        str(native_render_model.get("hook_text", "")),
        bool(option_result.get("show_hook_countdown", true))
    )
    if not bool(shared_model_result.get("success", false)):
        return _fail("D shared editorial model rejected source frame %d: %s" % [absolute_source_frame, str(shared_model_result.get("error", "unknown"))])
    var adapted_result: Dictionary = ChallengeEditorialAdapter.adapt_native_challenge_render_model(
        native_render_model,
        _intent,
        shared_model_result
    )
    if not bool(adapted_result.get("success", false)):
        return _fail("D native visibility adaptation failed: %s" % str(adapted_result.get("error", "unknown")))

    var editorial_enabled := bool(shared_model_result.get("header_active", false)) or bool(shared_model_result.get("footer_active", false))
    if editorial_enabled and not _mounted:
        _layer = SharedLayerScript.new()
        var mounted_value: Variant = _layer.call("mount", _frame)
        if typeof(mounted_value) != TYPE_BOOL or not bool(mounted_value):
            return _fail("C11C shared editorial layer could not mount on the existing UnifiedSocialFrame.")
        _mounted = true
        _mount_count += 1
        var header_background := _frame.get_header_content_root().get_node_or_null("C11CVisualEditorialHeader/C11CHeaderBackground") as ColorRect
        var footer_background := _frame.get_footer_content_root().get_node_or_null("C11CVisualEditorialFooter/C11CFooterBackground") as ColorRect
        if header_background == null or footer_background == null:
            return _fail("Mounted C11C shared editorial background nodes are incomplete.")
        header_background.color = Color("05070B")
        footer_background.color = Color("05070B")

    if _mounted:
        _layer.call("apply_render_model", shared_model_result["render_model"])

    var adapted_model: Dictionary = adapted_result.get("render_model", {})
    # Targeted component visibility only. Native text/value remains configured
    # by the single C SocialUIBinder call immediately before this method.
    _presentation_ui.hook_label.visible = bool(adapted_model.get("show_hook", false))
    _presentation_ui.countdown.visible = bool(adapted_model.get("countdown_visible", false))
    _presentation_ui.cta.visible = bool(adapted_model.get("cta_visible", false))

    _frame_count += 1
    if bool(shared_model_result.get("header_active", false)):
        _header_owner_frames += 1
    if bool(shared_model_result.get("footer_active", false)):
        _footer_owner_frames += 1
    if str(adapted_result.get("native_cta_owner", "")) == "C_CHALLENGE_PRESENTATION_UI" and bool(adapted_model.get("cta_visible", false)):
        _native_cta_owner_frames += 1
    return {
        "success": true,
        "enabled": true,
        "mounted": _mounted,
        "mount_count": _mount_count,
        "header_active": bool(shared_model_result.get("header_active", false)),
        "footer_active": bool(shared_model_result.get("footer_active", false)),
        "native_cta_owner": str(adapted_result.get("native_cta_owner", ""))
    }

func get_runtime_summary() -> Dictionary:
    return {
        "schema": "C11E-E4A6-LIVE-CONSUMER-RUNTIME-SUMMARY-V1",
        "status": "PASS_TEST_ONLY" if _enabled and not _failed else "NOT_ENABLED" if not _enabled else "FAIL",
        "enabled": _enabled,
        "failed": _failed,
        "error": _last_error,
        "envelope_sha256": _envelope_sha256,
        "intent_hash": str(_envelope.get("intent_hash", "")),
        "frames_seen": _frame_count,
        "mount_count": _mount_count,
        "header_d_owner_frames": _header_owner_frames,
        "footer_d_owner_frames": _footer_owner_frames,
        "native_cta_owner_frames": _native_cta_owner_frames,
        "production_dispatch": false,
        "renderer_input_emitted": false,
        "media_created": false,
        "release_authority": "NONE"
    }

func _expected_phase_ranges(timeline: VideoTimeline) -> Array[Dictionary]:
    var result: Array[Dictionary] = []
    var cursor := 0
    var rows := [
        {"phase": "HOOK", "count": timeline.hook_frames},
        {"phase": "GAME", "count": timeline.game_frames},
        {"phase": "REVEAL", "count": timeline.reveal_frames},
        {"phase": "CTA", "count": timeline.cta_frames}
    ]
    for row_value: Variant in rows:
        var row: Dictionary = row_value
        var count := int(row.get("count", -1))
        result.append({
            "phase": str(row.get("phase", "")),
            "start_frame": cursor,
            "end_frame": cursor + count
        })
        cursor += count
    return result

func _fail(message: String) -> Dictionary:
    _failed = true
    _last_error = message
    return {"success": false, "enabled": _enabled, "error": message}

func _sha256_text(value: String) -> String:
    return _sha256_bytes(value.to_utf8_buffer())

func _sha256_bytes(value: PackedByteArray) -> String:
    var hashing := HashingContext.new()
    if hashing.start(HashingContext.HASH_SHA256) != OK:
        return ""
    hashing.update(value)
    return hashing.finish().hex_encode()

func _is_sha256(value: String) -> bool:
    if value.length() != 64:
        return false
    for character in value:
        if not "0123456789abcdef".contains(character):
            return false
    return true
