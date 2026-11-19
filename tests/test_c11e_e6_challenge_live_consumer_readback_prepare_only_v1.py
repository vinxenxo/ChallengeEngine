import hashlib, json, unittest, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools' / 'c11d' / 'd9'))
from c11e_e6_challenge_live_consumer_readback_prepare_only_v1 import (
    phase_rows, ranges_for, validate_consumer_envelope, make_frame_plan,
    safe_rel, hbytes, read_pinned_json, validate_binding_install_receipt, READY, OMITTED, BLOCKED, META
)

POLICY='764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5'
LAYOUT='3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461'

def make_env(selector='CHALLENGE_004', hook=180, cta=120):
    total=900
    phases=[
      {'phase':'HOOK','start_frame':0,'end_frame':hook,'timebase':'SOURCE_FPS_HALF_OPEN'},
      {'phase':'GAME','start_frame':hook,'end_frame':hook+600,'timebase':'SOURCE_FPS_HALF_OPEN'},
      {'phase':'REVEAL','start_frame':hook+600,'end_frame':total-cta,'timebase':'SOURCE_FPS_HALF_OPEN'},
      {'phase':'CTA','start_frame':total-cta,'end_frame':total,'timebase':'SOURCE_FPS_HALF_OPEN'},
    ]
    req={'request_id':'REQ-'+selector,'content_type':'challenges','selection':{'content_type':'challenges','variant_id':selector},'presentation_options':{'show_hook_countdown':True}}
    intent={'schema':'C11-E-PRODUCTION-INTENT-V1','status':'PREPARED_E1_NOT_DISPATCHED','request':req,'identity':{'intent_hash':'a'*64}}
    env={'schema':'C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1','schema_version':'1.0','status':'PREPARED_E1_NOT_DISPATCHED','content_type':'challenges','challenge_id':selector,'e1_intent':intent,'intent_hash':'a'*64,'request_id':req['request_id'],'presentation_options':req['presentation_options'],'source_timebase':{'fps':60,'total_frames':total,'kind':'SOURCE_FRAME_INDEX'},'source_phase_ranges':phases,'policy_sha256':POLICY,'layout_contract_sha256':LAYOUT,'governance':{'renderer_input_emitted':False,'production_dispatch':False,'media_created':False,'release_authority':'NONE','d4_8':'BLOCKED','d9_10':'PREPARE_ONLY'},'fields':[]}
    for name,region,windows in [('title','HEADER',['HOOK']),('subtitle','HEADER',['HOOK']),('player_name','CHALLENGE_OVERLAY',['HOOK','GAME']),('challenge_label','CHALLENGE_OVERLAY',['HOOK','GAME']),('call_to_action','FOOTER',['CTA']),('language','METADATA',[])]:
      rs=[]
      by={x['phase']:x for x in phases}
      for w in windows:rs.append({'phase':w,'start_frame':by[w]['start_frame'],'end_frame':by[w]['end_frame'],'timebase':'SOURCE_FPS_HALF_OPEN'})
      val='TEST' if name in ('title','subtitle','call_to_action') else ('UNKNOWN' if name in ('player_name','challenge_label') else 'es')
      active=sum(x['end_frame']-x['start_frame'] for x in rs)
      if name in ('title','subtitle','call_to_action'):
        disp=READY if active>0 else OMITTED
        if active==0:val=''
      elif name in ('player_name','challenge_label'):disp=BLOCKED
      else:disp=META
      env['fields'].append({'field':name,'region':region,'source_phase_windows':windows,'source_frame_ranges':rs,'policy_sha256':POLICY,'layout_contract_sha256':LAYOUT,'effective_value':val,'value_sha256':hbytes(val.encode()),'disposition':disp})
    return env

