#!/usr/bin/env python3
"""Read-only E6 composition readiness audit. Does not launch media tools."""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PIN_REL = "definitions/c11e/test_only/C11E_E6_COMPOSITION_READINESS_SOURCE_PINS_V1.json"
SCOPE_REL = "definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json"
APPROVAL_REL = "definitions/c11e/test_only/C11E_E6_OPERATOR_SCOPE_APPROVAL_RECORD_V1.json"
CHALLENGE_RUN = "E6CHPREP_20261118T202841Z_37C6AE0E"
CHALLENGE_BASE = Path("artifacts/tests/c11e/e6_challenge_prepare_only_orchestrator") / CHALLENGE_RUN
CHALLENGE_RECEIPT_REL = (CHALLENGE_BASE / "E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_RECEIPT_V1.json").as_posix()
CHALLENGE_RECEIPT_SHA = "b54a884f1574d22fa65ea198d279d9ba84bb3967adc87885213f7659a1b1c944"
CHALLENGE_RECEIPT_BYTES = 63629
CHALLENGE_INPUT_SHA = "4607831a94ecbb64b2f1cfb6ef3a7480e3f7315e8aee588a3ef9a93f97ce8878"
CHALLENGE_INPUT_BYTES = 8245
REQUAL_REL = "artifacts/tests/c11e/e6_smoke18_reuse_requalification/E6SMK18REQUAL_20261118T141200Z_BA5AC046/E6_SMOKE18_REUSE_REQUALIFICATION_RECEIPT_V1.json"
REQUAL_SHA = "4d63b8caec7a975cc0362ee9d7a5924f5ab8371e8e8e1457e1d60956bf65ce33"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def check_sidecar(root: Path, sidecar_rel: str, expected_sha: str, expected_filename: str) -> dict[str, Any]:
    path = root / Path(sidecar_rel)
    item = {"path": sidecar_rel, "expected_sha256": expected_sha, "expected_filename": expected_filename}
    if not path.is_file():
        item.update(status="MISSING", actual_text=None)
        return item
    parts = path.read_text(encoding="ascii").strip().split()
    ok = len(parts) >= 2 and parts[0].lower() == expected_sha.lower() and parts[1] == expected_filename
    item.update(status="PASS" if ok else "MISMATCH", actual_text=" ".join(parts))
    return item


def check_file(root: Path, rel: str, expected_sha: str, expected_bytes: int | None = None) -> dict[str, Any]:
    path = root / Path(rel)
    item: dict[str, Any] = {"path": rel, "expected_sha256": expected_sha, "expected_bytes": expected_bytes}
    if not path.is_file():
        item.update(status="MISSING", actual_sha256=None, actual_bytes=None)
        return item
    actual_bytes = path.stat().st_size
    actual_sha = sha256_file(path)
    ok = actual_sha == expected_sha and (expected_bytes is None or actual_bytes == expected_bytes)
    item.update(status="PASS" if ok else "MISMATCH", actual_sha256=actual_sha, actual_bytes=actual_bytes)
    return item


