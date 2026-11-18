from __future__ import annotations

import ast
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[3] / "tools" / "c11d" / "d9" / "c11e_e6_ch004_historical_source_pin_adjudication_v1.py"
spec = __import__("importlib.util", fromlist=["spec_from_file_location"]).spec_from_file_location("ch004_adjudication", MODULE_PATH)
module = __import__("importlib.util", fromlist=["module_from_spec"]).module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class Ch004HistoricalAdjudicationTests(unittest.TestCase):
    def test_historical_pins_match_e4b_manifest_preimages(self):
        expected = {
            "tools/c11d/d9/universal_editorial_model.py": ("5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5", "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd"),
            "c11c-suite/c11c-producer/c11e_production_service.py": ("348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951", "08ab5a278de8ebb55795a57391c83a27207ce01920704c419b8e28be25ddcf65"),
        }
        for path, pair in expected.items():
            self.assertEqual(module.HISTORICAL_SOURCES[path]["sha256"], pair[0])
            self.assertEqual(module.HISTORICAL_SOURCES[path]["e4b_postimage_sha256"], pair[1])

    def test_e4a7_receipt_identity_is_immutable_and_pinned(self):
        self.assertEqual(module.E4A7_RECEIPT_SHA256, "102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0")
        self.assertEqual(module.E4A7_RECEIPT_REL.name, "C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json")

    def test_reconciliation_report_is_exactly_pinned(self):
        self.assertEqual(module.RECON_SHA256, "0e2c977f1122d9cfc69da255d8fa539720a23f00cdc2f4c030d48bd01019a59a")

    def test_reconciliation_counts_are_exact(self):
        counts = {"accepted_source_pins": "33/33", "additional_route_dependencies": "9/9", "ch004_observed_current_hashes": "2/2", "fixed_evidence_pins": "13/13"}
        self.assertEqual(len(counts), 4)
        self.assertEqual(counts["accepted_source_pins"], "33/33")
        self.assertEqual(counts["additional_route_dependencies"], "9/9")

    def test_reconciliation_failure_categories_are_nested_under_hydration(self):
        report = {"hydration_v2_reconciliation": {"check_count": 1803, "passed_checks": 1801, "failed_checks": 2, "failure_categories": {"historical_source_pin_divergence": 2, "other_failures": 0}}}
        hydration = report.get("hydration_v2_reconciliation", {})
        self.assertEqual(hydration.get("failure_categories"), {"historical_source_pin_divergence": 2, "other_failures": 0})
        self.assertEqual((hydration.get("check_count"), hydration.get("passed_checks"), hydration.get("failed_checks")), (1803, 1801, 2))

    def test_service_and_editorial_remain_distinct_lineage_entries(self):
        self.assertEqual(len(module.HISTORICAL_SOURCES), 2)
        self.assertNotEqual(
            module.HISTORICAL_SOURCES["tools/c11d/d9/universal_editorial_model.py"]["sha256"],
            module.HISTORICAL_SOURCES["c11c-suite/c11c-producer/c11e_production_service.py"]["sha256"],
        )

    def test_exact_preimage_bytes_pass(self):
        data = b"exact historic bytes"
        digest = hashlib.sha256(data).hexdigest()
        result = module.verify_preimage_bytes(data, digest, len(data))
        self.assertEqual(result["status"], "PASS")

    def test_wrong_preimage_hash_blocks(self):
        data = b"historic source"
        result = module.verify_preimage_bytes(data, "0" * 64, len(data))
        self.assertEqual(result["status"], "MISMATCH")

    def test_wrong_preimage_size_blocks(self):
        data = b"historic source"
        result = module.verify_preimage_bytes(data, hashlib.sha256(data).hexdigest(), len(data) + 1)
        self.assertEqual(result["status"], "MISMATCH")

    def test_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(module.AdjudicationError):
                module.safe_project_path(Path(temp), "../outside.txt")

    def test_rejects_absolute_path(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(module.AdjudicationError):
                module.safe_project_path(Path(temp), str(Path(temp).parent / "outside.txt"))

    def test_rejects_windows_drive_path(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(module.AdjudicationError):
                module.safe_project_path(Path(temp), r"C:\outside\evidence.json")

    def test_rejects_reparse_point_ancestor_without_creating_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "artifacts").mkdir()
            with mock.patch.object(module, "_is_reparse_point", side_effect=lambda p: p.name == "artifacts"):
                with self.assertRaises(module.AdjudicationError):
                    module.safe_project_path(root, "artifacts/evidence.json")

    def test_rejects_dangling_symlink_before_exists_check(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = Path.is_symlink
            def simulated_symlink(path):
                return path.name == "dangling" or original(path)
            with mock.patch.object(Path, "is_symlink", simulated_symlink):
                with self.assertRaises(module.AdjudicationError):
                    module.safe_project_path(root, "dangling/evidence.json")

    def test_diff_detects_modified_top_level_symbols(self):
        old = b"def alpha():\n    return 1\n"
        new = b"def alpha():\n    return 2\n\ndef beta():\n    return 3\n"
        result = module.summarize_diff(old, new)
        self.assertIn("alpha", result["top_level_symbol_delta"]["modified"])
        self.assertIn("beta", result["top_level_symbol_delta"]["added"])

    def test_no_media_execution_or_governance_override_in_module(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertNotIn("subprocess", imported)
        self.assertNotIn("git", imported)
        self.assertIn('"d4_8_overridden": False', source)
        self.assertIn('"media_created": False', source)

    def test_ch004_reuse_is_never_auto_accepted(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        self.assertIn('"automatic_reuse_acceptance": False', source)
        self.assertIn("REUSE_CANDIDATE_PENDING_SEMANTIC_DIFF_REVIEW_AND_E6_LEDGER_REQUALIFICATION", source)

    def test_d4_8_and_frozen_manifest_hashes_remain_locked(self):
        self.assertEqual(module.FROZEN_MANIFEST_SHA256, "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")
        self.assertEqual(module.D4_8_SHA256, "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")


if __name__ == "__main__":
    unittest.main(verbosity=2)
