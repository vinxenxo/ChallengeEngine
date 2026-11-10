from pathlib import Path
import json, shutil, tempfile, unittest
import c11e_e4c_drill_composition_proposal as mod
ROOT=Path(__file__).resolve().parents[3]
class DrillCompositionProposalTests(unittest.TestCase):
 def test_schema_and_source_pins(self):
  r=mod.validate(ROOT); self.assertEqual(r['status'],'PASS_PROPOSAL_ONLY'); self.assertEqual(r['pinned_c11c_sources'],7)
 def test_partition_geometry(self):
  r=mod.validate(ROOT); self.assertEqual(r['geometry'],'720x1280 / 192px bands / 504x896 source viewport')
 def test_phase_offset_remains_unresolved(self):
  d=json.loads((ROOT/mod.PROPOSAL).read_text(encoding='utf-8')); self.assertEqual(d['phase_ownership']['payload_to_final_presentation_offset'],'UNRESOLVED_REQUIRES_EXPLICIT_D_OWNED_TIMEBASE_DECISION')
 def test_native_cta_ownership_preserved(self):
  d=json.loads((ROOT/mod.PROPOSAL).read_text(encoding='utf-8')); self.assertEqual(d['native_source_ownership']['native_visual_drill_end_cta'],'PRESERVED_INSIDE_SOURCE_FRAME_HEADER_DURING_END_CTA')
 def test_unapproved_status_and_no_renderer(self):
  d=json.loads((ROOT/mod.PROPOSAL).read_text(encoding='utf-8')); self.assertEqual(d['status'],'PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT'); self.assertFalse(d['approval_gates']['drill_composition_approved']); self.assertEqual(d['execution_boundary']['renderer'],'OFF')
 def test_negative_timebase_inference_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); shutil.copytree(ROOT/'definitions',root/'definitions'); shutil.copytree(ROOT/'core',root/'core')
   p=root/mod.PROPOSAL; d=json.loads(p.read_text(encoding='utf-8')); d['phase_ownership']['payload_to_final_presentation_offset']='90_FRAMES'; p.write_text(json.dumps(d),encoding='utf-8')
   with self.assertRaises(mod.ProposalError): mod.validate(root)
 def test_negative_renderer_activation_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); shutil.copytree(ROOT/'definitions',root/'definitions'); shutil.copytree(ROOT/'core',root/'core')
   p=root/mod.PROPOSAL; d=json.loads(p.read_text(encoding='utf-8')); d['approval_gates']['renderer_activation']=True; p.write_text(json.dumps(d),encoding='utf-8')
   with self.assertRaises(mod.ProposalError): mod.validate(root)
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(DrillCompositionProposalTests); result=unittest.TextTestRunner(verbosity=2).run(suite)
 print('C11E E4C DRILL COMPOSITION PROPOSAL '+('PASS' if result.wasSuccessful() else 'FAIL')+' | proposal_only=true | renderer=OFF | media_created=false | release_authority=NONE')
 raise SystemExit(not result.wasSuccessful())
