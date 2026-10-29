#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, tempfile, unittest, zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
TOOL=HERE/'review_d_renderer_phase_ac_remaining_authority_candidates_20261029_v1.py'
spec=importlib.util.spec_from_file_location('phase_ac_generator',TOOL)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class PhaseACTests(unittest.TestCase):
 def make(self, root):
  root=Path(root); (root/'repo').mkdir(exist_ok=True); data={}; candidates=[]
  for i in range(107):
   if i<50: priority='HIGH_REVIEW_PRIORITY'; label='high'
   elif i<105: priority='MEDIUM_REVIEW_PRIORITY'; label='medium'
   else: priority='LOW_REVIEW_PRIORITY'; label='low'
   rel=f'docs/source_{i:03d}.md'; raw=(f'candidate {i} {label}\n').encode()
   if priority!='HIGH_REVIEW_PRIORITY':
    p=root/'repo'/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(raw); data[rel]=raw
   candidates.append({'path':rel,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'priority':priority,'priority_score':i,'priority_signals':[label]})
  triage={'phase':'U','status':'CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW','no_global_absence_claim':True,
   'counts':{'candidates':107,'high_priority':50,'medium_priority':55,'low_priority':2,'unsearched_documents':7,'scan_errors':0},
   'governance':{'renderer':'OFF','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'},
   'candidates':candidates}
  return root/'repo',triage,data
 def test_01_safe_relative(self): self.assertTrue(mod.safe_relpath('docs/current/a.md'))
 def test_02_reject_absolute_slash(self): self.assertFalse(mod.safe_relpath('/docs/a'))
 def test_03_reject_parent(self): self.assertFalse(mod.safe_relpath('../a'))
 def test_04_reject_windows_drive(self): self.assertFalse(mod.safe_relpath('C:/a'))
 def test_05_reject_empty(self): self.assertFalse(mod.safe_relpath(''))
 def test_06_phase_required(self):
  with self.assertRaisesRegex(ValueError,'PHASE_U_TRIAGE_STATUS_INVALID'): mod.select_remaining({'phase':'X'})
 def test_07_phase_invalid_raises(self):
  with self.assertRaisesRegex(ValueError,'PHASE_U_TRIAGE_STATUS_INVALID'): mod.select_remaining({'phase':'X','status':'x'})
 def test_08_count_all_required(self):
  with self.assertRaisesRegex(ValueError,'PHASE_U_COUNT_MISMATCH_candidates'):
   x={'phase':'U','status':'CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW','no_global_absence_claim':True,'counts':{'candidates':1}}
   mod.select_remaining(x)
 def test_09_global_absence_claim_false_rejected(self):
  with self.assertRaisesRegex(ValueError,'PHASE_U_GLOBAL_ABSENCE_SCOPE_INVALID'):
   x={'phase':'U','status':'CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW','no_global_absence_claim':False}; mod.select_remaining(x)
 def test_10_governance_renderer_off_required(self):
  root,triage,_=self.make(Path(tempfile.mkdtemp())); triage['governance']['renderer']='ON'
  with self.assertRaisesRegex(ValueError,'PHASE_U_GOVERNANCE_LOCK_MISMATCH'): mod.select_remaining(triage)
 def test_11_approved_binding_zero_required(self):
  root,triage,_=self.make(Path(tempfile.mkdtemp())); triage['governance']['approved_bindings']=1
  with self.assertRaisesRegex(ValueError,'PHASE_U_GOVERNANCE_LOCK_MISMATCH'): mod.select_remaining(triage)
 def test_12_missing_source_candidate_list(self):
  with self.assertRaisesRegex(ValueError,'PHASE_U_CANDIDATES_INVALID'):
   mod.select_remaining({'phase':'U','status':'CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW','no_global_absence_claim':True,'counts':{'candidates':107,'high_priority':50,'medium_priority':55,'low_priority':2,'unsearched_documents':7,'scan_errors':0},'governance':{'renderer':'OFF','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'},'candidates':[]})
 def test_13_selects_exact_57(self):
  _,t,_=self.make(Path(tempfile.mkdtemp())); self.assertEqual(len(mod.select_remaining(t)),57)
 def test_14_selects_55_medium(self):
  _,t,_=self.make(Path(tempfile.mkdtemp())); self.assertEqual(sum(x['priority']=='MEDIUM_REVIEW_PRIORITY' for x in mod.select_remaining(t)),55)
 def test_15_selects_2_low(self):
  _,t,_=self.make(Path(tempfile.mkdtemp())); self.assertEqual(sum(x['priority']=='LOW_REVIEW_PRIORITY' for x in mod.select_remaining(t)),2)
 def test_16_excludes_high(self):
  _,t,_=self.make(Path(tempfile.mkdtemp())); self.assertTrue(all(x['priority']!='HIGH_REVIEW_PRIORITY' for x in mod.select_remaining(t)))
 def test_17_duplicate_path_rejected(self):
  _,t,_=self.make(Path(tempfile.mkdtemp())); t['candidates'][1]['path']=t['candidates'][0]['path']
  with self.assertRaisesRegex(ValueError,'CANDIDATE_PATH_DUPLICATE'): mod.select_remaining(t)
 def test_18_bad_sha_rejected(self):
  _,t,_=self.make(Path(tempfile.mkdtemp())); t['candidates'][50]['sha256']='bad'
  with self.assertRaisesRegex(ValueError,'CANDIDATE_SHA256_INVALID'): mod.select_remaining(t)
 def test_19_bad_size_rejected(self):
  _,t,_=self.make(Path(tempfile.mkdtemp())); t['candidates'][50]['bytes']=True
  with self.assertRaisesRegex(ValueError,'CANDIDATE_BYTES_INVALID'): mod.select_remaining(t)
 def test_20_priority_distribution_rejected(self):
  _,t,_=self.make(Path(tempfile.mkdtemp())); t['candidates'][50]['priority']='LOW_REVIEW_PRIORITY'
  with self.assertRaisesRegex(ValueError,'PHASE_U_PRIORITY_DISTRIBUTION_MISMATCH'): mod.select_remaining(t)
 def test_21_bundle_preserves_raw_bytes(self):
  base=Path(tempfile.mkdtemp()); root,t,data=self.make(base); triage_sha=mod.EXPECTED_TRIAGE_SHA256
  out=base/'r.json'; md=base/'r.md'; zpath=base/'sources.zip'; result=mod.build_bundle(root,t,triage_sha,out,md,zpath)
  with zipfile.ZipFile(zpath) as z:
   for rel,raw in data.items(): self.assertEqual(z.read('sources/'+rel),raw)
 def test_22_bundle_count_58_members(self):
  base=Path(tempfile.mkdtemp()); root,t,_=self.make(base); mod.build_bundle(root,t,mod.EXPECTED_TRIAGE_SHA256,base/'r.json',base/'r.md',base/'sources.zip')
  with zipfile.ZipFile(base/'sources.zip') as z: self.assertEqual(len(z.namelist()),58)
 def test_23_bundle_crc_passes(self):
  base=Path(tempfile.mkdtemp()); root,t,_=self.make(base); mod.build_bundle(root,t,mod.EXPECTED_TRIAGE_SHA256,base/'r.json',base/'r.md',base/'sources.zip')
  with zipfile.ZipFile(base/'sources.zip') as z: self.assertIsNone(z.testzip())
 def test_24_missing_medium_source_fails(self):
  base=Path(tempfile.mkdtemp()); root,t,_=self.make(base); (root/'docs/source_050.md').unlink()
  with self.assertRaisesRegex(ValueError,'CANDIDATE_SOURCE_MISSING'): mod.build_bundle(root,t,mod.EXPECTED_TRIAGE_SHA256,base/'r.json',base/'r.md',base/'sources.zip')
 def test_25_changed_medium_hash_fails(self):
  base=Path(tempfile.mkdtemp()); root,t,_=self.make(base); (root/'docs/source_050.md').write_text('changed')
  with self.assertRaisesRegex(ValueError,'CANDIDATE_SOURCE_SIZE_MISMATCH|CANDIDATE_SOURCE_SHA256_MISMATCH'): mod.build_bundle(root,t,mod.EXPECTED_TRIAGE_SHA256,base/'r.json',base/'r.md',base/'sources.zip')
 def test_26_size_tamper_fails(self):
  base=Path(tempfile.mkdtemp()); root,t,_=self.make(base); t['candidates'][50]['bytes']+=1
  with self.assertRaisesRegex(ValueError,'CANDIDATE_SOURCE_SIZE_MISMATCH'): mod.build_bundle(root,t,mod.EXPECTED_TRIAGE_SHA256,base/'r.json',base/'r.md',base/'sources.zip')
 def test_27_triad_sha_wrong_fails(self):
  base=Path(tempfile.mkdtemp()); root,t,_=self.make(base)
  with self.assertRaisesRegex(ValueError,'PHASE_U_TRIAGE_SHA256_MISMATCH'): mod.build_bundle(root,t,'0'*64,base/'r.json',base/'r.md',base/'sources.zip')
 def test_28_outputs_must_not_exist(self):
  base=Path(tempfile.mkdtemp()); root,t,_=self.make(base); (base/'r.json').write_text('old')
  with self.assertRaisesRegex(ValueError,'OUTPUT_DESTINATION_EXISTS'): mod.build_bundle(root,t,mod.EXPECTED_TRIAGE_SHA256,base/'r.json',base/'r.md',base/'sources.zip')
 def test_29_report_counts_and_locks(self):
  base=Path(tempfile.mkdtemp()); root,t,_=self.make(base); r=mod.build_bundle(root,t,mod.EXPECTED_TRIAGE_SHA256,base/'r.json',base/'r.md',base/'sources.zip')
  self.assertEqual(r['counts']['bundled_sources'],57); self.assertEqual(r['authority_adjudication'],'NOT_PERFORMED'); self.assertEqual(r['hard_locks']['renderer'],'OFF')
 def test_30_markdown_reports_remaining_scope(self):
  base=Path(tempfile.mkdtemp()); root,t,_=self.make(base); mod.build_bundle(root,t,mod.EXPECTED_TRIAGE_SHA256,base/'r.json',base/'r.md',base/'sources.zip')
  md=(base/'r.md').read_text(); self.assertIn('55 medium-priority and 2 low-priority',md); self.assertIn('no global absence claim',md)

if __name__=='__main__':
 suite=unittest.main(exit=False, verbosity=2)
 if not suite.result.wasSuccessful(): raise SystemExit(1)
 print('PHASE_AC_REMAINING_CANDIDATE_REVIEW_TESTS=30/30')