def run_audit(root: Path) -> dict[str, Any]:
    pin_doc = read_json(root / PIN_REL)
    scope = read_json(root / SCOPE_REL)
    approval = read_json(root / APPROVAL_REL)
    pin_rows = [check_file(root, x["path"], x["sha256"], x["bytes"]) for x in pin_doc["pins"]]
    manifest_row = next((x for x in pin_rows if x["path"] == "release/C11C_FREEZE_PACKAGE_MANIFEST.json"), None)
    d48_row = next((x for x in pin_rows if x["path"].endswith("C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json")), None)

    receipt_row = check_file(root, CHALLENGE_RECEIPT_REL, CHALLENGE_RECEIPT_SHA, CHALLENGE_RECEIPT_BYTES)
    input_rel = "definitions/c11d/production/C11E_E6_CHALLENGE_PREPARE_ONLY_INPUT_MANIFEST_V1.json"
    input_row = check_file(root, input_rel, CHALLENGE_INPUT_SHA, CHALLENGE_INPUT_BYTES)
    requal_row = check_file(root, REQUAL_REL, REQUAL_SHA)
    receipt_sidecar = check_sidecar(root, CHALLENGE_RECEIPT_REL + ".sha256", CHALLENGE_RECEIPT_SHA, Path(CHALLENGE_RECEIPT_REL).name)
    requal_sidecar = check_sidecar(root, REQUAL_REL + ".sha256", REQUAL_SHA, Path(REQUAL_REL).name)
    challenge_detail: dict[str, Any] = {"receipt": receipt_row, "receipt_sidecar": receipt_sidecar, "input_manifest": input_row, "reuse_requalification_receipt": requal_row, "reuse_requalification_sidecar": requal_sidecar}
    written_rows: list[dict[str, Any]] = []
    challenge_counts_ok = False
    editorial_unknown = None
    input_personalization = None
    music_legacy_authority = None
    boundary_facts: dict[str, Any] = {}

    if receipt_row["status"] == "PASS":
        receipt = read_json(root / CHALLENGE_RECEIPT_REL)
        written = receipt.get("written_evidence_files", [])
        written_rows = [check_file(root, x["path"], x["sha256"], x["bytes"]) for x in written]
        counts = receipt.get("counts", {})
        challenge_counts_ok = (
            receipt.get("status") == "PASS_PREPARE_ONLY_18_E1_INTENTS_18_D_ENVELOPES_EXECUTION_HELD"
            and receipt.get("run_id") == CHALLENGE_RUN
            and counts.get("challenge_scenario_groups") == 6
            and counts.get("challenge_probe_subruns") == 18
            and counts.get("e1_intents") == 18
            and counts.get("d_envelopes") == 18
            and counts.get("smoke18_top_level_scenarios") == 6
            and len(written) == 36
        )
        intent_paths = [x["path"] for x in written if "/intents/" in x["path"]]
        envelope_paths = [x["path"] for x in written if "/envelopes/" in x["path"]]
        challenge_counts_ok = challenge_counts_ok and len(intent_paths) == 18 and len(set(intent_paths)) == 18 and len(envelope_paths) == 18 and len(set(envelope_paths)) == 18
        unknown_count, common_populated = 0, 0
        for rel in intent_paths:
            obj = read_json(root / rel)
            editorial = obj.get("editorial", {})
            for field in ("title", "subtitle", "call_to_action"):
                value = editorial.get(field)
                if value in (None, "", "UNKNOWN"):
                    unknown_count += 1
                else:
                    common_populated += 1
        editorial_unknown = {"intent_count":len(intent_paths),"unknown_common_fields":unknown_count,"populated_common_fields":common_populated,"required_common_fields":len(intent_paths)*3}
        challenge_detail["written_evidence_files"] = {"expected":36,"actual":len(written),"passed":sum(x["status"]=="PASS" for x in written_rows),"failed":[x for x in written_rows if x["status"]!="PASS"]}
        challenge_detail["counts"] = counts
        challenge_detail["status_valid"] = receipt.get("status")
        challenge_detail["execution_boundary"] = receipt.get("execution", {})
        challenge_detail["governance"] = receipt.get("governance", {})
    if input_row["status"] == "PASS":
        im = read_json(root / input_rel)
        req = im.get("request_template", {})
        input_personalization = req.get("personalization_enabled")
        music_legacy_authority = im.get("music_fixture", {}).get("authority")
        challenge_detail["input_manifest_status"] = im.get("status")
        challenge_detail["personalization_enabled"] = input_personalization
        challenge_detail["music_fixture_authority_at_plan_time"] = music_legacy_authority
        copy_rel = im.get("provenance", {}).get("copy_path") or None
        # The receipt, rather than a guessed filename, is the authority for its evidence copy.
        if not copy_rel:
            copy_rel = receipt.get("input_manifest", {}).get("copy_path") if receipt_row["status"] == "PASS" else None
        if copy_rel:
            copied = check_file(root, copy_rel, CHALLENGE_INPUT_SHA, CHALLENGE_INPUT_BYTES)
            copied_sidecar = check_sidecar(root, copy_rel + ".sha256", CHALLENGE_INPUT_SHA, Path(copy_rel).name)
            challenge_detail["input_manifest_evidence_copy"] = copied
            challenge_detail["input_manifest_evidence_copy_sidecar"] = copied_sidecar

    boundary_rel = "definitions/c11d/production/C11E_OPTION_C_D_POSTCOMPOSITION_BOUNDARY_V1.json"
    if (root / boundary_rel).is_file():
        b = read_json(root / boundary_rel)
        boundary_facts = {
            "status": b.get("status"),
            "d_composition_owner": b.get("d_composition", {}).get("ownership"),
            "emits": b.get("d_composition", {}).get("emits"),
            "proposal_status": b.get("layout_policy", {}).get("proposal_status"),
            "executable_geometry_approved": b.get("layout_policy", {}).get("executable_geometry_approved"),
            "hard_locks": b.get("hard_locks", {}),
        }

    source_pin_failures = [x for x in pin_rows if x["status"] != "PASS"]
    evidence_rows = [receipt_row, receipt_sidecar, input_row, requal_row, requal_sidecar] + written_rows
    for key in ("input_manifest_evidence_copy", "input_manifest_evidence_copy_sidecar"):
        if key in challenge_detail: evidence_rows.append(challenge_detail[key])
    evidence_failures = [x for x in evidence_rows if x["status"] != "PASS"]
    loop_pin = next((x for x in pin_rows if x["path"].endswith("c11e_e4b_loop_family_stage_contract.py")), None)
    drill_pin = next((x for x in pin_rows if x["path"].endswith("c11e_e4c_drill_visual_composition_consumer.py")), None)
    loop_boundary_ok = boundary_facts.get("status") == "PREPARE_ONLY_NOT_DISPATCHABLE" and boundary_facts.get("hard_locks", {}).get("compositor_invoked") is False and boundary_facts.get("hard_locks", {}).get("media_created") is False
    editorials_missing = (editorial_unknown is not None and editorial_unknown["populated_common_fields"] == 0 and input_personalization is False)
    blockers = []
    if source_pin_failures: blockers.append("LIVE_CHECKOUT_SOURCE_PIN_DIVERGENCE")
    if evidence_failures: blockers.append("UPSTREAM_RECEIPT_OR_NESTED_EVIDENCE_MISMATCH")
    if not challenge_counts_ok: blockers.append("CHALLENGE_PREPARE_ONLY_RECEIPT_COUNTS_OR_STATUS_MISMATCH")
    if loop_boundary_ok and loop_pin and loop_pin["status"] == "PASS": blockers.append("LOOP_D_POSTCOMPOSITOR_NOT_IMPLEMENTED_OR_NOT_ADMITTED")
    if editorials_missing: blockers.append("CHALLENGE_EDITORIAL_FIXTURE_MISSING_FROM_PREPARE_ONLY_INTENTS")
    if requal_row["status"] == "PASS": blockers.append("13_REUSE_CANDIDATES_REMAIN_NOT_E6_ACCEPTANCE")
    blockers.append("D4_8_SUCCESSOR_POLICY_AND_SEPARATE_E6_TEST_ONLY_EXECUTION_AUTHORIZATION_NOT_ISSUED")
    blockers.append("GLOBAL_D_RENDERER_IO_BASELINE_NOT_YET_ADMISSIBLE; LAST_PINNED_CHECKPOINT_REMAINS_0_OF_10_COMPLETE")
    if approval.get("pending_operator_decision", {}).get("status") == "PENDING": blockers.append("SPANISH_EDITORIAL_FIXTURE_VALUES_REQUIRE_OPERATOR_APPROVAL")

    audit_pass = not source_pin_failures and not evidence_failures and challenge_counts_ok
    report = {
        "schema":"C11E-E6-COMPOSITION-READINESS-AUDIT-RECEIPT-V1","schema_version":"1.0",
        "created_utc":datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z"),
        "project_root":str(root),
        "status":"PASS_AUDIT_ONLY_GAPS_IDENTIFIED_EXECUTION_HELD" if audit_pass else "BLOCKED_SOURCE_OR_EVIDENCE_RECONCILIATION",
        "audit_scope":"READ_ONLY_SOURCE_AND_EVIDENCE_RECONCILIATION_ONLY",
        "source_pin_summary":{"expected":len(pin_rows),"passed":len(pin_rows)-len(source_pin_failures),"failed":len(source_pin_failures),"rows":pin_rows},
        "protected_baselines":{"c11c_manifest":manifest_row,"d4_8_r1v_v2":d48_row},
        "challenge_prepare_only":challenge_detail,
        "challenge_editorial_fixture":editorial_unknown,
        "loop_d_composition":{
            "source_pin":loop_pin,"boundary":boundary_facts,
            "disposition":"PREPARE_ONLY_ONLY_NO_D_PIXEL_CONSUMER_ACCEPTED_FROM_E4B_SCOPE",
            "fresh_d_composition_required_for_six_smoke18_loop_rows":True
        },
        "drill_d_composition":{"source_pin":drill_pin,"disposition":"SIX_E4C_AV_REUSE_CANDIDATES_REQUIRING_E6_ROW_PREDICATE_REQUALIFICATION"},
        "reuse_requalification":requal_row,
        "music_fixture":{"operator_approved_test_only":scope.get("music_fixture",{}).get("operator_approved_test_fixture"),"challenge_fixture":scope.get("music_fixture",{}).get("challenge_only"),"plan_time_status":music_legacy_authority,"reprepare_required":True},
        "governance":{
          "operator_scope_approved":scope.get("operator_approved_scope",{}).get("smoke18_scope_approved"),
          "successor_policy_finalized":scope.get("execution_authority",{}).get("successor_policy_finalized"),
          "e6_test_only_authorized":False,"d4_8":"BLOCKED","renderer":"OFF","production_dispatch":False,"media_created":False,"release_authority":"NONE","batch_id_reserved":False
        },
        "blockers":blockers,
        "execution": {"godot_invoked":False,"ffmpeg_invoked":False,"ffprobe_invoked":False,"audio_generated":False,"mux_invoked":False,"media_created":False,"renderer_invoked":False,"dispatch_invoked":False,"batch_id_consumed":False},
        "limitations":["The audit validates exact hashes and recorded evidence only; it does not independently replay the original media QA or human review.","The nightly comparison archive is not a source authority; all pins are evaluated against the active checkout.","A successful audit means the gaps are precisely diagnosed, not that Smoke18 is render-ready or accepted."]
    }
    return report


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--output-root", required=True)
    args=ap.parse_args()
    root=Path(args.project_root).resolve()
    output=Path(args.output_root).resolve()
    if not root.is_dir():
        print("AUDIT_BLOCKED_PROJECT_ROOT_MISSING",file=sys.stderr); return 2
    # Keep output strictly inside the checkout's evidence tree.
    expected_prefix=(root/"artifacts"/"tests"/"c11e").resolve()
    try: output.relative_to(expected_prefix)
    except ValueError:
        print("AUDIT_BLOCKED_OUTPUT_ROOT_OUTSIDE_EVIDENCE_TREE",file=sys.stderr); return 2
    output.mkdir(parents=True,exist_ok=False)
    report=run_audit(root)
    out=output/"E6_COMPOSITION_READINESS_AUDIT_RECEIPT_V1.json"
    raw=(json.dumps(report,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    out.write_bytes(raw)
    digest=hashlib.sha256(raw).hexdigest()
    side=out.with_suffix(out.suffix+".sha256")
    side.write_text(f"{digest}  {out.name}\n",encoding="ascii")
    print(f"E6_COMPOSITION_READINESS_STATUS={report['status']}")
    print(f"SOURCE_PINS={report['source_pin_summary']['passed']}/{report['source_pin_summary']['expected']} PASS")
    print(f"CHALLENGE_WRITTEN_EVIDENCE={report['challenge_prepare_only'].get('written_evidence_files',{}).get('passed',0)}/36 PASS")
    print(f"CHALLENGE_EDITORIAL_POPULATED={report['challenge_editorial_fixture'].get('populated_common_fields',0) if report['challenge_editorial_fixture'] else 'UNKNOWN'}")
    print(f"LOOP_D_COMPOSITOR={report['loop_d_composition']['disposition']}")
    print(f"E6_ACCEPTED=0; MATRIX_FROZEN=FALSE; D4_8=BLOCKED; RENDERER=OFF; RELEASE_AUTHORITY=NONE")
    for item in report["blockers"]: print(f"BLOCKER={item}")
    print(f"AUDIT_RECEIPT={out}")
    print(f"AUDIT_RECEIPT_SHA256={digest}")
    return 0 if report["status"] == "PASS_AUDIT_ONLY_GAPS_IDENTIFIED_EXECUTION_HELD" else 3

if __name__ == "__main__": raise SystemExit(main())
