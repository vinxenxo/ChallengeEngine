from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_SCHEMA_V1.json")
CONTRACT_ID = "C11-D-RENDERER-EDITORIAL-FIELD-WINDOW-PROPOSAL-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-EDITORIAL-FIELD-WINDOW-PROPOSAL-V1"
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CHALLENGE_SHA256 = "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
POLICY_ID = "C11D_SAME_NAME_EDITORIAL_FIELD_TO_PHASE_FULL_WINDOW_V1"
EXPECTED_LINEAGE = [
    ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", FROZEN_MANIFEST_SHA256),
    ("challenges/CHALLENGE_004.json", CHALLENGE_SHA256),
    ("profiles/delivery/c11c_video_delivery_profiles.json", "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"),
    ("definitions/c11d/production/D_RENDERER_PROFILE_IDENTITY_SEPARATION_V1.json", "e217d0d94a580747e754be68aba18bcadc4cf954c09d60f97a07e2b9c35fbb77"),
    ("definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json", "602c938cbf8378e8f71aefc6fb46d61496e78f9ab84d595f9efab982a2820a38"),
    ("definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json", "660f20bf39f6c797e5b3f06615e19efe490353c35637effcacd2e7d4acc447fd"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1.json", "ed56660d77de32e288eb3f4106499e94e390785d6d6503c5c028fc3399dd20c5"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_V1.json", "30381dba04a07d6e0ea1d82b186f46b78ab7193ecaa82efe3e484dd5bcd64e22"),
]
PHASES = ["HOOK", "GAME", "REVEAL", "CTA"]
EXPECTED_DELIVERY_SEGMENTS = [
    {"phase": "HOOK", "start_frame": 0, "end_frame": 90, "frame_count": 90},
    {"phase": "GAME", "start_frame": 90, "end_frame": 300, "frame_count": 210},
    {"phase": "REVEAL", "start_frame": 300, "end_frame": 390, "frame_count": 90},
    {"phase": "CTA", "start_frame": 390, "end_frame": 450, "frame_count": 60},
]
EXPECTED_EDITORIAL = {"hook": "¡SOLO EL 1% APARCA SIN ROZAR!", "reveal": "", "cta": "¿Lo has clavado?"}


class EditorialFieldWindowError(ValueError):
    pass


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise EditorialFieldWindowError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EditorialFieldWindowError(f"Expected JSON object at {path}")
    return value


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha_json(value: Any) -> str:
    return _sha_bytes(_canonical(value).encode("utf-8"))


