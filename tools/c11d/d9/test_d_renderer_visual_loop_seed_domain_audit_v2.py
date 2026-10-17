from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("jsonschema is required for seed-domain V2 contract tests") from exc

ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = ROOT / "tools/c11d/d9/d_renderer_visual_loop_seed_domain_audit_v2.py"
SPEC = importlib.util.spec_from_file_location("_c11d_seed_domain_audit_v2_tests", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot load seed-domain V2 test target")
AUDIT = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def synthetic_matrix() -> list[dict]:
    rows = []
    for grammar, _index, _branch in AUDIT.GRAMMAR_MATRIX:
        selector_digest = _sha("selector:" + grammar)
        baseline_visual = {
            "style_parameters_sha256": _sha(grammar + ":style:12345"),
            "authoring_envelope_sha256": _sha(grammar + ":authoring:12345"),
            "family_variation_recipe_sha256": _sha(grammar + ":recipe:12345"),
            "resolved_palette_sha256": _sha(grammar + ":palette:12345"),
            "visual_spec_sha256": _sha(grammar + ":visual:12345"),
        }
        changed_gameplay_visual = {
            "style_parameters_sha256": _sha(grammar + ":style:54321"),
            "authoring_envelope_sha256": _sha(grammar + ":authoring:54321"),
            "family_variation_recipe_sha256": _sha(grammar + ":recipe:54321"),
            "resolved_palette_sha256": _sha(grammar + ":palette:54321"),
            "visual_spec_sha256": _sha(grammar + ":visual:54321"),
        }
        for variant in AUDIT.VARIANT_ROWS:
            variant_id = variant["variant_id"]
            gameplay_seed = variant["gameplay_seed"]
            music_seed = variant["music_seed"]
            if variant_id == "BASELINE":
                visual = baseline_visual
            elif variant_id == "GAMEPLAY_SEED_ONLY_CHANGED":
                visual = changed_gameplay_visual
            else:
                # Music changes request identity, not the gameplay-derived visual projection.
                visual = baseline_visual
            for repeat_index in (1, 2):
                request_hash = _sha(f"{grammar}:{variant_id}:request")
                plan_hash = _sha(f"{grammar}:{variant_id}:plan")
                rows.append({
                    "grammar_id": grammar,
                    "variant_id": variant_id,
                    "repeat_index": repeat_index,
                    "gameplay_seed": gameplay_seed,
                    "music_seed": music_seed,
                    "request_id": "D-GRAMMAR-CHAIN-GAP-" + grammar.upper(),
                    "request_hash": request_hash,
                    "plan_hash": plan_hash,
                    "editorial_hash": _sha(f"{grammar}:{variant_id}:editorial"),
                    "bridge_record_hash": _sha(f"{grammar}:{variant_id}:bridge"),
                    "adapter_envelope_hash": _sha(f"{grammar}:{variant_id}:adapter"),
                    "source_binding_sha256": _sha(f"{grammar}:{variant_id}:source"),
                    "request_parameter_binding_sha256": _sha(f"{grammar}:{variant_id}:binding"),
                    "style_parameters_sha256": visual["style_parameters_sha256"],
                    "parameter_instance_sha256": _sha(f"{grammar}:{variant_id}:parameter"),
                    "parent_binding_receipt_sha256": _sha(f"{grammar}:{variant_id}:parent"),
                    "authoring_envelope_sha256": visual["authoring_envelope_sha256"],
                    "family_variation_recipe_sha256": visual["family_variation_recipe_sha256"],
                    "resolved_palette_sha256": visual["resolved_palette_sha256"],
                    "visual_spec_sha256": visual["visual_spec_sha256"],
                    "payload_instance_sha256": _sha(f"{grammar}:{variant_id}:payload"),
                    "selector_policy_envelope_sha256": selector_digest,
                    "shared_policy_reference_set_sha256": _sha("shared-policy-set"),
                    "policy_reference_count": 9,
                    "policy_values_consumed": False,
                    "source_pins_verified": True,
                    "canonical_request_planned": True,
                    "parameter_instance_bound_in_memory": True,
                    "exact_selector_payload_materialized_in_memory": True,
                    "deterministic_repeat_pass": True,
                    "renderer_input_emitted": False,
                    "payload_file_written": False,
                    "candidate_input_admissible": False,
                    "renderer": "OFF",
                    "media_created": False,
                    "D4.8": "BLOCKED",
                    "release_authority": "NONE",
                })
    return rows


class VisualLoopSeedDomainAuditV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract, cls.schema, cls.report_schema, cls.lineage, *_ = AUDIT._load_contract(ROOT)

    def test_01_active_contract_and_direct_source_pins_validate(self):
        self.assertEqual(len(self.lineage), 70)
        self.assertEqual(self.lineage[0]["path"], "release/C11C_FREEZE_PACKAGE_MANIFEST.json")

    def test_02_contract_uses_strict_draft_2020_12(self):
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        Draft202012Validator.check_schema(self.schema)
        Draft202012Validator(self.schema).validate(self.contract)

    def test_03_report_schema_is_strict_and_valid(self):
        self.assertFalse(self.report_schema.get("additionalProperties", True))
        Draft202012Validator.check_schema(self.report_schema)

    def test_04_contract_keeps_automatic_seed_and_master_seed_disabled(self):
        self.assertFalse(self.contract["approval_state"]["automatic_seed_generation_approved"])
        self.assertFalse(self.contract["approval_state"]["master_seed_adopted"])
        self.assertFalse(self.contract["approval_state"]["seed_domains_complete_for_candidate_input"])

    def test_05_full_5x3x2_matrix_relationships_pass(self):
        result = AUDIT.evaluate_seed_domain_relationships(synthetic_matrix())
        self.assertEqual(result["selectors"], "5/5")
        self.assertEqual(result["seed_variant_chains"], "15/15")
        self.assertEqual(result["independent_repeat_pairs"], "15/15")
        self.assertEqual(result["gameplay_seed_sensitivity"], "5/5")
        self.assertEqual(result["music_seed_orthogonality"], "5/5")
        self.assertFalse(result["seed_domains_complete_for_candidate_input"])

    def test_06_incomplete_matrix_fails_closed(self):
        rows = synthetic_matrix()[:-1]
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_07_duplicate_repeat_index_fails_closed(self):
        rows = synthetic_matrix()
        rows[-1]["repeat_index"] = 1
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_08_gameplay_seed_mutation_must_change_visual_projection(self):
        rows = synthetic_matrix()
        for row in rows:
            if row["grammar_id"] == "harmonic_membrane" and row["variant_id"] == "GAMEPLAY_SEED_ONLY_CHANGED":
                row["visual_spec_sha256"] = next(x["visual_spec_sha256"] for x in rows if x["grammar_id"] == row["grammar_id"] and x["variant_id"] == "BASELINE")
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_09_music_seed_leak_into_visual_spec_fails_closed(self):
        rows = synthetic_matrix()
        base = next(x for x in rows if x["grammar_id"] == "interference_plane" and x["variant_id"] == "BASELINE")
        changed = next(x for x in rows if x["grammar_id"] == "interference_plane" and x["variant_id"] == "MUSIC_SEED_ONLY_CHANGED")
        changed["visual_spec_sha256"] = _sha("music leaked into visual spec")
        # Keep the independent repeat paired to the same bad result so the semantic guard is exercised.
        changed2 = next(x for x in rows if x["grammar_id"] == "interference_plane" and x["variant_id"] == "MUSIC_SEED_ONLY_CHANGED" and x["repeat_index"] == 2)
        changed2["visual_spec_sha256"] = changed["visual_spec_sha256"]
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_10_music_seed_must_change_request_identity(self):
        rows = synthetic_matrix()
        base = next(x for x in rows if x["grammar_id"] == "lattice_wave" and x["variant_id"] == "BASELINE")
        music_rows = [x for x in rows if x["grammar_id"] == "lattice_wave" and x["variant_id"] == "MUSIC_SEED_ONLY_CHANGED"]
        for row in music_rows:
            row["request_hash"] = base["request_hash"]
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_11_repeat_drift_fails_closed(self):
        rows = synthetic_matrix()
        row = next(x for x in rows if x["grammar_id"] == "orbital_wave" and x["variant_id"] == "BASELINE" and x["repeat_index"] == 2)
        row["payload_instance_sha256"] = _sha("drift")
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_12_policy_metadata_cannot_be_consumed(self):
        rows = synthetic_matrix()
        row = next(x for x in rows if x["grammar_id"] == "harmonic_membrane" and x["variant_id"] == "BASELINE")
        row["policy_values_consumed"] = True
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_13_renderer_input_or_candidate_admission_fails_closed(self):
        rows = synthetic_matrix()
        row = next(x for x in rows if x["grammar_id"] == "parametric_ribbon" and x["variant_id"] == "BASELINE")
        row["renderer_input_emitted"] = True
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_14_unknown_selector_fails_closed(self):
        rows = synthetic_matrix()
        rows[0]["grammar_id"] = "not_a_canonical_grammar"
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_15_malformed_digest_fails_closed(self):
        rows = synthetic_matrix()
        rows[0]["request_hash"] = "deadbeef"
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_16_source_receipt_missing_fails_closed(self):
        rows = synthetic_matrix()
        rows[0]["source_pins_verified"] = False
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)

    def test_17_same_full_payload_across_seed_variants_fails_closed(self):
        rows = synthetic_matrix()
        # Force a cross-variant full identity collision for a canonical grammar.
        base = next(x for x in rows if x["grammar_id"] == "orbital_wave" and x["variant_id"] == "BASELINE")
        changed = [x for x in rows if x["grammar_id"] == "orbital_wave" and x["variant_id"] == "MUSIC_SEED_ONLY_CHANGED"]
        for row in changed:
            row["payload_instance_sha256"] = base["payload_instance_sha256"]
        with self.assertRaises(AUDIT.SeedDomainAuditError):
            AUDIT.evaluate_seed_domain_relationships(rows)


if __name__ == "__main__":
    unittest.main(verbosity=2)
