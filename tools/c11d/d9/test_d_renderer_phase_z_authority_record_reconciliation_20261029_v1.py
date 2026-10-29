#!/usr/bin/env python3
"""Regression tests for Phase Z reconciliation and conservative governance locks."""
from __future__ import annotations
import argparse, json, unittest
from pathlib import Path
from verify_d_renderer_phase_z_authority_record_reconciliation_20261029_v1 import verify

EXPECTED_IDS = [
    "R-01-TIMEBASE-SAMPLING", "R-02-SPATIAL-MAPPING",
    "R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y", "R-04-VISIBILITY-AND-REGION-OWNERSHIP",
    "R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING", "R-06-INVALID-DATA-AND-TRACK-INTEGRITY",
    "R-07-SEMANTIC-VISUAL-OWNERSHIP", "R-08-CHALLENGE-008", "R-09-CHALLENGE-009"
]
def read_json(p):
    with Path(p).open("r", encoding="utf-8") as f: return json.load(f)
class PhaseZTests(unittest.TestCase):
    phase_y = None; phase_z = None; packet = None
    @classmethod
    def setUpClass(cls):
        if not cls.phase_y or not cls.phase_z or not cls.packet:
            raise RuntimeError("test fixture paths not provided")
    def test_01_phase_y_source_status(self): self.assertEqual(self.phase_y["status"], "PASS_CONTENT_REVIEW_COMPLETE_AUTHORITY_ADJUDICATION_PENDING")
    def test_02_phase_x_bundle_pin(self): self.assertEqual(self.phase_y["input_bundle"]["sha256"], "5a481bded8dc9634741f0e164696ee123e02e9f029bcf689c39cad6a6460811e")
    def test_03_source_hash_matches(self): self.assertEqual(self.phase_y["input_bundle"]["source_hash_matches"], 57)
    def test_04_no_source_hash_mismatches(self): self.assertEqual(self.phase_y["input_bundle"]["source_hash_mismatches"], 0)
    def test_05_no_source_files_missing(self): self.assertEqual(self.phase_y["input_bundle"]["source_files_missing"], 0)
    def test_06_nested_archives_crc_pass(self): self.assertEqual(self.phase_y["counts"]["nested_archive_crc_pass"], 7)
    def test_07_phase_z_status_pending(self): self.assertEqual(self.phase_z["status"], "PASS_RECONCILIATION_MATRIX_AND_DECISION_PACKET_PREPARED_AUTHORITY_ADJUDICATION_PENDING")
    def test_08_nine_decisions(self): self.assertEqual(self.phase_z["decision_count"], 9)
    def test_09_exact_r_ids_and_order(self): self.assertEqual([r["decision_id"] for r in self.phase_z["decisions"]], EXPECTED_IDS)
    def test_10_r01_to_r07_unadopted(self): self.assertTrue(all(r["status"] == "NOT_ADOPTED_KEEP_BLOCKED" for r in self.phase_z["decisions"][:7]))
    def test_11_r08_blocked(self): self.assertEqual(self.phase_z["decisions"][7]["status"], "BLOCKED_EXPLICIT_AUTHORITY_REQUIRED")
    def test_12_r09_blocked(self): self.assertEqual(self.phase_z["decisions"][8]["status"], "BLOCKED_EXPLICIT_AUTHORITY_REQUIRED")
    def test_13_r08_timing_conflict_retained(self):
        s=self.phase_z["decisions"][7]["evidence_assessment"]; self.assertIn("11 seconds",s); self.assertIn("12 seconds",s)
    def test_14_r09_timing_conflict_retained(self):
        s=self.phase_z["decisions"][8]["evidence_assessment"]; self.assertIn("11 seconds",s); self.assertIn("12 seconds",s)
    def test_15_renderer_stays_off(self): self.assertEqual(self.phase_z["governance_locks"]["renderer"], "OFF")
    def test_16_binding_counts_zero(self):
        g=self.phase_z["governance_locks"]; self.assertEqual(g["approved_bindings"],0); self.assertEqual(g["approved_custom_data_bindings"],0); self.assertEqual(g["approved_renderer_projection_bindings"],0)
    def test_17_d917_and_d10_blocked(self):
        g=self.phase_z["governance_locks"]; self.assertEqual(g["D9.17"],"BLOCKED_NO_GO"); self.assertEqual(g["D10"],"BLOCKED_FOR_PROMOTION")
    def test_18_release_authority_none(self): self.assertEqual(self.phase_z["governance_locks"]["release_authority"], "NONE")
    def test_19_no_broad_policy_adoption(self): self.assertEqual(self.phase_z["authority_assessment"]["broad_phase_r_policy_adoption"], "NONE")
    def test_20_narrow_records_do_not_expand(self): self.assertFalse(self.phase_z["authority_assessment"]["narrow_decisions_expand_to_broad_policy"])
    def test_21_test_pass_not_renderer_authority(self): self.assertFalse(self.phase_z["authority_assessment"]["historical_test_pass_grants_renderer_authority"])
    def test_22_packet_is_preparation_only(self): self.assertTrue(self.packet["preparation_only"])
    def test_23_packet_status_pending(self): self.assertEqual(self.packet["status"], "PREPARED_AWAITING_EXPLICIT_AUTHORITY_DECISIONS")
    def test_24_packet_rows_match(self): self.assertEqual([r["decision_id"] for r in self.packet["decisions"]], EXPECTED_IDS)
    def test_25_operator_choices_not_invented(self): self.assertTrue(all(r["selected_option"] is None and r["requested_operator_disposition"] == "PENDING" for r in self.packet["decisions"]))
    def test_26_authority_provenance_not_fabricated(self): self.assertTrue(all(r["approval_provenance_or_signature_ref"] is None for r in self.packet["decisions"]))
    def test_27_incomplete_defaults_blocked(self): self.assertEqual(self.packet["default_if_incomplete"], "KEEP_BLOCKED_NO_POLICY_ADOPTION")
    def test_28_next_gate(self): self.assertEqual(self.phase_z["next_gate"], "PHASE_AA_OPERATOR_DECISION_EVIDENCE_COMPLETION_AND_PRE_RENDER_READINESS")
    def test_29_required_fields_comprehensive(self):
        fields=set(self.phase_z["required_authority_fields"]); self.assertTrue({"decision_id","exact_policy_text_and_selected_option","named_approving_authority_and_role","authority_scope_and_delegation_basis","decision_date_and_effective_date","rationale","source_paths_and_sha256_pins","acceptance_test_obligations","verifiable_approval_provenance_or_signature","immutable_record_location"}.issubset(fields))
    def test_30_verifier_accepts_complete_structural_contract(self): self.assertTrue(verify(self.phase_y,self.phase_z,self.packet))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--phase-y-json",required=True); ap.add_argument("--phase-z-json",required=True); ap.add_argument("--decision-packet-json",required=True)
    a=ap.parse_args()
    PhaseZTests.phase_y=read_json(a.phase_y_json); PhaseZTests.phase_z=read_json(a.phase_z_json); PhaseZTests.packet=read_json(a.decision_packet_json)
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(PhaseZTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful(): return 1
    print("PHASE_Z_AUTHORITY_RECONCILIATION_TESTS=30/30")
    return 0
if __name__ == "__main__": raise SystemExit(main())
