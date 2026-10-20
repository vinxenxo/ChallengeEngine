"""Fail-closed Python contract tests for Challenge V2-C source-frame receipts."""
from __future__ import annotations
import copy, importlib.util, json, sys, unittest
from pathlib import Path

THIS = Path(__file__).resolve()
ROOT = THIS.parents[3]
RUNNER_PATH = THIS.with_name('d_renderer_challenge_visual_payload_v2c_source_frame_runtime.py')
spec = importlib.util.spec_from_file_location('v2c_source_frame_runner', RUNNER_PATH)
runner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runner
assert spec.loader is not None
spec.loader.exec_module(runner)
CONTRACT_PATH = ROOT / runner.CONTRACT_REL


def source_pin_map(contract):
    return {x['path']: x['sha256'] for x in contract['source_pins']}


def valid_receipt(contract, selector, run_id='R1', pid=1101):
    tb = selector['source_timebase']
    count = int(tb['fps'] * tb['game_duration_seconds'])
    candidate = {}
    kind = selector['candidate_kind']
    field = selector['candidate_field']
    types = {'target_x': 'float', 'target_position': 'Vector2', 'active_selection': 'int', 'displayed_count': 'int'}
    if kind == 'CUSTOM_DATA_FIELD_CANDIDATE':
        candidate[field] = {'present_frames': count, 'type_histogram': {types[field]: count}}
    pins = source_pin_map(contract)
    asset_pins = {}
    for alias, asset_ref in selector['declared_assets'].items():
        rel = asset_ref.removeprefix('res://')
        asset_pins[alias] = {'source_key': rel, 'sha256': pins[rel]}
    conflict = tb['timebase_conflict']
    return {
        'schema': runner.RECEIPT_ID, 'schema_version': '1.0', 'status': 'SOURCE_FRAME_RECEIPT',
        'selector': runner.selector_public(selector),
        'process': {'run_id': run_id, 'process_id': pid, 'exit_code': 0},
        'runtime': {'godot_version': '4.7.1.stable.mono.official.a13da4feb', 'engine_version_info': {'major': 4, 'minor': 7, 'patch': 1, 'string': '4.7.1.stable.mono.official.a13da4feb'}},
        'lineage': {
            'contract_sha256': runner.CONTRACT_SHA256, 'frozen_manifest_sha256': runner.FROZEN_SHA,
            'challenge_source_sha256': selector['source_sha256'], 'mechanic_source_sha256': pins[selector['mechanic_source']],
            'runtime_bridge_sha256': pins['core/execution/ChallengeRuntimeBridge.gd'],
            'frame_snapshot_sha256': pins['core/data/FrameSnapshot.gd'], 'verified_source_pin_count': contract['source_pin_count'],
        },
        'route': {
            'effective_mechanic': selector['mechanic'], 'runtime_bridge_method': 'ChallengeRuntimeBridge.run_effective_pipeline',
            'planner_request_hash': 'a'*64, 'planner_plan_hash': 'b'*64,
            'bridge_status': 'PLANNING_ONLY_NOT_RENDERABLE', 'adapter_status': 'PREPARED_NOT_DISPATCHED_RENDERER_DISABLED',
            'renderer': 'OFF', 'release_authority': 'NONE',
        },
        'source_frames': {
            'count': count, 'expected_game_frames': count, 'source_fps': tb['fps'],
            'game_duration_seconds': tb['game_duration_seconds'], 'finite_transform_frames': count,
            'frame_shape': ['position:Vector2', 'rotation:float', 'scale:Vector2', 'opacity:float', 'texture_index:int', 'variant_id:int'],
            'projection_fields': contract['frame_projection']['field_order'], 'projection_sha256': 'c'*64,
        },
        'source_timebase': {
            'declared_total_duration_seconds': tb['declared_total_duration_seconds'],
            'hook_duration_seconds': tb['hook_duration_seconds'], 'game_duration_seconds': tb['game_duration_seconds'],
            'reveal_duration_seconds': tb['reveal_duration_seconds'], 'cta_duration_seconds': tb['cta_duration_seconds'],
            'phase_duration_sum_seconds': tb['phase_duration_sum_seconds'], 'known_conflict': conflict,
            'phase_timeline_acceptance': 'BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY' if conflict else 'NOT_EVALUATED_SOURCE_FRAME_ONLY',
        },
        'source_asset_pins': asset_pins, 'candidate_field_observations': candidate,
        'semantic_binding_state': {'approved_bindings': 0, 'approved_custom_data_bindings': 0, 'custom_data_values_serialized': False},
        'side_effects': {
            'payload_file_written': False, 'media_created': False, 'renderer_native_input_emitted': False,
            'render_nodes_created': False, 'rendering_server_called': False, 'viewport_captured': False,
            'canonical_state_mutated': False, 'production_dispatched': False,
        },
    }


