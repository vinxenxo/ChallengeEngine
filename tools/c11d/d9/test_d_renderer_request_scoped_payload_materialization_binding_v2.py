from __future__ import annotations
import copy
import hashlib
import json
import unittest
from pathlib import Path

import d_renderer_request_scoped_payload_materialization_binding_v2 as v2

ROOT = Path(__file__).resolve().parents[3]

def _sha(value):
    return hashlib.sha256(v2._canonical(value).encode("utf-8")).hexdigest()

def _close(obj, key):
    obj[key] = _sha({k:v for k,v in obj.items() if k != key})
    return obj

def _fixture(content_type="visual_loops"):
    rows = {
        "challenges": {"content_type":"challenges","request_id":"D-PAYLOAD-BIND-CHALLENGES","selection":{"content_type":"challenges","family_id":"parking_v2","subtype_id":None,"variant_id":"CHALLENGE_004"},"gameplay_seed":314159,"scope":"CHALLENGE_RUNTIME_VISUAL_PAYLOAD_SOURCE_TIMEBASE"},
        "visual_loops": {"content_type":"visual_loops","request_id":"D-PAYLOAD-BIND-VISUAL_LOOPS","selection":{"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane","variant_id":None},"gameplay_seed":12345,"scope":"VISUAL_LOOP_SELECTOR_PAYLOAD_HARMONIC_MEMBRANE_V1"},
        "visual_drills": {"content_type":"visual_drills","request_id":"D-PAYLOAD-BIND-VISUAL_DRILLS","selection":{"content_type":"visual_drills","family_id":"tracking","subtype_id":None,"variant_id":"tier-2"},"gameplay_seed":12345,"scope":"VISUAL_DRILL_TIER_SEED_PAYLOAD"},
    }
    base = dict(rows[content_type])
    base.update({"music_seed":840001,"variation_index":0,"presentation_profile_id":"social_default_v1","delivery_profile_id":"REVIEW_720"})
    return base

