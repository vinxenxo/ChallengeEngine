from __future__ import annotations
import copy, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D9 = ROOT / 'tools' / 'c11d' / 'd9'
if str(D9) not in sys.path:
    sys.path.insert(0, str(D9))

from universal_producer import build_catalog, REQUEST_SCHEMA_ID
from shared_production_context_service import prepare_shared_production_context, SharedProductionContextError
from shared_production_context_gui_adapter import (
    SharedProductionContextGUIAdapterError,
    audit_gui_adapter,
    prepare_gui_shared_context,
    validate_gui_shared_context,
)

CONTRACT_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_ADAPTER_CONTRACT_V1.json')

def make_request(selection: dict, request_id: str) -> dict:
    return {
        'schema': REQUEST_SCHEMA_ID, 'schema_version': '1.0', 'request_id': request_id,
        'mode': 'REVIEW', 'selection': selection, 'seed': 12345, 'music_seed': 840001,
        'delivery_profile_id': 'REVIEW_720', 'presentation_profile_id': 'social_default_v1',
        'variation_index': 0, 'audio_enabled': True, 'personalization_enabled': True,
        'editorial_profile': {},
        'production_override': {
            'title': ' TÍTULO DE PRUEBA ', 'subtitle': 'Subtítulo compartido',
            'call_to_action': 'Continuar', 'language': ' ES ',
            **({'player_name':'ANA','challenge_label':'RETO'} if selection.get('content_type') == 'challenges' else {}),
        },
        'provenance': {'source_revision':'D9_SHARED_GUI_ADAPTER_TEST','request_origin':'GUI'},
    }

def representative_requests():
    catalog = build_catalog(ROOT)
    challenge = catalog['content_types']['challenges']['families'][0]
    loop_family = next(f for f in catalog['content_types']['visual_loops']['families'] if f['id'] == 'c11c_geometric_waves_v1')
    drill = catalog['content_types']['visual_drills']['families'][0]
    loop_subtype = next(s['id'] for s in loop_family['subtypes'] if s['id'] != 'auto')
    return [
        make_request({'content_type':'challenges','family_id':challenge['id'],'variant_id':challenge['variants'][0]['id']}, 'GUI-CTX-CHALLENGE-001'),
        make_request({'content_type':'visual_loops','family_id':loop_family['id'],'subtype_id':loop_subtype}, 'GUI-CTX-LOOP-001'),
        make_request({'content_type':'visual_drills','family_id':drill['id'],'variant_id':drill['variants'][0]['id']}, 'GUI-CTX-DRILL-001'),
    ]

