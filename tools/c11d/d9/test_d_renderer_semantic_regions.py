"""Fail-closed tests for D-owned semantic region layout proposal (no rendering)."""
from __future__ import annotations
import ast, copy, json, sys
from pathlib import Path
from typing import Any, Callable
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from d_renderer_candidate import sha256_json
from test_d_renderer_frame_program import _fixture
from d_renderer_semantic_regions import (CONTRACT_REL,OUTPUT_SCHEMA_REL,OUTPUT_SCHEMA,OUTPUT_STATUS,REGIONS,FIELD_TARGETS,DRendererSemanticRegionError,build_semantic_region_proposal,validate_semantic_region_proposal)
def _reseal(x:dict[str,Any])->dict[str,Any]: x['layout_sha256']=sha256_json({k:v for k,v in x.items() if k!='layout_sha256'}); return x
def _reject(label:str,fn:Callable[[],Any])->None:
    try: fn()
    except (DRendererSemanticRegionError,ValueError,TypeError,KeyError): return
    raise AssertionError(f'Expected fail-closed rejection: {label}')
def run_checks()->dict[str,int]:
    tree=ast.parse((HERE/'d_renderer_semantic_regions.py').read_text(encoding='utf-8'))
    forbidden_modules={'subprocess','ffmpeg','godot','shutil','socket','multiprocessing','pygame','cv2','PIL','av'}
    forbidden_calls={'write_text','write_bytes','Popen','system','startfile','run','call','check_call','check_output','unlink','mkdir','makedirs'}
    for n in ast.walk(tree):
        if isinstance(n,ast.Import): assert not any(a.name.split('.')[0] in forbidden_modules for a in n.names)
        elif isinstance(n,ast.ImportFrom): assert (n.module or '').split('.')[0] not in forbidden_modules
        elif isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute): assert n.func.attr not in forbidden_calls, n.func.attr
    sc=json.loads((ROOT/OUTPUT_SCHEMA_REL).read_text(encoding='utf-8'))
    assert sc.get('$schema')=='https://json-schema.org/draft/2020-12/schema' and sc.get('$id')=='urn:c11d:renderer-semantic-region-proposal:v1' and sc.get('additionalProperties') is False
    assert set(sc['required'])==set(sc['properties'])
    for k in ('contract_identity','source_identity','content_identity','canvas_descriptor','coordinate_model','timing_model','execution_boundary'):
        x=sc['properties'][k]; assert x.get('additionalProperties') is False and set(x['required'])==set(x['properties'])
    try: import jsonschema
    except ImportError: jsonschema=None
    if jsonschema: jsonschema.Draft202012Validator.check_schema(sc)
    positive=deterministic=flow=schema_checks=full_schema=0; fixtures={}
    expected_types=('challenges','visual_loops','visual_drills')
    for t in expected_types:
        env,preview,comp,fp=_fixture(t,f'D-REGION-{t.upper()}')
        proposal=build_semantic_region_proposal(fp,comp,preview,env,ROOT)
        repeated=build_semantic_region_proposal(copy.deepcopy(fp),copy.deepcopy(comp),copy.deepcopy(preview),copy.deepcopy(env),ROOT)
        assert proposal==repeated and proposal['schema']==OUTPUT_SCHEMA and proposal['status']==OUTPUT_STATUS
        assert [r['region_id'] for r in proposal['regions']]==['HEADER','CONTENT_STAGE','CHALLENGE_OVERLAY','FOOTER']
        assert proposal['coordinate_model']['pixel_coordinates_emitted'] is False
        assert proposal['execution_boundary']['region_layout_approved'] is False
        assert proposal['execution_boundary']['renderer_native_input_emitted'] is False and proposal['execution_boundary']['media_output_created'] is False
        assert proposal['timing_model']=={'state':'NOT_DEFINED','frame_schedule_defined':False,'durations_emitted':False}
        for reg in proposal['regions']:
            b=reg['bounds_permille']; assert b['x']+b['width']<=1000 and b['y']+b['height']<=1000
            assert reg['geometry_state']=='PROPOSED_NOT_APPROVED'
        byid={i['element_id']:i for i in fp['instructions']}; bindings={b['element_id']:b for b in proposal['text_element_bindings']}
        assert set(byid)==set(bindings)
        for eid,inst in byid.items():
            b=bindings[eid]; assert b['source_field']==inst['source_field'] and b['region_id']==FIELD_TARGETS[inst['source_field']] and b['text_sha256']==inst['text_sha256']
        assert validate_semantic_region_proposal(proposal,fp,comp,preview,env,ROOT) is True
        assert set(proposal)==set(sc['required']); schema_checks+=1
        if jsonschema: jsonschema.Draft202012Validator(sc).validate(proposal); full_schema+=1
        fixtures[t]=(env,preview,comp,fp,proposal); positive+=1; deterministic+=1; flow+=1
    negative=0
    env,prev,comp,fp,original=fixtures['visual_loops']
    mutations=[]
    x=copy.deepcopy(original); x['regions'][0]['bounds_permille']['x']=51; mutations.append(('bounds tamper',x))
    x=copy.deepcopy(original); x['regions'][0]['geometry_state']='APPROVED'; mutations.append(('self-approval',x))
    x=copy.deepcopy(original); x['execution_boundary']['renderer_activation']=True; mutations.append(('renderer activation',x))
    x=copy.deepcopy(original); x['execution_boundary']['media_output_created']=True; mutations.append(('media output',x))
    x=copy.deepcopy(original); x['execution_boundary']['release_authority']='APPROVED'; mutations.append(('release escalation',x))
    x=copy.deepcopy(original); x['regions'].pop(); mutations.append(('missing region',x))
    x=copy.deepcopy(original); x['regions'][1]['region_id']='UNREVIEWED'; mutations.append(('unknown region',x))
    x=copy.deepcopy(original); x['regions'][0]['bounds_permille']['width']=9999; mutations.append(('out of bounds',x))
    x=copy.deepcopy(original); x['regions'][1]['payload_contract']='READY_TO_RENDER'; mutations.append(('payload binding promotion',x))
    x=copy.deepcopy(original); x['text_element_bindings'][0]['region_id']='FOOTER'; mutations.append(('wrong field target',x))
    x=copy.deepcopy(original); x['text_element_bindings'].pop(); mutations.append(('missing text binding',x))
    x=copy.deepcopy(original); x['coordinate_model']['pixel_coordinates_emitted']=True; mutations.append(('pixel coordinates',x))
    x=copy.deepcopy(original); x['timing_model']['frame_schedule_defined']=True; mutations.append(('schedule escalation',x))
    x=copy.deepcopy(original); x['execution_boundary']['renderer_native_input_emitted']=True; mutations.append(('renderer input',x))
    x=copy.deepcopy(original); x['execution_boundary']['c11c_source_mutation']=True; mutations.append(('C11-C mutation',x))
    x=copy.deepcopy(original); x['schema']='C11-D-D9-RENDERER-NEUTRAL-FRAME-PROGRAM-V1'; mutations.append(('wrong schema',x))
    x=copy.deepcopy(original); x['source_identity']['frame_program_sha256']='0'*64; mutations.append(('source lineage',x))
    x=copy.deepcopy(original); x['regions'][1]['bounds_permille']['x']=90; x['regions'][1]['bounds_permille']['width']=930; mutations.append(('overflow x',x))
    x=copy.deepcopy(original); x['regions'][1]['bounds_permille']['y']=500; x['regions'][1]['bounds_permille']['height']=600; mutations.append(('overflow y',x))
    x=copy.deepcopy(original); x['unexpected']=True; mutations.append(('unknown key',x))
    for label,candidate in mutations:
        _reseal(candidate); _reject(label,lambda c=candidate:validate_semantic_region_proposal(c,fp,comp,prev,env,ROOT)); negative+=1
    return {'content_types':positive,'deterministic':deterministic,'editorial_flow':flow,'negative':negative,'schema':schema_checks,'jsonschema':full_schema}
def main()->int:
    r=run_checks();
    print(f"C11-D RENDERER SEMANTIC REGION PROPOSAL PASS | content_types={r['content_types']}/3 | deterministic={r['deterministic']}/3 | editorial_flow={r['editorial_flow']}/3 | negative={r['negative']}/20 | schema={r['schema']}/3 | jsonschema={r['jsonschema']}/3" + ("" if r['jsonschema']==3 else " (optional package absent; strict structural checks PASS)") + " | regions=PROPOSED_NOT_APPROVED | pixel_coordinates=NOT_EMITTED | frame_schedule=NOT_DEFINED | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0
if __name__=='__main__': raise SystemExit(main())
