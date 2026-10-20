#!/usr/bin/env python3
"""Read-only Challenge V2-C source-frame runtime receipts. No payload/materializer/media/render dispatch."""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path
from typing import Any, Mapping

# Do not create __pycache__ files in the active checkout during this receipt run.
sys.dont_write_bytecode = True

CONTRACT_REL = Path('definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json')
CONTRACT_SHA256 = '6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c'
CONTRACT_ID = 'C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-RECEIPT-CONTRACT-V1'
RECEIPT_ID = 'C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-RECEIPT-V1'
REPORT_ID = 'C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-REPORT-V1'
FROZEN_SHA = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
HARNESS = 'res://tools/c11d/d9/challenge_visual_payload_v2c_source_frame_runtime_in_memory.gd'
IDS = [f'CHALLENGE_{i:03d}' for i in range(1, 10)]
GOVERNANCE = {'renderer':'OFF','media_created':False,'candidate_input_admissible':False,'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed':'NOT_ADOPTED','D4.8':'BLOCKED','D9.10':'PREPARE_ONLY','D9.14':'BLOCKED','D9.16':'BLOCKED','D9.17':'BLOCKED_NO_GO','D10':'BLOCKED_FOR_PROMOTION','baseline_approval':'MISSING','freeze_eligible':False,'release_authority':'NONE','challenge_visual_seed_sensitivity':'NOT_TESTED'}
CONTRACT_KEYS = {'schema','schema_version','status','scope','authority_note','runtime_entry','canonical_planning','selectors','expected_selector_count','independent_processes_per_selector','repeat_comparison_fields','frame_projection','semantic_binding_policy','timebase_policy','side_effects_forbidden','governance_locks','frozen_c11c','source_pins','source_pin_count'}
RECEIPT_KEYS = {'schema','schema_version','status','selector','process','runtime','lineage','route','source_frames','source_timebase','source_asset_pins','candidate_field_observations','semantic_binding_state','side_effects'}
REPORT_KEYS = {'schema','schema_version','status','contract_sha256','frozen_manifest_sha256','source_pin_count','selector_count_expected','selectors','planner_invocations','godot_version_probe_invocations','godot_runtime_process_invocations','godot_runtime_processes_expected','payload_materialized','media_created','approved_bindings','visual_seed_sensitivity','governance_locks','evidence'}
ROW_KEYS = {'selector','status','block_reasons','planner','runtime_runs','repeat_agreement'}
PLANNER_KEYS = {'invocations','status','request_hash','plan_hash','bridge_status','adapter_status','gameplay_seed','music_seed'}
RUN_KEYS = {'run_id','process_id','exit_code','stdout_sha256','stderr_sha256','receipt_sha256','receipt'}

class ContractError(ValueError): pass
class PlannerInvocationFailed(ContractError): pass