def _valid_inputs(content_type="visual_loops"):
    f=_fixture(content_type); sha=lambda c:c*64
    request_hash=sha('a'); plan_hash=sha('b'); bridge_hash=sha('d'); adapter_hash=sha('e'); source_binding_hash=sha('f'); lineage_hash=sha('1'); manifest_payload=sha('2'); visual_state=sha('3'); legacy_hash=sha('4')
    canonical_selection = dict(f["selection"])
    canonical_selection.update({
        "variant_scope_id": {
            "challenges": "challenge:parking_v2:CHALLENGE_004",
            "visual_loops": "visual_loop:c11c_geometric_waves_v1:harmonic_membrane",
            "visual_drills": "visual_drill:tracking:tier-2",
        }[content_type],
        "difficulty_tier": "tier-2" if content_type == "visual_drills" else None,
    })
    editorial_values = {
        "title": f"{content_type} title",
        "subtitle": f"{content_type} subtitle",
        "call_to_action": "Play now",
        "language": "en",
    }
    if content_type == "challenges":
        editorial_values.update({"player_name": "Alex", "challenge_label": "Parking"})
    editorial_hash = _sha({"selection": canonical_selection, "editorial": editorial_values})
    canonical_result = {
        "status": "PLANNED",
        "canonical_request": {
            "request_id": f["request_id"],
            "selection": canonical_selection,
            "editorial": editorial_values,
        },
        "request_hash": request_hash,
        "plan_hash": plan_hash,
        "editorial_hash": editorial_hash,
    }
    mri={"request_id":f["request_id"],"content_type":f["content_type"],"selection":f["selection"],"canonical_request_sha256":request_hash,"plan_sha256":plan_hash,"editorial_sha256":editorial_hash,"gameplay_seed":f["gameplay_seed"],"music_seed":f["music_seed"],"variation_index":f["variation_index"],"presentation_profile_id":f["presentation_profile_id"],"delivery_profile_id":f["delivery_profile_id"]}
    msource={"bridge_record_sha256":bridge_hash,"adapter_envelope_sha256":adapter_hash,"request_scoped_binding_sha256":source_binding_hash,"dynamic_binding_lineage_sha256":lineage_hash}
    mpayload={"payload_sha256":manifest_payload,"visual_state_sha256":visual_state,"payload_scope":f["scope"]}
    manifest={"schema":v2.dynamic.PAYLOAD_MANIFEST_SCHEMA_ID,"schema_version":"1.0","status":v2.dynamic.PAYLOAD_MANIFEST_STATUS,"request_identity":mri,"source_lineage":msource,"payload_identity":mpayload}
    _close(manifest,"manifest_sha256")
    identity={"request_id":f["request_id"],"content_type":f["content_type"],"selection":f["selection"],"gameplay_seed":f["gameplay_seed"],"music_seed":f["music_seed"],"variation_index":f["variation_index"],"presentation_profile_id":f["presentation_profile_id"],"delivery_profile_id":f["delivery_profile_id"],"request_binding_sha256":sha('5')}
    source={"request_hash":request_hash,"plan_hash":plan_hash,"editorial_hash":editorial_hash,"bridge_record_hash":bridge_hash,"adapter_envelope_hash":adapter_hash,"source_binding_sha256":source_binding_hash,"source_lineage_sha256":lineage_hash,"request_scoped_binding_sha256":source_binding_hash,"request_payload_manifest_sha256":manifest["manifest_sha256"]}
    evidence={"payload_sha256":manifest_payload,"visual_state_sha256":visual_state,"payload_scope":mpayload["payload_scope"],"exact_selector_payload_materialized":True,"deterministic_repeat_pass":True,"materialization":"IN_MEMORY_ONLY","request_payload_manifest_sha256":manifest["manifest_sha256"]}
    # Match the actual dynamic binder V1 strict receipt shape: admission and render
    # readiness live under `readiness`, not as top-level receipt properties.
    binder={"schema":v2.dynamic.OUTPUT_SCHEMA_ID,"schema_version":"1.0","status":v2.dynamic.STATUS,"frozen_c11c_manifest_sha256":v2.MANIFEST_SHA256,"request_identity":identity,"source_identity":source,"payload_evidence":evidence,"payload_manifest":manifest,"readiness":{"candidate_input_admissible":False,"video_render_ready":False},"execution_boundary":copy.deepcopy(v2.dynamic.EXPECTED_BOUNDARY)}
    _close(binder,"receipt_sha256")
    material={"content_type":f["content_type"],"request_id":f["request_id"],"selection":f["selection"],"canonical_request_sha256":request_hash,"producer_plan_sha256":plan_hash,"bridge_record_sha256":bridge_hash,"adapter_envelope_sha256":adapter_hash,"request_source_binding_sha256":source_binding_hash,"gameplay_seed":f["gameplay_seed"],"music_seed":f["music_seed"],"variation_index":f["variation_index"],"presentation_profile_id":f["presentation_profile_id"],"delivery_profile_id":f["delivery_profile_id"],"source_seed_matches_request":True,"materialization":"IN_MEMORY_ONLY","video_render_ready":False,"payload_instance_id":"D-VLP-1234567890abcdef","payload_instance_sha256":legacy_hash}
    _close(material,"binding_sha256")
    carrier_fields = []
    for name, value in editorial_values.items():
        carrier_fields.append({"field_name":name,"value":value,"value_sha256":hashlib.sha256(value.encode("utf-8")).hexdigest()})
    carrier={"content_type":f["content_type"],"request_id":f["request_id"],"canonical_request_sha256":request_hash,"base_materialization_request_sha256":request_hash,"request_hash_matches_base_materialization_request":True,"payload_instance_id":material["payload_instance_id"],"payload_instance_sha256":legacy_hash,"editorial_values_sha256":_sha(editorial_values),"fields":carrier_fields,"payload_mutated":False,"editorial_values_injected_into_visual_payload":False,"visual_payload_consumed_editorial_text":False}
    _close(carrier,"carrier_binding_sha256")
    return f,binder,material,carrier,canonical_result

