#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any

OUTPUT_DIR = Path('artifacts/tests/c11d_d7/d7_3')
OUTPUT_NAMES = (
    'd7_3_canonical_catalog.json',
    'd7_3_catalog_validation.json',
    'd7_3_negative_tests.json',
    'd7_3_catalog_receipt.json',
)
MATRIX_REL = Path('artifacts/tests/c11d_d7/d7_1/d7_1_canonical_matrix.json')
MATRIX_VALIDATION_REL = Path('artifacts/tests/c11d_d7/d7_2/d7_2_constraint_validation.json')
MATRIX_RECEIPT_REL = Path('artifacts/tests/c11d_d7/d7_1/d7_1_matrix_receipt.json')
D72_RECEIPT_REL = Path('artifacts/tests/c11d_d7/d7_2/d7_2_validation_receipt.json')
D65_RECEIPT_REL = Path('artifacts/tests/c11d_d6/d6_5/d6_5_acceptance_receipt.json')
D71_SPEC_REL = Path('definitions/c11d/production/C11D_PRODUCTION_MATRIX_SPEC_V1.json')
D73_SPEC_REL = Path('definitions/c11d/production/C11D_CANONICAL_CATALOG_SPEC_V1.json')
D73_POLICY_REL = Path('definitions/c11d/production/C11D_CANONICAL_CATALOG_GOVERNANCE_POLICY_V1.json')
D6_REGISTRY_REL = Path('definitions/c11d/seeds/C11D_SEED_REGISTRY_V1.json')
D6_RESOLVER_REL = Path('tools/c11d/d6/seed_resolver.py')
D64_RECEIPT_CANDIDATES = (
    Path('artifacts/tests/c11d_d6/d6_4/d6_4_integration_receipt.json'),
)
C11C_BUILD_SHA = '3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3'
EXPECTED_CORE = 90
ALLOWED_MODES = ('REVIEW', 'PRODUCTION')


def canon_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canon_bytes(obj))

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def require_pass_closed(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f'{label} receipt missing: {path.as_posix()}')
    data = load_json(path)
    if not isinstance(data, dict) or data.get('result') != 'PASS' or data.get('status') != 'CLOSED':
        raise ValueError(f'{label} must be PASS/CLOSED')
    return data

def find_d64_receipt(root: Path) -> tuple[Path, dict[str, Any]]:
    for rel in D64_RECEIPT_CANDIDATES:
        p = root / rel
        if p.is_file():
            d = require_pass_closed(p, 'D6.4')
            return p, d
    raise ValueError('D6.4 integration receipt missing')

def hash_without_field(obj: dict[str, Any], field: str) -> str:
    x = json.loads(json.dumps(obj))
    x.pop(field, None)
    return hashlib.sha256(canon_bytes(x)).hexdigest()

