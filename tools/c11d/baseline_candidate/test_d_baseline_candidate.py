from __future__ import annotations
import copy
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import d_baseline_candidate as dbc


def _test_legacy_disposition_contract() -> None:
    """Exercise missing-untracked and fully ledger-reconciled legacy-tree cases in temp only."""
    legacy_names = ["main.py", "README.md", "run.bat", "self_test.py"]
    blobs = {
        name: (f"synthetic legacy fixture payload:{name}\n".encode("utf-8"))
        for name in legacy_names
    }
    entries = [
        {
            "path": f"{dbc.LEGACY_CONTROL_PREFIX}{name}",
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        for name, payload in blobs.items()
    ]
    synthetic_manifest = {"source_files": entries}
    with tempfile.TemporaryDirectory(prefix="d_baseline_legacy_disposition_") as temp_name:
        temp_root = Path(temp_name)
        untracked = dbc._legacy_control_disposition(temp_root, synthetic_manifest, dbc.EXPECTED_C_MANIFEST_SHA256)
        assert untracked["status"] == "SOURCE_MISSING_UNTRACKED" and not untracked["reconciled"]

        backend_source = ROOT / "tools/c11d/d9/maintenance.py"
        backend_target = temp_root / "tools/c11d/d9/maintenance.py"
        backend_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backend_source, backend_target)

        destination_rel = f"{dbc.QUARANTINE_DESTINATION_PREFIX}synthetic_fixture"
        destination = temp_root / destination_rel
        destination.mkdir(parents=True, exist_ok=True)
        for name, payload in blobs.items():
            (destination / name).write_bytes(payload)

        maintenance = dbc._load_maintenance_module(temp_root)
        actual = maintenance.inventory_tree(destination)
        ledger = {
            "schema": "C11-D-D9.11-MAINTENANCE-LEDGER-V1",
            "schema_version": "1.0",
            "events": [{
                "event_id": "QUARANTINED-SYNTHETIC",
                "event_type": "QUARANTINED",
                "resource": dbc.LEGACY_CONTROL_DIR,
                "destination_path": destination_rel,
                "tree_sha256": actual["tree_sha256"],
                "files": actual["files"],
                "historical_manifest_sha256": dbc.EXPECTED_C_MANIFEST_SHA256,
            }],
        }
        ledger_path = temp_root / dbc.MAINTENANCE_LEDGER_REL
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
        reconciled = dbc._legacy_control_disposition(temp_root, synthetic_manifest, dbc.EXPECTED_C_MANIFEST_SHA256)
        assert reconciled["status"] == "QUARANTINED_LEDGER_RECONCILED" and reconciled["reconciled"]
        assert reconciled["tree_hash_verified"] and reconciled["manifest_hash_verified"] and reconciled["entry_hashes_reconciled"]
        assert len(reconciled["entry_reconciliation"]) == 4
        assert all(row["matches"] for row in reconciled["entry_reconciliation"])

        # A valid tree/manifest ledger seal is not sufficient if a quarantined file differs from C11-C.
        bad_destination_rel = f"{dbc.QUARANTINE_DESTINATION_PREFIX}synthetic_mismatch"
        bad_destination = temp_root / bad_destination_rel
        bad_destination.mkdir(parents=True, exist_ok=True)
        for name, payload in blobs.items():
            altered = payload + (b"tampered" if name == "README.md" else b"")
            (bad_destination / name).write_bytes(altered)
        bad_inventory = maintenance.inventory_tree(bad_destination)
        bad_ledger = {
            "schema": "C11-D-D9.11-MAINTENANCE-LEDGER-V1",
            "schema_version": "1.0",
            "events": [{
                "event_id": "QUARANTINED-SYNTHETIC-MISMATCH",
                "event_type": "QUARANTINED",
                "resource": dbc.LEGACY_CONTROL_DIR,
                "destination_path": bad_destination_rel,
                "tree_sha256": bad_inventory["tree_sha256"],
                "files": bad_inventory["files"],
                "historical_manifest_sha256": dbc.EXPECTED_C_MANIFEST_SHA256,
            }],
        }
        ledger_path.write_text(json.dumps(bad_ledger), encoding="utf-8")
        mismatch = dbc._legacy_control_disposition(temp_root, synthetic_manifest, dbc.EXPECTED_C_MANIFEST_SHA256)
        assert mismatch["status"] == "QUARANTINED_MANIFEST_ENTRY_MISMATCH"
        assert mismatch["tree_hash_verified"] and mismatch["manifest_hash_verified"]
        assert not mismatch["entry_hashes_reconciled"] and not mismatch["reconciled"]
        assert len([row for row in mismatch["entry_reconciliation"] if not row["matches"]]) == 1
        mismatched_readme = next(row for row in mismatch["entry_reconciliation"] if row["manifest_path"].endswith("/README.md"))
        assert "ARCHIVE_HASH_DIFFERS_FROM_HISTORICAL_MANIFEST" in mismatched_readme["reasons"]


