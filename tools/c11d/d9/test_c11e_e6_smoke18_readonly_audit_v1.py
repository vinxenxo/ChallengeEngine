import unittest
import c11e_e6_smoke18_readonly_audit_v1 as audit

class E6ReadOnlyAuditContractTests(unittest.TestCase):
    def test_frozen_manifest_pin_is_canonical(self):
        self.assertEqual(len(audit.FROZEN_SHA),64)
        self.assertEqual(audit.SOURCE_PINS['release/C11C_FREEZE_PACKAGE_MANIFEST.json'],audit.FROZEN_SHA)
    def test_d4_8_policy_explicitly_blocks_smoke18_and_audio(self):
        p={'status':'APPROVED_BOUNDED_R1V_QUALIFICATION_ONLY','execution':{'launcher_invocations_exact':10},'scope':{'allowed_selector_count':5},'forbidden':{'smoke18_or_matrix99':True,'d3_music_engine':True,'pcm_audio_generation':True,'ffmpeg_filter_or_mux':True},'allowances':{'audio_or_music_generation':False,'ffmpeg_mux':False},'authority_boundary':{'general_d4_8_production':'BLOCKED'}}
        self.assertTrue(audit.evaluate_policy(p)['valid'])
    def test_policy_mismatch_fails_closed(self):
        p={'status':'APPROVED_BOUNDED_R1V_QUALIFICATION_ONLY','execution':{'launcher_invocations_exact':10},'scope':{'allowed_selector_count':5},'forbidden':{'smoke18_or_matrix99':False,'d3_music_engine':True,'pcm_audio_generation':True,'ffmpeg_filter_or_mux':True},'allowances':{'audio_or_music_generation':False,'ffmpeg_mux':False},'authority_boundary':{'general_d4_8_production':'BLOCKED'}}
        self.assertFalse(audit.evaluate_policy(p)['valid'])
    def test_drill_matrix_has_six_distinct_receipt_paths(self):
        self.assertEqual(len(audit.DRILL_CANDIDATES),6)
        self.assertEqual(len({x['path'] for x in audit.DRILL_CANDIDATES}),6)
    def test_loop_matrix_has_six_distinct_scenarios(self):
        self.assertEqual(len(audit.LOOP_CANDIDATES),6)
        self.assertEqual(len({(x['family_id'],x['grammar_id']) for x in audit.LOOP_CANDIDATES}),6)
    def test_challenge_pool_keeps_008_and_009_out(self):
        self.assertEqual(audit.CHALLENGE_PATHS,[f'challenges/CHALLENGE_{i:03d}.json' for i in range(1,8)])
        self.assertNotIn('challenges/CHALLENGE_008.json',audit.CHALLENGE_PATHS)
    def test_challenge_matrix_not_falsely_frozen(self):
        # Six of seven candidates require an explicit selection rule; this audit must not invent one.
        self.assertEqual(len(audit.CHALLENGE_PATHS),7)
    def test_source_pin_literals_are_sha256(self):
        self.assertTrue(all(len(v)==64 and all(c in '0123456789abcdef' for c in v) for v in audit.SOURCE_PINS.values()))
    def test_no_media_or_subprocess_dependency(self):
        import inspect
        source=inspect.getsource(audit)
        self.assertNotIn('subprocess.',source)
        self.assertNotIn('ffmpeg -',source.lower())
        self.assertNotIn('godot --',source.lower())
    def test_e6_reuse_requires_contract(self):
        self.assertTrue(all(x['evidence'] for x in audit.LOOP_CANDIDATES))
        self.assertTrue(all(x['sha256'] for x in audit.DRILL_CANDIDATES))

if __name__=='__main__':
    unittest.main(verbosity=2)
