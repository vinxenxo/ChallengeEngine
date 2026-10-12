from __future__ import annotations
import copy, json, shutil, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from universal_producer import REQUEST_SCHEMA_ID, evaluate_universal_request
from universal_editorial_model import build_catalog
from editorial_render_bridge import build_bridge_planning_record
from d_render_adapter import prepare_d_only_adapter_envelope, validate_d_only_adapter_envelope
from d_renderer_shared_editorial_presentation_context_binding import build_context_binding_from_result, validate_binding_record
from shared_production_context_service import (
    SharedProductionContextError, prepare_shared_production_context,
    validate_shared_production_context, validate_service_contract, audit, sha256,
)

def make_request(selection: dict, request_id: str) -> dict:
    return {
        'schema':REQUEST_SCHEMA_ID,'schema_version':'1.0','request_id':request_id,'mode':'REVIEW',
        'selection':selection,'seed':12345,'music_seed':840001,'delivery_profile_id':'REVIEW_720',
        'presentation_profile_id':'social_default_v1','variation_index':0,'audio_enabled':True,
        'personalization_enabled':True,'editorial_profile':{},
        'production_override':{'title':' TÍTULO DE PRUEBA ','subtitle':'Subtítulo compartido','call_to_action':'Continuar','language':' ES ',
          **({'player_name':'ANA','challenge_label':'RETO'} if selection.get('content_type')=='challenges' else {})},
        'provenance':{'source_revision':'D9_SHARED_FACADE_TEST','request_origin':'TEST'},
    }

def representative_requests():
    catalog=build_catalog(ROOT)
    challenge=catalog['content_types']['challenges']['families'][0]
    loop_family=next(f for f in catalog['content_types']['visual_loops']['families'] if f['id']=='c11c_geometric_waves_v1')
    drill=catalog['content_types']['visual_drills']['families'][0]
    loop_subtype=next(s['id'] for s in loop_family['subtypes'] if s['id']!='auto')
    return [
      make_request({'content_type':'challenges','family_id':challenge['id'],'variant_id':challenge['variants'][0]['id']},'FACADE-CHALLENGE-001'),
      make_request({'content_type':'visual_loops','family_id':loop_family['id'],'subtype_id':loop_subtype},'FACADE-LOOP-001'),
      make_request({'content_type':'visual_drills','family_id':drill['id'],'variant_id':drill['variants'][0]['id']},'FACADE-DRILL-001'),
    ]