class RequestPayloadInstanceV2Tests(unittest.TestCase):
    def test_contract_and_60_source_pins(self):
        contract,schema=v2._load_contract(ROOT)
        self.assertEqual(len(contract["source_pins"]),60)
        self.assertEqual(contract["scope"]["selector_scope"],"EXACT_EXISTING_FIXED_REVIEW_FIXTURES_ONLY")
        self.assertEqual(schema["$schema"],"https://json-schema.org/draft/2020-12/schema")

    def test_valid_join_preserves_distinct_payload_digest_namespaces(self):
        f,b,m,c,cr=_valid_inputs(); row=v2._join_one(b,m,c,f,cr)
        self.assertEqual(row["request_identity_join"],"EXACT_CANONICAL_REQUEST_HASH_AND_SELECTOR_JOIN_PASS")
        self.assertEqual(row["dynamic_payload_sha256"],b["payload_evidence"]["payload_sha256"])
        self.assertEqual(row["legacy_payload_instance_sha256"],m["payload_instance_sha256"])
        self.assertNotEqual(row["dynamic_payload_sha256"],row["legacy_payload_instance_sha256"])
        self.assertEqual(row["payload_digest_relation"],"SEPARATE_CONTRACTS_NO_EQUIVALENCE_CLAIM")

    def _sample_receipt(self):
        rows=[]
        for ct in ("challenges","visual_loops","visual_drills"):
            f,b,m,c,cr=_valid_inputs(ct)
            rows.append(v2._join_one(b,m,c,f,cr))
        schema = v2._read_json(ROOT, v2.SCHEMA_REL)
        receipt = {
            "schema":v2.OUTPUT_SCHEMA,"schema_version":"2.0","status":v2.STATUS,
            "frozen_c11c_manifest_sha256":v2.MANIFEST_SHA256,"candidate_input_admissible":False,"source_pin_count":60,
            "runtime_identity":{
                "contract_path":v2.CONTRACT_REL.as_posix(),"contract_sha256":"a"*64,
                "schema_path":v2.SCHEMA_REL.as_posix(),"schema_sha256":"b"*64,
                "implementation_path":"tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding_v2.py","implementation_sha256":"c"*64,
                "test_path":"tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding_v2.py","test_sha256":"d"*64,
                "proposal_contract_sha256":v2.PROPOSAL_SHA256,"decision_record_sha256":v2.DECISION_SHA256},
            "content_bindings":rows,
            "summary":{"content_types":3,"request_identity_joins":3,"payload_manifest_digests_verified":3,"editorial_sidecar_joins":3,"sidecar_field_values":14,"visual_text_sidecar_values":11,"metadata_only_values":3,"visual_payload_text_consumed":0,"payload_digest_equivalence_proven":False,"video_render_ready":False},
            "execution_boundary":{"mode":"IN_MEMORY_REVIEW_ONLY_REQUEST_PAYLOAD_JOIN_V2","request_input_persisted":False,"payload_files_written":False,"receipt_files_written":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"editorial_values_injected_into_visual_payload":False,"c11c_source_mutation":False,"d4_8":"BLOCKED","release_authority":"NONE","d9_14":"BLOCKED_AS_REQUIRED","d9_16":"BLOCKED_AS_REQUIRED","d9_17":"BLOCKED_NO_GO","d10":"BLOCKED"}}
        _close(receipt,"receipt_sha256")
        return receipt, schema

    def test_strict_output_schema_accepts_join_receipt(self):
        receipt,schema=self._sample_receipt()
        v2._validate_receipt(receipt,schema)

    def test_strict_output_schema_rejects_six_policy_and_shape_mutations(self):
        import jsonschema
        receipt,schema=self._sample_receipt()
        mutations=[]
        for path,value in [
            (("candidate_input_admissible",),True),
            (("execution_boundary","renderer_native_input_emitted"),True),
            (("execution_boundary","media_output_created"),True),
            (("summary","payload_digest_equivalence_proven"),True),
            (("summary","sidecar_field_values"),13),
        ]:
            changed=copy.deepcopy(receipt); node=changed
            for key in path[:-1]: node=node[key]
            node[path[-1]]=value; _close(changed,"receipt_sha256"); mutations.append(changed)
        changed=copy.deepcopy(receipt); changed["unexpected_property"]=True; _close(changed,"receipt_sha256"); mutations.append(changed)
        for changed in mutations:
            with self.subTest(changed=changed.get("unexpected_property",changed.get("summary",{}))):
                with self.assertRaises((jsonschema.ValidationError, v2.PayloadInstanceIntegrationError)):
                    v2._validate_receipt(changed,schema)

    def test_rejects_materialization_request_hash_mismatch(self):
        f,b,m,c,cr=_valid_inputs(); m["canonical_request_sha256"]="9"*64; _close(m,"binding_sha256")
        with self.assertRaises(v2.PayloadInstanceIntegrationError): v2._join_one(b,m,c,f,cr)

    def test_rejects_selector_mismatch(self):
        f,b,m,c,cr=_valid_inputs(); b["request_identity"]["selection"]["subtype_id"]="other"; b["payload_manifest"]["request_identity"]["selection"]["subtype_id"]="other"; _close(b["payload_manifest"],"manifest_sha256"); b["source_identity"]["request_payload_manifest_sha256"]=b["payload_manifest"]["manifest_sha256"]; b["payload_evidence"]["request_payload_manifest_sha256"]=b["payload_manifest"]["manifest_sha256"]; _close(b,"receipt_sha256")
        with self.assertRaises(v2.PayloadInstanceIntegrationError): v2._join_one(b,m,c,f,cr)

    def test_rejects_manifest_digest_corruption(self):
        f,b,m,c,cr=_valid_inputs(); b["payload_manifest"]["manifest_sha256"]="0"*64; _close(b,"receipt_sha256")
        with self.assertRaises(v2.PayloadInstanceIntegrationError): v2._join_one(b,m,c,f,cr)

    def test_rejects_editorial_sidecar_hash_mismatch(self):
        f,b,m,c,cr=_valid_inputs(); c["editorial_values_sha256"]="9"*64; _close(c,"carrier_binding_sha256")
        with self.assertRaises(v2.PayloadInstanceIntegrationError): v2._join_one(b,m,c,f,cr)

    def test_rejects_claimed_payload_mutation(self):
        f,b,m,c,cr=_valid_inputs(); c["payload_mutated"]=True; _close(c,"carrier_binding_sha256")
        with self.assertRaises(v2.PayloadInstanceIntegrationError): v2._join_one(b,m,c,f,cr)

    def test_accepts_actual_dynamic_v1_receipt_shape_without_top_level_admission_flag(self):
        f,b,m,c,cr=_valid_inputs()
        self.assertNotIn("candidate_input_admissible", b)
        self.assertIs(b["readiness"]["candidate_input_admissible"], False)
        row=v2._join_one(b,m,c,f,cr)
        self.assertEqual(row["content_type"], f["content_type"])

    def test_rejects_candidate_admissibility(self):
        f,b,m,c,cr=_valid_inputs(); b["readiness"]["candidate_input_admissible"]=True; _close(b,"receipt_sha256")
        with self.assertRaises(v2.PayloadInstanceIntegrationError): v2._join_one(b,m,c,f,cr)

    def test_rejects_missing_readiness_section(self):
        f,b,m,c,cr=_valid_inputs(); b.pop("readiness"); _close(b,"receipt_sha256")
        with self.assertRaises(v2.PayloadInstanceIntegrationError): v2._join_one(b,m,c,f,cr)

    def test_canonical_editorial_and_map_only_hash_namespaces_are_distinct(self):
        f,b,m,c,cr=_valid_inputs("challenges")
        row=v2._join_one(b,m,c,f,cr)
        self.assertEqual(row["editorial_values_sha256"], c["editorial_values_sha256"])
        self.assertEqual(row["canonical_editorial_sha256"], cr["editorial_hash"])
        self.assertEqual(row["canonical_editorial_reconstructed_sha256"], cr["editorial_hash"])
        self.assertNotEqual(row["editorial_values_sha256"], row["canonical_editorial_sha256"])
        self.assertEqual(row["editorial_values_hash_namespace"], "EDITORIAL_MAP_ONLY")
        self.assertEqual(row["canonical_editorial_hash_namespace"], "CANONICAL_SELECTION_PLUS_EDITORIAL_MAP")

    def test_rejects_sidecar_value_drift_even_if_sidecar_hashes_are_recomputed(self):
        f,b,m,c,cr=_valid_inputs("challenges")
        c["fields"][0]["value"] = "tampered title"
        c["fields"][0]["value_sha256"] = hashlib.sha256(b"tampered title").hexdigest()
        sidecar_values = {row["field_name"]: row["value"] for row in c["fields"]}
        c["editorial_values_sha256"] = _sha(sidecar_values)
        _close(c,"carrier_binding_sha256")
        with self.assertRaises(v2.PayloadInstanceIntegrationError):
            v2._join_one(b,m,c,f,cr)

    def test_rejects_mutated_full_selection_in_reconstructed_editorial_hash(self):
        f,b,m,c,cr=_valid_inputs("challenges")
        cr=copy.deepcopy(cr)
        cr["canonical_request"]["selection"]["variant_scope_id"] = "mutated-scope"
        with self.assertRaises(v2.PayloadInstanceIntegrationError):
            v2._join_one(b,m,c,f,cr)

    def test_full_canonical_producer_hash_reconstruction_for_all_fixed_fixtures(self):
        fixtures = v2.materialization_v1._fixture_requests(ROOT)
        self.assertEqual(set(fixtures), {"challenges", "visual_loops", "visual_drills"})
        for content_type in ("challenges", "visual_loops", "visual_drills"):
            with self.subTest(content_type=content_type):
                raw = v2.materialization_v1._raw_request(fixtures[content_type])
                result = v2.dynamic.evaluate_universal_request(dict(raw), ROOT)
                canonical = result["canonical_request"]
                composite = _sha({"selection": canonical["selection"], "editorial": canonical["editorial"]})
                map_only = _sha(canonical["editorial"])
                self.assertEqual(result["status"], "PLANNED")
                self.assertEqual(composite, result["editorial_hash"])
                self.assertNotEqual(map_only, result["editorial_hash"])
                self.assertEqual(len(canonical["editorial"]), 6 if content_type == "challenges" else 4)

if __name__ == '__main__':
    unittest.main(verbosity=2)
