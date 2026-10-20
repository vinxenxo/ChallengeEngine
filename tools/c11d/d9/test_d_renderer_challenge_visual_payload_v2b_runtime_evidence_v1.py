import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_d_renderer_challenge_visual_payload_v2b_runtime_evidence_v1.py"
spec = importlib.util.spec_from_file_location("v2b_audit", AUDIT_PATH)
audit = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = audit
spec.loader.exec_module(audit)

ROLES = audit.ROLES
IDS = audit.IDS

def h(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def fixture():
    design = {"selectors": []}
    rows = []
    for cid in IDS:
        candidate = audit.CANDIDATES[cid]
        mechanic = cid.removeprefix("CHALLENGE_").lower()
        selector = {"challenge_id": cid, "mechanic": mechanic,
                    "challenge_source_sha256": h(cid+"source"), "mechanic_source_sha256": h(cid+"mechanic")}
        design["selectors"].append(selector)
        planner=[]; runs=[]
        for ri, role in enumerate(ROLES):
            request_hash = h(cid+"req-base") if ri in (0,1) else h(cid+"req-"+role)
            plan_hash = h(cid+"plan-base") if ri in (0,1) else h(cid+"plan-"+role)
            editorial_hash = h(cid+"editorial-base") if ri != 4 else h(cid+"editorial-mut")
            gameplay_seed = 11 if ri != 2 else 12
            music_seed = 840001 if ri != 3 else 840002
            planner.append({"role":role,"status":"PLANNED","request_hash":request_hash,"plan_hash":plan_hash,
                "editorial_hash":editorial_hash,"gameplay_seed":gameplay_seed,"music_seed":music_seed,
                "bridge_status":"PLANNING_ONLY_NOT_RENDERABLE","adapter_status":"PREPARED_NOT_DISPATCHED_RENDERER_DISABLED",
                "request_id":f"C11D-V2B-{cid}","editorial_mutation_applied":ri==4})
            state_base=h(cid+"state-base")
            state=h(cid+"state-game") if ri==2 else state_base
            process_id=(len(IDS)*ri + IDS.index(cid)+2000)
            run_id=f"{cid}_{role}"
            if candidate is None:
                observations=[]; aggregate=None; probe_map={}
            else:
                field,typ=candidate
                base_value=h(cid+field+"baseline")
                if field=="target_x": game_value=base_value
                else: game_value=h(cid+field+"game")
                value=base_value if ri in (0,1,3,4) else game_value
                observations=[{"field":field,"semantic_type":typ,"present_frames":12,"type_histogram":{typ:12},
                    "value_stream_sha256":value,"raw_values_emitted":False,"renderer_binding_approved":False}]
                aggregate=h(cid+field+"agg-"+role)
                probe_map={field:value}
            identity={"canonical_request_hash":request_hash,"canonical_plan_hash":plan_hash,"editorial_hash":editorial_hash,
                "projection_instance_identity_sha256":h(cid+"projection"),"safe_projection_state_sha256":state,
                "candidate_field_probe_sha256":aggregate,"payload_identity":"NOT_CREATED"}
            conflict=cid in ("CHALLENGE_008","CHALLENGE_009")
            receipt={"schema":"C11D-V2B-SAFE-PROJECTION-RUNTIME-RECEIPT-V1","schema_version":"1.0","status":"SAFE_PROJECTION_RECEIPT",
                "selector":{"challenge_id":cid,"mechanic":mechanic},
                "process":{"run_id":run_id,"process_id":process_id,"variant_role":role,"exit_code":0},
                "runtime":{},
                "lineage":{"runtime_contract_sha256":audit.RUNTIME_CONTRACT_SHA,"design_contract_sha256":audit.DESIGN_SHA,
                    "frozen_manifest_sha256":audit.FROZEN_SHA,"challenge_source_sha256":selector["challenge_source_sha256"],
                    "mechanic_source_sha256":selector["mechanic_source_sha256"],"runtime_bridge_sha256":h("bridge"),
                    "frame_snapshot_sha256":h("framesnapshot"),"verified_source_pin_count":81,"verified_authority_input_pin_count":9},
                "identity":identity,"seeds":{"requested_gameplay_seed":gameplay_seed,"music_seed_request_domain":music_seed,"music_seed_copied_into_simulation":False},
                "simulation_input_sha256":h(cid+"sim"),
                "source_frames":{"count":12,"expected_game_frames":12,"coordinate_transform":"NONE","resampling":"PROHIBITED","projection_sha256":state},
                "source_timebase":{"known_conflict":conflict,"phase_timeline_acceptance":"BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY" if conflict else "NOT_EVALUATED_SOURCE_FRAME_ONLY"},
                "source_asset_pins":[],"candidate_field_observations":observations,
                "authority":{"approved_bindings":0,"approved_custom_data_bindings":0,"renderer":"OFF","payload_materialized":False,"media_created":False,"release_authority":"NONE"}}
            runs.append({"role":role,"run_id":run_id,"process_id":process_id,"exit_code":0,
                "stdout_sha256":h(run_id+"out"),"stderr_sha256":h(run_id+"err"),"receipt_sha256":h(run_id+"receipt"),"receipt":receipt})
        relations={}
        if candidate is not None:
            field,typ=candidate
            hashes={role:audit.candidate_hash_map(next(r["receipt"] for r in runs if r["role"]==role))[field] for role in ROLES}
            gp_pass=hashes[ROLES[2]]==hashes[ROLES[0]] if field=="target_x" else hashes[ROLES[2]]!=hashes[ROLES[0]]
            relations[field]={"baseline_sha256":hashes[ROLES[0]],"gameplay_variant_sha256":hashes[ROLES[2]],"music_variant_sha256":hashes[ROLES[3]],
                "editorial_variant_sha256":hashes[ROLES[4]],"gameplay_relation_pass":gp_pass,"music_invariant_pass":True,"editorial_invariant_pass":True}
        rows.append({"selector":{"challenge_id":cid,"mechanic":mechanic},"status":"ACCEPTED_SAFE_PROJECTION_RUNTIME","block_reasons":[],
            "planner_variants":planner,"runtime_runs":runs,"comparison":{"baseline_repeat_agreement":True,"gameplay_seed_safe_state_changed":True,
                "music_seed_safe_state_and_candidates_invariant":True,"editorial_safe_state_and_candidates_invariant":True,
                "candidate_probe_relations":relations,"status":"PASS"}})
    report={"schema":audit.REPORT_ID,"schema_version":"1.0","status":"PASS_SAFE_PROJECTION_SEED_SENSITIVITY",
        "runtime_contract_sha256":audit.RUNTIME_CONTRACT_SHA,"design_contract_sha256":audit.DESIGN_SHA,"frozen_manifest_sha256":audit.FROZEN_SHA,
        "selector_count_expected":9,"selectors":rows,"planner_invocations":45,"planner_invocations_expected":45,
        "godot_version_probe_invocations":1,"godot_runtime_process_invocations":45,"godot_runtime_processes_expected":45,
        "payload_materialized":False,"media_created":False,"approved_bindings":0,"approved_custom_data_bindings":0,
        "visual_seed_sensitivity":"ACCEPTED_BY_SAFE_PROJECTION_HASH",
        "governance_locks":{"renderer":"OFF","media_created":False,"payload_materialized":False,"candidate_input_admissible":False,
            "seed_domains_complete_for_candidate_input":False,"automatic_seed_generation":False,"master_seed":"NOT_ADOPTED",
            "D4.8":"BLOCKED","D9.10":"PREPARE_ONLY","D9.14":"BLOCKED","D9.16":"BLOCKED",
            "D9.17":"BLOCKED_NO_GO","D10":"BLOCKED_FOR_PROMOTION","baseline_approval":"MISSING","freeze_eligible":False,"release_authority":"NONE",
            "visual_seed_sensitivity":"NOT_TESTED_UNTIL_V2B_RUNTIME_ACCEPTED",
            "challenge_004_v1_fixture":"IMMUTABLE","challenge_008_009_phase_timeline_acceptance":"BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY"},
        "evidence":{"godot_version_probe_exit_code":0,"godot_version":"4.7.1.stable.mono.official.a13da4feb","failure":None,
            "implementation_test_receipt_sha256":h("static receipt"),"source_pin_errors_before_runtime":[],"source_pin_errors_after_runtime":[],"directory":"C:\\runtime",
            "evidence_file_sha256":{}}}
    receipt={"schema":audit.RECEIPT_ID,"status":"PASS_IMPLEMENTATION_STATIC_TESTS","test_count":198,"source_pin_count":81,"authority_input_pin_count":9,
        "runtime_contract_sha256":audit.RUNTIME_CONTRACT_SHA,"design_contract_sha256":audit.DESIGN_SHA,"frozen_manifest_sha256":audit.FROZEN_SHA}
    return report,design,receipt

class CandidateEvidenceAuditTests(unittest.TestCase):
    def test_accepts_complete_fixture(self):
        r,d,receipt=fixture(); s=audit.validate_report(r,d,receipt,h("static receipt")); self.assertEqual(len(s["selectors"]),9)
    def test_root_schema_rejected(self):
        r,d,rec=fixture(); r["schema"]="wrong"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_blocked_report(self):
        r,d,rec=fixture(); r["status"]="BLOCKED"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_incomplete_planner_denominator(self):
        r,d,rec=fixture(); r["planner_invocations"]=44
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_incomplete_godot_denominator(self):
        r,d,rec=fixture(); r["godot_runtime_process_invocations"]=44
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_duplicate_selector_row(self):
        r,d,rec=fixture(); r["selectors"][1]["selector"]["challenge_id"]="CHALLENGE_001"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_nonaccepted_selector(self):
        r,d,rec=fixture(); r["selectors"][2]["status"]="BLOCKED"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_incomplete_variant_row(self):
        r,d,rec=fixture(); r["selectors"][0]["runtime_runs"].pop()
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_duplicate_process_id(self):
        r,d,rec=fixture(); r["selectors"][0]["runtime_runs"][1]["process_id"]=r["selectors"][0]["runtime_runs"][0]["process_id"]
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_duplicate_run_id(self):
        r,d,rec=fixture(); r["selectors"][0]["runtime_runs"][1]["run_id"]=r["selectors"][0]["runtime_runs"][0]["run_id"]
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_changed_frozen_pin(self):
        r,d,rec=fixture(); r["frozen_manifest_sha256"]="0"*64
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_media_creation(self):
        r,d,rec=fixture(); r["media_created"]=True
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_payload_materialization(self):
        r,d,rec=fixture(); r["payload_materialized"]=True
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_binding_approval(self):
        r,d,rec=fixture(); r["approved_bindings"]=1
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_governance_renderer_change(self):
        r,d,rec=fixture(); r["governance_locks"]["renderer"]="ON"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_unexpected_nested_binding_count(self):
        r,d,rec=fixture(); r["governance_locks"]["approved_bindings"]=1
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_bad_godot_version(self):
        r,d,rec=fixture(); r["evidence"]["godot_version"]="4.7.1.stable"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_failed_internal_version_probe(self):
        r,d,rec=fixture(); r["evidence"]["godot_version_probe_exit_code"]=1
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_receipt_hash_mismatch(self):
        r,d,rec=fixture(); r["evidence"]["implementation_test_receipt_sha256"]="0"*64
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_receipt_pin_count(self):
        r,d,rec=fixture(); rec["source_pin_count"]=80
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_candidate_raw_values(self):
        r,d,rec=fixture(); obs=r["selectors"][2]["runtime_runs"][0]["receipt"]["candidate_field_observations"][0]; obs["raw_values_emitted"]=True
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_candidate_binding_flag(self):
        r,d,rec=fixture(); obs=r["selectors"][2]["runtime_runs"][0]["receipt"]["candidate_field_observations"][0]; obs["renderer_binding_approved"]=True
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_candidate_wrong_type(self):
        r,d,rec=fixture(); obs=r["selectors"][2]["runtime_runs"][0]["receipt"]["candidate_field_observations"][0]; obs["semantic_type"]="Vector2"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_candidate_missing_frames(self):
        r,d,rec=fixture(); obs=r["selectors"][2]["runtime_runs"][0]["receipt"]["candidate_field_observations"][0]; obs["present_frames"]=11
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_extra_raw_candidate_key(self):
        r,d,rec=fixture(); obs=r["selectors"][2]["runtime_runs"][0]["receipt"]["candidate_field_observations"][0]; obs["values"]=[1,2]
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_gameplay_state_invariant(self):
        r,d,rec=fixture(); row=r["selectors"][2]; row["runtime_runs"][2]["receipt"]["identity"]["safe_projection_state_sha256"]=row["runtime_runs"][0]["receipt"]["identity"]["safe_projection_state_sha256"]
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_music_seed_leak(self):
        r,d,rec=fixture(); row=r["selectors"][2]; row["runtime_runs"][3]["receipt"]["identity"]["safe_projection_state_sha256"]=h("leak")
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_editorial_seed_leak(self):
        r,d,rec=fixture(); row=r["selectors"][2]; row["runtime_runs"][4]["receipt"]["identity"]["safe_projection_state_sha256"]=h("leak")
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_candidate_mutation_relation_mismatch(self):
        r,d,rec=fixture(); relation=r["selectors"][4]["comparison"]["candidate_probe_relations"]["target_position"]; relation["gameplay_relation_pass"]=False
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_pilot_target_x_changed_by_gameplay_seed(self):
        r,d,rec=fixture(); row=r["selectors"][2]; field="target_x"; row["runtime_runs"][2]["receipt"]["candidate_field_observations"][0]["value_stream_sha256"]=h("changed")
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_v2c_timeline_relaxation_for_008(self):
        r,d,rec=fixture(); r["selectors"][7]["runtime_runs"][0]["receipt"]["source_timebase"]["phase_timeline_acceptance"]="ACCEPTED"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_candidate_on_noncandidate_selector(self):
        r,d,rec=fixture(); r["selectors"][0]["runtime_runs"][0]["receipt"]["candidate_field_observations"]=[{"field":"target_x"}]
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_missing_comparison_relation(self):
        r,d,rec=fixture(); del r["selectors"][2]["comparison"]["candidate_probe_relations"]["target_x"]
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_changed_adapter_boundary(self):
        r,d,rec=fixture(); r["selectors"][0]["planner_variants"][0]["adapter_status"]="DISPATCHED"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_payload_identity_creation(self):
        r,d,rec=fixture(); r["selectors"][0]["runtime_runs"][0]["receipt"]["identity"]["payload_identity"]="sha256:abc"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_bad_source_pin_errors(self):
        r,d,rec=fixture(); r["evidence"]["source_pin_errors_after_runtime"]=["drift"]
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_incomplete_report_roles(self):
        r,d,rec=fixture(); r["selectors"][0]["planner_variants"][2]["role"]="UNKNOWN"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_request_identity_not_changed(self):
        r,d,rec=fixture(); r["selectors"][2]["planner_variants"][2]["request_hash"]=r["selectors"][2]["planner_variants"][0]["request_hash"]
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))
    def test_rejects_static_receipt_status(self):
        r,d,rec=fixture(); rec["status"]="BLOCKED"
        with self.assertRaises(audit.AuditError): audit.validate_report(r,d,rec,h("static receipt"))

if __name__ == "__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(CandidateEvidenceAuditTests)
    count=suite.countTestCases()
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful(): print(f"C11D_V2B_CANDIDATE_EVIDENCE_AUDIT_TESTS_PASS={result.testsRun}/{count}")
    else: print("C11D_V2B_CANDIDATE_EVIDENCE_AUDIT_TESTS_FAIL")
    raise SystemExit(0 if result.wasSuccessful() else 1)
