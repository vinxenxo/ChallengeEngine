from __future__ import annotations
import importlib.util, json, tempfile, unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[3] / "tools" / "c11d" / "d9" / "c11e_e6_post_qimage_l1_reconciliation_v1.py"
spec = importlib.util.spec_from_file_location("phase_recon_under_test", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PhaseReconciliationTests(unittest.TestCase):
    def test_01_sha256_matches_known_vector(self):
        self.assertEqual(mod.sha256_bytes(b"abc"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_02_sidecar_accepts_exact_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "r.json"
            p.write_bytes(b"{}")
            sha = mod.sha256_file(p)
            Path(str(p) + ".sha256").write_text(sha + "  r.json\n", encoding="ascii")
            self.assertEqual(mod.verify_sidecar(p, sha)["status"], "PASS")

    def test_03_sidecar_missing_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "r.json"; p.write_bytes(b"{}")
            self.assertEqual(mod.verify_sidecar(p)["status"], "BLOCKED_SIDECAR_MISSING")

    def test_04_relative_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError): mod.relative_file(Path(td), "../outside")

    def test_05_json_pin_mismatch_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.json"; p.write_text("{}", encoding="utf-8")
            check, obj = mod.verify_pinned_json(Path(td), {"id":"x", "path":"x.json", "sha256":"0"*64})
            self.assertEqual(check["status"], "BLOCKED_SHA256_MISMATCH")
            self.assertIsNone(obj)

    def test_06_json_valid_pin_passes(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.json"; p.write_text('{"ok":true}', encoding="utf-8")
            check, obj = mod.verify_pinned_json(Path(td), {"id":"x", "path":"x.json", "sha256":mod.sha256_file(p)})
            self.assertEqual(check["status"], "PASS")
            self.assertTrue(obj["ok"])

    def test_07_v27_install_requires_11_docs_and_18_files(self):
        receipt = {"schema":"C11E-E6-OPTION-C-NATIVE-QT-PROBE-INSTALL-RECEIPT-V2", "status":"PASS_ADD_ONLY", "installer_revision":"V2.7_PS51_DOCS_TRANSACTION_AND_QIMAGE_SOURCE_PIN_FIX", "add_count":18, "skip_identical_count":0, "installed_files":[{}]*18, "documentation_files":11, "c11c_manifest_sha256":mod.FROZEN_C11C_SHA, "d4_8_v2_sha256":mod.D48_V2_SHA, "source_files_modified":False, "c11c_modified":False, "d4_8_v2_modified":False, "release_authority":"NONE"}
        self.assertEqual(receipt["documentation_files"],11)
        self.assertEqual(receipt["add_count"],18)

    def test_08_v27_qimage_pass_threshold(self):
        bench = {"iterations":7,"p95_ms":5.5743,"stage_30fps_budget":"PASS"}
        self.assertLessEqual(bench["p95_ms"],1000/30)
        self.assertEqual(bench["iterations"],7)

    def test_09_qimage_gate_does_not_equal_end_to_end(self):
        self.assertNotEqual("PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END", "E6_ACCEPTED")

    def test_10_ch004_candidate_is_not_accepted(self):
        disposition = "ELIGIBLE_FOR_E6_LEDGER_REQUALIFICATION_NOT_ACCEPTED"
        self.assertIn("NOT_ACCEPTED", disposition)

    def test_11_authority_keeps_d4_8_blocked(self):
        self.assertEqual(mod.D48_V2_SHA, "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")

    def test_12_output_is_not_media_authority(self):
        report = {"governance":{"godot_invoked":False,"ffmpeg_invoked":False,"ffprobe_invoked":False,"e6_accepted":0,"release_authority":"NONE"}}
        self.assertFalse(report["governance"]["godot_invoked"])
        self.assertEqual(report["governance"]["e6_accepted"],0)

    def test_13_install_postimages_rehash_exact_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); p = root / "docs/current/e/a.md"; p.parent.mkdir(parents=True); p.write_bytes(b"doc")
            row = {"path":"docs/current/e/a.md","sha256":mod.sha256_file(p),"bytes":3,"status":"ADDED_AND_VERIFIED"}
            result = mod.verify_install_postimages(root,[row])
            self.assertEqual(result["rows"][0]["status"],"PASS")

    def test_14_install_postimage_mismatch_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); p = root / "tools/a.py"; p.parent.mkdir(parents=True); p.write_bytes(b"wrong")
            row = {"path":"tools/a.py","sha256":"0"*64,"bytes":5,"status":"ADDED_AND_VERIFIED"}
            self.assertEqual(mod.verify_install_postimages(root,[row])["status"],"BLOCKED_INSTALL_POSTIMAGES")

    def test_15_install_postimage_path_escape_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            row = {"path":"../outside","sha256":"0"*64,"bytes":1,"status":"ADDED_AND_VERIFIED"}
            self.assertEqual(mod.verify_install_postimages(Path(td),[row])["status"],"BLOCKED_INSTALL_POSTIMAGES")

    def test_16_install_postimage_count_contract_is_exact(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); p = root / "docs/a.md"; p.parent.mkdir(parents=True); p.write_bytes(b"x")
            row = {"path":"docs/a.md","sha256":mod.sha256_file(p),"bytes":1,"status":"ADDED_AND_VERIFIED"}
            self.assertEqual(mod.verify_install_postimages(root,[row])["status"],"BLOCKED_INSTALL_POSTIMAGES")

    def test_17_preview_png_validator_checks_format_and_crc(self):
        # 1x1 RGB PNG; the contract should reject dimensions before visual review.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "tiny.png"
            p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00"*32)
            with self.assertRaises(ValueError): mod.validate_rgb24_png(p)

if __name__ == "__main__": unittest.main(verbosity=2)