def validate_contract(project_root: Path | str | None = None) -> tuple[dict[str, Any], dict[str, Any], str]:
    root = _root(project_root)
    contract = _read_json(root / CONTRACT_REL)
    schema = _read_json(root / SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise EditorialFieldWindowError("Contract identity/version drift")
    if contract.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
        raise EditorialFieldWindowError("Contract must remain proposal-only")
    if contract.get("supported_content_types") != ["challenges"]:
        raise EditorialFieldWindowError("Supported content-type scope drift")
    if contract.get("mapping_policy", {}).get("policy_id") != POLICY_ID or contract.get("mapping_policy", {}).get("state") != "PROPOSED_NOT_APPROVED":
        raise EditorialFieldWindowError("Field-window policy was changed or promoted")
    expected_mapping_policy = {
        "policy_id": POLICY_ID,
        "state": "PROPOSED_NOT_APPROVED",
        "field_to_phase": [
            {"field_id": "hook", "phase": "HOOK", "condition": "NONEMPTY_CANONICAL_EDITORIAL_VALUE"},
            {"field_id": "reveal", "phase": "REVEAL", "condition": "NONEMPTY_CANONICAL_EDITORIAL_VALUE"},
            {"field_id": "cta", "phase": "CTA", "condition": "NONEMPTY_CANONICAL_EDITORIAL_VALUE"},
        ],
        "visible_window_rule": "ASSIGN_THE_FULL_DELIVERY_PHASE_RANGE_ONLY_AFTER_EXPLICIT_FIELD_TO_PHASE_MAPPING",
        "empty_value_rule": "SUPPRESS_FIELD_AND_ASSIGN_NO_WINDOW",
        "interval_convention": "ZERO_BASED_HALF_OPEN_DELIVERY_FRAME_RANGE",
        "unknown_field_rule": "REJECT_UNTIL_EXPLICIT_MAPPING_IS_ADDED",
        "game_phase_rule": "NO_EDITORIAL_FIELD_ASSIGNED_BY_THIS_V1_POLICY",
        "text_transformations": "NONE_EXACT_SOURCE_STRING_PRESERVED",
        "geometry_and_style": "OUT_OF_SCOPE_NOT_EMITTED",
        "sample_selection_and_interpolation": "OUT_OF_SCOPE_NOT_EMITTED",
    }
    if contract.get("mapping_policy") != expected_mapping_policy:
        raise EditorialFieldWindowError("Field-to-phase mapping policy drifted or was promoted")
    expected_fixture = {
        "challenge_id": "CHALLENGE_004",
        "challenge_source_sha256": CHALLENGE_SHA256,
        "frozen_c11c_manifest_sha256": FROZEN_MANIFEST_SHA256,
        "source_fps": 60,
        "source_total_frames": 900,
        "delivery_profile_id": "REVIEW_720",
        "delivery_fps": 30,
        "delivery_total_frames": 450,
        "delivery_phase_boundaries": [0, 90, 300, 390, 450],
        "editorial_values": EXPECTED_EDITORIAL,
    }
    if contract.get("pinned_fixture") != expected_fixture:
        raise EditorialFieldWindowError("Pinned fixture/source facts drifted")
    expected_lineage = [{"path": p, "sha256": h} for p, h in EXPECTED_LINEAGE]
    if contract.get("source_lineage") != expected_lineage:
        raise EditorialFieldWindowError("Source-lineage pins drifted")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise EditorialFieldWindowError("Schema must be Draft 2020-12")
    expected_output = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "construction": "IN_MEMORY_REVIEW_ONLY",
        "canonicalization": "UTF8_JSON_SORTED_KEYS_COMPACT_NO_NAN",
        "persistent_report": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "media_created": False,
        "c11c_source_mutation": False,
        "video_render_ready": False,
    }
    if contract.get("output_contract") != expected_output:
        raise EditorialFieldWindowError("Output boundary drifted")
    expected_approval = {
        "field_window_policy_approved": False,
        "delivery_timebase_projection_approved": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_17_closure": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
        "release_authority": "NONE",
    }
    if contract.get("approval_state") != expected_approval:
        raise EditorialFieldWindowError("Approval state cannot be promoted by this contract")
    if contract.get("execution_boundary") != {"mode": "IN_MEMORY_REVIEW_ONLY", "renderer": "OFF", "media_created": False, "d4_8": "BLOCKED", "release_authority": "NONE"}:
        raise EditorialFieldWindowError("Execution-boundary declarations drifted")

    # When run from a real project checkout, all pinned sources must exist and match.
    # In an isolated preparation tree, unit tests verify the exact pin declarations and defer file evidence to the Godot harness.
    manifest = root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    if manifest.exists():
        for rel, expected_sha in EXPECTED_LINEAGE:
            path = root / rel
            if not path.is_file():
                raise EditorialFieldWindowError(f"Pinned source missing: {rel}")
            if _sha_bytes(path.read_bytes()) != expected_sha:
                raise EditorialFieldWindowError(f"Pinned source SHA-256 mismatch: {rel}")
        source_status = f"{len(EXPECTED_LINEAGE)}/{len(EXPECTED_LINEAGE)}"
    else:
        source_status = "DEFERRED_TO_GODOT"
    return contract, schema, source_status


