from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

import c11e_e5_cross_family_prepare_canary_v1 as runner


CONTRACT_PATH = Path(__file__).resolve().parents[3] / "definitions" / "c11d" / "production" / "C11E_E5_CROSS_FAMILY_CANARY_CONTRACT_V1.json"
EXPECTED_FAMILIES = ("challenge", "loop", "drill")
EXPECTED_PROBES = "ABCD"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


class E5CrossFamilyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load_contract()

    def test_01_contract_schema_and_phase_are_exact(self):
        self.assertEqual(self.contract["schema"], "C11E-E5-CROSS-FAMILY-PREPARE-CANARY-CONTRACT-V1")
        self.assertEqual(self.contract["phase"], "E5")
        self.assertEqual(self.contract["qualification_stage"], "OPENING_CROSS_FAMILY_PREPARE_ONLY_CANARY")

    def test_02_three_family_cardinality_is_exact(self):
        self.assertEqual(set(self.contract["families"]), set(EXPECTED_FAMILIES))
        self.assertEqual(self.contract["expected_cardinality"]["families"], 3)
        self.assertEqual(self.contract["expected_cardinality"]["probes_per_family"], 4)
        self.assertEqual(self.contract["expected_cardinality"]["selector_probe_pairs"], 12)
        self.assertEqual(self.contract["expected_cardinality"]["origin_rows"], 24)

    def test_03_static_source_pin_set_is_complete_and_unique(self):
        pins = self.contract["source_pins"]
        paths = [row["path"] for row in pins]
        self.assertGreaterEqual(len(pins), 31)
        self.assertEqual(len(paths), len(set(paths)))
        self.assertTrue(all(len(row["sha256"]) == 64 and row["bytes"] > 0 for row in pins))

    def test_04_frozen_c11c_manifest_identity_is_immutable(self):
        frozen = self.contract["frozen_c11c_manifest"]
        self.assertEqual(frozen["path"], "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
        self.assertEqual(frozen["bytes"], 796318)
        self.assertEqual(frozen["sha256"], runner.FROZEN_SHA256)

    def test_05_style_guide_v36_is_pinned(self):
        guide = self.contract["powershell_style_guide"]
        self.assertEqual(guide["version"], "V36")
        self.assertEqual(guide["path"], "docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V36.md")
        self.assertEqual(len(guide["sha256"]), 64)

    def test_06_family_music_profiles_are_distinct(self):
        profiles = [self.contract["families"][key]["music"]["profile_id"] for key in EXPECTED_FAMILIES]
        self.assertEqual(len(set(profiles)), 3)

    def test_07_challenge_selector_seed_and_timebase_are_pinned(self):
        row = self.contract["families"]["challenge"]
        self.assertEqual(row["selection"], {"content_type": "challenges", "family_id": "parking_v2", "variant_id": "CHALLENGE_004"})
        self.assertEqual(row["seeds"], {"gameplay": 314159, "gameplay_changed": 314160, "music": 840001, "music_changed": 840002})
        self.assertEqual(row["timebase"]["accepted_delivery_frames"], 450)
        self.assertEqual(row["timebase"]["delivery_seconds"], 15.0)

    def test_08_loop_selector_seed_and_native_timebase_are_pinned(self):
        row = self.contract["families"]["loop"]
        self.assertEqual(row["selection"], {"content_type": "visual_loops", "family_id": "c11c_fractal_bloom_v1", "subtype_id": "radial_bloom"})
        self.assertEqual(row["seeds"]["gameplay"], 100006)
        self.assertEqual(row["seeds"]["music"], 500006)
        self.assertEqual(row["timebase"]["native_frames"], 660)
        self.assertEqual(row["timebase"]["native_seconds"], 22.0)

    def test_09_drill_selector_seed_and_phase_timebase_are_pinned(self):
        row = self.contract["families"]["drill"]
        self.assertEqual(row["selection"], {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-2"})
        self.assertEqual(row["seeds"]["gameplay"], 12345)
        self.assertEqual(row["seeds"]["music"], 840001)
        self.assertEqual(row["timebase"]["expected_total_frames"], 810)
        self.assertEqual(row["timebase"]["expected_total_seconds"], 27.0)

    def test_10_a_and_b_requests_replay_semantics(self):
        for family in EXPECTED_FAMILIES:
            a = runner.build_request(family, "A", "TESTTOKEN", self.contract)
            b = runner.build_request(family, "B", "TESTTOKEN", self.contract)
            self.assertNotEqual(a["request_id"], b["request_id"])
            a.pop("request_id")
            b.pop("request_id")
            self.assertEqual(a, b)

    def test_11_c_changes_only_music_seed(self):
        for family in EXPECTED_FAMILIES:
            a = runner.build_request(family, "A", "TESTTOKEN", self.contract)
            c = runner.build_request(family, "C", "TESTTOKEN", self.contract)
            delta = {key for key in set(a) | set(c) if a.get(key) != c.get(key)} - {"request_id", "music_seed"}
            self.assertEqual(delta, set())
            self.assertNotEqual(a["music_seed"], c["music_seed"])
            self.assertEqual(a["seed"], c["seed"])

    def test_12_d_changes_only_gameplay_seed(self):
        for family in EXPECTED_FAMILIES:
            a = runner.build_request(family, "A", "TESTTOKEN", self.contract)
            d = runner.build_request(family, "D", "TESTTOKEN", self.contract)
            delta = {key for key in set(a) | set(d) if a.get(key) != d.get(key)} - {"request_id", "seed"}
            self.assertEqual(delta, set())
            self.assertEqual(a["music_seed"], d["music_seed"])
            self.assertNotEqual(a["seed"], d["seed"])

    def test_13_prepare_only_governance_is_hard_locked(self):
        boundary = self.contract["execution_boundary"]
        self.assertEqual(boundary["mode"], "PREPARE_ONLY")
        self.assertEqual(boundary["family_adapter"], "NOT_CONNECTED_E1")
        self.assertFalse(boundary["renderer"] != "OFF")
        self.assertFalse(boundary["production_dispatch"])
        self.assertFalse(boundary["production_media"])
        self.assertEqual(boundary["release_authority"], "NONE")
        self.assertFalse(boundary["godot"])
        self.assertFalse(boundary["ffmpeg"])
        self.assertFalse(boundary["d3_v5_invoked"])

    def test_14_identity_normalizer_strips_only_request_scoped_fields(self):
        sample = {
            "request_id": "A",
            "request_hash": "hash-A",
            "selector": "radial_bloom",
            "seed": 100006,
            "argument_vector": ["-Seed", "100006", "-OutputTag", "A"],
        }
        result = runner._strip_request_scoped_identity(sample)
        self.assertNotIn("request_id", result)
        self.assertNotIn("request_hash", result)
        self.assertEqual(result["selector"], "radial_bloom")
        self.assertEqual(result["seed"], 100006)
        self.assertEqual(result["argument_vector"], ["-Seed", "100006"])

    def test_15_path_guard_rejects_escape_and_accepts_contract_paths(self):
        project = Path(os.environ["C11E_E5_TEST_PROJECT_ROOT"]).resolve()
        self.assertTrue(runner.safe_project_path(project, "tools/c11d/d9/universal_producer.py").is_file())
        for invalid in ("../outside", "C:/outside", "tools\\bad.py", "/absolute"):
            with self.assertRaises(runner.E5CanaryError):
                runner.safe_project_path(project, invalid)

    def test_16_write_json_once_is_non_overwriting(self):
        with tempfile.TemporaryDirectory(prefix="c11e-e5-atomic-") as folder:
            target = Path(folder) / "receipt.json"
            digest = runner.write_json_once(target, {"status": "FIRST"})
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), digest)
            with self.assertRaises(FileExistsError):
                runner.write_json_once(target, {"status": "SECOND"})
            self.assertEqual(json.loads(target.read_text(encoding="utf-8"))["status"], "FIRST")

    def test_17_shared_service_gui_cli_static_boundary_is_present(self):
        project = Path(os.environ["C11E_E5_TEST_PROJECT_ROOT"]).resolve()
        result = runner.static_gui_wiring_check(project)
        self.assertEqual(result["status"], "PASS_GUI_STATIC_SERVICE_WIRING")
        self.assertFalse(result["actual_qt_ui_invoked"])

    def test_18_full_bulk_canary_emits_24_origin_rows_and_12_pairs(self):
        project = Path(os.environ["C11E_E5_TEST_PROJECT_ROOT"]).resolve()
        base = project / "artifacts" / "tests" / "c11e" / "e5_cross_family_prepare_canary" / "STAGED_INTEGRATION"
        base.mkdir(parents=True, exist_ok=False)
        receipt = base / "RUNNER_RESULT.json"
        result = runner.run_batch(
            project,
            project / "definitions" / "c11d" / "production" / "C11E_E5_CROSS_FAMILY_CANARY_CONTRACT_V1.json",
            receipt,
            fixed_batch_id="E5-XF-PREP-STAGED-INTEGRATION",
        )
        self.assertEqual(result["status"], "PASS_E5_PREPARE_ONLY_CROSS_FAMILY")
        batch_path = Path(result["batch_result_path"])
        batch = json.loads(batch_path.read_text(encoding="utf-8"))
        self.assertEqual(batch["completed_service_origin_rows"], 24)
        self.assertEqual(batch["completed_probe_pairs"], 12)
        self.assertEqual(batch["gui_cli_service_semantic_parity"], "PASS_12_OF_12")
        self.assertEqual(batch["profile_non_leakage"], "PASS_3_DISTINCT_PROFILE_BINDINGS")
        self.assertTrue(batch["source_pins_pre_post_equal"])
        self.assertEqual(batch["media_outputs"], 0)
        self.assertFalse(batch["renderer_invoked"])
        self.assertFalse(batch["godot_invoked"])
        self.assertFalse(batch["ffmpeg_invoked"])
        self.assertFalse(batch["production_dispatch"])
        self.assertEqual(batch["release_authority"], "NONE")
        row_receipts = list((batch_path.parent / "rows").glob("*/ROW_RECEIPT.json"))
        self.assertEqual(len(row_receipts), 12)
        for path in row_receipts:
            row = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(row["status"], "PASS_GUI_CLI_E1_PARITY")
            self.assertTrue(row["intent_semantics_match"])
            self.assertTrue(row["boundary_preparations_match"])
            self.assertFalse(row["media_created"])
        self.assertTrue(receipt.is_file())
        self.assertEqual(result["av_media_gate"], "BLOCKED_FAMILY_ADAPTER_NOT_CONNECTED_E1")
        self.assertEqual(result["e5_overall"], "OPEN_MEDIA_QUALIFICATION_REQUIRED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
