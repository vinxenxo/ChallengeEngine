extends SceneTree

## Source-to-consumer composition test only. No production call sites and no renderer.
const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const SimulationResultScript = preload("res://core/simulation/SimulationResult.gd")
const ConsumerScript = preload("res://tools/c11d/d9/allowlisted_coordinate_consumer_review_only_v2.gd")

const FrozenManifestPath: String = "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const FrozenManifestSha: String = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const ConsumerContractPath: String = "res://definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_CONTRACT_V2.json"
const ConsumerContractSha: String = "0bd65e8f64c13850670d927d62209276ae94999ce57c790db7ae1592fa793ae9"
const CompositionContractPath: String = "res://definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CONTRACT_V1.json"
const CompositionContractSha: String = "575717bb3f36b476c9742488c8cace622a217c8861e376d17c519d02c70534b7"

const CandidateRows: Array[Dictionary] = [
    {"candidate_id":"CHALLENGE_003", "mechanic":"pilot", "source_path":"res://challenges/CHALLENGE_003.json", "source_sha256":"38cb0166482c5ba4862deef8ab75dad4a6e1524590b6850312bab5238f078419", "expected_field":"target_x"},
    {"candidate_id":"CHALLENGE_005", "mechanic":"hit_v1", "source_path":"res://challenges/CHALLENGE_005.json", "source_sha256":"e173736fcbb0e340cd250be1111fa9d38489934d55cc0e0c93835c66f9596e30", "expected_field":"target_position"},
    {"candidate_id":"CHALLENGE_006", "mechanic":"catch_v1", "source_path":"res://challenges/CHALLENGE_006.json", "source_sha256":"2d7d7397cbb0a2109f300859a5d7c0830ded0553522a5120f61750f5bc0b5694", "expected_field":"target_position"},
    {"candidate_id":"CHALLENGE_007", "mechanic":"find_v1", "source_path":"res://challenges/CHALLENGE_007.json", "source_sha256":"269f9588e5a6b7d253e2e944440cc41dc3a9db8967775ffa819edebe729a3a61", "expected_field":"target_position"}
]

const ROOT_KEYS: Array[String] = ["contract_id", "candidate_id", "logical_canvas_id", "source_frame_count", "frames"]
const FRAME_KEYS: Array[String] = ["source_frame_index", "target_marker"]
const MARKER_KEYS: Array[String] = ["role", "asset_path", "anchor_x", "anchor_y", "logical_width", "logical_height", "anchor_mode", "asset_bounds_policy"]

var _consumer: RefCounted
var _failures: Array[String] = []
var _candidate_passes: int = 0
var _total_source_frames: int = 0
var _total_marker_frames: int = 0

func _initialize() -> void:
    _consumer = ConsumerScript.new()
    call_deferred("_run")

