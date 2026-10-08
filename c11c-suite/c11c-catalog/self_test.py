from __future__ import annotations
import hashlib, json, tempfile
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from c11d_catalog import build_catalog_data

def put_json(root, rel, data):
    p=root/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); return p

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def fixture(root):
    item={"catalog_key":"CHALLENGE_001|REVIEW_720|REVIEW","catalog_item_id":"cat_0123456789abcdef","challenge_id":"CHALLENGE_001","challenge_version":"1.0","delivery_profile_id":"REVIEW_720","mode":"REVIEW","seed_bindings":{"GAMEPLAY":{"authority":"gameplay","source_field":"request.seed"},"MUSIC":{"authority":"music","source_field":"request.music_seed"}},"personalization_profile":"none_v1","identity_hash":"a"*64,"provenance":{"matrix_validation":"artifacts/tests/c11d_d7/d7_2/d7_2_constraint_validation.json"}}
    put_json(root,'artifacts/tests/c11d_d7/d7_3/d7_3_canonical_catalog.json',{"authority":"D7.3","status":"CANONICAL","authority_state":{"runtime_authority":"NONE","production_execution":False,"renderer_execution":False},"items":[item]*0})
    # A canonical 90-row fixture with unique identities.
    items=[]
    for i in range(90):
        x=dict(item); x.update(catalog_key=f"MATRIX-{i:03d}",catalog_item_id=f"cat_{i:016x}",identity_hash=f"{i:064x}"); items.append(x)
    put_json(root,'artifacts/tests/c11d_d7/d7_3/d7_3_canonical_catalog.json',{"authority":"D7.3","status":"CANONICAL","authority_state":{"runtime_authority":"NONE","production_execution":False,"renderer_execution":False},"items":items})
    put_json(root,'artifacts/tests/c11d_d7/d7_3/d7_3_catalog_validation.json',{"result":"PASS"})
    put_json(root,'artifacts/tests/c11d_d7/d7_3/d7_3_catalog_receipt.json',{"result":"PASS","status":"CLOSED","release_authority":"NONE"})
    put_json(root,'artifacts/tests/c11d_d7/d7_4/d7_4_identity_receipt.json',{"result":"PASS","status":"CLOSED","release_authority":"NONE"})

    put_json(root,'artifacts/tests/c11d_d8/d8_7/d8_7_receipt.json',{"checkpoint":"D8.7","result":"PASS_NO_MEDIA","status":"CLOSED","d8_control_plane":"ACCEPTED","scope_candidate_count":0,"release_authority":"NONE"})
    put_json(root,'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json',{"contract":"C11-D-D8-MEDIA-SCOPE-V1","scope_mode":"EXPLICIT_REGISTRY_ONLY","registry":[],"candidate_count":0,"release_authority":"NONE","production_execution":False,"renderer_execution":False,"runtime_authority":"NONE"})
    media=root/'artifacts/tests/c11d_d9/d9_2/pilot_media/CHALLENGE_001_seed_12345_AV.mp4'; media.parent.mkdir(parents=True,exist_ok=True); media.write_bytes(b'fixture-media-not-a-real-video')
    media_row={"name":"D9.2_AV","path":media.relative_to(root).as_posix(),"sha256":sha(media),"bytes":media.stat().st_size}
    rows=[media_row]
    other_names=["D9.1_VIDEO","D9.3_REPEAT_A","D9.3_REPEAT_B","D9.3_NEGATIVE"]
    for i,n in enumerate(other_names):
        p=root/f'artifacts/tests/c11d_d9/fixture/{n}.mp4'; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes((n+'-media').encode())
        rows.append({"name":n,"path":p.relative_to(root).as_posix(),"sha256":sha(p),"bytes":p.stat().st_size})
    put_json(root,'artifacts/tests/c11d_d9/d9_4/evidence/d9_4_acceptance_manifest.json',{"checkpoint":"D9.4","result":"PASS","d9_status":"ACTIVE","release_authority":"NONE","production_execution":False,"renderer_execution":False,"media":rows})
    put_json(root,'artifacts/tests/c11d_d9/d9_4/evidence/d9_4_receipt.json',{"checkpoint":"D9.4","result":"PASS","status":"CLOSED","release_authority":"NONE"})
    put_json(root,'artifacts/tests/c11d_d9/d9_1/evidence/d9_1_receipt.json',{"checkpoint":"D9.1","result":"PASS","status":"PILOT_COMPLETE","challenge_id":"CHALLENGE_001","seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1","release_authority":"NONE"})
    put_json(root,'artifacts/tests/c11d_d9/d9_2/evidence/d9_2_receipt.json',{"checkpoint":"D9.2","result":"PASS","status":"PILOT_COMPLETE","challenge_id":"CHALLENGE_001","seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1","audio_codec":"aac","audio_sample_rate_hz":48000,"audio_channels":2,"release_authority":"NONE"})
    put_json(root,'artifacts/tests/c11d_d9/d9_3/evidence/d9_3_receipt.json',{"checkpoint":"D9.3","result":"PASS","status":"PILOT_REPEAT_COMPLETE","challenge_id":"CHALLENGE_001","seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1","release_authority":"NONE"})

    reqid='C11D-GUI-TEST-001'; folder=Path('artifacts/tests/c11d_d9/producer_gui')/reqid
    request={"request_id":reqid,"challenge_id":"CHALLENGE_001","challenge_version":"1.0","mode":"REVIEW","seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1"}
    plan={"mode":"REVIEW","challenge_id":"CHALLENGE_001","seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1","runtime_authority":"NONE","renderer_activation":False,"gui_activation":False,"orchestrator_execution":False,"simulation_truth_mutation":False,"winning_frame_mutation":False,"close_calls_mutation":False,"gameplay_rng_consumption":False,"structural_rng_consumption":False}
    parity={"status":"PASS","gui_plan_hash":"b"*64,"cli_plan_hash":"b"*64,"gui_request_hash":"c"*64}
    receipt={"schema":"C11-D-D9.5.1-PRODUCER-GUI-RECEIPT-V1","phase":"D9.5.1","result":"PASS_PLAN_ONLY","status":"PLANNED","request_id":reqid,"request_hash":"c"*64,"personalization_hash":"d"*64,"plan_hash":"b"*64,"gui_cli_parity":"PASS","renderer_execution":False,"production_execution":False,"release_authority":"NONE","d4_8":"BLOCKED"}
    personalization={"profile_id":"editorial_text_v1","values":{"title":"Test title"}}
    for name, data in (("request.json",request),("canonical_request.json",request),("resolved_personalization.json",personalization),("production_plan.json",plan),("gui_cli_parity.json",parity),("producer_gui_receipt.json",receipt)):
        put_json(root,folder/name,data)
    return rows, root / folder

