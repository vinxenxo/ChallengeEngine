from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "tools/c11d/d9/d_renderer_shared_editorial_presentation_inheritance.py"
SPEC = importlib.util.spec_from_file_location("shared_editorial_presentation_audit", MODULE_PATH)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(AUDIT)


class SharedEditorialPresentationInheritanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = AUDIT._read_json(ROOT, AUDIT.CONTRACT_PATH)

    def test_canonical_audit_passes_and_is_deterministic(self):
        first = AUDIT.audit(ROOT)
        second = AUDIT.audit(ROOT)
        self.assertEqual(first, second)
        self.assertEqual(first["checks_passed"], 14)
        self.assertEqual(first["source_pins_passed"], 8)
        self.assertEqual(first["shared_fields"], 4)
        self.assertEqual(first["challenge_only_fields"], 2)
        self.assertEqual(first["reserved_disabled_fields"], 12)

    def test_contract_schema_is_draft_2020_12_valid(self):
        import jsonschema
        schema = AUDIT._read_json(ROOT, AUDIT.SCHEMA_PATH)
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(self.contract)

    def test_shared_editorial_fields_match_canonical_d9_8_model(self):
        model = AUDIT._read_json(ROOT, "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
        fields = model["editorial_fields"]
        shared = [name for name, spec in fields.items() if spec.get("enabled") is True and all(t in spec.get("content_types", []) for t in AUDIT.SUPPORTED_TYPES)]
        self.assertEqual(shared, ["title", "subtitle", "call_to_action", "language"])
        self.assertEqual(self.contract["shared_editorial_layer"]["shared_enabled_fields"], shared)

    def test_language_is_metadata_not_display_text(self):
        layer = self.contract["shared_editorial_layer"]
        self.assertIn("language", layer["shared_metadata_fields"])
        self.assertNotIn("language", layer["shared_display_text_fields"])

    def test_challenge_specific_fields_do_not_leak_to_loops_or_drills(self):
        model = AUDIT._read_json(ROOT, "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
        for name in self.contract["shared_editorial_layer"]["challenge_only_enabled_fields"]:
            self.assertEqual(model["editorial_fields"][name]["content_types"], ["challenges"])

    def test_reserved_fields_stay_disabled(self):
        model = AUDIT._read_json(ROOT, "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
        for name in self.contract["shared_editorial_layer"]["reserved_disabled_fields"]:
            self.assertIs(model["editorial_fields"][name]["enabled"], False)

    def test_new_registered_family_inherits_shared_layers_by_default(self):
        registration = self.contract["new_family_registration"]
        self.assertIs(registration["shared_editorial_inheritance_default"], True)
        self.assertIs(registration["shared_presentation_inheritance_default"], True)
        self.assertTrue(registration["exception_free_registration_is_valid"])
        self.assertEqual(registration["unknown_family_before_registration"], "REJECT")

    def test_family_exception_requires_explicit_hash_bound_approved_record(self):
        policy = self.contract["family_exception_policy"]
        self.assertEqual(policy["active_exception_count"], 0)
        self.assertTrue(policy["exception_source_must_be_hash_bound"])
        self.assertTrue(policy["exception_must_be_explicitly_approved_before_activation"])
        self.assertFalse(policy["exception_may_enable_reserved_editorial_fields_without_separate_contract"])

    def test_presentation_geometry_is_not_approved_or_inferred(self):
        self.assertEqual(self.contract["shared_presentation_layer"]["profile_transport"], "REGISTERED_PROFILE_REFERENCE_ONLY")
        self.assertFalse(self.contract["shared_presentation_layer"]["semantic_region_mapping_approved"])
        self.assertFalse(self.contract["shared_presentation_layer"]["shared_presentation_region_policy_approved"])
        self.assertFalse(self.contract["shared_presentation_layer"]["coordinates_emitted"])

    def test_parameter_instance_does_not_claim_exact_loop_visual_payload(self):
        instance = AUDIT._read_json(ROOT, "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_PARAMETER_INSTANCE_V1.json")
        self.assertTrue(instance["materialization_semantics"]["exact_grammar_parameter_instance_materialized"])
        self.assertFalse(instance["materialization_semantics"]["exact_selector_visual_payload_materialized"])
        self.assertEqual(instance["materialization_semantics"]["family_authoring_envelope_grammar_gap"], "REMAINS_OPEN")

    def test_source_pin_mutation_fails_closed_without_touching_source_files(self):
        modified = copy.deepcopy(self.contract)
        modified["source_lineage"][1]["sha256"] = "0" * 64
        with self.assertRaises(AUDIT.AuditError):
            AUDIT.audit(ROOT, contract_override=modified)

    def test_contract_cannot_silently_enable_family_override(self):
        modified = copy.deepcopy(self.contract)
        modified["new_family_registration"]["silent_exception_allowed"] = True
        with self.assertRaises(AUDIT.AuditError):
            AUDIT.audit(ROOT, contract_override=modified)

    def test_contract_cannot_approve_presentation_geometry(self):
        modified = copy.deepcopy(self.contract)
        modified["shared_presentation_layer"]["shared_presentation_region_policy_approved"] = True
        with self.assertRaises(AUDIT.AuditError):
            AUDIT.audit(ROOT, contract_override=modified)

    def test_longform_and_unknown_selectors_remain_fail_closed(self):
        selection = self.contract["future_gui_selection_contract"]
        self.assertEqual(selection["longform"], "REJECT_UNTIL_CANONICAL_D_REQUEST_SUPPORTS_IT")
        self.assertEqual(selection["unknown_selection"], "REJECT")
        self.assertEqual(selection["silent_fallback"], "FORBIDDEN")

    def test_tool_is_stdout_only_and_governance_remains_locked(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("write_text(", source)
        self.assertNotIn("write_bytes(", source)
        self.assertNotIn("subprocess.run(", source)
        boundary = self.contract["execution_boundary"]
        self.assertEqual(boundary["renderer"], "OFF")
        self.assertFalse(boundary["renderer_dispatch_invoked"])
        self.assertFalse(boundary["media_created"])
        self.assertEqual(boundary["d4_8"], "BLOCKED")
        self.assertEqual(boundary["release_authority"], "NONE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
