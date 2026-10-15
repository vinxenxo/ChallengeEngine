from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import d_renderer_dynamic_request_payload_binding as binder  # noqa: E402
import d_renderer_visual_drill_seed_domain_audit as audit  # noqa: E402


class VisualDrillSeedDomainAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract, cls.schema, cls.pins = audit._load_and_validate_contract(ROOT)

    @staticmethod
    def _digest(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @classmethod
    def _fixture_matrices(cls):
        baseline = []
        gameplay_changed = []
        music_changed = []
        for family in binder.DRILL_V2_FAMILIES:
            for tier in binder.DRILL_V2_TIERS:
                key = f"{family}/{tier}"
                selection = {
                    "content_type": "visual_drills",
                    "family_id": family,
                    "subtype_id": None,
                    "variant_id": tier,
                }
                base_payload = cls._digest("base-payload-" + key)
                game_payload = cls._digest("game-payload-" + key)
                base_state = cls._digest("base-state-" + key)
                game_state = cls._digest("game-state-" + key)
                base_binding = cls._digest("base-binding-" + key)
                game_binding = cls._digest("game-binding-" + key)
                music_binding = cls._digest("music-binding-" + key)
                base_authoring = {"family_id": family, "tier": tier, "signature": cls._digest("authoring-" + key)}
                game_authoring = {"family_id": family, "tier": tier, "signature": cls._digest("changed-authoring-" + key)}

                def receipt(request_binding, gameplay_seed, music_seed, payload_sha, state_sha, authoring):
                    return {
                        "runtime_verification_status": "VERIFIED",
                        "runtime_repeat_evidence": {"status": "VERIFIED", "independent_runtime_executions": 2},
                        "request_identity": {
                            "request_id": "DRILL-SEED-" + key,
                            "content_type": "visual_drills",
                            "selection": copy.deepcopy(selection),
                            "gameplay_seed": gameplay_seed,
                            "music_seed": music_seed,
                            "variation_index": 0,
                            "presentation_profile_id": "social_vertical_v1",
                            "delivery_profile_id": "delivery_vertical_v1",
                            "request_binding_sha256": request_binding,
                        },
                        "source_identity": {"request_hash": cls._digest("canonical-request-" + key + str(gameplay_seed) + str(music_seed))},
                        "payload_evidence": {
                            "payload_sha256": payload_sha,
                            "visual_state_sha256": state_sha,
                            "exact_selector_payload_materialized": True,
                            "materialization": "IN_MEMORY_ONLY",
                            "visual_drill_authoring_evidence": copy.deepcopy(authoring),
                        },
                    }

                baseline.append(receipt(base_binding, audit.SEED_BASE, audit.MUSIC_SEED_BASE, base_payload, base_state, base_authoring))
                gameplay_changed.append(receipt(game_binding, audit.SEED_CHANGED, audit.MUSIC_SEED_BASE, game_payload, game_state, game_authoring))
                music_changed.append(receipt(music_binding, audit.SEED_BASE, audit.MUSIC_SEED_CHANGED, base_payload, base_state, base_authoring))
        return baseline, gameplay_changed, music_changed

    def test_contract_pins_all_v2_sources_and_reference_is_immutable(self):
        self.assertEqual(len(self.pins), 70)
        self.assertEqual(self.contract["source_pin_count"], 70)
        self.assertEqual(self.contract["source_of_truth"]["frozen_c11c_manifest_sha256"], audit.EXPECTED_MANIFEST_SHA256)
        self.assertEqual(audit._sha_file(ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"), audit.EXPECTED_MANIFEST_SHA256)
        self.assertEqual(self.contract["accepted_baseline_runtime_evidence"]["log_sha256"], "27a953d867169a3923049b07e0c3b0555867014ce8ecc51483342b222a777c53")

    def test_runtime_receipts_require_independent_repeat_evidence(self):
        baseline, gameplay, music = self._fixture_matrices()
        baseline[0]["runtime_repeat_evidence"]["status"] = "NOT_VERIFIED"
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "independent runtime repeat evidence"):
            audit.evaluate_seed_domain_relationships(baseline, gameplay, music)

    def test_request_id_must_remain_constant_across_seed_pairs(self):
        baseline, gameplay, music = self._fixture_matrices()
        gameplay[0]["request_identity"]["request_id"] = "MUTATED-REQUEST-ID"
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "Request identity field request_id drifted"):
            audit.evaluate_seed_domain_relationships(baseline, gameplay, music)

    def test_seed_request_variants_mutate_only_the_declared_seed_domain(self):
        base, game, music = audit.build_seed_experiment_requests(binder._visual_drill_matrix_raw_requests())
        self.assertEqual((20, 20, 20), (len(base), len(game), len(music)))
        for original, changed_game, changed_music in zip(base, game, music):
            self.assertEqual(original["request_id"], changed_game["request_id"])
            self.assertEqual(original["selection"], changed_game["selection"])
            self.assertEqual(original["request_id"], changed_music["request_id"])
            self.assertEqual(original["selection"], changed_music["selection"])
            self.assertNotEqual(original["seed"], changed_game["seed"])
            self.assertEqual(original["music_seed"], changed_game["music_seed"])
            self.assertEqual(original["seed"], changed_music["seed"])
            self.assertNotEqual(original["music_seed"], changed_music["music_seed"])
            self.assertEqual({"seed"}, {k for k in original if original[k] != changed_game[k]})
            self.assertEqual({"music_seed"}, {k for k in original if original[k] != changed_music[k]})

    def test_exact_twenty_selector_relationship_matrix_passes(self):
        baseline, gameplay, music = self._fixture_matrices()
        report = audit.evaluate_seed_domain_relationships(baseline, gameplay, music)
        self.assertEqual(report["cases"], 20)
        self.assertEqual(report["gameplay_seed_sensitivity"], {"passed": 20, "total": 20})
        self.assertEqual(report["music_seed_orthogonality"], {"passed": 20, "total": 20})
        self.assertFalse(report["seed_domains_complete_for_candidate_input"])
        self.assertEqual(len(report["per_selector"]), 20)

    def test_missing_selector_fails_closed(self):
        baseline, gameplay, music = self._fixture_matrices()
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "20 receipts"):
            audit.evaluate_seed_domain_relationships(baseline[:-1], gameplay, music)

    def test_duplicate_selector_fails_closed(self):
        baseline, gameplay, music = self._fixture_matrices()
        baseline[-1] = copy.deepcopy(baseline[0])
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "unknown/duplicate selector"):
            audit.evaluate_seed_domain_relationships(baseline, gameplay, music)

    def test_changed_gameplay_seed_must_change_visual_state(self):
        baseline, gameplay, music = self._fixture_matrices()
        gameplay[0]["payload_evidence"]["visual_state_sha256"] = baseline[0]["payload_evidence"]["visual_state_sha256"]
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "did not alter visual-state"):
            audit.evaluate_seed_domain_relationships(baseline, gameplay, music)

    def test_changed_gameplay_seed_must_change_payload(self):
        baseline, gameplay, music = self._fixture_matrices()
        gameplay[0]["payload_evidence"]["payload_sha256"] = baseline[0]["payload_evidence"]["payload_sha256"]
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "did not alter the selected visual payload"):
            audit.evaluate_seed_domain_relationships(baseline, gameplay, music)

    def test_music_seed_must_not_leak_into_visual_state_or_payload(self):
        baseline, gameplay, music = self._fixture_matrices()
        music[0]["payload_evidence"]["visual_state_sha256"] = self._digest("music-leak")
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "leaked into visual-state"):
            audit.evaluate_seed_domain_relationships(baseline, gameplay, music)
        baseline, gameplay, music = self._fixture_matrices()
        music[0]["payload_evidence"]["payload_sha256"] = self._digest("payload-music-leak")
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "leaked into the visual payload"):
            audit.evaluate_seed_domain_relationships(baseline, gameplay, music)

    def test_music_seed_change_must_change_canonical_request_identity(self):
        baseline, gameplay, music = self._fixture_matrices()
        music[0]["request_identity"]["request_binding_sha256"] = baseline[0]["request_identity"]["request_binding_sha256"]
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "not retained in request-binding identity"):
            audit.evaluate_seed_domain_relationships(baseline, gameplay, music)

    def test_report_schema_is_strict_and_summary_stays_fail_closed(self):
        baseline, gameplay, music = self._fixture_matrices()
        report = audit.evaluate_seed_domain_relationships(baseline, gameplay, music)
        report.update({
            "source_pin_count": 70,
            "godot_version": "4.7.1.stable.official",
            "frozen_c11c_manifest_sha256": audit.EXPECTED_MANIFEST_SHA256,
            "accepted_v2_runtime_log_sha256": "27a953d867169a3923049b07e0c3b0555867014ce8ecc51483342b222a777c53",
        })
        audit._validate_report_schema(report, self.schema)
        self.assertIs(self.schema.get("additionalProperties"), False)
        self.assertFalse(report["execution_boundary"]["renderer_input_emitted"])
        self.assertFalse(report["execution_boundary"]["media_created"])
        report["seed_domains_complete_for_candidate_input"] = True
        with self.assertRaises(Exception):
            audit._validate_report_schema(report, self.schema)

    def test_governance_boundary_is_not_a_render_path(self):
        source = (HERE / "d_renderer_visual_drill_seed_domain_audit.py").read_text(encoding="utf-8")
        self.assertNotIn("MovieWriter", source)
        self.assertNotIn("render_video(", source)
        self.assertNotIn("write_text(", source)
        self.assertNotIn("write_bytes(", source)
        self.assertIn('"renderer_activation": False', source)
        self.assertIn('"media_created": False', source)
        self.assertIn('"d4_8": "BLOCKED"', source)

    def test_missing_godot_executable_fails_closed_before_runtime(self):
        from io import StringIO
        from contextlib import redirect_stdout
        output = StringIO()
        with redirect_stdout(output):
            result = audit.main(["--godot", ""])
        self.assertEqual(result, 2)
        self.assertIn("Godot 4.7.1 executable missing", output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
