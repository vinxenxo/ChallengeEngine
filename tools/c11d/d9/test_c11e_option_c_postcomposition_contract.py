#!/usr/bin/env python3
"""Static and negative tests for C11-E Option C handoff (no media/dispatch)."""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from typing import Any

MODULE_PATH = Path(__file__).with_name("c11e_option_c_postcomposition_contract.py")
SPEC = importlib.util.spec_from_file_location("c11e_option_c_postcomposition_contract", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot load Option C contract module")
CONTRACT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CONTRACT
SPEC.loader.exec_module(CONTRACT)


class OptionCStaticContractTests(unittest.TestCase):
    project_root: Path
    recovered_zip: Path
    report: dict[str, Any]

    @classmethod
    def configure(cls, project_root: Path, recovered_zip: Path) -> None:
        cls.project_root = project_root.resolve()
        cls.recovered_zip = recovered_zip.resolve()
        cls.report = CONTRACT.build_report(cls.project_root, cls.recovered_zip)

    def test_operator_approved_option_c_but_execution_not_authorized(self) -> None:
        decision, boundary, policy = CONTRACT.validate_option_c_boundary(self.project_root)
        self.assertEqual(decision["decision_state"], "OPERATOR_APPROVED_OPTION_C")
        self.assertEqual(decision["operator_decision"]["selected_option"], "C")
        self.assertTrue(decision["approval_boundary"]["architecture_choice_approved"])
        self.assertFalse(decision["approval_boundary"]["r1v_physical_execution_authorized"])
        self.assertEqual(boundary["status"], "PREPARE_ONLY_NOT_DISPATCHABLE")
        self.assertEqual(policy["status"], "PROPOSED_NOT_APPROVED")
        self.assertFalse(policy["execution_authorized"])

    def test_all_27_receipts_resolve_to_unique_handoffs(self) -> None:
        self.assertEqual(self.report["status"], "PASS_OPTION_C_HANDOFF_CONTRACT_27_OF_27_PREPARE_ONLY")
        self.assertEqual(self.report["r1p"]["receipt_count"], 27)
        self.assertEqual(self.report["option_c_handoff"]["handoff_count"], 27)
        identities = {
            (item["content_identity"]["family_id"], item["content_identity"]["grammar_id"])
            for item in self.report["handoffs"]
        }
        self.assertEqual(len(identities), 27)
        self.assertEqual(self.report["r1p"]["family_counts"], CONTRACT.EXPECTED_FAMILY_COUNTS)

    def test_live_pin_validations_are_exactly_30_plus_3(self) -> None:
        pins = self.report["r1p"]
        self.assertEqual(pins["r1p_source_pin_count"], 30)
        self.assertEqual(pins["r1p_process_log_validation_count"], 4)
        self.assertEqual(pins["option_c_policy_pin_validation_count"], 3)
        self.assertEqual(pins["total_live_pin_validations"], 33)

    def test_handoffs_do_not_claim_actual_source_or_output_media(self) -> None:
        self.assertEqual(self.report["option_c_handoff"]["source_media_sha256_claims"], 0)
        self.assertEqual(self.report["option_c_handoff"]["measured_frame_inventories"], 0)
        self.assertEqual(self.report["option_c_handoff"]["d_output_artifacts"], 0)
        for handoff in self.report["handoffs"]:
            self.assertEqual(handoff["status"], "PREPARED_WAITING_FOR_R1V_ACTUAL_SOURCE_EVIDENCE")
            CONTRACT.validate_no_dispatch(handoff)

    def test_each_handoff_keeps_seed_domains_separate(self) -> None:
        for handoff in self.report["handoffs"]:
            seed = handoff["visual_seed_domain"]
            self.assertEqual(seed["source"], "request.seed")
            self.assertFalse(seed["music_seed_consumed_by_visual_composition"])
            self.assertNotEqual(seed["gameplay_seed"], seed["music_seed_lineage_only_for_future_d3"])

    def test_r1v_scope_is_five_pilots_and_ten_proposed_calls(self) -> None:
        r1v = self.report["r1v_qualification_request"]
        self.assertEqual(r1v["pilot_count"], 5)
        self.assertEqual(r1v["proposed_launcher_invocations"], 10)
        self.assertFalse(r1v["execution_authorized"])
        self.assertEqual({x["family_id"] for x in r1v["pilots"]}, set(CONTRACT.EXPECTED_FAMILY_COUNTS))

    def test_tampered_handoff_cannot_enable_dispatch(self) -> None:
        import copy
        mutated = copy.deepcopy(self.report["handoffs"][0])
        mutated["execution_boundary"]["compositor_invoked"] = True
        with self.assertRaises(CONTRACT.OptionCContractError):
            CONTRACT.validate_no_dispatch(mutated)

    def test_d_output_must_be_distinct_from_c_source(self) -> None:
        with self.assertRaises(CONTRACT.OptionCContractError):
            CONTRACT.validate_source_output_separation("artifacts/c_source.mp4", "artifacts/c_source.mp4")
        CONTRACT.validate_source_output_separation("artifacts/c_source.mp4", "artifacts/d_output.mp4")

    def test_contract_module_has_no_process_or_media_dispatch_surface(self) -> None:
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        forbidden_imports = {"subprocess", "ffmpeg", "ffmpegio", "cv2", "PIL", "godot"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse(any(alias.name.split(".")[0] in forbidden_imports for alias in node.names))
            elif isinstance(node, ast.ImportFrom):
                self.assertNotIn((node.module or "").split(".")[0], forbidden_imports)
            elif isinstance(node, ast.Call):
                func = node.func
                name = func.id if isinstance(func, ast.Name) else (func.attr if isinstance(func, ast.Attribute) else "")
                self.assertNotIn(name, {"Popen", "run", "call", "check_call", "check_output", "system", "startfile"})


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Option C static and negative contract tests")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--r1p-zip", required=True, type=Path)
    args, remaining = parser.parse_known_args()
    if sys.version_info[:2] != (3, 13):
        print(f"EXPECTED_PYTHON=3.13 ACTUAL={sys.version_info.major}.{sys.version_info.minor}", file=sys.stderr)
        return 2
    OptionCStaticContractTests.configure(args.project_root, args.r1p_zip)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(OptionCStaticContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"OPTION_C_UNIT_TESTS={result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
