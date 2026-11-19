from __future__ import annotations
import hashlib, importlib.util, sys, tempfile, types, unittest
from pathlib import Path

RUNNER_PATH = Path(__file__).resolve().parents[1] / "RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_4.py"
SPEC = importlib.util.spec_from_file_location("_c11e_v24_runner_for_test", str(RUNNER_PATH))
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("RUNNER_TEST_SPEC_UNAVAILABLE")
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)

class PinnedFileLoaderTests(unittest.TestCase):
    def setUp(self):
        self.module_path = RUNNER_PATH.parent / "support/a3_lineage_adjudicator_v4.py"
        self.expected = hashlib.sha256(self.module_path.read_bytes()).hexdigest()

    def test_01_load_exact_pinned_file(self):
        module = RUNNER.load_pinned_adjudicator(self.module_path, self.expected)
        self.assertTrue(callable(module.adjudicate_loop_a3))

    def test_02_ignore_preloaded_unrelated_support_namespace(self):
        prior = sys.modules.get("support")
        fake = types.ModuleType("support")
        fake.__path__ = []
        sys.modules["support"] = fake
        try:
            module = RUNNER.load_pinned_adjudicator(self.module_path, self.expected)
            self.assertTrue(callable(module.adjudicate_loop_a3))
        finally:
            if prior is None:
                sys.modules.pop("support", None)
            else:
                sys.modules["support"] = prior

    def test_03_reject_hash_mismatch_before_exec(self):
        with self.assertRaisesRegex(ValueError, "A3_ADJUDICATOR_SHA256_MISMATCH"):
            RUNNER.load_pinned_adjudicator(self.module_path, "0" * 64)

    def test_04_reject_missing_file(self):
        missing = self.module_path.parent / "not_present.py"
        with self.assertRaisesRegex(FileNotFoundError, "A3_ADJUDICATOR_FILE_MISSING"):
            RUNNER.load_pinned_adjudicator(missing, self.expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)
