from __future__ import annotations
import copy
import unittest
from pathlib import Path

from d_renderer_editorial_field_consumption_audit import (
    EditorialFieldConsumptionAuditError,
    build_audit,
    validate_audit,
    _root,
    _read_json,
    CONTRACT_REL,
    SCHEMA_REL,
)

ROOT = Path(__file__).resolve().parents[3]

class EditorialFieldConsumptionAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = build_audit(ROOT)

    def test_three_fixed_content_types_are_audited(self):
        self.assertEqual([x["content_type"] for x in self.audit["content_results"]], ["challenges", "visual_loops", "visual_drills"])
        self.assertEqual(self.audit["summary"]["content_types_reviewed"], 3)

    def test_enabled_field_counts_match_editorial_model(self):
        counts = {x["content_type"]: x["canonical_editorial_field_count"] for x in self.audit["content_results"]}
        self.assertEqual(counts, {"challenges": 6, "visual_loops": 4, "visual_drills": 4})
        self.assertEqual(self.audit["summary"]["enabled_field_instances"], 14)

    def test_review_chain_has_exact_value_parity_but_payload_does_not_consume(self):
        self.assertEqual(self.audit["summary"]["exact_review_chain_field_instances"], 14)
        self.assertEqual(self.audit["summary"]["visual_payload_consumed_field_instances"], 0)
        for result in self.audit["content_results"]:
            self.assertEqual(result["canonical_review_parity"], "PASS")
            self.assertFalse(result["visual_payload_consumption_complete"])
            self.assertFalse(result["video_render_ready"])
            self.assertTrue(result["payload_field_scan"]["no_editorial_value_keys_found"])

    def test_language_is_metadata_not_a_text_instruction(self):
        for result in self.audit["content_results"]:
            language = next(x for x in result["editorial_fields"] if x["field"] == "language")
            self.assertEqual(language["review_chain_state"], "LANGUAGE_METADATA_ONLY")

    def test_challenge_only_fields_are_not_claimed_for_loop_or_drill(self):
        for content_type in ("visual_loops", "visual_drills"):
            fields = {x["field"] for x in next(r for r in self.audit["content_results"] if r["content_type"] == content_type)["editorial_fields"]}
            self.assertNotIn("player_name", fields)
            self.assertNotIn("challenge_label", fields)

    def test_unknown_or_unapproved_states_remain_locked(self):
        self.assertFalse(self.audit["summary"]["candidate_input_admissible"])
        self.assertFalse(self.audit["execution_boundary"]["renderer_native_input_emitted"])
        self.assertFalse(self.audit["execution_boundary"]["renderer_dispatch_invoked"])
        self.assertEqual(self.audit["execution_boundary"]["d4_8"], "BLOCKED")
        self.assertEqual(self.audit["execution_boundary"]["release_authority"], "NONE")
        self.assertEqual(self.audit["approval_state"]["d9_17"], "BLOCKED_NO_GO")

    def test_receipt_revalidates_exactly(self):
        self.assertTrue(validate_audit(self.audit, ROOT))

    def test_changed_field_state_is_rejected_even_when_resigned(self):
        bad = copy.deepcopy(self.audit)
        bad["content_results"][0]["editorial_fields"][0]["visual_payload_consumption_state"] = "CONSUMED"
        from d_renderer_editorial_field_consumption_audit import _sha
        bad["audit_sha256"] = _sha({k: v for k, v in bad.items() if k != "audit_sha256"})
        with self.assertRaises(EditorialFieldConsumptionAuditError):
            validate_audit(bad, ROOT)

    def test_false_readiness_is_rejected(self):
        bad = copy.deepcopy(self.audit)
        bad["summary"]["video_render_ready"] = True
        from d_renderer_editorial_field_consumption_audit import _sha
        bad["audit_sha256"] = _sha({k: v for k, v in bad.items() if k != "audit_sha256"})
        with self.assertRaises(EditorialFieldConsumptionAuditError):
            validate_audit(bad, ROOT)

    def test_audit_contract_and_schema_are_present_and_strict(self):
        contract = _read_json(ROOT, CONTRACT_REL)
        schema = _read_json(ROOT, SCHEMA_REL)
        self.assertEqual(contract["status"], "PREPARATION_ONLY_FIELD_CONSUMPTION_GAP_AUDIT_NOT_RENDERER_INPUT")
        self.assertIs(schema["additionalProperties"], False)
        self.assertEqual(set(schema["required"]), set(schema["properties"]))

    def test_no_payload_or_receipt_files_were_written(self):
        self.assertFalse(self.audit["execution_boundary"]["payload_files_written"])
        self.assertFalse(self.audit["execution_boundary"]["receipt_files_written"])
        self.assertIsNone(self.audit["execution_boundary"]["output_artifact_path"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
