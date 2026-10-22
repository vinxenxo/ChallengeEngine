extends RefCounted

## Isolated C11-D V2-B review-only consumer. This script has no production call site.
## It returns in-memory logical marker descriptors only; it never loads assets,
## creates Nodes/Resources, serializes custom_data, writes files, or dispatches a renderer.

const SimulationResultScript = preload("res://core/simulation/SimulationResult.gd")
const FrameSnapshotScript = preload("res://core/data/FrameSnapshot.gd")

const CONTRACT_ID: String = "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_CONTRACT_V1"
const LOGICAL_CANVAS_ID: String = "LOGICAL_SOCIAL_CANVAS_540X960"
const OUTPUT_KIND: String = "LOGICAL_TARGET_MARKER_TRACK_SPECIFICATION"
const ASSET_INTRINSIC_SIZE: Vector2 = Vector2(100.0, 100.0)
const LOGICAL_ASSET_SIZE: Vector2 = Vector2(50.0, 50.0)
const CENTER_ANCHOR: String = "CENTER"
const ASSET_BOUNDS_POLICY: String = "CLIP_BOUNDS_WITHOUT_MOVING_POINT"

const FIELD_FOR_CANDIDATE: Dictionary = {
    "CHALLENGE_003": "target_x",
    "CHALLENGE_005": "target_position",
    "CHALLENGE_006": "target_position",
    "CHALLENGE_007": "target_position",
}

const ASSET_FOR_CANDIDATE: Dictionary = {
    "CHALLENGE_003": "assets/c6/waypoint.svg",
    "CHALLENGE_005": "assets/c6/target.svg",
    "CHALLENGE_006": "assets/c6/target.svg",
    "CHALLENGE_007": "assets/c6/target.svg",
}

static func expected_field_for_candidate(candidate_id: Variant) -> String:
    if typeof(candidate_id) != TYPE_STRING:
        return ""
    return str(FIELD_FOR_CANDIDATE.get(candidate_id, ""))

## Testable internal guard for the finite candidate/field contract.
## The public consumer entry point deliberately has no field argument.
static func _candidate_field_pair_failure(candidate_id: Variant, candidate_field: Variant) -> String:
    if typeof(candidate_id) != TYPE_STRING or not FIELD_FOR_CANDIDATE.has(candidate_id):
        return "UNSUPPORTED_CANDIDATE"
    if typeof(candidate_field) != TYPE_STRING:
        return "ALLOWLIST_MISMATCH"
    if str(FIELD_FOR_CANDIDATE[candidate_id]) != str(candidate_field):
        return "ALLOWLIST_MISMATCH"
    return ""

static func _failure(code: String) -> Dictionary:
    return {"ok": false, "error_code": code}

static func _asset_contract_is_valid(candidate_id: String) -> bool:
    if not ASSET_FOR_CANDIDATE.has(candidate_id):
        return false
    var expected_asset := str(ASSET_FOR_CANDIDATE[candidate_id])
    if expected_asset.is_empty():
        return false
    if ASSET_INTRINSIC_SIZE != Vector2(100.0, 100.0):
        return false
    if LOGICAL_ASSET_SIZE != Vector2(50.0, 50.0):
        return false
    if CENTER_ANCHOR != "CENTER" or ASSET_BOUNDS_POLICY != "CLIP_BOUNDS_WITHOUT_MOVING_POINT":
        return false
    return true

static func _is_finite_number(value: float) -> bool:
    return not is_nan(value) and not is_inf(value)

static func _is_finite_vector2(value: Vector2) -> bool:
    return _is_finite_number(value.x) and _is_finite_number(value.y)

static func _make_frame_descriptor(frame_index: int, asset_path: String, anchor_x: float, anchor_y: float) -> Dictionary:
    var marker: Dictionary = {
        "role": "TARGET",
        "asset_path": asset_path,
        "anchor_x": anchor_x,
        "anchor_y": anchor_y,
        "logical_width": LOGICAL_ASSET_SIZE.x,
        "logical_height": LOGICAL_ASSET_SIZE.y,
        "anchor_mode": CENTER_ANCHOR,
        "asset_bounds_policy": ASSET_BOUNDS_POLICY,
    }
    return {
        "source_frame_index": frame_index,
        "target_marker": marker,
    }

