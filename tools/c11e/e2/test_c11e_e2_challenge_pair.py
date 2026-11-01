from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

from c11e_e2_challenge_pair import (  # noqa: E402
    EXPECTED_CHALLENGE_ID,
    EXPECTED_MANIFEST_SHA256,
    E2PairError,
    build_effective_challenge_config,
    build_editorial_sidecar,
    build_raw_request,
    resolve_intent_pair,
)


class C11EE2ChallengePairTests(unittest.TestCase):
    def test_01_d99_e1_pair_resolves_same_request_except_title(self) -> None:
        request_id = "C11E-E2-UNIT-PAIR-20261030"
        pair = resolve_intent_pair(ROOT, request_id, 193847, 840001, "TITLE A", "TITLE B")
        a = pair[0]["prepared"]["intent"]
        b = pair[1]["prepared"]["intent"]
        self.assertEqual(a["request"], b["request"])
        self.assertEqual(a["seed_domains"], b["seed_domains"])
        self.assertEqual(a["source_identity"], b["source_identity"])
        self.assertNotEqual(a["editorial"]["title"], b["editorial"]["title"])
        for key in ("request_hash", "editorial_hash", "plan_hash", "intent_hash"):
            self.assertNotEqual(a["identity"][key], b["identity"][key])
        self.assertEqual(pair[0]["validation"]["status"], "PASS_E1_PREPARATION_ONLY")
        self.assertEqual(pair[1]["validation"]["status"], "PASS_E1_PREPARATION_ONLY")
        self.assertFalse((ROOT / a["output"]["planned_root"]).exists())

    def test_02_requests_differ_only_in_title(self) -> None:
        a = build_raw_request("C11E-E2-RAW-PAIR", 193847, 840001, "TITLE A")
        b = build_raw_request("C11E-E2-RAW-PAIR", 193847, 840001, "TITLE B")
        self.assertEqual(a.keys(), b.keys())
        for key in a:
            if key == "production_override":
                self.assertEqual(set(a[key]), set(b[key]))
                self.assertEqual({k: v for k, v in a[key].items() if k != "title"}, {k: v for k, v in b[key].items() if k != "title"})
                self.assertNotEqual(a[key]["title"], b[key]["title"])
            else:
                self.assertEqual(a[key], b[key], key)

    def test_03_effective_config_changes_only_gameplay_seed(self) -> None:
        source = json.loads((ROOT / "challenges" / f"{EXPECTED_CHALLENGE_ID}.json").read_text(encoding="utf-8-sig"))
        a = build_effective_challenge_config(source, 193847)
        b = build_effective_challenge_config(source, 193847)
        self.assertEqual(a, b)
        self.assertEqual(a["generation"]["seed"], 193847)
        self.assertEqual(a["content"], source["content"])
        self.assertEqual(source["generation"]["seed"], 193847)

    def test_04_sidecar_has_own_header_title_slot_and_no_hook_mapping(self) -> None:
        pair = resolve_intent_pair(ROOT, "C11E-E2-SIDECAR-UNIT", 193847, 840001, "TITLE A", "TITLE B")
        intent = pair[0]["prepared"]["intent"]
        sidecar = build_editorial_sidecar(intent, "a" * 64, "b" * 64)
        self.assertEqual(sidecar["schema"], "C11E-CHALLENGE-EDITORIAL-SIDECAR-V1")
        self.assertEqual(sidecar["visual_target"]["slot_id"], "header.editorial_title")
        self.assertEqual(sidecar["visual_target"]["region"], "HEADER")
        self.assertEqual(sidecar["visual_target"]["bounds_logical_540x960"], {"x": 24, "y": 24, "width": 496, "height": 104})
        self.assertEqual(sidecar["visual_target"]["visibility"], "ALL_CHALLENGE_FRAMES")
        self.assertEqual(sidecar["visual_target"]["semantic_separation"], "TITLE_IS_NOT_HOOK_CTA_OR_GAMEPLAY")
        self.assertEqual(sidecar["source_identity"]["c11c_manifest_sha256"], EXPECTED_MANIFEST_SHA256)
        self.assertFalse(sidecar["execution_boundary"]["audio_enabled"])

    def test_05_reject_equal_titles(self) -> None:
        with self.assertRaises(E2PairError):
            resolve_intent_pair(ROOT, "C11E-E2-REJECT-EQUAL", 193847, 840001, "SAME", "SAME")

    def test_06_reject_empty_and_control_character_titles(self) -> None:
        with self.assertRaises(E2PairError):
            build_raw_request("C11E-E2-REJECT-EMPTY", 193847, 840001, "  ")
        with self.assertRaises(E2PairError):
            build_raw_request("C11E-E2-REJECT-CONTROL", 193847, 840001, "BAD\nTITLE")

    def test_07_reject_seed_domain_type_and_range_errors(self) -> None:
        for seed, music_seed in ((True, 840001), (0, 840001), (193847, False), (193847, 2147483647)):
            with self.subTest(seed=seed, music_seed=music_seed):
                with self.assertRaises(E2PairError):
                    build_raw_request("C11E-E2-REJECT-SEED", seed, music_seed, "TITLE")

    def test_08_reject_non_challenge_source_config(self) -> None:
        with self.assertRaises(E2PairError):
            build_effective_challenge_config({"challenge_id": "CHALLENGE_005", "generation": {"seed": 1}}, 193847)

    def test_09_godot_scene_inherits_main_and_adds_no_c_source_edits(self) -> None:
        scene = (HERE / "C11EChallenge001E2.tscn").read_text(encoding="utf-8")
        script = (HERE / "C11EChallenge001E2.gd").read_text(encoding="utf-8")
        validator = (HERE / "C11EE2SidecarValidator.gd").read_text(encoding="utf-8")
        self.assertIn('res://Main.tscn', scene)
        self.assertIn('res://tools/c11e/e2/C11EChallenge001E2.gd', scene)
        self.assertIn('extends "res://GeneradorMaestro.gd"', script)
        self.assertIn('super._ready()', script)
        self.assertIn('header.editorial_title', script)
        # V9 moved semantic sidecar enforcement into the shared validator.
        # Assert the production scene delegates to it instead of requiring
        # the semantic marker to be duplicated in the scene source text.
        self.assertIn('C11EE2SidecarValidatorScript.validate(sidecar)', script)
        self.assertIn('visual.get("semantic_separation") != "TITLE_IS_NOT_HOOK_CTA_OR_GAMEPLAY"', validator)
        self.assertIn('str(_c11e_sidecar["editorial"]["title"])', script)
        self.assertNotIn('ChallengePresentationBinder.gd', script)
        self.assertNotIn('SimulationResult', script)
        self.assertNotIn('FrameSnapshot', script)


if __name__ == "__main__":
    result = unittest.main(verbosity=2)