def _test_operator_acceptance_checkpoint_contract() -> None:
    """Build an isolated sealed D9.15 ledger; verify checkpoint and evidence tampering are rejected."""
    import importlib.util
    with tempfile.TemporaryDirectory(prefix="d915_operator_acceptance_checkpoint_") as temp_name:
        temp_root = Path(temp_name)
        for rel in (
            "release/C11C_FREEZE_PACKAGE_MANIFEST.json",
            "definitions/c11d/baseline/D_BASELINE_OPERATOR_EVIDENCE_REQUIREMENTS_V1.json",
            "tools/c11d/baseline_candidate/operator_evidence.py",
        ):
            source = ROOT / rel
            target = temp_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        recorder_path = temp_root / "tools/c11d/baseline_candidate/operator_evidence.py"
        spec = importlib.util.spec_from_file_location("d915_checkpoint_fixture_recorder", recorder_path)
        assert spec is not None and spec.loader is not None
        recorder = importlib.util.module_from_spec(spec); spec.loader.exec_module(recorder)
        recorder.init_ledger(temp_root)
        req = recorder._requirements(temp_root)
        evidence_root = temp_root / req["evidence_root"]
        evidence_root.mkdir(parents=True, exist_ok=True)
        for idx, row in enumerate(req["required_evidence_pairings"], 1):
            rel = f"{req['evidence_root']}/fixture_{idx:02d}.txt"
            evidence = temp_root / rel
            evidence.write_text(f"isolated D9.15 evidence fixture {idx:02d}: no media\n", encoding="utf-8")
            recorder.record_event(temp_root, surface=row["surface_id"], capability=row["capability_id"],
                action=f"Isolated fixture verifies pairing {idx:02d}", evidence_file=rel,
                observed_status="PASS", operator="test fixture", operator_attestation=recorder.ATTESTATION)
        recorder.finalize_acceptance(temp_root, operator_attestation="I_CONFIRM_ALL_D915_PAIRINGS_REVIEWED_NO_MEDIA")
        verified = dbc._inspect_operator_acceptance_checkpoint(temp_root)
        assert verified["valid"] is True and verified["status"] == "PASS_CLOSED", verified
        checkpoint = temp_root / dbc.D9_15_OPERATOR_ACCEPTANCE_CHECKPOINT_REL
        original = checkpoint.read_bytes()
        tampered = json.loads(original.decode("utf-8")); tampered["passed_pairings"] = 12
        checkpoint.write_text(json.dumps(tampered, ensure_ascii=False, indent=2), encoding="utf-8")
        rejected = dbc._inspect_operator_acceptance_checkpoint(temp_root)
        assert rejected["exists"] is True and rejected["valid"] is False and rejected["status"] == "INVALID_OR_STALE", rejected
        checkpoint.write_bytes(original)
        first_evidence = next(evidence_root.glob("fixture_*.txt"))
        first_evidence.write_text("changed after checkpoint sealing; tampering must fail\n", encoding="utf-8")
        rejected = dbc._inspect_operator_acceptance_checkpoint(temp_root)
        assert rejected["valid"] is False and "changed after recording" in str(rejected["error"]), rejected


