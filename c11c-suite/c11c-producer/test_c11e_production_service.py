from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from c11e_production_service import (
    C11EProductionServiceError,
    prepare_c11e_production_intent,
    validate_c11e_production_intent,
)

ROOT = Path(__file__).resolve().parents[2]


def request(*, title: str = "E1 service test", seed: int = 12345, music_seed: int = 840001, origin: str = "TEST", request_id: str = "C11E-E1-TEST-001") -> dict:
    return {
        "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "PRODUCTION",
        "selection": {"content_type": "challenges", "variant_id": "CHALLENGE_001"},
        "seed": seed,
        "music_seed": music_seed,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": False,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": {"title": title},
        "provenance": {"source_revision": "C11E-E1-TEST", "request_origin": origin},
    }


class C11EProductionServiceTests(unittest.TestCase):
    def test_challenge_request_resolves_and_fails_closed(self):
        prepared = prepare_c11e_production_intent(request(), ROOT)
        intent = prepared["intent"]
        self.assertEqual(intent["status"], "PREPARED_E1_NOT_DISPATCHED")
        self.assertEqual(intent["request"]["selection"]["variant_id"], "CHALLENGE_001")
        self.assertEqual(intent["editorial"]["title"], "E1 service test")
        self.assertEqual(intent["seed_domains"]["gameplay"]["value"], 12345)
        self.assertEqual(intent["seed_domains"]["music"]["value"], 840001)
        self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")
        self.assertFalse(intent["execution_boundary"]["renderer_activation"])
        self.assertFalse(intent["execution_boundary"]["production_execution"])
        self.assertFalse(intent["execution_boundary"]["media_created"])

    def test_visual_loop_selection_is_resolved_and_source_identified(self):
        raw = request(request_id="C11E-E1-LOOP-001")
        raw["selection"] = {
            "content_type": "visual_loops",
            "family_id": "c11c_geometric_waves_v1",
            "subtype_id": "harmonic_membrane",
        }
        intent = prepare_c11e_production_intent(raw, ROOT)["intent"]
        self.assertEqual(intent["request"]["content_type"], "visual_loops")
        self.assertEqual(intent["family_adapter"]["target_gate"], "E4")
        self.assertIn("c11c-suite/c11c-producer/producer_schema.json", {
            row["path"] for row in intent["source_identity"]["source_pins"]
        })
        self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")

    def test_visual_drill_selection_is_resolved_and_source_identified(self):
        raw = request(request_id="C11E-E1-DRILL-001")
        raw["selection"] = {
            "content_type": "visual_drills",
            "family_id": "tracking",
            "variant_id": "tier-1",
        }
        intent = prepare_c11e_production_intent(raw, ROOT)["intent"]
        self.assertEqual(intent["request"]["content_type"], "visual_drills")
        self.assertEqual(intent["family_adapter"]["target_gate"], "E4")
        self.assertIn("c11c-suite/c11c-producer/producer_schema.json", {
            row["path"] for row in intent["source_identity"]["source_pins"]
        })
        self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")

    def test_title_changes_editorial_identity_not_seed_domains(self):
        first = prepare_c11e_production_intent(request(title="Title A"), ROOT)["intent"]
        second = prepare_c11e_production_intent(request(title="Title B"), ROOT)["intent"]
        self.assertNotEqual(first["identity"]["editorial_hash"], second["identity"]["editorial_hash"])
        self.assertNotEqual(first["identity"]["intent_hash"], second["identity"]["intent_hash"])
        self.assertEqual(first["seed_domains"], second["seed_domains"])

    def test_music_seed_is_independent_from_gameplay_seed(self):
        first = prepare_c11e_production_intent(request(seed=12345, music_seed=840001), ROOT)["intent"]
        second = prepare_c11e_production_intent(request(seed=12345, music_seed=840002), ROOT)["intent"]
        self.assertEqual(first["seed_domains"]["gameplay"]["value"], second["seed_domains"]["gameplay"]["value"])
        self.assertNotEqual(first["seed_domains"]["music"]["value"], second["seed_domains"]["music"]["value"])
        self.assertNotEqual(first["identity"]["request_hash"], second["identity"]["request_hash"])

    def test_gui_cli_origin_does_not_change_semantic_intent(self):
        raw = request()
        gui = prepare_c11e_production_intent(raw, ROOT, request_origin="GUI")["intent"]
        cli = prepare_c11e_production_intent(raw, ROOT, request_origin="CLI")["intent"]
        self.assertEqual(gui["request_origin"], "GUI")
        self.assertEqual(cli["request_origin"], "CLI")
        self.assertEqual(gui["identity"]["intent_hash"], cli["identity"]["intent_hash"])
        self.assertNotEqual(gui["intent_sha256"], cli["intent_sha256"])

    def test_service_is_side_effect_free(self):
        intent = prepare_c11e_production_intent(request(request_id="C11E-NO-WRITE-001"), ROOT)["intent"]
        planned = ROOT / intent["output"]["planned_root"]
        self.assertFalse(planned.exists(), "E1 preparation must not create production output directories")
        self.assertFalse(intent["output"]["created"])

    def test_existing_output_root_is_never_overwritten(self):
        with patch("c11e_production_service.Path.exists", return_value=True):
            with self.assertRaisesRegex(C11EProductionServiceError, "overwrite is forbidden"):
                prepare_c11e_production_intent(request(request_id="C11E-OUTPUT-COLLISION-001"), ROOT)

    def test_output_root_appearing_after_prepare_is_rejected(self):
        intent = prepare_c11e_production_intent(request(request_id="C11E-OUTPUT-RACE-001"), ROOT)["intent"]
        with patch("c11e_production_service.Path.exists", return_value=True):
            with self.assertRaisesRegex(C11EProductionServiceError, "appeared after preparation"):
                validate_c11e_production_intent(intent, ROOT)

    def test_invalid_origin_and_path_traversal_fail(self):
        with self.assertRaises(C11EProductionServiceError):
            prepare_c11e_production_intent(request(), ROOT, request_origin="ROOT")
        with self.assertRaises(C11EProductionServiceError):
            prepare_c11e_production_intent(request(request_id="../escape"), ROOT)

    def test_tampered_intent_fails_validation(self):
        intent = copy.deepcopy(prepare_c11e_production_intent(request(), ROOT)["intent"])
        intent["seed_domains"]["gameplay"]["value"] = 98765
        with self.assertRaises(C11EProductionServiceError):
            validate_c11e_production_intent(intent, ROOT)

    def test_longform_remains_rejected_by_canonical_resolver(self):
        raw = request()
        raw["selection"] = {"content_type": "longform"}
        with self.assertRaises(C11EProductionServiceError):
            prepare_c11e_production_intent(raw, ROOT)

    def test_cli_uses_the_same_service(self):
        with tempfile.TemporaryDirectory(prefix="c11e-e1-cli-") as temp:
            temp_root = Path(temp)
            request_path = temp_root / "request.json"
            output_path = temp_root / "intent.json"
            request_path.write_text(json.dumps(request()), encoding="utf-8")
            cli = ROOT / "c11c-suite" / "c11c-producer" / "c11e_production_cli.py"
            run = subprocess.run(
                [sys.executable, str(cli), "--request", str(request_path), "--origin", "CLI", "--output", str(output_path)],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=45,
            )
            self.assertEqual(run.returncode, 0, run.stdout + "\n" + run.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "PASS_E1_PREPARATION_ONLY")
            self.assertEqual(payload["intent"]["request_origin"], "CLI")
            self.assertEqual(payload["validation"]["status"], "PASS_E1_PREPARATION_ONLY")
            self.assertFalse(payload["execution_boundary"]["renderer_activation"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
