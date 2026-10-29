#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
VERIFIER = HERE.with_name('verify_d_renderer_phase_x_authority_source_content_20261029_v3.py')
SPEC = importlib.util.spec_from_file_location('phase_x_verifier_v3', VERIFIER)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class HighPriorityBundleCountTests(unittest.TestCase):
    def test_counts_string_bundle_members_without_type_error(self):
        records = [
            {'priority': 'HIGH_REVIEW_PRIORITY', 'bundle_member': 'high_priority_candidates/001.txt'},
            {'priority': 'HIGH_REVIEW_PRIORITY', 'bundle_member': 'high_priority_candidates/002.txt'},
        ]
        self.assertEqual(MODULE.count_high_priority_bundle_members(records), 2)

    def test_ignores_high_priority_without_bundle_member(self):
        records = [
            {'priority': 'HIGH_REVIEW_PRIORITY', 'bundle_member': None},
            {'priority': 'HIGH_REVIEW_PRIORITY'},
            {'priority': 'MEDIUM_REVIEW_PRIORITY', 'bundle_member': 'medium/001.txt'},
        ]
        self.assertEqual(MODULE.count_high_priority_bundle_members(records), 0)

    def test_counts_only_high_priority_members(self):
        records = [
            {'priority': 'HIGH_REVIEW_PRIORITY', 'bundle_member': 'high/1.txt'},
            {'priority': 'MEDIUM_REVIEW_PRIORITY', 'bundle_member': 'medium/1.txt'},
            {'priority': 'LOW_REVIEW_PRIORITY', 'bundle_member': 'low/1.txt'},
        ]
        self.assertEqual(MODULE.count_high_priority_bundle_members(records), 1)

    def test_empty_input(self):
        self.assertEqual(MODULE.count_high_priority_bundle_members([]), 0)

    def test_matches_expected_50_member_shape(self):
        records = [
            {'priority': 'HIGH_REVIEW_PRIORITY', 'bundle_member': f'high/{i:03d}.txt'}
            for i in range(1, 51)
        ] + [
            {'priority': 'MEDIUM_REVIEW_PRIORITY', 'bundle_member': f'medium/{i:03d}.txt'}
            for i in range(1, 58)
        ]
        self.assertEqual(MODULE.count_high_priority_bundle_members(records), 50)

if __name__ == '__main__':
    result = unittest.main(verbosity=2, exit=False)
    if not result.result.wasSuccessful():
        raise SystemExit(1)
    print('PHASE_X_V3_VERIFIER_NUMERIC_COUNT_TESTS=5/5')
