from __future__ import annotations
import copy, hashlib, json, subprocess, sys, tempfile, shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from shared_production_context_gui_catalog import build_dynamic_gui_catalog
from shared_production_context_gui_reactive_selection import (
 SharedProductionGUIReactiveSelectionError, audit_reactive_selection_contract,
 initialize_gui_reactive_selection_state, transition_gui_reactive_selection_state,
)

def step(snapshot, event):
 return transition_gui_reactive_selection_state(snapshot['state'],event,ROOT)

def cli_transition(snapshot,event):
 cmd=[sys.executable,'-B',str(HERE/'shared_production_context_gui_reactive_selection.py'),
      '--transition','--state-json',json.dumps(snapshot['state'],ensure_ascii=True,separators=(',',':')),
      '--event-json',json.dumps(event,ensure_ascii=True,separators=(',',':'))]
 proc=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=120)
 assert proc.returncode==0, f'CLI transition failed exit={proc.returncode}; stderr={(proc.stderr or b"").decode("utf-8",errors="replace")}'
 return json.loads(proc.stdout.decode('ascii'))

def assert_snapshot_hash(snapshot):
 unhashed=copy.deepcopy(snapshot)
 expected=unhashed['identity'].pop('snapshot_sha256')
 actual=hashlib.sha256(json.dumps(unhashed,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')).hexdigest()
 assert actual==expected, 'Snapshot self-hash must verify exactly'

def run_checks():
 audit=audit_reactive_selection_contract(ROOT)
 assert audit['source_pins']==9 and audit['parent_catalog_source_pins']==8 and audit['parent_state_source_pins']==14
 cat=build_dynamic_gui_catalog(ROOT)
 # Initialize empty: no invented default family/subtype.
 current=initialize_gui_reactive_selection_state('REVIEW',ROOT)
 assert current['state']['selection']=={'content_type':None,'family_id':None,'selector_field':None,'selector_id':None}
 assert current['readiness']['selection_path_complete'] is False
 assert len(current['available']['content_types'])==4
 # Content-type selection invalidates descendants rather than auto-selecting a family.
 current=step(current,{'action':'select_content_type','content_type':'challenges'})
 assert current['state']['selection']['content_type']=='challenges'
 assert current['state']['selection']['family_id'] is None and current['state']['selection']['selector_id'] is None
 assert current['available']['families'] and current['available']['selectors']==[]
 # Family selection must clear selector; no default selection.
 challenge_family=current['available']['families'][0]['id']
 current=step(current,{'action':'select_family','family_id':challenge_family})
 assert current['state']['selection']['family_id']==challenge_family
 assert current['state']['selection']['selector_id'] is None and current['available']['selectors']
 challenge_selector=current['available']['selectors'][0]['id']
 current=step(current,{'action':'select_selector','selector_id':challenge_selector})
 assert current['readiness']['selection_path_complete'] and current['readiness']['canonical_selection_resolved']
 assert current['readiness']['canonical_selection']['content_type']=='challenges'
 # API/CLI exact parity for the three cascading selector levels.
 initial=initialize_gui_reactive_selection_state('REVIEW',ROOT)
 assert_snapshot_hash(initial)
 parity_state=initial; parity=0
 parity_events=[
  {'action':'select_content_type','content_type':'challenges'},
  {'action':'select_family','family_id':challenge_family},
  {'action':'select_selector','selector_id':challenge_selector},
 ]
 for event in parity_events:
  api_next=step(parity_state,event)
  cli_next=cli_transition(parity_state,event)
  assert cli_next==api_next, f'API/CLI transition differs for {event["action"]}'
  assert_snapshot_hash(api_next)
  parity_state=api_next; parity+=1
 assert parity_state==current
 # Switch content type clears family/selector and never picks a replacement.
 loop_type=step(current,{'action':'select_content_type','content_type':'visual_loops'})
 assert loop_type['state']['selection']['family_id'] is None and loop_type['state']['selection']['selector_id'] is None
 loop_family=next(f for f in loop_type['available']['families'] if f['id']=='c11c_geometric_waves_v1')
 loop_type=step(loop_type,{'action':'select_family','family_id':loop_family['id']})
 assert loop_type['state']['selection']['selector_id'] is None
 loop_selector=next(s for s in loop_type['available']['selectors'] if s['id']!='auto')
 loop_type=step(loop_type,{'action':'select_selector','selector_id':loop_selector['id']})
 assert loop_type['readiness']['canonical_selection_resolved'] and loop_type['readiness']['exact_concrete_selector'] is True
 # Mode switch to production preserves a compatible challenge selection, but clears model-only descendants.
 production=step(current,{'action':'set_mode','mode':'PRODUCTION'})
 assert production['state']['mode']=='PRODUCTION' and production['readiness']['canonical_selection_resolved']
 loop_block=step(loop_type,{'action':'set_mode','mode':'PRODUCTION'})
 assert loop_block['state']['selection']['content_type']=='visual_loops'
 assert loop_block['state']['selection']['family_id'] is None and loop_block['state']['selection']['selector_id'] is None
 assert 'CONTENT_TYPE_NOT_ALLOWED_IN_MODE' in loop_block['readiness']['blockers']
 assert loop_block['transition']['invalidated_fields']
 # Mode-incompatible new content type and unknown family/selector fail closed.
 neg=0
 checks=[
  lambda: step(initial,{'action':'select_content_type','content_type':'longform'}),
  lambda: step(initial,{'action':'select_content_type','content_type':'future_type'}),
  lambda: step(production,{'action':'select_content_type','content_type':'visual_drills'}),
  lambda: step(initial,{'action':'select_family','family_id':'unknown'}),
  lambda: step(loop_type,{'action':'select_selector','selector_id':'unknown'}),
  lambda: step(initial,{'action':'choose_first_family','family_id':'x'}),
  lambda: step(initial,{'action':'set_mode','mode':'PROD'}),
  lambda: step(initial,{'action':'select_content_type','content_type':'challenges','extra':True}),
  lambda: step(initial,{'action':'select_content_type','content_type':'challenges','mode':'REVIEW'}),
  lambda: transition_gui_reactive_selection_state({**initial['state'],'unknown':1},{'action':'clear_selection'},ROOT),
 ]
 for op in checks:
  try: op()
  except (SharedProductionGUIReactiveSelectionError,TypeError): neg+=1
  else: raise AssertionError('Invalid UI selection transition must fail closed')
 assert neg==10
 # Explicit mode switch rejects a new unavailable type; input state remains byte-identical.
 old=json.dumps(loop_type['state'],sort_keys=True)
 try: step(loop_block,{'action':'select_content_type','content_type':'visual_loops'})
 except SharedProductionGUIReactiveSelectionError: pass
 else: raise AssertionError('Cannot select model-only content in production mode')
 assert json.dumps(loop_type['state'],sort_keys=True)==old
 # Clear is explicit and no persistence occurs.
 cleared=step(current,{'action':'clear_selection'})
 assert cleared['state']['selection']['content_type'] is None
 assert all(v is None for v in cleared['state']['selection'].values())
 assert cleared['execution_boundary']=={'request_created':False,'renderer_input_emitted':False,'renderer_dispatch_invoked':False,'media_created':False,'persisted':False,'release_authority':'NONE'}
 # Refresh action accepts stale identity only explicitly, then reports any invalidated descendants.
 stale=copy.deepcopy(initial['state']); stale['catalog_sha256']='0'*64
 refreshed=transition_gui_reactive_selection_state(stale,{'action':'refresh_catalog'},ROOT)
 assert refreshed['transition']['catalog_refreshed'] is True
 try: transition_gui_reactive_selection_state(stale,{'action':'clear_selection'},ROOT)
 except SharedProductionGUIReactiveSelectionError as exc: assert 'Stale GUI selection state' in str(exc)
 else: raise AssertionError('Stale catalog identity must reject ordinary transitions')
 # Hash binding and deterministic snapshot.
 again=initialize_gui_reactive_selection_state('REVIEW',ROOT)
 assert again['identity']['snapshot_sha256']==initial['identity']['snapshot_sha256']
 assert_snapshot_hash(again)
 assert current['identity']['catalog_sha256']==cat['identity']['catalog_sha256']
 # API/CLI init parity and audit are machine-readable ASCII JSON.
 proc=subprocess.run([sys.executable,'-B',str(HERE/'shared_production_context_gui_reactive_selection.py'),'--initialize','--mode','REVIEW'],cwd=ROOT,capture_output=True,timeout=120)
 assert proc.returncode==0, (proc.stderr or b'').decode('utf-8',errors='replace')
 cli_init=json.loads(proc.stdout.decode('ascii'))
 assert cli_init==again
 # No artifacts are persisted.
 assert not (ROOT/'shared_production_context_gui_reactive_selection_report.json').exists()
 # Source drift in an isolated full copy fails closed; no active source bytes touched.
 with tempfile.TemporaryDirectory(prefix='c11d_reactive_gui_drift_') as name:
  mirror=Path(name)/'repo'; shutil.copytree(ROOT,mirror,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  drift=mirror/'tools/c11d/d9/shared_production_context_gui_catalog.py'
  drift.write_bytes(drift.read_bytes()+b'\n# test-only drift\n')
  try: audit_reactive_selection_contract(mirror)
  except SharedProductionGUIReactiveSelectionError as exc: assert 'Pinned source drift' in str(exc) or 'Parent catalog/state contract failed' in str(exc)
  else: raise AssertionError('Catalog source drift must fail closed')
 return {'source_pins':audit['source_pins'],'catalog_parent_pins':audit['parent_catalog_source_pins'],'state_parent_pins':audit['parent_state_source_pins'],'content_types':len(cat['content_types']),'api_cli_parity':parity,'negative':neg,'refresh':1,'source_drift':1}

if __name__=='__main__':
 c=run_checks()
 print('C11-D SHARED PRODUCTION GUI REACTIVE SELECTION PASS | source_pins=%d/9 | parent_catalog=%d/8 | parent_gui_state=%d/14 | content_types=%d | API/CLI parity=%d/3 | fail_closed_negatives=%d/10 | explicit_refresh=%d/1 | source_drift=%d/1 | request_created=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE' % (c['source_pins'],c['catalog_parent_pins'],c['state_parent_pins'],c['content_types'],c['api_cli_parity'],c['negative'],c['refresh'],c['source_drift']))
