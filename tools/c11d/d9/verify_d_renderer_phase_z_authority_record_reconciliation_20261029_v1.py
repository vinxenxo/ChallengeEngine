#!/usr/bin/env python3
"""Read-only verifier for the C11-D Phase Z authority reconciliation package."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
EXPECTED_IDS = [
    "R-01-TIMEBASE-SAMPLING", "R-02-SPATIAL-MAPPING",
    "R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y", "R-04-VISIBILITY-AND-REGION-OWNERSHIP",
    "R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING", "R-06-INVALID-DATA-AND-TRACK-INTEGRITY",
    "R-07-SEMANTIC-VISUAL-OWNERSHIP", "R-08-CHALLENGE-008", "R-09-CHALLENGE-009"
]
EXPECTED_LOCKS = {
    "renderer": "OFF", "media_created": False, "payload_materialized": False,
    "candidate_input_admissible": False, "seed_domains_complete_for_candidate_input": False,
    "automatic_seed_generation": False, "master_seed": "NOT_ADOPTED",
    "approved_bindings": 0, "approved_custom_data_bindings": 0,
    "approved_renderer_projection_bindings": 0, "D4.8": "BLOCKED",
    "D9.10": "PREPARE_ONLY", "D9.14": "BLOCKED", "D9.16": "BLOCKED",
    "D9.17": "BLOCKED_NO_GO", "D10": "BLOCKED_FOR_PROMOTION",
    "baseline_approval": "MISSING", "freeze_eligible": False, "release_authority": "NONE"
}
def load(p):
    with Path(p).open("r", encoding="utf-8") as f: return json.load(f)
def verify(phase_y, phase_z, packet):
    assert phase_y["status"] == "PASS_CONTENT_REVIEW_COMPLETE_AUTHORITY_ADJUDICATION_PENDING"
    assert phase_y["input_bundle"]["sha256"] == "5a481bded8dc9634741f0e164696ee123e02e9f029bcf689c39cad6a6460811e"
    assert phase_y["input_bundle"]["source_hash_matches"] == 57
    assert phase_y["input_bundle"]["source_hash_mismatches"] == 0
    assert phase_y["input_bundle"]["source_files_missing"] == 0
    assert phase_z["status"] == "PASS_RECONCILIATION_MATRIX_AND_DECISION_PACKET_PREPARED_AUTHORITY_ADJUDICATION_PENDING"
    assert phase_z["decision_count"] == 9
    rows = phase_z["decisions"]
    assert [r["decision_id"] for r in rows] == EXPECTED_IDS
    assert len({r["decision_id"] for r in rows}) == 9
    assert phase_z["governance_locks"] == EXPECTED_LOCKS
    assert phase_z["authority_assessment"]["broad_phase_r_policy_adoption"] == "NONE"
    assert phase_z["authority_assessment"]["narrow_decisions_expand_to_broad_policy"] is False
    assert phase_z["authority_assessment"]["historical_test_pass_grants_renderer_authority"] is False
    assert phase_z["authority_assessment"]["generic_standing_approval_to_continue_engineering_grants_product_policy_authority"] is False
    assert all(r["default_disposition"] == "KEEP_BLOCKED_NO_POLICY_ADOPTION" for r in rows)
    assert all(len(r["unresolved_requirements"]) >= 3 for r in rows)
    assert rows[7]["status"] == "BLOCKED_EXPLICIT_AUTHORITY_REQUIRED"
    assert rows[8]["status"] == "BLOCKED_EXPLICIT_AUTHORITY_REQUIRED"
    assert "11 seconds" in rows[7]["evidence_assessment"] and "12 seconds" in rows[7]["evidence_assessment"]
    assert "11 seconds" in rows[8]["evidence_assessment"] and "12 seconds" in rows[8]["evidence_assessment"]
    assert packet["preparation_only"] is True and packet["status"] == "PREPARED_AWAITING_EXPLICIT_AUTHORITY_DECISIONS"
    assert [r["decision_id"] for r in packet["decisions"]] == EXPECTED_IDS
    assert all(r["requested_operator_disposition"] == "PENDING" for r in packet["decisions"])
    assert all(r["selected_option"] is None and r["approval_provenance_or_signature_ref"] is None for r in packet["decisions"])
    assert packet["default_if_incomplete"] == "KEEP_BLOCKED_NO_POLICY_ADOPTION"
    assert phase_z["next_gate"] == "PHASE_AA_OPERATOR_DECISION_EVIDENCE_COMPLETION_AND_PRE_RENDER_READINESS"
    return True
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--phase-y-json", required=True)
    ap.add_argument("--phase-z-json", required=True)
    ap.add_argument("--decision-packet-json", required=True)
    args=ap.parse_args()
    try:
        verify(load(args.phase_y_json), load(args.phase_z_json), load(args.decision_packet_json))
    except Exception as e:
        print(f"PHASE_Z_VERIFY_ERROR={type(e).__name__}:{e}")
        return 2
    print("PHASE_Z_AUTHORITY_RECONCILIATION_VERIFICATION=PASS_MATRIX_AND_LOCKS")
    print("PHASE_Z_VERIFIED_DECISIONS=9")
    print("PHASE_Z_OPERATOR_PACKET=PASS_UNSIGNED_PENDING_FIELDS")
    print("AUTHORITY_ADJUDICATION=PENDING; POLICY_ADOPTION=NONE; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE")
    print("NEXT_GATE=PHASE_AA_OPERATOR_DECISION_EVIDENCE_COMPLETION_AND_PRE_RENDER_READINESS")
    return 0
if __name__ == "__main__": sys.exit(main())
