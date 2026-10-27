#!/usr/bin/env python3
"""Phase O read-only crosswalk: accepted V2-C source-frame receipts -> semantic binding proposal.

This tool never invokes Godot, writes payloads/media, changes project sources, or approves bindings.
All outputs are written to an explicit TEMP directory outside the repository.
Python standard library only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FROZEN_MANIFEST_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
FROZEN_MANIFEST_BYTES = 796318
EXPECTED_RUNTIME_REPORT_SHA = "7f96c9aec3849212299afbcabe7fd3045fee815807c9cafe555ad8cb947f91f2"
EXPECTED_RUNTIME_STDOUT_SHA = "bacfa68d6cd7f89e2466baac2b28ec0a9b37af4bcd073af9581bd6e05bffd69a"
EXPECTED_TEST_STDOUT_SHA = "6e869618eb36c6f6ee74de8af851b9d3cb5810cfd35df37968176c06f17fb808"
EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
EXPECTED_CHECKPOINT_SHA = "9cccc148927a950a14f76a9e7afb13c1e0d8b8fa1f3ac556a7f01c7244985f2d"
EXPECTED_LEDGER_SHA = "7f44a13f633bd8847cfc60f24d635df6dfe17fb8024af38b8bf2404b68d2fa28"
EXPECTED_ACCEPTANCE_RECORD_SHA = "a0faf6e6ddf145b69b649de45366bfadf0947c7b55a78444c4d546fe3efdeb96"

PINNED_FILES = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": FROZEN_MANIFEST_SHA,
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json": "6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RECEIPT_SCHEMA_V1.json": "90f14fb8c68317f6cea2e473b775b044e69249a1fa4a4776905a140efed6f547",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_REPORT_SCHEMA_V1.json": "0f75fac465130fed3ea54099d296ad79b0d044cbf11ec37dd1540a09c139d57d",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json": "d37cb74f360e19e664b94673bbf4b95462cad6e681a08215a95f4565c6e810aa",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_SCHEMA_V1.json": "f017a8a0081cc42f08af6381e7d47accb7a522ce89301ab9724d003a51c2dcf7",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_REPORT_SCHEMA_V1.json": "57fc91fd8ee19a0f511692ef24e802c8df9c88e8eee73a7f30d14b3d5e3d7051",
    "definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_V1.json": "de44f159c95f31d034fe8356f650b5be320cb5fb1555197073d07875cf0cf1f9",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_V1.json": "3b4375957da12d16a6c7f652c1ba2536ce1a819b781b68b15e5dd3f0ee4bda75",
    "definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json": "e008217bd57303b638e13329d21e5ae56ee3b4efef790566e3702c89ee41a83f",
}
CHALLENGE_IDS = [f"CHALLENGE_{i:03d}" for i in range(1, 10)]
BASE_FIELDS = ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"]
EXPECTED_BASE_SHAPES = {
    "position": "Vector2", "rotation": "float", "scale": "Vector2",
    "opacity": "float", "texture_index": "int", "variant_id": "int",
}
EXPECTED_PROJECTION_FIELDS = ["position.x", "position.y", "rotation", "scale.x", "scale.y", "opacity", "texture_index", "variant_id"]
EXPECTED_CUSTOM_FIELDS = {
    "CHALLENGE_003": "target_x",
    "CHALLENGE_005": "target_position",
    "CHALLENGE_006": "target_position",
    "CHALLENGE_007": "target_position",
    "CHALLENGE_008": "active_selection",
    "CHALLENGE_009": "displayed_count",
}
EXPECTED_TIMEBASE_CONFLICTS = {"CHALLENGE_008", "CHALLENGE_009"}
GOVERNANCE_LOCKS = {
    "renderer": "OFF", "media_created": False, "payload_materialized": False,
    "candidate_input_admissible": False, "seed_domains_complete_for_candidate_input": False,
    "automatic_seed_generation": False, "master_seed": "NOT_ADOPTED",
    "D4.8": "BLOCKED", "D9.10": "PREPARE_ONLY", "D9.14": "BLOCKED",
    "D9.16": "BLOCKED", "D9.17": "BLOCKED_NO_GO", "D10": "BLOCKED_FOR_PROMOTION",
    "baseline_approval": "MISSING", "freeze_eligible": False, "release_authority": "NONE",
}
SIDECAR_FIELDS_BY_TYPE = {
    "challenges": ["title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"],
    "visual_loops": ["title", "subtitle", "call_to_action", "language"],
    "visual_drills": ["title", "subtitle", "call_to_action", "language"],
}


class AuditError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    if not path.is_file():
        raise AuditError(f"Required file missing: {path}")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_json_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def read_json(path: Path) -> Any:
    if not path.is_file():
        raise AuditError(f"Required JSON missing: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuditError(f"Cannot read JSON {path}: {exc}") from exc


def resolve_repo_path(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise AuditError(f"Unsafe repository path in contract: {relative}")
    result = (root / rel).resolve()
    root_resolved = root.resolve()
    try:
        result.relative_to(root_resolved)
    except ValueError as exc:
        raise AuditError(f"Path escapes repository: {relative}") from exc
    return result


def get_dotted(value: Any, dotted: str) -> tuple[bool, Any]:
    current = value
    for part in dotted.split(".") if dotted else []:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


def value_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        if not value:
            return "array[empty]"
        types = sorted({value_type(item) for item in value})
        return "array[" + ",".join(types) + "]"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def without_process(receipt: dict[str, Any]) -> dict[str, Any]:
    """Return receipt fields that should be identical across isolated process repeats."""
    return {key: value for key, value in receipt.items() if key != "process"}


def receipt_diff_keys(a: dict[str, Any], b: dict[str, Any]) -> list[str]:
    keys = sorted(set(a) | set(b))
    return [key for key in keys if a.get(key) != b.get(key)]


def classify_temporal_field(name: str) -> dict[str, Any]:
    if name == "winning_frame":
        return {
            "field": name, "category": "temporal_anchor",
            "runtime_receipt_serialized": False,
            "policy": "SOLE_CHALLENGE_TEMPORAL_TRUTH; NEVER_BIND_AS_VISUAL_STATE",
            "interpretation": "Temporal anchor only; this crosswalk does not infer or serialize its value.",
            "binding_approved": False,
        }
    if name == "close_calls":
        return {
            "field": name, "category": "episode_counter",
            "runtime_receipt_serialized": False,
            "policy": "COUNT_ONLY; NEVER_INTERPRET_AS_FRAME_OR_DURATION",
            "interpretation": "Episode counter only; not a winning frame, duration, or visual state.",
            "binding_approved": False,
        }
    raise ValueError(name)


def analyze_candidate_observation(field_name: str, obs_a: dict[str, Any], obs_b: dict[str, Any]) -> dict[str, Any]:
    a = obs_a.get(field_name)
    b = obs_b.get(field_name)
    if a is None and b is None:
        category, status = "absent", "NOT_OBSERVED_IN_EITHER_RECEIPT"
        agreement = True
    elif a is not None and b is not None:
        agreement = a == b
        category = "custom_data_candidate"
        status = "PRESENCE_AND_TYPE_ONLY_VALUES_NOT_SERIALIZED" if agreement else "REPEAT_OBSERVATION_MISMATCH"
    else:
        agreement = False
        category, status = "unresolved", "PRESENT_IN_ONLY_ONE_RECEIPT"
    return {
        "field": field_name, "category": category, "status": status,
        "repeat_presence_and_type_agreement": agreement,
        "run1_observation": a, "run2_observation": b,
        "actual_custom_data_values_serialized": False,
        "binding_approved": False,
        "evidence_limit": "Receipt records present-frame counts and type histogram only, not per-frame values or visual consumption.",
    }


def audit_main(root: Path, runtime_marker_path: Path, acceptance_marker_path: Path, output_dir: Path) -> dict[str, Any]:
    root = root.resolve()
    temp_root = Path(os.environ.get("TEMP", os.environ.get("TMP", str(Path.home() / "AppData" / "Local" / "Temp")))).resolve()
    output_dir = output_dir.resolve()
    try:
        output_dir.relative_to(temp_root)
    except ValueError as exc:
        raise AuditError(f"Output directory must be under TEMP and outside repository: {output_dir}") from exc
    try:
        output_dir.relative_to(root)
        raise AuditError("Refusing to write audit outputs inside the repository.")
    except ValueError:
        pass
    if output_dir.exists() and any(output_dir.iterdir()):
        raise AuditError(f"Output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    actual_pins: dict[str, str] = {}
    for rel, expected in PINNED_FILES.items():
        path = resolve_repo_path(root, rel)
        actual = sha256_file(path)
        actual_pins[rel] = actual
        if actual != expected:
            raise AuditError(f"Source pin mismatch: {rel}; observed={actual}; expected={expected}")
    manifest_path = resolve_repo_path(root, "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    if manifest_path.stat().st_size != FROZEN_MANIFEST_BYTES:
        raise AuditError("Frozen C11-C manifest byte count mismatch.")

    checkpoint_rel = "docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md"
    ledger_rel = "docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md"
    acceptance_record_rel = "docs/current/d/C11D_V2C_SOURCE_FRAME_RUNTIME_ACCEPTANCE_20261027_V1.md"
    doc_pins = {
        checkpoint_rel: EXPECTED_CHECKPOINT_SHA,
        ledger_rel: EXPECTED_LEDGER_SHA,
        acceptance_record_rel: EXPECTED_ACCEPTANCE_RECORD_SHA,
    }
    for rel, expected in doc_pins.items():
        actual = sha256_file(resolve_repo_path(root, rel))
        actual_pins[rel] = actual
        if actual != expected:
            raise AuditError(f"Phase N acceptance source pin changed: {rel}; observed={actual}; expected={expected}")

    runtime_marker = read_json(runtime_marker_path)
    acceptance_marker = read_json(acceptance_marker_path)
    if runtime_marker.get("schema") != "C11D-V2C-SOURCE-FRAME-RUNTIME-COMPLETION-V1":
        raise AuditError("Unexpected Phase N runtime completion marker schema.")
    required_runtime_marker = {
        "run_id": "994e039b597b496094eb72bf0ae145c5",
        "test_result": "PASS_28_OF_28",
        "runtime_status": "PASS_SOURCE_FRAME_ROUTE_ONLY",
        "runtime_report_sha256": EXPECTED_RUNTIME_REPORT_SHA,
        "test_stdout_sha256": EXPECTED_TEST_STDOUT_SHA,
        "test_stderr_sha256": EMPTY_SHA,
        "runtime_stdout_sha256": EXPECTED_RUNTIME_STDOUT_SHA,
        "runtime_stderr_sha256": EMPTY_SHA,
        "source_pin_count": 81,
        "planner_invocations": "9/9",
        "godot_version_probe_invocations": 1,
        "godot_runtime_process_invocations": "18/18",
        "accepted_selectors": "9/9",
        "process_evidence_files_verified": "36/36",
        "frozen_c11c_manifest": "UNCHANGED",
        "renderer": "OFF", "media_created": False, "payload_materialized": False,
        "candidate_input_admissible": False, "D4_8": "BLOCKED", "release_authority": "NONE",
    }
    for key, expected in required_runtime_marker.items():
        if runtime_marker.get(key) != expected:
            raise AuditError(f"Phase N runtime marker mismatch: {key}; observed={runtime_marker.get(key)!r}; expected={expected!r}")
    if acceptance_marker.get("schema") != "C11D-V2C-SOURCE-FRAME-RUNTIME-ACCEPTANCE-COMPLETION-V1":
        raise AuditError("Unexpected Phase N acceptance completion marker schema.")
    required_acceptance = {
        "status": "PASS_SOURCE_FRAME_ROUTE_ONLY", "test_result": "28/28",
        "source_pins": "81/81", "planner_invocations": "9/9", "godot_runtime_processes": "18/18",
        "selectors": "9/9", "process_evidence_files": "36/36",
        "report_sha256": EXPECTED_RUNTIME_REPORT_SHA, "stdout_sha256": EXPECTED_RUNTIME_STDOUT_SHA,
        "stderr_sha256": EMPTY_SHA, "checkpoint_sha256": EXPECTED_CHECKPOINT_SHA,
        "ledger_sha256": EXPECTED_LEDGER_SHA, "acceptance_record_sha256": EXPECTED_ACCEPTANCE_RECORD_SHA,
        "frozen_c11c_manifest": "UNCHANGED", "renderer": "OFF", "media_created": False,
        "payload_materialized": False, "candidate_input_admissible": False,
        "D4_8": "BLOCKED", "release_authority": "NONE",
    }
    for key, expected in required_acceptance.items():
        if acceptance_marker.get(key) != expected:
            raise AuditError(f"Phase N acceptance marker mismatch: {key}; observed={acceptance_marker.get(key)!r}; expected={expected!r}")

    report_path = Path(str(runtime_marker.get("runtime_report_path", ""))).resolve()
    accepted_report_path = Path(str(acceptance_marker.get("report_path", ""))).resolve()
    if report_path != accepted_report_path:
        raise AuditError("Runtime and acceptance markers reference different report paths.")
    if sha256_file(report_path) != EXPECTED_RUNTIME_REPORT_SHA:
        raise AuditError("Runtime report file SHA does not match Phase N acceptance.")
    report = read_json(report_path)
    if report.get("status") != "PASS_SOURCE_FRAME_ROUTE_ONLY" or report.get("schema") != "C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-REPORT-V1":
        raise AuditError("Runtime report schema/status is not accepted source-frame route-only.")
    if (report.get("source_pin_count") != 81 or report.get("planner_invocations") != 9 or
            report.get("godot_runtime_process_invocations") != 18 or report.get("selector_count_expected") != 9 or
            report.get("approved_bindings") != 0 or report.get("visual_seed_sensitivity") != "NOT_TESTED" or
            report.get("payload_materialized") is not False or report.get("media_created") is not False or
            report.get("frozen_manifest_sha256") != FROZEN_MANIFEST_SHA):
        raise AuditError("Runtime report summary disagrees with accepted Phase N values.")

    report_gov = report.get("governance_locks", {})
    expected_report_governance = {
        "renderer": "OFF", "media_created": False, "candidate_input_admissible": False,
        "seed_domains_complete_for_candidate_input": False, "automatic_seed_generation": False,
        "master_seed": "NOT_ADOPTED", "D4.8": "BLOCKED", "D9.10": "PREPARE_ONLY",
        "D9.14": "BLOCKED", "D9.16": "BLOCKED", "D9.17": "BLOCKED_NO_GO",
        "D10": "BLOCKED_FOR_PROMOTION", "baseline_approval": "MISSING",
        "freeze_eligible": False, "release_authority": "NONE",
        "challenge_visual_seed_sensitivity": "NOT_TESTED",
    }
    for key, expected in expected_report_governance.items():
        if report_gov.get(key) != expected:
            raise AuditError(f"Runtime report governance lock mismatch: {key}")

    proposal_path = resolve_repo_path(root, "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json")
    proposal = read_json(proposal_path)
    if proposal.get("schema") != "C11-D-RENDERER-CHALLENGE-VISUAL-PAYLOAD-SEMANTIC-BINDING-PROPOSAL-CONTRACT-V1" or proposal.get("schema_version") != "1.0" or proposal.get("status") != "PREPARATION_ONLY_PROPOSAL_NOT_APPROVED_NOT_RUNTIME_ACCEPTANCE":
        raise AuditError("Semantic binding proposal is not in expected preparation-only state.")
    semantics = proposal.get("selector_semantics")
    if not isinstance(semantics, list) or len(semantics) != 9:
        raise AuditError("Proposal does not define exactly nine selectors.")
    sem_by_id = {item.get("challenge_id"): item for item in semantics}
    if list(item.get("challenge_id") for item in semantics) != CHALLENGE_IDS or set(sem_by_id) != set(CHALLENGE_IDS):
        raise AuditError("Proposal selectors are missing, duplicated, or out of canonical order.")
    if proposal.get("scope", {}).get("approved_custom_data_bindings") != 0 or proposal.get("scope", {}).get("approved_renderer_projection_bindings") != 0:
        raise AuditError("Proposal scope unexpectedly reports approvals.")

    carrier_path = resolve_repo_path(root, "definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_V1.json")
    carrier = read_json(carrier_path)
    if carrier.get("status") != "PREPARATION_ONLY_HASH_BOUND_EDITORIAL_SIDECAR_NOT_VISUAL_CONSUMPTION":
        raise AuditError("Editorial carrier has an unexpected approval/consumption status.")
    if carrier.get("approval_state", {}).get("editorial_values_visually_consumed") is not False or carrier.get("candidate_input_admissible") is not False:
        raise AuditError("Editorial carrier claims visual consumption/admissibility unexpectedly.")
    supported_fields = carrier.get("supported_fields_by_content_type", {})
    if supported_fields != SIDECAR_FIELDS_BY_TYPE:
        raise AuditError("Editorial sidecar field set differs from the pinned field inventory.")

    expected_receipt_schema = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-RECEIPT-V1"
    report_selectors = report.get("selectors")
    if not isinstance(report_selectors, list) or len(report_selectors) != 9:
        raise AuditError("Runtime report does not have nine selector rows.")
    actual_selector_ids = [item.get("selector", {}).get("challenge_id") for item in report_selectors]
    if actual_selector_ids != CHALLENGE_IDS:
        raise AuditError("Runtime report selector ordering/identity does not match Challenge_001..009.")

    evidence_dir = Path(str(runtime_marker.get("evidence_directory", ""))).resolve()
    log_dir = Path(str(runtime_marker.get("log_directory", ""))).resolve()
    for directory in (evidence_dir, log_dir):
        try:
            directory.relative_to(temp_root)
        except ValueError as exc:
            raise AuditError(f"Phase N evidence/log directory is outside TEMP: {directory}") from exc
    if Path(str(report.get("evidence", {}).get("directory", ""))).resolve() != evidence_dir:
        raise AuditError("Runtime report evidence directory does not match Phase N marker.")
    evidence_map = report.get("evidence", {}).get("evidence_file_sha256")
    if not isinstance(evidence_map, dict) or len(evidence_map) != 36:
        raise AuditError("Runtime report evidence hash map must contain exactly 36 files.")
    evidence_verified: dict[str, str] = {}
    for name, expected_hash in evidence_map.items():
        if Path(name).name != name or name in {".", ".."}:
            raise AuditError(f"Unsafe evidence filename in report: {name}")
        path = evidence_dir / name
        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            raise AuditError(f"Evidence file hash mismatch: {name}; observed={actual_hash}; expected={expected_hash}")
        evidence_verified[name] = actual_hash

    proposal_crosswalk = []
    field_rows = []
    selector_summaries = []
    seen_run_ids: set[str] = set()
    seen_pids: set[int] = set()
    asset_pins_verified: dict[str, str] = {}
    time_conflicts: list[dict[str, Any]] = []
    custom_field_occurrences = 0
    custom_field_stable = 0
    static_pointers_present = 0
    static_pointer_count = 0
    base_field_rows = 0
    receipt_count = 0

    for selector_row in report_selectors:
        challenge_id = selector_row["selector"]["challenge_id"]
        semantics_row = sem_by_id[challenge_id]
        challenge_source_path = resolve_repo_path(root, str(semantics_row.get("challenge_source_path", "")))
        mechanic_source_path = resolve_repo_path(root, str(semantics_row.get("mechanic_source_path", "")))
        challenge_source_actual_sha = sha256_file(challenge_source_path)
        mechanic_source_actual_sha = sha256_file(mechanic_source_path)
        if challenge_source_actual_sha != semantics_row.get("challenge_source_sha256"):
            raise AuditError(f"Challenge source pin mismatch: {challenge_id}")
        if mechanic_source_actual_sha != semantics_row.get("mechanic_source_sha256"):
            raise AuditError(f"Mechanic source pin mismatch: {challenge_id}")
        actual_pins[str(semantics_row["challenge_source_path"])] = challenge_source_actual_sha
        actual_pins[str(semantics_row["mechanic_source_path"])] = mechanic_source_actual_sha
        if selector_row.get("status") != "ACCEPTED_SOURCE_FRAME_ONLY" or selector_row.get("repeat_agreement") is not True or selector_row.get("block_reasons") != []:
            raise AuditError(f"Selector row is not accepted/repeat-agreed: {challenge_id}")
        runs = selector_row.get("runtime_runs")
        if not isinstance(runs, list) or len(runs) != 2:
            raise AuditError(f"Selector must have exactly two runtime runs: {challenge_id}")
        runs_by_id = {str(item.get("run_id")): item for item in runs}
        expected_run_ids = [f"{challenge_id}_R1", f"{challenge_id}_R2"]
        if list(str(item.get("run_id")) for item in runs) != expected_run_ids:
            raise AuditError(f"Runtime runs not in exact expected R1/R2 order: {challenge_id}")
        receipts: list[dict[str, Any]] = []
        receipt_hashes: list[str] = []
        for run in runs:
            run_id = str(run.get("run_id"))
            pid = int(run.get("process_id", -1))
            if run_id in seen_run_ids or pid <= 0 or pid in seen_pids or int(run.get("exit_code", -1)) != 0:
                raise AuditError(f"Duplicate/invalid runtime process receipt: {run_id}")
            seen_run_ids.add(run_id); seen_pids.add(pid)
            receipt = run.get("receipt")
            if not isinstance(receipt, dict) or receipt.get("schema") != expected_receipt_schema or receipt.get("status") != "SOURCE_FRAME_RECEIPT":
                raise AuditError(f"Invalid source-frame receipt: {run_id}")
            if receipt.get("process", {}).get("run_id") != run_id or receipt.get("process", {}).get("process_id") != pid or receipt.get("process", {}).get("exit_code") != 0:
                raise AuditError(f"Receipt process identity mismatch: {run_id}")
            receipt_sha = canonical_json_sha256(receipt)
            if receipt_sha != run.get("receipt_sha256"):
                raise AuditError(f"Canonical receipt hash mismatch: {run_id}")
            if receipt.get("selector", {}).get("challenge_id") != challenge_id or receipt.get("selector", {}).get("mechanic") != semantics_row.get("mechanic"):
                raise AuditError(f"Receipt selector/mechanic mismatch: {run_id}")
            if "winning_frame" in receipt or "close_calls" in receipt or any(name in receipt.get("candidate_field_observations", {}) for name in ("winning_frame", "close_calls")):
                raise AuditError(f"Forbidden temporal/episode fields appeared in visual receipt: {run_id}")
            if receipt.get("semantic_binding_state") != {"approved_bindings": 0, "approved_custom_data_bindings": 0, "custom_data_values_serialized": False}:
                raise AuditError(f"Semantic binding state is not locked at zero: {run_id}")
            side_effects = receipt.get("side_effects", {})
            for side_effect_key in ("payload_file_written", "media_created", "renderer_native_input_emitted", "render_nodes_created", "rendering_server_called", "viewport_captured", "canonical_state_mutated", "production_dispatched"):
                if side_effects.get(side_effect_key) is not False:
                    raise AuditError(f"Unexpected side effect {side_effect_key} in {run_id}")
            route = receipt.get("route", {})
            if route.get("runtime_bridge_method") != "ChallengeRuntimeBridge.run_effective_pipeline" or route.get("renderer") != "OFF" or route.get("release_authority") != "NONE":
                raise AuditError(f"Runtime route/governance mismatch in {run_id}")
            lineage = receipt.get("lineage", {})
            if lineage.get("verified_source_pin_count") != 81 or lineage.get("frozen_manifest_sha256") != FROZEN_MANIFEST_SHA:
                raise AuditError(f"Receipt lineage/pin count mismatch in {run_id}")
            proposal_source_sha = semantics_row.get("challenge_source_sha256")
            proposal_mechanic_sha = semantics_row.get("mechanic_source_sha256")
            if lineage.get("challenge_source_sha256") != proposal_source_sha or lineage.get("mechanic_source_sha256") != proposal_mechanic_sha:
                raise AuditError(f"Receipt lineage does not match proposal source pins: {run_id}")
            file_out = f"{run_id}.out"; file_err = f"{run_id}.err"
            if evidence_map.get(file_out) != run.get("stdout_sha256") or evidence_map.get(file_err) != run.get("stderr_sha256"):
                raise AuditError(f"Run stdout/stderr hashes disagree with evidence map: {run_id}")
            receipts.append(receipt); receipt_hashes.append(receipt_sha); receipt_count += 1
            for asset_entry in receipt.get("source_asset_pins", {}).values():
                source_key = str(asset_entry.get("source_key", ""))
                source_sha = str(asset_entry.get("sha256", ""))
                if not source_key or not re.fullmatch(r"[0-9a-f]{64}", source_sha):
                    raise AuditError(f"Malformed source asset pin: {run_id}")
                source_path = resolve_repo_path(root, source_key)
                actual_asset_sha = sha256_file(source_path)
                if actual_asset_sha != source_sha:
                    raise AuditError(f"Asset source pin mismatch: {source_key}")
                previous = asset_pins_verified.setdefault(source_key, actual_asset_sha)
                if previous != actual_asset_sha:
                    raise AuditError(f"Asset pin drift across receipts: {source_key}")

        rec_a, rec_b = receipts
        differences = receipt_diff_keys(without_process(rec_a), without_process(rec_b))
        if differences:
            raise AuditError(f"Unexplained non-process receipt differences for {challenge_id}: {differences}")
        if rec_a.get("source_frames") != rec_b.get("source_frames"):
            raise AuditError(f"Source-frame projection metadata differs across repeats: {challenge_id}")
        shape_map = {}
        for item in rec_a.get("source_frames", {}).get("frame_shape", []):
            if not isinstance(item, str) or ":" not in item:
                raise AuditError(f"Invalid frame shape metadata in {challenge_id}: {item!r}")
            field, typ = item.split(":", 1)
            shape_map[field] = typ
        if shape_map != EXPECTED_BASE_SHAPES:
            raise AuditError(f"Base frame shape does not match contract for {challenge_id}: {shape_map}")
        source_frame_meta = rec_a.get("source_frames", {})
        if (source_frame_meta.get("projection_fields") != EXPECTED_PROJECTION_FIELDS or
                source_frame_meta.get("count") != source_frame_meta.get("expected_game_frames") or
                source_frame_meta.get("source_fps") != 60 or
                source_frame_meta.get("finite_transform_frames") != source_frame_meta.get("count") or
                source_frame_meta.get("game_duration_seconds") != source_frame_meta.get("count") / 60):
            raise AuditError(f"Source-frame counts/rate/projection metadata not self-consistent for {challenge_id}")
        for field in BASE_FIELDS:
            row = {
                "challenge_id": challenge_id, "field": field, "category": "safe_state",
                "source_pointer": f"SimulationResult.frames[*]/FrameSnapshot.{field}",
                "observed_shape": shape_map[field],
                "evidence_status": "FRAME_SHAPE_AND_PROJECTION_HASH_ONLY_VALUES_NOT_SERIALIZED",
                "stable_between_repeats": True,
                "binding_approved": False, "renderer_projection_approved": False,
            }
            field_rows.append(row); base_field_rows += 1

        proposal_base = semantics_row.get("base_track", {})
        if proposal_base.get("fields") != BASE_FIELDS or proposal_base.get("status") != "EXISTING_V1_REVIEW_ONLY_FIELD_SHAPE_NOT_RENDERER_APPROVED":
            raise AuditError(f"Proposal base track scope/status changed for {challenge_id}")
        sec = semantics_row.get("secondary_binding_proposal", {})
        if sec.get("binding_authorized") is not False or sec.get("renderer_projection_approved") is not False or sec.get("proposal_status") != "PROPOSAL_ONLY_NOT_APPROVED":
            raise AuditError(f"Secondary binding proposal unexpectedly approved for {challenge_id}")
        candidate_field = sec.get("candidate_custom_data_field")
        expected_candidate_field = EXPECTED_CUSTOM_FIELDS.get(challenge_id)
        if candidate_field != expected_candidate_field:
            raise AuditError(f"Selector-specific custom_data candidate differs from pinned expected allowlist: {challenge_id}")
        candidate_a = rec_a.get("candidate_field_observations", {})
        candidate_b = rec_b.get("candidate_field_observations", {})
        secondary_row: dict[str, Any]
        if candidate_field:
            custom_field_occurrences += 1
            secondary_row = analyze_candidate_observation(str(candidate_field), candidate_a, candidate_b)
            if secondary_row["category"] != "custom_data_candidate" or not secondary_row["repeat_presence_and_type_agreement"]:
                raise AuditError(f"Proposal custom_data candidate lacks stable presence/type evidence: {challenge_id}.{candidate_field}")
            custom_field_stable += 1
            if secondary_row["run1_observation"].get("present_frames") != rec_a["source_frames"].get("count") or secondary_row["run2_observation"].get("present_frames") != rec_b["source_frames"].get("count"):
                raise AuditError(f"Custom field is not present across expected source frames: {challenge_id}.{candidate_field}")
            expected_histogram = {str(sec.get("semantic_type")): rec_a["source_frames"]["count"]}
            if secondary_row["run1_observation"].get("type_histogram") != expected_histogram or secondary_row["run2_observation"].get("type_histogram") != expected_histogram:
                raise AuditError(f"Custom field type histogram does not match proposed semantic type: {challenge_id}.{candidate_field}")
            field_rows.append({"challenge_id": challenge_id, "field": str(candidate_field), "category": "custom_data_candidate", "source_pointer": sec.get("source_pointer"), "semantic_type": sec.get("semantic_type"), "run1_observation": secondary_row["run1_observation"], "run2_observation": secondary_row["run2_observation"], "evidence_status": secondary_row["status"], "stable_between_repeats": True, "actual_values_serialized": False, "binding_approved": False, "renderer_projection_approved": False})
        else:
            pointer = str(sec.get("source_pointer", ""))
            if pointer.startswith("FrameSnapshot.") or pointer.startswith("SimulationResult."):
                secondary_row = {"category": "unresolved", "status": "STATIC_POINTER_NOT_IN_PROPOSAL_EXPECTED_FORM"}
                exists, value = False, None
            else:
                source_path = str(semantics_row.get("challenge_source_path", ""))
                actual_source = resolve_repo_path(root, source_path)
                actual_source_sha = sha256_file(actual_source)
                if actual_source_sha != semantics_row.get("challenge_source_sha256"):
                    raise AuditError(f"Challenge source hash mismatch: {challenge_id}")
                challenge_config = read_json(actual_source)
                exists, value = get_dotted(challenge_config, pointer)
                static_pointer_count += 1
                if exists:
                    static_pointers_present += 1
                    if sec.get("semantic_type") == "Vector2" and not (isinstance(value, list) and len(value) == 2 and all(isinstance(item, (int, float)) and not isinstance(item, bool) for item in value)):
                        raise AuditError(f"Static Vector2 source pointer has invalid source shape: {challenge_id}.{pointer}")
                secondary_row = {
                    "category": "unresolved", "status": "SOURCE_POINTER_PRESENT_PROPOSAL_ONLY_NOT_SOURCE_FRAME_OBSERVATION" if exists else "SOURCE_POINTER_ABSENT_UNRESOLVED",
                    "source_path": source_path, "source_sha256": actual_source_sha,
                    "value_type": value_type(value) if exists else None,
                    "value_sha256": canonical_json_sha256(value) if exists else None,
                    "source_value_included": False,
                }
            if exists:
                secondary_row.update({"source_pointer": pointer, "semantic_type": sec.get("semantic_type"), "binding_approved": False, "renderer_projection_approved": False})
            else:
                secondary_row.update({"source_pointer": pointer, "semantic_type": sec.get("semantic_type"), "binding_approved": False, "renderer_projection_approved": False})
            field_rows.append({"challenge_id": challenge_id, "field": str(sec.get("candidate_custom_data_field") or pointer), "category": "unresolved", "source_pointer": pointer, "source_presence": exists, "source_value_type": secondary_row.get("value_type"), "source_value_sha256": secondary_row.get("value_sha256"), "evidence_status": secondary_row["status"], "receipt_observed": False, "binding_approved": False, "renderer_projection_approved": False})

        for forbidden in ("winning_frame", "close_calls"):
            if forbidden not in proposal.get("never_bind_by_default", []):
                raise AuditError(f"Proposal no longer prohibits default binding for {forbidden}")
        temporal = [classify_temporal_field("winning_frame"), classify_temporal_field("close_calls")]
        field_rows.extend({"challenge_id": challenge_id, **item} for item in temporal)

        timebase_a = rec_a.get("source_timebase", {})
        timebase_b = rec_b.get("source_timebase", {})
        if timebase_a != timebase_b:
            raise AuditError(f"Source timebase differs across repeats: {challenge_id}")
        conflict = bool(timebase_a.get("known_conflict"))
        if conflict != (challenge_id in EXPECTED_TIMEBASE_CONFLICTS):
            raise AuditError(f"Unexpected timebase conflict classification: {challenge_id}")
        if challenge_id in EXPECTED_TIMEBASE_CONFLICTS:
            declared = timebase_a.get("declared_total_duration_seconds")
            phase_sum = timebase_a.get("phase_duration_sum_seconds")
            proposal_time = proposal.get("temporal_review", {}).get(challenge_id, {})
            if declared != 11.0 or phase_sum != 12.0 or proposal_time.get("declared_total_seconds") != 11.0 or proposal_time.get("component_sum_seconds") != 12.0 or proposal_time.get("status") != "UNRESOLVED_BLOCKED_FROM_RUNTIME_MATERIALIZATION":
                raise AuditError(f"Known CHALLENGE_008/009 timebase conflict data mismatch: {challenge_id}")
            time_conflicts.append({"challenge_id": challenge_id, "declared_total_seconds": declared, "phase_duration_sum_seconds": phase_sum, "status": "UNRESOLVED_BLOCKED_FROM_RUNTIME_MATERIALIZATION", "decision_made": False})

        run_crosswalk = []
        for run, receipt_sha in zip(runs, receipt_hashes):
            rec = run["receipt"]
            run_crosswalk.append({
                "run_id": run["run_id"], "process_id": run["process_id"], "exit_code": run["exit_code"],
                "receipt_sha256": receipt_sha, "frame_snapshot_sha256": rec["lineage"]["frame_snapshot_sha256"],
                "challenge_source_sha256": rec["lineage"]["challenge_source_sha256"],
                "mechanic_source_sha256": rec["lineage"]["mechanic_source_sha256"],
                "planner_request_sha256": rec["route"]["planner_request_hash"],
                "planner_plan_sha256": rec["route"]["planner_plan_hash"],
                "projection_sha256": rec["source_frames"]["projection_sha256"],
                "source_frame_count": rec["source_frames"]["count"],
                "source_fps": rec["source_frames"]["source_fps"],
            })
        selector_summary = {
            "challenge_id": challenge_id,
            "mechanic": selector_row["selector"]["mechanic"],
            "family_id": selector_row["selector"]["family_id"],
            "selector_status": selector_row["status"],
            "repeat_agreement": selector_row["repeat_agreement"],
            "receipt_runs": run_crosswalk,
            "non_process_receipt_differences": differences,
            "source_frame_shape_only": shape_map,
            "projection_sha256_stable": rec_a["source_frames"]["projection_sha256"] == rec_b["source_frames"]["projection_sha256"],
            "candidate_field_observations_repeat_stable": rec_a.get("candidate_field_observations", {}) == rec_b.get("candidate_field_observations", {}),
            "source_timebase": timebase_a,
            "editorial_sidecar_fields": [{"field": field, "category": "editorial_sidecar_only", "receipt_observed": False, "visual_consumed": False, "binding_approved": False} for field in supported_fields["challenges"]],
            "secondary_binding_proposal": {
                "binding_kind": sec.get("binding_kind"), "source_pointer": sec.get("source_pointer"),
                "candidate_custom_data_field": candidate_field, "semantic_type": sec.get("semantic_type"),
                "asset_role": sec.get("asset_role"), "coordinate_policy": sec.get("coordinate_policy"),
                "source_evidence": secondary_row,
                "proposal_status": sec.get("proposal_status"), "binding_authorized": False,
                "renderer_projection_approved": False,
            },
            "base_track_proposal_status": proposal_base.get("status"),
        }
        proposal_crosswalk.append(selector_summary)

    if receipt_count != 18 or len(seen_run_ids) != 18 or len(seen_pids) != 18:
        raise AuditError("Expected exactly 18 unique receipts/process ids.")
    if custom_field_occurrences != 6 or custom_field_stable != 6:
        raise AuditError(f"Expected six stable custom_data candidate occurrences; observed {custom_field_occurrences}/{custom_field_stable}")
    if static_pointer_count != 3 or static_pointers_present != 3:
        raise AuditError(f"Expected three source-present static pointers; observed {static_pointers_present}/{static_pointer_count}")
    if len(time_conflicts) != 2:
        raise AuditError("Expected exactly the two unresolved timebase conflicts (CHALLENGE_008/009).")

    editorial_slots = sum(len(fields) for fields in supported_fields.values())
    if editorial_slots != 14:
        raise AuditError(f"Expected 14 editorial sidecar slots across content types; observed {editorial_slots}")

    # The 14 editorial slots are sidecar linkage only. Only six fields are applicable to Challenges.
    sidecar_rows = []
    for selector_row in report_selectors:
        for run in selector_row["runtime_runs"]:
            receipt = run["receipt"]
            for field in supported_fields["challenges"]:
                if field in receipt or field in receipt.get("candidate_field_observations", {}):
                    raise AuditError(f"Editorial sidecar field appeared in source-frame receipt: {selector_row['selector']['challenge_id']}.{field}")
    for content_type, fields in supported_fields.items():
        for field in fields:
            sidecar_rows.append({
                "content_type": content_type, "field": field, "category": "editorial_sidecar_only",
                "supported_by_carrier": True, "source_frame_receipt_observed": False,
                "visual_payload_consumed": False, "binding_approved": False,
                "carrier_status": carrier["status"],
            })
    field_rows.extend({"challenge_id": "ALL_CHALLENGES", **row} for row in sidecar_rows if row["content_type"] == "challenges")

    # The complete crosswalk does not infer values from hashes or call field presence visual consumption.
    report_out = {
        "schema": "C11D-PHASE-O-SOURCE-FRAME-SEMANTIC-BINDING-CROSSWALK-AUDIT-REPORT-V1",
        "schema_version": "1.0",
        "status": "PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "READ_ONLY_ACCEPTED_SOURCE_FRAME_RECEIPTS_TO_EXISTING_SEMANTIC_PROPOSAL",
        "input_evidence": {
            "runtime_report_path": str(report_path), "runtime_report_sha256": EXPECTED_RUNTIME_REPORT_SHA,
            "runtime_stdout_sha256": EXPECTED_RUNTIME_STDOUT_SHA, "runtime_stderr_sha256": EMPTY_SHA,
            "test_stdout_sha256": EXPECTED_TEST_STDOUT_SHA, "test_stderr_sha256": EMPTY_SHA,
            "runtime_log_directory": str(log_dir), "runtime_evidence_directory": str(evidence_dir),
            "runtime_completion_marker_sha256": sha256_file(runtime_marker_path),
            "acceptance_completion_marker_sha256": sha256_file(acceptance_marker_path),
            "acceptance_record_sha256": EXPECTED_ACCEPTANCE_RECORD_SHA,
            "proposal_sha256": actual_pins["definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json"],
            "carrier_contract_sha256": actual_pins["definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_V1.json"],
            "receipt_schema_sha256": actual_pins["definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RECEIPT_SCHEMA_V1.json"],
        },
        "source_pins": actual_pins,
        "summary": {
            "selectors_verified": len(proposal_crosswalk), "runtime_receipts_verified": receipt_count,
            "process_evidence_files_verified": len(evidence_verified), "asset_source_pins_verified": len(asset_pins_verified),
            "base_frame_field_rows": base_field_rows, "stable_custom_data_candidate_occurrences": f"{custom_field_stable}/{custom_field_occurrences}",
            "static_source_pointers_present": f"{static_pointers_present}/{static_pointer_count}",
            "timebase_conflicts_unresolved": len(time_conflicts), "challenge_editorial_sidecar_fields": len(supported_fields["challenges"]),
            "editorial_sidecar_slots_across_all_content_types": editorial_slots,
            "approved_bindings": 0, "approved_custom_data_bindings": 0, "approved_renderer_projection_bindings": 0,
            "editorial_fields_visually_consumed": 0, "custom_data_values_serialized": False,
            "renderer": "OFF", "media_created": False, "payload_materialized": False,
            "candidate_input_admissible": False, "release_authority": "NONE",
        },
        "selector_crosswalk": proposal_crosswalk,
        "field_crosswalk": field_rows,
        "temporal_policy_fields": [classify_temporal_field("winning_frame"), classify_temporal_field("close_calls")],
        "editorial_sidecar_inventory": sidecar_rows,
        "timebase_conflicts": time_conflicts,
        "asset_source_pins": [{"source_key": path, "sha256": digest} for path, digest in sorted(asset_pins_verified.items())],
        "process_evidence_sha256": evidence_verified,
        "invariants": {
            "winning_frame_is_only_challenge_temporal_anchor": True,
            "close_calls_is_episode_counter_only": True,
            "custom_data_values_serialized": False,
            "target_x_remains_scalar": True,
            "challenge_004_v1_regression_modified": False,
            "editorial_sidecar_visual_consumption": "NOT_IMPLEMENTED",
            "renderer_dispatch": False, "payload_persisted": False, "viewport_capture": False, "media_or_video_created": False,
            "source_mutation": False,
            "timebase_conflict_resolution": "NONE; CHALLENGE_008_AND_009_REMAIN_BLOCKED",
        },
        "governance_locks": GOVERNANCE_LOCKS,
        "next_safe_increment": "Prepare a narrow source-value versus frame-value provenance test for the six custom_data candidates; do not bind or serialize them until separate approval and dedicated tests exist.",
    }

    json_out = output_dir / "phase_o_crosswalk_report.json"
    json_out.write_text(json.dumps(report_out, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    csv_out = output_dir / "phase_o_field_crosswalk.csv"
    csv_fields = ["challenge_id", "content_type", "field", "category", "source_pointer", "observed_shape", "source_presence", "evidence_status", "stable_between_repeats", "receipt_observed", "actual_values_serialized", "visual_consumed", "binding_approved", "renderer_projection_approved", "source_sha256", "source_value_sha256"]
    with csv_out.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        for row in field_rows:
            writer.writerow({key: json.dumps(row[key], ensure_ascii=False) if isinstance(row.get(key), (dict, list)) else row.get(key, "") for key in csv_fields})
    md_out = output_dir / "phase_o_summary.md"
    md = [
        "# C11-D Phase O — Source-frame to semantic binding crosswalk",
        "", f"Status: `{report_out['status']}`", "",
        "## Runtime evidence", "",
        f"- Runtime report SHA-256: `{EXPECTED_RUNTIME_REPORT_SHA}`",
        f"- Source-frame receipts: `{receipt_count}/18` across `{len(proposal_crosswalk)}/9` selectors",
        f"- Process evidence files verified: `{len(evidence_verified)}/36`",
        f"- Asset source pins verified: `{len(asset_pins_verified)}`",
        f"- Frame-shape metadata rows: `{base_field_rows}` (not actual serialized per-frame values)",
        f"- Stable custom_data presence/type observations: `{custom_field_stable}/{custom_field_occurrences}`",
        f"- Static proposal source pointers found in pinned Challenge JSON: `{static_pointers_present}/{static_pointer_count}`",
        f"- Unresolved timebase conflicts: `{len(time_conflicts)}` (CHALLENGE_008, CHALLENGE_009)",
        "", "## Binding and governance status", "",
        "No binding is approved. `winning_frame` remains a temporal anchor only; `close_calls` remains an episode counter only. The six `custom_data` candidates have presence/type metadata only: values are not serialized in the receipts. Base track shapes and projection hashes do not demonstrate renderer consumption.",
        "", "Editorial sidecar values remain sidecar-only; the carrier contract explicitly reports visual consumption as not implemented. Coordinate projection and delivery resampling are unresolved. CHALLENGE_008/009 remain blocked on 11-second declaration vs 12-second phase sum.",
        "", "## Next safe increment", "", report_out["next_safe_increment"],
        "", "## Immutable locks", "", "`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.",
    ]
    md_out.write_text("\n".join(md) + "\n", encoding="utf-8")
    output_manifest = {
        "schema": "C11D-PHASE-O-CROSSWALK-OUTPUT-MANIFEST-V1",
        "status": report_out["status"],
        "runtime_report_sha256": EXPECTED_RUNTIME_REPORT_SHA,
        "outputs": {p.name: sha256_file(p) for p in (json_out, csv_out, md_out)},
        "output_directory": str(output_dir),
        "runtime_invocations": 0,
        "project_files_written": 0,
        "binding_approval_count": 0,
    }
    manifest_out = output_dir / "output_manifest.json"
    manifest_out.write_text(json.dumps(output_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"status": report_out["status"], "json": json_out, "csv": csv_out, "markdown": md_out, "manifest": manifest_out, "report": report_out, "output_manifest": output_manifest}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--runtime-marker", required=True, type=Path)
    parser.add_argument("--acceptance-marker", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        result = audit_main(args.root, args.runtime_marker, args.acceptance_marker, args.output_dir)
    except Exception as exc:
        print(f"C11D_PHASE_O_SOURCE_FRAME_SEMANTIC_CROSSWALK=FAIL_CLOSED", file=sys.stdout)
        print(f"ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    report = result["report"]
    print("C11D_PHASE_O_SOURCE_FRAME_SEMANTIC_CROSSWALK=PASS")
    print(f"SELECTORS={report['summary']['selectors_verified']}/9")
    print(f"SOURCE_FRAME_RECEIPTS={report['summary']['runtime_receipts_verified']}/18")
    print(f"PROCESS_EVIDENCE_FILES={report['summary']['process_evidence_files_verified']}/36")
    print(f"ASSET_SOURCE_PINS_VERIFIED={report['summary']['asset_source_pins_verified']}")
    print(f"BASE_FRAME_FIELD_ROWS={report['summary']['base_frame_field_rows']}")
    print(f"CUSTOM_DATA_CANDIDATES_STABLE={report['summary']['stable_custom_data_candidate_occurrences']}")
    print(f"STATIC_SOURCE_POINTERS={report['summary']['static_source_pointers_present']}")
    print(f"TIMEBASE_CONFLICTS_UNRESOLVED={report['summary']['timebase_conflicts_unresolved']}")
    print("APPROVED_BINDINGS=0")
    print("APPROVED_CUSTOM_DATA_BINDINGS=0")
    print("APPROVED_RENDERER_PROJECTION_BINDINGS=0")
    print("EDITORIAL_FIELDS_VISUALLY_CONSUMED=0")
    print(f"REPORT_PATH={result['json']}")
    print(f"REPORT_SHA256={sha256_file(result['json'])}")
    print(f"CSV_PATH={result['csv']}")
    print(f"CSV_SHA256={sha256_file(result['csv'])}")
    print(f"SUMMARY_PATH={result['markdown']}")
    print(f"SUMMARY_SHA256={sha256_file(result['markdown'])}")
    print(f"OUTPUT_MANIFEST_PATH={result['manifest']}")
    print(f"OUTPUT_MANIFEST_SHA256={sha256_file(result['manifest'])}")
    print(f"OUTPUT_DIRECTORY={args.output_dir.resolve()}")
    print("RUNTIME_INVOCATIONS=0")
    print("PROJECT_FILES_WRITTEN=0")
    print("RENDERER=OFF")
    print("MEDIA_CREATED=false")
    print("PAYLOAD_MATERIALIZED=false")
    print("CANDIDATE_INPUT_ADMISSIBLE=false")
    print("D4.8=BLOCKED")
    print("RELEASE_AUTHORITY=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
