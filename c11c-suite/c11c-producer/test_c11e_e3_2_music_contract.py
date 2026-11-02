from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from c11e_production_service import (
    C11EProductionServiceError,
    _build_music_contract,
    prepare_c11e_production_intent,
    sha256,
    validate_c11e_production_intent,
)

ROOT = Path(__file__).resolve().parents[2]
ENGINE_PATH = ROOT / "tools" / "c11d" / "d3" / "c11d_music_engine_v5.py"
SPEC_PATH = ROOT / "definitions" / "c11d" / "music" / "C11D_MUSIC_ENGINE_V5_SPEC_V1.json"
PROFILE_PATH = ROOT / "definitions" / "c11d" / "music" / "C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json"


def request(*, content_type: str = "challenges", audio_enabled: bool = True, seed: int = 12345, music_seed: int = 840001, request_id: str = "C11E-E3-2-TEST-001") -> dict:
    selection = {"content_type": content_type, "variant_id": "CHALLENGE_001"}
    if content_type == "visual_loops":
        selection = {"content_type": content_type, "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane"}
    elif content_type == "visual_drills":
        selection = {"content_type": content_type, "family_id": "tracking", "variant_id": "tier-1"}
    return {
        "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "PRODUCTION",
        "selection": selection,
        "seed": seed,
        "music_seed": music_seed,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": audio_enabled,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": {"title": "E3.2 music contract test"},
        "provenance": {"source_revision": "C11E-E3.2-TEST", "request_origin": "TEST"},
    }