def sha_bytes(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def sha_file(path: Path) -> str: return sha_bytes(path.read_bytes())
def is_sha(value: Any) -> bool: return isinstance(value, str) and re.fullmatch(r'[a-f0-9]{64}', value) is not None
def canon(value: Any) -> bytes: return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
def dump_json(path: Path, value: Any) -> str:
    data=(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n').encode('utf-8'); path.write_bytes(data); return sha_bytes(data)
def exact(value: Any, fields: set[str], label: str) -> None:
    if not isinstance(value, dict): raise ContractError(f'{label} must be an object')
    if set(value) != fields: raise ContractError(f'{label} fields mismatch: missing={sorted(fields-set(value))} unknown={sorted(set(value)-fields)}')
def pin_for(contract: Mapping[str, Any], rel: str) -> str:
    for pin in contract['source_pins']:
        if pin['path']==rel: return pin['sha256']
    raise ContractError(f'required source pin absent: {rel}')
def selector_public(s: Mapping[str, Any]) -> dict[str, str]: return {k:s[k] for k in ('challenge_id','mechanic','family_id')}
def selector_by_id(contract: Mapping[str, Any], cid: str) -> dict[str, Any]:
    for s in contract['selectors']:
        if s['challenge_id']==cid: return s
    raise ContractError(f'unknown selector: {cid}')

def validate_contract(c: Any) -> None:
    exact(c, CONTRACT_KEYS, 'contract')
    if (c['schema'],c['schema_version'],c['status'],c['scope']) != (CONTRACT_ID,'1.0','PREPARATION_ONLY_SOURCE_FRAME_RUNTIME_RECEIPT','SOURCE_FRAME_AND_ROUTE_ACCEPTANCE_ONLY'):
        raise ContractError('contract identity/scope mismatch')
    if c['expected_selector_count'] != 9 or c['independent_processes_per_selector'] != 2: raise ContractError('selector denominator/process count changed')
    selectors=c['selectors']
    if not isinstance(selectors,list) or [s.get('challenge_id') for s in selectors if isinstance(s,dict)] != IDS: raise ContractError('all nine selectors, in order, are mandatory')
    selector_fields={'challenge_id','mechanic','family_id','mechanic_source','candidate_kind','candidate_field','candidate_semantics','source_timebase','source_path','source_sha256','runtime_mechanic','custom_data_candidate_fields','declared_assets'}
    for s in selectors:
        exact(s,selector_fields,'selector')
        cid=s['challenge_id']; tb=s['source_timebase']
        exact(tb,{'fps','hook_duration_seconds','game_duration_seconds','reveal_duration_seconds','cta_duration_seconds','declared_total_duration_seconds','phase_duration_sum_seconds','timebase_conflict'},f'{cid}.source_timebase')
        if s['runtime_mechanic'] != s['mechanic'] or s['source_path'] != f'challenges/{cid}.json' or not is_sha(s['source_sha256']): raise ContractError(f'{cid} source identity malformed')
        if sum(float(tb[k]) for k in ('hook_duration_seconds','game_duration_seconds','reveal_duration_seconds','cta_duration_seconds')) != float(tb['phase_duration_sum_seconds']): raise ContractError(f'{cid} phase sum changed')
        conflict=cid in ('CHALLENGE_008','CHALLENGE_009')
        if tb['timebase_conflict'] is not conflict: raise ContractError(f'{cid} conflict status changed')
        if conflict and (tb['declared_total_duration_seconds'] != 11.0 or tb['phase_duration_sum_seconds'] != 12.0): raise ContractError(f'{cid} 11s/12s blocker changed')
        if s['candidate_kind']=='CUSTOM_DATA_FIELD_CANDIDATE':
            if s['custom_data_candidate_fields'] != [s['candidate_field']]: raise ContractError(f'{cid} candidate inventory mismatch')
        elif s['custom_data_candidate_fields'] != []: raise ContractError(f'{cid} static candidate misreported as custom_data')
        if not isinstance(s['declared_assets'],dict) or set(s['declared_assets'])-{'background_path','object_path','target_path'}: raise ContractError(f'{cid} assets malformed')
    pins=c['source_pins']
    if not isinstance(pins,list) or len(pins)!=c['source_pin_count'] or len(pins)<50: raise ContractError('source pin count/list mismatch')
    seen=set()
    for p in pins:
        exact(p,{'path','sha256'},'source pin')
        rel=p['path']
        if not isinstance(rel,str) or not rel or rel.startswith(('/','\\')) or '..' in Path(rel).parts or rel in seen or not is_sha(p['sha256']): raise ContractError(f'invalid/duplicate source pin: {rel}')
        seen.add(rel)
    required={'release/C11C_FREEZE_PACKAGE_MANIFEST.json','core/execution/ChallengeRuntimeBridge.gd','core/data/FrameSnapshot.gd','tools/c11d/d9/universal_producer.py','tools/c11d/d9/editorial_render_bridge.py','tools/c11d/d9/d_render_adapter.py','definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_V1.json','definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json','tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd'}
    required.update(f'challenges/{cid}.json' for cid in IDS); required.update(s['mechanic_source'] for s in selectors)
    required.update(v.removeprefix('res://') for s in selectors for v in s['declared_assets'].values())
    if not required.issubset(seen): raise ContractError(f'missing required pins: {sorted(required-seen)}')
    projection=c['frame_projection']
    if projection.get('field_order') != ['position.x','position.y','rotation','scale.x','scale.y','opacity','texture_index','variant_id'] or 'custom_data' in projection.get('field_order',[]): raise ContractError('unsafe/changed source projection fields')
    if projection.get('custom_data_policy') != 'NEVER_SERIALIZE_WHOLE_MAP; candidate-only presence/type histograms, no values': raise ContractError('custom_data serialization policy changed')
    sem=c['semantic_binding_policy']
    if sem.get('approved_bindings') != 0 or sem.get('approved_custom_data_bindings') != 0 or sem.get('all_candidates_approved') is not False: raise ContractError('binding proposal cannot imply approval')
    byid={s['challenge_id']:s for s in selectors}
    if byid['CHALLENGE_003']['candidate_field']!='target_x' or 'SCALAR_FLOAT_ONLY_NO_VECTOR2_CONVERSION' not in sem.get('target_x',''): raise ContractError('Pilot target_x scalar semantics changed')
    if byid['CHALLENGE_008']['candidate_field']!='active_selection' or byid['CHALLENGE_009']['candidate_field']!='displayed_count': raise ContractError('Choose/Count candidates changed')
    if c['timebase_policy'].get('phase_timeline_acceptance')!='NOT_EVALUATED': raise ContractError('phase/timeline acceptance out of scope')
    if c['governance_locks'] != GOVERNANCE: raise ContractError('governance locks changed')
    if c['frozen_c11c'].get('manifest_sha256') != FROZEN_SHA: raise ContractError('frozen C11-C manifest pin changed')
    if not c['side_effects_forbidden'] or any(v is not True for v in c['side_effects_forbidden'].values()): raise ContractError('every prohibited side effect must remain forbidden')

def load_contract(root: Path) -> tuple[dict[str, Any],str]:
    path=root/CONTRACT_REL
    raw=path.read_bytes(); actual=sha_bytes(raw)
    if actual != CONTRACT_SHA256: raise ContractError(f'contract SHA mismatch expected={CONTRACT_SHA256} actual={actual}')
    try: c=json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError,json.JSONDecodeError) as exc: raise ContractError(f'contract JSON invalid: {exc}') from exc
    validate_contract(c); return c,actual

def verify_pins(root: Path,c: Mapping[str,Any]) -> list[str]:
    errors=[]; manifest=root/'release/C11C_FREEZE_PACKAGE_MANIFEST.json'
    if not manifest.is_file() or sha_file(manifest)!=FROZEN_SHA: errors.append('FROZEN_C11C_MANIFEST_SHA_MISMATCH')
    for p in c['source_pins']:
        f=root/p['path']
        if not f.is_file(): errors.append(f'SOURCE_PIN_MISSING:{p["path"]}')
        elif sha_file(f)!=p['sha256']: errors.append(f'SOURCE_PIN_SHA_MISMATCH:{p["path"]}:{p["sha256"]}:{sha_file(f)}')
    return errors

def validate_receipt(r: Any,c: Mapping[str,Any],target: Mapping[str,Any]|None=None) -> None:
    exact(r,RECEIPT_KEYS,'receipt')
    if r.get('schema')!=RECEIPT_ID or r.get('schema_version')!='1.0' or r.get('status')!='SOURCE_FRAME_RECEIPT': raise ContractError('receipt schema/status mismatch')
    sel=r['selector']; exact(sel,{'challenge_id','mechanic','family_id'},'receipt.selector')
    target=target or selector_by_id(c,sel.get('challenge_id',''))
    if sel != selector_public(target): raise ContractError('selector/route mismatch')
    proc=r['process']; exact(proc,{'run_id','process_id','exit_code'},'receipt.process')
    if not isinstance(proc['run_id'],str) or not proc['run_id'] or not isinstance(proc['process_id'],int) or proc['process_id']<1 or proc['exit_code']!=0: raise ContractError('runtime process/exit invalid')
    runtime=r['runtime']; exact(runtime,{'godot_version','engine_version_info'},'receipt.runtime')
    if '4.7.1' not in runtime['godot_version'] or 'mono' not in runtime['godot_version'].lower() or not isinstance(runtime['engine_version_info'],dict): raise ContractError('Godot 4.7.1 Mono version not proven')
    lin=r['lineage']; linfields={'contract_sha256','frozen_manifest_sha256','challenge_source_sha256','mechanic_source_sha256','runtime_bridge_sha256','frame_snapshot_sha256','verified_source_pin_count'}; exact(lin,linfields,'receipt.lineage')
    for k in linfields-{'verified_source_pin_count'}:
        if not is_sha(lin[k]): raise ContractError(f'bad source lineage hash: {k}')
    if lin['contract_sha256']!=CONTRACT_SHA256 or lin['frozen_manifest_sha256']!=FROZEN_SHA or lin['challenge_source_sha256']!=target['source_sha256'] or lin['mechanic_source_sha256']!=pin_for(c,target['mechanic_source']) or lin['runtime_bridge_sha256']!=pin_for(c,'core/execution/ChallengeRuntimeBridge.gd') or lin['frame_snapshot_sha256']!=pin_for(c,'core/data/FrameSnapshot.gd') or lin['verified_source_pin_count']!=c['source_pin_count']: raise ContractError('source lineage pins mismatch')
    route=r['route']; exact(route,{'effective_mechanic','runtime_bridge_method','planner_request_hash','planner_plan_hash','bridge_status','adapter_status','renderer','release_authority'},'receipt.route')
    if route['effective_mechanic']!=target['mechanic'] or route['runtime_bridge_method']!='ChallengeRuntimeBridge.run_effective_pipeline' or not is_sha(route['planner_request_hash']) or not is_sha(route['planner_plan_hash']): raise ContractError('runtime/planner route identity invalid')
    if (route['bridge_status'],route['adapter_status'],route['renderer'],route['release_authority']) != ('PLANNING_ONLY_NOT_RENDERABLE','PREPARED_NOT_DISPATCHED_RENDERER_DISABLED','OFF','NONE'): raise ContractError('D9.10 route escaped planning-only state')
    f=r['source_frames']; exact(f,{'count','expected_game_frames','source_fps','game_duration_seconds','finite_transform_frames','frame_shape','projection_fields','projection_sha256'},'receipt.source_frames')
    if any(not isinstance(f[k],int) or f[k]<0 for k in ('count','expected_game_frames','source_fps','finite_transform_frames')) or f['source_fps']<1 or f['expected_game_frames']<1 or f['count']!=f['expected_game_frames'] or f['finite_transform_frames']!=f['count']: raise ContractError('frame cardinality/finite transform mismatch')
    tbtarget=target['source_timebase']
    if f['source_fps']!=tbtarget['fps'] or float(f['game_duration_seconds'])!=float(tbtarget['game_duration_seconds']): raise ContractError('source FPS/game duration differs from pin')
    shape=['position:Vector2','rotation:float','scale:Vector2','opacity:float','texture_index:int','variant_id:int']
    if f['frame_shape']!=shape or f['projection_fields']!=c['frame_projection']['field_order'] or not is_sha(f['projection_sha256']): raise ContractError('frame shape/projection mismatch')
    tb=r['source_timebase']; tbkeys={'declared_total_duration_seconds','hook_duration_seconds','game_duration_seconds','reveal_duration_seconds','cta_duration_seconds','phase_duration_sum_seconds','known_conflict','phase_timeline_acceptance'}; exact(tb,tbkeys,'receipt.source_timebase')
    for key,targetkey in [('declared_total_duration_seconds','declared_total_duration_seconds'),('hook_duration_seconds','hook_duration_seconds'),('game_duration_seconds','game_duration_seconds'),('reveal_duration_seconds','reveal_duration_seconds'),('cta_duration_seconds','cta_duration_seconds'),('phase_duration_sum_seconds','phase_duration_sum_seconds')]:
        if tb[key] != tbtarget[targetkey]: raise ContractError('timebase receipt failed source fidelity')
    if tb['known_conflict'] is not tbtarget['timebase_conflict']: raise ContractError('known timebase conflict flag mismatch')
    expected='BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY' if tbtarget['timebase_conflict'] else 'NOT_EVALUATED_SOURCE_FRAME_ONLY'
    if tb['phase_timeline_acceptance']!=expected: raise ContractError('phase/timeline acceptance must remain blocked/out of scope')
    a=r['source_asset_pins'];
    for alias,source_path in target['declared_assets'].items():
        rel=source_path.removeprefix('res://')
        if a.get(alias)!={'source_key':rel,'sha256':pin_for(c,rel)}: raise ContractError(f'asset lineage mismatch: {alias}')
    cand=r['candidate_field_observations']; allowed={'target_x','target_position','active_selection','displayed_count'}
    if not isinstance(cand,dict) or set(cand)!=set(target['custom_data_candidate_fields']) or set(cand)-allowed: raise ContractError('candidate custom_data scope mismatch')
    expected_type={'target_x':'float','target_position':'Vector2','active_selection':'int','displayed_count':'int'}
    for key,s in cand.items():
        exact(s,{'present_frames','type_histogram'},f'candidate {key}')
        hist=s['type_histogram']
        if not isinstance(s['present_frames'],int) or not 0<=s['present_frames']<=f['count'] or not isinstance(hist,dict) or sum(hist.values())!=s['present_frames'] or any(t not in {expected_type[key],'other'} or not isinstance(n,int) or n<1 for t,n in hist.items()): raise ContractError(f'candidate histogram invalid: {key}')
        if hist and set(hist)!={expected_type[key]}: raise ContractError(f'candidate type mismatch: {key}')
    sem=r['semantic_binding_state']; exact(sem,{'approved_bindings','approved_custom_data_bindings','custom_data_values_serialized'},'semantic_binding_state')
    if sem!={'approved_bindings':0,'approved_custom_data_bindings':0,'custom_data_values_serialized':False}: raise ContractError('binding approval or custom_data serialization state changed')
    side=r['side_effects']; sidekeys={'payload_file_written','media_created','renderer_native_input_emitted','render_nodes_created','rendering_server_called','viewport_captured','canonical_state_mutated','production_dispatched'}; exact(side,sidekeys,'side_effects')
    if any(side[k] is not False for k in sidekeys): raise ContractError('prohibited side effect reported')

def determinism_signature(r: Mapping[str,Any]) -> dict[str,Any]:
    return {k:r[k] for k in ('selector','lineage','route','source_frames','source_timebase','source_asset_pins','candidate_field_observations','semantic_binding_state','side_effects')}

def validate_report(report: Any,c: Mapping[str,Any]) -> None:
    exact(report,REPORT_KEYS,'report')
    if report.get('schema')!=REPORT_ID or report.get('schema_version')!='1.0' or report.get('contract_sha256')!=CONTRACT_SHA256 or report.get('frozen_manifest_sha256')!=FROZEN_SHA: raise ContractError('report identity/pins mismatch')
    if report['source_pin_count']!=c['source_pin_count'] or report['selector_count_expected']!=9 or report['godot_runtime_processes_expected']!=18: raise ContractError('report denominator mismatch')
    if report['payload_materialized'] is not False or report['media_created'] is not False or report['approved_bindings']!=0 or report['visual_seed_sensitivity']!='NOT_TESTED' or report['governance_locks']!=GOVERNANCE: raise ContractError('report policy/governance mismatch')
    rows=report['selectors']
    if not isinstance(rows,list) or len(rows)!=9 or [x.get('selector',{}).get('challenge_id') for x in rows]!=IDS: raise ContractError('report selector denominator mismatch')
    pc=rc=0; any_block=False
    for row,s in zip(rows,c['selectors']):
        exact(row,ROW_KEYS,f'report row {s["challenge_id"]}')
        if row['selector']!=selector_public(s) or row['status'] not in {'ACCEPTED_SOURCE_FRAME_ONLY','BLOCKED','NOT_RUN_AFTER_FIRST_FAILURE'}: raise ContractError('report selector/status mismatch')
        if not isinstance(row['block_reasons'],list): raise ContractError('block reasons must be a list')
        p=row['planner']; exact(p,PLANNER_KEYS,'planner row')
        if p['invocations']==0:
            if p['status']!='NOT_RUN' or any(p[k] is not None for k in PLANNER_KEYS-{'invocations','status'}): raise ContractError('NOT_RUN planner row has stale values')
        elif p['invocations']==1 and p['status']=='PLANNED':
            if not is_sha(p['request_hash']) or not is_sha(p['plan_hash']) or p['bridge_status']!='PLANNING_ONLY_NOT_RENDERABLE' or p['adapter_status']!='PREPARED_NOT_DISPATCHED_RENDERER_DISABLED' or p['gameplay_seed']==p['music_seed']: raise ContractError('planner/adapter lineage invalid')
        elif p['invocations']==1 and p['status']=='BLOCKED':
            if any(p[k] is not None for k in PLANNER_KEYS-{'invocations','status'}): raise ContractError('blocked planner row must not carry stale hashes/seeds')
        else: raise ContractError('planner status/count invalid')
        pc+=p['invocations']; runs=row['runtime_runs']
        if not isinstance(runs,list) or len(runs)>2: raise ContractError('runtime run list invalid')
        for run in runs:
            exact(run,RUN_KEYS,'runtime run'); rc+=1
            if not is_sha(run['stdout_sha256']) or not is_sha(run['stderr_sha256']) or not isinstance(run['process_id'],int) or run['process_id']<0: raise ContractError('runtime log/process fields invalid')
            if run['receipt'] is None:
                if run['receipt_sha256'] is not None: raise ContractError('receipt hash without receipt')
            else:
                validate_receipt(run['receipt'],c,s)
                if run['receipt_sha256']!=sha_bytes(canon(run['receipt'])): raise ContractError('receipt hash mismatch')
        if row['status']=='ACCEPTED_SOURCE_FRAME_ONLY':
            if row['block_reasons'] or len(runs)!=2 or any(x['exit_code']!=0 or x['receipt'] is None for x in runs) or row['repeat_agreement'] is not True or p['invocations']!=1: raise ContractError('accepted row lacks two agreeing receipts/planner')
            if runs[0]['run_id'] == runs[1]['run_id'] or runs[0]['process_id'] == runs[1]['process_id']: raise ContractError('repeat receipts did not come from independent processes')
            if determinism_signature(runs[0]['receipt']) != determinism_signature(runs[1]['receipt']): raise ContractError('report claims repeat agreement while deterministic receipt fields differ')
        else:
            any_block=True
            if not row['block_reasons'] or row['repeat_agreement'] not in (False,None): raise ContractError('blocked row lacks explicit reason or claims repeat agreement')
    if pc!=report['planner_invocations'] or rc!=report['godot_runtime_process_invocations']: raise ContractError('report invocation counters mismatch')
    if report['status']!=('BLOCKED' if any_block else 'PASS_SOURCE_FRAME_ROUTE_ONLY'): raise ContractError('top-level status contradicts selector rows')

def make_planner(root: Path,s: Mapping[str,Any]) -> dict[str,Any]:
    d9=str(root/'tools'/'c11d'/'d9')
    if d9 not in sys.path: sys.path.insert(0,d9)
    import universal_producer as planner
    import universal_editorial_model as editorial
    import d_renderer_dynamic_request_payload_binding as binder
    from editorial_render_bridge import build_bridge_planning_record
    from d_render_adapter import prepare_d_only_adapter_envelope
    source=json.loads((root/s['source_path']).read_text(encoding='utf-8')); generation=source.get('generation',{})
    seed=generation.get('seed') if isinstance(generation,dict) else None; music_seed=840001
    if isinstance(seed,bool) or not isinstance(seed,int) or not 1<=seed<=2147483646 or seed==music_seed: raise ContractError(f'explicit/separate seeds missing for {s["challenge_id"]}')
    resolved=editorial.resolve_selection({'content_type':'challenges','family_id':None,'subtype_id':None,'variant_id':s['challenge_id']},root)
    selection={k:resolved.get(k) for k in ('content_type','family_id','subtype_id','variant_id')}
    if selection != {'content_type':'challenges','family_id':s['family_id'],'subtype_id':None,'variant_id':s['challenge_id']}: raise ContractError(f'canonical selection route mismatch for {s["challenge_id"]}')
    raw=binder._base_request(selection,f'C11D-V2C-{s["challenge_id"]}'); raw['seed']=seed; raw['music_seed']=music_seed
    # From this point onward one canonical planner invocation is in flight; failures must count it.
    try:
        result=planner.evaluate_universal_request(raw,root)
        if result.get('status')!='PLANNED': raise ContractError(f'canonical planner returned {result.get("status")}')
        bridge=build_bridge_planning_record(result,root); adapter=prepare_d_only_adapter_envelope(result,bridge,root); plan=result.get('plan',{})
        if bridge.get('status')!='PLANNING_ONLY_NOT_RENDERABLE' or adapter.get('status')!='PREPARED_NOT_DISPATCHED_RENDERER_DISABLED': raise ContractError('D9.10 planning-only route boundary mismatch')
        if plan.get('renderer_activation') is not False or plan.get('production_execution') is not False or plan.get('d4_8')!='BLOCKED' or plan.get('release_authority')!='NONE': raise ContractError('planner governance gate mismatch')
        return {'invocations':1,'status':'PLANNED','request_hash':result['request_hash'],'plan_hash':result['plan_hash'],'bridge_status':bridge['status'],'adapter_status':adapter['status'],'gameplay_seed':seed,'music_seed':music_seed}
    except Exception as exc:
        raise PlannerInvocationFailed(f'{s["challenge_id"]}:{type(exc).__name__}:{exc}') from exc

def resolve_godot(explicit: str|None) -> str|None:
    candidates=[explicit,os.environ.get('C11D_GODOT_EXECUTABLE','').strip(),shutil.which('godot.exe'),shutil.which('godot')]
    for item in candidates:
        if not item: continue
        val=item.strip('"'); p=Path(val)
        if p.is_file(): return str(p.resolve())
        found=shutil.which(val)
        if found: return found
    return None

def version_probe(exe: str) -> tuple[str,int,str,str]:
    try:
        p=subprocess.run([exe,'--version'],capture_output=True,text=True,timeout=20,check=False); combined=((p.stdout or '')+'\n'+(p.stderr or '')).strip(); ver=combined.splitlines()[0].strip() if combined else ''
        return ver,int(p.returncode),sha_bytes((p.stdout or '').encode()),sha_bytes((p.stderr or '').encode())
    except (OSError,subprocess.TimeoutExpired) as e: return f'PROBE_ERROR:{type(e).__name__}:{e}',127,sha_bytes(b''),sha_bytes(str(e).encode())

def run_godot(exe: str,verified_version: str,root: Path,ev: Path,s: Mapping[str,Any],p: Mapping[str,Any],n: int,csha: str,c: Mapping[str,Any]) -> tuple[dict[str,Any],str|None]:
    cid=s['challenge_id']; rid=f'{cid}_R{n}'; prefix=ev/f'{cid}_R{n}'
    cmd=[exe,'--headless','--path',str(root),'--script',HARNESS,'--',f'--challenge-id={cid}',f'--contract-sha256={csha}',f'--run-id={rid}',f'--godot-version={verified_version}',f'--planner-request-hash={p["request_hash"]}',f'--planner-plan-hash={p["plan_hash"]}']
    pid=0; code=127; out=''; err=''; timed_out=False
    try:
        proc=subprocess.Popen(cmd,cwd=str(root),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace'); pid=int(proc.pid or 0)
        try: out,err=proc.communicate(timeout=180); code=int(proc.returncode if proc.returncode is not None else 127)
        except subprocess.TimeoutExpired:
            timed_out=True; proc.kill(); out,err=proc.communicate(); code=int(proc.returncode if proc.returncode is not None else 124); err+='\nV2C_TIMEOUT: Godot exceeded 180 seconds.\n'
    except OSError as e: err=f'V2C_PROCESS_START_ERROR:{type(e).__name__}:{e}'
    ob=out.encode('utf-8'); eb=err.encode('utf-8'); (prefix.with_suffix('.out')).write_bytes(ob); (prefix.with_suffix('.err')).write_bytes(eb)
    marker='C11D_V2C_SOURCE_FRAME_RECEIPT='; hits=[x[len(marker):] for x in out.splitlines() if x.startswith(marker)]; receipt=None; fail=None
    if timed_out: fail='GODOT_PROCESS_TIMEOUT'
    elif code!=0: fail=f'GODOT_EXIT_NONZERO:{code}'
    elif len(hits)!=1: fail=f'GODOT_RECEIPT_MARKER_COUNT:{len(hits)}'
    else:
        try:
            receipt=json.loads(hits[0]); validate_receipt(receipt,c,s)
            if receipt['process']['run_id']!=rid or receipt['process']['process_id']!=pid: raise ContractError('receipt process identity mismatch')
            if receipt['route']['planner_request_hash']!=p['request_hash'] or receipt['route']['planner_plan_hash']!=p['plan_hash']: raise ContractError('receipt planner lineage mismatch')
        except (json.JSONDecodeError,ContractError,KeyError,TypeError) as e: receipt=None; fail=f'GODOT_RECEIPT_INVALID:{e}'
    run={'run_id':rid,'process_id':pid,'exit_code':code,'stdout_sha256':sha_bytes(ob),'stderr_sha256':sha_bytes(eb),'receipt_sha256':sha_bytes(canon(receipt)) if receipt is not None else None,'receipt':receipt}
    return run,fail

def signature(r: Mapping[str,Any]) -> dict[str,Any]: return determinism_signature(r)
def blank_row(s: Mapping[str,Any],status='NOT_RUN_AFTER_FIRST_FAILURE',reason='NOT_RUN_AFTER_FIRST_FAILURE') -> dict[str,Any]:
    return {'selector':selector_public(s),'status':status,'block_reasons':[reason],'planner':{'invocations':0,'status':'NOT_RUN','request_hash':None,'plan_hash':None,'bridge_status':None,'adapter_status':None,'gameplay_seed':None,'music_seed':None},'runtime_runs':[],'repeat_agreement':None}
def evidence_hashes(ev: Path) -> dict[str,str]: return {p.name:sha_file(p) for p in sorted(ev.iterdir()) if p.is_file() and p.name!='report.json'}

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--repo-root',default='.'); ap.add_argument('--evidence-dir',required=True); ap.add_argument('--godot',default=None); args=ap.parse_args()
    root=Path(args.repo_root).resolve(); ev=Path(args.evidence_dir).resolve()
    if not root.is_dir() or not (root/'project.godot').is_file(): print('C11D_V2C_RESULT=BLOCKED reason=INVALID_REPO_ROOT',file=sys.stderr); return 2
    if ev.exists() and any(ev.iterdir()): print('C11D_V2C_RESULT=BLOCKED reason=EVIDENCE_DIR_NOT_EMPTY',file=sys.stderr); return 2
    ev.mkdir(parents=True,exist_ok=True); report_path=ev/'report.json'; failure=None; contract=None; csha=CONTRACT_SHA256; pin_errors=[]; version=''; vcode=-1; vout=sha_bytes(b''); verr=sha_bytes(b''); probes=0; planner_calls=0; runtime_calls=0; rows=[]
    try:
        contract,csha=load_contract(root); pin_errors=verify_pins(root,contract)
        if pin_errors: failure='SOURCE_PIN_RECONCILIATION_FAILED:'+pin_errors[0]
        exe=resolve_godot(args.godot) if not failure else None
        if not failure and not exe: failure='GODOT_EXECUTABLE_NOT_RESOLVED'
        if exe and not failure:
            probes=1; version,vcode,vout,verr=version_probe(exe)
            if vcode!=0 or '4.7.1' not in version or 'mono' not in version.lower(): failure=f'GODOT_4_7_1_MONO_REQUIRED:exit={vcode}:version={version}'
        if failure:
            rows=[blank_row(s,'BLOCKED',failure) for s in contract['selectors']]
        else:
            for i,s in enumerate(contract['selectors']):
                row=blank_row(s); row['block_reasons']=[]
                # One canonical planner call is recorded only after the planner actually returned a result.
                try:
                    preg=make_planner(root,s); planner_calls+=1; row['planner']=preg
                except PlannerInvocationFailed as e:
                    planner_calls+=1; row['planner']={'invocations':1,'status':'BLOCKED','request_hash':None,'plan_hash':None,'bridge_status':None,'adapter_status':None,'gameplay_seed':None,'music_seed':None}
                    row['status']='BLOCKED'; row['block_reasons']=[f'CANONICAL_PLANNER_OR_ROUTE_BLOCKED:{type(e).__name__}:{e}']; rows.append(row); failure=row['block_reasons'][0]; rows.extend(blank_row(x) for x in contract['selectors'][i+1:]); break
                except Exception as e:
                    row['status']='BLOCKED'; row['block_reasons']=[f'CANONICAL_SELECTION_PREPARATION_BLOCKED:{type(e).__name__}:{e}']; rows.append(row); failure=row['block_reasons'][0]; rows.extend(blank_row(x) for x in contract['selectors'][i+1:]); break
                for n in (1,2):
                    run,err=run_godot(exe,version,root,ev,s,preg,n,csha,contract); runtime_calls+=1; row['runtime_runs'].append(run)
                    if err:
                        row['status']='BLOCKED'; row['block_reasons']=[err]; rows.append(row); failure=err; rows.extend(blank_row(x) for x in contract['selectors'][i+1:]); break
                if failure: break
                row['repeat_agreement']=signature(row['runtime_runs'][0]['receipt'])==signature(row['runtime_runs'][1]['receipt'])
                if not row['repeat_agreement']:
                    row['status']='BLOCKED'; row['block_reasons']=['INDEPENDENT_PROCESS_REPEAT_MISMATCH']; rows.append(row); failure=row['block_reasons'][0]; rows.extend(blank_row(x) for x in contract['selectors'][i+1:]); break
                row['status']='ACCEPTED_SOURCE_FRAME_ONLY'; rows.append(row)
        if len(rows)!=9: raise ContractError(f'row denominator loss: {len(rows)}/9')
        final_pins=verify_pins(root,contract)
        if final_pins:
            failure='SOURCE_PIN_DRIFT_AFTER_RUNTIME:'+final_pins[0]
            for row in rows:
                row['status']='BLOCKED'; row['block_reasons']=(row['block_reasons'] or [])+[failure]; row['repeat_agreement']=None
        status='PASS_SOURCE_FRAME_ROUTE_ONLY' if all(r['status']=='ACCEPTED_SOURCE_FRAME_ONLY' for r in rows) else 'BLOCKED'
        report={'schema':REPORT_ID,'schema_version':'1.0','status':status,'contract_sha256':csha,'frozen_manifest_sha256':FROZEN_SHA,'source_pin_count':contract['source_pin_count'],'selector_count_expected':9,'selectors':rows,'planner_invocations':planner_calls,'godot_version_probe_invocations':probes,'godot_runtime_process_invocations':runtime_calls,'godot_runtime_processes_expected':18,'payload_materialized':False,'media_created':False,'approved_bindings':0,'visual_seed_sensitivity':'NOT_TESTED','governance_locks':GOVERNANCE,'evidence':{'directory':str(ev),'godot_executable':resolve_godot(args.godot) if probes else None,'godot_version':version,'godot_version_probe_exit_code':vcode,'godot_version_stdout_sha256':vout,'godot_version_stderr_sha256':verr,'source_pin_errors_before_runtime':pin_errors,'failure':failure,'evidence_file_sha256':evidence_hashes(ev),'scope_note':'Source-frame/route acceptance only; no payload, media, renderer input or visual seed sensitivity.'}}
        validate_report(report,contract)
    except Exception as e:
        message=f'{type(e).__name__}:{e}'; print('C11D_V2C_DIAGNOSTIC='+message,file=sys.stderr)
        if contract is None:
            # Preserve a fixed denominator even when the contract itself cannot be parsed.
            rows=[blank_row({'challenge_id':cid,'mechanic':'unknown','family_id':'unknown'},'BLOCKED','CONTRACT_PREFLIGHT_FAILED:'+message) for cid in IDS]
            report={'schema':REPORT_ID,'schema_version':'1.0','status':'BLOCKED','contract_sha256':csha if is_sha(csha) else '0'*64,'frozen_manifest_sha256':FROZEN_SHA,'source_pin_count':0,'selector_count_expected':9,'selectors':rows,'planner_invocations':0,'godot_version_probe_invocations':probes,'godot_runtime_process_invocations':runtime_calls,'godot_runtime_processes_expected':18,'payload_materialized':False,'media_created':False,'approved_bindings':0,'visual_seed_sensitivity':'NOT_TESTED','governance_locks':GOVERNANCE,'evidence':{'directory':str(ev),'godot_version':version,'source_pin_errors_before_runtime':pin_errors,'failure':message}}
        else:
            # If report validation fails, convert all rows to explicit blockers and never claim acceptance.
            for row in rows:
                if row['status']=='ACCEPTED_SOURCE_FRAME_ONLY': row['status']='BLOCKED'; row['block_reasons']=[f'REPORT_VALIDATION_FAILED:{message}']; row['repeat_agreement']=None
            report={'schema':REPORT_ID,'schema_version':'1.0','status':'BLOCKED','contract_sha256':csha,'frozen_manifest_sha256':FROZEN_SHA,'source_pin_count':contract['source_pin_count'],'selector_count_expected':9,'selectors':rows,'planner_invocations':planner_calls,'godot_version_probe_invocations':probes,'godot_runtime_process_invocations':runtime_calls,'godot_runtime_processes_expected':18,'payload_materialized':False,'media_created':False,'approved_bindings':0,'visual_seed_sensitivity':'NOT_TESTED','governance_locks':GOVERNANCE,'evidence':{'directory':str(ev),'godot_version':version,'source_pin_errors_before_runtime':pin_errors,'failure':message}}
    report_sha=dump_json(report_path,report)
    print('C11D_V2C_RESULT='+report['status']); print('C11D_V2C_REPORT='+str(report_path)); print('C11D_V2C_REPORT_SHA256='+report_sha)
    print(f'C11D_V2C_PLANNER_INVOCATIONS={planner_calls}/9'); print(f'C11D_V2C_GODOT_RUNTIME_PROCESSES={runtime_calls}/18'); print(f'C11D_V2C_SELECTORS={sum(x["status"]=="ACCEPTED_SOURCE_FRAME_ONLY" for x in rows)}/9'); print('C11D_V2C_GODOT_VERSION='+version)
    print('C11D_V2C_GOVERNANCE=renderer=OFF;media_created=false;approved_bindings=0;candidate_input_admissible=false;D4.8=BLOCKED;D9.10=PREPARE_ONLY;D10=BLOCKED_FOR_PROMOTION;release_authority=NONE')
    return 0 if report['status']=='PASS_SOURCE_FRAME_ROUTE_ONLY' else 1

if __name__=='__main__': raise SystemExit(main())
