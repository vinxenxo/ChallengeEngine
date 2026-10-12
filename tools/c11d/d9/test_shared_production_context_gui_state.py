from __future__ import annotations
import copy, json, subprocess, sys, tempfile, hashlib, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
D9=ROOT/'tools'/'c11d'/'d9'
if str(D9) not in sys.path: sys.path.insert(0,str(D9))
from universal_producer import build_catalog
from shared_production_context_service import prepare_shared_production_context
from shared_production_context_gui_adapter import prepare_gui_shared_context
from shared_production_context_gui_state import (
 SharedProductionGUIStateError, audit_gui_state_contract,
 build_canonical_request_from_gui_state, prepare_gui_state_context,
 validate_gui_state,
)
STATE_SCHEMA=ROOT/'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_SCHEMA_V1.json'
CONTRACT=ROOT/'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_CONTRACT_V1.json'

def make_state(selection, request_id, content_type=None):
 ct=content_type or selection['content_type']
 overrides={'title':' TÍTULO DE PRUEBA ','subtitle':'Subtítulo común','call_to_action':'Continuar','language':'ES'}
 if ct=='challenges': overrides.update({'player_name':'ANA','challenge_label':'RETO'})
 return {
  'schema':'C11-D-SHARED-GUI-PRODUCTION-STATE-V1','schema_version':'1.0','request_id':request_id,'mode':'REVIEW',
  'selection':selection,
  'production':{'seed':12345,'music_seed':840001,'delivery_profile_id':'REVIEW_720','presentation_profile_id':'social_default_v1','variation_index':0,'audio_enabled':True,'personalization_enabled':True},
  'editorial':{'profile':{},'overrides':overrides}
 }

def representative_states():
 catalog=build_catalog(ROOT)
 challenge=catalog['content_types']['challenges']['families'][0]
 loop_family=next(f for f in catalog['content_types']['visual_loops']['families'] if f['id']=='c11c_geometric_waves_v1')
 drill=catalog['content_types']['visual_drills']['families'][0]
 loop_subtype=next(s['id'] for s in loop_family['subtypes'] if s['id']!='auto')
 return [
  make_state({'content_type':'challenges','family_id':challenge['id'],'variant_id':challenge['variants'][0]['id']},'GUI-STATE-CHALLENGE-001'),
  make_state({'content_type':'visual_loops','family_id':loop_family['id'],'subtype_id':loop_subtype},'GUI-STATE-LOOP-001'),
  make_state({'content_type':'visual_drills','family_id':drill['id'],'variant_id':drill['variants'][0]['id']},'GUI-STATE-DRILL-001'),
 ]