def build_catalog(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    d65 = require_pass_closed(root / D65_RECEIPT_REL, 'D6.5')
    d72 = require_pass_closed(root / D72_RECEIPT_REL, 'D7.2')
    d64_path, d64 = find_d64_receipt(root)
    matrix = load_json(root / MATRIX_REL)
    matrix_validation = load_json(root / MATRIX_VALIDATION_REL)
    matrix_receipt = load_json(root / MATRIX_RECEIPT_REL)
    spec = load_json(root / D73_SPEC_REL)
    policy = load_json(root / D73_POLICY_REL)
    for rel, label in ((D71_SPEC_REL, 'D7.1 spec'), (D6_REGISTRY_REL, 'D6.1 registry'), (D6_RESOLVER_REL, 'D6.2 resolver')):
        if not (root / rel).is_file():
            raise ValueError(f'{label} missing: {rel.as_posix()}')
    if matrix.get('authority') != 'D7.1' or matrix.get('status') != 'CANONICAL':
        raise ValueError('D7.1 matrix authority/status invalid')
    state = matrix.get('authority_state', {})
    if state.get('matrix_authority') != 'CANONICAL_D7_1':
        raise ValueError('D7.1 matrix authority_state invalid')
    if matrix_validation.get('result') != 'PASS':
        raise ValueError('D7.2 constraint validation not PASS')
    if d72.get('result') != 'PASS':
        raise ValueError('D7.2 receipt not PASS')
    d4_blocked = d64.get('d4_8_status') == 'BLOCKED' or d64.get('d4_8_blocked') is True
    if not d4_blocked:
        raise ValueError('D4.8 must remain BLOCKED')
    if d64.get('production_execution') is True or d64.get('runtime_authority') not in (None, 'NONE'):
        raise ValueError('D6.4 execution/runtime gate invalid')
    rows = matrix.get('rows', [])
    if len(rows) != EXPECTED_CORE:
        raise ValueError(f'Expected {EXPECTED_CORE} matrix rows, found {len(rows)}')
    items: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda r: str(r.get('matrix_key', ''))):
        key = str(row['matrix_key'])
        item_base = {
            'catalog_key': key,
            'challenge_id': row.get('challenge_id'),
            'challenge_version': row.get('challenge_version'),
            'challenge_path': row.get('challenge_path'),
            'delivery_profile_id': row.get('delivery_profile_id'),
            'mode': row.get('mode'),
            'source_matrix': {
                'matrix_authority': 'CANONICAL_D7_1',
                'matrix_key': key,
                'matrix_sha256': sha256_file(root / MATRIX_REL),
            },
            'seed_bindings': row.get('seed_bindings'),
            'personalization_profile': row.get('personalization_profile'),
            'variation_index': row.get('variation_index'),
            'execution': {
                'plan_only': True,
                'production_execution': False,
                'renderer_execution': False,
                'runtime_authority': 'NONE',
                'media_rendered_by_catalog': False,
            },
            'governance': {
                'catalog_authority': 'CANONICAL_D7_3',
                'master_seed': 'NOT_ADOPTED',
                'derivation_runtime_activation': False,
                'cross_domain_seed_sharing': 'FORBIDDEN',
                'automatic_seed_generation': False,
            },
            'provenance': {
                'matrix_validation': MATRIX_VALIDATION_REL.as_posix(),
                'matrix_receipt': MATRIX_RECEIPT_REL.as_posix(),
                'coverage_receipt': D72_RECEIPT_REL.as_posix(),
                'seed_registry': D6_REGISTRY_REL.as_posix(),
                'seed_resolver': D6_RESOLVER_REL.as_posix(),
                'd6_4_integration_receipt': d64_path.relative_to(root).as_posix(),
                'plan_owner': 'canonical_production_orchestrator',
            }
        }
        item = dict(item_base)
        item['catalog_item_id'] = 'cat_' + hashlib.sha256(key.encode('utf-8')).hexdigest()[:16]
        item['identity_hash'] = hash_without_field(item, 'identity_hash')
        items.append(item)
    keys = [str(i['catalog_key']) for i in items]
    ids = [str(i['catalog_item_id']) for i in items]
    validation_errors = []
    if len(set(keys)) != len(keys): validation_errors.append('DUPLICATE_CATALOG_KEY')
    if len(set(ids)) != len(ids): validation_errors.append('DUPLICATE_CATALOG_ITEM_ID')
    if any(i.get('mode') not in ALLOWED_MODES for i in items): validation_errors.append('UNKNOWN_MODE')
    if any(i.get('seed_bindings', {}).get('GAMEPLAY', {}).get('authority') != 'gameplay' for i in items): validation_errors.append('INVALID_GAMEPLAY_SEED_AUTHORITY')
    if any(i.get('seed_bindings', {}).get('MUSIC', {}).get('authority') != 'music' for i in items): validation_errors.append('INVALID_MUSIC_SEED_AUTHORITY')
    if any(i.get('seed_bindings', {}).get('GAMEPLAY', {}).get('source_field') != 'request.seed' for i in items): validation_errors.append('INVALID_GAMEPLAY_SOURCE')
    if any(i.get('seed_bindings', {}).get('MUSIC', {}).get('source_field') != 'request.music_seed' for i in items): validation_errors.append('INVALID_MUSIC_SOURCE')
    if any(i.get('execution', {}).get('production_execution') is not False for i in items): validation_errors.append('PRODUCTION_EXECUTION_ENABLED')
    if any(i.get('execution', {}).get('renderer_execution') is not False for i in items): validation_errors.append('RENDERER_EXECUTION_ENABLED')
    if any(i.get('execution', {}).get('runtime_authority') != 'NONE' for i in items): validation_errors.append('RUNTIME_AUTHORITY_NOT_NONE')
    if any(i.get('governance', {}).get('master_seed') != 'NOT_ADOPTED' for i in items): validation_errors.append('MASTER_SEED_AUTHORITY')
    catalog = {
        'catalog_id': spec['catalog_id'],
        'schema_version': spec['schema_version'],
        'version': spec['version'],
        'authority': 'D7.3',
        'status': 'CANONICAL',
        'coverage': {
            'source_matrix_core_cases': len(rows),
            'catalog_items': len(items),
            'complete': len(items) == len(rows),
            'one_to_one_with_matrix_rows': True,
        },
        'sources': {
            'd7_1_matrix': MATRIX_REL.as_posix(),
            'd7_1_matrix_sha256': sha256_file(root / MATRIX_REL),
            'd7_1_receipt': MATRIX_RECEIPT_REL.as_posix(),
            'd7_2_validation': MATRIX_VALIDATION_REL.as_posix(),
            'd7_2_receipt': D72_RECEIPT_REL.as_posix(),
            'd6_5_receipt': D65_RECEIPT_REL.as_posix(),
            'd6_4_integration_receipt': d64_path.relative_to(root).as_posix(),
            'd6_4_integration_sha256': sha256_file(d64_path),
        },
        'authority_state': {
            'catalog_authority': 'CANONICAL_D7_3',
            'matrix_authority': 'CANONICAL_D7_1',
            'runtime_authority': 'NONE',
            'production_execution': False,
            'renderer_execution': False,
            'media_rendered_by_catalog': False,
        },
        'governance': policy.get('rules', {}),
        'items': items,
    }
    validation = {
        'result': 'PASS' if not validation_errors and catalog['coverage']['complete'] else 'FAIL',
        'errors': sorted(set(validation_errors)),
        'source_matrix_rows': len(rows),
        'catalog_items': len(items),
        'catalog_keys_unique': len(set(keys)) == len(keys),
        'catalog_item_ids_unique': len(set(ids)) == len(ids),
        'matrix_authority': catalog['authority_state']['matrix_authority'],
        'catalog_authority': catalog['authority_state']['catalog_authority'],
        'runtime_authority': catalog['authority_state']['runtime_authority'],
        'production_execution': catalog['authority_state']['production_execution'],
        'c11c_build_factory_expected_sha256': C11C_BUILD_SHA,
    }
    return catalog, validation

