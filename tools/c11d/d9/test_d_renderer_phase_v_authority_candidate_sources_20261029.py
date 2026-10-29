#!/usr/bin/env python3
"""40 static tests for Phase V source review helpers; no repository writes."""
import hashlib, json, tempfile, unittest
from pathlib import Path
from review_d_renderer_phase_v_authority_candidate_sources_20261029 import safe_relative, bounded_excerpts, build_report

def fixture(root: Path):
    a=root/'alpha.md';a.parent.mkdir(parents=True,exist_ok=True);a.write_text('\n'.join('line %d content'%i for i in range(1,15)),encoding='utf-8')
    b=root/'beta.json';b.write_text('{"authority":"proposal only"}\n',encoding='utf-8')
    c=root/'gamma.md';c.write_text('ordinary note\n',encoding='utf-8')
    def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    tri={'schema_version':'1.0.0','phase':'U','status':'CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW','no_global_absence_claim':True,'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE','source_scan_index_sha256':'a'*64,'counts':{'candidates':3,'high_priority':1,'medium_priority':1,'low_priority':1,'unsearched_documents':1},'governance':{'renderer':'OFF','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'},'timing_conflicts':[{'challenge':'CHALLENGE_008','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'},{'challenge':'CHALLENGE_009','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'}], 'candidates':[
    {'path':'alpha.md','sha256':sh(a),'bytes':a.stat().st_size,'priority':'HIGH_REVIEW_PRIORITY','priority_score':101,'matches':[{'line':7,'snippet':'line 7'}],'review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED'},
    {'path':'beta.json','sha256':sh(b),'bytes':b.stat().st_size,'priority':'MEDIUM_REVIEW_PRIORITY','priority_score':53,'matches':[{'line':1,'snippet':'authority'}],'review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED'},
    {'path':'gamma.md','sha256':sh(c),'bytes':c.stat().st_size,'priority':'LOW_REVIEW_PRIORITY','priority_score':0,'matches':[],'review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED'}],
    'unsearched_documents':[{'path':'missing.pdf','reason':'binary content not searched','review_status':'NOT_INSPECTED','authority_finding':'UNDETERMINED'}]}
    return tri,a,b,c

class PhaseVTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.tri,*self.files=fixture(self.root)
    def tearDown(self):self.tmp.cleanup()
    def test_01_safe_relative_simple(self):self.assertTrue(safe_relative('docs/a.md'))
    def test_02_safe_relative_nested(self):self.assertTrue(safe_relative('tools/c11d/d9/test.py'))
    def test_03_safe_relative_spaces(self):self.assertTrue(safe_relative('docs/my document.md'))
    def test_04_reject_empty(self):self.assertFalse(safe_relative(''))
    def test_05_reject_absolute_posix(self):self.assertFalse(safe_relative('/etc/passwd'))
    def test_06_reject_absolute_windows(self):self.assertFalse(safe_relative('C:\\temp\\a'))
    def test_07_reject_parent_traversal(self):self.assertFalse(safe_relative('../a'))
    def test_08_reject_nested_parent(self):self.assertFalse(safe_relative('a/../b'))
    def test_09_reject_dot_component(self):self.assertFalse(safe_relative('a/./b'))
    def test_10_excerpt_count(self):self.assertEqual(len(bounded_excerpts('a\nb\nc',[{'line':2}])),1)
    def test_11_excerpt_line_content(self):self.assertIn('2: b',bounded_excerpts('a\nb\nc',[{'line':2}])[0]['text'])
    def test_12_excerpt_start_bound(self):self.assertEqual(bounded_excerpts('a\nb\nc',[{'line':1}])[0]['start_line'],1)
    def test_13_excerpt_end_bound(self):self.assertEqual(bounded_excerpts('a\nb\nc',[{'line':3}])[0]['end_line'],3)
    def test_14_invalid_line_ignored(self):self.assertEqual(bounded_excerpts('a\nb',[{'line':0}]),[])
    def test_15_duplicate_windows_deduped(self):self.assertEqual(len(bounded_excerpts('a\nb\nc',[{'line':2},{'line':2}])),1)
    def test_16_source_count(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['counts']['candidates'],3)
    def test_17_high_count(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['counts']['high_priority'],1)
    def test_18_medium_count(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['counts']['medium_priority'],1)
    def test_19_low_count(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['counts']['low_priority'],1)
    def test_20_high_excerpt(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['counts']['high_priority_excerpts'],1)
    def test_21_all_hash_match(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['counts']['source_hash_matches'],3)
    def test_22_status_ready(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['status'],'SOURCE_EVIDENCE_INVENTORY_READY_FOR_HUMAN_REVIEW')
    def test_23_never_adjudicates(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['authority_adjudication'],'NOT_PERFORMED')
    def test_24_no_policy_adoption(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['policy_adoption'],'NONE')
    def test_25_candidates_unreviewed(self):self.assertTrue(all(x['review_status']=='NOT_REVIEWED' for x in build_report(self.root,self.tri,'b'*64)['candidates']))
    def test_26_findings_undetermined(self):self.assertTrue(all(x['authority_finding']=='UNDETERMINED' for x in build_report(self.root,self.tri,'b'*64)['candidates']))
    def test_27_unsearched_kept_unread(self):self.assertFalse(build_report(self.root,self.tri,'b'*64)['unsearched_documents'][0]['content_read'])
    def test_28_timing_preserved(self):self.assertEqual(len(build_report(self.root,self.tri,'b'*64)['timing_conflicts']),2)
    def test_29_source_pin_drift(self):
        self.files[0].write_text('changed')
        self.assertEqual(build_report(self.root,self.tri,'b'*64)['status'],'SOURCE_PIN_DRIFT_REQUIRES_RECONCILIATION')
    def test_30_missing_candidate(self):
        self.files[0].unlink()
        self.assertEqual(build_report(self.root,self.tri,'b'*64)['counts']['source_files_missing'],1)
    def test_31_governance_renderer(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['governance']['renderer'],'OFF')
    def test_32_governance_release(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['governance']['release_authority'],'NONE')
    def test_33_hash_sha_format(self):self.assertEqual(len(build_report(self.root,self.tri,'b'*64)['candidates'][0]['actual_sha256']),64)
    def test_34_actual_size(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['candidates'][0]['actual_bytes'],self.files[0].stat().st_size)
    def test_35_source_triage_hash_preserved(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['source_triage_sha256'],'b'*64)
    def test_36_scan_index_preserved(self):self.assertEqual(build_report(self.root,self.tri,'b'*64)['source_scan_index_sha256'],'a'*64)
    def test_37_reject_wrong_phase(self):
        t=dict(self.tri);t['phase']='T'
        with self.assertRaises(ValueError):build_report(self.root,t,'b'*64)
    def test_38_reject_bad_governance(self):
        t=dict(self.tri);t['governance']=dict(t['governance'],renderer='ON')
        with self.assertRaises(ValueError):build_report(self.root,t,'b'*64)
    def test_39_reject_bad_timing(self):
        t=dict(self.tri);t['timing_conflicts']=[dict(self.tri['timing_conflicts'][0],phase_duration_sum_seconds=11),self.tri['timing_conflicts'][1]]
        with self.assertRaises(ValueError):build_report(self.root,t,'b'*64)
    def test_40_reject_duplicate_candidate(self):
        t=dict(self.tri);t['candidates']=list(self.tri['candidates'])+[self.tri['candidates'][0]];t['counts']=dict(t['counts'],candidates=4)
        with self.assertRaises(ValueError):build_report(self.root,t,'b'*64)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(PhaseVTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    print('PHASE_V_SOURCE_REVIEW_TESTS=%d/%d'%(result.testsRun,result.testsRun))
    raise SystemExit(0 if result.wasSuccessful() else 1)