def run_checks():
 audit=audit_gui_state_contract(ROOT)
 assert audit['source_pins']==14 and audit['parent_source_pins']==8
 schema=json.loads(STATE_SCHEMA.read_text(encoding='utf-8'))
 import jsonschema
 jsonschema.Draft202012Validator.check_schema(schema)
 states=representative_states(); records=[]; parity=0
 for state in states:
  original=json.dumps(state,ensure_ascii=False,sort_keys=True)
  raw=build_canonical_request_from_gui_state(state,ROOT)
  assert raw['schema']=='C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1'
  assert raw['provenance']['request_origin']=='GUI'
  assert raw['selection']==state['selection']
  assert raw['seed']==state['production']['seed'] and raw['music_seed']==state['production']['music_seed']
  assert raw['production_override']==state['editorial']['overrides']
  assert json.dumps(state,ensure_ascii=False,sort_keys=True)==original
  record=prepare_gui_state_context(state,ROOT)
  direct=prepare_gui_shared_context(raw,ROOT)
  assert record==direct
  assert record==prepare_shared_production_context(raw,ROOT)
  assert record['canonical_result']['canonical_request']['request_id']==state['request_id']
  assert record['execution_boundary']['renderer_native_input_emitted'] is False
  assert record['execution_boundary']['renderer_dispatch_invoked'] is False
  assert record['execution_boundary']['media_created'] is False
  # The canonical CLI receives exactly the request produced from UI state.
  with tempfile.TemporaryDirectory(prefix='c11d_gui_state_cli_') as temp_name:
   temp=Path(temp_name); request_path=temp/'request.json'
   request_path.write_text(json.dumps(raw,ensure_ascii=False),encoding='utf-8')
   proc=subprocess.run([sys.executable,str(D9/'shared_production_context_cli.py'),'--project-root',str(ROOT),'--request',str(request_path)],cwd=ROOT,capture_output=True,timeout=120)
   assert proc.returncode==0, f'CLI exit={proc.returncode}; stderr={(proc.stderr or b'').decode("utf-8",errors="replace")!r}'
   cli=json.loads((proc.stdout or b'').decode('ascii'))
   assert cli==record
   assert sorted(p.name for p in temp.iterdir())==['request.json']
  records.append(record); parity+=1
 # Changing editorial text changes editorial/request identity, not seeds or profile id.
 changed=copy.deepcopy(states[1]); changed['editorial']['overrides']['title']='OTRO TÍTULO'
 a=prepare_gui_state_context(states[1],ROOT); b=prepare_gui_state_context(changed,ROOT)
 assert a['identity']['request_sha256']!=b['identity']['request_sha256']
 assert a['identity']['editorial_sha256']!=b['identity']['editorial_sha256']
 assert a['canonical_result']['plan']['seed']==b['canonical_result']['plan']['seed']
 assert a['canonical_result']['plan']['music_seed']==b['canonical_result']['plan']['music_seed']
 assert a['shared_context_binding']['presentation_binding']==b['shared_context_binding']['presentation_binding']
 # Fail closed: structural state faults are rejected by the mapper; catalogue/profile faults by canonical backend.
 negatives=0
 structural_bads=[]
 bad=copy.deepcopy(states[1]); bad['selection']['content_type']='longform'; structural_bads.append(bad)
 bad=copy.deepcopy(states[1]); bad['selection']['variant_id']='variant-ambiguous'; structural_bads.append(bad)
 bad=copy.deepcopy(states[1]); bad['production']['seed']=True; structural_bads.append(bad)
 bad=copy.deepcopy(states[1]); bad['editorial']['overrides']['player_name']='not for loops'; structural_bads.append(bad)
 bad=copy.deepcopy(states[1]); bad['editorial']['overrides']['title']=123; structural_bads.append(bad)
 bad=copy.deepcopy(states[1]); bad['production']['personalization_enabled']=False; structural_bads.append(bad)
 bad=copy.deepcopy(states[1]); bad['surprise']='unknown'; structural_bads.append(bad)
 bad=copy.deepcopy(states[0]); bad['editorial']['overrides']['challenge_label']=None; structural_bads.append(bad)
 bad=copy.deepcopy(states[1]); bad['selection'].pop('subtype_id'); structural_bads.append(bad)
 for bad in structural_bads:
  try: build_canonical_request_from_gui_state(bad,ROOT)
  except Exception: negatives+=1
  else: raise AssertionError('Structurally invalid GUI state must fail closed')
 bad_profile=copy.deepcopy(states[1]); bad_profile['production']['presentation_profile_id']='unregistered_future'
 try: prepare_gui_state_context(bad_profile,ROOT)
 except Exception: negatives+=1
 else: raise AssertionError('Unregistered presentation profile must fail closed in canonical backend')
 # Source drift check in a temporary mirror only, and no persistence in active repo.
 with tempfile.TemporaryDirectory(prefix='c11d_gui_state_drift_') as mirror_name:
  mirror=Path(mirror_name)
  contract=json.loads((ROOT/'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_CONTRACT_V1.json').read_text(encoding='utf-8'))
  parent_contract=json.loads((ROOT/'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_ADAPTER_CONTRACT_V1.json').read_text(encoding='utf-8'))
  # Source mirror for all pins inherited by parent contracts.
  for rel in [row['path'] for row in contract['source_lineage']]:
   src=ROOT/rel; dst=mirror/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
  for rel in [row['path'] for row in parent_contract['source_lineage']]:
   src=ROOT/rel; dst=mirror/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
  # Copy parent and new contracts required for audit.
  extras=['definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_ADAPTER_CONTRACT_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_ADAPTER_CONTRACT_SCHEMA_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_SCHEMA_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_SCHEMA_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_CONTRACT_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_CONTRACT_SCHEMA_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_SCHEMA_V1.json','tools/c11d/d9/shared_production_context_service.py','tools/c11d/d9/shared_production_context_gui_adapter.py','tools/c11d/d9/shared_production_context_gui_state.py','tools/c11d/d9/universal_producer.py','tools/c11d/d9/universal_editorial_model.py','tools/c11d/d9/editorial_render_bridge.py','tools/c11d/d9/d_render_adapter.py','tools/c11d/d9/d_renderer_shared_editorial_presentation_context_binding.py']
  for rel in extras:
   src=ROOT/rel; dst=mirror/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
  target=mirror/'tools/c11d/d9/universal_producer.py'; target.write_bytes(target.read_bytes()+b'\n# test-only drift')
  try: audit_gui_state_contract(mirror)
  except SharedProductionGUIStateError as exc: assert 'Parent GUI adapter contract failed' in str(exc) or 'Pinned GUI state source drift' in str(exc)
  else: raise AssertionError('GUI state source drift must fail closed')
 return {'source_pins':audit['source_pins'],'parent_pins':audit['parent_source_pins'],'types':3,'api_cli_parity':parity,'negative':negatives,'editorial_isolation':1,'source_drift':1}

if __name__=='__main__':
 c=run_checks()
 print('C11-D SHARED PRODUCTION GUI STATE CONTRACT PASS | source_pins=%d/%d | parent_pins=%d/%d | content_types=%d/3 | API/CLI parity=%d/3 | fail_closed_negatives=%d/10 | editorial_isolation=%d/1 | source_drift=%d/1 | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE' % (c['source_pins'],c['source_pins'],c['parent_pins'],c['parent_pins'],c['types'],c['api_cli_parity'],c['negative'],c['editorial_isolation'],c['source_drift']))