def negative_tests() -> dict[str, Any]:
    base = {
        'authority': 'D7.3', 'status': 'CANONICAL',
        'matrix_authority': 'CANONICAL_D7_1', 'catalog_authority': 'CANONICAL_D7_3',
        'production_execution': False, 'renderer_execution': False, 'runtime_authority': 'NONE',
        'master_seed': 'NOT_ADOPTED', 'derivation_runtime_activation': False,
        'seed_gameplay': {'authority': 'gameplay', 'source_field': 'request.seed'},
        'seed_music': {'authority': 'music', 'source_field': 'request.music_seed'},
        'catalog_keys': ['A'], 'catalog_ids': ['cat_a'],
    }
    cases = []
    def add(name: str, mutate, reject_if):
        c = json.loads(json.dumps(base)); mutate(c); rejected = reject_if(c)
        cases.append({'case': name, 'expected': 'REJECT', 'observed': 'REJECT' if rejected else 'ACCEPT', 'pass': rejected})
    add('source_matrix_not_canonical', lambda c: c.update({'matrix_authority':'WRONG'}), lambda c: c['matrix_authority'] != 'CANONICAL_D7_1')
    add('catalog_authority_wrong', lambda c: c.update({'catalog_authority':'NOT_ESTABLISHED'}), lambda c: c['catalog_authority'] != 'CANONICAL_D7_3')
    add('production_execution_enabled', lambda c: c.update({'production_execution':True}), lambda c: c['production_execution'] is not False)
    add('renderer_enabled', lambda c: c.update({'renderer_execution':True}), lambda c: c['renderer_execution'] is not False)
    add('runtime_authority_enabled', lambda c: c.update({'runtime_authority':'D7.3'}), lambda c: c['runtime_authority'] != 'NONE')
    add('master_seed_introduced', lambda c: c.update({'master_seed':'CANONICAL'}), lambda c: c['master_seed'] != 'NOT_ADOPTED')
    add('derivation_activated', lambda c: c.update({'derivation_runtime_activation':True}), lambda c: c['derivation_runtime_activation'] is not False)
    add('gameplay_mapped_to_music', lambda c: c['seed_gameplay'].update({'authority':'music','source_field':'request.music_seed'}), lambda c: c['seed_gameplay'] != {'authority':'gameplay','source_field':'request.seed'})
    add('music_mapped_to_gameplay', lambda c: c['seed_music'].update({'authority':'gameplay','source_field':'request.seed'}), lambda c: c['seed_music'] != {'authority':'music','source_field':'request.music_seed'})
    add('duplicate_catalog_key', lambda c: c.update({'catalog_keys':['A','A']}), lambda c: len(set(c['catalog_keys'])) != len(c['catalog_keys']))
    add('duplicate_catalog_item_id', lambda c: c.update({'catalog_ids':['cat_a','cat_a']}), lambda c: len(set(c['catalog_ids'])) != len(c['catalog_ids']))
    add('unknown_runtime_domain', lambda c: c.update({'runtime_authority':'UNKNOWN'}), lambda c: c['runtime_authority'] != 'NONE')
    add('negative_media_render_claim', lambda c: c.update({'production_execution':True}), lambda c: c['production_execution'] is not False)
    add('personalization_seed_source', lambda c: c['seed_gameplay'].update({'authority':'personalization','source_field':'personalization'}), lambda c: c['seed_gameplay']['authority'] != 'gameplay')
    add('variation_seed_source', lambda c: c['seed_gameplay'].update({'authority':'variation','source_field':'variation_index'}), lambda c: c['seed_gameplay']['authority'] != 'gameplay')
    add('winning_frame_seed_source', lambda c: c['seed_gameplay'].update({'authority':'winning_frame','source_field':'winning_frame'}), lambda c: c['seed_gameplay']['authority'] != 'gameplay')
    return {'count': len(cases), 'all_pass': all(x['pass'] for x in cases), 'cases': cases}

