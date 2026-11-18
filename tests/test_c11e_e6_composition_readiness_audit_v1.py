import json
import unittest
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
MODULE = PROJECT / "tools" / "c11d" / "d9" / "c11e_e6_composition_readiness_audit_v1.py"
sys.path.insert(0, str(MODULE.parent))
import c11e_e6_composition_readiness_audit_v1 as audit

class CompositionReadinessTests(unittest.TestCase):
    def test_scope_is_exactly_18_rows(self):
        scope=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json").read_text(encoding="utf-8"))
        rows=scope["smoke18_scenario_contract"]
        self.assertEqual(rows["top_level_rows"],18)
        self.assertEqual(rows["challenge_rows"]+rows["loop_rows"]+rows["drill_rows"],18)

    def test_challenge_abcs_are_nested(self):
        scope=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json").read_text(encoding="utf-8"))
        sub=scope["operator_approved_scope"]["challenge_subruns"]
        self.assertTrue(sub["nested_under_challenge_rows"])
        self.assertFalse(sub["additional_top_level_rows"])
        self.assertEqual(sub["count"],18)

    def test_music_fixture_is_test_only(self):
        scope=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json").read_text(encoding="utf-8"))
        fixture=scope["music_fixture"]
        self.assertTrue(fixture["operator_approved_test_fixture"])
        self.assertIn("NOT_PRODUCT_CONTRACT",fixture["authority"])
        self.assertEqual(fixture["challenge_only"]["A_music_seed"],840001)
        self.assertEqual(fixture["challenge_only"]["C_music_seed"],840002)

    def test_no_execution_authority(self):
        scope=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json").read_text(encoding="utf-8"))
        authority=scope["execution_authority"]
        self.assertFalse(authority["e6_test_only_authorized"])
        self.assertFalse(authority["renderer_activation"])
        self.assertFalse(authority["production_dispatch"])
        self.assertEqual(authority["release_authority"],"NONE")

    def test_loop_is_not_misrepresented_as_d_compositor_pass(self):
        scope=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json").read_text(encoding="utf-8"))
        loop=scope["evidence_disposition"]["visual_loop"]
        self.assertFalse(loop["d_composition_reuse_eligible"])
        self.assertTrue(loop["d_composition_required_for_each_row"])

    def test_drill_reuse_is_only_candidate(self):
        scope=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json").read_text(encoding="utf-8"))
        self.assertTrue(scope["evidence_disposition"]["visual_drill"]["reuse_requires_exact_e6_predicate_revalidation"])
        self.assertEqual(scope["evidence_disposition"]["e6_accepted_scenarios"],0)

    def test_editorial_test_fixture_not_implicitly_approved(self):
        scope=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json").read_text(encoding="utf-8"))
        self.assertEqual(scope["editorial_test_fixture"]["status"],"PROPOSED_VALUES_REQUIRE_OPERATOR_APPROVAL")

    def test_scope_approval_explicitly_excludes_render(self):
        approval=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_OPERATOR_SCOPE_APPROVAL_RECORD_V1.json").read_text(encoding="utf-8"))
        flags=approval["explicit_non_authorizations"]
        self.assertFalse(flags["godot"])
        self.assertFalse(flags["ffmpeg"])
        self.assertFalse(flags["mux"])
        self.assertFalse(flags["renderer_activation"])

    def test_pin_document_has_unique_paths(self):
        doc=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_COMPOSITION_READINESS_SOURCE_PINS_V1.json").read_text(encoding="utf-8"))
        paths=[x["path"] for x in doc["pins"]]
        self.assertEqual(len(paths),len(set(paths)))
        self.assertGreaterEqual(len(paths),15)

    def test_policy_preserves_d4_8_and_c11c_locks(self):
        scope=json.loads((PROJECT/"definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_SCOPE_V1.json").read_text(encoding="utf-8"))
        self.assertEqual(scope["authority"]["d4_8_r1v_v2_sha256"],"0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")
        self.assertEqual(scope["authority"]["frozen_c11c_manifest_sha256"],"e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")

if __name__ == "__main__": unittest.main(verbosity=2)
