from __future__ import annotations
import hashlib, json, shutil, tempfile, unittest
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
import d_renderer_visual_loop_geometric_request_chain_gap_audit as audit
ROOT=Path(__file__).resolve().parents[3]

class VisualLoopGeometricRequestChainGapAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract,cls.schema,cls.report_schema=audit.load_contract(ROOT)
        cls.report=audit.run_audit(ROOT)

    def test_contract_is_strict_and_not_self_approving(self):
        self.assertEqual(self.contract['status'],'PREPARATION_ONLY_CANONICAL_REQUEST_TO_BINDING_GAP_AUDIT_NOT_ADMISSION')
        self.assertIs(self.contract['candidate_input_admissible'],False)
        self.assertFalse(self.contract['approval_state']['timing_review_inheritance_approved'])
        self.assertEqual(len(self.contract['source_lineage']),13)

    def test_matrix_registry_and_contract_have_same_exact_five_grammars(self):
        expected=['harmonic_membrane','interference_plane','parametric_ribbon','lattice_wave','orbital_wave']
        self.assertEqual(self.contract['scope']['expected_grammar_ids'],expected)
        self.assertEqual([x['grammar_id'] for x in self.report['cases']],expected)

    def test_canonical_d99_plans_all_five_selectors(self):
        self.assertTrue(all(x['canonical_plan_status']=='PLANNED' for x in self.report['cases']))
        self.assertTrue(all(x['canonical_selection']['subtype_id']==x['grammar_id'] for x in self.report['cases']))

    def test_existing_v1_source_binding_stays_one_of_five(self):
        good=[x for x in self.report['cases'] if x['request_scoped_source_binding_status']==audit.BOUND_STATUS]
        blocked=[x for x in self.report['cases'] if x['request_scoped_source_binding_status']==audit.BLOCKED_STATUS]
        self.assertEqual([x['grammar_id'] for x in good],['harmonic_membrane'])
        self.assertEqual([x['grammar_id'] for x in blocked],self.contract['scope']['current_blocked_grammar_ids'])

    def test_four_rejections_are_the_exact_fixed_timing_review_guard(self):
        for item in self.report['cases']:
            if item['grammar_id']=='harmonic_membrane':
                self.assertIsNone(item['request_scoped_source_binding_error'])
            else:
                self.assertTrue(item['request_scoped_source_binding_error'].startswith(self.contract['scope']['blocked_reason_prefix']))
                self.assertIn(repr(item['grammar_id']),item['request_scoped_source_binding_error'])

    def test_report_schema_self_hash_and_governance_locks(self):
        self.assertEqual(self.report['audit_sha256'],audit._sha_json({k:v for k,v in self.report.items() if k!='audit_sha256'}))
        self.assertFalse(self.report['governance']['payload_instance_materialized'])
        self.assertFalse(self.report['governance']['renderer_dispatch_invoked'])
        self.assertFalse(self.report['governance']['media_created'])
        self.assertEqual(self.report['governance']['renderer'],'OFF')
        self.assertEqual(self.report['governance']['D4.8'],'BLOCKED')
        self.assertEqual(self.report['governance']['release_authority'],'NONE')

    def test_report_is_deterministic(self):
        second=audit.run_audit(ROOT)
        self.assertEqual(self.report,second)

    def test_source_drift_fails_closed(self):
        with tempfile.TemporaryDirectory(prefix='c11d-grammar-chain-gap-') as tmp:
            root=Path(tmp)
            for row in self.contract['source_lineage']:
                src=ROOT/row['path']; dest=root/row['path']; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dest)
            for rel in (audit.CONTRACT_REL,audit.CONTRACT_SCHEMA_REL,audit.REPORT_SCHEMA_REL):
                dest=root/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/rel,dest)
            victim=root/'tools/c11d/d9/universal_producer.py'
            victim.write_bytes(victim.read_bytes()+b'\n# controlled drift\n')
            with self.assertRaisesRegex(audit.RequestChainGapAuditError,'Pinned source drift'):
                audit.load_contract(root)

    def test_auto_and_unknown_grammar_are_never_counted_as_admitted(self):
        self.assertNotIn('auto',self.contract['scope']['expected_grammar_ids'])
        self.assertNotIn('unknown_grammar',self.contract['scope']['expected_grammar_ids'])
        self.assertEqual(self.report['summary']['source_binding_review_passes'],'1/5')

    def test_tool_is_read_only_and_does_not_launch_godot(self):
        source=(HERE/'d_renderer_visual_loop_geometric_request_chain_gap_audit.py').read_text(encoding='utf-8')
        self.assertNotIn('import subprocess',source)
        self.assertNotIn('subprocess.run',source)
        self.assertNotIn('write_text(',source)
        self.assertNotIn('write_bytes(',source)
        self.assertNotIn('ShaderMaterial.new',source)
        self.assertNotIn('renderer_dispatch_invoked":True',source)

if __name__=='__main__': unittest.main(verbosity=2)
