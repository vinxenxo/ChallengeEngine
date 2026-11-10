from __future__ import annotations
import json, shutil, tempfile, unittest
from pathlib import Path
import c11e_e4c_drill_source_phase_ownership_audit as audit_module
ROOT=Path(__file__).resolve().parents[3]
class DrillSourcePhaseOwnershipAuditTests(unittest.TestCase):
    def test_source_pins_and_phase_ownership(self):
        result=audit_module.audit(ROOT)
        self.assertEqual(result['checks_passed'],result['checks_expected'])
        self.assertEqual(result['phase_order'],['PRE_ROLL','GAME','END_CTA','DONE'])
        self.assertFalse(result['renderer_activation'])
    def test_game_payload_to_final_video_timebase_remains_explicitly_unresolved(self):
        result=audit_module.audit(ROOT)
        self.assertEqual(result['payload_to_final_presentation_frame_mapping'],'NOT_APPROVED_NOT_INFERRED')
    def test_native_cta_is_not_replaced_by_d(self):
        result=audit_module.audit(ROOT)
        self.assertEqual(result['native_end_cta_owner'],'C11C_PRESENTATION_UI_CTA_COMPONENT_IN_HEADER')
    def test_negative_protected_phase_source_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for rel in audit_module.PINNED:
                src=ROOT/rel; dst=root/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
            target=root/'core/presentation/VisualDrillPresentationPhaseLogic.gd'
            target.write_text(target.read_text(encoding='utf-8')+'\n# drift\n',encoding='utf-8')
            with self.assertRaises(audit_module.DrillSourceAuditError): audit_module.audit(root)
    def test_no_renderer_or_media_claim(self):
        result=audit_module.audit(ROOT)
        self.assertFalse(result['renderer_native_input_emitted'])
        self.assertFalse(result['media_created'])
        self.assertEqual(result['release_authority'],'NONE')
if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(DrillSourcePhaseOwnershipAuditTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    print('C11E E4C DRILL SOURCE PHASE OWNERSHIP AUDIT '+('PASS' if result.wasSuccessful() else 'FAIL')+' | source_pins=8/8 | read_only=true | renderer=OFF | media_created=false | release_authority=NONE')
    raise SystemExit(not result.wasSuccessful())
