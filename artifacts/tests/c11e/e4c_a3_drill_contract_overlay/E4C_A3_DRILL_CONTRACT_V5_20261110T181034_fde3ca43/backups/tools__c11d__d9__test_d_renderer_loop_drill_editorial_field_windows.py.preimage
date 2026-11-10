from __future__ import annotations
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from d_renderer_loop_drill_editorial_field_windows import FieldWindowProposalError, propose_field_windows, validate_contract

ROOT = Path(__file__).resolve().parents[3]
FIELDS = {"title": "TEST TITLE", "subtitle": "TEST SUBTITLE", "call_to_action": "TEST CTA", "language": "es"}

class LoopDrillEditorialFieldWindowProposalTests(unittest.TestCase):
    def test_contract_schema_lineage_and_proposed_state(self):
        result = validate_contract(ROOT)
        self.assertEqual(set(result["fixtures"]), {"visual_loops", "visual_drills"})
        self.assertEqual(result["contract"]["status"], "PROPOSAL_ONLY_NOT_RENDERER_INPUT")
        self.assertFalse(result["contract"]["approval_state"]["loop_editorial_field_mapping_approved"])
        self.assertFalse(result["contract"]["approval_state"]["drill_editorial_field_mapping_approved"])

    def test_loop_full_span(self):
        result = propose_field_windows("visual_loops", 600, FIELDS)
        self.assertEqual([(x["field_id"], x["start_frame"], x["end_frame"]) for x in result["field_windows"]], [("title",0,600),("subtitle",0,600),("call_to_action",0,600)])

    def test_drill_full_span(self):
        result = propose_field_windows("visual_drills", 630, FIELDS)
        self.assertTrue(all(x["end_frame"] == 630 and x["frame_count"] == 630 for x in result["field_windows"]))

    def test_language_is_metadata_only(self):
        result = propose_field_windows("visual_loops", 600, FIELDS)
        self.assertEqual(result["metadata_only_fields"], ["language"])
        self.assertNotIn("language", {x["field_id"] for x in result["field_windows"]})

    def test_empty_visual_fields_are_suppressed(self):
        fields = dict(FIELDS, subtitle="", call_to_action="")
        result = propose_field_windows("visual_drills", 630, fields)
        self.assertEqual(result["suppressed_empty_fields"], ["subtitle", "call_to_action"])
        self.assertEqual([x["field_id"] for x in result["field_windows"]], ["title"])

    def test_policy_stays_unapproved_and_no_renderer_input(self):
        result = propose_field_windows("visual_loops", 600, FIELDS)
        self.assertEqual(result["policy_state"], "PROPOSED_NOT_APPROVED")
        self.assertFalse(result["renderer_native_input_emitted"])
        self.assertFalse(result["media_created"])

    def test_half_open_interval_has_exact_frame_count(self):
        result = propose_field_windows("visual_loops", 600, FIELDS)
        for window in result["field_windows"]:
            self.assertEqual(window["end_frame"] - window["start_frame"], window["frame_count"])

    def test_request_text_preserved_verbatim(self):
        result = propose_field_windows("visual_loops", 600, FIELDS)
        self.assertEqual(result["field_windows"][0]["source_text"], FIELDS["title"])

    def test_negative_unsupported_challenge_type(self):
        with self.assertRaises(FieldWindowProposalError): propose_field_windows("challenges", 450, FIELDS)

    def test_negative_zero_frame_count(self):
        with self.assertRaises(FieldWindowProposalError): propose_field_windows("visual_loops", 0, FIELDS)

    def test_negative_negative_frame_count(self):
        with self.assertRaises(FieldWindowProposalError): propose_field_windows("visual_drills", -1, FIELDS)

    def test_negative_bool_frame_count(self):
        with self.assertRaises(FieldWindowProposalError): propose_field_windows("visual_drills", True, FIELDS)

    def test_negative_unknown_field_rejected(self):
        with self.assertRaisesRegex(FieldWindowProposalError, "unknown editorial field"):
            propose_field_windows("visual_loops", 600, dict(FIELDS, hook="not declared"))

    def test_negative_missing_required_field(self):
        with self.assertRaisesRegex(FieldWindowProposalError, "all four canonical"):
            propose_field_windows("visual_loops", 600, {"title":"x","subtitle":"x","call_to_action":"x"})

    def test_negative_non_string_editorial_value(self):
        with self.assertRaises(FieldWindowProposalError): propose_field_windows("visual_loops", 600, dict(FIELDS, title=None))

    def test_negative_metadata_language_never_gets_window(self):
        result = propose_field_windows("visual_drills", 630, FIELDS)
        self.assertNotIn("language", [x["field_id"] for x in result["field_windows"]])

    def test_negative_cannot_promote_contract_status(self):
        root = self._copy_root()
        p = root / "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
        data = json.loads(p.read_text(encoding="utf-8")); data["status"] = "APPROVED"; p.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(FieldWindowProposalError): validate_contract(root)

    def test_negative_cannot_promote_approval_state(self):
        root = self._copy_root()
        p = root / "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
        data = json.loads(p.read_text(encoding="utf-8")); data["approval_state"]["loop_editorial_field_mapping_approved"] = True; p.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(FieldWindowProposalError): validate_contract(root)

    def test_negative_lineage_digest_mismatch(self):
        root = self._copy_root()
        p = root / "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
        data = json.loads(p.read_text(encoding="utf-8")); data["source_lineage"][0]["sha256"] = "0" * 64; p.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(FieldWindowProposalError): validate_contract(root)

    def test_negative_fixture_frame_count_mismatch(self):
        root = self._copy_root()
        p = root / "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
        data = json.loads(p.read_text(encoding="utf-8")); data["review_fixtures"][0]["frame_count"] = 601; p.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(FieldWindowProposalError): validate_contract(root)

    def test_negative_wrong_field_region_rejected(self):
        root = self._copy_root()
        p = root / "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
        data = json.loads(p.read_text(encoding="utf-8")); data["mapping_policy"]["visible_fields"][0]["target_region"] = "FOOTER"; p.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(FieldWindowProposalError): validate_contract(root)

    def test_negative_execution_boundary_cannot_enable_renderer(self):
        root = self._copy_root()
        p = root / "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
        data = json.loads(p.read_text(encoding="utf-8")); data["execution_boundary"]["renderer_activation"] = True; p.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(FieldWindowProposalError): validate_contract(root)

    def _copy_root(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for directory in ("definitions", "profiles", "release"):
            shutil.copytree(ROOT / directory, root / directory)
        return root

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LoopDrillEditorialFieldWindowProposalTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("C11-D RENDERER LOOP/DRILL EDITORIAL FIELD-WINDOW PROPOSAL " + ("PASS" if result.wasSuccessful() else "FAIL") + " | loop=600@30FPS | drill=630@30FPS | full_span_nonempty_fields | empty=suppressed | language=metadata_only | policy=PROPOSED_NOT_APPROVED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    raise SystemExit(not result.wasSuccessful())