def _test_operator_evidence_waiver_contract() -> None:
    """The waiver is sealed/scope-limited and never claims screenshot evidence."""
    valid = dbc._inspect_operator_evidence_waiver(ROOT, dbc.EXPECTED_C_MANIFEST_SHA256)
    assert valid["valid"] is True and valid["status"] == "VALID_WAIVER", valid
    source = ROOT / dbc.D9_15_OPERATOR_EVIDENCE_WAIVER_REL
    original = json.loads(source.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="d915_operator_waiver_") as temp_name:
        temp_root = Path(temp_name)
        target = temp_root / dbc.D9_15_OPERATOR_EVIDENCE_WAIVER_REL
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(original, ensure_ascii=False, indent=2), encoding="utf-8")
        assert dbc._inspect_operator_evidence_waiver(temp_root, dbc.EXPECTED_C_MANIFEST_SHA256)["valid"] is True
        tampered = copy.deepcopy(original)
        tampered["captured_pairings"] = 13
        target.write_text(json.dumps(tampered, ensure_ascii=False, indent=2), encoding="utf-8")
        result = dbc._inspect_operator_evidence_waiver(temp_root, dbc.EXPECTED_C_MANIFEST_SHA256)
        assert result["valid"] is False and result["status"] == "INVALID"
        resealed = copy.deepcopy(original)
        resealed["d9_15_pass_claimed"] = True
        unsigned = dict(resealed); unsigned.pop("waiver_sha256", None)
        resealed["waiver_sha256"] = dbc._sha_bytes(dbc._canonical_json(unsigned))
        target.write_text(json.dumps(resealed, ensure_ascii=False, indent=2), encoding="utf-8")
        result = dbc._inspect_operator_evidence_waiver(temp_root, dbc.EXPECTED_C_MANIFEST_SHA256)
        assert result["valid"] is False and "d9_15_pass_claimed" in str(result["error"])