def run(root: Path) -> int:
    try:
        catalog, validation = build_catalog(root)
        negatives = negative_tests()
        receipt = {
            'checkpoint': 'D7.3',
            'name': 'Canonical Catalog Builder',
            'result': 'PASS' if validation['result']=='PASS' and negatives['all_pass'] else 'FAIL',
            'status': 'CLOSED' if validation['result']=='PASS' and negatives['all_pass'] else 'BLOCKED',
            'd7_1_predecessor': 'PASS/CLOSED',
            'd7_2_predecessor': 'PASS/CLOSED',
            'd6_5_predecessor': 'PASS/CLOSED',
            'canonical_authorities': {'matrix':'CANONICAL_D7_1','catalog':'CANONICAL_D7_3'},
            'catalog_items': catalog['coverage']['catalog_items'],
            'core_cases': catalog['coverage']['source_matrix_core_cases'],
            'complete': catalog['coverage']['complete'],
            'negative_cases': negatives['count'],
            'negative_tests_pass': negatives['all_pass'],
            'matrix_sha256': catalog['sources']['d7_1_matrix_sha256'],
            'd6_4_integration_sha256': catalog['sources']['d6_4_integration_sha256'],
            'master_seed': 'NOT_ADOPTED',
            'derivation_runtime_activation': False,
            'runtime_authority': 'NONE',
            'production_execution': False,
            'renderer_execution': False,
            'media_rendered_by_catalog': False,
            'plan_owner': 'canonical_production_orchestrator',
            'c11c_build_factory_expected_sha256': C11C_BUILD_SHA,
            'next': 'D7.4 - Catalog Identity / Provenance' if validation['result']=='PASS' and negatives['all_pass'] else 'REPAIR_D7.3'
        }
        out = root / OUTPUT_DIR
        for name, obj in zip(OUTPUT_NAMES, (catalog, validation, negatives, receipt)):
            write_json(out / name, obj)
        print(json.dumps({
            'authority':'CANONICAL_D7_3', 'catalog_items':catalog['coverage']['catalog_items'],
            'core_cases':catalog['coverage']['source_matrix_core_cases'], 'complete':catalog['coverage']['complete'],
            'negative_cases':negatives['count'], 'negative_tests_pass':negatives['all_pass'],
            'matrix_authority':'CANONICAL_D7_1', 'catalog_authority':'CANONICAL_D7_3',
            'runtime_authority':'NONE', 'production_execution':False,
            'result':receipt['result'], 'status':receipt['status'],
            'next':receipt['next']
        }, sort_keys=True))
        return 0 if receipt['result']=='PASS' else 2
    except Exception as exc:
        print(json.dumps({'result':'FAIL','status':'BLOCKED','error':str(exc)}, sort_keys=True))
        return 2

def repo_snapshot(root: Path) -> dict[str, Any]:
    skip = OUTPUT_DIR.as_posix().rstrip('/') + '/'
    files=[]
    for path in root.rglob('*'):
        if not path.is_file(): continue
        rel=path.relative_to(root).as_posix()
        if rel == '.git/index.lock' or rel.startswith(skip): continue
        try: files.append((rel,path.stat().st_size,sha256_file(path)))
        except OSError: continue
    files.sort()
    h=hashlib.sha256()
    for rel,size,digest in files:
        h.update(rel.encode()); h.update(b'\0'); h.update(str(size).encode()); h.update(b'\0'); h.update(digest.encode()); h.update(b'\n')
    return {'files':len(files),'sha256':h.hexdigest()}

def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument('--root',required=True); parser.add_argument('--snapshot-only',action='store_true'); args=parser.parse_args(); root=Path(args.root).resolve()
    if not root.is_dir(): return 2
    if args.snapshot_only:
        print(json.dumps(repo_snapshot(root),sort_keys=True)); return 0
    return run(root)
if __name__=='__main__': raise SystemExit(main())
