import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[3] / "tools" / "c11d" / "d9" / "c11e_e6_d9_dependency_pin_reconciliation_v1.py"
spec = importlib.util.spec_from_file_location("reconcile", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ReconciliationV2Tests(unittest.TestCase):
    def test_safe_relative_path(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.assertEqual(mod.safe_project_file(root, "tools/a.py"), root / "tools" / "a.py")

    def test_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, "UNSAFE_RELATIVE_PATH"):
                mod.safe_project_file(Path(td), "../outside")

    def test_rejects_absolute_path(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, "UNSAFE_RELATIVE_PATH"):
                mod.safe_project_file(Path(td), "/outside")

    def test_rejects_windows_drive_path(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, "UNSAFE_RELATIVE_PATH"):
                mod.safe_project_file(Path(td), "C:/outside")

    def test_rejects_symlink_resolved_escape_without_os_symlink_privilege(self):
        """Simulate Path.resolve() following an existing symlink/junction outside root.

        This exercises the same containment decision without creating an OS link,
        which requires SeCreateSymbolicLinkPrivilege on some Windows installations.
        """
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside:
            root = Path(td)
            candidate = root / "escape" / "file.json"
            outside_file = Path(outside) / "file.json"
            path_type = type(candidate)
            original_resolve = path_type.resolve

            def resolve_with_external_target(path, strict=False):
                if path == candidate:
                    return outside_file
                return original_resolve(path, strict=strict)

            with patch.object(path_type, "resolve", new=resolve_with_external_target):
                with self.assertRaisesRegex(ValueError, "PATH_ESCAPES_PROJECT_ROOT"):
                    mod.safe_project_file(root, "escape/file.json")

    def test_requires_exactly_33_pins(self):
        with self.assertRaisesRegex(ValueError, "EXPECTED_EXACTLY_33_SOURCE_PINS"):
            mod.validate_pin_rows([])

    def test_rejects_duplicate_pin(self):
        row = {"path": "a", "sha256": "a" * 64}
        with self.assertRaisesRegex(ValueError, "DUPLICATE_SOURCE_PIN"):
            mod.validate_pin_rows([row, row] + [{"path": f"p{i}", "sha256": "b" * 64} for i in range(31)])

    def test_rejects_invalid_sha(self):
        with self.assertRaisesRegex(ValueError, "INVALID_SOURCE_PIN_ROW"):
            mod.validate_pin_rows([{"path": f"p{i}", "sha256": "bad"} for i in range(33)])

    def test_all_nine_route_dependencies_reconcile(self):
        rows = [{"path": f"p{i}", "observed_sha256": f"{i:064x}"} for i in range(9)]
        route = {"findings": [{"id": "ADDITIONAL_RUNTIME_ROUTE_DEPENDENCY_FINGERPRINTS", "rows": rows}]}
        pins = {x["path"]: x["observed_sha256"] for x in rows}
        result = mod.reconcile_route_dependencies(route, pins)
        self.assertEqual(result["matched"], 9)
        self.assertEqual(result["status"], "PASS_9_OF_9_ALREADY_ACCEPTED")

    def test_route_dependency_mismatch_blocks(self):
        rows = [{"path": f"p{i}", "observed_sha256": f"{i:064x}"} for i in range(9)]
        route = {"findings": [{"id": "ADDITIONAL_RUNTIME_ROUTE_DEPENDENCY_FINGERPRINTS", "rows": rows}]}
        pins = {x["path"]: x["observed_sha256"] for x in rows}
        pins["p8"] = "f" * 64
        result = mod.reconcile_route_dependencies(route, pins)
        self.assertEqual(result["matched"], 8)
        self.assertEqual(result["status"], "BLOCKED_ROUTE_DEPENDENCY_PIN_GAP")

    def test_ch004_historical_divergence_is_not_waived(self):
        item = mod.CH004_HISTORICAL_DIVERGENCES["tools/c11d/d9/universal_editorial_model.py"]
        self.assertIn("NO_AUTO_WAIVER", item["disposition"])

    def test_service_drift_is_not_auto_reuse_acceptance(self):
        item = mod.CH004_HISTORICAL_DIVERGENCES["c11c-suite/c11c-producer/c11e_production_service.py"]
        self.assertIn("REUSE_NOT_AUTO_ACCEPTED", item["disposition"])

    def test_d4_8_is_never_overridden_by_reconciliation(self):
        self.assertEqual(mod.EXPECTED["d4_8_policy"][1], "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")


if __name__ == "__main__":
    unittest.main(verbosity=2)
