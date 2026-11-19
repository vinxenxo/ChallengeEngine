from __future__ import annotations
import importlib.util, sys, tempfile, types, unittest
from pathlib import Path

HELPER_PATH = Path(__file__).resolve().parents[1] / "support" / "qimage_import_bootstrap_v1.py"
SPEC = importlib.util.spec_from_file_location("_qimage_import_bootstrap_test_module", HELPER_PATH)
if SPEC is None or SPEC.loader is None: raise RuntimeError("QIMAGE_BOOTSTRAP_TEST_SPEC_UNAVAILABLE")
HELPER = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(HELPER)

class QImagePayloadImportBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="c11e_qimage_payload_")
        self.package = Path(self.temp.name) / "native_probe_v2"
        self.payload = self.package / "payload"
        self.module = self.payload / HELPER.QIMAGE_MODULE_REL
        self.module.parent.mkdir(parents=True, exist_ok=True)
        self.module.write_text("MARKER = 'EXPECTED_PAYLOAD_MODULE'\n", encoding="utf-8")
        self.old_path = list(sys.path)
        self.old_tools_modules = {name: module for name, module in list(sys.modules.items()) if name == "tools" or name.startswith("tools.")}
        for name in list(sys.modules):
            if name == "tools" or name.startswith("tools."):
                sys.modules.pop(name, None)
    def tearDown(self):
        sys.path[:] = self.old_path
        for name in list(sys.modules):
            if name == "tools" or name.startswith("tools."):
                sys.modules.pop(name, None)
        sys.modules.update(self.old_tools_modules)
        self.temp.cleanup()
    def test_01_payload_root_is_first_path_and_returns_exact_module(self):
        resolved = HELPER.ensure_payload_tools_root(self.package)
        self.assertEqual(resolved, self.module.resolve())
        self.assertEqual(Path(sys.path[0]).resolve(), self.payload.resolve())
    def test_02_duplicate_payload_root_is_collapsed(self):
        sys.path.extend([str(self.payload), str(self.payload)])
        HELPER.ensure_payload_tools_root(self.package)
        roots = [Path(p).resolve() for p in sys.path if p and Path(p).exists()]
        self.assertEqual(sum(p == self.payload.resolve() for p in roots), 1)
    def test_03_missing_qimage_module_fails_before_sys_path_change(self):
        before = list(sys.path)
        self.module.unlink()
        with self.assertRaisesRegex(FileNotFoundError, "QIMAGE_PAYLOAD_MODULE_MISSING"):
            HELPER.ensure_payload_tools_root(self.package)
        self.assertEqual(sys.path, before)
    def test_04_unrelated_preloaded_tools_package_is_rejected(self):
        fake = types.ModuleType("tools"); fake.__path__ = [str(Path(self.temp.name) / "foreign_tools")]
        sys.modules["tools"] = fake
        with self.assertRaisesRegex(ImportError, "QIMAGE_TOOLS_NAMESPACE_PRELOADED_OUTSIDE_PAYLOAD"):
            HELPER.ensure_payload_tools_root(self.package)
    def test_05_import_tools_module_resolves_to_payload_copy(self):
        expected = HELPER.ensure_payload_tools_root(self.package)
        import tools.c11d.d9.c11e_e6_option_c_qimage_frame_compositor_v1 as actual
        self.assertEqual(Path(actual.__file__).resolve(), expected)
        self.assertEqual(actual.MARKER, "EXPECTED_PAYLOAD_MODULE")
    def test_06_module_origin_mismatch_is_rejected(self):
        wrong = types.ModuleType("wrong"); wrong.__file__ = str(Path(self.temp.name) / "wrong.py")
        with self.assertRaisesRegex(ImportError, "QIMAGE_MODULE_ORIGIN_MISMATCH"):
            HELPER.validate_qimage_module_origin(wrong, self.module)

    def test_07_preloaded_nonpackage_tools_namespace_is_rejected(self):
        fake = types.ModuleType("tools")
        sys.modules["tools"] = fake
        with self.assertRaisesRegex(ImportError, "QIMAGE_TOOLS_NAMESPACE_PRELOADED_AS_NON_PACKAGE"):
            HELPER.ensure_payload_tools_root(self.package)
    def test_08_matching_preloaded_tools_namespace_is_accepted(self):
        fake = types.ModuleType("tools")
        fake.__path__ = [str(self.payload / "tools")]
        sys.modules["tools"] = fake
        resolved = HELPER.ensure_payload_tools_root(self.package)
        self.assertEqual(resolved, self.module.resolve())
        self.assertEqual(Path(sys.path[0]).resolve(), self.payload.resolve())

if __name__ == "__main__": unittest.main(verbosity=2)
