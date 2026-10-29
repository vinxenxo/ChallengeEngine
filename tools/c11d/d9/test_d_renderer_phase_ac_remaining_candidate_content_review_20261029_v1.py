#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, unittest, zipfile
from pathlib import Path

EXPECTED_BUNDLE_SHA = "5ee6ec0f5a6b3a0884c22bbecfc98691269bd431adc896c088e7eb7f9d0b7f08"
EXPECTED_MANIFEST_SHA = "bc8405ccba850a540ab00d50691462ef496f1ccda9586dda7f775ff09e5c7ac1"
EXPECTED_C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

class PhaseACContentReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ap=argparse.ArgumentParser()
        ap.add_argument('--review-json', required=True)
        ap.add_argument('--matrix-json', required=True)
        a=ap.parse_args()
        cls.r=load(a.review_json); cls.m=load(a.matrix_json)
        cls.rows=cls.r['source_dispositions']; cls.paths=[x['path'] for x in cls.rows]
        cls.by_path={x['path']:x for x in cls.rows}

    def test_01_report_schema(self): self.assertEqual(self.r['schema'],'C11D-PHASE-AC-REMAINING-CANDIDATE-CONTENT-REVIEW-RESULT-V1')
    def test_02_phase_ac(self): self.assertEqual(self.r['phase'],'AC')
    def test_03_status_review_complete(self): self.assertEqual(self.r['status'],'PASS_CONTENT_REVIEW_COMPLETE_NO_APPLICABLE_D_RENDER_AUTHORITY_FOUND')
    def test_04_bundle_sha_pin(self): self.assertEqual(self.r['input']['source_bundle_sha256'],EXPECTED_BUNDLE_SHA)
    def test_05_manifest_sha_pin(self): self.assertEqual(self.r['input']['source_manifest_sha256'],EXPECTED_MANIFEST_SHA)
    def test_06_exact_57_sources(self): self.assertEqual(len(self.rows),57)
    def test_07_55_medium(self): self.assertEqual(sum(x['priority']=='MEDIUM_REVIEW_PRIORITY' for x in self.rows),55)
    def test_08_two_low(self): self.assertEqual(sum(x['priority']=='LOW_REVIEW_PRIORITY' for x in self.rows),2)
    def test_09_unique_paths(self): self.assertEqual(len(set(self.paths)),57)
    def test_10_no_missing_sources(self): self.assertEqual(self.r['counts']['source_files_missing'],0)
    def test_11_no_hash_mismatches(self): self.assertEqual(self.r['counts']['source_hash_mismatches'],0)
    def test_12_all_hashes_match(self): self.assertEqual(self.r['counts']['source_hash_matches'],57)
    def test_13_sha_format(self): self.assertTrue(all(re.fullmatch(r'[0-9a-f]{64}',x['sha256']) for x in self.rows))
    def test_14_sizes_positive(self): self.assertTrue(all(isinstance(x['bytes'],int) and x['bytes']>0 for x in self.rows))
    def test_15_every_row_has_disposition(self): self.assertTrue(all(x['review_disposition'] and x['review_note'] for x in self.rows))
    def test_16_matrix_has_57_rows(self): self.assertEqual(len(self.m['source_dispositions']),57)
    def test_17_matrix_hash_matches_report(self): self.assertEqual([(x['path'],x['sha256']) for x in self.m['source_dispositions']],[(x['path'],x['sha256']) for x in self.rows])
    def test_18_matrix_bundle_pin(self): self.assertEqual(self.m['source_bundle']['sha256'],EXPECTED_BUNDLE_SHA)
    def test_19_applicable_render_authority_zero(self): self.assertEqual(self.r['counts']['authority_records_applicable_to_first_d_baseline_render'],0)
    def test_20_bounded_d914_record_count(self): self.assertEqual(self.r['counts']['bounded_qualification_records_out_of_scope'],1)
    def test_21_no_policy_adoption_count(self): self.assertEqual(self.r['counts']['policy_adoptions'],0)
    def test_22_no_operator_adjudication_count(self): self.assertEqual(self.r['counts']['authority_adjudications_from_operator_evidence'],0)
    def test_23_d914_scoped_record_classified(self): self.assertEqual(self.by_path['definitions/c11d/production/D9_14_PRODUCTION_QUALIFICATION_AUTHORIZATION_V1.json']['review_disposition'],'LIMITED_AUTHORIZATION_OUT_OF_SCOPE')
    def test_24_d914_scope_note_excludes_renderer(self): self.assertIn('No autoriza el primer render',self.by_path['definitions/c11d/production/D9_14_PRODUCTION_QUALIFICATION_AUTHORIZATION_V1.json']['review_note'])
    def test_25_d48_evidence_not_authority(self): self.assertEqual(self.by_path['artifacts/tests/c11d_d4/d4_8/d4_8_authorization_evidence.json']['review_disposition'],'TEST_EVIDENCE_NO_ACTIVATION')
    def test_26_semantic_record_limited(self): self.assertEqual(self.by_path['definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json']['review_disposition'],'LIMITED_DECISION_FUTURE_SPEC_ONLY')
    def test_27_field_region_record_limited(self): self.assertEqual(self.by_path['definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_V1.json']['review_disposition'],'LIMITED_DECISION_FUTURE_SPEC_ONLY')
    def test_28_phase_r_packet_preparation_only(self): self.assertEqual(self.by_path['docs/current/d/C11D_PHASE_R_OPERATOR_POLICY_DECISION_PACKET_20261029_V1.md']['review_disposition'],'PREPARATION_ONLY_NO_POLICY_ADOPTION')
    def test_29_d917_no_go(self): self.assertEqual(self.by_path['docs/current/d/D9.17_D9_CLOSURE_ADJUDICATION_CHECKPOINT.md']['review_disposition'],'EXPLICIT_NO_GO')
    def test_30_editorial_consumption_zero(self): self.assertIn('0/14',self.by_path['docs/current/d/D_RENDERER_EDITORIAL_FIELD_CONSUMPTION_AUDIT_CHECKPOINT_V1.md']['review_note'])
    def test_31_seed_governance_scoped(self): self.assertEqual(self.by_path['definitions/c11d/seeds/C11D_SEED_GOVERNANCE_POLICY_V1.json']['review_disposition'],'SCOPED_SEED_POLICY_NOT_RENDER_AUTHORITY')
    def test_32_schemas_not_decisions(self): self.assertTrue(all(x['review_disposition']=='SCHEMA_ONLY_NOT_DECISION' for x in self.rows if x['path'].endswith('_SCHEMA_V1.json')))
    def test_33_tool_tests_not_authority(self): self.assertTrue(all(x['review_disposition']=='STATIC_TEST_NOT_AUTHORITY' for x in self.rows if '/test_' in x['path']))
    def test_34_runner_tooling_not_authority(self): self.assertTrue(all(x['review_disposition'] in {'GOVERNANCE_EVALUATOR_NOT_AUTHORITY','VALIDATION_RUNNER_NOT_EXECUTION_AUTHORITY','AUDIT_RUNNER_NOT_AUTHORITY','AUDIT_IMPLEMENTATION_NOT_AUTHORITY','READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL','PREPARATION_TOOL_NOT_DECISION_AUTHORITY'} for x in self.rows if x['path'].startswith('tools/') and '/test_' not in x['path']))
    def test_35_renderer_off(self): self.assertEqual(self.r['governance']['renderer'],'OFF')
    def test_36_binding_counts_zero(self):
        g=self.r['governance']; self.assertEqual((g['approved_bindings'],g['approved_custom_data_bindings'],g['approved_renderer_projection_bindings']),(0,0,0))
    def test_37_candidate_input_inadmissible(self): self.assertFalse(self.r['governance']['candidate_input_admissible'])
    def test_38_master_seed_not_adopted(self): self.assertEqual(self.r['governance']['master_seed'],'NOT_ADOPTED')
    def test_39_d917_d10_stay_blocked(self):
        g=self.r['governance']; self.assertEqual(g['D9.17'],'BLOCKED_NO_GO'); self.assertEqual(g['D10'],'BLOCKED_FOR_PROMOTION')
    def test_40_release_none(self): self.assertEqual(self.r['governance']['release_authority'],'NONE')
    def test_41_c11c_immutable_pin(self): self.assertEqual(self.r['governance']['c11c_manifest_sha256'],EXPECTED_C11C_SHA)
    def test_42_no_global_absence_claim(self): self.assertTrue(self.r['coverage']['no_global_absence_claim'])
    def test_43_next_gate_phase_ad(self): self.assertEqual(self.r['authority_conclusion']['next_gate'],'PHASE_AD_OPERATOR_AUTHORITY_EVIDENCE_OR_EXPLICIT_KEEP_BLOCKED_DECISION')
    def test_44_no_runtime_claim(self): self.assertFalse(self.r['governance']['media_created']); self.assertFalse(self.r['governance']['payload_materialized'])
    def test_45_every_candidate_source_comes_from_manifest(self): self.assertTrue(all(x['archive_member']=='sources/'+x['path'] for x in self.rows))

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(PhaseACContentReviewTests)
    res=unittest.TextTestRunner(verbosity=2).run(suite)
    print('PHASE_AC_CONTENT_REVIEW_TESTS=%d/%d' % (res.testsRun,res.testsRun))
    raise SystemExit(0 if res.wasSuccessful() else 1)