def load_engine():
    spec = importlib.util.spec_from_file_location("c11e_e3_2_music_engine_under_test", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load reviewed V5 engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class C11EE32MusicContractTests(unittest.TestCase):
    def test_challenge_music_binding_is_planned_but_not_dispatchable(self):
        intent = prepare_c11e_production_intent(request(), ROOT)["intent"]
        music = intent["music_contract"]
        self.assertEqual(music["status"], "PLANNED_NOT_RENDERED")
        self.assertEqual(music["route"], "D3_V5_CHALLENGE_8BIT_PLANNING_BINDING_ONLY")
        self.assertEqual(music["engine"]["engine_id"], "c11d_music_engine_v5")
        self.assertEqual(music["style_profile"]["profile_id"], "challenge_8bit_v1")
        self.assertEqual(music["engine_request"]["music_seed"], 840001)
        self.assertEqual(music["engine_request"]["variation_index"], 0)
        self.assertEqual(music["unresolved_engine_parameters"], ["tempo_bpm", "duration_seconds"])
        self.assertFalse(music["dispatchable"])
        self.assertFalse(music["engine_invoked"])
        self.assertFalse(music["audio_created"])
        self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")

    def test_audio_disabled_remains_disabled(self):
        intent = prepare_c11e_production_intent(request(audio_enabled=False, request_id="C11E-E3-2-DISABLED"), ROOT)["intent"]
        music = intent["music_contract"]
        self.assertEqual(music["status"], "DISABLED_BY_REQUEST")
        self.assertIsNone(music["engine_request"])
        self.assertFalse(music["engine_invoked"])
        self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")

    def test_loop_and_drill_paths_are_not_rewired_to_challenge_profile(self):
        for content_type in ("visual_loops", "visual_drills"):
            with self.subTest(content_type=content_type):
                intent = prepare_c11e_production_intent(request(content_type=content_type, request_id="C11E-E3-2-" + content_type.upper()), ROOT)["intent"]
                music = intent["music_contract"]
                self.assertEqual(music["status"], "PROTECTED_FAMILY_NOT_REWIRED")
                self.assertEqual(music["route"], "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH")
                self.assertIsNone(music["engine"])
                self.assertIsNone(music["style_profile"])
                self.assertFalse(music["engine_invoked"])
                pinned_paths = {row["path"] for row in intent["source_identity"]["source_pins"]}
                self.assertNotIn("tools/c11d/d3/c11d_music_engine_v5.py", pinned_paths)
                self.assertNotIn("definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json", pinned_paths)
                self.assertEqual(validate_c11e_production_intent(intent, ROOT)["status"], "PASS_E1_PREPARATION_ONLY")

    def test_protected_loop_drill_binding_does_not_require_v5_files(self):
        for content_type in ("visual_loops", "visual_drills"):
            with self.subTest(content_type=content_type), tempfile.TemporaryDirectory(prefix="c11e-e3-2-protected-") as temp:
                binding, pins = _build_music_contract(
                    Path(temp),
                    {
                        "selection": {"content_type": content_type},
                        "music_seed": 840001,
                        "variation_index": 0,
                        "audio_enabled": True,
                    },
                )
                self.assertEqual(binding["status"], "PROTECTED_FAMILY_NOT_REWIRED")
                self.assertEqual(pins, [])
                self.assertIsNone(binding["engine"])
                self.assertIsNone(binding["style_profile"])

    def test_music_contract_tampering_is_rejected_even_after_outer_reseal(self):
        intent = prepare_c11e_production_intent(request(request_id="C11E-E3-2-TAMPER"), ROOT)["intent"]
        intent["music_contract"]["engine_request"]["music_seed"] += 1
        unsigned = dict(intent)
        unsigned.pop("intent_sha256", None)
        intent["intent_sha256"] = sha256(unsigned)
        with self.assertRaisesRegex(C11EProductionServiceError, "music contract binding mismatch"):
            validate_c11e_production_intent(intent, ROOT)

    def test_v5_engine_repeats_identically_and_music_seed_changes_audio(self):
        engine = load_engine()
        spec = json.loads(SPEC_PATH.read_text(encoding="utf-8-sig"))
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8-sig"))
        base = {
            "music_seed": 840001,
            "style_profile_id": "challenge_8bit_v1",
            "style_profile_version": "1.0",
            "duration_seconds": 0.75,
            "tempo_bpm": 104,
            "variation_index": 0,
        }
        with tempfile.TemporaryDirectory(prefix="c11e-e3-2-v5-test-") as temp:
            root = Path(temp)
            a = root / "a.wav"
            b = root / "b.wav"
            c = root / "c.wav"
            result_a = engine.render(dict(base), spec, profile, a)
            result_b = engine.render(dict(base), spec, profile, b)
            other = dict(base)
            other["music_seed"] = 840002
            result_c = engine.render(other, spec, profile, c)
            self.assertEqual(result_a["output_hash"], result_b["output_hash"])
            self.assertNotEqual(result_a["output_hash"], result_c["output_hash"])
            self.assertEqual(result_a["parameter_hash"], result_b["parameter_hash"])
            self.assertEqual(result_a["style_profile_id"], "challenge_8bit_v1")
            self.assertEqual(result_a["style_profile_version"], "1.0")
            self.assertEqual(result_a["frame_count"], round(0.75 * engine.SR))
            self.assertTrue(all(p.is_file() for p in (a, b, c)))
            self.assertTrue(all(p.stat().st_size > 44 for p in (a, b, c)))

    def test_v5_normalizes_profile_id_and_version_from_declarative_profile(self):
        engine = load_engine()
        spec = json.loads(SPEC_PATH.read_text(encoding="utf-8-sig"))
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8-sig"))
        req = {"music_seed": 840001, "duration_seconds": 0.1, "tempo_bpm": 104, "variation_index": 0}
        with tempfile.TemporaryDirectory(prefix="c11e-e3-2-v5-alias-") as temp:
            result = engine.render(req, spec, profile, Path(temp) / "alias.wav")
            self.assertEqual(result["style_profile_id"], profile["profile_id"])
            self.assertEqual(result["style_profile_version"], profile["profile_version"])

    def test_v5_rejects_profile_identity_mismatch(self):
        engine = load_engine()
        spec = json.loads(SPEC_PATH.read_text(encoding="utf-8-sig"))
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8-sig"))
        req = {
            "music_seed": 840001,
            "style_profile_id": "different_profile",
            "style_profile_version": "1.0",
            "duration_seconds": 0.1,
            "tempo_bpm": 104,
            "variation_index": 0,
        }
        with tempfile.TemporaryDirectory(prefix="c11e-e3-2-v5-negative-") as temp:
            with self.assertRaisesRegex(ValueError, "style profile identity mismatch"):
                engine.render(req, spec, profile, Path(temp) / "must_not_exist.wav")
            self.assertFalse((Path(temp) / "must_not_exist.wav").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