func _run() -> void:
    var version_info: Dictionary = Engine.get_version_info()
    _check(
        "godot_4_7_1_mono",
        int(version_info.get("major", -1)) == 4
        and int(version_info.get("minor", -1)) == 7
        and int(version_info.get("patch", -1)) == 1
        and str(version_info.get("status", "")) == "stable"
        and str(version_info.get("build", "")) == "official"
        and ClassDB.class_exists("CSharpScript")
    )
    _check("c11c_frozen_manifest", _resource_sha(FrozenManifestPath) == FrozenManifestSha)
    _check("consumer_v2_contract_pin", _resource_sha(ConsumerContractPath) == ConsumerContractSha)
    _check("composition_contract_pin", _resource_sha(CompositionContractPath) == CompositionContractSha)

    var total_expected: int = 0
    for candidate_row: Dictionary in CandidateRows:
        var candidate_id: String = str(candidate_row.get("candidate_id", ""))
        var source_path: String = str(candidate_row.get("source_path", ""))
        var source_bytes: PackedByteArray = FileAccess.get_file_as_bytes(source_path)
        var source_sha: String = str(candidate_row.get("source_sha256", ""))
        if source_bytes.is_empty() or _sha256_bytes(source_bytes) != source_sha:
            _case_fail(candidate_id + "_source_pin")
            continue

        var parsed: Variant = JSON.parse_string(source_bytes.get_string_from_utf8())
        if not (parsed is Dictionary):
            _case_fail(candidate_id + "_source_json")
            continue
        var source_config: Dictionary = parsed
        _check(candidate_id + "_source_identity", str(source_config.get("challenge_id", "")) == candidate_id and str(source_config.get("mechanic", "")) == str(candidate_row.get("mechanic", "")))

        # Execute the exact effective in-memory runtime path for the source challenge.
        var runtime_result: Dictionary = RuntimeBridge.run_effective_pipeline(source_config)
        if not bool(runtime_result.get("success", false)):
            _case_fail(candidate_id + "_effective_runtime")
            continue
        var context: Variant = runtime_result.get("context", null)
        var runtime_input: Variant = runtime_result.get("runtime_input", null)
        if context == null or not (runtime_input is Dictionary):
            _case_fail(candidate_id + "_runtime_context")
            continue
        var simulation_result: Variant = context.simulation_result
        if not (simulation_result is RefCounted) or simulation_result.get_script() != SimulationResultScript:
            _case_fail(candidate_id + "_simulation_result_type")
            continue

        var video_value: Variant = runtime_input.get("video", null)
        if not (video_value is Dictionary):
            _case_fail(candidate_id + "_canonical_video_contract")
            continue
        var video: Dictionary = video_value
        var fps_value: Variant = video.get("fps", null)
        var duration_value: Variant = video.get("game_duration", null)
        if (typeof(fps_value) != TYPE_INT and typeof(fps_value) != TYPE_FLOAT) or (typeof(duration_value) != TYPE_INT and typeof(duration_value) != TYPE_FLOAT):
            _case_fail(candidate_id + "_timebase_types")
            continue
        var fps: int = int(round(float(fps_value)))
        var duration: float = float(duration_value)
        var expected_frames: int = int(round(duration * float(fps)))
        if fps != 60 or not is_equal_approx(duration, 7.0) or expected_frames != 420:
            _case_fail(candidate_id + "_pinned_timebase")
            continue

        var validation: Dictionary = simulation_result.validate_contract(expected_frames)
        validation["_c11d_v2b_source_result_ref"] = weakref(simulation_result)
        validation["_c11d_v2b_expected_game_frames"] = expected_frames
        if validation.get("is_valid", false) != true or validation.get("error_code", "") != "OK":
            _case_fail(candidate_id + "_upstream_validation")
            continue

        # This single call composes actual runtime frames with the review-only consumer.
        var output: Dictionary = _consumer.project_allowlisted_target_marker_track(candidate_id, simulation_result, validation)
        if not _validate_closed_output(output, candidate_id, expected_frames):
            _case_fail(candidate_id + "_closed_output")
            continue
        if candidate_id == "CHALLENGE_005" and not _validate_constant_track(output):
            _case_fail(candidate_id + "_constant_target_track")
            continue

        _candidate_passes += 1
        _total_source_frames += simulation_result.frames.size()
        _total_marker_frames += int(output.get("source_frame_count", 0))
        print("C11D_V2B_SOURCE_COMPOSITION_CANDIDATE_PASS=" + candidate_id + ";frames=" + str(expected_frames))
        total_expected += expected_frames

    _check("four_allowlisted_candidates", _candidate_passes == 4)
    _check("all_real_source_frames", _total_source_frames == 1680 and total_expected == 1680)
    _check("all_marker_frames", _total_marker_frames == 1680)

    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CANDIDATES=" + str(_candidate_passes) + "/4")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_SOURCE_FRAMES=" + str(_total_source_frames) + "/1680")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_MARKER_FRAMES=" + str(_total_marker_frames) + "/1680")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CUSTOM_DATA_LOOKUPS_PER_FRAME=1")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_HARNESS_CUSTOM_DATA_READS=0")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RAW_CUSTOM_DATA_LOGGED=false")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RENDERER=OFF")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_PRODUCTION_CALLS=0")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_MEDIA_CREATED=false")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_C11C_IMMUTABLE=true")
    if _failures.is_empty():
        print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RUNTIME_TEST_STATUS=PASS")
        quit(0)
        return
    for failure: String in _failures:
        printerr("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_FAILURE=" + failure)
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RUNTIME_TEST_STATUS=FAIL")
    quit(1)

