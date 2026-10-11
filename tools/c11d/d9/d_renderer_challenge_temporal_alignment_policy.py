from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_SCHEMA_V1.json")
CONTRACT_SCHEMA = "C11-D-D9-RENDERER-CHALLENGE-TEMPORAL-ALIGNMENT-POLICY-PROPOSAL-V1"
EXPECTED_LINEAGE: tuple[tuple[str, str], ...] = (
    ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"),
    ("challenges/CHALLENGE_004.json", "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"),
    ("profiles/delivery/c11c_video_delivery_profiles.json", "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1.json", "ed56660d77de32e288eb3f4106499e94e390785d6d6503c5c028fc3399dd20c5"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_V1.json", "30381dba04a07d6e0ea1d82b186f46b78ab7193ecaa82efe3e484dd5bcd64e22"),
    ("definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json", "602c938cbf8378e8f71aefc6fb46d61496e78f9ab84d595f9efab982a2820a38"),
    ("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json", "23c33f99f0bef1c76edc6526bcdfa6bf98dc27d7d22b38f48a424008f8f59c5f"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json", "3e278481afe9d66458f05f29c15275819af49f9b68120b6a0b39dda2e9715cf3"),
)

class ChallengeTemporalAlignmentError(ValueError):
    """Raised when the temporal-alignment proposal is inconsistent or unsafe."""


def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    path = root / rel
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ChallengeTemporalAlignmentError(f"Cannot read JSON {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise ChallengeTemporalAlignmentError(f"Expected JSON object at {rel}")
    return value


def project_boundary(source_boundary: int, source_fps: int = 60, delivery_fps: int = 30) -> int:
    for name, value in (("source_boundary", source_boundary), ("source_fps", source_fps), ("delivery_fps", delivery_fps)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ChallengeTemporalAlignmentError(f"{name} must be an integer, not bool or another type")
    if source_boundary < 0 or source_fps <= 0 or delivery_fps <= 0:
        raise ChallengeTemporalAlignmentError("Boundary must be nonnegative and FPS values must be positive")
    if (source_fps, delivery_fps) != (60, 30):
        raise ChallengeTemporalAlignmentError("Unsupported timebase; a separate proposal is required")
    return (2 * source_boundary * delivery_fps + source_fps) // (2 * source_fps)


def _file_sha(root: Path, rel: str) -> str:
    try:
        return hashlib.sha256((root / rel).read_bytes()).hexdigest()
    except Exception as exc:
        raise ChallengeTemporalAlignmentError(f"Cannot hash source {rel}: {exc}") from exc


def load_contract(root: Path, *, verify_source_lineage: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise ChallengeTemporalAlignmentError("Contract identity/version mismatch")
    if contract.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
        raise ChallengeTemporalAlignmentError("Contract status must remain proposal-only")
    lineage = contract.get("source_lineage")
    expected = [{"path": p, "sha256": h} for p, h in EXPECTED_LINEAGE]
    if lineage != expected:
        raise ChallengeTemporalAlignmentError("Source-lineage manifest mismatch")
    if verify_source_lineage:
        for rel, expected_sha in EXPECTED_LINEAGE:
            actual = _file_sha(root, rel)
            if actual != expected_sha:
                raise ChallengeTemporalAlignmentError(f"Source lineage SHA-256 mismatch: {rel}")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ChallengeTemporalAlignmentError("Schema draft identity mismatch")
    _validate_static_facts(contract)
    return contract, schema


def _validate_static_facts(contract: Mapping[str, Any]) -> None:
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise ChallengeTemporalAlignmentError("Contract identity/version mismatch")
    if contract.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
        raise ChallengeTemporalAlignmentError("Contract status must remain proposal-only")
    expected_lineage = [{"path": path, "sha256": digest} for path, digest in EXPECTED_LINEAGE]
    if contract.get("source_lineage") != expected_lineage:
        raise ChallengeTemporalAlignmentError("Source-lineage manifest mismatch")
    policy = contract.get("policy", {})
    fixture = contract.get("fixture", {})
    anchor = contract.get("winning_anchor_reference", {})
    windows = contract.get("editorial_windows_reference", {})
    sample = contract.get("sample_selection_reference", {})
    approvals = contract.get("approval_state", {})
    boundary = contract.get("execution_boundary", {})
    if policy.get("policy_id") != "C11D_CHALLENGE_TEMPORAL_ALIGNMENT_60_TO_30_HALF_OPEN_BOUNDARIES_V1":
        raise ChallengeTemporalAlignmentError("Temporal alignment policy identity mismatch")
    if policy.get("state") != "PROPOSED_NOT_APPROVED":
        raise ChallengeTemporalAlignmentError("Temporal alignment policy was promoted")
    if policy.get("indexing") != "ZERO_BASED" or policy.get("interval_convention") != "HALF_OPEN_START_INCLUSIVE_END_EXCLUSIVE":
        raise ChallengeTemporalAlignmentError("Frame indexing/interval semantics changed")
    projection_policy = policy.get("boundary_projection", {})
    if projection_policy.get("formula") != "floor((2 * source_boundary * delivery_fps + source_fps) / (2 * source_fps))":
        raise ChallengeTemporalAlignmentError("Boundary projection formula changed")
    if projection_policy.get("rounding") != "NEAREST_DELIVERY_TICK_HALF_UP" or projection_policy.get("all_pinned_phase_boundaries_exactly_divisible_by_ratio") is not True:
        raise ChallengeTemporalAlignmentError("Boundary projection rounding/fixture claim changed")
    if policy.get("interpolation_rule") != "NONE; NO_SYNTHETIC_SIMULATION_STATE":
        raise ChallengeTemporalAlignmentError("Interpolation must remain disabled")
    if policy.get("editorial_rule") != "USE_EXPLICIT_FIELD_WINDOW_PROPOSAL; PHASE_NAME_ALONE_NEVER_ASSIGNS_TEXT_VISIBILITY":
        raise ChallengeTemporalAlignmentError("Editorial visibility must remain explicitly mapped")
    if (fixture.get("source_fps"), fixture.get("delivery_fps")) != (60, 30):
        raise ChallengeTemporalAlignmentError("Unsupported pinned timebase")
    if fixture.get("source_boundaries") != [0, 180, 600, 780, 900]:
        raise ChallengeTemporalAlignmentError("Source phase boundaries differ from frozen runtime fixture")
    if fixture.get("source_phase_frame_counts") != [180, 420, 180, 120]:
        raise ChallengeTemporalAlignmentError("Source phase frame-count fixture mismatch")
    if fixture.get("delivery_phase_frame_counts") != [90, 210, 90, 60]:
        raise ChallengeTemporalAlignmentError("Delivery phase frame-count fixture mismatch")
    if fixture.get("delivery_boundaries") != [0, 90, 300, 390, 450]:
        raise ChallengeTemporalAlignmentError("Delivery boundaries differ from the projection proposal")
    if fixture.get("phase_order") != ["HOOK", "GAME", "REVEAL", "CTA"]:
        raise ChallengeTemporalAlignmentError("Pinned phase order mismatch")
    if (fixture.get("source_total_frames"), fixture.get("delivery_fps"), fixture.get("delivery_width"), fixture.get("delivery_height")) != (900, 30, 720, 1280):
        raise ChallengeTemporalAlignmentError("Pinned delivery geometry or timeline mismatch")
    if [project_boundary(v, 60, 30) for v in fixture["source_boundaries"]] != fixture["delivery_boundaries"]:
        raise ChallengeTemporalAlignmentError("Projected phase boundaries do not match expected delivery boundaries")
    phases = contract.get("phase_alignment")
    if [p.get("phase") for p in phases] != fixture.get("phase_order"):
        raise ChallengeTemporalAlignmentError("Phase ordering mismatch")
    for index, phase in enumerate(phases):
        sr, dr = phase.get("source_range"), phase.get("delivery_range")
        if not (isinstance(sr, list) and len(sr) == 2 and isinstance(dr, list) and len(dr) == 2):
            raise ChallengeTemporalAlignmentError("Phase ranges must contain start/end pairs")
        if sr != fixture["source_boundaries"][index:index + 2] or dr != fixture["delivery_boundaries"][index:index + 2]:
            raise ChallengeTemporalAlignmentError(f"Phase range mismatch: {phase.get('phase')}")
        if phase.get("source_frames") != sr[1] - sr[0] or phase.get("delivery_frames") != dr[1] - dr[0]:
            raise ChallengeTemporalAlignmentError(f"Phase frame count mismatch: {phase.get('phase')}")
        if phase["source_frames"] != phase["delivery_frames"] * 2:
            raise ChallengeTemporalAlignmentError(f"Non-2:1 phase cadence: {phase.get('phase')}")
        if index and (phases[index - 1]["source_range"][1] != sr[0] or phases[index - 1]["delivery_range"][1] != dr[0]):
            raise ChallengeTemporalAlignmentError("Phase ranges contain a gap or overlap")
    if phases[-1]["source_range"][1] != fixture["source_total_frames"] or phases[-1]["delivery_range"][1] != sum(fixture["delivery_phase_frame_counts"]):
        raise ChallengeTemporalAlignmentError("Final boundary does not cover the declared timeline")
    if sum(fixture["source_phase_frame_counts"]) != fixture["source_total_frames"]:
        raise ChallengeTemporalAlignmentError("Source phase counts do not sum to timeline total")
    if sum(fixture["delivery_phase_frame_counts"]) != fixture["delivery_boundaries"][-1]:
        raise ChallengeTemporalAlignmentError("Delivery phase counts do not sum to timeline total")
    if fixture.get("duration_seconds") != fixture["source_total_frames"] / fixture["source_fps"] or fixture["delivery_boundaries"][-1] / fixture["delivery_fps"] != fixture["duration_seconds"]:
        raise ChallengeTemporalAlignmentError("Source and delivery duration differ")
    if anchor.get("source_absolute_frame_index") != 574 or anchor.get("source_game_local_index") != 394:
        raise ChallengeTemporalAlignmentError("Winning-frame reference fixture changed")
    if anchor.get("source_absolute_frame_index") != fixture["source_boundaries"][1] + anchor["source_game_local_index"]:
        raise ChallengeTemporalAlignmentError("Winning-frame source/global index relationship mismatch")
    if anchor.get("source_game_local_index") % 2 != 0 or not anchor.get("selected_by_even_local_index_cadence"):
        raise ChallengeTemporalAlignmentError("Winning-frame reference is not on the declared sampling cadence")
    if anchor.get("delivery_game_local_index") != anchor["source_game_local_index"] // 2:
        raise ChallengeTemporalAlignmentError("Winning-frame delivery GAME-local index mismatch")
    if anchor.get("delivery_absolute_frame_index") != fixture["delivery_boundaries"][1] + anchor["delivery_game_local_index"]:
        raise ChallengeTemporalAlignmentError("Winning-frame delivery/global index relationship mismatch")
    if project_boundary(anchor["source_absolute_frame_index"], 60, 30) != anchor["delivery_absolute_frame_index"]:
        raise ChallengeTemporalAlignmentError("Winning-frame time mapping mismatch")
    if anchor.get("winning_frame_mutated") is not False or anchor.get("close_calls_used_for_timing") is not False:
        raise ChallengeTemporalAlignmentError("Simulation truth or close_calls improperly used")
    if anchor.get("close_calls") != 1:
        raise ChallengeTemporalAlignmentError("close_calls fixture mismatch")
    if windows.get("state") != "PROPOSED_NOT_APPROVED" or windows.get("phase_ranges_are_not_implicitly_text_visibility") is not True:
        raise ChallengeTemporalAlignmentError("Editorial windows must remain explicit, unapproved and not inferred from phase names")
    if windows.get("expected_field_ranges") != {"hook": [0, 90], "reveal": None, "cta": [390, 450]}:
        raise ChallengeTemporalAlignmentError("Editorial field-window reference mismatch")
    if sample.get("state") != "PROPOSED_NOT_APPROVED" or sample.get("stride") != 2 or sample.get("interpolation") != "NONE":
        raise ChallengeTemporalAlignmentError("Sample selection policy changed or was promoted")
    if (sample.get("source_game_snapshots"), sample.get("delivery_game_snapshots"), sample.get("selected_local_indices")) != (420, 210, "0,2,4,...,418"):
        raise ChallengeTemporalAlignmentError("Sample-selection fixture changed")
    if sample.get("selection_uses_winning_frame_as_input") is not False or sample.get("selection_uses_close_calls_as_timing") is not False:
        raise ChallengeTemporalAlignmentError("Sample selection depends on runtime truth incorrectly")
    if any(approvals.get(k) is not False for k in (
        "challenge_temporal_alignment_policy_approved", "delivery_timebase_projection_policy_approved",
        "simulation_sample_selection_policy_approved", "interpolation_policy_approved",
        "editorial_field_window_policy_approved", "coordinate_projection_policy_approved",
        "renderer_baseline_approved", "renderer_baseline_frozen", "d4_8_authorized")):
        raise ChallengeTemporalAlignmentError("Approval / renderer / freeze lock is not fail-closed")
    if boundary.get("mode") != "STATIC_POLICY_REVIEW_ONLY":
        raise ChallengeTemporalAlignmentError("Unexpected execution mode")
    required_false = ("c11c_source_mutation", "payload_files_written", "persistent_report_written", "renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_created", "video_render_ready")
    if any(boundary.get(k) is not False for k in required_false):
        raise ChallengeTemporalAlignmentError("Execution boundary was escalated")
    if boundary.get("d4_8") != "BLOCKED" or boundary.get("release_authority") != "NONE":
        raise ChallengeTemporalAlignmentError("Governance lock changed")
    for key in ("d9_14_full_acceptance", "d9_16_full_acceptance"):
        if approvals.get(key) != "BLOCKED_AS_REQUIRED":
            raise ChallengeTemporalAlignmentError(f"Acceptance gate changed: {key}")
    if approvals.get("d9_17_closure") != "BLOCKED_NO_GO" or approvals.get("d10") != "BLOCKED" or approvals.get("release_authority") != "NONE":
        raise ChallengeTemporalAlignmentError("D9 closure / D10 / release lock changed")


def build_preview(root: Path, *, verify_source_lineage: bool = True) -> dict[str, Any]:
    contract, _ = load_contract(root, verify_source_lineage=verify_source_lineage)
    fixture = contract["fixture"]
    boundaries = [project_boundary(v, fixture["source_fps"], fixture["delivery_fps"]) for v in fixture["source_boundaries"]]
    phases = copy.deepcopy(contract["phase_alignment"])
    for i, phase in enumerate(phases):
        phase["computed_delivery_range"] = boundaries[i:i + 2]
        phase["boundary_exact"] = boundaries[i:i + 2] == phase["delivery_range"]
    anchor = copy.deepcopy(contract["winning_anchor_reference"])
    editorial = copy.deepcopy(contract["editorial_windows_reference"])
    sample = copy.deepcopy(contract["sample_selection_reference"])
    preview = {
        "schema": "C11-D-D9-RENDERER-CHALLENGE-TEMPORAL-ALIGNMENT-PREVIEW-V1",
        "schema_version": "1.0",
        "status": "REVIEW_ONLY_PROPOSAL_NOT_RENDERER_INPUT",
        "policy_id": contract["policy"]["policy_id"],
        "policy_state": contract["policy"]["state"],
        "source_timeline": {"fps": fixture["source_fps"], "total_frames": fixture["source_total_frames"], "boundaries": fixture["source_boundaries"], "phase_frames": fixture["source_phase_frame_counts"]},
        "delivery_timeline": {"fps": fixture["delivery_fps"], "total_frames": fixture["delivery_boundaries"][-1], "boundaries": boundaries, "phase_frames": fixture["delivery_phase_frame_counts"], "duration_seconds": fixture["duration_seconds"]},
        "phase_alignment": phases,
        "winning_anchor": anchor,
        "editorial_windows": editorial,
        "sample_selection": sample,
        "summary_facts": {"phase_boundaries_exact": all(p["boundary_exact"] for p in phases), "phase_count": len(phases), "duration_preserved": True, "delivery_candidate_materialized": False, "text_visibility_inferred_from_phase_names": False},
        "approval_state": copy.deepcopy(contract["approval_state"]),
        "execution_boundary": copy.deepcopy(contract["execution_boundary"]),
        "source_lineage": copy.deepcopy(contract["source_lineage"]),
    }
    return preview


def validate_preview(candidate: Mapping[str, Any], root: Path, *, verify_source_lineage: bool = True) -> None:
    if not isinstance(candidate, Mapping):
        raise ChallengeTemporalAlignmentError("Preview must be an object")
    expected = build_preview(root, verify_source_lineage=verify_source_lineage) if not getattr(validate_preview, "_building", False) else None
    if expected is not None and dict(candidate) != expected:
        raise ChallengeTemporalAlignmentError("Temporal alignment preview differs from the canonical proposal")
