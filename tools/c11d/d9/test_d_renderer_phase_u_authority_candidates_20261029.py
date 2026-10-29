import importlib.util, hashlib, json, tempfile, unittest
from pathlib import Path
MODULE_PATH=Path(__file__).with_name('triage_d_renderer_phase_u_authority_candidates_20261029.py')
spec=importlib.util.spec_from_file_location('phase_u_triage',MODULE_PATH); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def candidate(path='docs/authority.md', snippet='approved by director'):
 return {'path':path,'sha256':'a'*64,'bytes':10,'classification':'UNREVIEWED_CANDIDATE_NOT_AUTHORITY','filename_match':True,'matches':[{'line':1,'rule':'AUTHORITY_APPROVAL_OR_DECISION_FIELD_CANDIDATE','snippet':snippet}]}
def report():
 return {'phase':'T','status':'CANDIDATE_INVENTORY_READY_FOR_HUMAN_REVIEW','no_global_absence_claim':True,'scan_index_sha256':'b'*64,'counts':{'candidate_files':1,'unsearched_documents':1,'scan_errors':0,'files_seen':2,'text_files_scanned':1},'candidates':[candidate()],'unsearched_documents':[{'path':'docs/unsearched.pdf','reason':'binary content not inspected'}],'scan_errors':[],'skipped_large_files':[],'governance':{'renderer':'OFF','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'},'timing_conflicts':[{'challenge':'CHALLENGE_008','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'},{'challenge':'CHALLENGE_009','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'}]}
