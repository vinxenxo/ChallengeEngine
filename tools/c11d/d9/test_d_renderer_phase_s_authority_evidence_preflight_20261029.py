from __future__ import annotations
import hashlib, json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKET_PATH = ROOT / "docs/current/d/C11D_PHASE_S_AUTHORITY_EVIDENCE_PREFLIGHT_20261029_V1.json"
REVIEW_PATH = ROOT / "docs/current/d/C11D_PHASE_S_AUTHORITY_EVIDENCE_PREFLIGHT_20261029_V1.md"
SCHEMA_PATH = ROOT / "definitions/c11d/review/D_RENDERER_PHASE_S_AUTHORITY_EVIDENCE_PREFLIGHT_SCHEMA_V1.json"
R_PACKET_PATH = ROOT / "docs/current/d/C11D_PHASE_R_OPERATOR_POLICY_DECISION_PACKET_20261029_V1.json"
Q_MATRIX_PATH = ROOT / "docs/current/d/C11D_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_MATRIX_20261029_V1.json"
EXPECTED_PINS = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
    "AGENTS.md": "710b3e112e0400e4daac3b8828c89573549f6f59393f6ae5e081e3d482b5ffea",
    ".continue/rules/CONTINUE.md": "a5f2dcd3261b64933d85bda79c027d0bb840afda9444e4af6a6f431f01c1d7b4",
    "docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261029_V4.md": "315c526043f2dd8a24c7552a7f07472e49af7685f106210123b5625714c11245",
    "docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V27.md": "c6186f5adca109b53d2976e6c38d29d8c2b04de2ef7930c5adb8f7baf59dff1a",
    "prompts/C11D_D_FINAL_CLOSEOUT_HANDOVER_MASTER_PROMPT_20261029_V27.md": "f5c5f2efff1f8f7a55f7a83eaead8d14495c78130baf1f4ffa72873798c094b3",
    "prompts/C11D_D_FINAL_CLOSEOUT_START_PROMPT_20261029_V27.md": "5d2e785f480b2f8abcab3015392f4461ef39c4aa4527e56b970ba683a29f401c",
    "docs/current/d/C11D_PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTANCE_REVIEW_20261029_V1.md": "d75b13453fac89b01eb806aaff162771d33d7ff15d88d6f81c2825cf8bcc9132",
    "docs/current/d/C11D_PHASE_P_RUNTIME_EVIDENCE_VERIFICATION_20261029_9bb3b12b1f9b4658b5892679672bbf1a.md": "8eddd995c4351154275b3a6d60d328a6833c57fd6699dfb4dd698fe30b226d04",
    "docs/current/d/C11D_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_REVIEW_20261029_V1.md": "4cffdb3ef7edb3f4d201391b8156e4691ad0b98fdad2859703bcc20f589dd62f",
    "docs/current/d/C11D_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_MATRIX_20261029_V1.json": "de2d5e548e00442ee8f15ca7514744b402c6400b4a8497b2b6f6671d29b00390",
    "definitions/c11d/review/D_RENDERER_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_MATRIX_SCHEMA_V1.json": "cca024de2dd6a01805f431d3b140c77dce12bf781d12aee11df35fd426af910b",
    "tools/c11d/d9/test_d_renderer_phase_q_semantic_policy_dependency_review_20261029.py": "6cfa58e7f442d866d172a4ec5ee6d2e091ca0e6ff2c788cb776bf05e5e0aff1a",
    "docs/current/d/C11D_PHASE_Q_VERIFIER_RECOVERY_AND_REVIEW_CLOSEOUT_20261029_2175920e62954eb0b0fba64555870767.md": "5a8e62f9d38bbf31cfb64066fec57f17d2f931da2349f0078b7ea62ed77851d1",
    "docs/current/d/C11D_PHASE_R_OPERATOR_POLICY_DECISION_PACKET_20261029_V1.md": "7aa7bf2ccc67d606f2a9c1b3808a42b2dd07cedd8c792d8c118c185f85c708a2",
    "docs/current/d/C11D_PHASE_R_OPERATOR_POLICY_DECISION_PACKET_20261029_V1.json": "6b6cd0881e207b0b3ce55de7db87b7aa325f2ea65ecaa94d7efc1afd2a9b386a",
    "definitions/c11d/review/D_RENDERER_PHASE_R_OPERATOR_POLICY_DECISION_PACKET_SCHEMA_V1.json": "49d51d5b562c3834556ee9c78a40c3a5443a7e02c9be0d216fe1d917e002f539",
    "tools/c11d/d9/test_d_renderer_phase_r_operator_policy_decision_packet_20261029.py": "0e1b9a570de5068b1b506f8bca196f914b297b74ee8311773be86df218902817",
    "docs/current/d/C11D_PHASE_R_OPERATOR_POLICY_DECISION_PREPARATION_ACCEPTANCE_REVIEW_20261029_V1.md": "b6df812cb3242a175e750aa73af35c43a56d298960e0387bb734da746f5a7a91"
}
EXPECTED_DECISIONS = [
    "R-01-TIMEBASE-SAMPLING",
    "R-02-SPATIAL-MAPPING",
    "R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y",
    "R-04-VISIBILITY-AND-REGION-OWNERSHIP",
    "R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING",
    "R-06-INVALID-DATA-AND-TRACK-INTEGRITY",
    "R-07-SEMANTIC-VISUAL-OWNERSHIP",
    "R-08-CHALLENGE-008-DURATION-CONFLICT",
    "R-09-CHALLENGE-009-DURATION-AND-COUNT-ROLE",
]
EXPECTED_REQUIRED_FIELDS = [
    "authority_record_id", "decision_id", "exact_option_id_or_exact_policy_text",
    "authority_name_or_role", "authority_scope", "effective_date", "rationale",
    "source_pins", "acceptance_test_obligations", "approval_provenance",
    "immutable_record_location",
]
def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

class PhaseSAuthorityEvidencePreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        cls.review = REVIEW_PATH.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.r_packet = json.loads(R_PACKET_PATH.read_text(encoding="utf-8"))
        cls.q_matrix = json.loads(Q_MATRIX_PATH.read_text(encoding="utf-8"))
        cls.decisions = {d["decision_id"]: d for d in cls.packet["decisions"]}

    def test_01_schema_identifier(self): self.assertEqual(self.packet["schema"], "C11D-PHASE-S-AUTHORITY-EVIDENCE-PREFLIGHT-V1")
    def test_02_read_only_mode(self): self.assertEqual(self.packet["mode"], "READ_ONLY_AUTHORITY_EVIDENCE_PREFLIGHT")
    def test_03_preflight_not_adjudication(self): self.assertEqual(self.packet["status"], "AUTHORITY_EVIDENCE_NOT_PRESENT_IN_PINNED_PHASE_P_Q_R_RECORD_SET")
    def test_04_bounded_audit_not_global_claim(self): self.assertFalse(self.packet["audit_scope"]["global_absence_claim"])
    def test_05_no_authority_decisions_found_in_bounded_set(self): self.assertEqual(self.packet["audit_scope"]["authority_decisions_found"], 0)
    def test_06_nine_decisions_scoped(self): self.assertEqual(self.packet["audit_scope"]["decisions_scoped"], 9)
    def test_07_exact_nine_decision_ids(self): self.assertEqual(list(self.decisions), EXPECTED_DECISIONS)
    def test_08_all_nine_have_no_authority_evidence(self): self.assertTrue(all(d["authority_evidence_status"] == "NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET" for d in self.packet["decisions"]))
    def test_09_no_authority_record_path_fabricated(self): self.assertTrue(all(d["authority_record_path"] is None for d in self.packet["decisions"]))
    def test_10_no_policy_adopted(self): self.assertTrue(all(d["policy_adoption"] == "NOT_ADOPTED" for d in self.packet["decisions"]))
    def test_11_all_decisions_keep_blocked(self): self.assertTrue(all(d["current_action"] == "KEEP_BLOCKED_NO_POLICY_ADOPTION" for d in self.packet["decisions"]))
    def test_12_all_decisions_retain_options_unselected(self): self.assertTrue(all(len(d["option_ids_not_selected"]) >= 1 for d in self.packet["decisions"]))
    def test_13_authority_record_has_11_required_fields(self): self.assertEqual(self.packet["authority_record_contract"]["required_fields"], EXPECTED_REQUIRED_FIELDS)
    def test_14_no_generic_engineering_approval_as_policy_authority(self): self.assertTrue(any("generic approval" in s.lower() for s in self.packet["authority_record_contract"]["validation_rules"]))
    def test_15_pass_or_assistant_packet_not_authority(self): self.assertTrue(any("test PASS" in s for s in self.packet["authority_record_contract"]["insufficient_evidence_examples"]))
    def test_16_default_is_fail_closed(self): self.assertEqual(self.packet["authority_record_contract"]["default_if_missing_or_ambiguous"], "KEEP_BLOCKED_NO_POLICY_ADOPTION")
    def test_17_phase_p_scope_limited_to_provenance(self): self.assertIn("ONLY_NOT_VISUAL_CONSUMPTION", self.packet["phase_dependencies"]["phase_p_status"])
    def test_18_phase_q_read_only_inventory(self): self.assertEqual(self.packet["phase_dependencies"]["phase_q_status"], "PASS_READ_ONLY_INVENTORY")
    def test_19_phase_r_preparation_only(self): self.assertEqual(self.packet["phase_dependencies"]["phase_r_status"], "PASS_DECISION_PREPARATION_ONLY_NO_POLICY_ADOPTION")
    def test_20_phase_r_decision_ids_match_exactly(self): self.assertEqual([d["decision_id"] for d in self.r_packet["decisions"]], EXPECTED_DECISIONS); self.assertEqual(len(self.r_packet["decisions"]), 9)
    def test_21_schema_governance_and_timing_locks(self): self.assertEqual(self.schema["properties"]["schema"]["const"], self.packet["schema"]); self.assertEqual((self.schema["properties"]["decisions"]["minItems"], self.schema["properties"]["decisions"]["maxItems"]), (9,9)); self.assertEqual(self.packet["governance"]["renderer"], "OFF"); self.assertEqual([self.packet["governance"][k] for k in ("approved_bindings", "approved_custom_data_bindings", "approved_renderer_projection_bindings")], [0,0,0]); self.assertEqual(self.packet["governance"]["release_authority"], "NONE"); self.assertFalse(self.packet["governance"]["freeze_eligible"]); self.assertEqual([(x["declared_total_duration_seconds"], x["phase_duration_sum_seconds"], x["status"]) for x in self.packet["timing_conflicts"]], [(11,12,"BLOCKER_NO_CORRECTION_INFERRED"),(11,12,"BLOCKER_NO_CORRECTION_INFERRED")])

# One separate test method per source pin: exact hashes are the provenance gate.
def _make_pin_test(rel, expected):
    def _test(self):
        path = ROOT / rel
        self.assertTrue(path.is_file(), rel)
        self.assertEqual(sha(path), expected, rel)
    return _test

for _i, (_rel, _expected) in enumerate(EXPECTED_PINS.items(), start=22):
    setattr(PhaseSAuthorityEvidencePreflightTests, f"test_{_i:02d}_source_pin_{_i:02d}", _make_pin_test(_rel, _expected))

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PhaseSAuthorityEvidencePreflightTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    count = result.testsRun
    if result.wasSuccessful() and count == 40:
        print(f"PHASE_S_AUTHORITY_PREFLIGHT_TESTS={count}/{count}")
        raise SystemExit(0)
    print(f"PHASE_S_AUTHORITY_PREFLIGHT_TESTS=FAIL; passed={count-len(result.failures)-len(result.errors)}; total={count}")
    raise SystemExit(1)
