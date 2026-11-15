from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "c11d" / "d9" / "c11e_e4c_pursuit_tier_batch.py"
spec = importlib.util.spec_from_file_location("c11e_e4c_pursuit_tier_batch", MODULE_PATH)
assert spec and spec.loader
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)


class PursuitTierBatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = {
            "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1", "schema_version": "1.0",
            "request_id": "ACCEPTED-TIER-1", "mode": "PRODUCTION",
            "selection": {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"},
            "seed": 12345, "music_seed": 840001, "variation_index": 0,
            "audio_enabled": True, "personalization_enabled": True,
            "delivery_profile_id": "REVIEW_720", "presentation_profile_id": "social_default_v1",
            "production_override": {"title": "SEGUIMIENTO VISUAL · NIVEL 1",
                "subtitle": "Sigue la trayectoria del objetivo en movimiento",
                "call_to_action": "Mantén el objetivo a la vista", "language": "es"},
            "provenance": {"request_origin": "CLI", "source_revision": "C11D-D9.10-PRODUCER-0.11.1"},
        }

    def _project_root(self, root: Path) -> None:
        canonical = Path(__file__).resolve().parent / "fixtures" / "visual_drill_pursuit_canonical.json"
        target = root / batch.PURSUIT_CANONICAL_REL
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(canonical, target)

