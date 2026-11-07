#!/usr/bin/env python3
"""Static, negative and optional active-checkout integration tests for R1V Q5."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER_PATH = HERE / "c11e_r1v_five_family_qualification.py"
spec = importlib.util.spec_from_file_location("c11e_r1v", RUNNER_PATH)
r1v = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(r1v)

PAYLOAD_ROOT: Path | None = None
PROJECT_ROOT: Path | None = None
R1P_ARCHIVE: Path | None = None


class R1VStaticTests(unittest.TestCase):
    def test_canonical_json_is_stable(self):
        left = {"z": 1, "a": {"d": 4, "b": 2}}
        right = {"a": {"b": 2, "d": 4}, "z": 1}
        self.assertEqual(r1v.canonical_sha256(left), r1v.canonical_sha256(right))

    def test_rational_time_base(self):
        self.assertEqual(r1v.parse_rate("1/30"), r1v.Fraction(1, 30))

    def test_rational_rejects_invalid(self):
        with self.assertRaises(r1v.R1VError):
            r1v.parse_rate("not-a-rate")

    def test_read_exact_reads_full_buffer(self):
        import io
        self.assertEqual(r1v.read_exact(io.BytesIO(b"abcdefgh"), 8), b"abcdefgh")

    def test_read_exact_reports_short_buffer(self):
        import io
        self.assertEqual(r1v.read_exact(io.BytesIO(b"abc"), 5), b"abc")

    def test_exactly_five_family_selectors(self):
        self.assertEqual(len(r1v.SELECTOR_EXPECTATIONS), 5)
        self.assertEqual({x["family_id"] for x in r1v.SELECTOR_EXPECTATIONS}, {
            "c11c_fractal_bloom_v1", "c11c_geometric_waves_v1", "c11c_invisible_forces_v1",
            "c11c_living_particles_v1", "c11c_sacred_symmetry_v1"})
        self.assertEqual(len({x["gameplay_seed"] for x in r1v.SELECTOR_EXPECTATIONS}), 5)
        self.assertEqual(len({x["grammar_id"] for x in r1v.SELECTOR_EXPECTATIONS}), 5)

    def test_selector_timing_matches_r1p(self):
        for selector in r1v.SELECTOR_EXPECTATIONS:
            self.assertEqual(selector["frame_count_consistency_only"],
                             selector["fps"] * int(selector["duration_seconds"]))
            self.assertIn(selector["duration_seconds"], (20.0, 22.0, 23.0))
            self.assertEqual(selector["fps"], 30)

    def test_all_source_pins_are_finalized(self):
        pins = [*r1v.ADDITIONAL_SOURCE_PINS.values(), *r1v.OPTION_C_SOURCE_PINS.values()]
        self.assertEqual(len(r1v.ADDITIONAL_SOURCE_PINS), 28)
        self.assertEqual(len(r1v.OPTION_C_SOURCE_PINS), 3)
        for pin in pins:
            self.assertEqual(len(pin["sha256"]), 64)
            int(pin["sha256"], 16)
            self.assertGreater(pin["bytes"], 0)
        self.assertEqual(r1v.ADDITIONAL_SOURCE_PINS[
            "tools/prototypes/c11c_living_particles_v1/LivingParticles.gdshader"]["sha256"],
            "b1ec5c82d8905617cb78d9a905d1d2194c1a5d54e6b3ee049ad6a6cd6c54305f")

    def _c11c_sidecar_fixture(self):
        selector = r1v.SELECTOR_EXPECTATIONS[1]
        authoring = {
            "seed": selector["gameplay_seed"], "family_id": "geometric",
            "grammar_id": selector["grammar_id"], "duration_seconds": selector["duration_seconds"],
            "fps": 30, "frame_count": selector["frame_count_consistency_only"], "sound_enabled": False,
        }
        manifest = {
            "prototype_id": "C11-C.1_GEOMETRIC_WAVES_V1", "revision": "2.16.3",
            "seed": selector["gameplay_seed"], "family_id": "geometric", "production_id": selector["family_id"],
            "grammar_id": selector["grammar_id"],
            "visual": {"canvas": "720x1280", "duration_seconds": selector["duration_seconds"],
                       "fps": 30, "frame_count": selector["frame_count_consistency_only"]},
            "audio": {"enabled": False, "muxed_into_mp4": False},
            "artifact_policy": {"export_gif": False, "keep_avi": False, "avi_intermediate": True},
        }
        return selector, authoring, manifest

    def test_c11c_authentic_nested_sidecar_schema_passes(self):
        selector, authoring, manifest = self._c11c_sidecar_fixture()
        r1v.validate_c11c_sidecars(authoring, manifest, selector, "A")

    def test_c11c_sidecar_audio_enabled_is_rejected(self):
        selector, authoring, manifest = self._c11c_sidecar_fixture()
        manifest["audio"]["enabled"] = True
        with self.assertRaises(r1v.R1VError):
            r1v.validate_c11c_sidecars(authoring, manifest, selector, "A")

    def test_c11c_sidecar_audio_mux_is_rejected(self):
        selector, authoring, manifest = self._c11c_sidecar_fixture()
        manifest["audio"]["muxed_into_mp4"] = True
        with self.assertRaises(r1v.R1VError):
            r1v.validate_c11c_sidecars(authoring, manifest, selector, "A")

    def test_c11c_sidecar_gif_and_avi_retention_are_rejected(self):
        selector, authoring, manifest = self._c11c_sidecar_fixture()
        manifest["artifact_policy"]["export_gif"] = True
        with self.assertRaises(r1v.R1VError):
            r1v.validate_c11c_sidecars(authoring, manifest, selector, "A")
        selector, authoring, manifest = self._c11c_sidecar_fixture()
        manifest["artifact_policy"]["keep_avi"] = True
        with self.assertRaises(r1v.R1VError):
            r1v.validate_c11c_sidecars(authoring, manifest, selector, "A")

    def test_launcher_command_exactly_limited(self):
        selector = r1v.SELECTOR_EXPECTATIONS[0]
        cmd = r1v.build_launcher_command("powershell.exe", Path("launcher.ps1"), selector,
                                         Path("new-output"), "R1V_TEST_A")
        self.assertIn("-NoSound", cmd)
        self.assertIn("-Seed", cmd)
        self.assertIn(str(selector["gameplay_seed"]), cmd)
        self.assertIn("-Grammar", cmd)
        self.assertIn(selector["grammar_id"], cmd)
        self.assertIn("-Duration", cmd)
        self.assertIn("-OutputRoot", cmd)
        self.assertIn("-OutputTag", cmd)
        self.assertNotIn("-KeepAvi", cmd)
        self.assertNotIn("-ExportGif", cmd)
        self.assertNotIn("-NoFooter", cmd)
        self.assertNotIn("-MusicSeed", cmd)
        self.assertEqual(cmd.count("-NoSound"), 1)

    def test_launcher_command_uses_only_allowed_switch_count(self):
        selector = r1v.SELECTOR_EXPECTATIONS[2]
        cmd = r1v.build_launcher_command("powershell.exe", Path("launcher.ps1"), selector,
                                         Path("new-output"), "R1V_TEST_B")
        switches = [x for x in cmd if x.startswith("-")]
        self.assertEqual(switches, ["-NoProfile", "-ExecutionPolicy", "-File", "-Seed", "-Grammar",
                                    "-Duration", "-NoSound", "-OutputRoot", "-OutputTag"])

    def test_policy_and_approval_hashes(self):
        self.assertIsNotNone(PAYLOAD_ROOT)
        policy_path = PAYLOAD_ROOT / "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json"
        approval_path = PAYLOAD_ROOT / "definitions/c11d/production/C11E_D4_8_R1V_OPERATOR_APPROVAL_RECORD_20261107_V1.json"
        policy = r1v.load_json(policy_path)
        approval = r1v.load_json(approval_path)
        self.assertEqual(r1v.sha256_file(policy_path), r1v.R1V_POLICY_SHA256)
        approval_data = dict(approval)
        stored = approval_data.pop("approval_record_sha256")
        self.assertEqual(stored, r1v.canonical_sha256(approval_data))
        self.assertEqual(stored, policy["authority_boundary"]["approval_record_sha256"])

    def test_policy_enforces_exact_approval_scope(self):
        self.assertIsNotNone(PAYLOAD_ROOT)
        policy_path = PAYLOAD_ROOT / "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json"
        approval_path = PAYLOAD_ROOT / "definitions/c11d/production/C11E_D4_8_R1V_OPERATOR_APPROVAL_RECORD_20261107_V1.json"
        policy = r1v.load_json(policy_path)
        approval = r1v.load_json(approval_path)
        self.assertEqual(policy["selectors"], [{k: s[k] for k in (
            "receipt_index", "family_id", "grammar_id", "grammar_index", "gameplay_seed", "duration_seconds",
            "fps", "frame_count_consistency_only", "launcher_path", "launcher_sha256", "prototype_path",
            "prototype_sha256", "scene_path", "scene_sha256")}
            for s in r1v.SELECTOR_EXPECTATIONS])
        self.assertEqual(policy["execution"]["approval_scope"], approval["scope"])
        self.assertEqual(approval["scope"]["launcher_invocations"], 10)
        self.assertTrue(policy["execution"]["launcher_invocations_exact"] == 10)
        self.assertTrue(policy["forbidden"]["d_compositor_dispatch"])
        self.assertTrue(policy["forbidden"]["d3_music_engine"])
        self.assertTrue(policy["forbidden"]["ffmpeg_filter_or_mux"])
        self.assertFalse(policy["forbidden"]["ffmpeg_encode_filter_or_mux"])
        self.assertEqual(policy["governance"]["d_renderer_dispatch"], "OFF")
        self.assertEqual(policy["governance"]["d4_8_general_production"], "BLOCKED")

    def test_policy_encodes_only_exact_native_silent_encode_argv(self):
        self.assertIsNotNone(PAYLOAD_ROOT)
        policy_path = PAYLOAD_ROOT / "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json"
        policy = r1v.load_json(policy_path)
        self.assertEqual(policy["permitted_native_c11c_encode"]["argv_template"], [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", "<AVI>", "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "<MP4>"])
        self.assertFalse(policy["allowances"]["ffmpeg_filters"])
        self.assertFalse(policy["allowances"]["ffmpeg_mux"])

    def test_policy_hash_changes_when_tampered(self):
        self.assertIsNotNone(PAYLOAD_ROOT)
        policy_path = PAYLOAD_ROOT / "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json"
        original = r1v.sha256_file(policy_path)
        self.assertEqual(original, r1v.R1V_POLICY_SHA256)
        altered = policy_path.read_bytes() + b" "
        self.assertNotEqual(hashlib.sha256(altered).hexdigest(), r1v.R1V_POLICY_SHA256)

    def test_compare_repeats_passes_identical_source_inventory(self):
        rows = []
        for s in r1v.SELECTOR_EXPECTATIONS:
            base = {"selector": s["family_id"], "frame_count": s["frame_count_consistency_only"],
                    "pts": list(range(s["frame_count_consistency_only"])), "time_base": "1/30",
                    "frame_hashes": ["a" * 64, "b" * 64],
                    "global_decoded_stream_sha256": "c" * 64,
                    "video_sha256": "d" * 64,
                    "video_stream": {"width":720,"height":1280,"pix_fmt":"yuv420p","r_frame_rate":"30/1"}}
            rows.append({**base,"repeat":"A"})
            rows.append({**base,"repeat":"B"})
        result = r1v.compare_repeats(rows)
        self.assertEqual(result["deterministic_repeat_passed"], 5)

    def test_compare_repeats_rejects_pixel_divergence(self):
        rows = []
        for s in r1v.SELECTOR_EXPECTATIONS:
            base = {"selector": s["family_id"], "frame_count": s["frame_count_consistency_only"],
                    "pts": list(range(s["frame_count_consistency_only"])), "time_base": "1/30",
                    "frame_hashes": ["a" * 64], "global_decoded_stream_sha256": "c" * 64,
                    "video_sha256": "d" * 64,
                    "video_stream": {"width":720,"height":1280,"pix_fmt":"yuv420p","r_frame_rate":"30/1"}}
            rows.append({**base,"repeat":"A"})
            rows.append({**base,"repeat":"B", "frame_hashes":["e"*64]})
        with self.assertRaises(r1v.R1VError):
            r1v.compare_repeats(rows)

    def test_override_restore_recovers_only_exact_known_c11c_temporary_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "override.cfg"
            original = b"[display]\nwindow/size/viewport_width=640\n"
            path.write_bytes(original)
            path.write_bytes(r1v.EXPECTED_C11C_OVERRIDE_BYTES)
            result = r1v.restore_known_c11c_override_state(path, True, original)
            self.assertEqual(result, "RESTORED_EXACT_KNOWN_C11C_TEMPORARY; RUN_MUST_FAIL")
            self.assertEqual(path.read_bytes(), original)

    def test_override_restore_never_clobbers_unknown_external_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "override.cfg"
            original = b"original"
            unexpected = b"changed by another process"
            path.write_bytes(unexpected)
            with self.assertRaises(r1v.R1VError):
                r1v.restore_known_c11c_override_state(path, True, original)
            self.assertEqual(path.read_bytes(), unexpected)

    def test_override_created_unknown_is_left_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "override.cfg"
            unexpected = b"external edit"
            path.write_bytes(unexpected)
            with self.assertRaises(r1v.R1VError):
                r1v.restore_known_c11c_override_state(path, False, None)
            self.assertEqual(path.read_bytes(), unexpected)

    def test_safe_project_file_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaises(r1v.R1VError):
                r1v.safe_project_file(root,"../outside.txt")

    def test_report_and_policy_constants_are_pinned(self):
        self.assertEqual(r1v.FROZEN_C11C_MANIFEST_SHA256,
                         "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")
        self.assertEqual(r1v.STATIC_AUDIT_SHA256,
                         "600c22dafe2e377cb02b4a69f8823a44745d705b71cdb0d6bcec38da52df3e92")
        self.assertEqual(r1v.R1P_RECOVERED_ZIP_SHA256,
                         "d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52")


class R1VActiveCheckoutIntegrationTests(unittest.TestCase):
    def test_active_checkout_r1p_receipts_and_all_source_pins(self):
        if not (PROJECT_ROOT and PAYLOAD_ROOT and R1P_ARCHIVE):
            self.skipTest("active-checkout args not supplied")
        result = r1v.verify_r1p_archive(PROJECT_ROOT, R1P_ARCHIVE)
        self.assertEqual(result["receipt_count"], 27)
        self.assertEqual(result["total_source_pins_verified"], 61)

    def test_active_checkout_option_c_receipts(self):
        if not (PROJECT_ROOT and PAYLOAD_ROOT):
            self.skipTest("active-checkout args not supplied")
        result = r1v.verify_option_c_evidence(PROJECT_ROOT)
        self.assertEqual(result["handoffs"], 27)
        self.assertEqual(result["architecture_decision"], "OPERATOR_APPROVED_OPTION_C")

    def test_active_checkout_d4_policy_and_r1v_approval(self):
        if not (PROJECT_ROOT and PAYLOAD_ROOT):
            self.skipTest("active-checkout args not supplied")
        policy = PAYLOAD_ROOT / "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json"
        approval = PAYLOAD_ROOT / "definitions/c11d/production/C11E_D4_8_R1V_OPERATOR_APPROVAL_RECORD_20261107_V1.json"
        result = r1v.verify_approval_policy(PROJECT_ROOT, policy, approval)
        self.assertEqual(result["launcher_invocations_authorized"], 10)
        self.assertEqual(result["d4_8_production_policy_state"], "DISABLED_UNCHANGED")


def main() -> int:
    global PAYLOAD_ROOT, PROJECT_ROOT, R1P_ARCHIVE
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--payload-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--r1p-archive", type=Path)
    args = parser.parse_args()
    PAYLOAD_ROOT = args.payload_root.resolve()
    PROJECT_ROOT = args.project_root.resolve() if args.project_root else None
    if args.r1p_archive:
        R1P_ARCHIVE = args.r1p_archive.resolve()
    elif PROJECT_ROOT:
        R1P_ARCHIVE = PROJECT_ROOT / "artifacts/tests/c11e/e4b_r1p/E4B_R1P_20261107_032743_5F75045C_RECOVERED.zip"
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({"status": "PASS_R1V_STATIC_AND_ACTIVE_CHECKOUT_TESTS" if result.wasSuccessful() else "FAIL_R1V_TESTS",
                      "tests_run": result.testsRun, "failures": len(result.failures),
                      "errors": len(result.errors), "active_checkout_integration": PROJECT_ROOT is not None}, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
