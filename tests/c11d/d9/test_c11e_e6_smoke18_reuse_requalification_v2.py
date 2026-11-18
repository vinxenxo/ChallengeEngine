import json, pathlib, tempfile, unittest, sys, hashlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'tools' / 'c11d' / 'd9'))
import validate_c11e_e6_smoke18_reuse_requalification_v2 as v

class RequalificationLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=pathlib.Path(__file__).resolve().parents[3]/'definitions/c11d/production/C11E_E6_SMOKE18_EVIDENCE_REUSE_REQUALIFIED_DRAFT_V2.json'
        cls.obj=json.loads(p.read_text(encoding='utf-8'))
    def test_01_schema_exact(self): self.assertEqual(self.obj['schema'],'C11E-E6-SMOKE18-EVIDENCE-REUSE-REQUALIFICATION-DRAFT-V2')
    def test_02_status_not_frozen(self): self.assertIn('NOT_FROZEN',self.obj['status'])
    def test_03_status_not_accepted(self): self.assertIn('NOT_E6_ACCEPTED',self.obj['status'])
    def test_04_total_18(self): self.assertEqual(len(self.obj['smoke18_scenarios']),18)
    def test_05_six_challenges(self): self.assertEqual(sum(x['family']=='challenge' for x in self.obj['smoke18_scenarios']),6)
    def test_06_six_loops(self): self.assertEqual(sum(x['family']=='visual_loop' for x in self.obj['smoke18_scenarios']),6)
    def test_07_six_drills(self): self.assertEqual(sum(x['family']=='visual_drill' for x in self.obj['smoke18_scenarios']),6)
    def test_08_reuse_candidates_13(self): self.assertEqual(self.obj['summary']['reuse_candidates_total'],13)
    def test_09_e6_accepted_zero(self): self.assertEqual(self.obj['summary']['e6_accepted_scenarios'],0)
    def test_10_d4_8_blocked(self): self.assertEqual(self.obj['governance']['d4_8'],'BLOCKED_PINNED_R1V_ONLY')
    def test_11_release_none(self): self.assertEqual(self.obj['governance']['release_authority'],'NONE')
    def test_12_no_media_authority(self): self.assertFalse(self.obj['governance']['e6_media_authorized'])
    def test_13_ch004_semantic_v4_pin(self):
        x=next(x for x in self.obj['smoke18_scenarios'] if x['scenario_id']=='E6-CH-004')
        self.assertEqual(x['reuse_evidence']['semantic_review_v4']['sha256'],v.EXPECTED_CH004_V4)
    def test_14_ch004_not_accepted(self):
        x=next(x for x in self.obj['smoke18_scenarios'] if x['scenario_id']=='E6-CH-004')
        self.assertEqual(x['ledger_reuse_disposition'],'ELIGIBLE_FOR_E6_LEDGER_REQUALIFICATION_NOT_ACCEPTED')
    def test_15_loop22_a_sha(self):
        x=next(x for x in self.obj['smoke18_scenarios'] if x['scenario_id']=='E6-LP-06')
        self.assertEqual(x['verified_media_outputs']['A']['sha256'],v.EXPECTED_LOOP22)
    def test_16_loop22_b_sha(self):
        x=next(x for x in self.obj['smoke18_scenarios'] if x['scenario_id']=='E6-LP-06')
        self.assertEqual(x['verified_media_outputs']['B']['sha256'],v.EXPECTED_LOOP22)
    def test_17_loop22_size(self):
        x=next(x for x in self.obj['smoke18_scenarios'] if x['scenario_id']=='E6-LP-06')
        self.assertEqual(x['verified_media_outputs']['A']['bytes'],10500987)
        self.assertEqual(x['verified_media_outputs']['B']['bytes'],10500987)
    def test_18_r1v_five_pairs(self): self.assertEqual(len(self.obj['reuse_requalification']['r1v_loop_pairs']),5)
    def test_19_drill_six_receipts(self): self.assertEqual(len(self.obj['reuse_requalification']['drill_receipts']),6)
    def test_20_challenge_music_stays_proposal(self):
        for x in self.obj['smoke18_scenarios']:
            if x['family']=='challenge':
                for p in x['execution_probes']:
                    self.assertEqual(p['music_seed_status'],'PROPOSAL_ONLY_NOT_AUTHORIZED')
    def test_21_ch008_ch009_not_selected(self):
        ids=[x['selector'] for x in self.obj['smoke18_scenarios'] if x['family']=='challenge']
        self.assertNotIn('CHALLENGE_008',ids); self.assertNotIn('CHALLENGE_009',ids)
    def test_22_loop_profile_not_normalized(self):
        x=next(x for x in self.obj['smoke18_scenarios'] if x['scenario_id']=='E6-LP-06')
        self.assertEqual(x['technical_profile_observation']['pixel_format'],'yuvj420p')
        self.assertEqual(x['technical_profile_observation']['color_range'],'pc')
    def test_23_no_candidate_accepted(self):
        self.assertFalse(any(x.get('e6_acceptance')=='ACCEPTED' for x in self.obj['smoke18_scenarios']))
    def test_24_validator_accepts_ledger(self): v.validate_ledger(self.obj)
    def test_25_parent_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError): v.safe_file(pathlib.Path(t),'../escape')
    def test_26_absolute_path_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError): v.safe_file(pathlib.Path(t),str(pathlib.Path(t).anchor+'forbidden'))
    def test_27_expected_hash_constants(self):
        self.assertEqual(v.EXPECTED_C11C,'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953')
        self.assertEqual(v.EXPECTED_D48,'0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07')
    def test_28_open_gates_present(self): self.assertGreaterEqual(len(self.obj['open_gates']),6)

    def test_29_installer_uses_process_based_python_version_probe(self):
        package_root=pathlib.Path(__file__).resolve().parents[4]
        source=(package_root/'INSTALL_C11E_E6_SMOKE18_REUSE_REQUALIFICATION_V2.ps1').read_text(encoding='utf-8')
        self.assertIn("$psi.Arguments = '--version'", source)
        self.assertIn('ReadToEndAsync()', source)
        self.assertNotIn('& $PythonExe -c', source)
    def test_30_installer_sets_explicit_exit_code(self):
        package_root=pathlib.Path(__file__).resolve().parents[4]
        source=(package_root/'INSTALL_C11E_E6_SMOKE18_REUSE_REQUALIFICATION_V2.ps1').read_text(encoding='utf-8')
        self.assertIn('$global:LASTEXITCODE = 1', source)
        self.assertIn('$global:LASTEXITCODE = 0', source)
    def test_31_runner_uses_process_based_python_version_probe(self):
        package_root=pathlib.Path(__file__).resolve().parents[4]
        source=(package_root/'payload/tools/c11d/d9/RUN_C11E_E6_SMOKE18_REUSE_REQUALIFICATION_V2.ps1').read_text(encoding='utf-8')
        self.assertIn("$psi.Arguments = '--version'", source)
        self.assertIn('ReadToEndAsync()', source)
        self.assertNotIn('& $PythonExe -c', source)
    def test_32_runner_sets_explicit_exit_code(self):
        package_root=pathlib.Path(__file__).resolve().parents[4]
        source=(package_root/'payload/tools/c11d/d9/RUN_C11E_E6_SMOKE18_REUSE_REQUALIFICATION_V2.ps1').read_text(encoding='utf-8')
        self.assertIn('$global:LASTEXITCODE = 1', source)
        self.assertIn('$global:LASTEXITCODE = 0', source)

    def test_33_package_manifest_payload_hashes_and_sizes(self):
        package_root=pathlib.Path(__file__).resolve().parents[4]
        manifest=json.loads((package_root/'PACKAGE_MANIFEST_V2.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['install_mode'],'ADD_ONLY')
        self.assertEqual(manifest['payload_count'],5)
        self.assertEqual(len(manifest['payloads']),5)
        for item in manifest['payloads']:
            raw=(package_root/item['package_relative_path']).read_bytes()
            self.assertEqual(len(raw),item['bytes'],item['package_relative_path'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256'],item['package_relative_path'])
    def test_34_installer_fails_closed_on_nonidentical_destination(self):
        package_root=pathlib.Path(__file__).resolve().parents[4]
        source=(package_root/'INSTALL_C11E_E6_SMOKE18_REUSE_REQUALIFICATION_V2.ps1').read_text(encoding='utf-8')
        self.assertIn('DESTINATION_CONFLICT_NOT_OVERWRITTEN',source)
        self.assertIn('SKIP_IDENTICAL',source)
        self.assertIn('ADD_ONLY',source)

if __name__=='__main__': unittest.main(verbosity=2)
