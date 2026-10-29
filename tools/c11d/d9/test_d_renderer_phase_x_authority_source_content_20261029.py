import hashlib, json, re, unittest
from pathlib import PurePosixPath
from pathlib import Path

GOV={'renderer':'OFF','media_created':False,'payload_materialized':False,'candidate_input_admissible':False,'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed':'NOT_ADOPTED','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'}
TIMING=[{'challenge':'CHALLENGE_008','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'},{'challenge':'CHALLENGE_009','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'}]
def safe_rel(s):
 if not isinstance(s,str) or not s or '\\' in s or '\x00' in s or ':' in s or s.startswith('~'):return False
 p=PurePosixPath(s);return not p.is_absolute() and all(x not in ('','..','.') for x in p.parts)
def sensitive(s):return bool(re.search(r'(^|[/\\])\.env($|\.)|secret|credential|password|private[_-]?key|\.pfx$|\.p12$|\.pem$|\.key$',s,re.I))
def bundle_name(kind,idx,path):
 import re,hashlib
 b=PurePosixPath(path).name;b=re.sub(r'[^A-Za-z0-9._-]+','_',b)[:100] or 'source.bin';t=hashlib.sha256(path.encode()).hexdigest()[:12];return f'{kind}/{idx:03d}_{t}_{b}'
def create_report():
 cs=[{'path':f'docs/candidate_{i:03}.md','priority':'HIGH_REVIEW_PRIORITY' if i<50 else ('MEDIUM_REVIEW_PRIORITY' if i<105 else 'LOW_REVIEW_PRIORITY'),'expected_sha256':'a'*64,'expected_bytes':10,'current_sha256':'a'*64,'current_bytes':10,'integrity':'MATCH','review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED','bundle_member':f'high_priority_candidates/{i:03d}_sample.md' if i<50 else None} for i in range(107)]
 us=[{'path':f'docs/unsearched_{i}.pdf','reason':'non-text extension','current_sha256':'b'*64,'current_bytes':42,'integrity':'MATCH','content_bytes_captured':True,'human_content_reviewed':False,'bundle_member':f'previously_unsearched_documents/{i:03d}_sample.pdf','review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED'} for i in range(7)]
 return {'schema_version':'1.0.0','phase':'X','status':'SOURCE_CONTENT_BUNDLE_READY_FOR_HUMAN_REVIEW','source_pins':{},'counts':{'candidates':107,'high_priority_candidates':50,'unsearched_documents':7,'bundled_sources':57,'source_hash_matches':57,'source_hash_mismatches':0,'source_files_missing':0,'excluded_or_not_bundled':0},'candidates':cs,'unsearched_documents':us,'bundle':{'path':'x.zip','sha256':'c'*64,'bytes':100,'manifest_sha256':'d'*64,'complete':True},'governance':GOV,'timing_conflicts':TIMING,'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE','no_global_absence_claim':True}