class PhaseUTests(unittest.TestCase):
 def setUp(self): self.r=report(); self.t=mod.triage_report(self.r,'c'*64)
 def test_01_report_schema_version(self): self.assertEqual(self.t['schema_version'],'1.0.0')
 def test_02_phase(self): self.assertEqual(self.t['phase'],'U')
 def test_03_status(self): self.assertEqual(self.t['status'],'CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW')
 def test_04_source_hash(self): self.assertEqual(self.t['source_report_sha256'],'c'*64)
 def test_05_source_index_hash(self): self.assertEqual(self.t['source_scan_index_sha256'],'b'*64)
 def test_06_scope_input_only(self): self.assertTrue(self.t['scope']['input_phase_t_report_only'])
 def test_07_no_rescan(self): self.assertFalse(self.t['scope']['working_tree_rescanned'])
 def test_08_no_git_history(self): self.assertFalse(self.t['scope']['git_history_searched'])
 def test_09_no_external(self): self.assertFalse(self.t['scope']['external_files_searched'])
 def test_10_no_binary_content(self): self.assertFalse(self.t['scope']['binary_document_contents_searched'])
 def test_11_priority_not_authority(self): self.assertFalse(self.t['scope']['priority_is_authority'])
 def test_12_counts_candidate(self): self.assertEqual(self.t['counts']['candidates'],1)
 def test_13_counts_high(self): self.assertEqual(self.t['counts']['high_priority'],1)
 def test_14_medium_zero(self): self.assertEqual(self.t['counts']['medium_priority'],0)
 def test_15_low_zero(self): self.assertEqual(self.t['counts']['low_priority'],0)
 def test_16_unsearched_count(self): self.assertEqual(self.t['counts']['unsearched_documents'],1)
 def test_17_scan_errors(self): self.assertEqual(self.t['counts']['scan_errors'],0)
 def test_18_safe_relative_path(self): self.assertTrue(mod.safe_relative('docs/a.md'))
 def test_19_reject_parent_path(self): self.assertFalse(mod.safe_relative('../a.md'))
 def test_20_reject_absolute_path(self): self.assertFalse(mod.safe_relative('/docs/a.md'))
 def test_21_candidate_sha_preserved(self): self.assertEqual(self.t['candidates'][0]['sha256'],'a'*64)
 def test_22_candidate_bytes(self): self.assertEqual(self.t['candidates'][0]['bytes'],10)
 def test_23_priority_high(self): self.assertEqual(self.t['candidates'][0]['priority'],'HIGH_REVIEW_PRIORITY')
 def test_24_priority_score(self): self.assertGreaterEqual(self.t['candidates'][0]['priority_score'],100)
 def test_25_review_not_done(self): self.assertEqual(self.t['candidates'][0]['review_status'],'NOT_REVIEWED')
 def test_26_authority_undetermined(self): self.assertEqual(self.t['candidates'][0]['authority_finding'],'UNDETERMINED')
 def test_27_preserve_match(self): self.assertEqual(self.t['candidates'][0]['matches'],self.r['candidates'][0]['matches'])
 def test_28_unsearched_not_inspected(self): self.assertEqual(self.t['unsearched_documents'][0]['review_status'],'NOT_INSPECTED')
 def test_29_unsearched_reason(self): self.assertIn('binary',self.t['unsearched_documents'][0]['reason'])
 def test_30_governance_renderer(self): self.assertEqual(self.t['governance']['renderer'],'OFF')
 def test_31_governance_bindings(self): self.assertEqual(self.t['governance']['approved_bindings'],0)
 def test_32_release_authority(self): self.assertEqual(self.t['governance']['release_authority'],'NONE')
 def test_33_timing_count(self): self.assertEqual(len(self.t['timing_conflicts']),2)
 def test_34_timing_duration(self): self.assertTrue(all(x['declared_total_duration_seconds']==11 for x in self.t['timing_conflicts']))
 def test_35_timing_sum(self): self.assertTrue(all(x['phase_duration_sum_seconds']==12 for x in self.t['timing_conflicts']))
 def test_36_no_global_absence(self): self.assertTrue(self.t['no_global_absence_claim'])
 def test_37_no_authority_adjudication(self): self.assertEqual(self.t['authority_adjudication'],'NOT_PERFORMED')
 def test_38_no_policy_adoption(self): self.assertEqual(self.t['policy_adoption'],'NONE')
 def test_39_markdown_disclaimer(self): self.assertIn('not authority',mod.render_markdown(self.t).lower())
 def test_40_markdown_unsearched(self): self.assertIn('docs/unsearched.pdf',mod.render_markdown(self.t))
 def test_41_reject_wrong_phase(self):
  r=report();r['phase']='S'
  with self.assertRaisesRegex(ValueError,'PHASE_NOT_T'):mod.triage_report(r,'c'*64)
 def test_42_reject_wrong_status(self):
  r=report();r['status']='FAILED'
  with self.assertRaisesRegex(ValueError,'STATUS_INVALID'):mod.triage_report(r,'c'*64)
 def test_43_reject_global_absence_claim(self):
  r=report();r['no_global_absence_claim']=False
  with self.assertRaisesRegex(ValueError,'GLOBAL_ABSENCE'):mod.triage_report(r,'c'*64)
 def test_44_reject_candidate_count(self):
  r=report();r['counts']['candidate_files']=2
  with self.assertRaisesRegex(ValueError,'CANDIDATE_COUNT'):mod.triage_report(r,'c'*64)
 def test_45_reject_unsearched_count(self):
  r=report();r['counts']['unsearched_documents']=2
  with self.assertRaisesRegex(ValueError,'UNSEARCHED_COUNT'):mod.triage_report(r,'c'*64)
 def test_46_reject_scan_errors_count(self):
  r=report();r['scan_errors']=[{'path':'x'}]
  with self.assertRaisesRegex(ValueError,'SCAN_ERROR_COUNT'):mod.triage_report(r,'c'*64)
 def test_47_reject_renderer_on(self):
  r=report();r['governance']['renderer']='ON'
  with self.assertRaisesRegex(ValueError,'GOVERNANCE_LOCK'):mod.triage_report(r,'c'*64)
 def test_48_reject_approved_binding(self):
  r=report();r['governance']['approved_bindings']=1
  with self.assertRaisesRegex(ValueError,'GOVERNANCE_LOCK'):mod.triage_report(r,'c'*64)
 def test_49_reject_duplicate_candidate(self):
  r=report();r['candidates'].append(candidate()) ; r['counts']['candidate_files']=2
  with self.assertRaisesRegex(ValueError,'PATH_DUPLICATE'):mod.triage_report(r,'c'*64)
 def test_50_reject_bad_sha(self):
  r=report();r['candidates'][0]['sha256']='xyz'
  with self.assertRaisesRegex(ValueError,'SHA256_INVALID'):mod.triage_report(r,'c'*64)
 def test_51_reject_negative_bytes(self):
  r=report();r['candidates'][0]['bytes']=-1
  with self.assertRaisesRegex(ValueError,'BYTES_INVALID'):mod.triage_report(r,'c'*64)
 def test_52_reject_changed_classification(self):
  r=report();r['candidates'][0]['classification']='AUTHORITY'
  with self.assertRaisesRegex(ValueError,'CLASSIFICATION_INVALID'):mod.triage_report(r,'c'*64)
 def test_53_reject_timing_conflict_changed(self):
  r=report();r['timing_conflicts'][0]['phase_duration_sum_seconds']=11
  with self.assertRaisesRegex(ValueError,'TIMING_CONFLICT_CHANGED'):mod.triage_report(r,'c'*64)
 def test_54_medium_priority(self): self.assertEqual(mod.classify_priority(candidate('misc/file.txt','renderer binding policy'))[0],'MEDIUM_REVIEW_PRIORITY')
 def test_55_low_priority_fallback(self): self.assertEqual(mod.classify_priority(candidate('misc/file.txt','example phrase with no scoring terms'))[0],'LOW_REVIEW_PRIORITY')
 def test_56_candidate_order_deterministic(self):
  r=report();r['candidates']=[candidate('z.md','example'),candidate('a.md','approved by director')];r['counts']['candidate_files']=2
  a=mod.triage_report(r,'c'*64); b=mod.triage_report(r,'c'*64)
  self.assertEqual([(x['path'],x['priority_score']) for x in a['candidates']],[(x['path'],x['priority_score']) for x in b['candidates']])
 def test_57_candidate_paths_are_unique(self):
  r=report();r['candidates']=[candidate(),candidate()];r['counts']['candidate_files']=2
  with self.assertRaisesRegex(ValueError,'PATH_DUPLICATE'):mod.triage_report(r,'c'*64)
 def test_58_unsearched_duplicate_rejected(self):
  r=report();r['unsearched_documents'].append(dict(r['unsearched_documents'][0]));r['counts']['unsearched_documents']=2
  with self.assertRaisesRegex(ValueError,'UNSEARCHED_PATH_DUPLICATE'):mod.triage_report(r,'c'*64)
 def test_59_unsearched_path_safe(self):
  r=report();r['unsearched_documents'][0]['path']='../outside.pdf'
  with self.assertRaisesRegex(ValueError,'UNSEARCHED_PATH_UNSAFE'):mod.triage_report(r,'c'*64)
 def test_60_human_checks_present(self): self.assertGreaterEqual(len(self.t['candidates'][0]['human_review_checks']),8)
if __name__=='__main__':
 result=unittest.main(verbosity=2,exit=False)
 ok=result.result.wasSuccessful()
 passed=result.result.testsRun-len(result.result.failures)-len(result.result.errors)
 print(f'PHASE_U_AUTHORITY_CANDIDATE_TRIAGE_TESTS={passed}/{result.result.testsRun}')
 raise SystemExit(0 if ok else 1)