## Review-only entry point defined by the accepted design. `upstream_validation`
## is the actual SimulationResult.validate_contract() dictionary with two local
## provenance fields appended by the isolated adapter: a WeakRef to the exact
## SimulationResult and the expected game-frame count. Core simulation files are
## intentionally not changed to manufacture provenance they do not currently expose.
func project_allowlisted_target_marker_track(
    candidate_id: Variant,
    simulation_result: Variant,
    upstream_validation: Variant
) -> Dictionary:
    if typeof(candidate_id) != TYPE_STRING or not FIELD_FOR_CANDIDATE.has(candidate_id):
        return _failure("UNSUPPORTED_CANDIDATE")

    var candidate_key: String = str(candidate_id)
    var field_name: String = str(FIELD_FOR_CANDIDATE[candidate_key])
    var pair_failure := _candidate_field_pair_failure(candidate_key, field_name)
    if not pair_failure.is_empty():
        return _failure(pair_failure)

    if not (simulation_result is RefCounted) or simulation_result.get_script() != SimulationResultScript:
        return _failure("SNAPSHOT_CONTRACT_NOT_VALID")
    if not (upstream_validation is Dictionary):
        return _failure("SNAPSHOT_CONTRACT_NOT_VALID")

    if typeof(upstream_validation.get("is_valid", null)) != TYPE_BOOL or upstream_validation.get("is_valid", false) != true:
        return _failure("SNAPSHOT_CONTRACT_NOT_VALID")
    if typeof(upstream_validation.get("error_code", null)) != TYPE_STRING or upstream_validation.get("error_code", "") != "OK":
        return _failure("SNAPSHOT_CONTRACT_NOT_VALID")

    var source_ref_value: Variant = upstream_validation.get("_c11d_v2b_source_result_ref", null)
    if not (source_ref_value is WeakRef):
        return _failure("SNAPSHOT_CONTRACT_NOT_VALID")
    var source_ref: WeakRef = source_ref_value
    var bound_source: Variant = source_ref.get_ref()
    if bound_source == null or bound_source != simulation_result:
        return _failure("SNAPSHOT_CONTRACT_NOT_VALID")

    var expected_count_value: Variant = upstream_validation.get("_c11d_v2b_expected_game_frames", null)
    if typeof(expected_count_value) != TYPE_INT:
        return _failure("SNAPSHOT_CONTRACT_NOT_VALID")

    var source_frames: Array = simulation_result.frames
    var expected_count: int = int(expected_count_value)
    if expected_count < 0 or expected_count != source_frames.size():
        return _failure("FRAME_CARDINALITY_MISMATCH")
    if source_frames.is_empty():
        return _failure("EMPTY_SOURCE_FRAMES")
    if not _asset_contract_is_valid(candidate_key):
        return _failure("INVALID_ASSET_DIMENSIONS")

    # Unique per invocation. Each source frame gets exactly one get() on exactly
    # its candidate's allowlisted custom_data key. Never use has(), indexing,
    # enumeration, duplicate(), stringify(), logging, or serialization here.
    var missing_sentinel: RefCounted = RefCounted.new()
    var projected_frames: Array = []
    var has_constant_position: bool = false
    var first_constant_position: Vector2 = Vector2.ZERO
    var asset_path: String = str(ASSET_FOR_CANDIDATE[candidate_key])

    for frame_index in range(source_frames.size()):
        var frame_value: Variant = source_frames[frame_index]
        if not (frame_value is RefCounted) or frame_value.get_script() != FrameSnapshotScript:
            return _failure("SNAPSHOT_CONTRACT_NOT_VALID")

        var source_value: Variant = frame_value.custom_data.get(field_name, missing_sentinel)
        if source_value == missing_sentinel:
            return _failure("MISSING_ALLOWLISTED_FIELD")

        var logical_x: float = 0.0
        var logical_y: float = 0.0

        if candidate_key == "CHALLENGE_003":
            var source_type: int = typeof(source_value)
            if source_type != TYPE_INT and source_type != TYPE_FLOAT:
                return _failure("INVALID_VALUE_TYPE")

            var scalar_value: float = float(source_value)
            if not _is_finite_number(scalar_value):
                return _failure("NONFINITE_VALUE")
            if scalar_value < 0.0 or scalar_value > 100.0:
                return _failure("VALUE_OUT_OF_DOMAIN")

            logical_x = (scalar_value / 100.0) * 540.0
            logical_y = 480.0
        else:
            if typeof(source_value) != TYPE_VECTOR2:
                return _failure("INVALID_VALUE_TYPE")

            var source_position: Vector2 = source_value
            if not _is_finite_vector2(source_position):
                return _failure("NONFINITE_VALUE")
            if source_position.x < 0.0 or source_position.x > 1080.0 or source_position.y < 0.0 or source_position.y > 1920.0:
                return _failure("VECTOR_OUT_OF_BOUNDS")

            if candidate_key == "CHALLENGE_005":
                if not has_constant_position:
                    first_constant_position = source_position
                    has_constant_position = true
                elif source_position != first_constant_position:
                    return _failure("PER_RUN_CONSTANT_MISMATCH")

            logical_x = source_position.x * 0.5
            logical_y = source_position.y * 0.5

        projected_frames.append(_make_frame_descriptor(frame_index, asset_path, logical_x, logical_y))

    if projected_frames.size() != source_frames.size() or projected_frames.size() != expected_count:
        return _failure("FRAME_CARDINALITY_MISMATCH")

    # This success shape is intentionally closed and contains no source objects,
    # input values, custom_data, score, close-call metrics, or renderer fields.
    return {
        "contract_id": CONTRACT_ID,
        "candidate_id": candidate_key,
        "logical_canvas_id": LOGICAL_CANVAS_ID,
        "source_frame_count": projected_frames.size(),
        "frames": projected_frames,
    }