def run_checks():
    audit = audit_gui_adapter(ROOT)
    assert audit == {'source_pins':8,'parent_source_pins':22,'supported_content_types':3,'existing_gui_source_modified_by_overlay':False,'renderer':False,'media_created':False,'release_authority':'NONE'}
    contract = json.loads((ROOT/CONTRACT_REL).read_text(encoding='utf-8'))
    assert contract['integration_boundary']['existing_gui_source_modified_by_overlay'] is False
    assert contract['integration_boundary']['adapter_connected_to_current_gui'] is False
    # The active GUI sources are pinned by this D-owned overlay; the release manifest remains authoritative for the original C11-C source hash.
    manifest = json.loads((ROOT/'release/C11C_FREEZE_PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    manifest_by_path = {x['path']:x for x in manifest['source_files']}
    for path in ('c11c-suite/c11c-producer/main.py','c11c-suite/c11c-producer/c11d_gui_request.py'):
        entry = manifest_by_path[path]
        active_hash = hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        assert active_hash == next(row['sha256'] for row in contract['source_lineage'] if row['path'] == path)
        assert entry['sha256'] == ('b975d1d9158c113c89a7ed8a91245cb0d6a553531b0df2b3c36869730f572c49' if path.endswith('main.py') else active_hash)
        if path.endswith('c11d_gui_request.py'):
            assert active_hash == entry['sha256']
    requests = representative_requests()
    parity = 0
    for req in requests:
        before = json.dumps(req, ensure_ascii=False, sort_keys=True)
        gui_record = prepare_gui_shared_context(req, ROOT)
        assert validate_gui_shared_context(gui_record, req, ROOT)
        assert prepare_shared_production_context(req, ROOT) == gui_record
        assert json.dumps(req, ensure_ascii=False, sort_keys=True) == before
        assert req['provenance']['request_origin'] == 'GUI'
        assert gui_record['canonical_result']['canonical_request']['request_id'] == req['request_id']
        assert gui_record['execution_boundary']['renderer_native_input_emitted'] is False
        assert gui_record['execution_boundary']['renderer_dispatch_invoked'] is False
        assert gui_record['execution_boundary']['media_created'] is False
        with tempfile.TemporaryDirectory(prefix='c11d_gui_context_parity_') as temp_name:
            temp = Path(temp_name)
            input_path = temp/'gui-request.json'
            input_path.write_text(json.dumps(req, ensure_ascii=False), encoding='utf-8')
            proc = subprocess.run([
                sys.executable, str(D9/'shared_production_context_cli.py'),
                '--project-root', str(ROOT), '--request', str(input_path),
            ], cwd=ROOT, capture_output=True, timeout=120)
            assert proc.returncode == 0, f'CLI failed: code={proc.returncode}; stderr={(proc.stderr or b"").decode("utf-8",errors="replace")!r}'
            cli_record = json.loads((proc.stdout or b'').decode('ascii'))
            assert cli_record == gui_record
            assert sorted(p.name for p in temp.iterdir()) == ['gui-request.json']
        parity += 1
    # Fail closed for origin mismatch, missing provenance and unregistered profile.
    negatives = 0
    for mutate in (
        lambda r: r['provenance'].update(request_origin='CLI'),
        lambda r: r.pop('provenance'),
        lambda r: r.update(presentation_profile_id='unregistered_future_profile'),
        lambda r: r['selection'].update(content_type='longform'),
    ):
        bad = copy.deepcopy(requests[1]); mutate(bad)
        try:
            prepare_gui_shared_context(bad, ROOT)
        except Exception:
            negatives += 1
        else:
            raise AssertionError('Invalid GUI request should fail closed')
    tampered = copy.deepcopy(prepare_gui_shared_context(requests[0], ROOT))
    tampered['canonical_result']['plan']['selection']['family_id'] = 'FAKE'
    try:
        validate_gui_shared_context(tampered, requests[0], ROOT)
    except SharedProductionContextGUIAdapterError:
        negatives += 1
    else:
        raise AssertionError('Tampered GUI record must reject')
    # Adapter must remain a thin delegator, not duplicate D9.8/D9.9/D9.10 resolution.
    adapter_text = (D9/'shared_production_context_gui_adapter.py').read_text(encoding='utf-8')
    for forbidden in ('evaluate_universal_request(', 'build_bridge_planning_record(', 'prepare_d_only_adapter_envelope('):
        assert forbidden not in adapter_text, f'GUI adapter duplicates canonical resolution: {forbidden}'
    assert 'prepare_shared_production_context(raw_request, root)' in adapter_text
    assert 'subprocess' not in adapter_text and '.write_text(' not in adapter_text
    # Parent facade source drift checks are inherited; local GUI lineage drift must also fail closed.
    with tempfile.TemporaryDirectory(prefix='c11d_gui_adapter_drift_') as temp_name:
        mirror = Path(temp_name)
        parent_contract = json.loads((ROOT/'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_V1.json').read_text(encoding='utf-8'))
        for row in parent_contract['source_lineage']:
            src = ROOT/row['path']; dst = mirror/row['path']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        for rel in ('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_SCHEMA_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_SCHEMA_V1.json',
                    'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_ADAPTER_CONTRACT_V1.json','definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_ADAPTER_CONTRACT_SCHEMA_V1.json',
                    'tools/c11d/d9/shared_production_context_gui_adapter.py'):
            src=ROOT/rel; dst=mirror/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        for row in contract['source_lineage']:
            src=ROOT/row['path']; dst=mirror/row['path']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        target=mirror/'c11c-suite/c11c-producer/c11d_gui_request.py'; target.write_bytes(target.read_bytes()+b'\n# test-only drift')
        try: audit_gui_adapter(mirror)
        except SharedProductionContextGUIAdapterError as exc: assert 'Pinned GUI source drift' in str(exc)
        else: raise AssertionError('GUI source drift must fail closed')
    assert negatives == 5
    return {'source_pins':audit['source_pins'],'parent_pins':audit['parent_source_pins'],'content_types':3,'api_cli_parity':parity,'negatives':negatives,'frozen_gui_pins':2,'source_drift':1}

if __name__ == '__main__':
    c=run_checks()
    print('C11-D SHARED PRODUCTION CONTEXT GUI ADAPTER CONTRACT PASS | '
          f"gui_source_pins={c['source_pins']}/{c['source_pins']} | parent_source_pins={c['parent_pins']}/{c['parent_pins']} | "
          f"content_types={c['content_types']}/3 | gui_api_cli_parity={c['api_cli_parity']}/3 | "
          f"fail_closed_negatives={c['negatives']}/5 | active_gui_source_pins={c['frozen_gui_pins']}/2 | original_manifest_main_hash=1/1 | gui_helper_manifest_match=1/1 | source_drift_negative={c['source_drift']}/1 | "
          'existing_gui_source_modified_by_overlay=false | future_gui_adapter=READY | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE')