    def _source_inventory(self, root: Path) -> list[dict[str, object]]:
        inventory = []
        source_root = root / "source_pin_fixture"
        source_root.mkdir(parents=True, exist_ok=True)
        for index in range(91):
            body = f"pursuit-source-pin-{index:03d}".encode("ascii")
            rel = f"source_pin_fixture/{index:03d}.bin"
            path = root / rel
            path.write_bytes(body)
            inventory.append({"path": rel, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
        return inventory

    def _final_fixture(self, frames: int = 690, duration: float = 23.0):
        streams = [
            {"codec_type": "video", "codec_name": "h264", "profile": "High", "width": 720,
             "height": 1280, "pix_fmt": "yuv420p", "color_range": "tv", "avg_frame_rate": "30/1",
             "nb_read_frames": str(frames)},
            {"codec_type": "audio", "codec_name": "aac", "profile": "LC", "sample_rate": "48000",
             "channels": 2, "channel_layout": "stereo"},
        ]
        return {"duration_seconds": duration, "av_start_delta_seconds": 0.0,
                "ffprobe": {"streams": streams}}

    def _qualification_fixture(self, root: Path, tier: int = 1, request_id: str = "E4C-PRS-T1-b3abbe94"):
        self._project_root(root)
        pins = self._source_inventory(root)
        output_root = root / "artifacts" / "production" / "c11e" / request_id
        output_root.mkdir(parents=True, exist_ok=True)

        def put(name: str, body: bytes) -> tuple[str, str]:
            path = output_root / name
            path.write_bytes(body)
            return str(path), hashlib.sha256(body).hexdigest()

        wav_a, wav_a_sha = put("music_A.wav", b"wav-a")
        wav_b, wav_b_sha = put("music_B.wav", b"wav-a")
        wav_c, wav_c_sha = put("music_C.wav", b"wav-c")
        mp4_a, mp4_a_sha = put("final_A.mp4", b"video-a")
        mp4_c, mp4_c_sha = put("final_C.mp4", b"video-c")
        final = self._final_fixture()
        receipt = {
            "status": "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION", "request_id": request_id,
            "request_origin": "CLI", "family": "pursuit", "tier": tier, "gameplay_seed": 12345,
            "music_seed_a": 840001, "music_seed_b": 840001, "family_music_profile": "ORGANIC_BLOOM",
            "family_adapter_preparation_status": "NOT_CONNECTED_E1", "release_authority": "NONE",
            "production_dispatch": False, "production_release": False, "c11c_frozen_manifest_unchanged": True,
            "c11c_manifest_sha256": batch.FROZEN_MANIFEST_SHA256, "c11c_source_mutation": False,
            "renderer_invoked": True, "d_postcomposition": True, "ffmpeg_decode_encode_mux": True,
            "audio_generated": True, "source_pins_pre_post_equal": True, "source_pin_count": 91,
            "source_pins_pre_execution": pins, "source_pins_immediately_pre_renderer": pins,
            "source_pins_post_execution": pins,
            "family_adapter_execution": {"shared_entrypoint": "c11e_e4c_drill_execution.py"},
            "e1_gui_cli_parity": {"status": "PASS_E1_SHARED_GUI_CLI_INTENT_PARITY", "semantic_identity_equal": True},
            "e1_validation": {"status": "PASS_E1_PREPARATION_ONLY"},
            "native_timeline": {"fps": 30, "total_frames": 690, "gameplay_frames": 510,
                                "duration_seconds": 23.0, "pre_roll_frames": 90, "end_cta_frames": 90},
            "d_composition": {"frames_composed": 690, "frames_expected": 690,
                              "phase_counts": {"PRE_ROLL": 90, "GAME": 510, "END_CTA": 90}},
            "d_editorial_visible_fields": ["title", "subtitle", "call_to_action"],
            "family_music": {"route": "C11_C_FAMILY_MUSIC_V4", "profile_id": "ORGANIC_BLOOM",
                "same_seed_ab_identical": True, "changed_seed_c_distinct": True,
                "A": {"path": wav_a, "sha256": wav_a_sha}, "B": {"path": wav_b, "sha256": wav_b_sha},
                "C": {"path": wav_c, "sha256": wav_c_sha}},
            "bitstream_isolation": {"video_stream_identical": True, "audio_stream_changed": True,
                "video_stream_sha256_A": "a" * 64, "video_stream_sha256_C": "a" * 64,
                "audio_stream_sha256_A": "b" * 64, "audio_stream_sha256_C": "c" * 64},
            "final_A": {"path": mp4_a, "sha256": mp4_a_sha, **final},
            "final_C_changed_music": {"path": mp4_c, "sha256": mp4_c_sha, **final},
        }
        receipt_path = output_root / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        summary = {"status": receipt["status"], "request_id": request_id,
                   "selector": f"pursuit/tier-{tier}", "family_music_profile": "ORGANIC_BLOOM",
                   "receipt": str(receipt_path)}
        summary_path = root / "artifacts" / "tests" / "c11e" / "batch" / f"{request_id}.CLI_EXECUTION_RESULT.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary), encoding="utf-8")
        request = batch.create_request(self.base, tier, request_id)
        return request, summary_path, receipt_path

    def test_plan_is_exactly_four_executable_pursuit_rows_tier_2_to_5(self):
        rows = batch.batch_plan("E4C-PURSUIT-T2-5-20261115T221400Z-a1b2c3d4")
        self.assertEqual([r["selector"] for r in rows], ["pursuit/tier-2", "pursuit/tier-3", "pursuit/tier-4", "pursuit/tier-5"])
        self.assertEqual(len({r["request_id"] for r in rows}), 4)
        self.assertTrue(all(r["family_music_profile"] == "ORGANIC_BLOOM" for r in rows))
        self.assertTrue(all(r["expected_frames"] == 690 for r in rows))

    def test_plan_rejects_consumed_or_malformed_t1_batch_id(self):
        for batch_id in ("E4C-PURSUIT-T1-5-20261115T012400Z-a1b2c3d4", "E4C-PURSUIT-T2-5-x123456", "bad-id", "E4C-TRACKING-T2-5-short"):
            with self.subTest(batch_id=batch_id), self.assertRaises(batch.BatchError):
                batch.batch_plan(batch_id)

    def test_request_is_selector_specific_and_seed_domains_are_preserved(self):
        request = batch.create_request(self.base, 4, "E4C-PRS-T4-a1b2c3d4")
        self.assertEqual(request["selection"], {"content_type": "visual_drills", "family_id": "pursuit", "variant_id": "tier-4"})
        self.assertEqual(request["request_id"], "E4C-PRS-T4-a1b2c3d4")
        self.assertEqual(request["seed"], 12345)
        self.assertEqual(request["music_seed"], 840001)
        self.assertNotEqual(request["seed"], request["music_seed"])
        self.assertEqual(request["production_override"]["title"], "PERSECUCIÓN VISUAL · NIVEL 4")
        self.assertTrue(request["audio_enabled"] and request["personalization_enabled"])
        self.assertEqual(request["provenance"]["request_origin"], "CLI")

    def test_request_does_not_mutate_base_template(self):
        before = self.base["selection"]["variant_id"]
        batch.create_request(self.base, 5, "E4C-PRS-T5-a1b2c3d4")
        self.assertEqual(self.base["selection"]["variant_id"], before)
        self.assertEqual(self.base["production_override"]["title"], "SEGUIMIENTO VISUAL · NIVEL 1")

    def test_expected_source_and_canonical_pins_are_bound(self):
        self.assertEqual(batch.SOURCE_PINS[batch.CONSUMER_REL], "d5cd8e24c0cfdd83ec035b006c76468ed637d6babf5f0a9fcca8a93817ba1aa8")
        self.assertEqual(batch.SOURCE_PINS[batch.CONSUMER_TEST_REL], "5da9ec59d0f6d716861e9a4cbcfc36db5e61f992c966a2294bb23ef2c344bafb")
        self.assertEqual(batch.SOURCE_PINS[batch.EXECUTOR_REL], "b7cbf7bd97f76f4c2e339840fc694d3f5b0e50186ba2456e45ff00e585751abe")
        self.assertEqual(batch.SOURCE_PINS["release/C11C_FREEZE_PACKAGE_MANIFEST.json"], batch.FROZEN_MANIFEST_SHA256)
        self.assertEqual(batch.SOURCE_PINS[batch.PURSUIT_CANONICAL_REL], batch.PURSUIT_CANONICAL_SHA256)
        self.assertEqual(len(batch.SOURCE_PINS), 35)

    def test_pursuit_timeline_is_derived_from_native_definition_and_dynamic_game_frames(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._project_root(root)
            timeline = batch.pursuit_timeline_contract(root)
            self.assertEqual(timeline["fps"], 30)
            self.assertEqual(timeline["gameplay_frames"], 510)
            self.assertEqual(timeline["pre_roll_frames"], 90)
            self.assertEqual(timeline["end_cta_frames"], 90)
            self.assertEqual(timeline["phase_counts"], {"PRE_ROLL": 90, "GAME": 510, "END_CTA": 90})
            self.assertEqual(timeline["total_frames"], 690)
            self.assertEqual(timeline["duration_seconds"], 23.0)

    def test_ffprobe_contract_accepts_23s_690_frame_h264_aac_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._project_root(root)
            timeline = batch.pursuit_timeline_contract(root)
            batch.verify_ffprobe_contract(self._final_fixture(), "PURSUIT_TIER_2_A", timeline)

    def test_ffprobe_contract_rejects_tracking_810_frame_27s_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._project_root(root)
            timeline = batch.pursuit_timeline_contract(root)
            with self.assertRaisesRegex(batch.BatchError, "DURATION_MISMATCH|FRAME_COUNT_MISMATCH"):
                batch.verify_ffprobe_contract(self._final_fixture(810, 27.0), "PURSUIT_TIER_2_A", timeline)

    def test_ffprobe_contract_rejects_wrong_pixel_format_and_av_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._project_root(root)
            timeline = batch.pursuit_timeline_contract(root)
            final = self._final_fixture()
            final["ffprobe"]["streams"][0]["pix_fmt"] = "yuvj420p"
            with self.assertRaises(batch.BatchError):
                batch.verify_ffprobe_contract(final, "PURSUIT_TIER_2_A", timeline)
            final = self._final_fixture()
            final["av_start_delta_seconds"] = 0.01
            with self.assertRaises(batch.BatchError):
                batch.verify_ffprobe_contract(final, "PURSUIT_TIER_2_A", timeline)

    def test_91_pin_snapshots_require_three_equal_physical_inventories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pins = self._source_inventory(root)
            receipt = {"source_pin_count": 91, "source_pins_pre_post_equal": True,
                       "source_pins_pre_execution": pins, "source_pins_immediately_pre_renderer": pins,
                       "source_pins_post_execution": pins}
            self.assertEqual(len(batch.verify_91_pin_snapshots(root, receipt, "pursuit/tier-2")), 64)
            receipt["source_pins_immediately_pre_renderer"] = pins[:-1]
            with self.assertRaisesRegex(batch.BatchError, "CARDINALITY_FAIL"):
                batch.verify_91_pin_snapshots(root, receipt, "pursuit/tier-2")

    def test_91_pin_snapshot_rejects_windows_and_posix_path_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pins = self._source_inventory(root)
            bad = dict(pins[0])
            bad["path"] = r"..\outside.bin"
            receipt = {"source_pin_count": 91, "source_pins_pre_post_equal": True,
                       "source_pins_pre_execution": [bad] + pins[1:],
                       "source_pins_immediately_pre_renderer": [bad] + pins[1:],
                       "source_pins_post_execution": [bad] + pins[1:]}
            with self.assertRaisesRegex(batch.BatchError, "PATH_INVALID"):
                batch.verify_91_pin_snapshots(root, receipt, "pursuit/tier-2")

    def test_91_pin_snapshot_detects_physical_source_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pins = self._source_inventory(root)
            receipt = {"source_pin_count": 91, "source_pins_pre_post_equal": True,
                       "source_pins_pre_execution": pins, "source_pins_immediately_pre_renderer": pins,
                       "source_pins_post_execution": pins}
            (root / pins[0]["path"]).write_bytes(b"mutated")
            with self.assertRaisesRegex(batch.BatchError, "SIZE_MISMATCH|SHA_MISMATCH"):
                batch.verify_91_pin_snapshots(root, receipt, "pursuit/tier-2")

    def test_full_qualification_accepts_native_pursuit_690_frame_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request, summary_path, _ = self._qualification_fixture(root, tier=2, request_id="E4C-PRS-T2-a1b2c3d4")
            result = batch.validate_qualification(root, request, summary_path, 2)
            self.assertEqual(result["selector"], "pursuit/tier-2")
            self.assertEqual(result["native_total_frames"], 690)
            self.assertEqual(result["native_duration_seconds"], 23.0)
            self.assertEqual(result["review_status"], "PENDING_OPERATOR_VISUAL_AUDIO_REVIEW")

    def test_full_qualification_rejects_tracking_810_frame_assumption(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request, summary_path, receipt_path = self._qualification_fixture(root, tier=2, request_id="E4C-PRS-T2-a1b2c3d4")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["native_timeline"].update({"total_frames": 810, "duration_seconds": 27.0, "gameplay_frames": 630})
            receipt["d_composition"].update({"frames_composed": 810, "frames_expected": 810,
                "phase_counts": {"PRE_ROLL": 90, "GAME": 630, "END_CTA": 90}})
            receipt["final_A"].update(self._final_fixture(810, 27.0))
            receipt["final_C_changed_music"].update(self._final_fixture(810, 27.0))
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            with self.assertRaisesRegex(batch.BatchError, "NATIVE_TIMELINE_MISMATCH"):
                batch.validate_qualification(root, request, summary_path, 2)

    def test_exact_failed_v4_t1_is_recovered_from_existing_receipt_without_rerender(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request, summary_path, _ = self._qualification_fixture(root, tier=1, request_id=batch.RECOVERY_T1_REQUEST_ID)
            evidence = root / "artifacts/tests/c11e/e4c_pursuit_tier_batch" / batch.RECOVERY_BATCH_ID
            evidence.mkdir(parents=True)
            (evidence / f"{batch.RECOVERY_T1_REQUEST_ID}.request.json").write_text(json.dumps(request), encoding="utf-8")
            expected_ids = [f"E4C-PRS-T{tier}-b3abbe94" for tier in (1, 2, 3, 4, 5)]
            values = {
                "ATTEMPT_RESERVED.lock.json": {"schema": "C11E-E4C-PURSUIT-TIER-BATCH-LOCK-V1",
                    "status": "ATTEMPT_RESERVED", "batch_id": batch.RECOVERY_BATCH_ID, "request_ids": expected_ids,
                    "source_pin_set_sha256": batch.RECOVERY_SOURCE_PIN_SET_SHA256, "git_checks": "SKIPPED", "commits": "OPERATOR_MANAGED"},
                "EXECUTION_AUTHORIZED_ONCE.json": {"schema": "C11E-E4C-PURSUIT-TIER-BATCH-EXECUTION-AUTH-V1",
                    "status": "AUTHORIZED_ONCE_BEFORE_FIRST_CHILD", "batch_id": batch.RECOVERY_BATCH_ID, "request_ids": expected_ids},
                "BATCH_PROGRESS.json": {"status": "STOPPED_FAIL_CLOSED", "batch_id": batch.RECOVERY_BATCH_ID,
                    "completed_rows": [], "current_selector": "pursuit/tier-1", "failed_selector": "pursuit/tier-1"},
                f"{batch.RECOVERY_T1_REQUEST_ID}.BATCH_ROW_FAILURE.json": {"status": "POST_CHILD_AUDIT_FAIL_CLOSED",
                    "error": "BatchError: pursuit/tier-1_NATIVE_TIMELINE_MISMATCH", "process_exit_code": 0,
                    "selector": "pursuit/tier-1", "request_id": batch.RECOVERY_T1_REQUEST_ID},
                f"{batch.RECOVERY_T1_REQUEST_ID}.CLI_EXECUTION_RESULT.json": json.loads(summary_path.read_text(encoding="utf-8")),
            }
            for filename, value in values.items():
                (evidence / filename).write_text(json.dumps(value), encoding="utf-8")
            summary_path.unlink()
            recovered = batch.recover_failed_tier1(root)
            self.assertEqual(recovered["selector"], "pursuit/tier-1")
            self.assertEqual(recovered["recovery_mode"], "REUSED_EXISTING_T1_NO_RERENDER")
            self.assertFalse(recovered["renderer_invoked_by_recovery"])
            self.assertEqual(recovered["native_total_frames"], 690)

    def test_recovery_rejects_changed_or_missing_one_shot_authorization(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "artifacts/tests/c11e/e4c_pursuit_tier_batch" / batch.RECOVERY_BATCH_ID
            evidence.mkdir(parents=True)
            for name in ("ATTEMPT_RESERVED.lock.json", "EXECUTION_AUTHORIZED_ONCE.json", "BATCH_PROGRESS.json",
                         f"{batch.RECOVERY_T1_REQUEST_ID}.BATCH_ROW_FAILURE.json",
                         f"{batch.RECOVERY_T1_REQUEST_ID}.CLI_EXECUTION_RESULT.json",
                         f"{batch.RECOVERY_T1_REQUEST_ID}.request.json"):
                (evidence / name).write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(batch.BatchError, "T1_RECOVERY_ORIGINAL_LOCK_MISMATCH"):
                batch.recover_failed_tier1(root)

    def test_missing_source_pin_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(batch.BatchError):
                batch.verify_pins(Path(directory))


if __name__ == "__main__":
    unittest.main(verbosity=2)
