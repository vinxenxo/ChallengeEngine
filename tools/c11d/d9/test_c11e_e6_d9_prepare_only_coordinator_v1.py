from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import c11e_e6_d9_prepare_only_coordinator_v1 as coord  # noqa: E402


def dump(path: Path, value: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.receipt, self.plan = self._fixture()

    def tearDown(self):
        self.tmp.cleanup()

    def _fixture(self):
        selected_rows = []
        intent_rows, envelope_rows = [], []
        execution = {k: False for k in ("e6_test_only_authorized", "godot_invoked", "renderer_invoked", "ffmpeg_invoked", "ffprobe_invoked", "audio_generated", "mux_invoked", "media_created", "production_dispatch", "new_batch_id_consumed")}
        execution["release_authority"] = "NONE"
        for challenge_id in coord.SELECTED_IDS:
            total = coord.EXPECTED_FRAMES[challenge_id]
            selected_rows.append({"challenge_id": challenge_id, "source_fps": 60, "source_frames": total, "gameplay_seed": 1000 + coord.SELECTED_IDS.index(challenge_id), "phase_ranges": []})
        for matrix_row in selected_rows:
            cid, total, seed = matrix_row["challenge_id"], matrix_row["source_frames"], matrix_row["gameplay_seed"]
            # Four contiguous half-open phases, ending exactly at native frame count.
            lengths = [1, total - 3, 1, 1]
            cursor = 0
            phases = []
            for name, length in zip(("HOOK", "GAME", "REVEAL", "CTA"), lengths):
                phases.append({"phase": name, "start_frame": cursor, "end_frame": cursor + length, "timebase": "SOURCE_FPS_HALF_OPEN"})
                cursor += length
            matrix_row["phase_ranges"] = phases
            for label in coord.LABELS:
                music_seed = coord.MUSIC_SEEDS[label]
                request_id = f"FIXTURE-{cid}-{label}"
                intent = {
                    "schema": "C11-E-PRODUCTION-INTENT-V1", "status": "PREPARED_E1_NOT_DISPATCHED",
                    "request": {"request_id": request_id, "content_type": "challenges", "selection": {"variant_id": cid}},
                    "seed_domains": {"gameplay": {"value": seed}, "music": {"value": music_seed}, "independent_domains": True},
                    "identity": {"intent_hash": f"intent-{cid}-{label}"},
                    "music_contract": {"unresolved_engine_parameters": ["tempo_bpm", "duration_seconds"], "dispatchable": False, "engine_invoked": False, "audio_created": False, "engine_request": {"music_seed": music_seed, "tempo_bpm": None, "duration_seconds": None}},
                    "execution_boundary": {"dispatch_authorized": False, "renderer_input_emitted": False, "renderer_dispatch_invoked": False, "renderer_activation": False, "production_execution": False, "media_created": False, "release_authority": "NONE", "d4_8": "BLOCKED"},
                    "output": {"created": False},
                }
                intent_path = self.root / "artifacts" / cid / f"{label}_intent.json"
                intent_sha = dump(intent_path, intent)
                envelope = {
                    "schema": "C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1", "schema_version": "1.0", "content_type": "challenges",
                    "status": "PREPARED_E1_NOT_DISPATCHED", "challenge_id": cid, "request_id": request_id,
                    "fields": [{"field": str(i)} for i in range(6)],
                    "e1_intent": intent, "intent_hash": intent["identity"]["intent_hash"],
                    "source_timebase": {"fps": 60, "total_frames": total, "kind": "SOURCE_FRAME_INDEX"},
                    "source_phase_ranges": phases,
                    "governance": {"renderer_input_emitted": False, "production_dispatch": False, "media_created": False, "release_authority": "NONE", "d4_8": "BLOCKED"},
                }
                envelope_path = self.root / "artifacts" / cid / f"{label}_envelope.json"
                envelope_sha = dump(envelope_path, envelope)
                intent_rows.append({"challenge_id": cid, "label": label, "gameplay_seed": seed, "music_seed": music_seed, "request_id": request_id, "validation_status": "PASS_E1_PREPARATION_ONLY", "intent_sha256": intent_sha, "intent_path": intent_path.relative_to(self.root).as_posix()})
                envelope_rows.append({"challenge_id": cid, "label": label, "intent_hash": intent["identity"]["intent_hash"], "envelope_sha256": envelope_sha, "envelope_path": envelope_path.relative_to(self.root).as_posix()})
        receipt = {
            "schema": "C11E-E6-CHALLENGE-PLAN-ONLY-RECEIPT-V1", "status": "PASS_E1_AND_D_ENVELOPE_PLANS_18_OF_18_EXECUTION_HELD", "run_id": coord.PLAN_RUN_ID,
            "c11c_frozen_manifest_sha256": coord.FROZEN_MANIFEST_SHA256, "d4_8_policy_sha256": coord.D4_8_SHA256,
            "source_pins": {"expected": 20, "passed": 20, "failed": 0}, "execution": execution,
            "e1_intents": {"expected": 18, "passed": 18, "rows": intent_rows}, "d_envelopes": {"expected": 18, "passed": 18, "rows": envelope_rows},
        }
        plan = {"schema": "C11E-E6-CHALLENGE-SIX-SELECTOR-PLAN-V1", "status": "PREPARED_PLAN_ONLY_NOT_FROZEN_FOR_MEDIA", "run_id": coord.PLAN_RUN_ID, "receipt_sha256": coord.PLAN_RECEIPT_SHA256, "selected_ids": list(coord.SELECTED_IDS), "selected_rows": selected_rows, "execution": execution}
        return receipt, plan

    def test_exact_six_selectors_and_18_probes_pass(self):
        rows = coord.validate_plan_artifacts(self.root, self.receipt, self.plan)
        self.assertEqual(len(rows), 18)
        self.assertEqual({r["challenge_id"] for r in rows}, set(coord.SELECTED_IDS))

    def test_rejects_wrong_selector_set(self):
        plan = copy.deepcopy(self.plan)
        plan["selected_ids"][0] = "CHALLENGE_003"
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, self.receipt, plan)

    def test_rejects_missing_probe(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["e1_intents"]["rows"].pop()
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_rejects_duplicate_probe(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["e1_intents"]["rows"][-1] = copy.deepcopy(receipt["e1_intents"]["rows"][0])
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_rejects_gameplay_seed_drift(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["e1_intents"]["rows"][0]["gameplay_seed"] += 1
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_rejects_music_seed_drift(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["e1_intents"]["rows"][2]["music_seed"] += 1
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_rejects_artifact_hash_tamper(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["e1_intents"]["rows"][0]["intent_sha256"] = "0" * 64
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_rejects_nested_selector_mismatch(self):
        receipt = copy.deepcopy(self.receipt)
        row = receipt["e1_intents"]["rows"][0]
        p = self.root / row["intent_path"]
        obj = json.loads(p.read_text())
        obj["request"]["selection"]["variant_id"] = "CHALLENGE_003"
        dump(p, obj)
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_rejects_timeline_mismatch(self):
        receipt = copy.deepcopy(self.receipt)
        row = receipt["d_envelopes"]["rows"][0]
        p = self.root / row["envelope_path"]
        obj = json.loads(p.read_text())
        obj["source_timebase"]["total_frames"] += 1
        dump(p, obj)
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_rejects_media_authority(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["execution"]["godot_invoked"] = True
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_rejects_path_traversal(self):
        with self.assertRaises(coord.CoordinatorError):
            coord.contained_path(self.root, "../../outside.json")

    def test_rejects_noncontiguous_phase_ranges(self):
        with self.assertRaises(coord.CoordinatorError):
            coord._phase_signature([
                {"phase":"HOOK","start_frame":0,"end_frame":1},
                {"phase":"GAME","start_frame":2,"end_frame":3},
                {"phase":"REVEAL","start_frame":3,"end_frame":4},
                {"phase":"CTA","start_frame":4,"end_frame":5},
            ])

    def test_rejects_envelope_nested_intent_mismatch(self):
        receipt = copy.deepcopy(self.receipt)
        row = receipt["d_envelopes"]["rows"][0]
        p = self.root / row["envelope_path"]
        obj = json.loads(p.read_text())
        obj["e1_intent"]["request"]["request_id"] = "TAMPERED"
        row["envelope_sha256"] = dump(p, obj)
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_rejects_phase_range_drift_against_plan(self):
        receipt = copy.deepcopy(self.receipt)
        row = receipt["d_envelopes"]["rows"][0]
        p = self.root / row["envelope_path"]
        obj = json.loads(p.read_text())
        obj["source_phase_ranges"][1]["start_frame"] += 1
        row["envelope_sha256"] = dump(p, obj)
        with self.assertRaises(coord.CoordinatorError):
            coord.validate_plan_artifacts(self.root, receipt, self.plan)

    def test_coordinator_has_no_subprocess_or_os_command_imports(self):
        import ast
        tree = ast.parse((HERE / "c11e_e6_d9_prepare_only_coordinator_v1.py").read_text(encoding="utf-8"))
        imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        imported.update(node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module)
        self.assertNotIn("subprocess", imported)
        external_calls = {
            node.func.attr for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name) and node.func.value.id in {"os", "subprocess"}
        }
        self.assertFalse({"system", "popen", "run", "Popen"} & external_calls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