def run_checks():
    state=validate_service_contract(ROOT)
    assert state['lineage_count']==22, state['lineage_count']
    counts=audit(ROOT)
    assert counts=={'source_pins':22,'supported_content_types':3,'composition_stages':6,'cli_gui_backend':'ONE_SHARED_API','result_persistence':'NONE'}
    # The CLI must discover the repository root from its own location without --project-root.
    audit_proc=subprocess.run([sys.executable,str(HERE/'shared_production_context_cli.py'),'--audit-only'],cwd=ROOT,capture_output=True,timeout=60)
    assert audit_proc.returncode==0, f'default-root CLI audit failed: {(audit_proc.stdout or b"")[:500]!r}; {(audit_proc.stderr or b"").decode("utf-8",errors="replace")!r}'
    assert b'C11-D SHARED BACKEND CLI AUDIT PASS' in (audit_proc.stdout or b'')
    requests=representative_requests()
    records=[]
    for req in requests:
        record=prepare_shared_production_context(req,ROOT)
        assert validate_shared_production_context(record,req,ROOT)
        canonical=evaluate_universal_request(req,ROOT)
        bridge=build_bridge_planning_record(canonical,ROOT)
        adapter=prepare_d_only_adapter_envelope(canonical,bridge,ROOT)
        binding=build_context_binding_from_result(canonical,ROOT)
        assert validate_d_only_adapter_envelope(adapter,ROOT)
        assert validate_binding_record(binding,canonical,ROOT)
        assert record['canonical_result']==canonical
        assert record['bridge_planning_record']==bridge
        assert record['d_only_adapter_envelope']==adapter
        assert record['shared_context_binding']==binding
        assert record['identity']['request_sha256']==canonical['request_hash']
        assert record['identity']['editorial_sha256']==canonical['editorial_hash']
        assert record['identity']['plan_sha256']==canonical['plan_hash']
        assert record['execution_boundary']['renderer_native_input_emitted'] is False
        assert record['execution_boundary']['record_persisted'] is False
        assert record['execution_boundary']['renderer_activation'] is False
        records.append(record)
    assert [r['identity']['content_type'] for r in records]==['challenges','visual_loops','visual_drills']
    assert len({r['record_sha256'] for r in records})==3
    # Exact API/CLI parity with Unicode editorial, through UTF-8/ASCII-safe stdout.
    with tempfile.TemporaryDirectory(prefix='c11d_shared_backend_facade_') as temp_name:
        temp=Path(temp_name)
        for i,(req,expected) in enumerate(zip(requests,records)):
            path=temp/f'request-{i}.json'; path.write_text(json.dumps(req,ensure_ascii=False),encoding='utf-8')
            proc=subprocess.run([sys.executable,str(HERE/'shared_production_context_cli.py'),'--project-root',str(ROOT),'--request',str(path)],cwd=ROOT,capture_output=True,timeout=120)
            assert proc.returncode==0, f'CLI code={proc.returncode}; stderr={(proc.stderr or b"").decode("utf-8",errors="replace")!r}; stdout={(proc.stdout or b"")[:500]!r}'
            out=(proc.stdout or b'').decode('ascii')
            assert json.loads(out)==expected
        assert sorted(p.name for p in temp.iterdir())==[f'request-{i}.json' for i in range(3)]
    # Editorial changes affect only editorial/context identities, not gameplay/music or profile identity.
    base=requests[1]; a=prepare_shared_production_context(base,ROOT)
    changed=copy.deepcopy(base); changed['production_override']['title']='OTRO TÍTULO'
    b=prepare_shared_production_context(changed,ROOT)
    assert a['identity']['request_sha256']!=b['identity']['request_sha256']
    assert a['identity']['editorial_sha256']!=b['identity']['editorial_sha256']
    assert a['identity']['shared_context_binding_sha256']!=b['identity']['shared_context_binding_sha256']
    assert a['canonical_result']['plan']['seed']==b['canonical_result']['plan']['seed']
    assert a['canonical_result']['plan']['music_seed']==b['canonical_result']['plan']['music_seed']
    assert a['shared_context_binding']['presentation_binding']==b['shared_context_binding']['presentation_binding']
    # Fail closed: unregistered presentation profile, unknown content type, Longform, corrupt input and tampered returned record.
    negatives=0
    for mutate, expected_fragment in [
        (lambda r:r.update(presentation_profile_id='future_profile'),'Unregistered presentation_profile_id'),
        (lambda r:r['selection'].update(content_type='unknown_type'),'Unsupported content type'),
        (lambda r:r['selection'].update(content_type='longform'),'Unsupported content type'),
        (lambda r:r.update(seed=0),'seed'),
    ]:
        bad=copy.deepcopy(requests[1]); mutate(bad)
        try: prepare_shared_production_context(bad,ROOT)
        except Exception as exc:
            message=str(exc).lower()
            if expected_fragment.lower() not in message and not any(token in message for token in ('unsupported','unknown','longform','invalid','must','seed','profile','content type')):
                raise AssertionError(f'Unexpected rejection: {exc}')
        else: raise AssertionError('Invalid request should fail closed')
        negatives+=1
    tampered=copy.deepcopy(records[1]); tampered['shared_context_binding']['editorial_binding']['resolved_values']['title']='FAKE'
    try: validate_shared_production_context(tampered,requests[1],ROOT)
    except SharedProductionContextError: pass
    else: raise AssertionError('Tampered facade record must reject')
    negatives+=1
    # Reproducibility/self-hash check.
    assert prepare_shared_production_context(requests[1],ROOT)==records[1]
    assert records[1]['context_sha256']==sha256({k:v for k,v in records[1].items() if k not in ('context_sha256','record_sha256')})
    assert records[1]['record_sha256']==sha256({k:v for k,v in records[1].items() if k!='record_sha256'})
    # Source drift fails closed in a temporary mirror only; no active source is changed.
    with tempfile.TemporaryDirectory(prefix='c11d_facade_drift_') as mirror_name:
        mirror=Path(mirror_name)
        for row in state['contract']['source_lineage']:
            src=ROOT/row['path']; dst=mirror/row['path']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        (mirror/'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_V1.json').parent.mkdir(parents=True,exist_ok=True)
        for rel in ('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_SCHEMA_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_SCHEMA_V1.json'):
            src=ROOT/rel; dst=mirror/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        target=mirror/'tools/c11d/d9/universal_producer.py'; target.write_bytes(target.read_bytes()+b'\n# test-only drift\n')
        try: validate_service_contract(mirror)
        except SharedProductionContextError as exc: assert 'Pinned source drift' in str(exc)
        else: raise AssertionError('Pinned source drift must fail closed')
    return {'source_pins':state['lineage_count'],'content_types':len(records),'component_parity':len(records),'cli_parity':len(records),'negatives':negatives,'editorial_mutation':1,'drift_negative':1}

if __name__=='__main__':
    c=run_checks()
    print('C11-D SHARED PRODUCTION CONTEXT FACADE CONTRACT PASS | '
          f"source_pins={c['source_pins']}/{c['source_pins']} | content_types={c['content_types']}/3 | "
          f"component_parity={c['component_parity']}/3 | cli_api_parity={c['cli_parity']}/3 | "
          f"fail_closed_negatives={c['negatives']}/5 | editorial_mutation_seed_isolation={c['editorial_mutation']}/1 | "
          f"source_drift_negative={c['drift_negative']}/1 | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
