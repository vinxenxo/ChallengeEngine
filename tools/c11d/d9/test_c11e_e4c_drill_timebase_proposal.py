from pathlib import Path
import json, shutil, tempfile, unittest
import c11e_e4c_drill_timebase_proposal as mod
ROOT=Path(__file__).resolve().parents[3]
class DrillTimebaseProposalTests(unittest.TestCase):
 def _copy(self,td):
  root=Path(td)
  for d in ('core','definitions','docs/current/e'):
   shutil.copytree(ROOT/d,root/d)
  return root
 def test_schema_source_pins_and_proposed_state(self):
  r=mod.validate(ROOT); self.assertEqual(r['status'],'PASS_PROPOSAL_ONLY'); self.assertEqual(r['source_pins'],len(mod.SOURCE_PINS))
 def test_exact_30fps_phase_counts(self):
  self.assertEqual(mod.countdown_frames(30),90); self.assertEqual(mod.end_cta_frames(30),90)
 def test_game_payload_first_and_last_frame_mapping(self):
  self.assertEqual(mod.map_player_frame_to_final('GAME',0,630,30)['final_presentation_frame_index'],90)
  self.assertEqual(mod.map_player_frame_to_final('GAME',629,630,30)['final_presentation_frame_index'],719)
 def test_half_open_game_window_maps_to_final_interval(self):
  a=mod.map_player_frame_to_final('GAME',0,630,30); b=mod.map_player_frame_to_final('GAME',629,630,30)
  self.assertEqual(b['final_presentation_frame_index']-a['final_presentation_frame_index']+1,630)
 def test_pre_roll_indices_are_global_and_d_editorial_suppressed(self):
  r=mod.map_player_frame_to_final('PRE_ROLL',89,630,30); self.assertEqual(r['final_presentation_frame_index'],89); self.assertFalse(r['d_editorial_visible']); self.assertEqual(r['source_frame_index'],0)
 def test_end_cta_indices_are_global_native_last_frame_and_d_suppressed(self):
  r=mod.map_player_frame_to_final('END_CTA',720,630,30); self.assertEqual(r['final_presentation_frame_index'],720); self.assertEqual(r['source_frame_index'],629); self.assertFalse(r['d_editorial_visible'])
 def test_total_frame_count_preserves_three_second_phases(self):
  self.assertEqual(mod.countdown_frames(30)+630+mod.end_cta_frames(30),810)
 def test_invalid_indices_and_phase_are_rejected(self):
  with self.assertRaises(mod.TimebaseProposalError): mod.map_player_frame_to_final('GAME',630,630,30)
  with self.assertRaises(mod.TimebaseProposalError): mod.map_player_frame_to_final('PRE_ROLL',90,630,30)
  with self.assertRaises(mod.TimebaseProposalError): mod.map_player_frame_to_final('UNKNOWN',0,630,30)
 def test_negative_protected_source_drift(self):
  with tempfile.TemporaryDirectory() as td:
   root=self._copy(td); f=root/'core/presentation/VisualDrillPresentationPhaseLogic.gd'; f.write_text(f.read_text()+'\n# drift\n')
   with self.assertRaises(mod.TimebaseProposalError): mod.validate(root)
 def test_negative_proposal_cannot_be_approved_or_change_mapping(self):
  with tempfile.TemporaryDirectory() as td:
   root=self._copy(td); p=root/mod.PROPOSAL; d=json.loads(p.read_text()); d['approval']['timebase_mapping_approved']=True; p.write_text(json.dumps(d))
   with self.assertRaises(mod.TimebaseProposalError): mod.validate(root)
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(DrillTimebaseProposalTests); result=unittest.TextTestRunner(verbosity=2).run(suite)
 print('C11E E4C DRILL TIMEBASE PROPOSAL '+('PASS' if result.wasSuccessful() else 'FAIL')+' | proposal_only=true | renderer=OFF | media_created=false | release_authority=NONE')
 raise SystemExit(not result.wasSuccessful())