def valid_planner():
    return {'invocations': 1, 'status': 'PLANNED', 'request_hash': 'd'*64, 'plan_hash': 'e'*64,
            'bridge_status': 'PLANNING_ONLY_NOT_RENDERABLE', 'adapter_status': 'PREPARED_NOT_DISPATCHED_RENDERER_DISABLED',
            'gameplay_seed': 12345, 'music_seed': 840001}


def valid_report(contract):
    rows=[]
    for i, selector in enumerate(contract['selectors']):
        r1=valid_receipt(contract, selector, f'{selector["challenge_id"]}_R1', 2000+i*2)
        r2=valid_receipt(contract, selector, f'{selector["challenge_id"]}_R2', 2001+i*2)
        # Deterministic hashes bind to each compact receipt but run IDs/process IDs vary by process.
        run1={'run_id': r1['process']['run_id'], 'process_id': r1['process']['process_id'], 'exit_code':0,
              'stdout_sha256':'1'*64,'stderr_sha256':'2'*64,'receipt_sha256':runner.sha_bytes(runner.canon(r1)),'receipt':r1}
        run2={'run_id': r2['process']['run_id'], 'process_id': r2['process']['process_id'], 'exit_code':0,
              'stdout_sha256':'3'*64,'stderr_sha256':'4'*64,'receipt_sha256':runner.sha_bytes(runner.canon(r2)),'receipt':r2}
        rows.append({'selector':runner.selector_public(selector),'status':'ACCEPTED_SOURCE_FRAME_ONLY','block_reasons':[],
                      'planner':valid_planner(),'runtime_runs':[run1,run2],'repeat_agreement':True})
    return {'schema':runner.REPORT_ID,'schema_version':'1.0','status':'PASS_SOURCE_FRAME_ROUTE_ONLY',
            'contract_sha256':runner.CONTRACT_SHA256,'frozen_manifest_sha256':runner.FROZEN_SHA,
            'source_pin_count':contract['source_pin_count'],'selector_count_expected':9,'selectors':rows,
            'planner_invocations':9,'godot_version_probe_invocations':1,'godot_runtime_process_invocations':18,
            'godot_runtime_processes_expected':18,'payload_materialized':False,'media_created':False,'approved_bindings':0,
            'visual_seed_sensitivity':'NOT_TESTED','governance_locks':runner.GOVERNANCE,'evidence':{}}


