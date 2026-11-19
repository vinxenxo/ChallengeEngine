#!/usr/bin/env python3
"""Static D Challenge consumer compatibility audit and readback-vector preparation.

This module does NOT execute Godot, the GDScript consumer, FFmpeg, media, or renderer.
It validates the exact 18 derived D envelopes against the pinned current consumer
contract, then emits deterministic source-frame readback vectors for a separately
authorized runtime qualification.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INPUTS_REL=Path('definitions/c11e/test_only/C11E_E6_CHALLENGE_LIVE_CONSUMER_READBACK_PREPARE_ONLY_INPUTS_V1.json')
INPUTS_SHA256='23a36815ff0452b92d16b6ec33b154ec7ee02469e68d8e9dc5995522eddc3f93'
EMPTY_SHA=hashlib.sha256(b'').hexdigest()
SELECTORS=('CHALLENGE_001','CHALLENGE_002','CHALLENGE_004','CHALLENGE_005','CHALLENGE_006','CHALLENGE_007')
VARIANTS=('A','B_REPEAT','C_CHANGED_MUSIC_SEED')
FIELDS=('title','subtitle','player_name','challenge_label','call_to_action','language')
RENDERABLE=('title','subtitle','call_to_action')
REGIONS={'title':'HEADER','subtitle':'HEADER','player_name':'CHALLENGE_OVERLAY','challenge_label':'CHALLENGE_OVERLAY','call_to_action':'FOOTER','language':'METADATA'}
WINDOWS={'title':['HOOK'],'subtitle':['HOOK'],'player_name':['HOOK','GAME'],'challenge_label':['HOOK','GAME'],'call_to_action':['CTA'],'language':[]}
READY='READY_FOR_ISOLATED_TEST_PIXEL_DRAW'; OMITTED='OMITTED_EMPTY'; BLOCKED='BLOCKED_GEOMETRY_UNRESOLVED'; META='METADATA_ONLY'
class AuditError(RuntimeError): pass

def hbytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def hfile(p:Path)->str:
    d=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):d.update(c)
    return d.hexdigest()
def safe_rel(s:str)->Path:
    p=Path(s)
    if not s or p.is_absolute() or '\\' in s or ':' in s or '..' in p.parts or s.startswith('/'):
        raise AuditError('UNSAFE_RELATIVE_PATH:'+s)
    return p
def read_json(p:Path)->Any:
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:raise AuditError('JSON_READ_FAILED:%s:%s'%(p,type(e).__name__)) from e
def read_pinned_json(p:Path,expected_sha:str)->Any:
    if not p.is_file():raise AuditError('INPUTS_FILE_MISSING:'+str(p))
    raw=p.read_bytes();actual=hbytes(raw)
    if actual!=expected_sha:raise AuditError('INPUTS_SHA_MISMATCH:'+actual)
    sp=Path(str(p)+'.sha256')
    if not sp.is_file():raise AuditError('INPUTS_SIDECAR_MISSING:'+str(sp))
    try:side=sp.read_text(encoding='ascii').strip()
    except Exception as e:raise AuditError('INPUTS_SIDECAR_READ_FAILED:'+type(e).__name__) from e
    m=re.fullmatch(r'([0-9a-fA-F]{64})(?:\s+.+)?',side)
    if not m or m.group(1).lower()!=actual:raise AuditError('INPUTS_SIDECAR_MISMATCH:'+str(sp))
    try:return json.loads(raw.decode('utf-8'))
    except Exception as e:raise AuditError('INPUTS_JSON_INVALID_UTF8:'+type(e).__name__) from e
def validate_binding_install_receipt(receipt:dict)->None:
    if receipt.get('status')!='PASS_ADD_ONLY_INSTALL_COMMITTED' or int(receipt.get('added',-1))!=19 or int(receipt.get('replaced',-1))!=0:
        raise AuditError('BINDING_INSTALL_RECEIPT_NOT_SUCCESSFUL')
def verify_file(root:Path,rel:str,expected_sha:str,sidecar:bool=True)->dict:
    p=root/safe_rel(rel)
    if not p.is_file():raise AuditError('FILE_MISSING:'+rel)
    actual=hfile(p)
    if actual!=expected_sha:raise AuditError('FILE_SHA_MISMATCH:%s:%s'%(rel,actual))
    if sidecar:
        sp=Path(str(p)+'.sha256')
        if not sp.is_file():raise AuditError('SIDECAR_MISSING:'+str(sp))
        m=re.fullmatch(r'([0-9a-fA-F]{64})(?:\s+.+)?',sp.read_text(encoding='ascii').strip())
        if not m or m.group(1).lower()!=actual:raise AuditError('SIDECAR_MISMATCH:'+str(sp))
    return {'path':rel,'bytes':p.stat().st_size,'sha256':actual,'sidecar':'PASS' if sidecar else 'NOT_REQUIRED'}
def phase_rows(env:dict)->dict:
    tb=env.get('source_timebase')
    if not isinstance(tb,dict) or int(tb.get('fps',-1))!=60 or int(tb.get('total_frames',0))<=0 or tb.get('kind')!='SOURCE_FRAME_INDEX':
        raise AuditError('SOURCE_TIMEBASE_INVALID')
    rows=env.get('source_phase_ranges')
    if not isinstance(rows,list) or len(rows)!=4:raise AuditError('PHASE_SET_INVALID')
    out={}; cursor=0; total=int(tb['total_frames'])
    for r in rows:
        name=str(r.get('phase',''))
        st=int(r.get('start_frame',-1)); en=int(r.get('end_frame',-1))
        if name not in ('HOOK','GAME','REVEAL','CTA') or name in out or st!=cursor or en<st or en>total or r.get('timebase')!='SOURCE_FPS_HALF_OPEN':
            raise AuditError('PHASE_RANGE_INVALID:'+name)
        out[name]=r;cursor=en
    if set(out)!=set(('HOOK','GAME','REVEAL','CTA')) or cursor!=total:raise AuditError('PHASE_COVERAGE_INVALID')
    return out
def ranges_for(name:str, phases:dict)->list:
    return [{'phase':p,'start_frame':int(phases[p]['start_frame']),'end_frame':int(phases[p]['end_frame']),'timebase':'SOURCE_FPS_HALF_OPEN'} for p in WINDOWS[name]]
def check_consumer_source(root:Path,pins:list)->dict:
    found={}
    for pin in pins:
        rel=pin['path']; path=root/safe_rel(rel)
        if not path.is_file() or path.stat().st_size!=int(pin['bytes']) or hfile(path)!=pin['sha256']:
            raise AuditError('RUNTIME_SOURCE_PIN_MISMATCH:'+rel)
        found[rel]=path.read_text(encoding='utf-8')
    consumer=found['tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd']
    adapter=found['tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd']
    required_consumer=(
      'const EnvelopeSchema := "C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1"',
      'const ApprovedPolicySha := "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5"',
      'const LayoutContractSha := "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461"',
      'func validate_envelope(', 'func apply_after_native_bind(',
      'if disposition == "READY_FOR_ISOLATED_TEST_PIXEL_DRAW":',
      'elif disposition == "OMITTED_EMPTY":',
      'func _source_frame_ranges_match(',
      'ChallengeEditorialAdapter.build_shared_editorial_model(',
      'ChallengeEditorialAdapter.adapt_native_challenge_render_model(',
      'renderer_input_emitted": false',
    )
    missing=[x for x in required_consumer if x not in consumer]
    if missing:raise AuditError('CONSUMER_STATIC_CONTRACT_MISSING:'+repr(missing))
    required_adapter=(
      'static func build_shared_editorial_model(',
      'if disposition == "OMITTED_EMPTY" or disposition == "METADATA_ONLY" or disposition == "BLOCKED_GEOMETRY_UNRESOLVED":',
      'if start_frame < 0 or end_frame <= start_frame or end_frame > source_frame_count:',
      'var header_native_hook_migrated := header_active and show_hook_countdown and not clean_hook.is_empty()',
      '"D_C11C_SHARED_FOOTER" if footer_active else "C_CHALLENGE_PRESENTATION_UI"',
    )
    missing=[x for x in required_adapter if x not in adapter]
    if missing:raise AuditError('ADAPTER_STATIC_CONTRACT_MISSING:'+repr(missing))
    return {'consumer_sha256':pins[0]['sha256'],'adapter_sha256':pins[1]['sha256'],'consumer_static_contract':'PASS','adapter_static_contract':'PASS','gdscript_runtime_executed':False}
def validate_consumer_envelope(env:dict,source_env:dict,selector:str,variant:str,policy_sha:str,layout_sha:str)->dict:
    if env.get('schema')!='C11E-CHALLENGE-LIVE-EDITORIAL-ENVELOPE-V1' or env.get('schema_version')!='1.0':raise AuditError('CONSUMER_SCHEMA_MISMATCH:'+selector+':'+variant)
    if env.get('status')!='PREPARED_E1_NOT_DISPATCHED' or env.get('content_type')!='challenges' or env.get('challenge_id')!=selector:raise AuditError('CONSUMER_IDENTITY_OR_BOUNDARY_MISMATCH:'+selector+':'+variant)
    intent=env.get('e1_intent')
    if not isinstance(intent,dict) or intent!=source_env.get('e1_intent'):raise AuditError('E1_INTENT_MUTATED:'+selector+':'+variant)
    if env.get('intent_hash')!=source_env.get('intent_hash') or env.get('intent_hash')!=intent.get('identity',{}).get('intent_hash'):raise AuditError('E1_INTENT_HASH_MUTATED:'+selector+':'+variant)
    req=intent.get('request',{}); sel=req.get('selection',{})
    if intent.get('schema')!='C11-E-PRODUCTION-INTENT-V1' or intent.get('status')!='PREPARED_E1_NOT_DISPATCHED' or req.get('content_type')!='challenges' or sel.get('content_type')!='challenges' or sel.get('variant_id')!=selector:raise AuditError('NESTED_E1_CONTRACT_INVALID:'+selector+':'+variant)
    if env.get('request_id')!=req.get('request_id'):raise AuditError('REQUEST_ID_MISMATCH:'+selector+':'+variant)
    options=req.get('presentation_options')
    if not isinstance(options,dict) or set(options)!= {'show_hook_countdown'} or not isinstance(options['show_hook_countdown'],bool):raise AuditError('PRESENTATION_OPTION_INVALID:'+selector+':'+variant)
    if env.get('presentation_options')!=options:raise AuditError('PRESENTATION_OPTION_MISMATCH:'+selector+':'+variant)
    if env.get('policy_sha256')!=policy_sha or env.get('layout_contract_sha256')!=layout_sha:raise AuditError('POLICY_LAYOUT_PIN_MISMATCH:'+selector+':'+variant)
    if env.get('source_timebase')!=source_env.get('source_timebase') or env.get('source_phase_ranges')!=source_env.get('source_phase_ranges'):raise AuditError('SOURCE_TIMEBASE_OR_PHASES_MUTATED:'+selector+':'+variant)
    phases=phase_rows(env)
    rows=env.get('fields')
    if not isinstance(rows,list) or len(rows)!=6:raise AuditError('FIELD_COUNT_INVALID:'+selector+':'+variant)
    by={}
    for row in rows:
        n=str(row.get('field',''))
        if n not in FIELDS or n in by:raise AuditError('FIELD_ALLOWLIST_INVALID:'+selector+':'+variant)
        by[n]=row
    if set(by)!=set(FIELDS):raise AuditError('FIELD_ALLOWLIST_INCOMPLETE:'+selector+':'+variant)
    visible=[]; omitted=[]
    for name in FIELDS:
        row=by[name]
        if row.get('region')!=REGIONS[name] or row.get('source_phase_windows')!=WINDOWS[name] or row.get('policy_sha256')!=policy_sha or row.get('layout_contract_sha256')!=layout_sha:
            raise AuditError('FIELD_POLICY_MISMATCH:%s:%s:%s'%(selector,variant,name))
        expected_ranges=ranges_for(name,phases)
        if row.get('source_frame_ranges')!=expected_ranges:raise AuditError('FIELD_RANGE_MISMATCH:%s:%s:%s'%(selector,variant,name))
        value=str(row.get('effective_value',''))
        if row.get('value_sha256')!=hbytes(value.encode('utf-8')):raise AuditError('FIELD_VALUE_HASH_MISMATCH:%s:%s:%s'%(selector,variant,name))
        if name in RENDERABLE:
            active=sum(x['end_frame']-x['start_frame'] for x in expected_ranges)
            if active==0:
                if row.get('disposition')!=OMITTED or value!='' or row.get('value_sha256')!=EMPTY_SHA:raise AuditError('ZERO_WINDOW_NOT_OMITTED:%s:%s:%s'%(selector,variant,name))
                omitted.append(name)
            else:
                if row.get('disposition')!=READY or not value.strip():raise AuditError('POSITIVE_WINDOW_NOT_READY:%s:%s:%s'%(selector,variant,name))
                visible.append(name)
        elif name in ('player_name','challenge_label'):
            if value not in ('','UNKNOWN') or row.get('disposition') not in (OMITTED,BLOCKED):raise AuditError('IDENTITY_FIELD_VISUALIZED:%s:%s:%s'%(selector,variant,name))
        else:
            if value not in ('','UNKNOWN','es') or row.get('disposition') not in (OMITTED,META):raise AuditError('LANGUAGE_FIELD_VISUALIZED:%s:%s'% (selector,variant))
    gov=env.get('governance',{})
    if gov.get('renderer_input_emitted') is not False or gov.get('production_dispatch') is not False or gov.get('media_created') is not False or gov.get('release_authority')!='NONE' or gov.get('d4_8')!='BLOCKED' or gov.get('d9_10')!='PREPARE_ONLY':raise AuditError('ENVELOPE_GOVERNANCE_INVALID:'+selector+':'+variant)
    return {'visible_fields':visible,'omitted_zero_window_fields':omitted,'hook_frames':phases['HOOK']['end_frame']-phases['HOOK']['start_frame'],'cta_frames':phases['CTA']['end_frame']-phases['CTA']['start_frame'],'total_frames':int(env['source_timebase']['total_frames']),'fps':int(env['source_timebase']['fps']),'show_hook_countdown':bool(options['show_hook_countdown'])}
def make_frame_plan(env:dict,summary:dict,selector:str,variant:str)->dict:
    phases=phase_rows(env); total=summary['total_frames']; samples=set()
    for p in ('HOOK','GAME','REVEAL','CTA'):
        st=int(phases[p]['start_frame']); en=int(phases[p]['end_frame'])
        if en>st:
            samples.update((st,st+(en-st)//2,en-1))
            if st>0:samples.add(st-1)
            if en<total:samples.add(en)
    frames=[]
    visible=set(summary['visible_fields'])
    hook=phases['HOOK']; cta=phases['CTA']
    for f in sorted(x for x in samples if 0<=x<total):
        header=bool(visible.intersection({'title','subtitle'})) and int(hook['start_frame'])<=f<int(hook['end_frame'])
        footer='call_to_action' in visible and int(cta['start_frame'])<=f<int(cta['end_frame'])
        frames.append({'source_frame':f,'phase':next((p for p,r in phases.items() if int(r['start_frame'])<=f<int(r['end_frame'])),None),'expected_d_header_active':header,'expected_d_footer_active':footer,'native_hook_migration':'CONDITIONAL_HEADER_ACTIVE_AND_SHOW_HOOK_COUNTDOWN_AND_NATIVE_HOOK_TEXT_NONEMPTY' if header and summary['show_hook_countdown'] else 'FALSE','expected_native_cta_owner':'D_C11C_SHARED_FOOTER' if footer else 'C_CHALLENGE_PRESENTATION_UI','expected_reserved_header_footer_bands':'BLACK','expected_mount_count':1,'required_runtime_observation':['header_active','footer_active','native_cta_owner','native_hook_label_visibility','countdown_visibility','reserved_band_black','mount_count']})
    return {'selector':selector,'variant':variant,'source_fps':summary['fps'],'total_frames':total,'phase_frames':{p:{'start':int(r['start_frame']),'end':int(r['end_frame']),'duration':int(r['end_frame'])-int(r['start_frame'])} for p,r in phases.items()},'frame_samples':frames}
def run(project_root:Path,inputs_path:Path|None=None)->dict:
    root=project_root.resolve(strict=True); inputs_path=inputs_path or (root/INPUTS_REL)
    inputs=read_pinned_json(inputs_path,INPUTS_SHA256)
    if inputs.get('schema')!='C11E-E6-CHALLENGE-LIVE-CONSUMER-READBACK-PREPARE-ONLY-INPUTS-V1' or inputs.get('status')!='PINNED_INPUTS_PREPARE_ONLY_NOT_RUNTIME_AUTHORIZATION':raise AuditError('INPUTS_SCHEMA_OR_STATUS_INVALID')
    pins=[]
    for pin in inputs['runtime_source_pins']:
        pins.append(verify_file(root,pin['path'],pin['sha256'],False))
    static=check_consumer_source(root,inputs['runtime_source_pins'][:2])
    bind=inputs['binding_run']; broot=safe_rel(bind['root'])
    mrel=(broot/bind['manifest_name']).as_posix(); rrel=(broot/bind['receipt_name']).as_posix()
    mcheck=verify_file(root,mrel,bind['manifest_sha256'],True); rcheck=verify_file(root,rrel,bind['receipt_sha256'],True)
    icheck=verify_file(root,bind['install_receipt_path'],bind['install_receipt_sha256'],True)
    manifest=read_json(root/mrel); receipt=read_json(root/rrel); install_receipt=read_json(root/safe_rel(bind['install_receipt_path']))
    validate_binding_install_receipt(install_receipt)
    if manifest.get('status')!='PASS_PREPARE_ONLY_18_CHALLENGE_ENVELOPES_27_VISIBLE_27_SUPPRESSED' or manifest.get('run_id')!=bind['run_id']:raise AuditError('BINDING_MANIFEST_STATUS_OR_RUN_ID_INVALID')
    if receipt.get('status')!=manifest['status'] or receipt.get('run_id')!=bind['run_id'] or receipt.get('manifest_sha256')!=bind['manifest_sha256'] or receipt.get('runtime_editorial_readback')!='NOT_PROVEN':raise AuditError('BINDING_RECEIPT_LINKAGE_INVALID')
    counts=manifest.get('counts',{})
    expected=inputs['expected_counts']
    for k in ('selectors','nested_probes','bound_envelopes','editorial_slots','visible_slots','intentionally_suppressed_zero_window_slots'):
        target={'selectors':'selectors','nested_probes':'probes','bound_envelopes':'envelopes','editorial_slots':'editorial_slots','visible_slots':'visible','intentionally_suppressed_zero_window_slots':'omitted_zero_window'}[k]
        if int(counts.get(k,-1))!=int(expected[target]):raise AuditError('BINDING_MANIFEST_COUNT_INVALID:'+k)
    if len(manifest.get('outputs',[]))!=18 or receipt.get('output_envelopes')!=18:raise AuditError('BOUND_OUTPUT_COUNT_INVALID')
    policy_sha=next(p['sha256'] for p in inputs['runtime_source_pins'] if p['path'].endswith('C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json'))
    layout_sha=next(p['sha256'] for p in inputs['runtime_source_pins'] if p['path'].endswith('D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md'))
    records=[]; frame_plans=[]; visible_total=0; omitted_total=0; observed=set()
    for rec in manifest['outputs']:
        selector=str(rec['selector']); variant=str(rec['variant']); key=(selector,variant)
        if selector not in SELECTORS or variant not in VARIANTS or key in observed:raise AuditError('OUTPUT_IDENTITY_OR_DUPLICATE_INVALID:'+str(key))
        observed.add(key)
        outrel=(broot/Path(rec['output_relative_path'])).as_posix()
        outcheck=verify_file(root,outrel,rec['output_sha256'],True)
        if outcheck['bytes']!=int(rec['output_bytes']):raise AuditError('BOUND_OUTPUT_BYTES_MISMATCH:'+outrel)
        source_env=verify_file(root,rec['source_envelope_path'],rec['source_envelope_sha256'],True)
        source_intent=verify_file(root,rec['source_intent_path'],rec['source_intent_sha256'],True)
        env=read_json(root/outrel); original=read_json(root/rec['source_envelope_path']); intent=read_json(root/rec['source_intent_path'])
        if original.get('e1_intent')!=intent:raise AuditError('SOURCE_E1_INTENT_LINK_MISMATCH:'+str(key))
        summary=validate_consumer_envelope(env,original,selector,variant,policy_sha,layout_sha)
        if env.get('e1_intent')!=intent:raise AuditError('DERIVED_NESTED_INTENT_MISMATCH:'+str(key))
        if rec.get('visible_fields')!=summary['visible_fields'] or rec.get('suppressed_zero_window_fields')!=summary['omitted_zero_window_fields']:raise AuditError('MANIFEST_FIELD_COUNTS_MISMATCH:'+str(key))
        if summary['hook_frames']!=int(rec['hook_frames']) or summary['cta_frames']!=int(rec['cta_frames']):raise AuditError('MANIFEST_PHASE_DURATION_MISMATCH:'+str(key))
        visible_total+=len(summary['visible_fields']);omitted_total+=len(summary['omitted_zero_window_fields'])
        frame_plans.append(make_frame_plan(env,summary,selector,variant))
        records.append({'selector':selector,'variant':variant,'bound_envelope_path':outrel,'bound_envelope_sha256':rec['output_sha256'],'source_envelope_sha256':source_env['sha256'],'source_intent_sha256':source_intent['sha256'],'consumer_contract':'PASS_STATIC','visible_fields':summary['visible_fields'],'omitted_zero_window_fields':summary['omitted_zero_window_fields'],'hook_frames':summary['hook_frames'],'cta_frames':summary['cta_frames'],'frame_sample_count':len(frame_plans[-1]['frame_samples'])})
    if observed!={(s,v) for s in SELECTORS for v in VARIANTS}:raise AuditError('PROBE_CARTESIAN_PRODUCT_INCOMPLETE')
    if visible_total!=27 or omitted_total!=27:raise AuditError('VISIBLE_OMITTED_TOTAL_MISMATCH')
    governance=inputs['governance']
    if governance['d4_8']!='BLOCKED' or governance['renderer']!='OFF' or governance['e6_test_only_execution_authorized'] is not False or governance['release_authority']!='NONE':raise AuditError('INPUT_GOVERNANCE_NOT_HELD')
    parent=root/'artifacts/tests/c11e/e6_challenge_live_consumer_readback_prepare_only'
    parent.mkdir(parents=True,exist_ok=True)
    run_id='E6CHLIVECONTRACT_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+uuid.uuid4().hex[:8].upper()
    out=parent/run_id;out.mkdir()
    plan={'schema':'C11E-E6-CHALLENGE-LIVE-CONSUMER-READBACK-PLAN-V1','status':'PASS_STATIC_CONSUMER_CONTRACT_18_ENVELOPES_RUNTIME_READBACK_NOT_PERFORMED','run_id':run_id,'binding_run_id':bind['run_id'],'binding_manifest_sha256':bind['manifest_sha256'],'binding_receipt_sha256':bind['receipt_sha256'],'binding_install_receipt_sha256':bind['install_receipt_sha256'],'consumer_source_pins':static,'counts':{'selectors':6,'probes':18,'envelopes_static_compatible':18,'visible_field_slots':visible_total,'omitted_zero_window_field_slots':omitted_total,'frame_sample_vectors':sum(len(p['frame_samples']) for p in frame_plans)},'outputs':records,'runtime_frame_plans':frame_plans,'runtime_readback':'NOT_PERFORMED','engine_invocation':'NOT_AUTHORIZED','governance':{'d4_8':'BLOCKED','renderer':'OFF','e6_test_only_execution_authorized':False,'release_authority':'NONE','godot_invoked':False,'ffmpeg_invoked':False,'ffprobe_invoked':False,'audio_generated':False,'mux_invoked':False,'media_created':False,'production_dispatch':False,'e6_accepted':0,'matrix_frozen':False},'limitations':['This is static compatibility validation of exact D envelopes against pinned GDScript source and an offline frame-vector plan.','The GDScript consumer and adapter were not executed in Godot; runtime editorial readback and pixel output remain unproven.','Frame vectors specify expected D header/footer activity and native ownership for a future separately authorized runtime pass.','No D4.8 policy, E1 intent, source envelope, canonical Challenge, C11-C, or production runtime file is modified.']}
    pb=(json.dumps(plan,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8');(out/'E6_CHALLENGE_LIVE_CONSUMER_READBACK_PLAN_V1.json').write_bytes(pb)
    ph=hbytes(pb);(out/'E6_CHALLENGE_LIVE_CONSUMER_READBACK_PLAN_V1.json.sha256').write_text(ph+'  E6_CHALLENGE_LIVE_CONSUMER_READBACK_PLAN_V1.json\n',encoding='ascii')
    receipt={'schema':'C11E-E6-CHALLENGE-LIVE-CONSUMER-READBACK-RECEIPT-V1','status':plan['status'],'run_id':run_id,'plan_path':str((out/'E6_CHALLENGE_LIVE_CONSUMER_READBACK_PLAN_V1.json').relative_to(root)),'plan_sha256':ph,'binding_manifest_sha256':bind['manifest_sha256'],'binding_receipt_sha256':bind['receipt_sha256'],'source_pins':len(pins),'binding_install_receipt_sha256':bind['install_receipt_sha256'],'consumer_compatibility':'PASS_STATIC','runtime_editorial_readback':'NOT_PERFORMED','governance':plan['governance']}
    rb=(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8');(out/'E6_CHALLENGE_LIVE_CONSUMER_READBACK_RECEIPT_V1.json').write_bytes(rb)
    rh=hbytes(rb);(out/'E6_CHALLENGE_LIVE_CONSUMER_READBACK_RECEIPT_V1.json.sha256').write_text(rh+'  E6_CHALLENGE_LIVE_CONSUMER_READBACK_RECEIPT_V1.json\n',encoding='ascii')
    print('BINDING_MANIFEST=PASS/'+bind['manifest_sha256'])
    print('BINDING_RECEIPT=PASS/'+bind['receipt_sha256'])
    print('BINDING_INSTALL_RECEIPT=PASS/'+bind['install_receipt_sha256'])
    print('RUNTIME_SOURCE_PINS=PASS/%d'%len(pins))
    print('GDSCRIPT_STATIC_CONSUMER_CONTRACT=PASS')
    print('CHALLENGE_ENVELOPES=18/18_STATIC_COMPATIBLE')
    print('VISIBLE_SLOTS=27; ZERO_WINDOW_SUPPRESSED=27')
    print('RUNTIME_FRAME_VECTORS=%d'%plan['counts']['frame_sample_vectors'])
    print('RUNTIME_EDITORIAL_READBACK=NOT_PERFORMED')
    print('GODOT=NOT_INVOKED; FFMPEG=NOT_INVOKED; FFPROBE=NOT_INVOKED')
    print('D4_8=BLOCKED; RENDERER=OFF; E6_TEST_ONLY_AUTHORIZED=FALSE; RELEASE_AUTHORITY=NONE')
    print('READBACK_PLAN=%s'%str(out/'E6_CHALLENGE_LIVE_CONSUMER_READBACK_PLAN_V1.json'))
    print('READBACK_PLAN_SHA256=%s'%ph)
    print('READBACK_RECEIPT=%s'%str(out/'E6_CHALLENGE_LIVE_CONSUMER_READBACK_RECEIPT_V1.json'))
    print('READBACK_RECEIPT_SHA256=%s'%rh)
    print('CHALLENGE_LIVE_CONSUMER_READBACK_PREPARE_ONLY=PASS')
    return receipt

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--project-root',required=True);ap.add_argument('--inputs',default=None);a=ap.parse_args()
    try:run(Path(a.project_root),Path(a.inputs) if a.inputs else None)
    except Exception as e:print('READBACK_AUDIT_FAILED=%s:%s'%(type(e).__name__,e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
