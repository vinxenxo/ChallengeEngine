"""Focused read-only tests for the E4B policy-readiness audit."""
from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

import c11e_e4b_loop_policy_readiness as audit


def _root() -> Path:
    return Path(os.environ.get("C11E_PROJECT_ROOT", Path(__file__).resolve().parents[3])).resolve()


def _gui() -> Path:
    return Path(os.environ.get(
        "C11E_GUI_EVIDENCE_ROOT",
        _root() / "artifacts/tests/c11e/e4b_loop_family_matrix/E4B_LOOP_GUI_20261106T211920Z_F9377504",
    )).resolve()


def _cli() -> Path:
    return Path(os.environ.get(
        "C11E_CLI_EVIDENCE_ROOT",
        _root() / "artifacts/tests/c11e/e4b_loop_family_matrix/CLI_20261106T212054Z-DE8364C4",
    )).resolve()


class PolicyReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = _root()
        cls.gui = _gui()
        cls.cli = _cli()

    def test_gui_report_sidecar(self) -> None:
        result = audit.verify_sidecar(self.gui, "matrix_report.json")
        self.assertTrue(result["sidecar_pass"])

    def test_gui_template_sidecar(self) -> None:
        result = audit.verify_sidecar(self.gui, "matrix_request_template.json")
        self.assertTrue(result["sidecar_pass"])

    def test_cli_report_and_template_sidecars(self) -> None:
        self.assertTrue(audit.verify_sidecar(self.cli, "matrix_report.json")["sidecar_pass"])
        self.assertTrue(audit.verify_sidecar(self.cli, "matrix_request_template.json")["sidecar_pass"])

    def test_gui_report_scope_and_seed_distribution(self) -> None:
        report = audit.read_json(self.gui / "matrix_report.json")
        summary = audit._check_matrix_report(report, "GUI")
        self.assertEqual(summary["case_count"], 81)
        self.assertEqual(summary["selector_count"], 27)
        self.assertEqual(summary["seed_relation_count"], 27)

    def test_cli_report_scope_and_seed_distribution(self) -> None:
        report = audit.read_json(self.cli / "matrix_report.json")
        summary = audit._check_matrix_report(report, "CLI")
        self.assertEqual(summary["case_count"], 81)
        self.assertEqual(summary["deterministic_repeats"], 81)

    def test_nine_canonical_identities_match_for_all_cases(self) -> None:
        gui = audit.read_json(self.gui / "matrix_report.json")
        cli = audit.read_json(self.cli / "matrix_report.json")
        parity = audit._compare_gui_cli(gui, cli)
        self.assertEqual(len(parity["direct_identity_fields"]), 9)
        self.assertTrue(all(value == 81 for value in parity["direct_identity_fields"].values()))

    def test_d98_metadata_remains_plan_only_pending(self) -> None:
        d98 = audit.read_json(self.root / audit.D98_MODEL)
        loop = d98["content_types"]["visual_loops"]
        self.assertEqual(loop["model_state"], "ACTIVE_MODEL_ONLY")
        self.assertEqual(loop["request_plan_compatibility"], "PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER")

    def test_all_current_policy_proposals_remain_unapproved(self) -> None:
        for label, relpath in audit.POLICY_FILES.items():
            document = audit.read_json(self.root / relpath)
            audit._approval_booleans_false(document, label)
            if label != "loop_composition":
                self.assertEqual(document["status"], "PROPOSAL_ONLY_NOT_RENDERER_INPUT")
                state = document.get("policy", document.get("mapping_policy", {})).get("state")
                self.assertEqual(state, "PROPOSED_NOT_APPROVED")
            else:
                self.assertEqual(document["status"], "PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT")

    def test_packet_v1_has_three_stale_policy_hashes(self) -> None:
        text = (self.root / audit.APPROVAL_PACKET).read_text(encoding="utf-8-sig")
        self.assertEqual(text.splitlines()[2].strip(), "**Status:** `REVIEW_PACKET_ONLY_ALL_POLICIES_UNAPPROVED`")
        expected = {
            "shared_regions": False,
            "loop_drill_windows": True,
            "delivery_timebase": True,
            "audio_music_delivery": True,
        }
        current = {label: audit.sha256_file(self.root / rel) for label, rel in audit.POLICY_FILES.items() if label != "loop_composition"}
        stale = [label for label in expected if audit.parse_packet_pin(text, label) != current[label]]
        self.assertEqual(set(stale), {"loop_drill_windows", "delivery_timebase", "audio_music_delivery"})

    def test_historical_payload_scope_is_geometric_only_and_blocked(self) -> None:
        exact = (self.root / audit.EXACT_SELECTOR_CHECKPOINT).read_text(encoding="utf-8-sig")
        self.assertIn("exact_selector_visual_payload_instances_materialized=5/5", exact)
        self.assertIn("renderer_inputs_emitted=0/5", exact)
        self.assertIn("approvals_granted=0", exact)
        self.assertIn("c11c_geometric_waves_v1", exact)

    def test_full_audit_reports_required_operator_decisions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="c11e_policy_readiness_test_") as temp:
            report = audit.run_policy_readiness_audit(self.root, self.gui, self.cli, Path(temp) / "audit")
            self.assertEqual(report["status"], "PASS_AUDIT_ONLY_POLICY_APPROVAL_REQUIRED")
            self.assertEqual(report["stale_packet_v1_hash_count"], 3)
            self.assertFalse(report["next_gate"]["consumer_implementation_authorized"])
            self.assertFalse(report["next_gate"]["renderer_input_authorized"])
            saved = json.loads((Path(temp) / "audit/C11E_E4B_LOOP_POLICY_READINESS_REPORT_V1.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["report_sha256"], report["report_sha256"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
