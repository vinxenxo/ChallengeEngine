#!/usr/bin/env python3
"""Validate the current C11-D V2B source-composition evidence receipt against the active checkout and operator temp logs.
Uses Python standard library only. This validates evidence integrity, not production authority.
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
from pathlib import Path

RECEIPT_REL = "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_V2_20261026.json"
SCHEMA_REL = "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_SCHEMA_V2_20261026.json"
CONTRACT_REL = "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CONTRACT_V1.json"
EXPECTED_RECEIPT_SCHEMA = "C11D-V2B-ALLOWLISTED-COORDINATE-SOURCE-COMPOSITION-RUNTIME-EVIDENCE-V2"
EXPECTED_SCHEMA_ID = "C11D-V2B-ALLOWLISTED-COORDINATE-SOURCE-COMPOSITION-RUNTIME-EVIDENCE-SCHEMA-V2"
EXPECTED_C11C = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_CONTRACT = "575717bb3f36b476c9742488c8cace622a217c8861e376d17c519d02c70534b7"
EXPECTED_CONTRACT_SCHEMA = "a24948379e03762b8074b571801a3eb12f5ae006fcf4443ce4f4f7b9330cebae"
EXPECTED_HARNESS = "06417bf63a8c89c4ac5afb0ab818b3b395c48e31c5a0c6d45bd10e1aadccaa28"
EXPECTED_STATIC_V1 = "c18082f7ad62722153088b07ade0f1753be739a7a6b00da0d08bf1db4e671946"
EXPECTED_STATIC_V2 = "a3e13c382cf0fb7ebaa57896b75d36809ebfd09e6425f87936b9f2a2b8be7a1e"
EXPECTED_STATIC_COMPOSITION = "37317cd3462e555afba5c883aef97e6632ec9387d099fd33c24e4ab1d0c14c14"
EXPECTED_CONSUMER_V2 = "2376d4c9208d749b3681f8083d1d0be1a5658f62930b9b92167916196aec3eef"
EXPECTED_RUNTIME_INPUT_PINS = {
 "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_CONTRACT_V2.json":"0bd65e8f64c13850670d927d62209276ae94999ce57c790db7ae1592fa793ae9",
 "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_CONTRACT_SCHEMA_V2.json":"197cbad2f479f9baa3500c784bec7c4d84a7640c5ddeb43ccc8edfac95c60315",
 "tools/c11d/d9/allowlisted_coordinate_consumer_review_only_v2.gd":"2376d4c9208d749b3681f8083d1d0be1a5658f62930b9b92167916196aec3eef",
 "tools/c11d/d9/test_allowlisted_coordinate_consumer_review_only_runtime_v2.gd":"8b30bc90fa7f95ac8b38e8ad2b01670ed1fb97416acfc437225db4f478f8ded5",
 "tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_allowlisted_coordinate_consumer_runtime_static_v2.py":"a3e13c382cf0fb7ebaa57896b75d36809ebfd09e6425f87936b9f2a2b8be7a1e",
 "docs/current/d/C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_FIX_CHECKPOINT_20261022_V2.md":"edf2109d457eeec117e866712063bc580e6223379ed6fc72b7e6e3b5dc773d0f"
}
EXPECTED_ACCEPTANCE_RECORD = "5ce4cddace9a8a04b4c1ba520cfdeeb79ee3a7e1952dc70f60baf45e02623d34"
EXPECTED_HISTORICAL_EVIDENCE = "a4684fdb7b3ea4b85f68b561d9aaa64981517f65530ba8a8787f820eb5e3960f"
EXPECTED_HISTORICAL_DECISION = "a52d5d8a4564cc96d47633c5527248bdc102152da8ce13ad699575fb5b677a08"
EXPECTED_RUNTIME_STDOUT = "b5e1465894a9d5ad5a26715f10459bf578809d4a3fadce7fc030b4964aa2c3bb"
EXPECTED_EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
EXPECTED_DESIGN_RECEIPT = "9148ad3dfc21857d7decf5885a3fb0e10a839234ba7672040cfdfa86b57c7bd2"
PASS_MARKER = "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RUNTIME_TEST_STATUS=PASS"
FAIL_MARKER = "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RUNTIME_TEST_STATUS=FAIL"

checks: list[tuple[str, bool]] = []
def check(name: str, condition: bool) -> None:
    checks.append((name, bool(condition)))
def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().lower()
def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))
def main() -> int:
    if len(sys.argv) != 3:
        print("USAGE=test_d_renderer_challenge_visual_payload_v2b_source_composition_runtime_evidence_v2.py REPO_ROOT RUNTIME_EVIDENCE_DIR", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    evidence_dir = Path(sys.argv[2]).resolve()
    receipt_path = root / RECEIPT_REL
    schema_path = root / SCHEMA_REL
    contract_path = root / CONTRACT_REL
    out_path = evidence_dir / "composition_runtime_stdout.txt"
    err_path = evidence_dir / "composition_runtime_stderr.txt"
    summary_path = evidence_dir / "runtime_execution_summary.json"

    check("repo_root_exists", root.is_dir())
    check("receipt_exists", receipt_path.is_file())
    check("schema_exists", schema_path.is_file())
    check("source_composition_contract_exists", contract_path.is_file())
    check("runtime_stdout_exists", out_path.is_file())
    check("runtime_stderr_exists", err_path.is_file())
    check("runtime_summary_exists", summary_path.is_file())
    if not all(p.is_file() for p in [receipt_path, schema_path, contract_path, out_path, err_path, summary_path]):
        failed = [n for n, ok in checks if not ok]
        print(f"C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_CHECKS={len(checks)-len(failed)}/{len(checks)}")
        print("C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_VALIDATION_STATUS=FAIL")
        for name, ok in checks:
            if not ok: print("C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_FAILURE=" + name, file=sys.stderr)
        return 1

    try:
        receipt = load_json(receipt_path)
        schema = load_json(schema_path)
        contract = load_json(contract_path)
        summary = load_json(summary_path)
        stdout = out_path.read_text(encoding="utf-8-sig", errors="replace")
        stderr_bytes = err_path.read_bytes()
    except Exception as exc:
        print("RECEIPT_VALIDATION_INPUT_ERROR=" + str(exc), file=sys.stderr)
        return 1

    expected_top = ["schema", "schema_version", "evidence_status", "scope", "observed_date", "reference_snapshot", "execution", "source_lineage", "observed_runtime_markers", "reconciliation", "governance_locks", "next_gate", "notes"]
    check("receipt_top_level_is_object", isinstance(receipt, dict))
    check("receipt_closed_top_level_shape", isinstance(receipt, dict) and set(receipt) == set(expected_top))
    check("schema_is_draft_2020_12", schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema")
    check("schema_id_exact", schema.get("$id") == EXPECTED_SCHEMA_ID)
    check("schema_closed_top_level", schema.get("additionalProperties") is False)
    check("schema_required_exact", set(schema.get("required", [])) == set(expected_top))
    check("schema_properties_exact", set(schema.get("properties", {})) == set(expected_top))
    check("receipt_schema_id_exact", receipt.get("schema") == EXPECTED_RECEIPT_SCHEMA)
    check("receipt_schema_version", receipt.get("schema_version") == "1.0")
    check("receipt_pending_review_status", receipt.get("evidence_status") == "CAPTURED_OPERATOR_RUNTIME_PASS_PENDING_FORMAL_REVIEW")
    check("receipt_scope_is_test_only", receipt.get("scope") == "ISOLATED_IN_MEMORY_SOURCE_COMPOSITION_TEST_ONLY_NOT_PRODUCTION_WIRING")
    check("receipt_observed_date", receipt.get("observed_date") == "2026-10-26")

    snapshot = receipt.get("reference_snapshot", {})
    check("snapshot_archive_name", snapshot.get("filename") == "ChallengeEngineV01_STATELESS_C11-D_20261026_013616.zip")
    check("snapshot_archive_sha", snapshot.get("sha256") == "3e48ee2d815593137f5863139e05c1aa04eb40b4a58ddfb3bed4507125c96874")
    check("snapshot_archive_size", snapshot.get("size_bytes") == 8001498)
    check("snapshot_entry_count", snapshot.get("zip_entry_count") == 3378)
    check("snapshot_integrity_pass_crc", snapshot.get("zip_integrity_status") == "PASS_CRC")
    check("snapshot_c11c_manifest_expected_pin", snapshot.get("frozen_c11c_manifest_sha256") == EXPECTED_C11C)
    check("snapshot_embedded_manifest_observed_hash", snapshot.get("manifest_sha256_observed_in_zip") == "f6b2fc6ce36973eb620738c8446d529d98da0fb79892132cf4708e6f453051b5")
    check("snapshot_manifest_observed_bytes", snapshot.get("manifest_bytes_observed_in_zip") == 1070256)
    check("snapshot_manifest_timestamp", snapshot.get("manifest_generated_at_utc_in_zip") == "2026-10-26T00:38:03.0481714Z")
    check("snapshot_manifest_declared_source_tree", snapshot.get("manifest_source_tree_sha256_declared_in_zip") == "74c3cc20ba41ba51b131f6c42c313161409b05ffa54911790833e7312ce5ba43")
    check("snapshot_manifest_self_entry_hash", snapshot.get("manifest_sha256_declared_by_self_entry") == EXPECTED_C11C)
    check("snapshot_manifest_self_entry_bytes", snapshot.get("manifest_bytes_declared_by_self_entry") == 796318)
    check("snapshot_manifest_mismatch_explicit", snapshot.get("manifest_reconciliation_status") == "MISMATCH_STOP_AND_VERIFY_ACTIVE_CHECKOUT")
    active_manifest = root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    check("active_checkout_frozen_manifest_exists", active_manifest.is_file())
    if active_manifest.is_file():
        check("active_checkout_frozen_manifest_sha", sha(active_manifest) == EXPECTED_C11C)
        check("active_checkout_frozen_manifest_bytes", active_manifest.stat().st_size == 796318)

    lineage = receipt.get("source_lineage", {})
    check("lineage_c11c_pin", lineage.get("frozen_c11c_manifest_sha256") == EXPECTED_C11C)
    check("lineage_parent_pin_count", lineage.get("contract_declared_parent_source_pin_count") == 81)
    check("lineage_pin_list_nonempty", isinstance(lineage.get("pins"), list) and len(lineage["pins"]) >= 19)
    seen: set[str] = set()
    for i, pin in enumerate(lineage.get("pins", [])):
        label = f"receipt_source_pin_{i:02d}"
        rel = pin.get("path") if isinstance(pin, dict) else None
        expected = pin.get("sha256", "").lower() if isinstance(pin, dict) else ""
        check(label + "_shape", isinstance(pin, dict) and set(pin) == {"path", "sha256", "role"} and isinstance(rel, str) and bool(rel))
        if not isinstance(rel, str) or not rel:
            continue
        check(label + "_unique_path", rel not in seen)
        seen.add(rel)
        target = root / Path(rel)
        check(label + "_exists", target.is_file())
        if target.is_file(): check(label + "_sha_matches", sha(target) == expected)
    check("lineage_historical_receipt_path", lineage.get("historical_v1_receipt_path") == "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_V1_20261023.json")
    check("lineage_historical_receipt_sha", lineage.get("historical_v1_receipt_sha256") == EXPECTED_HISTORICAL_EVIDENCE)
    check("lineage_historical_decision_sha", lineage.get("historical_v1_decision_sha256") == EXPECTED_HISTORICAL_DECISION)
    check("lineage_design_receipt_sha", lineage.get("design_receipt_sha256") == EXPECTED_DESIGN_RECEIPT)

    # Revalidate all source pins embedded in the existing source-composition contract (81 parents).
    check("contract_current_sha", sha(contract_path) == EXPECTED_CONTRACT)
    check("contract_schema_current_sha", sha(root / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CONTRACT_SCHEMA_V1.json") == EXPECTED_CONTRACT_SCHEMA)
    check("contract_status_retained_pending", contract.get("status") == "PENDING_OPERATOR_SOURCE_RUNTIME_COMPOSITION_TEST")
    check("contract_runtime_status_retained_pending", contract.get("runtime_test_contract", {}).get("status") == "PENDING_OPERATOR_GODOT_MONO_RUN")
    authority = contract.get("source_authority", {})
    source_pins = authority.get("source_pins", [])
    check("contract_parent_pin_count_matches", authority.get("source_pin_count") == 81 and len(source_pins) == 81)
    check("contract_frozen_manifest_pin", authority.get("frozen_c11c_manifest_sha256") == EXPECTED_C11C)
    for i, pin in enumerate(source_pins):
        rel = pin.get("path", "")
        expected = pin.get("sha256", "").lower()
        target = root / Path(rel)
        check(f"contract_parent_pin_{i:02d}_exists", bool(rel) and target.is_file())
        if rel and target.is_file(): check(f"contract_parent_pin_{i:02d}_sha", sha(target) == expected)
    runtime_input_pins = authority.get("runtime_input_pins", [])
    check("contract_runtime_input_pin_count", authority.get("runtime_input_pin_count") == 6 and len(runtime_input_pins) == 6)
    for i, pin in enumerate(runtime_input_pins):
        rel = pin.get("path", "")
        expected = pin.get("sha256", "").lower()
        target = root / Path(rel)
        check(f"contract_runtime_input_pin_{i:02d}_exists", bool(rel) and target.is_file())
        if rel and target.is_file(): check(f"contract_runtime_input_pin_{i:02d}_sha", sha(target) == expected)
    rec_runtime_pins = lineage.get("runtime_input_pins", [])
    check("receipt_runtime_input_pin_count", lineage.get("runtime_input_pin_count") == 6 and len(rec_runtime_pins) == 6)
    check("receipt_runtime_input_pin_paths_exact", {x.get("path") for x in rec_runtime_pins} == set(EXPECTED_RUNTIME_INPUT_PINS))
    for i, pin in enumerate(rec_runtime_pins):
        rel = pin.get("path", "")
        expected = EXPECTED_RUNTIME_INPUT_PINS.get(rel)
        target = root / Path(rel)
        check(f"receipt_runtime_input_pin_{i:02d}_exists", bool(rel) and target.is_file())
        check(f"receipt_runtime_input_pin_{i:02d}_expected_sha", expected is not None and pin.get("sha256", "").lower() == expected)
        if rel and target.is_file() and expected: check(f"receipt_runtime_input_pin_{i:02d}_live_sha", sha(target) == expected)

    # Pin the previous receipt and its contemporaneous decision; do not rewrite history.
    hist_rel = lineage.get("historical_v1_receipt_path", "")
    hist_path = root / Path(hist_rel)
    check("historical_v1_receipt_unchanged", hist_path.is_file() and sha(hist_path) == EXPECTED_HISTORICAL_EVIDENCE)
    check("historical_decision_document_unchanged", (root / "docs/current/d/C11D_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_DECISION_V1_20261023.md").is_file() and sha(root / "docs/current/d/C11D_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_DECISION_V1_20261023.md") == EXPECTED_HISTORICAL_DECISION)
    if hist_path.is_file():
        old = load_json(hist_path)
        old_pins = old.get("source_sha256", {})
        check("historical_receipt_contract_pin_stays_old", old_pins.get("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CONTRACT_V1.json") == "d3265f1ba91dc664e85bbb0dc87ea6b145f0fed34ffa4552412c8fa70c19b2ab")
        check("historical_receipt_harness_pin_stays_old", old_pins.get("tools/c11d/d9/test_allowlisted_coordinate_consumer_source_composition_runtime.gd") == "74fe446ef69c92de0291aa739caf1b5c25dbcdaed7f9939eb1e63c9a4623cfe2")
        check("historical_receipt_static_runner_pin_stays_old", old_pins.get("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_allowlisted_coordinate_source_composition_static.py") == "5c69f08194213b7bcf48fe7f52bd17e8ec29a2d6e275c4c73787e7fa20b174ff")
    recon = receipt.get("reconciliation", {})
    check("historical_v1_retained_flag", recon.get("historical_v1_retained_unchanged") is True)
    check("historical_v1_not_current_flag", recon.get("historical_v1_applies_to_current_source_hashes") is False)
    check("contract_pending_flag", recon.get("current_source_composition_contract_status_retained_pending") is True)
    check("historical_decision_not_rewritten", recon.get("historical_acceptance_decision_rewritten") is False)

    execution = receipt.get("execution", {})
    check("godot_version_exact", execution.get("godot_version") == "4.7.1.stable.mono.official.a13da4feb")
    check("design_receipt_pin", execution.get("design_receipt_sha256") == EXPECTED_DESIGN_RECEIPT)
    static = execution.get("static_gates", [])
    static_expected = {
       "runtime_static_v1": (113, "ca63239a81d23fd3bef046db02c67d7565aa4b24aefef4c1b849af71d1ecef8e", EXPECTED_STATIC_V1),
       "runtime_static_v2": (115, "bbf030cb4aa8319d007eae259a7dac52294a29fc9cddd1d242b09306b25548df", EXPECTED_STATIC_V2),
       "composition_static": (132, "74aad0a3ef62052e211932328d0a7d780c00ea1bb1bc1c118c2ff01a4e30a84f", EXPECTED_STATIC_COMPOSITION),
    }
    check("three_static_gates_exact", len(static) == 3 and {x.get("name") for x in static} == set(static_expected))
    for item in static:
        exp = static_expected.get(item.get("name"))
        if exp:
            n, out_sha, src_sha = exp
            check(item["name"] + "_status_pass", item.get("status") == "PASS")
            check(item["name"] + "_count", item.get("checks") == n)
            check(item["name"] + "_exit", item.get("exit_code") == 0)
            check(item["name"] + "_stdout_sha", item.get("stdout_sha256") == out_sha)
            check(item["name"] + "_stderr_empty_sha", item.get("stderr_sha256") == EXPECTED_EMPTY_SHA)
            check(item["name"] + "_source_sha", item.get("source_sha256") == src_sha)

    runtime = execution.get("runtime", {})
    check("runtime_exit_zero", runtime.get("operator_reported_exit_code") == 0 and summary.get("runtime_exit_code") == 0)
    check("runtime_stdout_receipt_sha", runtime.get("stdout_sha256") == EXPECTED_RUNTIME_STDOUT and sha(out_path) == EXPECTED_RUNTIME_STDOUT and summary.get("stdout_sha256", "").lower() == EXPECTED_RUNTIME_STDOUT)
    check("runtime_stderr_empty", runtime.get("stderr_sha256") == EXPECTED_EMPTY_SHA and hashlib.sha256(stderr_bytes).hexdigest() == EXPECTED_EMPTY_SHA and summary.get("stderr_sha256", "").lower() == EXPECTED_EMPTY_SHA)
    check("summary_pass_marker", summary.get("expected_pass_marker_present") is True)
    check("summary_failure_marker_false", summary.get("failure_or_error_marker_present") is False)
    check("summary_1680_marker", summary.get("output_mentions_1680") is True)
    check("summary_renderer_off", summary.get("renderer") == "OFF")
    check("summary_media_false", summary.get("media_created") is False)
    check("summary_payload_false", summary.get("payload_materialized") is False)
    check("summary_production_calls_zero", summary.get("production_calls") == 0)
    check("summary_not_promoted", summary.get("repository_evidence_promoted") is False)
    check("pass_marker_exactly_once", stdout.count(PASS_MARKER) == 1)
    check("fail_marker_absent", FAIL_MARKER not in stdout and "_FAILURE=" not in stdout)
    check("no_runtime_error_markers", re.search(r"(?im)(SCRIPT ERROR:|ERROR:)", stdout) is None and not stderr_bytes)
    candidate_matches = re.findall(r"^C11D_V2B_SOURCE_COMPOSITION_CANDIDATE_PASS=(CHALLENGE_\d{3});frames=(\d+)$", stdout, re.M)
    check("four_expected_candidate_pass_markers", sorted(candidate_matches) == sorted([(x, "420") for x in ["CHALLENGE_003","CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"]]))
    for marker_index, marker in enumerate([
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CANDIDATES=4/4",
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_SOURCE_FRAMES=1680/1680",
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_MARKER_FRAMES=1680/1680",
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_CUSTOM_DATA_LOOKUPS_PER_FRAME=1",
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_HARNESS_CUSTOM_DATA_READS=0",
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RAW_CUSTOM_DATA_LOGGED=false",
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_RENDERER=OFF",
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_PRODUCTION_CALLS=0",
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_MEDIA_CREATED=false",
       "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_SOURCE_COMPOSITION_C11C_IMMUTABLE=true",
    ]):
        check(f"runtime_marker_{marker_index:02d}", marker in stdout)

    observed = receipt.get("observed_runtime_markers", {})
    check("observed_candidates", observed.get("candidates_passed") == "4/4")
    check("observed_source_frames", observed.get("source_frames") == "1680/1680")
    check("observed_marker_frames", observed.get("marker_frames") == "1680/1680")
    check("observed_lookups", observed.get("custom_data_lookups_per_frame") == 1)
    check("observed_harness_reads", observed.get("harness_custom_data_reads") == 0)
    check("observed_raw_logging_false", observed.get("raw_custom_data_logged") is False)
    check("observed_renderer_off", observed.get("renderer") == "OFF")
    check("observed_production_calls_zero", observed.get("production_calls") == 0)
    check("observed_media_false", observed.get("media_created") is False)
    check("observed_c11c_immutable", observed.get("c11c_immutable") is True)
    locks = receipt.get("governance_locks", {})
    expected_locks = {
      "renderer":"OFF", "media_created":False, "payload_materialized":False, "candidate_input_admissible":False,
      "seed_domains_complete_for_candidate_input":False, "automatic_seed_generation":False, "master_seed":"NOT_ADOPTED",
      "approved_bindings":0, "approved_custom_data_bindings":0, "approved_renderer_projection_bindings":0,
      "D4.8":"BLOCKED", "D9.10":"PREPARE_ONLY", "D9.14":"BLOCKED", "D9.16":"BLOCKED",
      "D9.17":"BLOCKED_NO_GO", "D10":"BLOCKED_FOR_PROMOTION", "baseline_approval":"MISSING",
      "freeze_eligible":False, "release_authority":"NONE", "runtime_implementation_authorized_for_production":False,
      "render_test_authorized":False, "production_dispatch":False
    }
    check("governance_lock_set_exact", locks == expected_locks)
    check("next_gate_requires_review_not_integration", receipt.get("next_gate") == "VERIFY_ACTIVE_FROZEN_C11C_MANIFEST_THEN_VALIDATE_V2_EVIDENCE_RECEIPT_AND_COMPLETE_SEPARATE_OPERATOR_REVIEW; NO_PRODUCTION_INTEGRATION")

    failed = [name for name, ok in checks if not ok]
    print(f"C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_CHECKS={len(checks)-len(failed)}/{len(checks)}")
    print("C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_RECEIPT_SHA256=" + sha(receipt_path))
    print("C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_SCHEMA_SHA256=" + sha(schema_path))
    print("C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_VALIDATION_STATUS=" + ("PASS_RECEIPT_AND_CURRENT_SOURCE_PINS" if not failed else "FAIL"))
    print("C11D_V2B_SOURCE_COMPOSITION_FORMAL_OPERATOR_REVIEW_REQUIRED=true")
    print("C11D_V2B_SOURCE_COMPOSITION_PRODUCTION_INTEGRATION_AUTHORIZED=false")
    print("C11D_V2B_SOURCE_COMPOSITION_RENDERER=OFF")
    print("C11D_V2B_SOURCE_COMPOSITION_MEDIA_CREATED=false")
    for name in failed:
        print("C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_FAILURE=" + name, file=sys.stderr)
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
