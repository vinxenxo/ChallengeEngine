#!/usr/bin/env python3
"""Read-only V2-B runtime evidence audit. Emits only hashes and typed metadata."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

REPORT_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-REPORT-V1"
RECEIPT_ID = "C11D-V2B-RUNTIME-IMPLEMENTATION-TEST-RECEIPT-V1"
RUNTIME_RECEIPT_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-RECEIPT-V1"
AUDIT_ID = "C11D-V2B-CANDIDATE-EVIDENCE-AUDIT-V1"
FROZEN_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
DESIGN_SHA = "e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc"
MATRIX_SHA = "d69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a"
V2C_SHA = "6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c"
RUNTIME_CONTRACT_SHA = "f89235640f40c81be6100f01f1007ed4e787990a1bbf7927fcd8d676ef2cb9a3"
ROLES = ["BASELINE_R1", "BASELINE_R2", "GAMEPLAY_SEED_MUTATION", "MUSIC_SEED_MUTATION", "EDITORIAL_MUTATION"]
IDS = [f"CHALLENGE_{i:03d}" for i in range(1, 10)]
CANDIDATES = {
    "CHALLENGE_001": None, "CHALLENGE_002": None, "CHALLENGE_003": ("target_x", "float"),
    "CHALLENGE_004": None, "CHALLENGE_005": ("target_position", "Vector2"),
    "CHALLENGE_006": ("target_position", "Vector2"), "CHALLENGE_007": ("target_position", "Vector2"),
    "CHALLENGE_008": ("active_selection", "int"), "CHALLENGE_009": ("displayed_count", "int"),
}
HEX = re.compile(r"^[a-f0-9]{64}$")

class AuditError(Exception):
    pass

def need(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)

def is_sha(value: Any) -> bool:
    return isinstance(value, str) and HEX.fullmatch(value) is not None

def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuditError(f"{label} unreadable or invalid: {exc}") from exc
    need(isinstance(data, dict), f"{label} must be a JSON object")
    return data

def role_map(runs: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    need([x.get("role") for x in runs] == ROLES, f"{label}: role order/denominator mismatch")
    return {x["role"]: x for x in runs}

def candidate_hash_map(receipt: Mapping[str, Any]) -> dict[str, str]:
    return {str(x["field"]): str(x["value_stream_sha256"]) for x in receipt["candidate_field_observations"]}

def validate_report(report: Any, design: Mapping[str, Any], receipt: Mapping[str, Any], expected_receipt_sha: str) -> dict[str, Any]:
    need(isinstance(report, dict), "runtime report must be a JSON object")
    required = {
        "schema", "schema_version", "status", "runtime_contract_sha256", "design_contract_sha256", "frozen_manifest_sha256",
        "selector_count_expected", "selectors", "planner_invocations", "planner_invocations_expected", "godot_version_probe_invocations",
        "godot_runtime_process_invocations", "godot_runtime_processes_expected", "payload_materialized", "media_created",
        "approved_bindings", "approved_custom_data_bindings", "visual_seed_sensitivity", "governance_locks", "evidence"
    }
    need(set(report) == required, "runtime report root fields mismatch")
    need(report["schema"] == REPORT_ID and report["schema_version"] == "1.0", "runtime report identity mismatch")
    need(report["status"] == "PASS_SAFE_PROJECTION_SEED_SENSITIVITY", "runtime report is not accepted")
    need(report["runtime_contract_sha256"] == RUNTIME_CONTRACT_SHA, "runtime contract pin mismatch")
    need(report["design_contract_sha256"] == DESIGN_SHA and report["frozen_manifest_sha256"] == FROZEN_SHA, "design/frozen pin mismatch")
    need(report["selector_count_expected"] == 9 and len(report["selectors"]) == 9, "selector denominator mismatch")
    need(report["planner_invocations"] == report["planner_invocations_expected"] == 45, "planner invocation denominator mismatch")
    need(report["godot_runtime_process_invocations"] == report["godot_runtime_processes_expected"] == 45, "Godot process denominator mismatch")
    need(report["godot_version_probe_invocations"] == 1, "Godot version probe count mismatch")
    need(report["payload_materialized"] is False and report["media_created"] is False, "runtime evidence indicates prohibited side effect")
    need(report["approved_bindings"] == 0 and report["approved_custom_data_bindings"] == 0, "approved binding count changed")
    need(report["visual_seed_sensitivity"] == "ACCEPTED_BY_SAFE_PROJECTION_HASH", "safe-state seed sensitivity not accepted")

    locks = report["governance_locks"]
    # The runtime contract deliberately stores approved-binding counts at the
    # report root, not inside governance_locks. Keep this map byte-for-byte
    # aligned with the canonical runtime GOVERNANCE object.
    locked = {
        "renderer": "OFF", "media_created": False, "payload_materialized": False,
        "candidate_input_admissible": False, "seed_domains_complete_for_candidate_input": False,
        "automatic_seed_generation": False, "master_seed": "NOT_ADOPTED",
        "D4.8": "BLOCKED", "D9.10": "PREPARE_ONLY",
        "D9.14": "BLOCKED", "D9.16": "BLOCKED", "D9.17": "BLOCKED_NO_GO",
        "D10": "BLOCKED_FOR_PROMOTION", "baseline_approval": "MISSING", "freeze_eligible": False,
        "release_authority": "NONE",
        "visual_seed_sensitivity": "NOT_TESTED_UNTIL_V2B_RUNTIME_ACCEPTED",
        "challenge_008_009_phase_timeline_acceptance": "BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY",
        "challenge_004_v1_fixture": "IMMUTABLE"
    }
    need(locks == locked, "governance lock map mismatch")

    evidence = report["evidence"]
    need(isinstance(evidence, dict), "runtime evidence object missing")
    need(evidence.get("godot_version_probe_exit_code") == 0, "runner's own Godot version probe did not pass")
    gv = str(evidence.get("godot_version", ""))
    need("4.7.1" in gv and "mono" in gv.lower(), "runner Godot version is not 4.7.1 Mono")
    need(evidence.get("failure") in (None, "", False), "runtime report contains a failure")
    need(evidence.get("implementation_test_receipt_sha256") == expected_receipt_sha, "runtime report is not bound to the static receipt")
    need(evidence.get("source_pin_errors_before_runtime") == [] and evidence.get("source_pin_errors_after_runtime") == [], "source pin errors present in runtime report")

    design_selectors = design.get("selectors")
    need(isinstance(design_selectors, list) and [s.get("challenge_id") for s in design_selectors] == IDS, "design selector list mismatch")
    selector_map = {s["challenge_id"]: s for s in design_selectors}
    used_pids: set[int] = set()
    used_run_ids: set[str] = set()
    summaries: list[dict[str, Any]] = []
    total_planners = total_runs = 0

    row_fields = {"selector", "status", "block_reasons", "planner_variants", "runtime_runs", "comparison"}
    receipt_fields = {"schema", "schema_version", "status", "selector", "process", "runtime", "lineage", "identity", "seeds", "simulation_input_sha256", "source_frames", "source_timebase", "source_asset_pins", "candidate_field_observations", "authority"}
    for index, row in enumerate(report["selectors"]):
        need(isinstance(row, dict) and set(row) == row_fields, f"selector row {index} fields mismatch")
        cid = IDS[index]
        design_selector = selector_map[cid]
        need(row["selector"] == {"challenge_id": cid, "mechanic": design_selector["mechanic"]}, f"selector identity mismatch: {cid}")
        need(row["status"] == "ACCEPTED_SAFE_PROJECTION_RUNTIME" and row["block_reasons"] == [], f"selector not accepted: {cid}")
        planners = row["planner_variants"]
        runs = row["runtime_runs"]
        need(isinstance(planners, list) and len(planners) == 5, f"planner row incomplete: {cid}")
        need(isinstance(runs, list) and len(runs) == 5, f"runtime row incomplete: {cid}")
        pmap = role_map(planners, f"{cid} planner")
        rmap = role_map(runs, f"{cid} runtime")
        total_planners += len(planners); total_runs += len(runs)
        for role in ROLES:
            p = pmap[role]
            for digest_key in ("request_hash", "plan_hash", "editorial_hash"):
                need(is_sha(p.get(digest_key)), f"{cid}/{role}: invalid planner {digest_key}")
            need(p.get("status") == "PLANNED" and p.get("bridge_status") == "PLANNING_ONLY_NOT_RENDERABLE", f"{cid}/{role}: planner/bridge status changed")
            need(p.get("adapter_status") == "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED", f"{cid}/{role}: D9.10 adapter status changed")
            need(p.get("request_id") == f"C11D-V2B-{cid}", f"{cid}/{role}: request identity mismatch")

            run = rmap[role]
            need(run.get("exit_code") == 0 and isinstance(run.get("receipt"), dict), f"{cid}/{role}: runtime receipt/exit missing")
            need(isinstance(run.get("process_id"), int) and run["process_id"] > 0, f"{cid}/{role}: invalid process ID")
            need(run["process_id"] not in used_pids, f"process ID reused: {run['process_id']}")
            used_pids.add(run["process_id"])
            need(isinstance(run.get("run_id"), str) and run["run_id"] not in used_run_ids, f"run ID reused: {run.get('run_id')}")
            used_run_ids.add(run["run_id"])
            need(is_sha(run.get("stdout_sha256")) and is_sha(run.get("stderr_sha256")) and is_sha(run.get("receipt_sha256")), f"{cid}/{role}: malformed runtime hashes")
            r = run["receipt"]
            need(set(r) == receipt_fields, f"{cid}/{role}: receipt fields mismatch")
            need(r["schema"] == RUNTIME_RECEIPT_ID and r["schema_version"] == "1.0" and r["status"] == "SAFE_PROJECTION_RECEIPT", f"{cid}/{role}: receipt identity mismatch")
            need(r["selector"] == {"challenge_id": cid, "mechanic": design_selector["mechanic"]}, f"{cid}/{role}: receipt selector mismatch")
            need(r["process"] == {"run_id": run["run_id"], "process_id": run["process_id"], "variant_role": role, "exit_code": 0}, f"{cid}/{role}: receipt process mismatch")
            lin = r["lineage"]
            need(lin.get("runtime_contract_sha256") == RUNTIME_CONTRACT_SHA and lin.get("design_contract_sha256") == DESIGN_SHA and lin.get("frozen_manifest_sha256") == FROZEN_SHA, f"{cid}/{role}: lineage authority mismatch")
            need(lin.get("challenge_source_sha256") == design_selector["challenge_source_sha256"] and lin.get("mechanic_source_sha256") == design_selector["mechanic_source_sha256"], f"{cid}/{role}: source/mechanic lineage mismatch")
            need(lin.get("verified_source_pin_count") == 81 and lin.get("verified_authority_input_pin_count") == 9, f"{cid}/{role}: pin counts are incomplete")
            ident = r["identity"]
            for key in ("canonical_request_hash", "canonical_plan_hash", "editorial_hash", "projection_instance_identity_sha256", "safe_projection_state_sha256"):
                need(is_sha(ident.get(key)), f"{cid}/{role}: malformed identity {key}")
            need(ident["canonical_request_hash"] == p["request_hash"] and ident["canonical_plan_hash"] == p["plan_hash"] and ident["editorial_hash"] == p["editorial_hash"], f"{cid}/{role}: planner/receipt identity mismatch")
            need(ident.get("payload_identity") == "NOT_CREATED", f"{cid}/{role}: payload identity was created")
            agg = ident.get("candidate_field_probe_sha256")
            need(agg is None or is_sha(agg), f"{cid}/{role}: invalid aggregate candidate hash")
            need(r.get("simulation_input_sha256") is None or is_sha(r.get("simulation_input_sha256")), f"{cid}/{role}: invalid simulation input hash")
            frames = r["source_frames"]
            need(isinstance(frames.get("count"), int) and frames["count"] > 0 and frames.get("count") == frames.get("expected_game_frames"), f"{cid}/{role}: frame cardinality mismatch")
            need(frames.get("coordinate_transform") == "NONE" and frames.get("resampling") == "PROHIBITED", f"{cid}/{role}: projection policy changed")
            need(frames.get("projection_sha256") == ident["safe_projection_state_sha256"], f"{cid}/{role}: projection/state hashes disagree")
            conflict = cid in ("CHALLENGE_008", "CHALLENGE_009")
            phase = "BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY" if conflict else "NOT_EVALUATED_SOURCE_FRAME_ONLY"
            need(r["source_timebase"].get("known_conflict") is conflict and r["source_timebase"].get("phase_timeline_acceptance") == phase, f"{cid}/{role}: timebase policy changed")
            need(r["seeds"].get("requested_gameplay_seed") == p.get("gameplay_seed") and r["seeds"].get("music_seed_request_domain") == p.get("music_seed") and r["seeds"].get("music_seed_copied_into_simulation") is False, f"{cid}/{role}: seed domains mismatch")
            cand = CANDIDATES[cid]
            observations = r["candidate_field_observations"]
            need(isinstance(observations, list), f"{cid}/{role}: candidate observations are not a list")
            if cand is None:
                need(observations == [] and agg is None, f"{cid}/{role}: unexpected candidate observation")
            else:
                need(len(observations) == 1, f"{cid}/{role}: expected one candidate observation")
                obs = observations[0]
                field, semantic_type = cand
                keys = {"field", "semantic_type", "present_frames", "type_histogram", "value_stream_sha256", "raw_values_emitted", "renderer_binding_approved"}
                need(set(obs) == keys, f"{cid}/{role}: candidate observation includes unexpected/raw fields")
                need(obs["field"] == field and obs["semantic_type"] == semantic_type, f"{cid}/{role}: candidate field/type mismatch")
                need(obs["present_frames"] == frames["count"] and obs["type_histogram"] == {semantic_type: frames["count"]}, f"{cid}/{role}: candidate type/cardinality mismatch")
                need(is_sha(obs["value_stream_sha256"]) and obs["raw_values_emitted"] is False and obs["renderer_binding_approved"] is False, f"{cid}/{role}: candidate disclosure/approval policy changed")
                need(is_sha(agg), f"{cid}/{role}: candidate aggregate hash is absent")
            auth = r["authority"]
            need(auth == {"approved_bindings": 0, "approved_custom_data_bindings": 0, "renderer": "OFF", "payload_materialized": False, "media_created": False, "release_authority": "NONE"}, f"{cid}/{role}: receipt authority lock changed")

        # Cross-role identity/determinism requirements, independently recomputed from receipts.
        base = rmap[ROLES[0]]["receipt"]; repeat = rmap[ROLES[1]]["receipt"]
        game = rmap[ROLES[2]]["receipt"]; music = rmap[ROLES[3]]["receipt"]; editorial = rmap[ROLES[4]]["receipt"]
        bp = pmap[ROLES[0]]; rp = pmap[ROLES[1]]; gp = pmap[ROLES[2]]; mp = pmap[ROLES[3]]; ep = pmap[ROLES[4]]
        bi, ri, gi, mi, ei = [x["identity"] for x in (base, repeat, game, music, editorial)]
        bprobe, rprobe, gprobe, mprobe, eprobe = [candidate_hash_map(x) for x in (base, repeat, game, music, editorial)]
        need(bp["request_hash"] == rp["request_hash"] and bp["plan_hash"] == rp["plan_hash"] and bp["editorial_hash"] == rp["editorial_hash"], f"{cid}: planner baseline repeats diverge")
        need(bi["projection_instance_identity_sha256"] == ri["projection_instance_identity_sha256"] and bi["safe_projection_state_sha256"] == ri["safe_projection_state_sha256"] and bprobe == rprobe, f"{cid}: baseline state/candidate repeat diverges")
        need(bi["canonical_request_hash"] == ri["canonical_request_hash"] and bi["canonical_plan_hash"] == ri["canonical_plan_hash"] and bi["editorial_hash"] == ri["editorial_hash"], f"{cid}: baseline receipt identities diverge")
        need(rmap[ROLES[0]]["process_id"] != rmap[ROLES[1]]["process_id"] and rmap[ROLES[0]]["run_id"] != rmap[ROLES[1]]["run_id"], f"{cid}: baseline processes are not independent")
        need(gi["safe_projection_state_sha256"] != bi["safe_projection_state_sha256"], f"{cid}: gameplay seed does not change base projection")
        need(mi["safe_projection_state_sha256"] == bi["safe_projection_state_sha256"] and mprobe == bprobe and music["simulation_input_sha256"] == base["simulation_input_sha256"], f"{cid}: music mutation leaks into state/candidate")
        need(ei["safe_projection_state_sha256"] == bi["safe_projection_state_sha256"] and eprobe == bprobe and editorial["simulation_input_sha256"] == base["simulation_input_sha256"], f"{cid}: editorial mutation leaks into state/candidate")
        need(gp["gameplay_seed"] != bp["gameplay_seed"] and gp["music_seed"] == bp["music_seed"], f"{cid}: gameplay seed domain crossed")
        need(mp["music_seed"] != bp["music_seed"] and mp["gameplay_seed"] == bp["gameplay_seed"], f"{cid}: music seed domain crossed")
        need(ep["editorial_hash"] != bp["editorial_hash"] and ep["gameplay_seed"] == bp["gameplay_seed"] and ep["music_seed"] == bp["music_seed"], f"{cid}: editorial variant invalid")
        for role in (ROLES[2], ROLES[3], ROLES[4]):
            ix = role_map(planners, f"{cid} planner")[role]
            need(ix["request_hash"] != bp["request_hash"] and ix["plan_hash"] != bp["plan_hash"], f"{cid}/{role}: canonical request/plan identity did not change")
        need(row["comparison"].get("status") == "PASS", f"{cid}: report comparison status is not PASS")
        for key in ("baseline_repeat_agreement", "gameplay_seed_safe_state_changed", "music_seed_safe_state_and_candidates_invariant", "editorial_safe_state_and_candidates_invariant"):
            need(row["comparison"].get(key) is True, f"{cid}: comparison oracle failed: {key}")

        expected_fields = set() if CANDIDATES[cid] is None else {CANDIDATES[cid][0]}
        relations = row["comparison"].get("candidate_probe_relations")
        need(isinstance(relations, dict) and set(relations) == expected_fields, f"{cid}: candidate comparison scope mismatch")
        candidate_summary = []
        if expected_fields:
            field, semantic_type = CANDIDATES[cid]
            actual_hashes = {role: candidate_hash_map(rmap[role]["receipt"])[field] for role in ROLES}
            relation = relations[field]
            need(relation.get("baseline_sha256") == actual_hashes["BASELINE_R1"], f"{cid}: candidate baseline hash mismatch")
            need(relation.get("gameplay_variant_sha256") == actual_hashes["GAMEPLAY_SEED_MUTATION"], f"{cid}: candidate gameplay hash mismatch")
            need(relation.get("music_variant_sha256") == actual_hashes["MUSIC_SEED_MUTATION"], f"{cid}: candidate music hash mismatch")
            need(relation.get("editorial_variant_sha256") == actual_hashes["EDITORIAL_MUTATION"], f"{cid}: candidate editorial hash mismatch")
            expected_game_relation = actual_hashes["GAMEPLAY_SEED_MUTATION"] == actual_hashes["BASELINE_R1"] if field == "target_x" else actual_hashes["GAMEPLAY_SEED_MUTATION"] != actual_hashes["BASELINE_R1"]
            need(relation.get("gameplay_relation_pass") is expected_game_relation and relation.get("music_invariant_pass") is True and relation.get("editorial_invariant_pass") is True, f"{cid}: candidate field relation oracle mismatch")
            candidate_summary.append({
                "field": field, "semantic_type": semantic_type, "present_frames": rmap[ROLES[0]]["receipt"]["candidate_field_observations"][0]["present_frames"], "binding_status": "OBSERVED_NOT_APPROVED",
                "hash_by_role": actual_hashes,
                "gameplay_seed_relation_pass": expected_game_relation,
                "music_seed_invariant_pass": True, "editorial_invariant_pass": True,
                "raw_values_included": False, "renderer_binding_approved": False
            })

        summaries.append({
            "challenge_id": cid, "mechanic": design_selector["mechanic"], "status": "ACCEPTED_SAFE_PROJECTION_RUNTIME",
            "baseline_repeat_agreement": True, "gameplay_seed_safe_state_changed": True,
            "music_seed_safe_state_and_candidates_invariant": True,
            "editorial_safe_state_and_candidates_invariant": True,
            "payload_identity": "NOT_CREATED", "candidate_observations": candidate_summary,
            "source_frame_only": True,
            "timeline_acceptance": "BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY" if cid in ("CHALLENGE_008", "CHALLENGE_009") else "NOT_EVALUATED_SOURCE_FRAME_ONLY",
            "safe_state_hash_by_role": {role: rmap[role]["receipt"]["identity"]["safe_projection_state_sha256"] for role in ROLES},
            "canonical_request_hash_by_role": {role: rmap[role]["receipt"]["identity"]["canonical_request_hash"] for role in ROLES},
            "canonical_plan_hash_by_role": {role: rmap[role]["receipt"]["identity"]["canonical_plan_hash"] for role in ROLES},
        })

    need(total_planners == 45 and total_runs == 45 and len(used_pids) == 45 and len(used_run_ids) == 45, "45/45 unique planner/runtime execution proof missing")
    need(receipt.get("schema") == RECEIPT_ID and receipt.get("status") == "PASS_IMPLEMENTATION_STATIC_TESTS" and receipt.get("test_count") == 198, "static implementation receipt not accepted")
    need(receipt.get("source_pin_count") == 81 and receipt.get("authority_input_pin_count") == 9, "static receipt pin denominators mismatch")
    need(receipt.get("runtime_contract_sha256") == RUNTIME_CONTRACT_SHA and receipt.get("design_contract_sha256") == DESIGN_SHA and receipt.get("frozen_manifest_sha256") == FROZEN_SHA, "static receipt authority pins mismatch")

    return {
        "schema": AUDIT_ID, "schema_version": "1.0", "status": "PASS_CANDIDATE_EVIDENCE_AUDIT",
        "runtime_report_sha256": None, "implementation_test_receipt_sha256": expected_receipt_sha,
        "runtime_contract_sha256": RUNTIME_CONTRACT_SHA, "design_contract_sha256": DESIGN_SHA,
        "seed_matrix_sha256": MATRIX_SHA, "v2c_source_frame_contract_sha256": V2C_SHA,
        "frozen_manifest_sha256": FROZEN_SHA, "selector_count": 9,
        "planner_invocations": 45, "godot_runtime_processes": 45,
        "godot_version": str(evidence["godot_version"]), "source_pin_count": 81,
        "authority_input_pin_count": 9, "approved_bindings": 0, "approved_custom_data_bindings": 0,
        "candidate_input_admissible": False, "payload_materialized": False, "media_created": False,
        "renderer": "OFF", "release_authority": "NONE", "candidate_binding_status": "OBSERVED_NOT_APPROVED",
        "selectors": summaries,
        "next_gate": "REVIEW_CANDIDATE_SEMANTICS_AND_SEPARATE_EXPLICIT_APPROVAL; NO_PAYLOAD_CONSUMER",
        "raw_candidate_values_included": False
    }

def verify_active_sources(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    frozen = root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    design_path = root / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_V1.json"
    matrix_path = root / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json"
    v2c_path = root / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json"
    contract_path = root / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json"
    for path, expected, label in (
        (frozen, FROZEN_SHA, "frozen C11-C manifest"), (design_path, DESIGN_SHA, "V2-B design"),
        (matrix_path, MATRIX_SHA, "V2-B seed matrix"), (v2c_path, V2C_SHA, "V2-C source-frame contract"),
        (contract_path, RUNTIME_CONTRACT_SHA, "V2-B runtime contract")):
        need(path.is_file(), f"missing {label}: {path}")
        actual = sha_file(path)
        need(actual == expected, f"{label} SHA mismatch: {actual}")
    design = load_json(design_path, "V2-B design")
    matrix = load_json(matrix_path, "V2-B seed matrix")
    need(len(design.get("source_pins", [])) == 81 and len(design.get("authority_input_pins", [])) == 9, "design pins denominator mismatch")
    for pin in design["source_pins"]:
        p = root / str(pin["path"])
        need(p.is_file() and sha_file(p) == pin["sha256"], f"source pin drift: {pin['path']}")
    for pin in design["authority_input_pins"]:
        p = root / str(pin["path"])
        need(p.is_file() and sha_file(p) == pin["sha256"], f"authority pin drift: {pin['path']}")
    need(matrix.get("status") == "DESIGN_ONLY_NOT_EXECUTED", "V2-B matrix design status unexpectedly changed")
    return design, matrix

def run(args: argparse.Namespace) -> dict[str, Any]:
    root = args.repo_root.resolve()
    report_path = args.runtime_report.resolve()
    receipt_path = args.implementation_test_receipt.resolve()
    out_dir = args.output_dir.resolve()
    need(report_path.is_file() and receipt_path.is_file(), "runtime report/static receipt not found")
    need(out_dir.is_dir(), "output directory must already exist")
    output_path = out_dir / "candidate_evidence_audit.json"
    need(not output_path.exists(), "audit output already exists; refusing overwrite")
    report_sha = sha_file(report_path)
    receipt_sha = sha_file(receipt_path)
    need(report_sha == args.expected_runtime_report_sha256.lower(), f"runtime report SHA mismatch: {report_sha}")
    need(receipt_sha == args.expected_implementation_test_receipt_sha256.lower(), f"implementation receipt SHA mismatch: {receipt_sha}")
    design, _matrix = verify_active_sources(root)
    report = load_json(report_path, "runtime report")
    receipt = load_json(receipt_path, "implementation test receipt")
    report_dir = report_path.parent
    need(str(Path(str(report.get("evidence", {}).get("directory", ""))).resolve()) == str(report_dir), "report evidence directory does not match report location")
    hashes = report.get("evidence", {}).get("evidence_file_sha256")
    need(isinstance(hashes, dict) and len(hashes) >= 90, "runtime report does not pin at least 90 individual evidence files")
    expected_names = set()
    for name, digest in hashes.items():
        need(isinstance(name, str) and name == Path(name).name and name not in ("", ".", ".."), f"unsafe evidence filename: {name!r}")
        need(is_sha(digest), f"malformed evidence file hash: {name}")
        path = report_dir / name
        need(path.is_file(), f"runtime evidence file missing: {name}")
        need(sha_file(path) == digest, f"runtime evidence file hash mismatch: {name}")
        expected_names.add(name)
    actual_names = {p.name for p in report_dir.iterdir() if p.is_file() and p.name != "report.json"}
    need(actual_names == expected_names, "runtime evidence directory has missing or unpinned extra files")
    summary = validate_report(report, design, receipt, receipt_sha)
    summary["runtime_report_sha256"] = report_sha
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
    # Final source check after the read-only audit and output generation.
    try:
        verify_active_sources(root)
    except Exception:
        if output_path.exists():
            output_path.unlink()
        raise
    print("C11D_V2B_CANDIDATE_EVIDENCE_AUDIT=PASS")
    print("C11D_V2B_CANDIDATE_EVIDENCE_SELECTORS=9/9")
    print("C11D_V2B_CANDIDATE_EVIDENCE_PLANNER=45/45")
    print("C11D_V2B_CANDIDATE_EVIDENCE_GODOT=45/45")
    print("C11D_V2B_CANDIDATE_EVIDENCE_PINS=81/81")
    print("C11D_V2B_CANDIDATE_EVIDENCE_AUTHORITY_PINS=9/9")
    print("C11D_V2B_CANDIDATE_BINDINGS_APPROVED=0")
    print(f"C11D_V2B_CANDIDATE_EVIDENCE_REPORT_SHA256={report_sha}")
    print(f"C11D_V2B_CANDIDATE_EVIDENCE_AUDIT_JSON={output_path}")
    print(f"C11D_V2B_CANDIDATE_EVIDENCE_AUDIT_JSON_SHA256={sha_file(output_path)}")
    return summary

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--runtime-report", required=True, type=Path)
    parser.add_argument("--expected-runtime-report-sha256", required=True)
    parser.add_argument("--implementation-test-receipt", required=True, type=Path)
    parser.add_argument("--expected-implementation-test-receipt-sha256", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    for label, value in (("runtime report SHA", args.expected_runtime_report_sha256), ("implementation receipt SHA", args.expected_implementation_test_receipt_sha256)):
        if not is_sha(value.lower()):
            print("C11D_V2B_CANDIDATE_EVIDENCE_AUDIT=BLOCKED", file=sys.stderr)
            print(f"invalid {label}", file=sys.stderr)
            return 2
    try:
        run(args)
        return 0
    except (AuditError, OSError, ValueError, KeyError, TypeError) as exc:
        print("C11D_V2B_CANDIDATE_EVIDENCE_AUDIT=BLOCKED", file=sys.stderr)
        print(f"C11D_V2B_CANDIDATE_EVIDENCE_DIAGNOSTIC={type(exc).__name__}:{exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