def _validate_delivery_segments(segments: Any) -> dict[str, dict[str, int | str]]:
    if not isinstance(segments, list) or len(segments) != 4:
        raise EditorialFieldWindowError("Expected four delivery phase segments")
    by_phase: dict[str, dict[str, int | str]] = {}
    for idx, segment in enumerate(segments):
        if not isinstance(segment, Mapping):
            raise EditorialFieldWindowError("Delivery segments must be objects")
        phase = segment.get("phase")
        if phase != PHASES[idx]:
            raise EditorialFieldWindowError("Delivery phase order/identity mismatch")
        start, end, count = segment.get("start_frame"), segment.get("end_frame"), segment.get("frame_count")
        if any(isinstance(v, bool) or not isinstance(v, int) for v in (start, end, count)):
            raise EditorialFieldWindowError("Frame boundaries/counts must be integers, not booleans")
        if (start, end, count) != tuple(EXPECTED_DELIVERY_SEGMENTS[idx][k] for k in ("start_frame", "end_frame", "frame_count")):
            raise EditorialFieldWindowError(f"Delivery phase range mismatch for {phase}")
        if end - start != count or start < 0 or end <= start:
            raise EditorialFieldWindowError(f"Invalid half-open frame range for {phase}")
        if idx and start != int(segments[idx - 1]["end_frame"]):
            raise EditorialFieldWindowError("Delivery phase segments must be contiguous")
        by_phase[str(phase)] = {"start_frame": start, "end_frame": end, "frame_count": count, "phase": str(phase)}
    if by_phase["HOOK"]["start_frame"] != 0 or by_phase["CTA"]["end_frame"] != 450:
        raise EditorialFieldWindowError("Delivery timeline bounds drifted")
    return by_phase


def build_field_window_proposal(editorial_content: Mapping[str, Any], delivery_segments: Any, content_type: str = "challenges") -> dict[str, Any]:
    if content_type != "challenges":
        raise EditorialFieldWindowError("No editorial field-window mapping is defined for this content type")
    if not isinstance(editorial_content, Mapping):
        raise EditorialFieldWindowError("Editorial content must be an object")
    if set(editorial_content.keys()) != set(EXPECTED_EDITORIAL.keys()):
        raise EditorialFieldWindowError("Editorial fields must be exactly hook, reveal, cta until a versioned mapping declares more")
    by_phase = _validate_delivery_segments(delivery_segments)
    fields: list[dict[str, Any]] = []
    for field_id, phase in (("hook", "HOOK"), ("reveal", "REVEAL"), ("cta", "CTA")):
        value = editorial_content.get(field_id)
        if not isinstance(value, str):
            raise EditorialFieldWindowError(f"Editorial field {field_id} must be a string")
        if value != EXPECTED_EDITORIAL[field_id]:
            raise EditorialFieldWindowError(f"Editorial field {field_id} differs from pinned CHALLENGE_004 canonical copy")
        row: dict[str, Any] = {
            "field_id": field_id,
            "phase": phase,
            "source_text": value,
            "source_text_sha256": _sha_bytes(value.encode("utf-8")),
        }
        if value.strip() == "":
            row.update({"state": "SUPPRESSED_EMPTY_EDITORIAL_FIELD", "visibility_range": None})
        else:
            seg = by_phase[phase]
            row.update({"state": "PROPOSED_VISIBLE_WINDOW", "visibility_range": {
                "start_frame": int(seg["start_frame"]),
                "end_frame": int(seg["end_frame"]),
                "frame_count": int(seg["frame_count"]),
            }})
        fields.append(row)

    source_segments = [
        {"phase": "HOOK", "start_frame": 0, "end_frame": 180, "frame_count": 180},
        {"phase": "GAME", "start_frame": 180, "end_frame": 600, "frame_count": 420},
        {"phase": "REVEAL", "start_frame": 600, "end_frame": 780, "frame_count": 180},
        {"phase": "CTA", "start_frame": 780, "end_frame": 900, "frame_count": 120},
    ]
    report: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FROZEN_MANIFEST_SHA256,
        "challenge_source_sha256": CHALLENGE_SHA256,
        "challenge_id": "CHALLENGE_004",
        "profile_identity": {
            "legacy_video_profile_id": "test_master_11s",
            "source_presentation_profile_id": "social_default_v1",
            "d_presentation_profile_id": "social_default_v1",
            "delivery_profile_id": "REVIEW_720",
        },
        "source_timeline": {"fps": 60, "total_frames": 900, "duration_seconds": 15, "phase_order": list(PHASES), "boundary_frames": [0, 180, 600, 780, 900]},
        "delivery_profile": {"profile_id": "REVIEW_720", "fps": 30, "total_frames": 450, "width": 720, "height": 1280},
        "source_segments": source_segments,
        "delivery_segments": [dict(x) for x in EXPECTED_DELIVERY_SEGMENTS],
        "policy": {
            "policy_id": POLICY_ID,
            "state": "PROPOSED_NOT_APPROVED",
            "interval_convention": "ZERO_BASED_HALF_OPEN_DELIVERY_FRAME_RANGE",
            "visible_window_rule": "ASSIGN_THE_FULL_DELIVERY_PHASE_RANGE_ONLY_AFTER_EXPLICIT_FIELD_TO_PHASE_MAPPING",
            "empty_value_rule": "SUPPRESS_FIELD_AND_ASSIGN_NO_WINDOW",
        },
        "fields": fields,
        "unresolved_content_types": {
            "visual_loops": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED",
            "visual_drills": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED",
        },
        "source_lineage": [{"path": p, "sha256": h} for p, h in EXPECTED_LINEAGE],
        "runtime_evidence": {
            "mode": "PYTHON_CONTRACT_ONLY",
            "runtime_success": None,
            "repeat_deterministic": None,
            "simulation_frame_signature_unchanged": None,
            "winning_frame_unchanged": None,
            "metrics_unchanged": None,
            "game_frame_count": None,
        },
        "identity_evidence": {
            "legacy_runtime_bound_presentation_profile_id": "test_master_11s",
            "d_presentation_render_model_sha256": None,
            "winning_frame_mapping": "NOT_MAPPED_BY_POLICY",
        },
        "execution_boundary": {
            "report_file_written": False,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "media_created": False,
            "c11c_source_mutation": False,
            "output_artifact_path": None,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "video_render_ready": False,
        },
    }
    report["proposal_sha256"] = _sha_json(report)
    return report


