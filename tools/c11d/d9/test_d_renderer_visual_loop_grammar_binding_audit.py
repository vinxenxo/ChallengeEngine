from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent))
import d_renderer_visual_loop_grammar_binding_audit as audit  # noqa: E402


class VisualLoopGrammarBindingAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract, cls.schema, cls.receipt_schema = audit.load_and_validate_contract(ROOT)

    def _receipt(self) -> dict:
        contract = self.contract
        mapping = contract["grammar_binding"]
        return {
            "schema": "C11D-VISUAL-LOOP-GRAMMAR-BINDING-PROBE-RECEIPT-V1",
            "schema_version": "1.0",
            "status": "READ_ONLY_IN_MEMORY_PROTOTYPE_GRAMMAR_PARAMETER_PROBE",
            "selection": {
                "content_type": "visual_loops",
                "family_id": "c11c_geometric_waves_v1",
                "internal_family": "geometric",
                "subtype_id": "harmonic_membrane",
            },
            "mapping": {
                "environment_override": "C11C_VISUAL_GRAMMAR",
                "grammar_ids": mapping["prototype_grammar_ids"],
                "selected_grammar_id": "harmonic_membrane",
                "selected_grammar_index": 0,
                "selected_shader_branch": "field_harmonic_membrane",
                "style_parameter_count": 20,
            },
            "seed_cases": [
                {
                    "seed": seed,
                    "seed_profile_grammar_before_override": "orbital_wave" if seed % 2 else "interference_plane",
                    "bound_grammar_id": "harmonic_membrane",
                    "bound_grammar_index": 0,
                    "style_parameter_count": 20,
                    "style_sha256": hashlib.sha256(f"style-{seed}".encode()).hexdigest(),
                    "repeat_style_sha256": hashlib.sha256(f"style-{seed}".encode()).hexdigest(),
                    "deterministic_repeat": True,
                }
                for seed in mapping["runtime_seed_set"]
            ],
            "findings": {
                "prototype_override_source_pinned": True,
                "renderer_set_style_source_pinned": True,
                "shader_branch_source_pinned": True,
                "family_envelope_grammar_gap_remains": True,
                "seed_profile_changes_style_parameters": True,
                "selected_grammar_is_seed_independent": True,
                "exact_selector_payload_materialized": False,
            },
            "execution_boundary": {
                "probe_mode": "GODOT_HEADLESS_PROFILE_AND_SOURCE_PROBE_ONLY",
                "renderer_native_input_emitted": False,
                "renderer_instance_created": False,
                "renderer_dispatch_invoked": False,
                "shader_executed": False,
                "media_created": False,
                "disk_writes": False,
                "c11c_source_mutation": False,
                "candidate_input_admissible": False,
                "renderer": "OFF",
                "d4_8": "BLOCKED",
                "release_authority": "NONE",
                "d9_17": "BLOCKED_NO_GO",
                "d10": "BLOCKED",
            },
        }

    def test_contract_schema_and_lineage_are_strict_and_complete(self) -> None:
        self.assertEqual(self.contract["schema_version"], "1.0")
        self.assertEqual(len(self.contract["source_lineage"]), 13)
        self.assertEqual(self.contract["source_lineage"][0]["path"], audit.MANIFEST_REL.as_posix())
        self.assertEqual(self.contract["grammar_binding"]["style_parameter_count"], 20)

    def test_every_protected_c11c_source_matches_the_frozen_manifest(self) -> None:
        manifest = json.loads((ROOT / audit.MANIFEST_REL).read_text(encoding="utf-8"))
        frozen = {row["path"]: row["sha256"] for row in manifest["source_files"]}
        pins = {row["path"]: row["sha256"] for row in self.contract["source_lineage"]}
        for path in audit.PROTECTED_C11C_PATHS:
            self.assertIn(path, frozen)
            self.assertEqual(pins[path], frozen[path], path)

    def test_producer_prototype_profile_and_shader_share_the_same_grammar_order(self) -> None:
        source_findings = audit._static_source_audit(ROOT, self.contract)
        self.assertTrue(source_findings["producer_registry"])
        self.assertTrue(source_findings["prototype_override"])
        self.assertTrue(source_findings["seed_profile"])
        self.assertTrue(source_findings["profile_input_fields"])
        self.assertTrue(source_findings["renderer_style_signature"])
        self.assertTrue(source_findings["shader_branch"])

    def test_renderer_style_projection_has_all_twenty_ordered_parameters(self) -> None:
        self.assertEqual(self.contract["grammar_binding"]["style_parameter_order"], audit.EXPECTED_STYLE_ORDER)
        self.assertEqual(self.contract["grammar_binding"]["renderer_style_argument_order"], audit.EXPECTED_STYLE_ARGUMENT_ORDER)
        renderer = (ROOT / "tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd").read_text(encoding="utf-8-sig")
        self.assertIn('_material.set_shader_parameter("grammar_mode", clampi(grammar_mode, 0, 4))', renderer)

    def test_profile_input_keys_are_distinct_from_renderer_output_aliases(self) -> None:
        source = (ROOT / audit.HARNESS_REL).read_text(encoding="utf-8-sig")
        input_keys = audit._quoted_ids(
            source,
            r"const\s+PROFILE_INPUT_KEYS:\s*Array\[String\]\s*=\s*\[(.*?)\]",
            "probe source-profile input keys",
        )
        self.assertEqual(input_keys, audit.EXPECTED_PROFILE_INPUT_ORDER)
        self.assertEqual(len(input_keys), 20)
        self.assertIn('"glow_strength": clamp(float(value["glow"]), 0.0, 1.0)', source)
        self.assertIn("for key: String in PROFILE_INPUT_KEYS:", source)
        self.assertNotIn("for key: String in STYLE_KEYS:", source)
        self.assertIn("glow", input_keys)
        self.assertNotIn("glow_strength", input_keys)
        self.assertNotEqual(input_keys, audit.EXPECTED_STYLE_ORDER)

    def test_family_authoring_envelope_remains_truthfully_unresolved(self) -> None:
        scope = self.contract["truthful_limitations"]
        self.assertEqual(scope["d_authoring_envelope"], "FAMILY_LEVEL_GEOMETRIC_ONLY")
        self.assertIs(scope["exact_selector_payload_materialized"], False)
        dynamic = json.loads((ROOT / "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V1.json").read_text(encoding="utf-8"))
        loop = dynamic["supported_selector_matrix"]["visual_loops"]
        self.assertIs(loop["exact_selector_payload_materialized"], False)
        self.assertEqual(loop["payload_scope"], "VISUAL_LOOP_FAMILY_ENVELOPE_GRAMMAR_INSTANCE_UNRESOLVED")

    def test_read_only_godot_probe_does_not_instantiate_or_dispatch_renderer(self) -> None:
        source = (ROOT / audit.HARNESS_REL).read_text(encoding="utf-8")
        self.assertIn("C11CVariationProfileScript.build(\"geometric\", seed_value)", source)
        self.assertNotIn("GeometricWavesRenderer.new", source)
        self.assertNotIn("ShaderMaterial.new", source)
        self.assertNotIn("DirAccess.make_dir", source)
        self.assertNotIn("FileAccess.open", source)
        self.assertIn('"renderer_instance_created":false', source)
        self.assertIn('"exact_selector_payload_materialized":false', source)

    def test_godot_receipt_schema_accepts_a_valid_read_only_probe(self) -> None:
        audit.validate_runtime_receipt(self._receipt(), self.contract, self.receipt_schema)

    def test_receipt_rejects_seed_dependent_grammar_index(self) -> None:
        receipt = self._receipt()
        receipt["seed_cases"][2]["bound_grammar_index"] = 1
        with self.assertRaises(audit.GrammarAuditError):
            audit.validate_runtime_receipt(receipt, self.contract, self.receipt_schema)

    def test_receipt_rejects_visual_metadata_only_hash_changes(self) -> None:
        receipt = self._receipt()
        constant = "a" * 64
        for case in receipt["seed_cases"]:
            case["style_sha256"] = constant
            case["repeat_style_sha256"] = constant
        with self.assertRaises(audit.GrammarAuditError):
            audit.validate_runtime_receipt(receipt, self.contract, self.receipt_schema)

    def test_receipt_rejects_any_renderer_or_media_activation_claim(self) -> None:
        for key in ("renderer_native_input_emitted", "renderer_instance_created", "renderer_dispatch_invoked", "shader_executed", "media_created", "disk_writes", "c11c_source_mutation", "candidate_input_admissible"):
            receipt = self._receipt()
            receipt["execution_boundary"][key] = True
            with self.subTest(key=key), self.assertRaises(audit.GrammarAuditError):
                audit.validate_runtime_receipt(receipt, self.contract, self.receipt_schema)

    def test_source_drift_fails_closed_without_touching_checkout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="c11d-grammar-audit-") as tmp:
            target = Path(tmp)
            for rel in (audit.CONTRACT_REL, audit.CONTRACT_SCHEMA_REL, audit.RECEIPT_SCHEMA_REL):
                dest = target / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, dest)
            for row in self.contract["source_lineage"]:
                rel = Path(row["path"])
                dest = target / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    shutil.copy2(ROOT / rel, dest)
            shader = target / "tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader"
            original = shader.read_bytes()
            shader.write_bytes(original + b"\n// intentional negative test drift\n")
            with self.assertRaises(audit.GrammarAuditError):
                audit.load_and_validate_contract(target)
            self.assertEqual(shader.read_bytes(), original + b"\n// intentional negative test drift\n")

    def test_runner_parses_stdout_receipt_and_never_persists_it(self) -> None:
        receipt = self._receipt()
        result = SimpleNamespace(returncode=0, stdout=audit.EXPECTED_GODOT_VERSION + "\n", stderr="")
        probe = SimpleNamespace(returncode=0, stdout="C11D_GRAMMAR_PROBE_RECEIPT=" + json.dumps(receipt) + "\n", stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=[result, probe]) as subprocess_run:
            actual = audit.run_godot_probe(ROOT, "C:/Godot/Godot_v4.7.1-stable_win64_console.exe", 120)
        self.assertEqual(actual["schema"], receipt["schema"])
        self.assertEqual(subprocess_run.call_count, 2)
        command = subprocess_run.call_args_list[1].args[0]
        self.assertIn("--headless", command)
        self.assertIn("--script", command)
        self.assertFalse(any("output" in str(arg).lower() and str(arg).lower().endswith((".mp4", ".png", ".json")) for arg in command))

    def test_cli_requires_explicit_real_godot_and_probe_is_stdout_only(self) -> None:
        source = (ROOT / "tools/c11d/d9/d_renderer_visual_loop_grammar_binding_audit.py").read_text(encoding="utf-8")
        self.assertIn('parser.add_argument("--godot", required=True', source)
        self.assertIn("subprocess.run(command", source)
        self.assertNotIn("write_text(", source)
        self.assertNotIn("write_bytes(", source)
        self.assertNotIn("os.replace(", source)
        self.assertNotIn("ffmpeg", source.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
