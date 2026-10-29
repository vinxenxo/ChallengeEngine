#!/usr/bin/env python3
import importlib.util, unittest, json, hashlib, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / 'prepare_d_renderer_phase_w_authority_candidate_source_review_20261029.py'
spec = importlib.util.spec_from_file_location('phase_w_prepare', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def build_checks():
    checks = []
    def add(name, fn): checks.append((name, fn))
    case = unittest.TestCase()
    safe_paths = [
        'docs/a.md', 'docs/current/d/result.json', 'tools/c11d/test.py',
        'AGENTS.md', 'prompts/start.md', 'definitions/schema.json',
        'docs/current/d/x-y_z.md', 'folder.with.dot/file.txt',
        'a/b/c/d/e.txt', 'relative_01/path_02.dat'
    ]
    for i, path in enumerate(safe_paths, 1):
        add('safe_relative_path_' + str(i), lambda p=path: case.assertTrue(module.safe_relative(p)))
    unsafe_paths = [
        '', '../secret', 'a/../b', '/absolute', '\\rooted',
        'C:\\Windows\\x', 'a//b', 'a/./b', '..', 'a/../../x'
    ]
    for i, path in enumerate(unsafe_paths, 1):
        add('unsafe_relative_path_' + str(i), lambda p=path: case.assertFalse(module.safe_relative(p)))
    add('governance_renderer_is_off', lambda: case.assertEqual(module.GOV['renderer'], 'OFF'))
    add('governance_all_binding_counts_zero', lambda: case.assertEqual(
        [module.GOV[k] for k in ('approved_bindings','approved_custom_data_bindings','approved_renderer_projection_bindings')], [0,0,0]))
    add('governance_release_authority_none', lambda: case.assertEqual(module.GOV['release_authority'], 'NONE'))
    add('priority_high_label', lambda: case.assertEqual(module.PRIORITIES[0], 'HIGH_REVIEW_PRIORITY'))
    add('priority_medium_label', lambda: case.assertEqual(module.PRIORITIES[1], 'MEDIUM_REVIEW_PRIORITY'))
    add('priority_low_label', lambda: case.assertEqual(module.PRIORITIES[2], 'LOW_REVIEW_PRIORITY'))
    add('phase_u_hash_pin_length', lambda: case.assertEqual(len(module.EXPECTED_U_SHA), 64))
    add('phase_v_hash_pin_length', lambda: case.assertEqual(len(module.EXPECTED_V_SHA), 64))
    add('challenge_008_11_vs_12', lambda: case.assertEqual(
        (module.TIMING[0]['challenge'],module.TIMING[0]['declared_total_duration_seconds'],module.TIMING[0]['phase_duration_sum_seconds']), ('CHALLENGE_008',11,12)))
    add('challenge_009_11_vs_12', lambda: case.assertEqual(
        (module.TIMING[1]['challenge'],module.TIMING[1]['declared_total_duration_seconds'],module.TIMING[1]['phase_duration_sum_seconds']), ('CHALLENGE_009',11,12)))
    add('timing_conflicts_do_not_infer_correction', lambda: case.assertTrue(all(t['status']=='BLOCKER_NO_CORRECTION_INFERRED' for t in module.TIMING)))
    candidate = {'path':'docs/example.md','sha256':'a'*64,'bytes':12,'priority':'HIGH_REVIEW_PRIORITY','priority_score':9,'matches':[{'line':4}]}
    source_review = {'candidate_by_path':{'docs/example.md':{'actual_sha256':'a'*64,'actual_bytes':12,'excerpts':[{'match_line':4,'start_line':2,'end_line':6,'text':'example evidence excerpt'}],'excerpt_status':'CURRENT_SOURCE_CONTEXT_EXTRACTED'}}}
    row = module.make_candidate(candidate, source_review, 'a'*64, 12, 'MATCH')
    add('candidate_path_preserved', lambda: case.assertEqual(row['path'], 'docs/example.md'))
    add('candidate_integrity_match', lambda: case.assertEqual(row['source_integrity'], 'MATCH'))
    add('candidate_review_not_started', lambda: case.assertEqual(row['review_status'], 'NOT_REVIEWED'))
    add('candidate_finding_undetermined', lambda: case.assertEqual(row['authority_finding'], 'UNDETERMINED'))
    add('candidate_full_document_not_inspected', lambda: case.assertIs(row['full_document_inspected'], False))
    report = {
        'status':'SOURCE_QUEUE_READY_FOR_HUMAN_REVIEW', 'source_triage_sha256':'a'*64,
        'source_review_sha256':'b'*64,
        'counts':{'candidates':1,'high_priority':1,'medium_priority':0,'low_priority':0,
                  'source_hash_matches':1,'source_hash_mismatches':0,'source_files_missing':0,
                  'high_priority_excerpts':1,'unsearched_documents':1,'unsearched_existing':1,'unsearched_missing':0},
        'candidates':[row],
        'unsearched_documents':[{'path':'archive.zip','reason':'archive content excluded','review_status':'NOT_INSPECTED',
             'authority_finding':'UNDETERMINED','current_file_state':'EXISTS_CONTENT_NOT_READ','current_sha256':'c'*64,'current_bytes':4,'content_read':False}],
        'governance':module.GOV,'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE'
    }
    markdown = module.render_markdown(report)
    add('markdown_contains_evidence_excerpt', lambda: case.assertIn('example evidence excerpt', markdown))
    add('markdown_lists_unsearched_documents', lambda: case.assertIn('Seven mandatory content inspections', markdown))
    add('markdown_states_authority_threshold', lambda: case.assertIn('Authority threshold', markdown))
    add('markdown_preserves_renderer_lock', lambda: case.assertIn('renderer=OFF', markdown))
    if len(checks) != 40:
        raise AssertionError('Expected 40 tests, generated ' + str(len(checks)))
    return checks

class PhaseWTests(unittest.TestCase):
    pass
for name, fn in build_checks():
    setattr(PhaseWTests, 'test_' + name, lambda self, fn=fn: fn())
if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PhaseWTests))
    if result.wasSuccessful():
        print('PHASE_W_SOURCE_HUMAN_REVIEW_TESTS=40/40')
    raise SystemExit(0 if result.wasSuccessful() else 1)
