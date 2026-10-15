from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import test_d_renderer_dynamic_request_payload_binding as v1_test  # noqa: E402
import d_renderer_candidate_seed_domain_audit as audit  # noqa: E402


class CandidateCrossTypeSeedDomainAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract, cls.schema, cls.pins = audit._load_and_validate_contract(ROOT)
        cls.matrix = audit._collect_receipts(
            "C:\\Godot\\Godot_v4.7.1-stable_win64_console.exe", 120, ROOT,
            process_runner=v1_test._fake_process_runner,
        )

    @staticmethod
    def _digest(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def _clone_matrix(self):
        return deepcopy(self.matrix)

    def test_contract_pins_canonical_bindings_loop_and_challenge_sources(self):
        self.assertEqual(len(self.pins), 18)
        self.assertEqual(self.contract["source_pin_count"], 18)
        self.assertEqual(self.contract["source_of_truth"]["frozen_c11c_manifest_sha256"], audit.EXPECTED_MANIFEST_SHA256)
        self.assertEqual(audit._sha_file(ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"), audit.EXPECTED_MANIFEST_SHA256)
        self.assertIn("definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_V1.json", {p["path"] for p in self.pins})

    def test_planned_variants_mutate_only_the_declared_seed_domain(self):
        planned = audit._build_experiment_requests()
        self.assertEqual(set(planned), set(audit.CONTENT_TYPES))
        for content_type, variants in planned.items():
            baseline = variants["BASELINE"]
            game = variants["GAMEPLAY_SEED_ONLY_CHANGED"]
            music = variants["MUSIC_SEED_ONLY_CHANGED"]
            self.assertEqual(baseline["request_id"], game["request_id"])
            self.assertEqual(baseline["request_id"], music["request_id"])
            self.assertEqual(baseline["selection"], game["selection"])
            self.assertEqual(baseline["selection"], music["selection"])
            self.assertEqual({"seed"}, {k for k in baseline if baseline[k] != game.get(k)})
            self.assertEqual({"music_seed"}, {k for k in baseline if baseline[k] != music.get(k)})

    def test_two_selector_relationship_matrix_and_six_repeats_pass(self):
        report = audit.evaluate_seed_domain_relationships(self._clone_matrix(), len(self.pins))
        self.assertEqual(report["selectors"], 2)
        self.assertEqual(report["gameplay_seed_sensitivity"], {"passed": 2, "total": 2})
        self.assertEqual(report["music_seed_orthogonality"], {"passed": 2, "total": 2})
        self.assertEqual(report["independent_repeat_checks"], {"passed": 6, "total": 6})
        self.assertEqual(len(report["per_selector"]), 2)
        self.assertFalse(report["seed_domains_complete_for_candidate_input"])

    def test_missing_selector_variant_fails_closed(self):
        matrix = self._clone_matrix()
        del matrix["challenges"]["MUSIC_SEED_ONLY_CHANGED"]
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "Variant matrix incomplete"):
            audit.evaluate_seed_domain_relationships(matrix, len(self.pins))

    def test_independent_repeat_payload_drift_fails_closed(self):
        matrix = self._clone_matrix()
        matrix["challenges"]["BASELINE"][1]["payload_evidence"]["payload_sha256"] = self._digest("repeat-drift")
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "Independent repeat drifted in payload_sha256"):
            audit.evaluate_seed_domain_relationships(matrix, len(self.pins))

    def test_gameplay_seed_must_change_visual_payload_and_state(self):
        matrix = self._clone_matrix()
        base = matrix["challenges"]["BASELINE"][0]["payload_evidence"]
        game = matrix["challenges"]["GAMEPLAY_SEED_ONLY_CHANGED"][0]["payload_evidence"]
        for receipt in matrix["challenges"]["GAMEPLAY_SEED_ONLY_CHANGED"]:
            receipt["payload_evidence"]["payload_sha256"] = base["payload_sha256"]
            receipt["payload_evidence"]["visual_state_sha256"] = base["visual_state_sha256"]
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "Gameplay seed did not alter payload_sha256"):
            audit.evaluate_seed_domain_relationships(matrix, len(self.pins))

    def test_music_seed_must_not_leak_into_visual_payload(self):
        matrix = self._clone_matrix()
        matrix["visual_loops"]["MUSIC_SEED_ONLY_CHANGED"][0]["payload_evidence"]["payload_sha256"] = self._digest("music-leak")
        matrix["visual_loops"]["MUSIC_SEED_ONLY_CHANGED"][1]["payload_evidence"]["payload_sha256"] = self._digest("music-leak")
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "Music seed leaked into payload_sha256"):
            audit.evaluate_seed_domain_relationships(matrix, len(self.pins))

    def test_music_seed_must_change_request_binding_identity(self):
        matrix = self._clone_matrix()
        base_binding = matrix["challenges"]["BASELINE"][0]["request_identity"]["request_binding_sha256"]
        for receipt in matrix["challenges"]["MUSIC_SEED_ONLY_CHANGED"]:
            receipt["request_identity"]["request_binding_sha256"] = base_binding
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "Music seed not captured in request binding"):
            audit.evaluate_seed_domain_relationships(matrix, len(self.pins))

    def test_visual_loop_must_return_the_pinned_grammar_instance(self):
        matrix = self._clone_matrix()
        for variant in audit.VARIANTS:
            for receipt in matrix["visual_loops"][variant]:
                receipt["payload_evidence"]["grammar_parameter_evidence"]["grammar_id"] = "unapproved_grammar"
        with self.assertRaisesRegex(audit.SeedDomainAuditError, "pinned harmonic_membrane instance"):
            audit.evaluate_seed_domain_relationships(matrix, len(self.pins))

    def test_report_schema_is_strict_and_governance_stays_locked(self):
        report = audit.evaluate_seed_domain_relationships(self._clone_matrix(), len(self.pins))
        report["godot_version"] = "4.7.1.stable.official"
        report["accepted_visual_drill_seed_audit_contract_sha256"] = audit._sha_file(ROOT / audit.drill_audit.CONTRACT_REL)
        report["audit_sha256"] = audit._sha_json(report)
        audit._validate_report_schema(report, self.schema)
        self.assertFalse(report["execution_boundary"]["renderer_input_emitted"])
        self.assertFalse(report["execution_boundary"]["media_created"])
        self.assertEqual(report["execution_boundary"]["d4_8"], "BLOCKED")
        promoted = deepcopy(report)
        promoted["execution_boundary"]["renderer_activation"] = True
        with self.assertRaises(Exception):
            audit._validate_report_schema(promoted, self.schema)

    def test_tool_is_stdout_only_and_not_a_render_path(self):
        source = (HERE / "d_renderer_candidate_seed_domain_audit.py").read_text(encoding="utf-8")
        for forbidden in ("write_text(", "write_bytes(", "MovieWriter", "render_video(", "FileAccess.open("):
            self.assertNotIn(forbidden, source)
        self.assertIn('"renderer_activation": False', source)
        self.assertIn('"media_created": False', source)
        self.assertIn('"d4_8": "BLOCKED"', source)

    def test_missing_godot_executable_fails_closed(self):
        from io import StringIO
        from contextlib import redirect_stdout
        output = StringIO()
        with redirect_stdout(output):
            result = audit.main(["--godot", ""])
        self.assertEqual(result, 2)
        self.assertIn("Godot 4.7.1 executable missing", output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