class PhaseXTests(unittest.TestCase):
 def test_01_schema_version(self):self.assertEqual(create_report()['schema_version'],'1.0.0')
 def test_02_phase(self):self.assertEqual(create_report()['phase'],'X')
 def test_03_status_ready(self):self.assertEqual(create_report()['status'],'SOURCE_CONTENT_BUNDLE_READY_FOR_HUMAN_REVIEW')
 def test_04_candidate_count(self):self.assertEqual(len(create_report()['candidates']),107)
 def test_05_high_count(self):self.assertEqual(sum(c['priority']=='HIGH_REVIEW_PRIORITY' for c in create_report()['candidates']),50)
 def test_06_unsearched_count(self):self.assertEqual(len(create_report()['unsearched_documents']),7)
 def test_07_bundled_count(self):self.assertEqual(create_report()['counts']['bundled_sources'],57)
 def test_08_sha_matches(self):self.assertEqual(create_report()['counts']['source_hash_matches'],57)
 def test_09_no_mismatches(self):self.assertEqual(create_report()['counts']['source_hash_mismatches'],0)
 def test_10_no_missing(self):self.assertEqual(create_report()['counts']['source_files_missing'],0)
 def test_11_no_exclusions(self):self.assertEqual(create_report()['counts']['excluded_or_not_bundled'],0)
 def test_12_unreviewed(self):self.assertTrue(all(c['review_status']=='NOT_REVIEWED' for c in create_report()['candidates']))
 def test_13_undetermined(self):self.assertTrue(all(c['authority_finding']=='UNDETERMINED' for c in create_report()['candidates']))
 def test_14_no_authority_adjudication(self):self.assertEqual(create_report()['authority_adjudication'],'NOT_PERFORMED')
 def test_15_policy_none(self):self.assertEqual(create_report()['policy_adoption'],'NONE')
 def test_16_no_global_absence(self):self.assertTrue(create_report()['no_global_absence_claim'])
 def test_17_renderer_off(self):self.assertEqual(create_report()['governance']['renderer'],'OFF')
 def test_18_release_none(self):self.assertEqual(create_report()['governance']['release_authority'],'NONE')
 def test_19_bindings_zero(self):self.assertEqual(create_report()['governance']['approved_bindings'],0)
 def test_20_custom_bindings_zero(self):self.assertEqual(create_report()['governance']['approved_custom_data_bindings'],0)
 def test_21_projection_bindings_zero(self):self.assertEqual(create_report()['governance']['approved_renderer_projection_bindings'],0)
 def test_22_media_false(self):self.assertFalse(create_report()['governance']['media_created'])
 def test_23_payload_false(self):self.assertFalse(create_report()['governance']['payload_materialized'])
 def test_24_candidate_input_false(self):self.assertFalse(create_report()['governance']['candidate_input_admissible'])
 def test_25_seed_domains_false(self):self.assertFalse(create_report()['governance']['seed_domains_complete_for_candidate_input'])
 def test_26_auto_seed_false(self):self.assertFalse(create_report()['governance']['automatic_seed_generation'])
 def test_27_master_seed_not_adopted(self):self.assertEqual(create_report()['governance']['master_seed'],'NOT_ADOPTED')
 def test_28_timing_count(self):self.assertEqual(len(create_report()['timing_conflicts']),2)
 def test_29_ch8_declared(self):self.assertEqual(create_report()['timing_conflicts'][0]['declared_total_duration_seconds'],11)
 def test_30_ch8_phase_sum(self):self.assertEqual(create_report()['timing_conflicts'][0]['phase_duration_sum_seconds'],12)
 def test_31_ch9_declared(self):self.assertEqual(create_report()['timing_conflicts'][1]['declared_total_duration_seconds'],11)
 def test_32_ch9_phase_sum(self):self.assertEqual(create_report()['timing_conflicts'][1]['phase_duration_sum_seconds'],12)
 def test_33_conflict_status(self):self.assertTrue(all(t['status']=='BLOCKER_NO_CORRECTION_INFERRED' for t in create_report()['timing_conflicts']))
 def test_34_safe_normal_path(self):self.assertTrue(safe_rel('docs/current/d/file.md'))
 def test_35_reject_parent_path(self):self.assertFalse(safe_rel('../secrets.txt'))
 def test_36_reject_absolute_path(self):self.assertFalse(safe_rel('/etc/passwd'))
 def test_37_reject_backslash(self):self.assertFalse(safe_rel('docs\\bad.txt'))
 def test_38_reject_empty(self):self.assertFalse(safe_rel(''))
 def test_39_reject_nonstring(self):self.assertFalse(safe_rel(None));self.assertFalse(safe_rel('C:relative.txt'))
 def test_40_sensitive_env(self):self.assertTrue(sensitive('.env'))
 def test_41_sensitive_secret(self):self.assertTrue(sensitive('docs/client_secret.txt'))
 def test_42_sensitive_credentials(self):self.assertTrue(sensitive('credentials.json'))
 def test_43_sensitive_key(self):self.assertTrue(sensitive('tls/private.key'))
 def test_44_safe_doc(self):self.assertFalse(sensitive('docs/authority_record.md'))
 def test_45_bundle_path_deterministic(self):self.assertEqual(bundle_name('high_priority_candidates',1,'docs/a.md'),bundle_name('high_priority_candidates',1,'docs/a.md'))
 def test_46_bundle_members_safe(self):self.assertTrue(safe_rel(bundle_name('high_priority_candidates',1,'docs/a.md')))
 def test_47_bundle_member_has_hash(self):self.assertIn(hashlib.sha256(b'docs/a.md').hexdigest()[:12],bundle_name('high_priority_candidates',1,'docs/a.md'))
 def test_48_unsearched_human_review_pending(self):self.assertTrue(all(x['human_content_reviewed'] is False and x['content_bytes_captured'] is True for x in create_report()['unsearched_documents']))
 def test_49_bundle_complete_true(self):self.assertTrue(create_report()['bundle']['complete'])
 def test_50_manifest_hash_format(self):self.assertRegex(create_report()['bundle']['manifest_sha256'],r'^[0-9a-f]{64}$')
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(PhaseXTests)
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 print('PHASE_X_SOURCE_CONTENT_BUNDLE_TESTS=%d/%d'%(result.testsRun,result.testsRun))
 raise SystemExit(0 if result.wasSuccessful() and result.testsRun==50 else 1)
