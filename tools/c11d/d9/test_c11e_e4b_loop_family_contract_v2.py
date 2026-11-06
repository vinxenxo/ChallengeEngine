from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = Path(os.environ.get("C11E_PROJECT_ROOT", HERE.parents[3])).resolve()
if str(PROJECT_ROOT / "tools" / "c11d" / "d9") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "tools" / "c11d" / "d9"))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import universal_producer
import editorial_render_bridge
import c11e_e4b_loop_family_stage_contract as family_contract
import c11e_e4b_loop_family_contract_audit_v2 as contract_audit_v2


class E4BLoopFamilyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((PROJECT_ROOT / "c11c-suite/c11c-producer/producer_schema.json").read_text(encoding="utf-8-sig"))
        cls.cases = []
        serial = 0
        for family_id, family in cls.schema["families"].items():
            for item in family.get("grammars", []):
                grammar_id = item[0]
                if grammar_id == "auto":
                    continue
                serial += 1
                raw = {
                    "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
                    "schema_version": "1.0",
                    "request_id": f"E4B_CONTRACT_{serial:02d}",
                    "mode": "REVIEW",
                    "selection": {"content_type": "visual_loops", "family_id": family_id, "subtype_id": grammar_id},
                    "seed": 100000 + serial,
                    "music_seed": 500000 + serial,
                    "delivery_profile_id": "REVIEW_720",
                    "presentation_profile_id": "UNKNOWN",
                    "variation_index": 0,
                    "audio_enabled": True,
                    "personalization_enabled": True,
                    "editorial_profile": {},
                    "production_override": {
                        "title": f"Loop title {serial}",
                        "subtitle": "UNKNOWN",
                        "call_to_action": "Continue",
                        "language": "en",
                    },
                    "provenance": {"request_origin": "TEST"},
                }
                result = universal_producer.evaluate_universal_request(raw, PROJECT_ROOT)
                bridge = editorial_render_bridge.build_bridge_planning_record(result, PROJECT_ROOT)
                contract = family_contract.build_loop_family_stage_contract(result, bridge, PROJECT_ROOT)
                cls.cases.append((family_id, grammar_id, result, bridge, contract))

    def test_all_27_grammars_build_a_family_bound_contract(self):
        self.assertEqual(len(self.cases), 27)
        counts = {}
        for family_id, grammar_id, result, bridge, contract in self.cases:
            counts[family_id] = counts.get(family_id, 0) + 1
            self.assertEqual(contract["status"], "FAMILY_BOUND_PREPARATION_NOT_DISPATCHABLE")
            self.assertEqual(contract["content_identity"]["family_id"], family_id)
            self.assertEqual(contract["content_identity"]["grammar_id"], grammar_id)
            self.assertEqual(contract["family_visual_stage"]["audio_switch"], "-NoSound")
            self.assertTrue(family_contract.validate_loop_family_stage_contract(contract))
        self.assertEqual(sorted(counts.values()), [5, 5, 5, 5, 7])

    def test_family_launcher_uses_gameplay_seed_only(self):
        for _family, _grammar, result, _bridge, contract in self.cases:
            args = contract["family_visual_stage"]["argument_vector"]
            self.assertIn(str(result["canonical_request"]["seed"]), args)
            self.assertNotIn(str(result["canonical_request"]["music_seed"]), args)
            self.assertFalse(contract["family_visual_stage"]["music_seed_passed_to_visual_launcher"])
            self.assertEqual(contract["family_visual_stage"]["music_seed"], result["canonical_request"]["music_seed"])

    def test_unknown_editorial_fields_suppress_composition(self):
        _family, _grammar, result, bridge, _contract = self.cases[0]
        raw = dict(result["canonical_request"])
        raw["request_id"] = "E4B_UNKNOWN_ONLY"
        raw["production_override"] = {}
        # Build an equivalent canonical request with every visible field unresolved.
        raw_request = {
            "schema": raw["schema"], "schema_version": raw["schema_version"],
            "request_id": raw["request_id"], "mode": raw["mode"],
            "selection": {key: raw["selection"][key] for key in ("content_type", "family_id", "subtype_id", "variant_id") if key in raw["selection"]}, "seed": raw["seed"], "music_seed": raw["music_seed"],
            "delivery_profile_id": raw["delivery_profile_id"], "presentation_profile_id": raw["presentation_profile_id"],
            "variation_index": raw["variation_index"], "audio_enabled": raw["audio_enabled"],
            "personalization_enabled": raw["personalization_enabled"], "editorial_profile": {},
            "production_override": {}, "provenance": {"request_origin": "TEST"},
        }
        planned = universal_producer.evaluate_universal_request(raw_request, PROJECT_ROOT)
        bridge_record = editorial_render_bridge.build_bridge_planning_record(planned, PROJECT_ROOT)
        prepared = family_contract.build_loop_family_stage_contract(planned, bridge_record, PROJECT_ROOT)
        self.assertEqual(prepared["editorial"]["visible_visual_field_count"], 0)
        self.assertEqual(prepared["editorial"]["activation"], "UNCHANGED_FULL_FRAME_PASSTHROUGH")
        self.assertTrue(all(item["visibility_window"] is None for item in prepared["editorial"]["fields"]))

    def test_contract_hash_detects_tampering(self):
        contract = json.loads(json.dumps(self.cases[0][4]))
        contract["family_visual_stage"]["music_seed_passed_to_visual_launcher"] = True
        with self.assertRaises(family_contract.LoopFamilyContractError):
            family_contract.validate_loop_family_stage_contract(contract)

    def test_contract_fails_closed_when_audio_or_dispatch_is_enabled(self):
        for contract_key in ("audio_asset_selected", "audio_generated", "pcm_samples_emitted", "audio_payload_materialized", "mux_invoked", "d3_v5_invoked"):
            contract = json.loads(json.dumps(self.cases[0][4]))
            contract["audio_delivery_envelope"][contract_key] = True
            contract["contract_sha256"] = family_contract._sha256({k: v for k, v in contract.items() if k != "contract_sha256"})
            with self.assertRaises(family_contract.LoopFamilyContractError):
                family_contract.validate_loop_family_stage_contract(contract)
        contract = json.loads(json.dumps(self.cases[0][4]))
        contract["governance"]["renderer_native_input_emitted"] = True
        contract["contract_sha256"] = family_contract._sha256({k: v for k, v in contract.items() if k != "contract_sha256"})
        with self.assertRaises(family_contract.LoopFamilyContractError):
            family_contract.validate_loop_family_stage_contract(contract)

    def test_visual_composition_obeys_approved_geometry_and_source_span(self):
        for _family, _grammar, _result, _bridge, contract in self.cases:
            comp = contract["composition"]
            self.assertEqual(comp["canvas"], {"width": 720, "height": 1280, "aspect_ratio": "9:16"})
            self.assertEqual(comp["source_frame_viewport"]["width"], 504)
            self.assertEqual(comp["source_frame_viewport"]["height"], 896)
            self.assertEqual(comp["source_frame_window"], "[0, ACTUAL_C11C_PAYLOAD.frame_count)")
            self.assertTrue(comp["materialized_payload_receipt_required"])
            self.assertEqual(comp["frame_order"], "IDENTITY_NO_RESAMPLING")

    def test_operator_decision_and_static_family_audit(self):
        report = contract_audit_v2.build_report(PROJECT_ROOT)
        self.assertEqual(report["schema"], "C11E-E4B-LOOP-FAMILY-CONTRACT-AUDIT-V2")
        self.assertEqual(report["status"], "PASS_OPERATOR_DECISIONS_AND_FAMILY_STATIC_CONTRACT_AUDIT_ONLY")
        self.assertEqual(report["audit_target"], "ACTIVE_CHECKOUT_PROJECT_ROOT")
        self.assertEqual(report["operator_decisions"]["decision_count"], 5)
        self.assertEqual(report["family_interface_audit"]["grammar_count"], 27)
        coverage = report["historical_product_coverage"]
        self.assertEqual(coverage["manifest_authoring_pairs"], "27/27")
        observed = contract_audit_v2.validate_mp4_presence_observation(coverage)
        self.assertEqual(coverage["mp4_present_in_project_root_count"], observed)
        self.assertFalse(coverage["visual_review_performed"])
        self.assertIn("NO_MP4_VISUAL_REVIEW", coverage["evidence_scope"])
        self.assertEqual(report["governance"]["d4_8"], "BLOCKED")
        self.assertEqual(report["governance"]["release_authority"], "NONE")

    def test_mp4_presence_is_observational_and_never_requires_zero(self):
        all_absent = [{"mp4_present_in_project_root": False} for _ in range(27)]
        all_present = [{"mp4_present_in_project_root": True} for _ in range(27)]
        mixed = [{"mp4_present_in_project_root": i < 13} for i in range(27)]
        self.assertEqual(contract_audit_v2.count_mp4_presence(all_absent), 0)
        self.assertEqual(contract_audit_v2.count_mp4_presence(all_present), 27)
        self.assertEqual(contract_audit_v2.count_mp4_presence(mixed), 13)
        with self.assertRaises(contract_audit_v2.AuditV2Error):
            contract_audit_v2.validate_mp4_presence_observation({
                "selectors": all_present,
                "selector_count": 27,
                "mp4_present_in_project_root_count": 0,
                "visual_review_performed": False,
            })


if __name__ == "__main__":
    unittest.main(verbosity=2)
