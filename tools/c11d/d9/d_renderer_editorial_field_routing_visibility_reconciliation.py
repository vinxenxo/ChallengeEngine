"""Read-only reconciliation of existing editorial routing and visibility proposals.

This does not create layout coordinates, evaluate runtime windows, materialize new
payloads, emit renderer input, dispatch a renderer, or write a receipt to disk.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from d_renderer_editorial_field_consumption_audit import build_audit

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_ROUTING_VISIBILITY_RECONCILIATION_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_ROUTING_VISIBILITY_RECONCILIATION_SCHEMA_V1.json")
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_ID = "C11-D-RENDERER-EDITORIAL-FIELD-ROUTING-VISIBILITY-RECONCILIATION-V1"
STATUS = "PREPARATION_ONLY_RECONCILIATION_NOT_RENDERER_INPUT"
CONTENT_TYPES = ("challenges", "visual_loops", "visual_drills")
EXPECTED_FIELDS = {
    "challenges": ("title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"),
    "visual_loops": ("title", "subtitle", "call_to_action", "language"),
    "visual_drills": ("title", "subtitle", "call_to_action", "language"),
}
VISUAL_FIELDS = {"title", "subtitle", "call_to_action", "player_name", "challenge_label"}


class EditorialRoutingReconciliationError(ValueError):
    """Raised if source lineage, routing agreement, or governance invariants drift."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _sha_file(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise EditorialRoutingReconciliationError(f"Cannot read/hash required source {path}: {exc}") from exc