def validate_preview(report: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    if not isinstance(report, Mapping):
        raise EditorialFieldWindowError("Preview must be an object")
    candidate = copy.deepcopy(dict(report))
    digest = candidate.pop("proposal_sha256", None)
    if not isinstance(digest, str) or digest != _sha_json(candidate):
        raise EditorialFieldWindowError("Proposal digest mismatch")
    if candidate.get("schema") != OUTPUT_SCHEMA or candidate.get("status") != "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT":
        raise EditorialFieldWindowError("Preview identity/status mismatch")
    if candidate.get("policy", {}).get("state") != "PROPOSED_NOT_APPROVED":
        raise EditorialFieldWindowError("Field window policy was promoted")
    if candidate.get("challenge_id") != "CHALLENGE_004" or candidate.get("delivery_profile", {}) != {"profile_id": "REVIEW_720", "fps": 30, "total_frames": 450, "width": 720, "height": 1280}:
        raise EditorialFieldWindowError("Challenge/delivery identity drift")
    if candidate.get("profile_identity") != {"legacy_video_profile_id": "test_master_11s", "source_presentation_profile_id": "social_default_v1", "d_presentation_profile_id": "social_default_v1", "delivery_profile_id": "REVIEW_720"}:
        raise EditorialFieldWindowError("Presentation and delivery profile identities drift")
    if candidate.get("source_timeline") != {"fps": 60, "total_frames": 900, "duration_seconds": 15, "phase_order": PHASES, "boundary_frames": [0, 180, 600, 780, 900]}:
        # JSON serialization turns tuples/lists uniformly; direct list-valued expected form below is used for strict equality.
        expected_timeline = {"fps": 60, "total_frames": 900, "duration_seconds": 15, "phase_order": list(PHASES), "boundary_frames": [0, 180, 600, 780, 900]}
        if candidate.get("source_timeline") != expected_timeline:
            raise EditorialFieldWindowError("Source timeline identity/boundaries drift")
    expected_source = [
        {"phase": "HOOK", "start_frame": 0, "end_frame": 180, "frame_count": 180},
        {"phase": "GAME", "start_frame": 180, "end_frame": 600, "frame_count": 420},
        {"phase": "REVEAL", "start_frame": 600, "end_frame": 780, "frame_count": 180},
        {"phase": "CTA", "start_frame": 780, "end_frame": 900, "frame_count": 120},
    ]
    if candidate.get("source_segments") != expected_source or candidate.get("delivery_segments") != EXPECTED_DELIVERY_SEGMENTS:
        raise EditorialFieldWindowError("Source/delivery phase ranges drifted")
    fields = candidate.get("fields")
    if not isinstance(fields, list) or [f.get("field_id") for f in fields] != ["hook", "reveal", "cta"]:
        raise EditorialFieldWindowError("Editorial field ordering/identity drift")
    expected_ranges = [(0, 90, 90), None, (390, 450, 60)]
    expected_values = [EXPECTED_EDITORIAL["hook"], EXPECTED_EDITORIAL["reveal"], EXPECTED_EDITORIAL["cta"]]
    for field, expected_range, expected_text in zip(fields, expected_ranges, expected_values, strict=True):
        if field.get("phase") not in {"HOOK", "REVEAL", "CTA"} or field.get("source_text") != expected_text or field.get("source_text_sha256") != _sha_bytes(expected_text.encode("utf-8")):
            raise EditorialFieldWindowError("Editorial source text/hash/phase mismatch")
        actual_range = field.get("visibility_range")
        if expected_range is None:
            if field.get("state") != "SUPPRESSED_EMPTY_EDITORIAL_FIELD" or actual_range is not None:
                raise EditorialFieldWindowError("Empty editorial field must have no visibility window")
        else:
            if field.get("state") != "PROPOSED_VISIBLE_WINDOW" or not isinstance(actual_range, Mapping):
                raise EditorialFieldWindowError("Non-empty field lacks an explicitly proposed visibility window")
            if tuple(actual_range.get(k) for k in ("start_frame", "end_frame", "frame_count")) != expected_range:
                raise EditorialFieldWindowError("Editorial field window does not match proposed phase mapping")
            if actual_range["end_frame"] - actual_range["start_frame"] != actual_range["frame_count"]:
                raise EditorialFieldWindowError("Visibility range is not half-open/cardinality-consistent")
    if candidate.get("unresolved_content_types") != {"visual_loops": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED", "visual_drills": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED"}:
        raise EditorialFieldWindowError("Unsupported content-type coverage was invented")
    runtime = candidate.get("runtime_evidence", {})
    if runtime.get("mode") == "PYTHON_CONTRACT_ONLY":
        if any(runtime.get(k) is not None for k in ("runtime_success", "repeat_deterministic", "simulation_frame_signature_unchanged", "winning_frame_unchanged", "metrics_unchanged", "game_frame_count")):
            raise EditorialFieldWindowError("Python test may not claim Godot runtime evidence")
    elif runtime.get("mode") == "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY":
        if any(runtime.get(k) is not True for k in ("runtime_success", "repeat_deterministic", "simulation_frame_signature_unchanged", "winning_frame_unchanged", "metrics_unchanged")) or runtime.get("game_frame_count") != 420:
            raise EditorialFieldWindowError("Godot runtime invariance evidence failed")
    else:
        raise EditorialFieldWindowError("Unknown runtime evidence mode")
    identity_evidence = candidate.get("identity_evidence", {})
    if identity_evidence.get("winning_frame_mapping") != "NOT_MAPPED_BY_POLICY":
        raise EditorialFieldWindowError("winning_frame must not be mapped into delivery time")
    if identity_evidence.get("d_presentation_render_model_sha256") is not None and (not isinstance(identity_evidence["d_presentation_render_model_sha256"], str) or len(identity_evidence["d_presentation_render_model_sha256"]) != 64):
        raise EditorialFieldWindowError("Invalid presentation render model digest")
    boundary = candidate.get("execution_boundary", {})
    required_false = ("report_file_written", "renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "media_created", "c11c_source_mutation", "video_render_ready")
    if any(boundary.get(k) is not False for k in required_false):
        raise EditorialFieldWindowError("Execution boundary lock was escalated")
    if boundary.get("output_artifact_path", "not-null") is not None or boundary.get("d4_8") != "BLOCKED" or boundary.get("release_authority") != "NONE":
        raise EditorialFieldWindowError("Output path/authority lock was escalated")
    try:
        import jsonschema
        jsonschema.Draft202012Validator(dict(schema)).validate(dict(report))
    except ImportError:
        pass
    except Exception as exc:
        raise EditorialFieldWindowError(f"JSON Schema validation failed: {exc}") from exc


def canonical_json(report: Mapping[str, Any]) -> str:
    return _canonical(report)
