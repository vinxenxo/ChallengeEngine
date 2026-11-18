from __future__ import annotations
import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'definitions/c11e/test_only/C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.json'
sys.path.insert(0,str(ROOT/'tools/c11d/d9'))
import c11e_e6_smoke18_family_editorial_fixture_audit_v1 as audit

class FamilyEditorialFixtureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.obj=json.loads(FIX.read_text(encoding='utf-8'))
 def test_01_schema(self): self.assertEqual(self.obj['schema'],'C11E-E6-SMOKE18-FAMILY-EDITORIAL-FIXTURE-V1')
 def test_02_fixture_test_only(self): self.assertEqual(self.obj['fixture_scope']['data_classification'],'SYNTHETIC_TEST_ONLY')
 def test_03_defaults_not_mutated(self):
  s=self.obj['fixture_scope']; self.assertFalse(s['product_defaults_mutated']); self.assertFalse(s['canonical_definitions_mutated']); self.assertFalse(s['e1_request_defaults_mutated'])
 def test_04_three_families(self): self.assertEqual(set(self.obj['family_fixtures']),{'challenge','visual_loop','visual_drill'})
 def test_05_each_family_has_three_fields(self):
  for x in self.obj['family_fixtures'].values():
   for k in ('title','subtitle','call_to_action'): self.assertTrue(x[k].strip())
 def test_06_copy_has_e6_marker(self):
  for x in self.obj['family_fixtures'].values(): self.assertIn('E6',x['title'])
 def test_07_titles_differ(self): self.assertEqual(len({x['title'] for x in self.obj['family_fixtures'].values()}),3)
 def test_08_subtitles_differ(self): self.assertEqual(len({x['subtitle'] for x in self.obj['family_fixtures'].values()}),3)
 def test_09_ctas_differ(self): self.assertEqual(len({x['call_to_action'] for x in self.obj['family_fixtures'].values()}),3)
 def test_10_row_count(self): self.assertEqual(len(self.obj['rows']),18)
 def test_11_challenge_rows_six(self): self.assertEqual(sum(x['family']=='challenge' for x in self.obj['rows']),6)
 def test_12_loop_rows_six(self): self.assertEqual(sum(x['family']=='visual_loop' for x in self.obj['rows']),6)
 def test_13_drill_rows_six(self): self.assertEqual(sum(x['family']=='visual_drill' for x in self.obj['rows']),6)
 def test_14_challenge_selectors_exact(self):
  self.assertEqual([x['selector'] for x in self.obj['rows'] if x['family']=='challenge'],['CHALLENGE_001','CHALLENGE_002','CHALLENGE_004','CHALLENGE_005','CHALLENGE_006','CHALLENGE_007'])
 def test_15_challenge_three_nested_probes(self):
  for x in self.obj['rows']:
   if x['family']=='challenge': self.assertEqual(x['probe_targets'],['A','B_REPEAT','C_CHANGED_MUSIC_SEED'])
 def test_16_loop_six_identified(self): self.assertEqual(len([x for x in self.obj['rows'] if x['family']=='visual_loop']),6)
 def test_17_drill_six_identified(self): self.assertEqual(len([x for x in self.obj['rows'] if x['family']=='visual_drill']),6)
 def test_18_target_count_30(self): self.assertEqual(sum(len(x['probe_targets']) for x in self.obj['rows']),30)
 def test_19_family_target_counts(self):
  self.assertEqual({f:sum(len(x['probe_targets']) for x in self.obj['rows'] if x['family']==f) for f in ('challenge','visual_loop','visual_drill')},{'challenge':18,'visual_loop':6,'visual_drill':6})
 def test_20_challenge_player_blocked(self): self.assertIn('UNKNOWN',self.obj['fixture_scope']['challenge_player_name'])
 def test_21_challenge_label_blocked(self): self.assertIn('UNKNOWN',self.obj['fixture_scope']['challenge_label'])
 def test_22_e1_personalization_off(self): self.assertFalse(self.obj['fixture_scope']['e1_personalization_enabled'])
 def test_23_music_not_changed(self): self.assertTrue(self.obj['challenge_probe_contract']['music_seed_isolation_is_unchanged'])
 def test_24_gameplay_identity_unchanged(self): self.assertTrue(self.obj['challenge_probe_contract']['same_gameplay_identity_across_A_B_C'])
 def test_25_prepare_only(self): self.assertTrue(self.obj['execution_boundary']['plan_generation_only'])
 def test_26_media_not_authorized(self):
  b=self.obj['execution_boundary']; self.assertFalse(b['e6_test_only_authorized']); self.assertFalse(b['godot_invoked']); self.assertFalse(b['ffmpeg_invoked']); self.assertFalse(b['ffprobe_invoked'])
 def test_27_release_none(self): self.assertEqual(self.obj['execution_boundary']['release_authority'],'NONE')
 def test_28_d4_8_blocked(self): self.assertEqual(self.obj['execution_boundary']['d4_8'],'BLOCKED')
 def test_29_plan_generation_counts(self):
  p=audit.build_plan(self.obj,{'fixture':{'sha256':'0'*64}}); self.assertEqual(p['top_level_rows_actual'],18); self.assertEqual(p['editorial_targets_actual'],30)
 def test_30_plan_family_counts(self):
  p=audit.build_plan(self.obj,{'fixture':{'sha256':'0'*64}}); self.assertEqual(p['family_counts'],{'challenge':6,'visual_loop':6,'visual_drill':6})
 def test_31_challenge_same_text_all_probes(self):
  p=audit.build_plan(self.obj,{'fixture':{'sha256':'0'*64}})
  for row in p['rows']:
   if row['family']=='challenge':
    for target in row['targets']: self.assertEqual(target['editorial'],row['editorial'])
 def test_32_loop_single_scenario_target(self):
  p=audit.build_plan(self.obj,{'fixture':{'sha256':'0'*64}})
  for row in p['rows']:
   if row['family']=='visual_loop': self.assertEqual(len(row['targets']),1)
 def test_33_drill_single_scenario_target(self):
  p=audit.build_plan(self.obj,{'fixture':{'sha256':'0'*64}})
  for row in p['rows']:
   if row['family']=='visual_drill': self.assertEqual(len(row['targets']),1)
 def test_34_plan_does_not_claim_runtime_consumption(self):
  p=audit.build_plan(self.obj,{'fixture':{'sha256':'0'*64}}); self.assertIn('NOT_PROVEN',p['runtime_consumption']['challenge']); self.assertIn('BLOCKED',p['runtime_consumption']['visual_loop'])

if __name__=='__main__': unittest.main(verbosity=2)