def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise EditorialRoutingReconciliationError(f"Cannot read JSON {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise EditorialRoutingReconciliationError(f"Expected JSON object: {rel}")
    return value


def _verify_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise EditorialRoutingReconciliationError("Routing/visibility contract identity/version mismatch")
    if contract.get("status") != STATUS:
        raise EditorialRoutingReconciliationError("Routing/visibility contract cannot self-promote")
    if contract.get("authority", {}).get("frozen_c11c_manifest_sha256") != MANIFEST_SHA256:
        raise EditorialRoutingReconciliationError("Frozen C11-C pin drift")
    if _sha_file(root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json") != MANIFEST_SHA256:
        raise EditorialRoutingReconciliationError("Frozen C11-C manifest SHA-256 mismatch")
    if contract.get("approval_state") != {
        "routing_matrix_approved": False,
        "semantic_region_mapping_approved": False,
        "editorial_field_window_policy_approved": False,
        "editorial_values_visually_consumed": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "d9_14": "BLOCKED_AS_REQUIRED",
        "d9_16": "BLOCKED_AS_REQUIRED",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
        "release_authority": "NONE",
    }:
        raise EditorialRoutingReconciliationError("Governance approvals/locks were changed")
    if contract.get("execution_boundary") != {
        "mode": "IN_MEMORY_RECONCILIATION_ONLY",
        "persistent_report_written": False,
        "payload_files_written": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_created": False,
        "output_artifact_path": None,
        "c11c_source_mutation": False,
        "renderer": "OFF",
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
    }:
        raise EditorialRoutingReconciliationError("Execution boundary changed/promoted")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise EditorialRoutingReconciliationError("Contract schema must use JSON Schema Draft 2020-12")
    if schema.get("additionalProperties") is not False or set(schema.get("required", [])) != set(schema.get("properties", {})):
        raise EditorialRoutingReconciliationError("Contract schema must be strict and exact at top level")

    raw_lineage = contract.get("source_lineage")
    if not isinstance(raw_lineage, list) or len(raw_lineage) != 27:
        raise EditorialRoutingReconciliationError("Source lineage must contain exactly 27 pinned inputs")
    lineage: dict[str, dict[str, Any]] = {}
    for row in raw_lineage:
        if not isinstance(row, Mapping) or set(row) != {"path", "sha256"}:
            raise EditorialRoutingReconciliationError("Malformed source-lineage entry")
        rel, expected = str(row["path"]), str(row["sha256"])
        if rel in lineage:
            raise EditorialRoutingReconciliationError(f"Duplicate source-lineage input: {rel}")
        actual = _sha_file(root / rel)
        if actual != expected:
            raise EditorialRoutingReconciliationError(f"Source hash mismatch: {rel}")
        lineage[rel] = {"path": rel, "sha256": actual}
    if list(lineage)[0] != "release/C11C_FREEZE_PACKAGE_MANIFEST.json":
        raise EditorialRoutingReconciliationError("Frozen manifest must be the first source pin")

    sources: dict[str, dict[str, Any]] = {}
    for key, rel in contract.get("sources", {}).items():
        sources[key] = _read_json(root, rel)
    expected_status = {
        "logical_composition": "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN",
        "neutral_frame_program": "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN",
        "semantic_region_proposal": "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN",
        "challenge_phase_field_window_proposal": "PROPOSAL_ONLY_NOT_RENDERER_INPUT",
        "loop_drill_field_window_proposal": "PROPOSAL_ONLY_NOT_RENDERER_INPUT",
        "field_consumption_audit": "PREPARATION_ONLY_FIELD_CONSUMPTION_GAP_AUDIT_NOT_RENDERER_INPUT",
        "temporal_bound_preview": "PREPARATION_ONLY_SOURCE_BOUND_TEMPORAL_PREVIEW_NOT_APPROVED_NOT_FROZEN",
    }
    for key, status in expected_status.items():
        if sources.get(key, {}).get("status") != status:
            raise EditorialRoutingReconciliationError(f"Unexpected upstream state for {key}")
    return contract, schema, sources


def _derive_routes(sources: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    composition = sources["logical_composition"]
    frame = sources["neutral_frame_program"]
    regions = sources["semantic_region_proposal"]
    challenge_windows = sources["challenge_phase_field_window_proposal"]
    loop_drill_windows = sources["loop_drill_field_window_proposal"]

    required = composition.get("required_editorial_fields")
    if required != {key: list(value) for key, value in EXPECTED_FIELDS.items()}:
        raise EditorialRoutingReconciliationError("D9.9 universal editorial field set changed")
    field_targets = composition.get("field_targets")
    frame_targets = frame.get("field_region_targets")
    region_targets = regions.get("field_targets")
    if not all(isinstance(x, Mapping) for x in (field_targets, frame_targets, region_targets)):
        raise EditorialRoutingReconciliationError("One or more semantic routing maps are absent")

    loop_visible = loop_drill_windows.get("mapping_policy", {}).get("visible_fields")
    loop_visible_by_field = {x.get("field_id"): x for x in loop_visible or [] if isinstance(x, Mapping)}
    loop_meta = loop_drill_windows.get("mapping_policy", {}).get("metadata_only_fields", [])
    loop_metadata_fields = {x.get("field_id") for x in loop_meta if isinstance(x, Mapping)}
    if set(loop_visible_by_field) != {"title", "subtitle", "call_to_action"} or loop_metadata_fields != {"language"}:
        raise EditorialRoutingReconciliationError("Loop/Drill window policy scope drift")
    if loop_drill_windows.get("scope", {}).get("supported_content_types") != ["visual_loops", "visual_drills"]:
        raise EditorialRoutingReconciliationError("Loop/Drill window proposal improperly broadens its scope")

    phase_fields = challenge_windows.get("mapping_policy", {}).get("field_to_phase")
    phase_field_names = [x.get("field_id") for x in phase_fields or [] if isinstance(x, Mapping)]
    if phase_field_names != ["hook", "reveal", "cta"]:
        raise EditorialRoutingReconciliationError("Challenge phase-window source namespace changed")
    if challenge_windows.get("supported_content_types") != ["challenges"]:
        raise EditorialRoutingReconciliationError("Challenge phase-window scope drift")

    region_ids = {x.get("region_id") for x in frame.get("region_definitions", {}).keys()} if False else set(frame.get("region_definitions", {}))
    if not region_ids:
        raise EditorialRoutingReconciliationError("Frame-program semantic region definitions are missing")
    region_fields: dict[str, set[str]] = {}
    for item in regions.get("regions", []):
        rid = item.get("region_id")
        region_fields[rid] = set(item.get("mapped_fields", []))

    routes: list[dict[str, Any]] = []
    for content_type in CONTENT_TYPES:
        fields = required[content_type]
        for field in fields:
            if field == "language":
                route = {
                    "content_type": content_type,
                    "source_field": field,
                    "field_kind": "METADATA",
                    "semantic_region_id": None,
                    "region_mapping_state": "NOT_APPLICABLE_METADATA_ONLY",
                    "geometry_state": "NOT_APPLICABLE_METADATA_ONLY",
                    "visibility_policy_id": None,
                    "visibility_rule": None,
                    "visibility_state": "METADATA_ONLY_NO_WINDOW",
                    "evaluated_window": None,
                    "payload_consumption_state": "METADATA_NOT_VISUAL",
                    "approval_state": "NOT_A_VISUAL_ROUTING_DECISION",
                }
            else:
                logical_target = field_targets.get(field)
                if not isinstance(logical_target, Mapping):
                    raise EditorialRoutingReconciliationError(f"Missing logical target: {field}")
                target = logical_target.get("target_region")
                if target != frame_targets.get(field) or target != region_targets.get(field):
                    raise EditorialRoutingReconciliationError(f"Field-to-region disagreement across sources: {field}")
                if logical_target.get("mapping_state") != "PROPOSED_NOT_APPROVED":
                    raise EditorialRoutingReconciliationError(f"Logical field routing was promoted: {field}")
                if target not in region_ids or field not in region_fields.get(target, set()):
                    raise EditorialRoutingReconciliationError(f"Semantic region declaration missing field {field}")

                policy_id: str | None = None
                rule: str | None = None
                if content_type in ("visual_loops", "visual_drills"):
                    declared = loop_visible_by_field.get(field)
                    if declared is not None:
                        if declared.get("target_region") != target or declared.get("window_rule") != "FULL_CONTINUOUS_PAYLOAD_SPAN":
                            raise EditorialRoutingReconciliationError(f"Loop/Drill field/window mapping drift: {content_type}.{field}")
                        policy_id = loop_drill_windows["mapping_policy"]["policy_id"]
                        rule = "FULL_CONTINUOUS_PAYLOAD_SPAN_IF_NONEMPTY"
                    else:
                        raise EditorialRoutingReconciliationError(f"No explicit Loop/Drill visibility rule for {field}")
                # Challenge's current phase policy is intentionally not used for D9.9 universal fields.
                route = {
                    "content_type": content_type,
                    "source_field": field,
                    "field_kind": "VISUAL_TEXT",
                    "semantic_region_id": target,
                    "region_mapping_state": "PROPOSED_NOT_APPROVED",
                    "geometry_state": "UNRESOLVED_NO_COORDINATES",
                    "visibility_policy_id": policy_id,
                    "visibility_rule": rule,
                    "visibility_state": "PROPOSED_RULE_NOT_EVALUATED_RAW_EDITORIAL_VALUES_NOT_EXPOSED" if policy_id else "NO_D9_9_FIELD_WINDOW_MAPPING",
                    "evaluated_window": None,
                    "payload_consumption_state": "NOT_CONSUMED_BY_CURRENT_IN_MEMORY_VISUAL_PAYLOAD_HARNESS",
                    "approval_state": "PROPOSED_NOT_APPROVED",
                }
            routes.append(route)
    return routes


def build_reconciliation(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, sources = _verify_contract(root)
    derived = _derive_routes(sources)
    if contract.get("field_routes") != derived:
        raise EditorialRoutingReconciliationError("Canonical field_routes differ from the live upstream contract join")

    # Reuse the established in-memory source audit to corroborate counts; it writes no output.
    audit = build_audit(root)
    summary = audit.get("summary", {})
    if summary.get("enabled_field_instances") != 14 or summary.get("exact_review_chain_field_instances") != 14:
        raise EditorialRoutingReconciliationError("Editorial review chain does not contain the expected 14 field instances")
    if summary.get("visual_payload_consumed_field_instances") != 0:
        raise EditorialRoutingReconciliationError("Current payload-consumption baseline unexpectedly changed; re-audit before updating this contract")

    visual_routes = [row for row in derived if row["field_kind"] == "VISUAL_TEXT"]
    metadata_routes = [row for row in derived if row["field_kind"] == "METADATA"]
    loop_rules = [row for row in visual_routes if row["content_type"] in ("visual_loops", "visual_drills") and row["visibility_policy_id"]]
    challenge_unmapped = [row for row in visual_routes if row["content_type"] == "challenges" and row["visibility_state"] == "NO_D9_9_FIELD_WINDOW_MAPPING"]

    report = {
        "schema": "C11-D-RENDERER-EDITORIAL-FIELD-ROUTING-VISIBILITY-RECONCILIATION-REPORT-V1",
        "schema_version": "1.0",
        "status": STATUS,
        "contract_sha256": _sha_file(root / CONTRACT_REL),
        "implementation_sha256": _sha_file(Path(__file__).resolve()),
        "frozen_c11c_manifest_sha256": MANIFEST_SHA256,
        "source_lineage": copy.deepcopy(contract["source_lineage"]),
        "field_routes": derived,
        "field_domain_separation": copy.deepcopy(contract["field_domain_separation"]),
        "summary": {
            "content_types_reviewed": 3,
            "field_instances_reviewed": len(derived),
            "visual_field_instances": len(visual_routes),
            "metadata_only_field_instances": len(metadata_routes),
            "canonical_review_chain_parity": "PASS_14_OF_14",
            "current_visual_payload_consumption": "ZERO_OF_14",
            "loop_drill_rules_declared_but_not_evaluated": len(loop_rules),
            "challenge_universal_fields_without_window_policy": len(challenge_unmapped),
            "evaluated_visibility_windows": 0,
            "semantic_region_mapping_approved": False,
            "editorial_field_window_policy_approved": False,
            "editorial_values_visually_consumed": False,
            "candidate_input_admissible": False,
        },
        "unresolved_gaps": [
            "D9_9 universal Challenge title/subtitle/call_to_action/player_name/challenge_label have no matching approved visibility-window contract.",
            "Challenge hook/reveal/cta phase policy is a separate namespace; no implicit aliases to universal D9.9 fields are allowed.",
            "Loop/Drill window rules are proposed but evaluated visibility_windows remain null because raw editorial values are not exposed by the current runtime summary.",
            "Semantic routing IDs are not geometry; all geometry remains unresolved or profile/family-resolved outside this reconciliation.",
            "No current visual payload harness consumes canonical editorial text as first-class payload members.",
            "Dynamic arbitrary-request transport, renderer-native input, and renderer implementation remain absent.",
        ],
        "execution_boundary": copy.deepcopy(contract["execution_boundary"]),
        "approval_state": copy.deepcopy(contract["approval_state"]),
    }
    report["reconciliation_sha256"] = _sha_json(report)
    return report


def validate_reconciliation(report: Mapping[str, Any], project_root: Path | str | None = None) -> bool:
    root = _root(project_root)
    if not isinstance(report, Mapping):
        raise EditorialRoutingReconciliationError("Reconciliation report must be an object")
    supplied = dict(report)
    given_hash = supplied.get("reconciliation_sha256")
    unsigned = {k: copy.deepcopy(v) for k, v in supplied.items() if k != "reconciliation_sha256"}
    if not isinstance(given_hash, str) or given_hash != _sha_json(unsigned):
        raise EditorialRoutingReconciliationError("Reconciliation digest mismatch")
    expected = build_reconciliation(root)
    if supplied != expected:
        raise EditorialRoutingReconciliationError("Reconciliation differs from pinned sources or governance locks")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--json", action="store_true", help="Print the in-memory reconciliation JSON to stdout; no files are written")
    args = parser.parse_args(argv)
    try:
        report = build_reconciliation(args.project_root)
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            s = report["summary"]
            print(
                "C11-D EDITORIAL FIELD ROUTING/VISIBILITY RECONCILIATION PASS | "
                f"content_types={s['content_types_reviewed']}/3 | field_instances={s['field_instances_reviewed']}/14 | "
                f"review_chain=14/14 | payload_consumption=0/14 | loop_drill_rules={s['loop_drill_rules_declared_but_not_evaluated']} | "
                f"challenge_universal_windows=UNMAPPED | evaluated_windows=0 | approved=false | "
                "renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
            )
        return 0
    except (EditorialRoutingReconciliationError, OSError, ValueError) as exc:
        print(f"C11-D EDITORIAL FIELD ROUTING/VISIBILITY RECONCILIATION FAIL | {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
