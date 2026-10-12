from __future__ import annotations
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from shared_production_context_gui_catalog import (
    SharedProductionGUICatalogError, audit_dynamic_gui_catalog,
    build_dynamic_gui_catalog, get_family_options, get_selector_options,
    resolve_gui_catalog_selection, _sha_value,
)
from universal_editorial_model import build_catalog

CONTRACT=ROOT/'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_CATALOG_CONTRACT_V1.json'
CATALOG_SCHEMA=ROOT/'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_CATALOG_SCHEMA_V1.json'
SELECTION_SCHEMA=ROOT/'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_SELECTION_SCHEMA_V1.json'


def run_checks():
    audit=audit_dynamic_gui_catalog(ROOT)
    assert audit['source_pins']==8 and audit['active_type_contract_parity']==3 and audit['longform_present_disabled'] is True
    contract=json.loads(CONTRACT.read_text(encoding='utf-8'))
    assert hashlib.sha256((ROOT/'tools/c11d/d9/shared_production_context_gui_catalog.py').read_bytes()).hexdigest()==contract['implementation_sha256']
    import jsonschema
    for schema_path in (CATALOG_SCHEMA, SELECTION_SCHEMA):
        jsonschema.Draft202012Validator.check_schema(json.loads(schema_path.read_text(encoding='utf-8')))
    snapshot=build_dynamic_gui_catalog(ROOT)
    jsonschema.Draft202012Validator(json.loads(CATALOG_SCHEMA.read_text(encoding='utf-8'))).validate(snapshot)
    raw=build_catalog(ROOT)
    assert [row['id'] for row in snapshot['content_types']]==list(raw['content_types'].keys())
    types={row['id']:row for row in snapshot['content_types']}
    assert set(('challenges','visual_loops','visual_drills','longform')).issubset(types)
    assert types['challenges']['allowed_modes']==['REVIEW','PRODUCTION']
    assert types['visual_loops']['allowed_modes']==['REVIEW'] and types['visual_loops']['request_plan_compatible'] is False
    assert types['visual_drills']['allowed_modes']==['REVIEW'] and types['visual_drills']['request_plan_compatible'] is False
    assert types['longform']['selection_enabled'] is False and types['longform']['families']==[]
    # Dynamic inventory follows canonical build_catalog; no family IDs are duplicated in GUI code.
    for content_type, raw_info in raw['content_types'].items():
        row=types[content_type]
        assert row['family_count']==len(raw_info.get('families',[]))
        for fam_raw, fam_row in zip(raw_info.get('families',[]),row['families']):
            key='subtypes' if content_type=='visual_loops' else 'variants'
            assert [s['id'] for s in fam_row['selectors']]==[s['id'] for s in fam_raw.get(key,[])]
    total_families=sum(len(i.get('families',[])) for i in raw['content_types'].values())
    total_selectors=sum(len(f.get('subtypes',f.get('variants',[]))) for i in raw['content_types'].values() for f in i.get('families',[]))
    assert snapshot['inventory_summary']['family_count']==total_families
    assert snapshot['inventory_summary']['selector_count']==total_selectors
    # Modes and selectors are validated by the source resolver; REVIEW permits model-only types but not production mode.
    challenge_family=raw['content_types']['challenges']['families'][0]
    challenge_selector=challenge_family['variants'][0]['id']
    chall=resolve_gui_catalog_selection('challenges',challenge_family['id'],challenge_selector,'PRODUCTION',ROOT)
    assert chall['selection']['variant_id']==challenge_selector and chall['request_plan_compatible'] is True
    loop_family=next(f for f in raw['content_types']['visual_loops']['families'] if f.get('subtypes'))
    loop_selector=next(s['id'] for s in loop_family['subtypes'] if s['id']!='auto')
    loop=resolve_gui_catalog_selection('visual_loops',loop_family['id'],loop_selector,'REVIEW',ROOT)
    assert loop['selection']['subtype_id']==loop_selector and loop['exact_concrete_grammar'] is True
    assert loop['renderer_input_emitted'] is False and loop['media_created'] is False and loop['release_authority']=='NONE'
    loop_identity=dict(loop); loop_digest=loop_identity.pop('identity_sha256'); assert _sha_value(loop_identity)==loop_digest
    auto_rows=[s for s in get_selector_options('visual_loops',loop_family['id'],'REVIEW',ROOT) if s['id']=='auto']
    assert auto_rows and auto_rows[0]['selection_mode'] is True and auto_rows[0]['concrete_variant'] is False
    drill_family=raw['content_types']['visual_drills']['families'][0]
    drill_selector=drill_family['variants'][0]['id']
    drill=resolve_gui_catalog_selection('visual_drills',drill_family['id'],drill_selector,'REVIEW',ROOT)
    assert drill['selection']['variant_id']==drill_selector and drill['request_plan_compatible'] is False
    # Reject disabled mode, longform, unknown IDs, and type/family/selector cross-wiring.
    negatives=0
    attempts=[
        lambda: get_family_options('visual_loops','PRODUCTION',ROOT),
        lambda: get_family_options('longform','REVIEW',ROOT),
        lambda: get_family_options('future_type','REVIEW',ROOT),
        lambda: get_selector_options('visual_loops','not_a_family','REVIEW',ROOT),
        lambda: resolve_gui_catalog_selection('visual_loops',loop_family['id'],'not_a_grammar','REVIEW',ROOT),
        lambda: resolve_gui_catalog_selection('challenges',challenge_family['id'],'tier-1','REVIEW',ROOT),
        lambda: resolve_gui_catalog_selection('visual_drills',drill_family['id'],drill_selector,'PRODUCTION',ROOT),
    ]
    for operation in attempts:
        try: operation()
        except SharedProductionGUICatalogError: negatives+=1
        else: raise AssertionError('Unknown or incompatible GUI selector must fail closed')
    assert negatives==7
    # CLI and API catalog projections must match exactly and remain ASCII-safe JSON.
    cli=subprocess.run([sys.executable,'-B',str(HERE/'shared_production_context_gui_catalog.py'),'--catalog','--project-root',str(ROOT)],cwd=ROOT,capture_output=True,timeout=60)
    assert cli.returncode==0, f'CLI catalog failed {cli.returncode}: {(cli.stderr or b"").decode("utf-8",errors="replace")}'
    cli_catalog=json.loads(cli.stdout.decode('ascii'))
    assert cli_catalog==snapshot
    audit_cli=subprocess.run([sys.executable,'-B',str(HERE/'shared_production_context_gui_catalog.py'),'--audit-only','--project-root',str(ROOT)],cwd=ROOT,capture_output=True,timeout=60)
    assert audit_cli.returncode==0
    assert json.loads(audit_cli.stdout.decode('ascii'))['audit']==audit
    # Default root discovery must work from the repository root without --project-root.
    default_cli=subprocess.run([sys.executable,'-B',str(HERE/'shared_production_context_gui_catalog.py'),'--audit-only'],cwd=ROOT,capture_output=True,timeout=60)
    assert default_cli.returncode==0, f'default-root CLI failed {default_cli.returncode}: {(default_cli.stderr or b"").decode("utf-8",errors="replace")}'
    assert json.loads(default_cli.stdout.decode('ascii'))['audit']==audit
    default_families=subprocess.run([sys.executable,'-B',str(HERE/'shared_production_context_gui_catalog.py'),'--families-for','visual_loops','--mode','REVIEW'],cwd=ROOT,capture_output=True,timeout=60)
    assert default_families.returncode==0 and len(json.loads(default_families.stdout.decode('ascii'))['families'])==len(raw['content_types']['visual_loops']['families'])
    # No report or artifacts are persisted by the API or CLI.
    assert not (ROOT/'shared_production_context_gui_catalog_report.json').exists()
    assert not (ROOT/'artifacts/tests/c11d_d9/gui_dynamic_catalog').exists()
    # Source drift fails closed in a disposable mirror with the canonical inputs needed to rebuild catalog.
    with tempfile.TemporaryDirectory(prefix='c11d_gui_catalog_drift_') as temp_name:
        mirror=Path(temp_name)
        src_contract=json.loads(CONTRACT.read_text(encoding='utf-8'))
        all_paths={r['path'] for r in src_contract['source_lineage']}
        all_paths|={
            'definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json',
            'c11c-suite/c11c-producer/producer_schema.json',
            'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_CATALOG_CONTRACT_V1.json',
            'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_CATALOG_CONTRACT_SCHEMA_V1.json',
            'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_CATALOG_SCHEMA_V1.json',
            'definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_SELECTION_SCHEMA_V1.json',
            'tools/c11d/d9/shared_production_context_gui_catalog.py',
        }
        for rel in all_paths:
            src=ROOT/rel; dst=mirror/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        drift=mirror/'c11c-suite/c11c-producer/producer_schema.json'
        drift.write_bytes(drift.read_bytes()+b'\n# test-only source drift\n')
        try: audit_dynamic_gui_catalog(mirror)
        except SharedProductionGUICatalogError as exc: assert 'Pinned source drift' in str(exc)
        else: raise AssertionError('Pinned producer schema drift must fail closed')
    return {'source_pins':audit['source_pins'],'types':len(snapshot['content_types']),'active_types':audit['active_type_contract_parity'],'families':total_families,'selectors':total_selectors,'negative':negatives,'cli_api_parity':1,'source_drift':1}

if __name__=='__main__':
    c=run_checks()
    print('C11-D SHARED PRODUCTION GUI DYNAMIC CATALOG PASS | source_pins=%d/8 | active_types=%d/3 | content_types=%d | families=%d | selectors=%d | fail_closed_negatives=%d/7 | CLI/API parity=PASS | source_drift=%d/1 | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE' % (c['source_pins'],c['active_types'],c['types'],c['families'],c['selectors'],c['negative'],c['source_drift']))
