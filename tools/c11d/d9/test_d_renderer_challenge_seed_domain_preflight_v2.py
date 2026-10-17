from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import d_renderer_challenge_seed_domain_preflight_v2 as audit  # noqa: E402

EXPECTED_PINS = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
    "tools/c11d/d9/universal_producer.py": "9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1",
    "tools/c11d/d9/universal_editorial_model.py": "5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5",
    "tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py": "bad418fcee9b219c4ccd3f3720b8d623737b9790968608ba3f605430c8bb149b",
    "definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json": "342a61338c80a2f1616e8e9f38986bd90f410257c0e321f99840380fb0fd804b",
    "profiles/delivery/c11c_video_delivery_profiles.json": "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3",
    "c11c-suite/c11c-producer/c11d_gui_request.py": "0e95109ffd3ba5655d28292309196349470ab7958a467f096543a2c98c22976e",
    "challenges/CHALLENGE_001.json": "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea",
    "challenges/CHALLENGE_002.json": "db5d70a28c460e986e785c6787447529372ac5ea3b5a7ff0507667decbe2a160",
    "challenges/CHALLENGE_003.json": "38cb0166482c5ba4862deef8ab75dad4a6e1524590b6850312bab5238f078419",
    "challenges/CHALLENGE_004.json": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "challenges/CHALLENGE_005.json": "e173736fcbb0e340cd250be1111fa9d38489934d55cc0e0c93835c66f9596e30",
    "challenges/CHALLENGE_006.json": "2d7d7397cbb0a2109f300859a5d7c0830ded0553522a5120f61750f5bc0b5694",
    "challenges/CHALLENGE_007.json": "269f9588e5a6b7d253e2e944440cc41dc3a9db8967775ffa819edebe729a3a61",
    "challenges/CHALLENGE_008.json": "c3be7c943f5f4419497e371a181cd66d10ec2a7cdf76833b8627029c7a76c309",
    "challenges/CHALLENGE_009.json": "32dea4f9b3054fa2df1ace5680ce11cc9e167212f87a8688d374548135499151",
}

