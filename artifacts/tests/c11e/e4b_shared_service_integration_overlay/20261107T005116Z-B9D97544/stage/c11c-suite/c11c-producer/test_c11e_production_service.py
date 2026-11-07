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
    sha256,
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

    def test_challenge_presentation_option_defaults_on_and_is_sealed(self):
        intent = prepare_c11e_production_intent(request(), ROOT)["intent"]
        self.assertEqual(intent["schema_version"], "1.1")
        self.assertEqual(intent["request"]["presentation_options"], {"show_hook_countdown": True})
        self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")

    def test_challenge_presentation_option_off_is_sealed_and_changes_intent_identity(self):
        raw = request(request_id="C11E-E1-CHALLENGE-VISIBILITY-OFF")
        raw["presentation_options"] = {"show_hook_countdown": False}
        intent = prepare_c11e_production_intent(raw, ROOT)["intent"]
        self.assertEqual(intent["request"]["presentation_options"], {"show_hook_countdown": False})
        self.assertNotEqual(
            intent["identity"]["intent_hash"],
            prepare_c11e_production_intent(request(), ROOT)["intent"]["identity"]["intent_hash"],
        )
        self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")

    def test_legacy_challenge_intent_without_visibility_option_remains_valid(self):
        intent = copy.deepcopy(prepare_c11e_production_intent(request(), ROOT)["intent"])
        intent["request"].pop("presentation_options")
        semantics = {
            "request_id": intent["request"]["request_id"],
            "mode": intent["request"]["mode"],
            "selection": intent["request"]["selection"],
            "request_hash": intent["identity"]["request_hash"],
            "editorial_hash": intent["identity"]["editorial_hash"],
            "plan_hash": intent["identity"]["plan_hash"],
            "gameplay_seed": intent["seed_domains"]["gameplay"]["value"],
            "music_seed": intent["seed_domains"]["music"]["value"],
            "delivery_profile_id": intent["delivery"]["resolved_profile_id"],
            "presentation_profile_id": intent["delivery"]["presentation_profile_id"],
            "audio_enabled": intent["delivery"]["audio_enabled"],
            "editorial": intent["editorial"],
            "music_contract": intent["music_contract"],
            "source_identity": intent["source_identity"],
            "output_root": intent["output"]["planned_root"],
        }
        intent["identity"]["intent_hash"] = sha256(semantics)
        intent.pop("intent_sha256")
        intent["intent_sha256"] = sha256(intent)
        self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")

    def test_challenge_presentation_option_rejects_invalid_shape_and_boolean_coercion(self):
        invalid_values = [
            {"show_hook_countdown": 0},
            {"show_hook_countdown": "false"},
            {"show_hook_countdown": False, "extra": True},
            [],
            None,
        ]
        for index, value in enumerate(invalid_values):
            raw = request(request_id=f"C11E-E1-CHALLENGE-VISIBILITY-NEG-{index}")
            raw["presentation_options"] = value
            with self.subTest(value=value), self.assertRaises(C11EProductionServiceError):
                prepare_c11e_production_intent(raw, ROOT)

    def test_challenge_presentation_option_is_rejected_for_loop_and_drill(self):
        for content_type, selection in (
            ("visual_loops", {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane"}),
            ("visual_drills", {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"}),
        ):
            raw = request(request_id=f"C11E-E1-{content_type.upper()}-VISIBILITY-NEG")
            raw["selection"] = selection
            raw["presentation_options"] = {"show_hook_countdown": False}
            with self.subTest(content_type=content_type), self.assertRaises(C11EProductionServiceError):
                prepare_c11e_production_intent(raw, ROOT)

    def test_loop_and_drill_intents_keep_the_pre_e4a1_request_shape(self):
        for content_type, selection in (
            ("visual_loops", {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane"}),
            ("visual_drills", {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"}),
        ):
            raw = request(request_id=f"C11E-E1-{content_type.upper()}-NO-VISIBILITY-OPTION")
            raw["selection"] = selection
            intent = prepare_c11e_production_intent(raw, ROOT)["intent"]
            self.assertNotIn("presentation_options", intent["request"])
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
        raw["presentation_options"] = {"show_hook_countdown": False}
        gui = prepare_c11e_production_intent(raw, ROOT, request_origin="GUI")["intent"]
        cli = prepare_c11e_production_intent(raw, ROOT, request_origin="CLI")["intent"]
        self.assertEqual(gui["request_origin"], "GUI")
        self.assertEqual(cli["request_origin"], "CLI")
        self.assertEqual(gui["identity"]["intent_hash"], cli["identity"]["intent_hash"])
        self.assertEqual(gui["request"]["presentation_options"], cli["request"]["presentation_options"])
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
            cli_request = request()
            cli_request["presentation_options"] = {"show_hook_countdown": False}
            request_path.write_text(json.dumps(cli_request), encoding="utf-8")
            cli = ROOT / "c11c-suite" / "c11c-producer" / "c11e_production_cli.py"
            run = subprocess.run(
                [sys.executable, str(cli), "--request", str(request_path), "--origin", "CLI", "--output", str(output_path)],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=45,
            )
            self.assertEqual(run.returncode, 0, run.stdout + "\n" + run.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "PASS_E1_PREPARATION_ONLY")
            self.assertEqual(payload["intent"]["request_origin"], "CLI")
            self.assertEqual(payload["intent"]["request"]["presentation_options"], {"show_hook_countdown": False})
            self.assertEqual(payload["validation"]["status"], "PASS_E1_PREPARATION_ONLY")
            self.assertFalse(payload["execution_boundary"]["renderer_activation"])


    @staticmethod
    def loop_request(*, family_id: str = "c11c_geometric_waves_v1", grammar_id: str = "harmonic_membrane", seed: int = 12345, music_seed: int = 840001, request_id: str = "C11E-E4B-SHARED-LOOP-001") -> dict:
        raw = request(seed=seed, music_seed=music_seed, request_id=request_id)
        raw["mode"] = "PRODUCTION"
        raw["selection"] = {
            "content_type": "visual_loops",
            "family_id": family_id,
            "subtype_id": grammar_id,
        }
        raw["production_override"] = {
            "title": "E4B shared service",
            "subtitle": "UNKNOWN",
            "call_to_action": "Continue",
            "language": "en",
        }
        return raw

    def test_loop_shared_service_prepares_existing_d_boundary_and_keeps_locks(self):
        intent = prepare_c11e_production_intent(self.loop_request(), ROOT, request_origin="GUI")["intent"]
        self.assertEqual(intent["schema_version"], "1.2")
        self.assertEqual(intent["status"], "PREPARED_E1_NOT_DISPATCHED")
        preparation = intent["d9_boundary_preparation"]
        self.assertEqual(preparation["status"], "LOOP_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE")
        self.assertEqual(preparation["bridge_planning_record"]["status"], "PLANNING_ONLY_NOT_RENDERABLE")
        stage = preparation["loop_family_stage_contract"]
        self.assertEqual(stage["status"], "FAMILY_BOUND_PREPARATION_NOT_DISPATCHABLE")
        self.assertEqual(stage["governance"]["d4_8"], "BLOCKED")
        self.assertEqual(stage["governance"]["d9_10"], "PREPARE_ONLY")
        self.assertFalse(stage["governance"]["renderer_native_input_emitted"])
        self.assertFalse(stage["governance"]["renderer_dispatch_invoked"])
        self.assertFalse(stage["governance"]["launcher_invoked"])
        self.assertFalse(stage["governance"]["media_created"])
        self.assertEqual(intent["family_adapter"]["status"], "NOT_CONNECTED_E1")
        self.assertTrue({
            "tools/c11d/d9/editorial_render_bridge.py",
            "tools/c11d/d9/d_render_adapter.py",
            "tools/c11d/d9/c11e_e4b_loop_family_stage_contract.py",
        }.issubset({row["path"] for row in intent["source_identity"]["source_pins"]}))
        self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")

    def test_all_27_loop_grammars_prepare_through_the_shared_e_service(self):
        schema = json.loads((ROOT / "c11c-suite" / "c11c-producer" / "producer_schema.json").read_text(encoding="utf-8-sig"))
        prepared_count = 0
        family_counts = {}
        for family_id, family in sorted(schema["families"].items()):
            for grammar in family["grammars"]:
                grammar_id = grammar[0]
                if grammar_id == "auto":
                    continue
                serial = prepared_count + 1
                raw = self.loop_request(
                    family_id=family_id,
                    grammar_id=grammar_id,
                    seed=100000 + serial,
                    music_seed=500000 + serial,
                    request_id=f"C11E-E4B-SHARED-{serial:02d}",
                )
                intent = prepare_c11e_production_intent(raw, ROOT, request_origin="TEST")["intent"]
                self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")
                stage = intent["d9_boundary_preparation"]["loop_family_stage_contract"]
                self.assertEqual(stage["content_identity"]["family_id"], family_id)
                self.assertEqual(stage["content_identity"]["grammar_id"], grammar_id)
                visual = stage["family_visual_stage"]
                args = visual["argument_vector"]
                self.assertIn("-NoSound", args)
                self.assertIn(str(raw["seed"]), args)
                self.assertNotIn(str(raw["music_seed"]), args)
                self.assertFalse(visual["music_seed_passed_to_visual_launcher"])
                self.assertFalse(visual["launcher_execution"])
                self.assertTrue(stage["composition"]["materialized_payload_receipt_required"])
                self.assertFalse(stage["governance"]["renderer_native_input_emitted"])
                self.assertFalse(stage["governance"]["media_created"])
                self.assertEqual(stage["governance"]["d4_8"], "BLOCKED")
                family_counts[family_id] = family_counts.get(family_id, 0) + 1
                prepared_count += 1
        self.assertEqual(prepared_count, 27)
        self.assertEqual(sorted(family_counts.values()), [5, 5, 5, 5, 7])

    def test_loop_shared_boundary_is_repeatable_and_gui_cli_semantics_match(self):
        raw = self.loop_request(request_id="C11E-E4B-REPEATABLE-001")
        gui = prepare_c11e_production_intent(raw, ROOT, request_origin="GUI")["intent"]
        cli = prepare_c11e_production_intent(raw, ROOT, request_origin="CLI")["intent"]
        repeat = prepare_c11e_production_intent(raw, ROOT, request_origin="GUI")["intent"]
        self.assertEqual(gui["d9_boundary_preparation"], cli["d9_boundary_preparation"])
        self.assertEqual(gui["d9_boundary_preparation"], repeat["d9_boundary_preparation"])
        self.assertEqual(gui["identity"]["intent_hash"], cli["identity"]["intent_hash"])
        self.assertNotEqual(gui["intent_sha256"], cli["intent_sha256"])

    def test_loop_shared_boundary_tampering_fails_closed(self):
        intent = copy.deepcopy(prepare_c11e_production_intent(self.loop_request(request_id="C11E-E4B-TAMPER-001"), ROOT)["intent"])
        intent["d9_boundary_preparation"]["loop_family_stage_contract"]["family_visual_stage"]["argument_vector"].append("-Sound")
        with self.assertRaises(C11EProductionServiceError):
            validate_c11e_production_intent(intent, ROOT)

    def test_cli_loop_request_emits_the_same_shared_boundary_contract(self):
        with tempfile.TemporaryDirectory(prefix="c11e-e4b-loop-cli-") as temp:
            temp_root = Path(temp)
            request_path = temp_root / "request.json"
            output_path = temp_root / "intent.json"
            request_path.write_text(json.dumps(self.loop_request(request_id="C11E-E4B-CLI-LOOP-001")), encoding="utf-8")
            cli = ROOT / "c11c-suite" / "c11c-producer" / "c11e_production_cli.py"
            run = subprocess.run(
                [sys.executable, str(cli), "--request", str(request_path), "--origin", "CLI", "--output", str(output_path)],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=45,
            )
            self.assertEqual(run.returncode, 0, run.stdout + "\n" + run.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "PASS_E1_PREPARATION_ONLY")
            self.assertEqual(payload["intent"]["request_origin"], "CLI")
            self.assertEqual(payload["intent"]["d9_boundary_preparation"]["status"], "LOOP_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE")
            self.assertEqual(payload["intent"]["d9_boundary_preparation"]["loop_family_stage_contract"]["status"], "FAMILY_BOUND_PREPARATION_NOT_DISPATCHABLE")
            self.assertEqual(payload["validation"]["status"], "PASS_E1_PREPARATION_ONLY")
            self.assertFalse(payload["execution_boundary"]["renderer_activation"])

    def test_gui_uses_shared_loop_boundary_contract_instead_of_rebuilding_it(self):
        gui_source = (ROOT / "c11c-suite" / "c11c-producer" / "main.py").read_text(encoding="utf-8-sig")
        self.assertIn('d9_boundary_preparation = e1_intent.get("d9_boundary_preparation")', gui_source)
        self.assertIn('"loop_boundary_preparation_equal": e1_intent.get("d9_boundary_preparation") == e_cli_intent.get("d9_boundary_preparation")', gui_source)
        self.assertIn('write_json(run_root / "loop_family_stage_contract.json", loop_family_stage_contract)', gui_source)



if __name__ == "__main__":
    unittest.main(verbosity=2)
