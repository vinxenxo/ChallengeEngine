from __future__ import annotations

from copy import deepcopy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import d_renderer_dynamic_request_payload_binding as binder  # noqa: E402
import d_renderer_candidate_seed_domain_audit as cross_audit  # noqa: E402
import d_renderer_seed_domain_collision_audit as audit  # noqa: E402


class SeedDomainCollisionRejectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract, cls.schema, cls.pins = audit._load_and_validate_contract(ROOT)
        cls.report = audit.run_seed_domain_rejection_audit(ROOT)

    def test_contract_pins_twenty_three_sources_and_preserves_c11c(self):
        self.assertEqual(len(self.pins), 23)
        self.assertEqual(self.contract["source_pin_count"], 23)
        self.assertEqual(self.contract["source_of_truth"]["frozen_c11c_manifest_sha256"], audit.EXPECTED_MANIFEST_SHA256)
        self.assertIn("tools/c11d/d9/d_render_adapter.py", {p["path"] for p in self.pins})
        self.assertEqual(audit._sha_file(ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"), audit.EXPECTED_MANIFEST_SHA256)

    def test_missing_or_invalid_seed_forms_rejected_for_both_content_types(self):
        outcomes = audit._rejected_implicit_seed_cases(ROOT)
        self.assertEqual(len(outcomes), 20)
        self.assertEqual({row["result"] for row in outcomes}, {"REJECTED_AS_REQUIRED"})
        self.assertEqual({row["content_type"] for row in outcomes}, {"challenges", "visual_loops"})
        self.assertEqual({row["case"] for row in outcomes}, set(audit.NEGATIVE_CASES))

    def test_equal_numeric_seed_values_rejected_before_godot_for_each_selector_and_value(self):
        outcomes = audit._rejected_numeric_seed_collisions(ROOT)
        self.assertEqual(len(outcomes), 4)
        self.assertEqual({row["collision_value"] for row in outcomes}, {12345, 840001})
        self.assertEqual({row["content_type"] for row in outcomes}, {"challenges", "visual_loops"})
        self.assertEqual({row["result"] for row in outcomes}, {"REJECTED_BEFORE_GODOT_AS_REQUIRED"})

    def test_main_report_passes_strict_schema_but_stays_non_admissible(self):
        report = deepcopy(self.report)
        self.assertEqual(report["explicit_seed_negative_cases"], {"passed":20,"total":20})
        self.assertEqual(report["numeric_seed_collision_rejections"], {"passed":4,"total":4})
        self.assertEqual(report["runtime_invocations"], 0)
        self.assertTrue(report["all_rejections_precede_godot"])
        self.assertFalse(report["seed_domains_complete_for_candidate_input"])
        self.assertFalse(report["execution_boundary"]["renderer_input_emitted"])
        self.assertFalse(report["execution_boundary"]["media_created"])
        self.assertEqual(report["execution_boundary"]["d4_8"], "BLOCKED")
        audit._validate_report_schema(report, self.schema)

    def test_weakened_collision_policy_fails_closed(self):
        altered = deepcopy(self.contract["seed_policy"])
        altered["equal_numeric_values_across_domains"] = "ALLOWED"
        with self.assertRaisesRegex(audit.SeedCollisionAuditError, "Seed-domain policy was weakened"):
            audit._validate_seed_policy(altered)

    def test_runner_never_invokes_godot_or_writes_artifacts(self):
        source = (HERE / "d_renderer_seed_domain_collision_audit.py").read_text(encoding="utf-8")
        for forbidden in ("subprocess.run", "MovieWriter", "render_video(", "FileAccess.open(", "write_text(", "write_bytes("):
            self.assertNotIn(forbidden, source)
        self.assertIn('"runtime": "PYTHON_PREFLIGHT_REJECTION_ONLY_NO_GODOT_INVOCATION"', source)
        self.assertIn('"renderer_activation": False', source)
        self.assertIn('"media_created": False', source)

    def test_cross_type_selector_scope_remains_the_accepted_pair(self):
        self.assertEqual(set(cross_audit.EXPECTED_SELECTOR_SCOPE), {"challenges", "visual_loops"})
        self.assertEqual(self.contract["experiment"]["collision_values_tested"], [12345, 840001])


if __name__ == "__main__":
    unittest.main(verbosity=2)
