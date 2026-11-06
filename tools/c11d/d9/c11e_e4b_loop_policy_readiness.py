"""Read-only E4B Loop policy-readiness audit.

Audits the accepted 5-family / 27-grammar plan-only matrix against the current
D9.8 model, historical D policy proposals and D renderer approval packet.
It does not modify source, approve policies, materialize payloads or invoke a
renderer, generator, Godot, family music, D3 V5, FFmpeg or media operation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "C11E-E4B-LOOP-POLICY-READINESS-AUDIT-V1"
IDENTITY_FIELDS = (
    "canonical_request_hash",
    "editorial_hash",
    "plan_hash",
    "bridge_hash",
    "adapter_envelope_hash",
    "e1_request_hash",
    "e1_plan_hash",
    "e1_intent_hash",
    "music_profile_id_from_frozen_c11c_profile_registry",
)
POLICY_FILES = {
    "shared_regions": "definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json",
    "loop_drill_windows": "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json",
    "delivery_timebase": "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json",
    "audio_music_delivery": "definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json",
    "loop_composition": "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json",
}
D98_MODEL = "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"
APPROVAL_PACKET = "docs/current/d/D_RENDERER_POLICY_APPROVAL_DECISION_PACKET_V1.md"
EXACT_SELECTOR_CHECKPOINT = "docs/current/d/C11D_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2_RUNTIME_ACCEPTANCE_CHECKPOINT_20261017.md"
TIMING_CARRIER_CHECKPOINT = "docs/current/d/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REQUEST_BOUND_REFERENCE_CARRIER_CHECKPOINT_20261016.md"
FIELD_WINDOW_REVIEW = "docs/current/d/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_UNIFIED_REVIEW_INTEGRATION_CHECKPOINT.md"
FIELD_ROUTING_REVIEW = "docs/current/d/D_RENDERER_EDITORIAL_FIELD_ROUTING_VISIBILITY_RECONCILIATION_CHECKPOINT_V1.md"


class PolicyReadinessError(RuntimeError):
    """Raised when evidence/source prerequisites are missing or inconsistent."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): canonical(value[k]) for k in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def sha256_json(value: Any) -> str:
    raw = json.dumps(canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return sha256_bytes(raw)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - report a single controlled failure
        raise PolicyReadinessError(f"Invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PolicyReadinessError(f"Expected JSON object: {path}")
    return value


def verify_sidecar(folder: Path, filename: str) -> dict[str, Any]:
    target = folder / filename
    sidecar = folder / (target.stem + ".sha256")
    if not target.is_file() or not sidecar.is_file():
        raise PolicyReadinessError(f"Missing evidence or SHA sidecar: {target}")
    actual = sha256_file(target)
    declared = sidecar.read_text(encoding="ascii").strip().split()[0]
    if not re.fullmatch(r"[0-9a-f]{64}", declared) or declared != actual:
        raise PolicyReadinessError(f"SHA sidecar mismatch: {target}")
    return {"path": str(target), "sha256": actual, "sidecar": str(sidecar), "sidecar_pass": True}


def verify_report_self_hash(report: Mapping[str, Any], label: str) -> str:
    material = copy.deepcopy(dict(report))
    declared = material.pop("report_sha256", None)
    actual = sha256_json(material)
    if not isinstance(declared, str) or declared != actual:
        raise PolicyReadinessError(f"{label} report self-hash mismatch")
    return actual


def _all_true(mapping: Mapping[str, Any]) -> bool:
    return bool(mapping) and all(value is True for value in mapping.values())


def _approval_booleans_false(document: Mapping[str, Any], label: str) -> dict[str, Any]:
    approval = document.get("approval_state", document.get("approval_gates"))
    if not isinstance(approval, Mapping):
        raise PolicyReadinessError(f"{label} has no approval_state/approval_gates object")
    boolean_values = {str(k): v for k, v in approval.items() if isinstance(v, bool)}
    true_values = sorted(k for k, v in boolean_values.items() if v is True)
    if true_values:
        raise PolicyReadinessError(f"{label} unexpectedly contains approved flags: {true_values}")
    return {"boolean_approval_flags": boolean_values, "all_boolean_approvals_false": True}


def parse_packet_pin(packet_text: str, label: str) -> str:
    patterns = {
        "shared_regions": r"\|\s*Shared presentation semantic-region map\s*\|[^\n]*?\|\s*`([0-9a-f]{64})`\s*\|",
        "loop_drill_windows": r"\|\s*Visual Loop/Drill field windows\s*\|[^\n]*?\|\s*`([0-9a-f]{64})`\s*\|",
        "delivery_timebase": r"\|\s*Unified delivery timebase\s*\|[^\n]*?\|\s*`([0-9a-f]{64})`\s*\|",
        "audio_music_delivery": r"\|\s*Unified audio/music delivery\s*\|[^\n]*?\|\s*`([0-9a-f]{64})`\s*\|",
    }
    pattern = patterns.get(label)
    if pattern is None:
        raise PolicyReadinessError(f"No V1 packet parser for policy: {label}")
    match = re.search(pattern, packet_text)
    if not match:
        raise PolicyReadinessError(f"Could not parse V1 approval-packet pin for {label}")
    return match.group(1)


def _check_matrix_report(report: Mapping[str, Any], label: str) -> dict[str, Any]:
    if report.get("schema") != "C11E-E4B-LOOP-FAMILY-MATRIX-RECEIPT-V1":
        raise PolicyReadinessError(f"{label} matrix schema mismatch")
    if report.get("status") != "PASS_LOOP_FAMILY_PLAN_MATRIX_ONLY":
        raise PolicyReadinessError(f"{label} matrix status is not PASS_LOOP_FAMILY_PLAN_MATRIX_ONLY")
    scope = report.get("scope", {})
    if (scope.get("family_count"), scope.get("grammar_count"), scope.get("case_count")) != (5, 27, 81):
        raise PolicyReadinessError(f"{label} matrix scope is not 5/27/81")
    cases = report.get("cases")
    if not isinstance(cases, list) or len(cases) != 81:
        raise PolicyReadinessError(f"{label} matrix does not contain exactly 81 cases")
    keys = {(c.get("family_id"), c.get("subtype_id"), c.get("scenario")) for c in cases if isinstance(c, Mapping)}
    if len(keys) != 81:
        raise PolicyReadinessError(f"{label} matrix contains duplicate or malformed case keys")
    scenario_counts: dict[str, int] = {}
    for case in cases:
        scenario = str(case.get("scenario"))
        scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
        if case.get("d9_actual_plan_status") != "PLANNED" or case.get("d9_plan_kind") != "UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY":
            raise PolicyReadinessError(f"{label} contains a non-plan-only D9.9 case")
        if case.get("editorial_fields_preserved") is not True:
            raise PolicyReadinessError(f"{label} loses Loop editorial fields")
        if set(case.get("editorial_fields", {})) != {"title", "subtitle", "call_to_action", "language"}:
            raise PolicyReadinessError(f"{label} Loop editorial keyset mismatch")
        if case.get("e1_editorial_consumer_status") != "NOT_CONSUMED_E1":
            raise PolicyReadinessError(f"{label} no longer records the E1 consumption gate")
        if case.get("e1_adapter_status") != "NOT_CONNECTED_E1":
            raise PolicyReadinessError(f"{label} no longer records the E1 family adapter gate")
        if case.get("music_route") != "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH":
            raise PolicyReadinessError(f"{label} family music route changed")
        repeat = case.get("deterministic_repeat", {})
        if not isinstance(repeat, Mapping) or not _all_true(repeat):
            raise PolicyReadinessError(f"{label} deterministic repeat failed")
        governance = case.get("governance", {})
        if not isinstance(governance, Mapping) or not _all_true(governance):
            raise PolicyReadinessError(f"{label} case governance assertions failed")
        for field in ("music_engine_invoked", "music_audio_created", "renderer_invoked", "ffmpeg_mux_invoked"):
            if case.get(field) is not False:
                raise PolicyReadinessError(f"{label} invoked forbidden operation {field}")
    if scenario_counts != {"BASELINE": 27, "GAMEPLAY_SEED_ONLY_CHANGED": 27, "MUSIC_SEED_ONLY_CHANGED": 27}:
        raise PolicyReadinessError(f"{label} seed scenario distribution mismatch: {scenario_counts}")
    relations = report.get("seed_domain_relations")
    if not isinstance(relations, list) or len(relations) != 27:
        raise PolicyReadinessError(f"{label} expected 27 seed-domain relation rows")
    if not all(isinstance(r, Mapping) and _all_true(r.get("checks", {})) for r in relations):
        raise PolicyReadinessError(f"{label} seed-domain orthogonality failed")
    governance = report.get("governance", {})
    expected_false = ("renderer", "renderer_input_emitted", "renderer_dispatch_invoked", "production_execution", "media_created", "godot_invoked", "c11c_family_visual_generators_invoked", "c11c_family_music_generator_invoked", "d3_v5_invoked", "ffmpeg_invoked", "c11c_baseline_modified")
    for field in expected_false:
        if governance.get(field) is not False:
            raise PolicyReadinessError(f"{label} governance is not fail-closed: {field}")
    if governance.get("release_authority") != "NONE" or governance.get("d4_8") != "BLOCKED" or governance.get("d9_10") != "PREPARE_ONLY":
        raise PolicyReadinessError(f"{label} governance gate values changed")
    return {
        "request_origin": report.get("request_origin"),
        "case_count": len(cases),
        "selector_count": len({(c["family_id"], c["subtype_id"]) for c in cases}),
        "scenario_counts": scenario_counts,
        "deterministic_repeats": len(cases),
        "seed_relation_count": len(relations),
        "status": report.get("status"),
        "governance": {field: governance.get(field) for field in expected_false + ("release_authority", "d4_8", "d9_10")},
    }


def _compare_gui_cli(gui: Mapping[str, Any], cli: Mapping[str, Any]) -> dict[str, Any]:
    gui_by_key = {(c["family_id"], c["subtype_id"], c["scenario"]): c for c in gui["cases"]}
    cli_by_key = {(c["family_id"], c["subtype_id"], c["scenario"]): c for c in cli["cases"]}
    if set(gui_by_key) != set(cli_by_key):
        raise PolicyReadinessError("GUI and CLI selector/scenario keysets differ")
    hashes: dict[str, int] = {}
    for field in IDENTITY_FIELDS:
        equal = 0
        for key, left in gui_by_key.items():
            right = cli_by_key[key]
            if left.get(field) == right.get(field):
                equal += 1
        if equal != 81:
            raise PolicyReadinessError(f"GUI/CLI identity mismatch in {field}: {equal}/81")
        hashes[field] = equal
    parity = cli.get("gui_cli_parity")
    if not isinstance(parity, Mapping) or parity.get("status") != "PASS_GUI_CLI_ALL_27_SELECTOR_PARITY_ONLY" or parity.get("case_count") != 81:
        raise PolicyReadinessError("CLI report does not contain the accepted 81-row GUI/CLI parity marker")
    parity_rows = parity.get("cases", [])
    if len(parity_rows) != 81 or not all(_all_true(row.get("checks", {})) for row in parity_rows):
        raise PolicyReadinessError("CLI report contains a failed GUI/CLI parity row")
    return {"status": parity["status"], "cases": 81, "direct_identity_fields": hashes}


def run_policy_readiness_audit(project_root: Path | str, gui_evidence_root: Path | str, cli_evidence_root: Path | str, output_root: Path | str | None = None) -> dict[str, Any]:
    root = Path(project_root).resolve()
    gui_root = Path(gui_evidence_root).resolve()
    cli_root = Path(cli_evidence_root).resolve()

    gui_integrity = [verify_sidecar(gui_root, "matrix_request_template.json"), verify_sidecar(gui_root, "matrix_report.json")]
    cli_integrity = [verify_sidecar(cli_root, "matrix_request_template.json"), verify_sidecar(cli_root, "matrix_report.json")]
    gui_report = read_json(gui_root / "matrix_report.json")
    cli_report = read_json(cli_root / "matrix_report.json")
    gui_self_hash = verify_report_self_hash(gui_report, "GUI")
    cli_self_hash = verify_report_self_hash(cli_report, "CLI")
    gui_summary = _check_matrix_report(gui_report, "GUI")
    cli_summary = _check_matrix_report(cli_report, "CLI")
    parity = _compare_gui_cli(gui_report, cli_report)

    d98 = read_json(root / D98_MODEL)
    loop_model = d98.get("content_types", {}).get("visual_loops", {})
    d98_compatibility = loop_model.get("request_plan_compatibility")
    if d98.get("checkpoint") != "D9.8" or loop_model.get("model_state") != "ACTIVE_MODEL_ONLY":
        raise PolicyReadinessError("D9.8 Loop model state has drifted")
    if d98_compatibility != "PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER":
        raise PolicyReadinessError(f"Unexpected D9.8 Loop compatibility metadata: {d98_compatibility}")

    policy_results: dict[str, Any] = {}
    current_policy_hashes: dict[str, str] = {}
    for label, relpath in POLICY_FILES.items():
        path = root / relpath
        document = read_json(path)
        current_hash = sha256_file(path)
        current_policy_hashes[label] = current_hash
        approvals = _approval_booleans_false(document, label)
        policy_results[label] = {
            "path": relpath,
            "sha256": current_hash,
            "status": document.get("status"),
            "policy_state": document.get("policy", {}).get("state") if isinstance(document.get("policy"), Mapping) else document.get("mapping_policy", {}).get("state"),
            "approval_state": approvals,
        }
    packet_text = (root / APPROVAL_PACKET).read_text(encoding="utf-8-sig")
    if "REVIEW_PACKET_ONLY_ALL_POLICIES_UNAPPROVED" not in packet_text:
        raise PolicyReadinessError("Historical D renderer approval packet V1 status has changed")
    packet_hashes = {}
    stale_hashes = []
    for label in ("shared_regions", "loop_drill_windows", "delivery_timebase", "audio_music_delivery"):
        packet_hash = parse_packet_pin(packet_text, label)
        current_hash = current_policy_hashes[label]
        matches = packet_hash == current_hash
        packet_hashes[label] = {"packet_v1_sha256": packet_hash, "current_file_sha256": current_hash, "matches": matches}
        if not matches:
            stale_hashes.append(label)

    exact_selector_text = (root / EXACT_SELECTOR_CHECKPOINT).read_text(encoding="utf-8-sig")
    if not re.search(r"exact_selector_visual_payload_instances_materialized=5/5", exact_selector_text):
        raise PolicyReadinessError("Historical exact-selector checkpoint does not confirm five in-memory geometric payloads")
    if not re.search(r"renderer_inputs_emitted=0/5", exact_selector_text) or not re.search(r"approvals_granted=0", exact_selector_text):
        raise PolicyReadinessError("Historical exact-selector checkpoint is no longer renderer-input/approval blocked")
    if "c11c_geometric_waves_v1" not in exact_selector_text or "five geometric" not in exact_selector_text.lower():
        raise PolicyReadinessError("Historical exact-selector family scope is not explicitly geometric-only")

    timing_text = (root / TIMING_CARRIER_CHECKPOINT).read_text(encoding="utf-8-sig")
    if "NOT_BINDING_NOT_APPROVED" not in timing_text or "five geometric Visual Loop selectors" not in timing_text:
        raise PolicyReadinessError("Historical request-bound timing carrier scope/status has drifted")
    window_review_text = (root / FIELD_WINDOW_REVIEW).read_text(encoding="utf-8-sig")
    if "INTEGRATED FOR REVIEW / NOT APPROVED" not in window_review_text or "visibility_windows` continues to be `null" not in window_review_text:
        raise PolicyReadinessError("Historical Loop/Drill field-window review status has drifted")
    routing_text = (root / FIELD_ROUTING_REVIEW).read_text(encoding="utf-8-sig")
    if "Evaluated visibility windows" not in routing_text or "0 |" not in routing_text:
        raise PolicyReadinessError("Historical field-routing reconciliation no longer records zero evaluated windows")

    composition = policy_results["loop_composition"]
    if composition["status"] != "PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT":
        raise PolicyReadinessError("Loop composition proposal is no longer pending review")
    for label in ("shared_regions", "loop_drill_windows", "delivery_timebase", "audio_music_delivery"):
        if policy_results[label]["status"] != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
            raise PolicyReadinessError(f"{label} proposal status is no longer proposal-only")
        if policy_results[label]["policy_state"] != "PROPOSED_NOT_APPROVED":
            raise PolicyReadinessError(f"{label} policy state is no longer proposed/unapproved")

    report: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PASS_AUDIT_ONLY_POLICY_APPROVAL_REQUIRED",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "evidence": {
            "gui_root": str(gui_root),
            "cli_root": str(cli_root),
            "gui_integrity": gui_integrity,
            "cli_integrity": cli_integrity,
            "gui_report_self_hash": gui_self_hash,
            "cli_report_self_hash": cli_self_hash,
            "gui": gui_summary,
            "cli": cli_summary,
            "gui_cli_parity": parity,
        },
        "d98_d99_boundary": {
            "d98_loop_model_state": loop_model.get("model_state"),
            "d98_request_plan_compatibility": d98_compatibility,
            "d99_plan_status_across_matrix": "PLANNED",
            "d99_plan_kind_across_matrix": "UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY",
            "interpretation": "D9.9 supports canonical editorial intent planning for all 27 Loop selectors; this is not D4 executable-plan or renderer compatibility. D9.8 metadata remains deliberately unchanged pending a versioned semantic reconciliation.",
            "matrix_report_flag_note": "d9_catalog_request_plan_compatible_flag is serialized as false by the matrix helper; the authoritative current D9.8 metadata was independently read from the pinned model file above.",
        },
        "policy_proposals": policy_results,
        "approval_packet_v1_pin_reconciliation": packet_hashes,
        "stale_packet_v1_hash_labels": stale_hashes,
        "stale_packet_v1_hash_count": len(stale_hashes),
        "approval_packet_v1_status": "REVIEW_PACKET_ONLY_ALL_POLICIES_UNAPPROVED",
        "historical_payload_boundary": {
            "exact_selector_checkpoint_scope": "GEOMETRIC_WAVES_FIVE_GRAMMARS_ONLY",
            "in_memory_payload_instances": "5/5",
            "renderer_inputs_emitted": "0/5",
            "policy_approval_assertions_checked": 19,
            "approvals_granted": 0,
            "request_bound_timing_reference": "PREPARATION_ONLY_NOT_BINDING_NOT_APPROVED",
            "loop_drill_evaluated_visibility_windows": 0,
            "family_matrix_visual_payloads_materialized": False,
        },
        "next_gate": {
            "classification": "OPERATOR_POLICY_DECISION_AND_PIN_RECONCILIATION_REQUIRED",
            "loop_visual_decision_groups": ["A.1_SHARED_PRESENTATION_REGIONS", "A.3_LOOP_DRILL_FIELD_WINDOWS", "E4B_LOOP_COMPOSITION_PROPOSAL_V1"],
            "loop_av_decision_groups_later": ["B.1_UNIFIED_DELIVERY_TIMEBASE", "D.1_UNIFIED_AUDIO_MUSIC_DELIVERY"],
            "family_binding_work_after_policy_decisions": "RECONCILE_EXISTING_GEOMETRIC_ONLY_BINDING_SCOPE_BEFORE_EXTENDING_TO_ALL_27_GRAMMARS",
            "renderer_input_authorized": False,
            "consumer_implementation_authorized": False,
            "release_authority": "NONE",
        },
        "governance": {
            "renderer": False,
            "renderer_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "production_execution": False,
            "media_created": False,
            "c11c_baseline_modified": False,
            "godot_invoked": False,
            "c11c_family_visual_generators_invoked": False,
            "c11c_family_music_generator_invoked": False,
            "d3_v5_invoked": False,
            "ffmpeg_invoked": False,
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "d9_14": "BLOCKED",
            "d9_16": "BLOCKED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED_FOR_PROMOTION",
            "release_authority": "NONE",
        },
    }
    report["report_sha256"] = sha256_json(report)
    if output_root is not None:
        output = Path(output_root).resolve()
        if output.exists():
            raise PolicyReadinessError(f"Output root exists; overwrite denied: {output}")
        output.mkdir(parents=True, exist_ok=False)
        report_path = output / "C11E_E4B_LOOP_POLICY_READINESS_REPORT_V1.json"
        raw = json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8")
        report_path.write_bytes(raw)
        (output / "C11E_E4B_LOOP_POLICY_READINESS_REPORT_V1.sha256").write_text(f"{sha256_bytes(raw)}  {report_path.name}\n", encoding="ascii")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--gui-evidence-root", required=True)
    parser.add_argument("--cli-evidence-root", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args(argv)
    try:
        report = run_policy_readiness_audit(args.project_root, args.gui_evidence_root, args.cli_evidence_root, args.output_root)
    except PolicyReadinessError as exc:
        print(f"C11E_E4B_LOOP_POLICY_READINESS=BLOCKED; ERROR={exc}", file=sys.stderr)
        return 2
    print("C11E_E4B_LOOP_POLICY_READINESS=PASS_AUDIT_ONLY_POLICY_APPROVAL_REQUIRED")
    print(f"GUI_CASES={report['evidence']['gui']['case_count']}; CLI_CASES={report['evidence']['cli']['case_count']}; PARITY={report['evidence']['gui_cli_parity']['cases']}/81")
    print(f"DIRECT_IDENTITIES_EQUAL={len(report['evidence']['gui_cli_parity']['direct_identity_fields'])}/9_FIELDS_X_81_CASES")
    print(f"D98_LOOP_COMPATIBILITY={report['d98_d99_boundary']['d98_request_plan_compatibility']}")
    print(f"STALE_APPROVAL_PACKET_V1_HASHES={report['stale_packet_v1_hash_count']}; LABELS={','.join(report['stale_packet_v1_hash_labels']) or 'NONE'}")
    print("LOOP_VISUAL_POLICY_DECISIONS=REQUIRED; COMPOSITION=NOT_APPROVED; FAMILY_PAYLOAD_SCOPE=GEOMETRIC_ONLY_HISTORICALLY")
    print("RENDERER=OFF; MEDIA=FALSE; RELEASE_AUTHORITY=NONE")
    print(f"REPORT_SHA256={report['report_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
