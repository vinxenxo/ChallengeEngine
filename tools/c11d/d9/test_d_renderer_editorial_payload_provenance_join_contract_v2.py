import hashlib
import json
import re
import sys
import unittest
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parents[3]
OVERLAY_ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE
PROJECT_ROOT = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else HERE

CONTRACT_REL = "definitions/c11d/production/D_RENDERER_EDITORIAL_PAYLOAD_PROVENANCE_JOIN_CONTRACT_V2.json"
SCHEMA_REL = "definitions/c11d/production/D_RENDERER_EDITORIAL_PAYLOAD_PROVENANCE_JOIN_SCHEMA_V2.json"
RUNNER_REL = "tools/c11d/d9/d_renderer_editorial_payload_provenance_join_v2.py"
TEST_REL = "tools/c11d/d9/test_d_renderer_editorial_payload_provenance_join_contract_v2.py"

EXPECTED_PINS = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
    "definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json": "e008217bd57303b638e13329d21e5ae56ee3b4efef790566e3702c89ee41a83f",
    "tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding.py": "244426e8f742e221f1fbb6885103135bd01d202cb6c8b641f877bd089e81ab9d",
    "tools/c11d/d9/d_renderer_request_scoped_payload_binding.py": "3b3ced5f51309fff791a166109baebd37511b354b1704ae2e59a0b9aa4e6df8b",
    "tools/c11d/d9/d_renderer_visual_payload_materialization_preview.py": "cebe9b79c519675e61aa0d136ec08814e38eef91d3f55d19e9355929d677bfee",
    "tools/c11d/d9/d_renderer_editorial_field_consumption_audit.py": "7001098cec9239027784abfc20ed17024f5bb45993b20f308e1debfb7fd5b85a",
    "tools/c11d/d9/materialize_visual_payloads_in_memory.gd": "33c63c2f692ddf64a37d3e64a7be219c96df048059dcfded848ae9f3dada29a8",
    "tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd": "8f8e4c9be6170d48319b62512a1e1cdb40c4f126563deb3546dfd302b080179e",
    "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json": "2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json": "39f6f979a5d8b189cbb3a375b0c33ed7fdb3f2b9bc59fcb587f31a6c65ede5a6",
    "definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json": "4bb817b3d782b4f7c61d93a48df9c11766c78018b6c9e7ea43155cb96bda5229",
    "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json": "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc",
    "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json": "41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85",
    "definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json": "101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a",
    "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_V1.json": "8ccbb98f63f6e6041cf047ccff8cda2c0b4c4e1c7cb772017f7cb2851a0d99fe",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json": "dbd12b8e71f55223b29a479c93c7b4565b2fee3dfe0da54816900cf6da10d33b",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(root, relative):
    path = root.joinpath(*PurePosixPath(relative).parts)
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


class ProvenanceJoinContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load_json(OVERLAY_ROOT, CONTRACT_REL)
        cls.schema = load_json(OVERLAY_ROOT, SCHEMA_REL)

    def test_01_contract_has_exact_identity_and_preparation_status(self):
        self.assertEqual(
            "C11-D-D9-RENDERER-EDITORIAL-PAYLOAD-PROVENANCE-JOIN-CONTRACT-V2",
            self.contract["schema"],
        )
        self.assertEqual("1.0", self.contract["schema_version"])
        self.assertEqual(
            "PREPARATION_ONLY_IN_MEMORY_PROVENANCE_JOIN_NOT_RENDERER_INPUT",
            self.contract["status"],
        )

    def test_02_schema_declares_all_required_top_level_properties(self):
        self.assertEqual("object", self.schema["type"])
        self.assertEqual(16, self.schema["properties"]["source_pin_count"]["const"])
        self.assertEqual(
            set(self.schema["required"]),
            set(self.contract.keys()),
        )

    def test_03_contract_contains_exactly_16_unique_source_pins(self):
        pins = self.contract["source_pins"]
        self.assertEqual(16, self.contract["source_pin_count"])
        self.assertEqual(16, len(pins))
        paths = [pin["path"] for pin in pins]
        self.assertEqual(16, len(set(paths)))
        self.assertEqual(set(EXPECTED_PINS), set(paths))

    def test_04_all_pinned_sources_match_hash_and_size(self):
        for pin in self.contract["source_pins"]:
            path = PROJECT_ROOT.joinpath(*PurePosixPath(pin["path"]).parts)
            with self.subTest(path=pin["path"]):
                self.assertTrue(path.is_file())
                self.assertEqual(EXPECTED_PINS[pin["path"]], pin["sha256"])
                self.assertEqual(pin["sha256"], digest(path))
                self.assertEqual(pin["bytes"], path.stat().st_size)

    def test_05_editorial_field_cardinality_is_six_four_four(self):
        self.assertEqual(
            {
                "challenges": 6,
                "visual_loops": 4,
                "visual_drills": 4,
                "total": 14,
                "nonempty_visual_fields_in_pinned_fixture": 11,
                "language_metadata_fields": 3,
            },
            self.contract["editorial_field_cardinality"],
        )

    def test_06_expected_runtime_rows_match_three_payload_fixtures(self):
        rows = {row["content_type"]: row for row in self.contract["expected_payload_observations"]}
        self.assertEqual({"challenges", "visual_loops", "visual_drills"}, set(rows))
        self.assertEqual((900, 60, 420), (
            rows["challenges"]["observed_source_frame_count"],
            rows["challenges"]["observed_source_fps"],
            rows["challenges"]["challenge_game_frame_count"],
        ))
        self.assertEqual((600, 30, 20.0), (
            rows["visual_loops"]["observed_source_frame_count"],
            rows["visual_loops"]["observed_source_fps"],
            rows["visual_loops"]["observed_source_duration_seconds"],
        ))
        self.assertEqual((630, 30, 21.0), (
            rows["visual_drills"]["observed_source_frame_count"],
            rows["visual_drills"]["observed_source_fps"],
            rows["visual_drills"]["observed_source_duration_seconds"],
        ))

    def test_07_effective_delivery_frame_count_remains_unresolved(self):
        for row in self.contract["expected_payload_observations"]:
            with self.subTest(content_type=row["content_type"]):
                self.assertIsNone(row["effective_delivery_frame_count"])
                self.assertEqual(
                    "NOT_ESTABLISHED_TIMEBASE_POLICY_NOT_APPROVED",
                    row["delivery_frame_count_status"],
                )
                self.assertEqual("NOT_EVALUATED", row["visibility_window_status"])

    def test_08_challenge_payload_identity_quality_is_not_overstated(self):
        challenge = next(
            row for row in self.contract["expected_payload_observations"]
            if row["content_type"] == "challenges"
        )
        self.assertEqual(
            "DERIVED_RECEIPT_ALIAS_NOT_NATIVE_RUNTIME_INSTANCE_ID",
            challenge["payload_identity_quality"],
        )

    def test_09_challenge_phase_fields_are_separate_and_proposed(self):
        phase = self.contract["challenge_phase_namespace"]
        self.assertEqual(["hook", "reveal", "cta"], phase["field_ids"])
        self.assertTrue(phase["distinct_from_universal_D9_9_fields"])
        self.assertTrue(phase["empty_reveal_suppressed"])
        self.assertEqual("POLICY_FIXTURE_ONLY_NOT_EVALUATED", phase["range_state"])
        self.assertEqual([0, 90], phase["candidate_ranges"]["hook"])
        self.assertIsNone(phase["candidate_ranges"]["reveal"])
        self.assertEqual([390, 450], phase["candidate_ranges"]["cta"])

    def test_10_contract_does_not_store_raw_editorial_text_or_field_hashes(self):
        scope = self.contract["runtime_scope"]
        self.assertIs(scope["raw_editorial_values_persisted"], False)
        self.assertIs(scope["per_field_value_hashes_persisted"], False)
        serialized = json.dumps(self.contract, ensure_ascii=False)
        self.assertNotIn("¡SOLO EL 1%", serialized)
        self.assertNotIn("Continuar", serialized)
        self.assertNotIn("D10 request-scoped materialization review", serialized)

    def test_11_runtime_evidence_hashes_are_well_formed(self):
        evidence = self.contract["runtime_evidence"]
        self.assertEqual(20, evidence["previous_integration_tests_passed"])
        for key in (
            "previous_in_memory_receipt_sha256",
            "previous_in_memory_trace_sha256",
            "godot_executable_sha256",
        ):
            with self.subTest(key=key):
                self.assertRegex(evidence[key], r"^[0-9a-f]{64}$")

    def test_12_governance_and_execution_locks_remain_closed(self):
        boundary = self.contract["execution_boundary"]
        self.assertIsNone(boundary["effective_delivery_frame_count"])
        self.assertEqual(0, boundary["visibility_windows_evaluated"])
        self.assertEqual("OFF", boundary["renderer"])
        for key in (
            "persistent_receipt_written",
            "payload_files_written",
            "renderer_native_input_emitted",
            "renderer_dispatch_invoked",
            "renderer_activation",
            "production_execution",
            "media_created",
            "candidate_input_admissible",
        ):
            self.assertIs(boundary[key], False)
        approvals = self.contract["approval_state"]
        for key, value in approvals.items():
            if isinstance(value, bool):
                with self.subTest(key=key):
                    self.assertIs(value, False)
        self.assertEqual("BLOCKED_AS_REQUIRED", approvals["D9_14"])
        self.assertEqual("BLOCKED_AS_REQUIRED", approvals["D9_16"])
        self.assertEqual("BLOCKED_NO_GO", approvals["D9_17"])
        self.assertEqual("BLOCKED_FOR_PROMOTION", approvals["D10"])
        self.assertEqual("NONE", approvals["release_authority"])

    def test_13_runner_is_present_and_contains_the_contract_validation(self):
        runner = OVERLAY_ROOT.joinpath(*PurePosixPath(RUNNER_REL).parts)
        test_file = OVERLAY_ROOT.joinpath(*PurePosixPath(TEST_REL).parts)
        self.assertTrue(runner.is_file())
        self.assertTrue(test_file.is_file())
        source = runner.read_text(encoding="utf-8-sig")
        self.assertIn("load_join_contract()", source)
        self.assertIn("source_timeline", source)
        self.assertIn("effective_delivery_frame_count", source)

    def test_14_overlay_does_not_modify_the_frozen_manifest(self):
        manifest = PROJECT_ROOT.joinpath(*PurePosixPath("release/C11C_FREEZE_PACKAGE_MANIFEST.json").parts)
        self.assertEqual(EXPECTED_PINS["release/C11C_FREEZE_PACKAGE_MANIFEST.json"], digest(manifest))


if __name__ == "__main__":
    unittest.main(verbosity=2)