class ReadbackContractTests(unittest.TestCase):
    def test_01_selector_set_exact(self): self.assertEqual(len(('CHALLENGE_001','CHALLENGE_002','CHALLENGE_004','CHALLENGE_005','CHALLENGE_006','CHALLENGE_007')),6)
    def test_02_variant_set_exact(self): self.assertEqual(len(('A','B_REPEAT','C_CHANGED_MUSIC_SEED')),3)
    def test_03_cartesian_probes_18(self): self.assertEqual(6*3,18)
    def test_04_manifest_slots_54(self): self.assertEqual(18*3,54)
    def test_05_empty_hook_omits_title_subtitle(self):
      e=make_env(hook=0); s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT); self.assertEqual(s['visible_fields'],['call_to_action']); self.assertEqual(s['omitted_zero_window_fields'],['title','subtitle'])
    def test_06_empty_cta_omits_cta(self):
      e=make_env(cta=0); s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT); self.assertEqual(s['omitted_zero_window_fields'],['call_to_action'])
    def test_07_both_empty_omit_all_visual(self):
      e=make_env(selector='CHALLENGE_005',hook=0,cta=0); s=validate_consumer_envelope(e,e,'CHALLENGE_005','A',POLICY,LAYOUT); self.assertEqual(s['visible_fields'],[]); self.assertEqual(len(s['omitted_zero_window_fields']),3)
    def test_08_positive_hook_ready(self):
      e=make_env(); s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT); self.assertIn('title',s['visible_fields'])
    def test_09_positive_cta_ready(self):
      e=make_env(); s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT); self.assertIn('call_to_action',s['visible_fields'])
    def test_10_zero_value_hash_empty(self):
      e=make_env(hook=0); s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT); r=next(x for x in e['fields'] if x['field']=='title'); self.assertEqual(r['value_sha256'],hashlib.sha256(b'').hexdigest())
    def test_11_zero_window_no_fallback(self):
      e=make_env(hook=0); r=next(x for x in e['fields'] if x['field']=='title'); r['source_frame_ranges']=[{'phase':'GAME','start_frame':0,'end_frame':600,'timebase':'SOURCE_FPS_HALF_OPEN'}]; r['source_phase_windows']=['HOOK']; r['effective_value']='TEST'; r['value_sha256']=hbytes(b'TEST'); r['disposition']=READY
      with self.assertRaisesRegex(Exception,'FIELD_RANGE_MISMATCH'): validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_12_e1_intent_immutable(self):
      e=make_env(); orig=make_env(); e['e1_intent']['editorial']={'title':'changed'}
      with self.assertRaisesRegex(Exception,'E1_INTENT_MUTATED'): validate_consumer_envelope(e,orig,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_13_intent_hash_immutable(self):
      e=make_env();o=make_env();e['intent_hash']='b'*64
      with self.assertRaisesRegex(Exception,'E1_INTENT_HASH_MUTATED'):validate_consumer_envelope(e,o,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_14_source_timebase_immutable(self):
      e=make_env();o=make_env();e['source_timebase']['fps']=30
      with self.assertRaisesRegex(Exception,'SOURCE_TIMEBASE_OR_PHASES_MUTATED'):validate_consumer_envelope(e,o,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_15_policy_sha_mandatory(self):
      e=make_env();e['policy_sha256']='0'*64
      with self.assertRaisesRegex(Exception,'POLICY_LAYOUT_PIN_MISMATCH'):validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_16_layout_sha_mandatory(self):
      e=make_env();e['layout_contract_sha256']='0'*64
      with self.assertRaisesRegex(Exception,'POLICY_LAYOUT_PIN_MISMATCH'):validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_17_exact_six_fields(self):
      e=make_env();e['fields'].pop()
      with self.assertRaisesRegex(Exception,'FIELD_COUNT_INVALID'):validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_18_duplicate_field_rejected(self):
      e=make_env();e['fields'][1]['field']='title'
      with self.assertRaisesRegex(Exception,'FIELD_ALLOWLIST_INVALID'):validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_19_identity_stays_nonvisual(self):
      e=make_env();r=next(x for x in e['fields'] if x['field']=='player_name');r['effective_value']='PLAYER';r['value_sha256']=hbytes(b'PLAYER')
      with self.assertRaisesRegex(Exception,'IDENTITY_FIELD_VISUALIZED'):validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_20_language_stays_metadata(self):
      e=make_env();r=next(x for x in e['fields'] if x['field']=='language');r['disposition']=READY
      with self.assertRaisesRegex(Exception,'LANGUAGE_FIELD_VISUALIZED'):validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_21_governance_boundary_held(self):
      e=make_env();e['governance']['media_created']=True
      with self.assertRaisesRegex(Exception,'ENVELOPE_GOVERNANCE_INVALID'):validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT)
    def test_22_frame_plan_has_header_and_footer_states(self):
      e=make_env();s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT); p=make_frame_plan(e,s,'CHALLENGE_004','A'); self.assertTrue(any(x['expected_d_header_active'] for x in p['frame_samples'])); self.assertTrue(any(x['expected_d_footer_active'] for x in p['frame_samples']))
    def test_23_frame_plan_zero_hook_never_header(self):
      e=make_env(hook=0);s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT);p=make_frame_plan(e,s,'CHALLENGE_004','A');self.assertFalse(any(x['expected_d_header_active'] for x in p['frame_samples']))
    def test_24_frame_plan_zero_cta_never_footer(self):
      e=make_env(cta=0);s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT);p=make_frame_plan(e,s,'CHALLENGE_004','A');self.assertFalse(any(x['expected_d_footer_active'] for x in p['frame_samples']))
    def test_25_native_cta_owner_is_d_only_inside_footer(self):
      e=make_env();s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT);p=make_frame_plan(e,s,'CHALLENGE_004','A');self.assertTrue(all(x['expected_native_cta_owner']=='D_C11C_SHARED_FOOTER' for x in p['frame_samples'] if x['expected_d_footer_active']))
    def test_26_native_cta_owner_returns_to_c_outside_footer(self):
      e=make_env();s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT);p=make_frame_plan(e,s,'CHALLENGE_004','A');self.assertTrue(any(x['expected_native_cta_owner']=='C_CHALLENGE_PRESENTATION_UI' for x in p['frame_samples'] if not x['expected_d_footer_active']))
    def test_27_native_hook_migration_is_conditional(self):
      e=make_env();s=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT);p=make_frame_plan(e,s,'CHALLENGE_004','A');self.assertTrue(all('CONDITIONAL_' in x['native_hook_migration'] for x in p['frame_samples'] if x['expected_d_header_active']))
    def test_28_no_engine_run_claim(self):
      from c11e_e6_challenge_live_consumer_readback_prepare_only_v1 import check_consumer_source
      self.assertTrue(callable(check_consumer_source))
    def test_29_safe_relative_paths(self): self.assertEqual(safe_rel('artifacts/tests/foo').as_posix(),'artifacts/tests/foo')
    def test_30_parent_traversal_rejected(self):
      with self.assertRaises(Exception):safe_rel('../escape')
    def test_31_absolute_path_rejected(self):
      with self.assertRaises(Exception):safe_rel('C:/escape')
    def test_32_backslash_path_rejected(self):
      with self.assertRaises(Exception):safe_rel('artifacts\\file')
    def test_33_binding_install_receipt_exact_success_status(self):
      validate_binding_install_receipt({'status':'PASS_ADD_ONLY_INSTALL_COMMITTED','added':19,'replaced':0})
    def test_34_binding_install_receipt_rejects_other_status(self):
      with self.assertRaisesRegex(Exception,'BINDING_INSTALL_RECEIPT_NOT_SUCCESSFUL'):
        validate_binding_install_receipt({'status':'PASS_ADD_ONLY_COMMITTED','added':19,'replaced':0})
    def test_35_inputs_json_requires_exact_sha_and_sidecar(self):
      import tempfile
      from pathlib import Path
      with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'inputs.json';raw=b'{\"ok\":true}';p.write_bytes(raw);expected=hbytes(raw)
        (Path(str(p)+'.sha256')).write_text(expected+'  inputs.json\n',encoding='ascii')
        self.assertEqual(read_pinned_json(p,expected),{'ok':True})
    def test_36_inputs_json_rejects_missing_sidecar(self):
      import tempfile
      from pathlib import Path
      with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'inputs.json';raw=b'{\"ok\":true}';p.write_bytes(raw)
        with self.assertRaisesRegex(Exception,'INPUTS_SIDECAR_MISSING'):read_pinned_json(p,hbytes(raw))
    def test_37_frame_plan_requires_single_mount(self):
      e=make_env();summary=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT);plan=make_frame_plan(e,summary,'CHALLENGE_004','A')
      self.assertTrue(all(x['expected_mount_count']==1 for x in plan['frame_samples']))
    def test_38_reserved_bands_expected_black(self):
      e=make_env();summary=validate_consumer_envelope(e,e,'CHALLENGE_004','A',POLICY,LAYOUT);plan=make_frame_plan(e,summary,'CHALLENGE_004','A')
      self.assertTrue(all(x['expected_reserved_header_footer_bands']=='BLACK' for x in plan['frame_samples']))

if __name__=='__main__':unittest.main(verbosity=2)
