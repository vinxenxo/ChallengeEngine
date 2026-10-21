#!/usr/bin/env python3
"""Read-only C11-D V2-B field-region visibility decision-record regression gate.
Uses Python standard library only; no Godot, rendering, media, or payload consumer.
"""
from __future__ import annotations
import hashlib, json, math, os, sys
from pathlib import Path

EXPECTED = {
    "c11c": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
    "old_record": "cc3550cd4d13f228ec9b3d51eeaa199505c5975b42882fb06ba3e83c4a000e90",
    "old_receipt": "3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9",
    "proposal": "f3afe4d7d08791c7634c9851500ca551438870babc195db1908440b93e740692",
    "proposal_schema": "503d0cbe4af4c5db04161d8a54e96f41b2dd8b503d5190169d5f208f8a44937a",
    "proposal_test": "e3c9b47e075d14145117b3c5f325681e37c01e3504a2fabc0f7e5133c13458de",
    "proposal_test_receipt": "87c8ab97db18a7531dc2df610b51fe819c8bf746b2b66475b544220c37c95cbb",
    "proposal_stdout": "dc6ecb960fc59852c4b3251a1146ef6425675c44be4cf03304d3fc0026942d27",
    "empty_sha": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
}
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4]
RECEIPT = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
RECORD_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_SCHEMA_V1.json")
PROPOSAL_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_V1.json")
PROPOSAL_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_SCHEMA_V1.json")
PROPOSAL_TEST_REL = Path("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_field_region_visibility_proposal_v1.py")
OLD_RECORD_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json")
FROZEN_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")

class Gate:
    def __init__(self): self.count = 0; self.failures = []
    def check(self, cond, label):
        self.count += 1
        if not cond: self.failures.append(f"CHECK_{self.count:03d}: {label}")
    def same(self, a, b, label): self.check(a == b, label)
    def true(self, v, label): self.check(v is True, label)
    def false(self, v, label): self.check(v is False, label)
    def sha_file(self, path, expected, label):
        self.check(path.is_file(), label + " exists")
        if path.is_file(): self.same(hashlib.sha256(path.read_bytes()).hexdigest(), expected, label + " sha256")
    def finish(self):
        if self.failures:
            print("C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_STATUS=FAIL")
            for line in self.failures[:80]: print(line)
            print(f"C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_TESTS={self.count-len(self.failures)}/{self.count}")
            return 1
        print(f"C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_TESTS={self.count}/{self.count}")
        print("C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISIONS=4_ACCEPTED_FOR_COORDINATE_POLICY_SPECIFICATION_ONLY")
        print("C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_BLOCKED_CANDIDATES=2/2_RETAINED")
        print("C11D_V2B_COORDINATE_POLICY_AUTHORIZATION=NOT_GRANTED")
        print("C11D_V2B_BINDING_AUTHORIZATION=NOT_GRANTED")
        print("C11D_V2B_RENDERER_PROJECTION_AUTHORIZATION=NOT_GRANTED")
        print("C11D_V2B_RENDER_TEST_AUTHORIZATION=NOT_GRANTED")
        print("C11D_V2B_CANDIDATE_INPUT_ADMISSIBLE=false")
        print("C11D_V2B_RENDERER=OFF")
        print("C11D_V2B_MEDIA_CREATED=false")
        print("C11D_V2B_C11C_IMMUTABLE=true")
        return 0