def main() -> int:
    _test_legacy_disposition_contract()
    _test_operator_evidence_waiver_contract()
    _test_operator_acceptance_checkpoint_contract()
    record = dbc.build_candidate_preflight(ROOT)
    result = dbc.validate_candidate_preflight(record, ROOT)
    assert result["valid"] is True and result["freeze_eligible"] is False
    assert record["decision"] == "PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED"
    assert record["immutable_reference"]["release"] == "C11-C 2.19.12"
    assert record["inventory"]["c_manifest_entries"] == 2545
    assert not record["inventory"]["c_manifest_missing_nonlegacy_entries"]
    assert set(record["inventory"]["c_manifest_missing_entries"]) == set(record["inventory"]["c_manifest_missing_legacy_entries"])
    disposition = record["inventory"]["legacy_c11d_control_disposition"]
    assert disposition["manifest_reference_count"] == 4
    if disposition["reconciled"]:
        assert "LEGACY_C11D_CONTROL_QUARANTINE_REVIEW_REQUIRED" not in record["blockers"]
    else:
        assert "LEGACY_C11D_CONTROL_QUARANTINE_REVIEW_REQUIRED" in record["blockers"]
    if disposition["missing_source_reference_count"] > 0 and not disposition["reconciled"]:
        assert "C11C_MANIFEST_LEGACY_ENTRIES_PENDING_DISPOSITION" in record["blockers"]
    if record["inventory"]["c_manifest_missing_legacy_entries"]:
        assert record["inventory"]["c_manifest_unreconciled_legacy_entries"] in (0, 4)
    assert record["inventory"]["protected_c_entries"] >= 800
    assert not record["inventory"]["protected_c_changed_entries"]
    assert record["inventory"]["c_manifest_changed_entries_confined_to_d_roots"] is True
    assert record["canonical_surfaces"]["count"] == 5
    assert record["governance"]["d4_8"] == "BLOCKED"
    assert record["governance"]["renderer_activation"] is False
    assert record["governance"]["media_created"] is False
    assert record["governance"]["release_authority"] == "NONE"
    must_block = {
        "D9_14_REAL_MEDIA_CERTIFICATION_BLOCKED",
        "D9_16_FULL_ACCEPTANCE_NOT_CLOSED",
        "D9_17_CLOSURE_NO_GO",
        "D_RENDERER_BASELINE_APPROVAL_NOT_RECORDED",
        "D_BASELINE_APPROVAL_NOT_RECORDED",
    }
    assert must_block.issubset(set(record["blockers"])), sorted(set(must_block) - set(record["blockers"]))
    assert record["governance"]["d9_15_operator_evidence_waiver_valid"] is True
    assert record["governance"]["d9_15_operator_evidence_waiver_status"] == "VALID_WAIVER"
    if record["governance"]["d9_15_operator_acceptance_checkpoint_valid"] is True:
        assert record["governance"]["d9_15_candidate_evidence_gate_status"] == "D9.15_OPERATOR_EVIDENCE_PASS_CLOSED"
        assert record["governance"]["d9_15_operator_evidence_pass_closed"] is True
        assert record["governance"]["d9_15_operator_acceptance_checkpoint_status"] == "PASS_CLOSED"
        assert len(record["governance"]["d9_15_operator_acceptance_checkpoint_sha256"]) == 64
        assert record["governance"]["d9_16_full_acceptance_blocker_count"] == 1
    else:
        assert record["governance"]["d9_15_candidate_evidence_gate_status"] == "WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY"
        assert record["governance"]["d9_15_operator_evidence_pass_closed"] is False
        assert record["governance"]["d9_16_full_acceptance_blocker_count"] == 2
    assert "D9_15_OPERATOR_EVIDENCE_MATRIX_REQUIRED" not in record["blockers"]
    assert record["side_effects"] == {"repository_files_written": False, "freeze_archive_created": False, "media_created": False, "renderer_activation": False, "manifest_modified": False, "release_authority_granted": False}

    negatives = 0
    def reject(label, mutate, reseal=True):
        nonlocal negatives
        candidate = copy.deepcopy(record)
        mutate(candidate)
        if reseal:
            candidate = dbc._seal(candidate)
        try:
            dbc.validate_candidate_preflight(candidate, ROOT)
        except dbc.CandidateAuditError:
            negatives += 1
        else:
            raise AssertionError(f"D baseline candidate negative unexpectedly accepted: {label}")

    reject("promote candidate", lambda x: x.update(candidate_freeze_eligible=True))
    reject("promote decision", lambda x: x.update(decision="CANDIDATE_FREEZE_READY"))
    reject("grant authority", lambda x: x.update(candidate_release_authority="GRANTED"))
    reject("unlock D4.8", lambda x: x["governance"].update(d4_8="AUTHORIZED"))
    reject("activate renderer", lambda x: x["governance"].update(renderer_activation=True))
    reject("claim media output", lambda x: x["governance"].update(media_created=True))
    reject("alter C manifest", lambda x: x["immutable_reference"].update(manifest_sha256="0" * 64))
    reject("alter protected entry count", lambda x: x["inventory"].update(protected_c_entries=1))
    reject("hide changed C paths", lambda x: x["inventory"].update(c_manifest_changed_entries=[]))
    reject("claim changed paths outside extensions are acceptable", lambda x: x["inventory"].update(c_manifest_changed_entries_confined_to_d_roots=False))
    reject("sixth surface", lambda x: x["canonical_surfaces"].update(count=6))
    reject("claim D9.14 pass", lambda x: x["blockers"].remove("D9_14_REAL_MEDIA_CERTIFICATION_BLOCKED"))
    if record["governance"]["d9_15_operator_acceptance_checkpoint_valid"] is True:
        reject("downgrade canonical D9.15 checkpoint", lambda x: x["governance"].update(d9_15_candidate_evidence_gate_status="WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY", d9_15_operator_evidence_pass_closed=False, d9_15_operator_acceptance_checkpoint_valid=False))
    else:
        reject("forge D9.15 PASS from waiver", lambda x: x["governance"].update(d9_15_candidate_evidence_gate_status="D9.15_OPERATOR_EVIDENCE_PASS_CLOSED", d9_15_operator_evidence_pass_closed=True, d9_15_operator_acceptance_checkpoint_valid=True, d9_15_operator_acceptance_checkpoint_status="PASS_CLOSED", d9_15_operator_acceptance_checkpoint_sha256="0"*64, d9_15_operator_acceptance_checkpoint_ledger_sha256="0"*64))
    reject("claim D9.16 closed", lambda x: x["blockers"].remove("D9_16_FULL_ACCEPTANCE_NOT_CLOSED"))
    reject("claim D9.17 closed", lambda x: x["blockers"].remove("D9_17_CLOSURE_NO_GO"))
    reject("claim renderer approval", lambda x: x["blockers"].remove("D_RENDERER_BASELINE_APPROVAL_NOT_RECORDED"))
    reject("claim D baseline approval", lambda x: x["blockers"].remove("D_BASELINE_APPROVAL_NOT_RECORDED"))
    reject("remove no-write invariant", lambda x: x["side_effects"].update(repository_files_written=True))
    reject("create freeze archive", lambda x: x["side_effects"].update(freeze_archive_created=True))
    reject("mutate C manifest", lambda x: x["side_effects"].update(manifest_modified=True))
    reject("tamper tree fingerprint", lambda x: x["tree_identity"].update(sha256="0" * 64))
    reject("raw seal tamper", lambda x: x.update(candidate_freeze_eligible=True), reseal=False)
    assert negatives == 22, f"negative controls mismatch: {negatives}/22"
    blockers = ",".join(record["blockers"])
    legacy = record["inventory"]["legacy_c11d_control_disposition"]
    mismatch_rows = [row for row in legacy.get("entry_reconciliation", []) if not row.get("matches")]
    if legacy.get("status") == "QUARANTINED_MANIFEST_ENTRY_MISMATCH":
        mismatch_names = ",".join(Path(row["manifest_path"]).name for row in mismatch_rows) or "unspecified"
    elif legacy.get("reconciled"):
        mismatch_names = "none"
    else:
        mismatch_names = "not_applicable"
    reconciled_count = 4 if legacy.get("reconciled") else 0
    print(
        "C11-D BASELINE CANDIDATE PREFLIGHT PASS | "
        f"candidate=C11-D-BASELINE-CANDIDATE-0.1 | C11-C=IMMUTABLE_REFERENCE_MATCH | "
        f"manifest_paths_present={record['inventory']['c_manifest_source_present_entries']}/{record['inventory']['c_manifest_entries']} | "
        f"legacy_missing={len(record['inventory']['c_manifest_missing_legacy_entries'])}/4 | "
        f"legacy_disposition={legacy['status']} | legacy_reconciled_files={reconciled_count}/4 | legacy_mismatch_files={mismatch_names} | "
        f"protected_entries={record['inventory']['protected_c_entries']}/{record['inventory']['protected_c_entries']} | "
        f"manifest_exact={record['inventory']['c_manifest_exact_matches']}/{record['inventory']['c_manifest_entries']} | "
        f"allowed_D_changes={len(record['inventory']['c_manifest_changed_entries'])} | "
        f"active_surfaces={record['canonical_surfaces']['count']}/5 | negative={negatives}/22 | "
        f"D9.15={record['governance']['d9_15_candidate_evidence_gate_status']} | "
        f"baseline_approval={record['governance']['baseline_approval_checkpoint_status']} | "
        f"freeze_eligible=false | blockers={len(record['blockers'])} | "
        f"tree_files={record['tree_identity']['included_files']} | tree_sha256={record['tree_identity']['sha256']} | "
        "renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