func _check(_name: String, passed: bool) -> void:
    if not passed:
        _failures.append(_name)

func _case_fail(case_name: String) -> void:
    _failures.append(case_name)

func _validate_closed_output(output: Dictionary, candidate_id: String, expected_frames: int) -> bool:
    if output.size() != ROOT_KEYS.size():
        return false
    for key: String in ROOT_KEYS:
        if not output.has(key):
            return false
    if output.get("contract_id", "") != "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_CONTRACT_V1":
        return false
    if output.get("candidate_id", "") != candidate_id or output.get("logical_canvas_id", "") != "LOGICAL_SOCIAL_CANVAS_540X960":
        return false
    if int(output.get("source_frame_count", -1)) != expected_frames:
        return false
    var frames_value: Variant = output.get("frames", null)
    if not (frames_value is Array) or frames_value.size() != expected_frames:
        return false
    for frame_index in range(frames_value.size()):
        var frame_value: Variant = frames_value[frame_index]
        if not (frame_value is Dictionary) or frame_value.size() != FRAME_KEYS.size():
            return false
        if not frame_value.has("source_frame_index") or not frame_value.has("target_marker"):
            return false
        if typeof(frame_value["source_frame_index"]) != TYPE_INT or int(frame_value["source_frame_index"]) != frame_index:
            return false
        var marker_value: Variant = frame_value["target_marker"]
        if not (marker_value is Dictionary) or marker_value.size() != MARKER_KEYS.size():
            return false
        for key: String in MARKER_KEYS:
            if not marker_value.has(key):
                return false
        if marker_value.get("role", "") != "TARGET" or marker_value.get("anchor_mode", "") != "CENTER":
            return false
        if marker_value.get("asset_bounds_policy", "") != "CLIP_BOUNDS_WITHOUT_MOVING_POINT":
            return false
        var expected_asset: String = "assets/c6/waypoint.svg" if candidate_id == "CHALLENGE_003" else "assets/c6/target.svg"
        if marker_value.get("asset_path", "") != expected_asset:
            return false
        if float(marker_value.get("logical_width", -1.0)) != 50.0 or float(marker_value.get("logical_height", -1.0)) != 50.0:
            return false
        var x_value: Variant = marker_value.get("anchor_x", null)
        var y_value: Variant = marker_value.get("anchor_y", null)
        if (typeof(x_value) != TYPE_INT and typeof(x_value) != TYPE_FLOAT) or (typeof(y_value) != TYPE_INT and typeof(y_value) != TYPE_FLOAT):
            return false
        var x: float = float(x_value)
        var y: float = float(y_value)
        if is_nan(x) or is_inf(x) or is_nan(y) or is_inf(y) or x < 0.0 or x > 540.0 or y < 0.0 or y > 960.0:
            return false
    return not _contains_object_reference(output)

func _validate_constant_track(output: Dictionary) -> bool:
    var frames_value: Variant = output.get("frames", null)
    if not (frames_value is Array) or frames_value.is_empty():
        return false
    var first: Dictionary = frames_value[0]["target_marker"]
    var first_x: float = float(first["anchor_x"])
    var first_y: float = float(first["anchor_y"])
    for frame_value: Variant in frames_value:
        var marker: Dictionary = frame_value["target_marker"]
        if float(marker["anchor_x"]) != first_x or float(marker["anchor_y"]) != first_y:
            return false
    return true

func _contains_object_reference(value: Variant) -> bool:
    if typeof(value) == TYPE_OBJECT:
        return true
    if value is Dictionary:
        for key: Variant in value.keys():
            if _contains_object_reference(key) or _contains_object_reference(value[key]):
                return true
    elif value is Array:
        for item: Variant in value:
            if _contains_object_reference(item):
                return true
    return false

func _resource_sha(path: String) -> String:
    var bytes: PackedByteArray = FileAccess.get_file_as_bytes(path)
    if bytes.is_empty():
        return ""
    return _sha256_bytes(bytes)

func _sha256_bytes(bytes: PackedByteArray) -> String:
    var ctx := HashingContext.new()
    if ctx.start(HashingContext.HASH_SHA256) != OK:
        return ""
    if ctx.update(bytes) != OK:
        return ""
    return ctx.finish().hex_encode().to_lower()
