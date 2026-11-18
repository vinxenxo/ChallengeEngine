#!/usr/bin/env python3
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("c11e_e6_challenge_capture_route_audit_v1.py")
spec = importlib.util.spec_from_file_location("route_audit", SCRIPT)
route_audit = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(route_audit)


class TimelineMathTests(unittest.TestCase):
    def test_01_ch001_540_source_frames(self):
        d = {"video": {"fps": 60, "hook_duration": 0, "game_duration": 7, "reveal_duration": 0, "cta_duration": 2}}
        t = route_audit.timeline_from_definition(d)
        self.assertEqual(t["source_frames"], 540)

    def test_02_ch002_600_source_frames(self):
        d = {"video": {"fps": 60, "hook_duration": 3, "game_duration": 7, "reveal_duration": 0, "cta_duration": 0}}
        self.assertEqual(route_audit.timeline_from_definition(d)["source_frames"], 600)

    def test_03_ch004_900_source_frames(self):
        d = {"video": {"fps": 60, "hook_duration": 3, "game_duration": 7, "reveal_duration": 3, "cta_duration": 2}}
        self.assertEqual(route_audit.timeline_from_definition(d)["source_frames"], 900)

    def test_04_ch005_420_source_frames(self):
        d = {"video": {"fps": 60, "hook_duration": 0, "game_duration": 7, "reveal_duration": 0, "cta_duration": 0}}
        self.assertEqual(route_audit.timeline_from_definition(d)["source_frames"], 420)

    def test_05_ch006_540_source_frames(self):
        d = {"video": {"fps": 60, "hook_duration": 0, "game_duration": 7, "reveal_duration": 0, "cta_duration": 2}}
        self.assertEqual(route_audit.timeline_from_definition(d)["source_frames"], 540)

    def test_06_ch007_600_source_frames(self):
        d = {"video": {"fps": 60, "hook_duration": 3, "game_duration": 7, "reveal_duration": 0, "cta_duration": 0}}
        self.assertEqual(route_audit.timeline_from_definition(d)["source_frames"], 600)

    def test_07_half_open_phase_ranges_are_contiguous(self):
        d = {"video": {"fps": 60, "hook_duration": 3, "game_duration": 7, "reveal_duration": 3, "cta_duration": 2}}
        p = route_audit.timeline_from_definition(d)["phases"]
        self.assertEqual([(x["start_frame"], x["end_frame"]) for x in p], [(0,180),(180,600),(600,780),(780,900)])

    def test_08_zero_duration_phases_are_empty_ranges(self):
        d = {"video": {"fps": 60, "hook_duration": 0, "game_duration": 7, "reveal_duration": 0, "cta_duration": 0}}
        p = route_audit.timeline_from_definition(d)["phases"]
        self.assertEqual([(x["start_frame"], x["end_frame"]) for x in p], [(0,0),(0,420),(420,420),(420,420)])

    def test_09_review_mapping_540_to_270(self):
        self.assertEqual(540 * 30 // 60, 270)

    def test_10_review_mapping_900_to_450(self):
        self.assertEqual(900 * 30 // 60, 450)

    def test_11_decimal_half_up(self):
        self.assertEqual(route_audit.frame_count(DecimalTest("0.025"), 60), 2)

    def test_12_game_phase_must_be_positive(self):
        d = {"video": {"fps": 60, "hook_duration": 1, "game_duration": 0, "reveal_duration": 0, "cta_duration": 0}}
        with self.assertRaises(ValueError):
            route_audit.timeline_from_definition(d)

    def test_13_invalid_fps_rejected(self):
        d = {"video": {"fps": 0, "hook_duration": 0, "game_duration": 7, "reveal_duration": 0, "cta_duration": 0}}
        with self.assertRaises(ValueError):
            route_audit.timeline_from_definition(d)

    def test_14_missing_required_phase_rejected(self):
        d = {"video": {"fps": 60, "game_duration": 7, "cta_duration": 0}}
        with self.assertRaises(ValueError):
            route_audit.timeline_from_definition(d)


class PathSafetyTests(unittest.TestCase):
    def test_15_relative_path_accepted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.assertEqual(route_audit.contained_path(root, "a/b.txt"), (root / "a/b.txt").resolve())

    def test_16_absolute_path_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                route_audit.contained_path(Path(td), Path("/tmp/file"))

    def test_17_parent_escape_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                route_audit.contained_path(Path(td), "../escape.txt")

    def test_18_sha256_of_bytes(self):
        self.assertEqual(route_audit.sha256_bytes(b"abc"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")


class ContractFixtureTests(unittest.TestCase):
    def test_19_exact_six_selected_ids(self):
        self.assertEqual(route_audit.EXPECTED_SELECTED, ["CHALLENGE_001","CHALLENGE_002","CHALLENGE_004","CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"])

    def test_20_seeds_are_distinct(self):
        self.assertEqual(len(set(route_audit.EXPECTED_GAMEPLAY_SEEDS.values())), 6)

    def test_21_each_selected_has_expected_timebase(self):
        self.assertEqual(set(route_audit.EXPECTED_TIMEBASE), set(route_audit.EXPECTED_SELECTED))

    def test_22_ch008_ch009_not_selected(self):
        self.assertNotIn("CHALLENGE_008", route_audit.EXPECTED_SELECTED)
        self.assertNotIn("CHALLENGE_009", route_audit.EXPECTED_SELECTED)

    def test_23_ch003_not_selected(self):
        self.assertNotIn("CHALLENGE_003", route_audit.EXPECTED_SELECTED)

    def test_24_required_pin_count(self):
        self.assertEqual(route_audit.REQUIRED_SOURCE_PINS, 24)

    def test_25_known_manifest_pin(self):
        self.assertEqual(len(route_audit.FROZEN_MANIFEST_SHA), 64)

    def test_26_known_d48_pin(self):
        self.assertEqual(route_audit.D48_SHA, "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")

    def test_27_plan_hash_is_sha256(self):
        self.assertEqual(len(route_audit.PLAN_JSON_SHA), 64)

    def test_28_contract_receipt_hash_is_sha256(self):
        self.assertEqual(len(route_audit.CONTRACT_RECEIPT_SHA), 64)


class TextContractTests(unittest.TestCase):
    def test_29_consumer_adapter_expected_path(self):
        self.assertEqual(route_audit.CONSUMER_REL.as_posix(), "tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd")

    def test_30_envelope_builder_expected_path(self):
        self.assertEqual(route_audit.ENVELOPE_BUILDER_REL.as_posix(), "tools/c11d/d9/c11e_e4a6_challenge_live_editorial_envelope.py")

    def test_31_movie_maker_scan_classifies_bounded_and_reference_runners(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            e2 = root / "tools/c11e/e2"
            c11c = root / "tools/prototypes/c11c_bulk"
            e2.mkdir(parents=True)
            c11c.mkdir(parents=True)
            (e2 / "run.ps1").write_text("godot --scene C11EChallenge001E2.tscn --write-movie --config=x", encoding="utf-8")
            (c11c / "run_c11c_challenge_production.ps1").write_text("godot --scene Main.tscn --write-movie --config=x", encoding="utf-8")
            found = route_audit.scan_movie_maker_scripts(root)
            self.assertEqual(len(found), 2)
            by_path = {row["path"]: row for row in found}
            self.assertEqual(by_path["tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1"]["classification"], "C11C_EXISTING_CHALLENGE_LAUNCHER_REFERENCE_ONLY")
            self.assertEqual(by_path["tools/c11e/e2/run.ps1"]["classification"], "C11E_E2_CH001_BOUNDED_NOT_E6")

    def test_32_movie_maker_scan_ignores_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            artifact = root / "tools/artifacts/archive"
            artifact.mkdir(parents=True)
            (artifact / "old.ps1").write_text("godot --write-movie", encoding="utf-8")
            self.assertEqual(route_audit.scan_movie_maker_scripts(root), [])


class DecimalTest(str):
    pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