def load(path): return json.loads(path.read_text(encoding="utf-8"))
def file_sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    g = Gate()
    record_path = ROOT / RECORD_REL
    schema_path = ROOT / SCHEMA_REL
    proposal_path = ROOT / PROPOSAL_REL
    proposal_schema_path = ROOT / PROPOSAL_SCHEMA_REL
    proposal_test_path = ROOT / PROPOSAL_TEST_REL
    old_record_path = ROOT / OLD_RECORD_REL
    frozen_path = ROOT / FROZEN_REL
    for rel, expected, name in [
        (FROZEN_REL, EXPECTED["c11c"], "frozen C11-C manifest"),
        (OLD_RECORD_REL, EXPECTED["old_record"], "prior semantic decision record"),
        (PROPOSAL_REL, EXPECTED["proposal"], "field-region proposal"),
        (PROPOSAL_SCHEMA_REL, EXPECTED["proposal_schema"], "field-region proposal schema"),
        (PROPOSAL_TEST_REL, EXPECTED["proposal_test"], "field-region proposal regression suite"),
        (RECORD_REL, "1ec59d7a9257cfc2477fc37efe8cb2f04d9807a7f9986d96afc2f2ddd9b4f7af", "new field-region decision record"),
        (SCHEMA_REL, "bb32a0631216c8b557ee48f85ff06dbf1588c125606b917acff22930aa6ce50e", "new field-region decision schema"),
    ]:
        g.sha_file(ROOT / rel, expected, name)

    rec = load(record_path); sch = load(schema_path); prop = load(proposal_path); pschema = load(proposal_schema_path); old = load(old_record_path)
    g.same(rec.get("schema"), "C11D-V2B-CANDIDATE-FIELD-REGION-VISIBILITY-DECISION-RECORD-V1", "record schema id")
    g.same(rec.get("schema_version"), "1.0", "record schema version")
    g.same(rec.get("status"), "FIELD_REGION_VISIBILITY_ACCEPTED_FOR_COORDINATE_POLICY_SPECIFICATION_ONLY", "record status")
    g.same(rec.get("decision_scope"), "FUTURE_COORDINATE_POLICY_SPECIFICATION_ONLY", "decision scope")
    g.same(rec.get("reviewer_role"), "operator", "reviewer role")
    g.check(isinstance(rec.get("reviewed_at"), str) and "+02:00" in rec.get("reviewed_at", ""), "RFC3339 timestamp retains Europe/Madrid offset")
    g.same(rec.get("previous_semantic_decision_record_sha256"), EXPECTED["old_record"], "prior semantic decision pin")
    g.same(rec.get("previous_semantic_decision_test_receipt_sha256"), EXPECTED["old_receipt"], "prior semantic decision test receipt pin")
    g.same(rec.get("field_region_visibility_proposal_sha256"), EXPECTED["proposal"], "proposal pin")
    g.same(rec.get("field_region_visibility_proposal_schema_sha256"), EXPECTED["proposal_schema"], "proposal schema pin")
    g.same(rec.get("field_region_visibility_test_script_sha256"), EXPECTED["proposal_test"], "proposal test script pin")
    g.same(rec.get("field_region_visibility_test_count"), 551, "prior proposal test denominator")
    g.same(rec.get("field_region_visibility_test_stdout_sha256"), EXPECTED["proposal_stdout"], "prior proposal stdout pin")
    g.same(rec.get("field_region_visibility_test_stderr_sha256"), EXPECTED["empty_sha"], "prior proposal stderr empty pin")
    g.same(rec.get("field_region_visibility_test_receipt_sha256"), EXPECTED["proposal_test_receipt"], "prior proposal receipt pin")
    g.same(rec.get("frozen_c11c_manifest_sha256"), EXPECTED["c11c"], "frozen manifest pin")
    g.same(len(rec.get("decisions", [])), 4, "four decisions")
    g.same(rec.get("accepted_candidate_count"), 4, "accepted count")
    g.same(rec.get("blocked_candidate_count"), 2, "blocked count")

    # Strict schema structure and closed object boundaries.
    g.same(sch.get("$schema"), "https://json-schema.org/draft/2020-12/schema", "JSON Schema dialect")
    g.same(sch.get("type"), "object", "schema root object")
    g.false(sch.get("additionalProperties", True), "schema rejects additional root properties")
    for required in ["schema","schema_version","status","decision_scope","reviewer_role","reviewed_at","decisions","blocked_candidates_retained","source_pins","authority_input_pins","semantic_decision_input_pins","authorization","governance_locks","next_gate","notes"]:
        g.check(required in sch.get("required", []), "schema requires " + required)
    g.same(sch.get("properties", {}).get("schema", {}).get("const"), rec["schema"], "schema record id const")
    g.same(sch.get("properties", {}).get("status", {}).get("const"), rec["status"], "schema status const")
    g.same(sch.get("properties", {}).get("decisions", {}).get("minItems"), 4, "schema four decisions minimum")
    g.same(sch.get("properties", {}).get("decisions", {}).get("maxItems"), 4, "schema four decisions maximum")
    g.same(sch.get("properties", {}).get("source_pins", {}).get("minItems"), 81, "schema source pins minimum")
    g.same(sch.get("properties", {}).get("source_pins", {}).get("maxItems"), 81, "schema source pins maximum")
    g.same(sch.get("properties", {}).get("authority_input_pins", {}).get("minItems"), 9, "schema authority pins minimum")
    g.same(sch.get("properties", {}).get("authority_input_pins", {}).get("maxItems"), 9, "schema authority pins maximum")
    g.same(sch.get("properties", {}).get("semantic_decision_input_pins", {}).get("minItems"), 6, "schema semantic pins minimum")
    g.same(sch.get("properties", {}).get("semantic_decision_input_pins", {}).get("maxItems"), 6, "schema semantic pins maximum")

    expected_candidates = [("CHALLENGE_003","target_x"),("CHALLENGE_005","target_position"),("CHALLENGE_006","target_position"),("CHALLENGE_007","target_position")]
    g.same([(d.get("challenge_id"), d.get("field")) for d in rec["decisions"]], expected_candidates, "exact candidate decision order")
    prop_by_key = {(x.get("challenge_id"),x.get("field")):x for x in prop.get("candidates", [])}
    old_by_key = {(x.get("challenge_id"),x.get("field")):x for x in old.get("decisions", [])}
    for idx, decision in enumerate(rec["decisions"]):
        key=(decision.get("challenge_id"),decision.get("field")); prefix=f"decision {idx+1} {key[0]}.{key[1]}"
        g.check(key in prop_by_key, prefix + " exists in proposal")
        g.check(key in old_by_key, prefix + " exists in prior semantic decision")
        g.same(decision.get("decision"), "ACCEPT_FOR_FUTURE_COORDINATE_POLICY_SPECIFICATION_ONLY", prefix + " decision scope")
        g.check(isinstance(decision.get("rationale"), str) and len(decision.get("rationale", "")) >= 80, prefix + " substantive rationale")
        g.true(decision.get("source_semantics_acknowledged"), prefix + " source semantics acknowledged")
        g.true(decision.get("field_region_proposal_reviewed"), prefix + " proposal reviewed")
        g.true(decision.get("visibility_window_accepted_for_specification_only"), prefix + " visibility only accepted for specification")
        g.false(decision.get("coordinate_transform_approved"), prefix + " no transform approval")
        g.false(decision.get("binding_approved"), prefix + " no binding approval")
        g.false(decision.get("renderer_projection_approved"), prefix + " no projection approval")
        g.false(decision.get("pixel_placement_approved"), prefix + " no pixel placement approval")
        if key in prop_by_key:
            pc = prop_by_key[key]
            g.same(pc.get("proposal_status"), "PROPOSED_NOT_APPROVED", prefix + " source proposal still unapproved")
            g.false(pc.get("binding_authorized"), prefix + " proposal does not authorize binding")
            g.false(pc.get("renderer_projection_approved"), prefix + " proposal does not approve projection")
            g.false(pc.get("candidate_renderable"), prefix + " proposal candidate remains non-renderable")
            g.same(pc.get("region_mapping", {}).get("renderer_destination_space"), "UNRESOLVED_NOT_APPROVED", prefix + " destination remains unresolved")
            g.false(pc.get("region_mapping", {}).get("coordinate_transform_authorized"), prefix + " transform remains unauthorized")
            g.false(pc.get("region_mapping", {}).get("actual_pixel_placement_authorized"), prefix + " pixel placement remains unauthorized")
            g.same(pc.get("visibility_policy", {}).get("status"), "PROPOSED_NOT_APPROVED", prefix + " visibility status remains proposal")
            g.same(pc.get("visibility_policy", {}).get("visibility_window_approval"), "PENDING_OPERATOR_REVIEW", prefix + " proposal's original status immutable")
            g.same(pc.get("sample_contract", {}).get("expected_sample_count"), "EXACT_SOURCE_FRAME_COUNT", prefix + " exact source-frame cardinality")
            g.same(pc.get("sample_contract", {}).get("missing_sample_behavior"), "FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK", prefix + " fail closed on missing samples")
            g.same(pc.get("sample_contract", {}).get("nonfinite_sample_behavior"), "FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK", prefix + " fail closed on non-finite samples")
            g.same(pc.get("sample_contract", {}).get("cardinality_mismatch_behavior"), "FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK", prefix + " fail closed on cardinality mismatch")
            g.false(pc.get("sample_contract", {}).get("serialize_whole_custom_data_map", True), prefix + " no custom_data map serialization")
        if key in old_by_key:
            g.same(old_by_key[key].get("semantic_decision"), "ACCEPT_SEMANTIC_DEFINITION_FOR_FUTURE_BINDING_SPECIFICATION", prefix + " prior semantic acceptance alignment")

    g.same(len(rec.get("blocked_candidates_retained", [])), 2, "two blocked candidates retained")
    expected_blocked = [("CHALLENGE_008","active_selection"),("CHALLENGE_009","displayed_count")]
    g.same([(d.get("challenge_id"),d.get("field")) for d in rec["blocked_candidates_retained"]], expected_blocked, "exact blocked candidate matrix")
    for b in rec["blocked_candidates_retained"]:
        g.same(b.get("status"), "REMAINS_BLOCKED", "blocked status " + b.get("challenge_id", "unknown"))
        g.check(len(b.get("reason", "")) >= 60, "blocked rationale adequate " + b.get("challenge_id", "unknown"))

    # Exact input pins, byte-level verification from the active D checkout.
    for pin_type, expected_n in [("source_pins",81),("authority_input_pins",9),("semantic_decision_input_pins",6)]:
        pins=rec.get(pin_type, [])
        g.same(len(pins), expected_n, pin_type + " denominator")
        seen=set()
        for idx,pin in enumerate(pins):
            p=ROOT / Path(pin["path"])
            key=pin["path"]
            g.check(key not in seen, pin_type + " unique path " + key)
            seen.add(key)
            g.check(p.is_file(), pin_type + " exists " + key)
            if p.is_file(): g.same(file_sha(p), pin["sha256"], pin_type + " sha " + key)
            g.check(bool(__import__("re").fullmatch(r"[0-9a-f]{64}", pin["sha256"])), pin_type + " sha format " + key)

    # Cross-check the actual input lists and their identities against the accepted proposal package.
    g.same(rec["source_pins"], prop["source_pins"], "source pin list unchanged from proposal")
    g.same(rec["authority_input_pins"], prop["authority_input_pins"], "authority input pin list unchanged from proposal")
    g.same(rec["semantic_decision_input_pins"], prop["semantic_decision_input_pins"], "semantic input pin list unchanged from proposal")
    g.same(prop.get("status"), "PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED", "immutable field-region proposal stays proposed")
    g.same(prop.get("candidate_count"), 4, "proposal contains four candidates only")
    g.same(prop.get("decision_gate", {}).get("status"), "PENDING_EXPLICIT_OPERATOR_REVIEW", "proposal's recorded gate remains proposal state")
    g.same(prop.get("candidates", [{}])[0].get("visibility_policy", {}).get("actual_render_enablement"), "BLOCKED_UNTIL_COORDINATE_POLICY_AND_SEPARATE_BINDING_AND_PROJECTION_AUTHORIZATIONS", "source proposal does not authorize render test")

    # Invariants for CHALLENGE_003 scalar-only and three vector fields.
    c003=prop_by_key[("CHALLENGE_003","target_x")]
    g.same(c003.get("semantic_type"), "float", "003 scalar type")
    g.same(c003.get("coordinate_space"), "PILOT_0X100", "003 source coordinate space")
    g.same(c003.get("coordinate_policy"), "X_AXIS_ONLY_NO_2D_POSITION_CONVERSION", "003 scalar only")
    g.same(c003.get("mapping_blocker"), "Y_COORDINATE_ABSENT_AND_PILOT_TO_CANVAS_MAPPING_UNRESOLVED", "003 missing Y remains blocker")
    g.same(c003.get("asset_path"), "assets/c6/waypoint.svg", "003 proposed asset")
    g.same(c003.get("track_specific_policy", {}).get("primary_snapshot_position_role"), "PILOT_PRIMARY_POSITION_REMAINS_SEPARATE_FROM_TARGET_X", "003 primary pilot position stays separate")
    for challenge in ("CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"):
        c=prop_by_key[(challenge,"target_position")]
        g.same(c.get("semantic_type"), "Vector2", challenge + " Vector2")
        g.same(c.get("coordinate_space"), "CANVAS_1080X1920", challenge + " source space remains explicit")
        g.same(c.get("coordinate_policy"), "PRESERVE_RAW_SOURCE_COORDINATES_NO_PROJECTION", challenge + " no projection")
        g.same(c.get("region_mapping", {}).get("renderer_destination_space"), "UNRESOLVED_NOT_APPROVED", challenge + " destination unresolved")
        g.same(c.get("asset_path"), "assets/c6/target.svg", challenge + " target asset")
    g.same(prop_by_key[("CHALLENGE_005","target_position")].get("source_track_kind"), "PER_RUN_CONSTANT_REPEATED_PER_FRAME", "005 constant per-run target")
    g.same(prop_by_key[("CHALLENGE_006","target_position")].get("source_track_kind"), "PER_FRAME_VECTOR", "006 source track")
    g.same(prop_by_key[("CHALLENGE_007","target_position")].get("source_track_kind"), "PER_FRAME_VECTOR", "007 source track")

    auth=rec.get("authorization", {})
    g.same(auth.get("field_region_visibility_decision"), "ACCEPTED_FOR_FUTURE_COORDINATE_POLICY_SPECIFICATION_ONLY", "authorization scope")
    g.same(auth.get("coordinate_policy_approval"), "NOT_GRANTED_BY_THIS_DECISION", "policy not approved")
    g.same(auth.get("coordinate_transform_authorization"), "NOT_GRANTED", "transform not authorized")
    g.same(auth.get("binding_authorization"), "NOT_GRANTED", "binding not authorized")
    g.same(auth.get("renderer_projection_authorization"), "NOT_GRANTED", "projection not authorized")
    g.false(auth.get("payload_consumer_implementation_authorized"), "consumer not authorized")
    g.false(auth.get("renderer_activation_authorized"), "renderer not authorized")
    g.false(auth.get("render_test_authorized"), "render test not authorized")
    g.false(auth.get("payload_materialization_authorized"), "payload not authorized")
    g.false(auth.get("media_creation_authorized"), "media not authorized")
    g.same(auth.get("release_authority"), "NONE", "release authority none")

    locks=rec.get("governance_locks", {})
    lock_expected={"renderer":"OFF","media_created":False,"payload_materialized":False,"candidate_input_admissible":False,
     "seed_domains_complete_for_candidate_input":False,"automatic_seed_generation":False,"master_seed":"NOT_ADOPTED","approved_bindings":0,
     "approved_custom_data_bindings":0,"approved_renderer_projection_bindings":0,"D4.8":"BLOCKED","D9.10":"PREPARE_ONLY","D9.14":"BLOCKED",
     "D9.16":"BLOCKED","D9.17":"BLOCKED_NO_GO","D10":"BLOCKED_FOR_PROMOTION","baseline_approval":"MISSING","freeze_eligible":False,
     "release_authority":"NONE","whole_custom_data_serialization_allowed":False,"challenge_json_modification_allowed":False,"challenge_004_v1_harness_mutation_allowed":False}
    for k,v in lock_expected.items(): g.same(locks.get(k),v,"governance lock " + k)
    for note in rec.get("notes", []): g.check(isinstance(note,str) and len(note)>=40, "note substantive")
    g.check("COORDINATE_POLICY" in rec.get("next_gate", ""), "next gate points to coordinate policy specification")
    g.check(record_path.is_file(), "decision record exists")
    g.check(schema_path.is_file(), "decision schema exists")
    g.same(rec.get("source_pins", [{}])[0].get("path"), "assets/c6/car.svg", "source pin ordering stable")
    g.same(rec.get("authority_input_pins", [{}])[0].get("role"), "capability_contract", "authority pin roles retained")
    g.same(rec.get("semantic_decision_input_pins", [{}])[3].get("role"), "operator_confirmed_semantic_decision_record", "operator decision input retained")

    # Actual Windows run supplies the exact prior test receipt path as argv[2].
    g.check(RECEIPT is not None, "prior proposal test receipt path provided")
    if RECEIPT is not None:
        g.check(RECEIPT.is_file(), "prior proposal test receipt exists")
        if RECEIPT.is_file():
            try:
                rr=load(RECEIPT)
                g.same(rr.get("status"), "PASS_STATIC_TESTS", "prior proposal receipt status")
                g.same(rr.get("test_count"), 551, "prior proposal receipt count")
                g.same(rr.get("proposal_sha256"), EXPECTED["proposal"], "prior proposal receipt proposal pin")
                g.same(rr.get("proposal_schema_sha256"), EXPECTED["proposal_schema"], "prior proposal receipt schema pin")
                g.same(rr.get("test_script_sha256"), EXPECTED["proposal_test"], "prior proposal receipt script pin")
                g.same(rr.get("stdout_sha256"), EXPECTED["proposal_stdout"], "prior proposal receipt stdout pin")
                g.same(rr.get("stderr_sha256"), EXPECTED["empty_sha"], "prior proposal receipt stderr empty")
                g.same(rr.get("frozen_manifest_sha256"), EXPECTED["c11c"], "prior proposal receipt frozen manifest pin")
                g.same(rr.get("accepted_semantic_candidates"), 4, "prior proposal receipt candidate count")
                g.same(rr.get("blocked_candidates"), 2, "prior proposal receipt blocked count")
                g.same(rr.get("approved_bindings"), 0, "prior proposal receipt binding lock")
                g.same(rr.get("approved_renderer_projection_bindings"), 0, "prior proposal receipt projection lock")
                g.false(rr.get("candidate_input_admissible"), "prior proposal receipt input inadmissible")
                g.same(rr.get("renderer"), "OFF", "prior proposal receipt renderer OFF")
                g.false(rr.get("media_created"), "prior proposal receipt no media")
                g.false(rr.get("payload_materialized"), "prior proposal receipt no payload")
            except Exception as exc:
                g.check(False, "prior proposal receipt valid JSON " + str(exc))

    return g.finish()

if __name__ == "__main__":
    raise SystemExit(main())