class V2CContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))

    def test_01_contract_valid(self):
        runner.validate_contract(self.contract)

    def test_02_source_pin_omission_rejected(self):
        c=copy.deepcopy(self.contract); c['source_pins'].pop();
        with self.assertRaises(runner.ContractError): runner.validate_contract(c)

    def test_03_invalid_source_sha_rejected(self):
        c=copy.deepcopy(self.contract); c['source_pins'][0]['sha256']='bad'
        with self.assertRaises(runner.ContractError): runner.validate_contract(c)

    def test_04_selector_omission_rejected(self):
        c=copy.deepcopy(self.contract); c['selectors'].pop()
        with self.assertRaises(runner.ContractError): runner.validate_contract(c)

    def test_05_unknown_contract_field_rejected(self):
        c=copy.deepcopy(self.contract); c['allow_render']=True
        with self.assertRaises(runner.ContractError): runner.validate_contract(c)

    def test_06_whole_custom_data_projection_rejected(self):
        c=copy.deepcopy(self.contract); c['frame_projection']['field_order'].append('custom_data')
        with self.assertRaises(runner.ContractError): runner.validate_contract(c)

    def test_07_implicit_binding_approval_rejected(self):
        c=copy.deepcopy(self.contract); c['semantic_binding_policy']['approved_bindings']=1
        with self.assertRaises(runner.ContractError): runner.validate_contract(c)

    def test_08_pilot_target_x_vector_conversion_rejected(self):
        c=copy.deepcopy(self.contract); c['semantic_binding_policy']['target_x']='VECTOR2'
        with self.assertRaises(runner.ContractError): runner.validate_contract(c)

    def test_09_timebase_conflict_cannot_be_normalized(self):
        c=copy.deepcopy(self.contract); c['selectors'][7]['source_timebase']['phase_duration_sum_seconds']=11.0
        with self.assertRaises(runner.ContractError): runner.validate_contract(c)

    def test_10_all_nine_valid_receipts(self):
        for s in self.contract['selectors']:
            with self.subTest(selector=s['challenge_id']): runner.validate_receipt(valid_receipt(self.contract,s),self.contract,s)

    def test_11_unknown_receipt_field_rejected(self):
        r=valid_receipt(self.contract,self.contract['selectors'][0]); r['custom_data']={'leak':'no'}
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract)

    def test_12_wrong_selector_route_rejected(self):
        r=valid_receipt(self.contract,self.contract['selectors'][0]); r['selector']['mechanic']='wrong'
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract)

    def test_13_frame_cardinality_mismatch_rejected(self):
        r=valid_receipt(self.contract,self.contract['selectors'][0]); r['source_frames']['count']-=1
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract)

    def test_14_frame_shape_mismatch_rejected(self):
        r=valid_receipt(self.contract,self.contract['selectors'][0]); r['source_frames']['frame_shape'][0]='position:float'
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract)

    def test_15_phase_acceptance_for_008_remains_blocked(self):
        s=self.contract['selectors'][7]; r=valid_receipt(self.contract,s); r['source_timebase']['phase_timeline_acceptance']='NOT_EVALUATED_SOURCE_FRAME_ONLY'
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract,s)

    def test_16_unknown_custom_data_candidate_rejected(self):
        s=self.contract['selectors'][2]; r=valid_receipt(self.contract,s); r['candidate_field_observations']['custom_data']={'present_frames':420,'type_histogram':{'Dictionary':420}}
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract,s)

    def test_17_custom_data_values_serialized_rejected(self):
        r=valid_receipt(self.contract,self.contract['selectors'][2]); r['semantic_binding_state']['custom_data_values_serialized']=True
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract)

    def test_18_side_effect_flag_rejected(self):
        r=valid_receipt(self.contract,self.contract['selectors'][0]); r['side_effects']['rendering_server_called']=True
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract)

    def test_19_full_report_valid(self):
        runner.validate_report(valid_report(self.contract),self.contract)

    def test_20_report_selector_omission_rejected(self):
        report=valid_report(self.contract); report['selectors'].pop()
        with self.assertRaises(runner.ContractError): runner.validate_report(report,self.contract)

    def test_21_unknown_report_field_rejected(self):
        report=valid_report(self.contract); report['phase_acceptance']='PASS'
        with self.assertRaises(runner.ContractError): runner.validate_report(report,self.contract)

    def test_22_repeat_hash_mismatch_rejected(self):
        report=valid_report(self.contract); receipt=report['selectors'][0]['runtime_runs'][1]['receipt']; receipt['source_frames']['projection_sha256']='f'*64
        report['selectors'][0]['runtime_runs'][1]['receipt_sha256']=runner.sha_bytes(runner.canon(receipt))
        with self.assertRaises(runner.ContractError): runner.validate_report(report,self.contract)

    def test_23_d910_dispatch_route_rejected(self):
        r=valid_receipt(self.contract,self.contract['selectors'][0]); r['route']['adapter_status']='DISPATCHED'
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract)

    def test_24_candidate_values_are_not_allowed_in_summary(self):
        r=valid_receipt(self.contract,self.contract['selectors'][2]); r['candidate_field_observations']['target_x']['value']=50.0
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract)

    def test_25_pilot_target_x_vector_histogram_rejected(self):
        r=valid_receipt(self.contract,self.contract['selectors'][2]); r['candidate_field_observations']['target_x']['type_histogram']={'Vector2':420}
        with self.assertRaises(runner.ContractError): runner.validate_receipt(r,self.contract)

    def test_26_timebase_declaration_kept_separate_from_acceptance(self):
        for cid in ('CHALLENGE_008','CHALLENGE_009'):
            s=next(x for x in self.contract['selectors'] if x['challenge_id']==cid); r=valid_receipt(self.contract,s)
            self.assertEqual(r['source_timebase']['declared_total_duration_seconds'],11.0)
            self.assertEqual(r['source_timebase']['phase_duration_sum_seconds'],12.0)
            self.assertEqual(r['source_timebase']['phase_timeline_acceptance'],'BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY')

    def test_27_mono_launcher_identity_is_separate_from_engine_version_info(self):
        harness_path = ROOT / runner.HARNESS.removeprefix('res://')
        harness_source = harness_path.read_text(encoding='utf-8')
        runner_source = RUNNER_PATH.read_text(encoding='utf-8')
        self.assertIn("f'--godot-version={verified_version}'", runner_source)
        self.assertIn('var verified_godot_version := str(_args.get("godot-version", ""))', harness_source)
        self.assertIn('"godot_version": verified_godot_version', harness_source)
        self.assertIn('"engine_version_info": version_info', harness_source)
        self.assertIn('int(version_info.get("major", -1)) != 4', harness_source)
        self.assertIn('int(version_info.get("minor", -1)) != 7', harness_source)
        self.assertIn('int(version_info.get("patch", -1)) != 1', harness_source)
        self.assertNotIn('not engine_version.to_lower().contains("mono")', harness_source)

    def test_28_legacy_video_profile_binding_resolves_and_stays_pinned(self):
        harness_path = ROOT / runner.HARNESS.removeprefix('res://')
        harness_source = harness_path.read_text(encoding='utf-8')
        bridge_source = (ROOT / 'core/execution/ChallengeRuntimeBridge.gd').read_text(encoding='utf-8-sig')
        self.assertIn('const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")', harness_source)
        self.assertIn('elif runtime_video is String:', harness_source)
        self.assertIn('VideoProfileRegistry.get_profile(video_profile_id)', harness_source)
        self.assertIn('EFFECTIVE_RUNTIME_VIDEO_PROFILE_UNRESOLVED:', harness_source)
        self.assertIn('core/authoring/VideoProfileRegistry.gd', source_pin_map(self.contract))
        self.assertIn('EFFECTIVE_RUNTIME_TIMEBASE_SOURCE_PIN_MISMATCH:', harness_source)
        self.assertIn('f4_legacy_60_h0_g7_r0_c2', bridge_source)
        self.assertIn('f4_legacy_60_h3_g7_r0_c0', bridge_source)
        self.assertIn('var hook_duration := 0.0', harness_source)
        self.assertIn('var reveal_duration := 0.0', harness_source)
        self.assertIn('var cta_duration := 0.0', harness_source)
        cases = {
            'CHALLENGE_001': 'f4_legacy_60_h0_g7_r0_c2',
            'CHALLENGE_002': 'f4_legacy_60_h3_g7_r0_c0',
        }
        phase_names = {'hook_duration': 'hook_duration_seconds', 'game_duration': 'game_duration_seconds', 'reveal_duration': 'reveal_duration_seconds', 'cta_duration': 'cta_duration_seconds'}
        for cid, profile_id in cases.items():
            selector = next(x for x in self.contract['selectors'] if x['challenge_id'] == cid)
            profile_path = ROOT / 'profiles/video' / f'{profile_id}.json'
            profile = json.loads(profile_path.read_text(encoding='utf-8'))
            self.assertEqual(profile['fps'], selector['source_timebase']['fps'])
            self.assertEqual(profile['phases']['game_duration'], selector['source_timebase']['game_duration_seconds'])
            for profile_phase, selector_phase in phase_names.items():
                self.assertEqual(profile['phases'][profile_phase], selector['source_timebase'][selector_phase], f'{cid} {profile_phase}')


def main():
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(V2CContractTests)
    result=unittest.TextTestRunner(stream=sys.stdout,verbosity=2).run(suite)
    if result.wasSuccessful(): print(f'C11D_V2C_PYTHON_CONTRACT_TESTS_PASS={result.testsRun}/28')
    else: print(f'C11D_V2C_PYTHON_CONTRACT_TESTS_FAIL={len(result.failures)+len(result.errors)}/{result.testsRun}')
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__': raise SystemExit(main())
