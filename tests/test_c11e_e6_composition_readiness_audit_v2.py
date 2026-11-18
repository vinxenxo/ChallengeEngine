import json
import sys
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
MODULE = PROJECT / "tools" / "c11d" / "d9" / "c11e_e6_composition_readiness_audit_v2.py"
sys.path.insert(0, str(MODULE.parent))
import c11e_e6_composition_readiness_audit_v2 as audit

class CompositionReadinessV2Tests(unittest.TestCase):
    def _json(self, rel):
        return json.loads((PROJECT / rel).read_text(encoding="utf-8"))

    def test_scope_exactly_18_rows_and_abc_nested(self):
        scope=self._json("definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json")
        rows=scope["smoke18_scenario_contract"]
        self.assertEqual(rows["top_level_rows"],18)
        self.assertEqual(rows["challenge_rows"]+rows["loop_rows"]+rows["drill_rows"],18)
        sub=scope["operator_approved_scope"]["challenge_subruns"]
        self.assertTrue(sub["nested_under_challenge_rows"])
        self.assertFalse(sub["additional_top_level_rows"])
        self.assertEqual(sub["count"],18)

    def test_music_fixture_is_approved_test_only(self):
        scope=self._json("definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json")
        f=scope["music_fixture"]
        self.assertTrue(f["operator_approved_test_fixture"])
        self.assertIn("NOT_PRODUCT_CONTRACT",f["authority"])
        c=f["challenge_only"]
        self.assertEqual((c["A_music_seed"],c["B_music_seed"],c["C_music_seed"],c["tempo_bpm"]),(840001,840001,840002,104))
        self.assertIn("FFPROBE",c["duration_rule"])

    def test_spanish_editorial_fixture_remains_pending(self):
        approval=self._json("definitions/c11e/test_only/C11E_E6_OPERATOR_SCOPE_APPROVAL_RECORD_V1.json")
        self.assertEqual(approval["pending_operator_decision"]["status"],"PENDING")

    def test_v2_pin_corrects_only_known_bad_literal(self):
        old=self._json("definitions/c11e/test_only/C11E_E6_COMPOSITION_READINESS_SOURCE_PINS_V1.json")
        new=self._json("definitions/c11e/test_only/C11E_E6_COMPOSITION_READINESS_SOURCE_PINS_V2.json")
        def get(doc): return next(x for x in doc["pins"] if x["path"]==audit.CONSUMER_REL)["sha256"]
        self.assertEqual(get(old),audit.V1_BAD_PIN)
        self.assertEqual(get(new),audit.ACCEPTED_PIN)
        other_old={x["path"]:x["sha256"] for x in old["pins"] if x["path"]!=audit.CONSUMER_REL}
        other_new={x["path"]:x["sha256"] for x in new["pins"] if x["path"]!=audit.CONSUMER_REL}
        self.assertEqual(other_old,other_new)

    def test_prior_pin_adjudication_is_exact(self):
        doc=self._json("definitions/c11e/test_only/C11E_E6_COMPOSITION_READINESS_SOURCE_PINS_V2.json")
        a=doc["pin_adjudication"]
        self.assertEqual(a["classification"],"AUDIT_PACKAGE_PIN_LITERAL_ERROR_NOT_LIVE_SOURCE_REGRESSION")
        self.assertEqual(a["accepted_prior_e6_pin_receipt"]["sha256"],audit.PRIOR_PIN_RECEIPT_SHA)
        self.assertEqual(a["v1_blocked_receipt"]["sha256"],audit.V1_AUDIT_RECEIPT_SHA)
        self.assertFalse(a["source_mutation_authorized"])

    def test_v2_pin_list_has_unique_paths_and_17_files(self):
        doc=self._json("definitions/c11e/test_only/C11E_E6_COMPOSITION_READINESS_SOURCE_PINS_V2.json")
        paths=[x["path"] for x in doc["pins"]]
        self.assertEqual(len(paths),17)
        self.assertEqual(len(paths),len(set(paths)))

    def test_loop_needs_six_new_d_compositions(self):
        scope=self._json("definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json")
        loop=scope["evidence_disposition"]["visual_loop"]
        self.assertFalse(loop["d_composition_reuse_eligible"])
        self.assertTrue(loop["d_composition_required_for_each_row"])

    def test_drill_is_candidate_reuse_not_accepted(self):
        scope=self._json("definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json")
        self.assertEqual(scope["evidence_disposition"]["e6_accepted_scenarios"],0)
        self.assertTrue(scope["evidence_disposition"]["visual_drill"]["reuse_requires_exact_e6_predicate_revalidation"])

    def test_successor_policy_is_draft_and_no_execution(self):
        policy=self._json("definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V1.json")
        self.assertEqual(policy["status"],"DRAFT_PREPARED_NOT_APPROVED_NOT_EXECUTION_AUTHORIZED")
        flags=policy["explicit_non_authorizations"]
        self.assertFalse(flags["godot"]); self.assertFalse(flags["ffmpeg"]); self.assertFalse(flags["ffprobe"])
        self.assertFalse(flags["media_creation"]); self.assertEqual(flags["release_authority"],"NONE")

    def test_no_renderer_or_batch_authority_in_scope(self):
        scope=self._json("definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json")
        e=scope["execution_authority"]
        self.assertFalse(e["e6_test_only_authorized"]); self.assertFalse(e["renderer_activation"])
        self.assertFalse(e["production_dispatch"]); self.assertEqual(e["release_authority"],"NONE")

    def test_old_challenge_plan_remains_unmodified_and_reprepare_required(self):
        policy=self._json("definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V1.json")
        self.assertTrue(policy["evidence_rules"]["never_mutate_c11c_or_original_d4_8"])
        self.assertIn("Challenge new plan-only manifest", policy["prerequisites_before_final_authorization"][1])

    def test_pin_adjudication_function_requires_both_exact_receipts(self):
        import tempfile
        from unittest.mock import patch
        def fake_check(root, rel, sha, expected_bytes=None):
            return {"path":rel,"status":"PASS","expected_sha256":sha}
        prior={"accepted_33_source_pin_checks":[{"path":audit.CONSUMER_REL,"actual_sha256":audit.ACCEPTED_PIN,"expected_sha256":audit.ACCEPTED_PIN,"status":"PASS"}]}
        v1={"source_pin_summary":{"expected":17,"passed":16,"failed":1,"rows":[{"path":audit.CONSUMER_REL,"expected_sha256":audit.V1_BAD_PIN,"actual_sha256":audit.ACCEPTED_PIN,"actual_bytes":26367,"status":"MISMATCH"}]},"status":"BLOCKED_SOURCE_OR_EVIDENCE_RECONCILIATION"}
        with patch.object(audit,"check_file",side_effect=fake_check), patch.object(audit,"read_json",side_effect=[prior,v1]):
            result=audit.adjudicate_v1_pin_error(Path("."))
        self.assertEqual(result["status"],"PASS_AUDIT_PACKAGE_PIN_ENTRY_ERROR_RECONCILED")

if __name__ == "__main__": unittest.main(verbosity=2)