class ChallengeSeedDomainPreflightV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract, cls.schema, cls.report_schema, cls.lineage, cls.matrix = audit._load_and_validate_contract(ROOT)
        cls.report = audit.evaluate_challenge_seed_preflight(ROOT)

    def test_01_contract_and_all_source_pins_validate(self):
        self.assertEqual(len(self.lineage), 16)
        self.assertEqual({x['path'] for x in self.lineage}, set(EXPECTED_PINS))
        for row in self.lineage:
            self.assertEqual(row['sha256'], EXPECTED_PINS[row['path']])

    def test_02_contract_schema_is_strict_draft_2020_12(self):
        self.assertEqual(self.schema['$schema'], 'https://json-schema.org/draft/2020-12/schema')
        self.assertIs(self.schema['additionalProperties'], False)

    def test_03_report_schema_is_strict_draft_2020_12(self):
        self.assertEqual(self.report_schema['$schema'], 'https://json-schema.org/draft/2020-12/schema')
        self.assertIs(self.report_schema['additionalProperties'], False)

    def test_04_canonical_challenge_selector_inventory_is_9_of_9(self):
        self.assertEqual([r['challenge_id'] for r in self.matrix], list(audit.CHALLENGE_IDS))
        self.assertEqual(len({r['family_id'] for r in self.matrix}), 9)

    def test_05_matrix_contains_27_seed_variant_cases(self):
        self.assertEqual(len(self.report['cases']), 27)
        self.assertEqual(self.report['summary']['seed_variant_cases'], '27/27')

    def test_06_each_case_has_two_stable_planner_repeats(self):
        self.assertTrue(all(row['repeat_stable'] for row in self.report['cases']))
        self.assertEqual(self.report['summary']['repeat_consistency_checks'], '27/27')

    def test_07_gameplay_seed_changes_canonical_request_and_plan_identity(self):
        self.assertEqual(self.report['summary']['request_identity_seed_sensitivity'], '9/9')
        self.assertEqual(self.report['summary']['plan_identity_seed_sensitivity'], '9/9')

    def test_08_music_seed_changes_request_and_plan_identity(self):
        for cid in audit.CHALLENGE_IDS:
            rows = {x['variant_id']: x for x in self.report['cases'] if x['challenge_id'] == cid}
            self.assertNotEqual(rows['BASELINE']['request_hash'], rows['MUSIC_SEED_ONLY_CHANGED']['request_hash'])
            self.assertNotEqual(rows['BASELINE']['plan_hash'], rows['MUSIC_SEED_ONLY_CHANGED']['plan_hash'])

    def test_09_editorial_identity_is_invariant_across_seed_variants(self):
        self.assertEqual(self.report['summary']['editorial_identity_invariance'], '9/9')
        for cid in audit.CHALLENGE_IDS:
            hashes = {x['editorial_hash'] for x in self.report['cases'] if x['challenge_id'] == cid}
            self.assertEqual(len(hashes), 1)

    def test_10_all_plans_pass_canonical_d4_parity(self):
        self.assertTrue(all(x['canonical_plan_status'] == 'PLANNED' for x in self.report['cases']))
        self.assertTrue(all(x['canonical_d4_parity_status'] == 'PASS' for x in self.report['cases']))

    def test_11_challenge_008_and_009_timebase_conflicts_are_detected(self):
        conflicts = [x['challenge_id'] for x in self.report['timing_review'] if x['duration_conflict']]
        self.assertEqual(conflicts, ['CHALLENGE_008', 'CHALLENGE_009'])
        for cid in conflicts:
            row = next(x for x in self.report['timing_review'] if x['challenge_id'] == cid)
            self.assertEqual(row['explicit_total_duration_seconds'], 11.0)
            self.assertEqual(row['component_sum_duration_seconds'], 12.0)

    def test_12_planner_matrix_does_not_claim_payload_or_godot_execution(self):
        self.assertEqual(self.report['summary']['planner_invocations'], 54)
        self.assertEqual(self.report['summary']['godot_invocations'], 0)
        self.assertIs(self.report['summary']['payload_materialized'], False)
        self.assertEqual(self.report['summary']['challenge_visual_payload_seed_sensitivity'], 'NOT_TESTED')

    def test_13_unknown_challenge_fails_closed(self):
        with self.assertRaises(Exception):
            audit._selection_for(ROOT, 'CHALLENGE_010')

    def test_14_family_mismatch_fails_closed(self):
        with self.assertRaises(Exception):
            audit._selection_for(ROOT, 'CHALLENGE_001', 'parking_v2')

    def test_15_undeclared_subtype_fails_closed(self):
        with self.assertRaises(Exception):
            audit._selection_for(ROOT, 'CHALLENGE_001', None, 'illegal-subtype')

    def test_16_boolean_seed_fails_closed(self):
        selection = audit._selection_for(ROOT, 'CHALLENGE_001')
        raw = audit._build_raw_request(selection, 'TEST-BOOL-SEED')
        raw['seed'] = True
        with self.assertRaises(Exception):
            audit.planner.evaluate_universal_request(raw, ROOT)

    def test_17_zero_music_seed_fails_closed(self):
        selection = audit._selection_for(ROOT, 'CHALLENGE_001')
        raw = audit._build_raw_request(selection, 'TEST-ZERO-MUSIC-SEED')
        raw['music_seed'] = 0
        with self.assertRaises(Exception):
            audit.planner.evaluate_universal_request(raw, ROOT)

    def test_18_report_schema_and_digest_validate(self):
        self.assertEqual(self.report['schema_version'], '2.0')
        self.assertEqual(self.report['audit_sha256'], audit._sha_json({k:v for k,v in self.report.items() if k != 'audit_sha256'}))

    def test_19_execution_and_release_governance_remain_blocked(self):
        g = self.report['governance']
        self.assertEqual(g['renderer'], 'OFF')
        self.assertIs(g['candidate_input_admissible'], False)
        self.assertIs(g['seed_domains_complete_for_candidate_input'], False)
        self.assertEqual(g['D4.8'], 'BLOCKED')
        self.assertEqual(g['D9.10'], 'PREPARE_ONLY')
        self.assertEqual(g['D9.17'], 'BLOCKED_NO_GO')
        self.assertEqual(g['D10'], 'BLOCKED')
        self.assertEqual(g['release_authority'], 'NONE')

    def test_20_five_negative_preflight_cases_fail_closed(self):
        self.assertEqual(self.report['summary']['negative_cases'], '5/5')
        self.assertEqual(len(self.report['negative_cases']), 5)

if __name__ == '__main__':
    unittest.main(verbosity=2)