def run_checks():
    with tempfile.TemporaryDirectory(prefix='c11d_d96_catalog_') as td:
        root=Path(td)
        rows, plan_folder=fixture(root)
        # Unregistered media under artifacts is not promoted into product records.
        rogue=root/'artifacts/tests/unregistered/looks_like_product.mp4'; rogue.parent.mkdir(parents=True); rogue.write_bytes(b'not registered')
        result=build_catalog_data(root)
        assert result['summary']['canonical_intents']==90, result['summary']
        assert result['summary']['pilot_media']==5, result['summary']
        assert result['summary']['producer_plans']==1, result['summary']
        assert result['summary']['release_products']==0
        plan=next(x for x in result['records'] if x['record_type']=='PRODUCER_PLAN')
        assert plan['status']=='PLAN_ONLY' and plan['release_authority']=='NONE'
        canonical=next(x for x in result['records'] if x['record_type']=='CANONICAL_INTENT')
        assert canonical['identity_hash'] and canonical['plan_hash'] is None
        assert plan['reproduction_command'] and 'production_cli.py' in plan['reproduction_command']
        media=next(x for x in result['records'] if x['record_type']=='PILOT_MEDIA' and x['record_id']=='D9.2_AV')
        assert media['media_eligibility']=='NOT_REGISTERED_FOR_D8_RELEASE'
        assert media['media_sha256']==sha(root/media['media_path'])
        assert all(x['record_id']!='looks_like_product.mp4' for x in result['records'])
        # D8 scope must stay empty; a non-empty registry blocks pilot media promotion.
        scope_path=root/'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json'
        scope=json.loads(scope_path.read_text(encoding='utf-8')); scope['candidate_count']=1; scope['registry']=[{'path':'old.mp4'}]; scope_path.write_text(json.dumps(scope),encoding='utf-8')
        blocked_scope=build_catalog_data(root)
        assert not any(x['record_type']=='PILOT_MEDIA' for x in blocked_scope['records'])
        assert any(i['code']=='MEDIA_SCOPE_NOT_EMPTY' for i in blocked_scope['issues'])
        scope['candidate_count']=0; scope['registry']=[]; scope_path.write_text(json.dumps(scope),encoding='utf-8')
        # A tampered explicit media hash must be rejected, never silently admitted.
        manifest_path=root/'artifacts/tests/c11d_d9/d9_4/evidence/d9_4_acceptance_manifest.json'
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        manifest['media'][0]['sha256']='0'*64
        manifest_path.write_text(json.dumps(manifest),encoding='utf-8')
        tampered=build_catalog_data(root)
        assert any(i['code']=='MEDIA_HASH_OR_SIZE_MISMATCH' for i in tampered['issues']), tampered['issues']
        assert not any(x['record_type']=='PILOT_MEDIA' and x['record_id']=='D9.2_AV' for x in tampered['records'])
        # Unsafe traversal paths are rejected.
        manifest['media'][0]['path']='../../outside.mp4'; manifest['media'][0]['sha256']='0'*64
        manifest_path.write_text(json.dumps(manifest),encoding='utf-8')
        traversal=build_catalog_data(root)
        assert any(i['code']=='MEDIA_PATH_MISSING_OR_OUTSIDE_ROOT' for i in traversal['issues'])
        # Invalid/partially written Producer records are not promoted.
        bad=plan_folder/'gui_cli_parity.json'; payload=json.loads(bad.read_text()); payload['status']='FAIL'; bad.write_text(json.dumps(payload),encoding='utf-8')
        invalid=build_catalog_data(root)
        assert not any(x['record_type']=='PRODUCER_PLAN' for x in invalid['records'])
        assert any(i['code']=='PLAN_RECORD_INVALID' for i in invalid['issues'])
    return {"canonical_intents":90,"pilot_media":5,"producer_plans":1,"negative_controls":5}

if __name__=='__main__':
    counts=run_checks()
    print('C11-D D9.6 Catalog integration PASS | intents={canonical_intents}/90 | pilot_media={pilot_media}/5 | producer_plans={producer_plans}/1 | negative_controls={negative_controls}/5'.format(**counts))
