from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "c11e_e6_d9_capture_orchestration_prepare_only_v1.py"
spec = importlib.util.spec_from_file_location("capture_plan", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def jwrite(path: Path, value: dict) -> str:
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def fixture_probes(root: Path, *, c_gameplay_override=None, c_music_override=None, bad_phase=False):
    rows = []
    for challenge_id in module.SELECTED_IDS:
        frames = module.EXPECTED_SOURCE_FRAMES[challenge_id]
        gameplay = module.EXPECTED_GAMEPLAY_SEEDS[challenge_id]
        phase_ranges = [
            {"phase": "HOOK", "start_frame": 0, "end_frame": 0},
            {"phase": "GAME", "start_frame": 0, "end_frame": frames - 120},
            {"phase": "REVEAL", "start_frame": frames - 120, "end_frame": frames - 120},
            {"phase": "CTA", "start_frame": frames - 120, "end_frame": frames},
        ]
        if bad_phase and challenge_id == "CHALLENGE_001":
            phase_ranges[1]["end_frame"] -= 1
        for label in module.LABELS:
            music = 840001 if label in ("A", "B_REPEAT") else 840002
            row_gameplay = gameplay
            if label == "C_CHANGED_MUSIC_SEED" and c_gameplay_override is not None and challenge_id == "CHALLENGE_001":
                row_gameplay = c_gameplay_override
            if label == "C_CHANGED_MUSIC_SEED" and c_music_override is not None and challenge_id == "CHALLENGE_001":
                music = c_music_override
            request_id = f"TEST-{challenge_id}-{label}"
            intent_hash = hashlib.sha256(request_id.encode()).hexdigest()
            intent = {
                "request_origin": "TEST",
                "request": {"request_id": request_id, "selection": {"variant_id": challenge_id}},
                "identity": {"intent_hash": intent_hash},
                "seed_domains": {"gameplay": {"value": row_gameplay}, "music": {"value": music}},
                "music_contract": {
                    "engine_request": {"music_seed": music, "tempo_bpm": None, "duration_seconds": None},
                    "engine_invoked": False,
                    "audio_created": False,
                },
                "execution_boundary": {
                    "dispatch_authorized": False,
                    "renderer_input_emitted": False,
                    "renderer_dispatch_invoked": False,
                    "renderer_activation": False,
                    "production_execution": False,
                    "media_created": False,
                    "release_authority": "NONE",
                    "d4_8": "BLOCKED",
                },
            }
            intent_rel = f"intents/{challenge_id}_{label}.json"
            intent_sha = jwrite(root / intent_rel, intent)
            envelope = {
                "challenge_id": challenge_id,
                "request_id": request_id,
                "intent_hash": intent_hash,
                "e1_intent": intent,
                "source_timebase": {"fps": 60, "total_frames": frames, "kind": "SOURCE_FRAME_INDEX"},
                "source_phase_ranges": phase_ranges,
                "status": "PREPARED_E1_NOT_DISPATCHED",
                "governance": {"media_created": False},
            }
            env_rel = f"envelopes/{challenge_id}_{label}.json"
            env_sha = jwrite(root / env_rel, envelope)
            rows.append({
                "challenge_id": challenge_id,
                "label": label,
                "gameplay_seed": gameplay,
                "music_seed": 840001 if label in ("A", "B_REPEAT") else 840002,
                "request_id": request_id,
                "intent_hash": intent_hash,
                "intent_sha256": intent_sha,
                "intent_path": intent_rel,
                "envelope_sha256": env_sha,
                "envelope_path": env_rel,
                "source_fps": 60,
                "source_frames": frames,
                "phase_ranges": phase_ranges,
            })
    return rows


def hydration_fixture():
    return {
        "run_id": module.HYDRATION_RUN_ID,
        "status": "BLOCKED_E6_REUSE_EVIDENCE_INCOMPLETE",
        "check_count": 1803,
        "passed_checks": 1801,
        "failed_checks": 2,
        "failure_categories": {"historical_source_pin_divergence": 2, "other_failures": 0},
        "checks": [
            {"path": p, "expected_sha256": e, "actual_sha256": a, "status": "HISTORICAL_SOURCE_PIN_DIVERGENCE"}
            for p, e, a in sorted(module.EXPECTED_HISTORICAL_FAILURES)
        ] + [{"check": "sample-pass", "status": "PASS"}],
        "counts": {
            "challenge004_nested_files": 34,
            "drill_nested_files": 1680,
            "drill_receipts": 6,
            "loop22_nested_files": 8,
            "r1v_loop_slots": 5,
            "source_pins": 33,
        },
        "governance": {
            "source_checkout_mutated": False,
            "godot_invoked": False,
            "ffmpeg_invoked": False,
            "ffprobe_invoked": False,
            "media_created": False,
            "batch_id_consumed": False,
            "release_authority": "NONE",
        },
    }


class PhaseRangeTests(unittest.TestCase):
    def test_01_four_phase_half_open_ranges_pass(self):
        self.assertEqual(module.phase_signature([
            {"phase": "HOOK", "start_frame": 0, "end_frame": 0},
            {"phase": "GAME", "start_frame": 0, "end_frame": 100},
            {"phase": "REVEAL", "start_frame": 100, "end_frame": 100},
            {"phase": "CTA", "start_frame": 100, "end_frame": 150},
        ], 150)[-1]["end_frame"], 150)

    def test_02_gap_rejected(self):
        with self.assertRaisesRegex(module.PlanError, "CONTIGUOUS"):
            module.phase_signature([
                {"phase": "HOOK", "start_frame": 0, "end_frame": 0},
                {"phase": "GAME", "start_frame": 1, "end_frame": 100},
                {"phase": "REVEAL", "start_frame": 100, "end_frame": 100},
                {"phase": "CTA", "start_frame": 100, "end_frame": 150},
            ], 150)

    def test_03_phase_sum_mismatch_rejected(self):
        with self.assertRaisesRegex(module.PlanError, "PHASE_SUM"):
            module.phase_signature([
                {"phase": "HOOK", "start_frame": 0, "end_frame": 0},
                {"phase": "GAME", "start_frame": 0, "end_frame": 100},
                {"phase": "REVEAL", "start_frame": 100, "end_frame": 100},
                {"phase": "CTA", "start_frame": 100, "end_frame": 149},
            ], 150)


class ProbeLinkTests(unittest.TestCase):
    def test_04_exact_18_rows_pass(self):
        with tempfile.TemporaryDirectory() as td:
            rows = fixture_probes(Path(td))
            checked = module.verify_probes(Path(td), rows)
            self.assertEqual(len(checked), 18)

    def test_05_missing_probe_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            rows = fixture_probes(Path(td))
            with self.assertRaisesRegex(module.PlanError, "EXPECTED_18"):
                module.verify_probes(Path(td), rows[:-1])

    def test_06_duplicate_probe_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            rows = fixture_probes(Path(td))
            rows[-1] = dict(rows[0])
            with self.assertRaisesRegex(module.PlanError, "UNKNOWN_OR_DUPLICATE"):
                module.verify_probes(Path(td), rows)

    def test_07_c_gameplay_seed_change_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            rows = fixture_probes(Path(td), c_gameplay_override=999)
            with self.assertRaisesRegex(module.PlanError, "GAMEPLAY_SEED_MISMATCH"):
                module.verify_probes(Path(td), rows)

    def test_08_c_music_seed_not_changed_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            rows = fixture_probes(Path(td), c_music_override=840001)
            with self.assertRaisesRegex(module.PlanError, "MUSIC_SEED_PROPOSAL_MISMATCH"):
                module.verify_probes(Path(td), rows)

    def test_09_intent_sha_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            rows = fixture_probes(Path(td))
            rows[0]["intent_sha256"] = "0" * 64
            with self.assertRaisesRegex(module.PlanError, "SHA256_MISMATCH"):
                module.verify_probes(Path(td), rows)

    def test_10_envelope_sha_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            rows = fixture_probes(Path(td))
            rows[0]["envelope_sha256"] = "0" * 64
            with self.assertRaisesRegex(module.PlanError, "SHA256_MISMATCH"):
                module.verify_probes(Path(td), rows)

    def test_11_phase_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            rows = fixture_probes(Path(td), bad_phase=True)
            with self.assertRaisesRegex(module.PlanError, "CONTIGUOUS"):
                module.verify_probes(Path(td), rows)


class HydrationDispositionTests(unittest.TestCase):
    def test_12_exact_two_ch004_failures_are_recognized_without_waiver(self):
        result = module.validate_hydration_report_content(hydration_fixture())
        self.assertEqual(result["failures"], 2)
        self.assertIn("PENDING_HISTORICAL_SOURCE_PIN_ADJUDICATION", result["failure_disposition"])

    def test_13_third_failure_is_rejected(self):
        report = hydration_fixture()
        report["checks"].append({"path": "unexpected.py", "expected_sha256": "a", "actual_sha256": "b", "status": "FAIL"})
        with self.assertRaisesRegex(module.PlanError, "FAILURE_SET_MISMATCH"):
            module.validate_hydration_report_content(report)

    def test_14_mutated_checkout_or_media_is_rejected(self):
        report = hydration_fixture()
        report["governance"]["media_created"] = True
        with self.assertRaisesRegex(module.PlanError, "CROSSED_EXECUTION_BOUNDARY"):
            module.validate_hydration_report_content(report)


class CaptureCardinalityTests(unittest.TestCase):
    def test_15_six_groups_each_have_one_visual_source_and_three_audio_probes(self):
        probes = []
        for challenge_id in module.SELECTED_IDS:
            for label in module.LABELS:
                probes.append({
                    "challenge_id": challenge_id, "label": label,
                    "request_id": f"{challenge_id}-{label}", "intent_hash": "a" * 64,
                    "intent_sha256": "b" * 64, "envelope_sha256": "c" * 64,
                    "gameplay_seed": module.EXPECTED_GAMEPLAY_SEEDS[challenge_id],
                    "music_seed_proposal": 840001 if label != "C_CHANGED_MUSIC_SEED" else 840002,
                })
        with patch.object(module, "verify_file", side_effect=lambda root, rel, expected, label, sidecar=True: {"path": str(rel), "sha256": expected, "bytes": 1, "status": "PASS"}):
            with tempfile.TemporaryDirectory() as td:
                groups = module.build_capture_groups(Path(td), probes)
        self.assertEqual(len(groups), 6)
        for group in groups:
            self.assertEqual(group["visual_source"]["logical_capture_count"], 1)
            self.assertEqual(group["visual_source"]["shared_by_probe_labels"], list(module.LABELS))
            self.assertEqual(len(group["audio_probe_variants"]), 3)
            self.assertTrue(all(x["shares_visual_source"] for x in group["audio_probe_variants"]))

    def test_16_ch004_not_marked_reusable(self):
        probes = []
        for challenge_id in module.SELECTED_IDS:
            for label in module.LABELS:
                probes.append({
                    "challenge_id": challenge_id, "label": label,
                    "request_id": f"{challenge_id}-{label}", "intent_hash": "a" * 64,
                    "intent_sha256": "b" * 64, "envelope_sha256": "c" * 64,
                    "gameplay_seed": module.EXPECTED_GAMEPLAY_SEEDS[challenge_id],
                    "music_seed_proposal": 840001 if label != "C_CHANGED_MUSIC_SEED" else 840002,
                })
        with patch.object(module, "verify_file", side_effect=lambda root, rel, expected, label, sidecar=True: {"path": str(rel), "sha256": expected, "bytes": 1, "status": "PASS"}):
            with tempfile.TemporaryDirectory() as td:
                groups = module.build_capture_groups(Path(td), probes)
        ch004 = next(g for g in groups if g["challenge_id"] == "CHALLENGE_004")
        self.assertIn("FRESH_SOURCE_CAPTURE_REQUIRED", ch004["reuse_disposition"])
        self.assertIn("HISTORICAL_SOURCE_PIN_DIVERGENCE", ch004["reuse_disposition"])


class SafetyAndIOTests(unittest.TestCase):
    def test_17_no_process_execution_imports(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(imported.isdisjoint({"subprocess", "multiprocessing", "shutil", "pexpect"}))

    def test_18_atomic_write_is_add_only(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "receipt.json"
            path.write_text("existing", encoding="utf-8")
            with self.assertRaisesRegex(module.PlanError, "OUTPUT_COLLISION"):
                module.atomic_write(path, b"new")
            self.assertEqual(path.read_text(encoding="utf-8"), "existing")

    def test_19_route_audit_hash_is_configured(self):
        self.assertRegex(module.ROUTE_AUDIT_SCRIPT_SHA256, r"^[0-9a-f]{64}$")
        self.assertEqual(module.ROUTE_AUDIT_SCRIPT_NAME, "c11e_e6_challenge_capture_route_audit_v1.py")


if __name__ == "__main__":
    unittest.main(verbosity=2)
