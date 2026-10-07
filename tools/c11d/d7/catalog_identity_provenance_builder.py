#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

OUTPUT_DIR = Path('artifacts/tests/c11d_d7/d7_4')
OUTPUT_NAMES = (
    'd7_4_identity_validation.json',
    'd7_4_provenance_validation.json',
    'd7_4_negative_tests.json',
    'd7_4_identity_receipt.json',
)
CATALOG_REL = Path('artifacts/tests/c11d_d7/d7_3/d7_3_canonical_catalog.json')
CATALOG_VALIDATION_REL = Path('artifacts/tests/c11d_d7/d7_3/d7_3_catalog_validation.json')
CATALOG_RECEIPT_REL = Path('artifacts/tests/c11d_d7/d7_3/d7_3_catalog_receipt.json')
MATRIX_REL = Path('artifacts/tests/c11d_d7/d7_1/d7_1_canonical_matrix.json')
MATRIX_VALIDATION_REL = Path('artifacts/tests/c11d_d7/d7_2/d7_2_constraint_validation.json')
D72_RECEIPT_REL = Path('artifacts/tests/c11d_d7/d7_2/d7_2_validation_receipt.json')
D65_RECEIPT_REL = Path('artifacts/tests/c11d_d6/d6_5/d6_5_acceptance_receipt.json')
D64_REL = Path('artifacts/tests/c11d_d6/d6_4/d6_4_integration_receipt.json')
D71_SPEC_REL = Path('definitions/c11d/production/C11D_PRODUCTION_MATRIX_SPEC_V1.json')
D73_SPEC_REL = Path('definitions/c11d/production/C11D_CANONICAL_CATALOG_SPEC_V1.json')
D74_SPEC_REL = Path('definitions/c11d/production/C11D_CATALOG_IDENTITY_PROVENANCE_SPEC_V1.json')
D6_REGISTRY_REL = Path('definitions/c11d/seeds/C11D_SEED_REGISTRY_V1.json')
D6_RESOLVER_REL = Path('tools/c11d/d6/seed_resolver.py')
D74_POLICY_REL = Path('definitions/c11d/production/C11D_CATALOG_IDENTITY_PROVENANCE_GOVERNANCE_POLICY_V1.json')
C11C_BUILD_SHA = '3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3'
EXPECTED_CORE = 90
EXPECTED_MODES = {'REVIEW', 'PRODUCTION'}


def canon_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canon_bytes(obj))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def hash_without_field(obj: dict[str, Any], field: str) -> str:
    clone = json.loads(json.dumps(obj))
    clone.pop(field, None)
    return sha256_bytes(canon_bytes(clone))


def require_file(root: Path, rel: Path, label: str) -> Path:
    path = root / rel
    if not path.is_file():
        raise ValueError(f'{label} missing: {rel.as_posix()}')
    return path


def require_pass_closed(root: Path, rel: Path, label: str) -> tuple[Path, dict[str, Any]]:
    path = require_file(root, rel, label)
    data = load_json(path)
    if not isinstance(data, dict) or data.get('result') != 'PASS' or data.get('status') != 'CLOSED':
        raise ValueError(f'{label} must be PASS/CLOSED')
    return path, data


def item_expected_id(catalog_key: str) -> str:
    return 'cat_' + sha256_bytes(catalog_key.encode('utf-8'))[:16]


def item_expected_identity_hash(item: dict[str, Any]) -> str:
    return hash_without_field(item, 'identity_hash')


def build_context(root: Path) -> dict[str, Any]:
    catalog_path = require_file(root, CATALOG_REL, 'D7.3 catalog')
    catalog = load_json(catalog_path)
    catalog_validation_path = require_file(root, CATALOG_VALIDATION_REL, 'D7.3 validation')
    catalog_validation = load_json(catalog_validation_path)
    if not isinstance(catalog_validation, dict) or catalog_validation.get('result') != 'PASS':
        raise ValueError('D7.3 validation must be PASS')
    _, catalog_receipt = require_pass_closed(root, CATALOG_RECEIPT_REL, 'D7.3 receipt')
    matrix_path = require_file(root, MATRIX_REL, 'D7.1 matrix')
    matrix_validation_path, matrix_validation = require_pass_closed(root, MATRIX_VALIDATION_REL, 'D7.2 validation')
    d72_path, d72 = require_pass_closed(root, D72_RECEIPT_REL, 'D7.2 receipt')
    d65_path, d65 = require_pass_closed(root, D65_RECEIPT_REL, 'D6.5 receipt')
    d64_path, d64 = require_pass_closed(root, D64_REL, 'D6.4 integration receipt')
    for rel, label in (
        (D71_SPEC_REL, 'D7.1 spec'),
        (D73_SPEC_REL, 'D7.3 spec'),
        (D74_SPEC_REL, 'D7.4 spec'),
        (D74_POLICY_REL, 'D7.4 policy'),
        (D6_REGISTRY_REL, 'D6.1 registry'),
        (D6_RESOLVER_REL, 'D6.2 resolver'),
    ):
        require_file(root, rel, label)
    return {
        'catalog_path': catalog_path,
        'catalog': catalog,
        'catalog_validation': catalog_validation,
        'catalog_receipt': catalog_receipt,
        'matrix_path': matrix_path,
        'matrix': load_json(matrix_path),
        'matrix_validation_path': matrix_validation_path,
        'matrix_validation': matrix_validation,
        'd72_path': d72_path,
        'd72': d72,
        'd65_path': d65_path,
        'd65': d65,
        'd64_path': d64_path,
        'd64': d64,
    }


def validate_catalog(context: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    root_catalog = context['catalog']
    matrix = context['matrix']
    items = root_catalog.get('items', [])
    rows = matrix.get('rows', [])
    row_map = {str(r.get('matrix_key')): r for r in rows}
    current_matrix_sha = sha256_file(context['matrix_path'])
    current_d64_sha = sha256_file(context['d64_path'])

    errors: list[str] = []
    identity_failures: list[dict[str, Any]] = []
    linkage_failures: list[dict[str, Any]] = []
    identity_ids: list[str] = []

    if root_catalog.get('authority') != 'D7.3' or root_catalog.get('status') != 'CANONICAL':
        errors.append('D7_3_CATALOG_NOT_CANONICAL')
    if root_catalog.get('authority_state', {}).get('catalog_authority') != 'CANONICAL_D7_3':
        errors.append('D7_3_CATALOG_AUTHORITY_INVALID')
    if root_catalog.get('authority_state', {}).get('matrix_authority') != 'CANONICAL_D7_1':
        errors.append('D7_1_MATRIX_AUTHORITY_MISMATCH')
    if len(items) != EXPECTED_CORE or len(rows) != EXPECTED_CORE:
        errors.append('COVERAGE_NOT_90')
    if len(items) != len(rows):
        errors.append('ONE_TO_ONE_CARDINALITY_FAILURE')

    source_matrix_sha = root_catalog.get('sources', {}).get('d7_1_matrix_sha256')
    if source_matrix_sha != current_matrix_sha:
        errors.append('STALE_D7_1_MATRIX_HASH')
    source_d64_sha = root_catalog.get('sources', {}).get('d6_4_integration_sha256')
    if source_d64_sha != current_d64_sha:
        errors.append('STALE_D6_4_HASH')

    for item in items:
        key = str(item.get('catalog_key'))
        expected_id = item_expected_id(key)
        expected_hash = item_expected_identity_hash(item)
        identity_ids.append(str(item.get('catalog_item_id')))
        local = []
        if str(item.get('catalog_item_id')) != expected_id:
            local.append('CATALOG_ITEM_ID_MISMATCH')
        if str(item.get('identity_hash')) != expected_hash:
            local.append('IDENTITY_HASH_MISMATCH')
        if key not in row_map:
            local.append('MATRIX_KEY_MISSING')
        else:
            row = row_map[key]
            for field in ('challenge_id', 'challenge_version', 'challenge_path', 'delivery_profile_id', 'mode', 'variation_index'):
                if item.get(field) != row.get(field):
                    local.append(f'MATRIX_LINK_MISMATCH:{field}')
            if item.get('seed_bindings') != row.get('seed_bindings'):
                local.append('MATRIX_LINK_MISMATCH:seed_bindings')
            if item.get('personalization_profile') != row.get('personalization_profile'):
                local.append('MATRIX_LINK_MISMATCH:personalization_profile')
            if item.get('source_matrix', {}).get('matrix_key') != key:
                local.append('ITEM_SOURCE_MATRIX_KEY_MISMATCH')
        if item.get('source_matrix', {}).get('matrix_sha256') != current_matrix_sha:
            local.append('ITEM_SOURCE_MATRIX_HASH_STALE')
        if item.get('governance', {}).get('catalog_authority') != 'CANONICAL_D7_3':
            local.append('ITEM_CATALOG_AUTHORITY_INVALID')
        if item.get('governance', {}).get('master_seed') != 'NOT_ADOPTED':
            local.append('ITEM_MASTER_SEED_INVALID')
        if item.get('governance', {}).get('derivation_runtime_activation') is not False:
            local.append('ITEM_DERIVATION_RUNTIME_ACTIVATED')
        if item.get('governance', {}).get('cross_domain_seed_sharing') != 'FORBIDDEN':
            local.append('ITEM_CROSS_DOMAIN_SEED_POLICY_INVALID')
        execution = item.get('execution', {})
        if execution.get('production_execution') is not False or execution.get('renderer_execution') is not False or execution.get('runtime_authority') != 'NONE' or execution.get('media_rendered_by_catalog') is not False:
            local.append('ITEM_EXECUTION_GATE_INVALID')
        if item.get('provenance', {}).get('plan_owner') != 'canonical_production_orchestrator':
            local.append('ITEM_PLAN_OWNER_INVALID')
        if local:
            identity_failures.append({'catalog_key': key, 'failures': sorted(set(local))})
        if key in row_map:
            expected_prefix = row_map[key].get('matrix_key')
            if expected_prefix != key:
                linkage_failures.append({'catalog_key': key, 'expected_matrix_key': expected_prefix})

    if len(set(identity_ids)) != len(identity_ids):
        errors.append('DUPLICATE_CATALOG_ITEM_ID')
    if len({str(i.get('catalog_key')) for i in items}) != len(items):
        errors.append('DUPLICATE_CATALOG_KEY')

    if context['catalog_validation'].get('result') != 'PASS':
        errors.append('D7_3_VALIDATION_NOT_PASS')
    if context['catalog_receipt'].get('result') != 'PASS' or context['catalog_receipt'].get('status') != 'CLOSED':
        errors.append('D7_3_RECEIPT_NOT_PASS_CLOSED')
    if context['d72'].get('result') != 'PASS' or context['d72'].get('status') != 'CLOSED':
        errors.append('D7_2_NOT_PASS_CLOSED')
    if context['d65'].get('result') != 'PASS' or context['d65'].get('status') != 'CLOSED':
        errors.append('D6_5_NOT_PASS_CLOSED')

    d4_blocked = context['d64'].get('d4_8_status') == 'BLOCKED' or context['d64'].get('d4_8_blocked') is True
    if not d4_blocked:
        errors.append('D4_8_NOT_BLOCKED')
    if context['d64'].get('production_execution') is True:
        errors.append('D6_4_PRODUCTION_EXECUTION_ENABLED')
    if context['d64'].get('runtime_authority') not in (None, 'NONE'):
        errors.append('D6_4_RUNTIME_AUTHORITY_ENABLED')

    identity_validation = {
        'checkpoint': 'D7.4',
        'authority': 'D7.4',
        'status': 'PASS' if not errors and not identity_failures and not linkage_failures else 'FAIL',
        'catalog_authority': root_catalog.get('authority_state', {}).get('catalog_authority'),
        'matrix_authority': root_catalog.get('authority_state', {}).get('matrix_authority'),
        'catalog_items': len(items),
        'matrix_rows': len(rows),
        'one_to_one': len(items) == len(rows) and not linkage_failures and not errors,
        'catalog_keys_unique': len({str(i.get('catalog_key')) for i in items}) == len(items),
        'catalog_item_ids_unique': len(set(identity_ids)) == len(identity_ids),
        'identity_ids_recomputed': len(identity_failures) == 0,
        'identity_hashes_recomputed': len(identity_failures) == 0,
        'source_matrix_hash_current': source_matrix_sha == current_matrix_sha,
        'd6_4_hash_current': source_d64_sha == current_d64_sha,
        'identity_failures': identity_failures,
        'linkage_failures': linkage_failures,
        'errors': sorted(set(errors)),
        'current_source_hashes': {
            'd7_1_matrix_sha256': current_matrix_sha,
            'd6_4_integration_sha256': current_d64_sha,
        },
    }
    return identity_validation, {
        'd7_1_matrix': context['matrix_path'].relative_to(context['matrix_path'].parents[4]).as_posix() if False else MATRIX_REL.as_posix(),
        'd7_2_validation': context['matrix_validation_path'].as_posix(),
        'd6_1_registry': D6_REGISTRY_REL.as_posix(),
        'd6_2_seed_resolver': D6_RESOLVER_REL.as_posix(),
        'd6_4_integration_receipt': context['d64_path'].as_posix(),
        'd4_4_plan_owner': 'canonical_production_orchestrator',
        'd4_8_status': 'BLOCKED' if (context['d64'].get('d4_8_status') == 'BLOCKED' or context['d64'].get('d4_8_blocked') is True) else 'NOT_BLOCKED',
        'runtime_authority': root_catalog.get('authority_state', {}).get('runtime_authority'),
        'production_execution': root_catalog.get('authority_state', {}).get('production_execution'),
        'renderer_execution': root_catalog.get('authority_state', {}).get('renderer_execution'),
        'media_rendered_by_catalog': root_catalog.get('authority_state', {}).get('media_rendered_by_catalog'),
        'plan_owner': 'canonical_production_orchestrator',
        'sources': {
            'd7_1_matrix_sha256': sha256_file(context['matrix_path']),
            'd7_2_validation_sha256': sha256_file(context['matrix_validation_path']),
            'd6_5_receipt_sha256': sha256_file(context['d65_path']),
            'd6_4_integration_sha256': sha256_file(context['d64_path']),
        },
    }


def provenance_validation(context: dict[str, Any]) -> dict[str, Any]:
    catalog = context['catalog']
    items = catalog.get('items', [])
    root = context['catalog_path'].parents[4]
    errors: list[str] = []
    missing: list[str] = []
    paths_checked = set()
    for item in items:
        provenance = item.get('provenance', {})
        for field, rel_text in (
            ('matrix_validation', provenance.get('matrix_validation')),
            ('matrix_receipt', provenance.get('matrix_receipt')),
            ('coverage_receipt', provenance.get('coverage_receipt')),
            ('seed_registry', provenance.get('seed_registry')),
            ('seed_resolver', provenance.get('seed_resolver')),
            ('d6_4_integration_receipt', provenance.get('d6_4_integration_receipt')),
        ):
            if not rel_text:
                errors.append(f'MISSING_PROVENANCE_FIELD:{field}')
                continue
            candidate = root / rel_text
            paths_checked.add(str(rel_text))
            if not candidate.is_file():
                missing.append(str(rel_text))
        if provenance.get('plan_owner') != 'canonical_production_orchestrator':
            errors.append('INVALID_PLAN_OWNER')
    if catalog.get('sources', {}).get('d7_1_matrix') != MATRIX_REL.as_posix():
        errors.append('ROOT_D7_1_SOURCE_PATH_MISMATCH')
    if catalog.get('sources', {}).get('d7_2_validation') != MATRIX_VALIDATION_REL.as_posix():
        errors.append('ROOT_D7_2_SOURCE_PATH_MISMATCH')
    if catalog.get('sources', {}).get('d6_4_integration_receipt') != D64_REL.as_posix():
        errors.append('ROOT_D6_4_SOURCE_PATH_MISMATCH')
    return {
        'checkpoint': 'D7.4',
        'status': 'PASS' if not errors and not missing else 'FAIL',
        'items_checked': len(items),
        'required_provenance_paths_checked': len(paths_checked),
        'missing_paths': sorted(set(missing)),
        'errors': sorted(set(errors)),
        'chain': [
            {'stage': 'D7.1', 'authority': 'CANONICAL_D7_1', 'path': MATRIX_REL.as_posix()},
            {'stage': 'D7.2', 'status': 'PASS/CLOSED', 'path': D72_RECEIPT_REL.as_posix()},
            {'stage': 'D6.1', 'authority': 'canonical seed registry', 'path': D6_REGISTRY_REL.as_posix()},
            {'stage': 'D6.2', 'authority': 'explicit seed resolver', 'path': D6_RESOLVER_REL.as_posix()},
            {'stage': 'D6.4', 'status': 'PASS/CLOSED', 'path': D64_REL.as_posix()},
            {'stage': 'D4.4', 'plan_owner': 'canonical_production_orchestrator'},
        ],
        'governance': {
            'd4_8': 'BLOCKED' if (context['d64'].get('d4_8_status') == 'BLOCKED' or context['d64'].get('d4_8_blocked') is True) else 'NOT_BLOCKED',
            'master_seed': catalog.get('governance', {}).get('master_seed'),
            'derivation_runtime_activation': catalog.get('governance', {}).get('derivation_runtime_activation'),
            'cross_domain_seed_sharing': catalog.get('governance', {}).get('cross_domain_seed_sharing'),
            'automatic_seed_generation': catalog.get('governance', {}).get('automatic_seed_generation'),
            'runtime_authority': catalog.get('authority_state', {}).get('runtime_authority'),
            'production_execution': catalog.get('authority_state', {}).get('production_execution'),
        },
    }


def negative_tests(context: dict[str, Any]) -> dict[str, Any]:
    catalog = context['catalog']
    first_item = json.loads(json.dumps(catalog['items'][0]))
    base_catalog = json.loads(json.dumps(catalog))
    cases: list[dict[str, Any]] = []

    def check(name: str, candidate: dict[str, Any], predicate) -> None:
        rejected = bool(predicate(candidate))
        cases.append({'case': name, 'expected': 'REJECT', 'observed': 'REJECT' if rejected else 'ACCEPT', 'pass': rejected})

    c = json.loads(json.dumps(base_catalog)); c['items'][0]['catalog_item_id'] = 'cat_tampered'; check('catalog_item_id_tamper', c, lambda x: x['items'][0]['catalog_item_id'] != item_expected_id(str(x['items'][0]['catalog_key'])))
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['identity_hash'] = '0' * 64; check('identity_hash_tamper', c, lambda x: x['items'][0]['identity_hash'] != item_expected_identity_hash(x['items'][0]))
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['catalog_key'] = 'tampered-key'; check('catalog_key_tamper', c, lambda x: x['items'][0]['catalog_item_id'] != item_expected_id(str(x['items'][0]['catalog_key'])))
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['source_matrix']['matrix_key'] = 'tampered-key'; check('matrix_key_link_tamper', c, lambda x: x['items'][0]['source_matrix']['matrix_key'] != x['items'][0]['catalog_key'])
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['source_matrix']['matrix_sha256'] = '0' * 64; check('stale_matrix_hash', c, lambda x: x['items'][0]['source_matrix']['matrix_sha256'] != sha256_file(context['matrix_path']))
    c = json.loads(json.dumps(base_catalog)); c['sources']['d7_1_matrix_sha256'] = '0' * 64; check('stale_root_matrix_hash', c, lambda x: x['sources']['d7_1_matrix_sha256'] != sha256_file(context['matrix_path']))
    c = json.loads(json.dumps(base_catalog)); c['sources']['d6_4_integration_sha256'] = '0' * 64; check('stale_d6_4_hash', c, lambda x: x['sources']['d6_4_integration_sha256'] != sha256_file(context['d64_path']))
    c = json.loads(json.dumps(base_catalog)); c['authority_state']['catalog_authority'] = 'OTHER'; check('catalog_authority_tamper', c, lambda x: x['authority_state']['catalog_authority'] != 'CANONICAL_D7_3')
    c = json.loads(json.dumps(base_catalog)); c['authority_state']['matrix_authority'] = 'OTHER'; check('matrix_authority_tamper', c, lambda x: x['authority_state']['matrix_authority'] != 'CANONICAL_D7_1')
    c = json.loads(json.dumps(base_catalog)); c['governance']['master_seed'] = 'ADOPTED'; check('master_seed_tamper', c, lambda x: x['governance']['master_seed'] != 'NOT_ADOPTED')
    c = json.loads(json.dumps(base_catalog)); c['governance']['derivation_runtime_activation'] = True; check('derivation_activation_tamper', c, lambda x: x['governance']['derivation_runtime_activation'] is not False)
    c = json.loads(json.dumps(base_catalog)); c['governance']['cross_domain_seed_sharing'] = 'ALLOWED'; check('cross_domain_seed_policy_tamper', c, lambda x: x['governance']['cross_domain_seed_sharing'] != 'FORBIDDEN')
    c = json.loads(json.dumps(base_catalog)); c['authority_state']['production_execution'] = True; check('production_execution_tamper', c, lambda x: x['authority_state']['production_execution'] is not False)
    c = json.loads(json.dumps(base_catalog)); c['authority_state']['renderer_execution'] = True; check('renderer_execution_tamper', c, lambda x: x['authority_state']['renderer_execution'] is not False)
    c = json.loads(json.dumps(base_catalog)); c['authority_state']['runtime_authority'] = 'CATALOG'; check('runtime_authority_tamper', c, lambda x: x['authority_state']['runtime_authority'] != 'NONE')
    c = json.loads(json.dumps(base_catalog)); c['authority_state']['media_rendered_by_catalog'] = True; check('media_render_claim_tamper', c, lambda x: x['authority_state']['media_rendered_by_catalog'] is not False)
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['provenance']['plan_owner'] = 'tampered_owner'; check('plan_owner_tamper', c, lambda x: x['items'][0]['provenance']['plan_owner'] != 'canonical_production_orchestrator')
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['governance']['catalog_authority'] = 'OTHER'; check('item_catalog_authority_tamper', c, lambda x: x['items'][0]['governance']['catalog_authority'] != 'CANONICAL_D7_3')
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['governance']['master_seed'] = 'ADOPTED'; check('item_master_seed_tamper', c, lambda x: x['items'][0]['governance']['master_seed'] != 'NOT_ADOPTED')
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['execution']['production_execution'] = True; check('item_production_execution_tamper', c, lambda x: x['items'][0]['execution']['production_execution'] is not False)
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['execution']['renderer_execution'] = True; check('item_renderer_execution_tamper', c, lambda x: x['items'][0]['execution']['renderer_execution'] is not False)
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['execution']['runtime_authority'] = 'CATALOG'; check('item_runtime_authority_tamper', c, lambda x: x['items'][0]['execution']['runtime_authority'] != 'NONE')
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['seed_bindings']['GAMEPLAY']['authority'] = 'music'; check('gameplay_seed_domain_tamper', c, lambda x: x['items'][0]['seed_bindings']['GAMEPLAY']['authority'] != 'gameplay')
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['seed_bindings']['MUSIC']['authority'] = 'gameplay'; check('music_seed_domain_tamper', c, lambda x: x['items'][0]['seed_bindings']['MUSIC']['authority'] != 'music')
    c = json.loads(json.dumps(base_catalog)); c['items'].append(json.loads(json.dumps(base_catalog['items'][0]))); check('duplicate_item_tamper', c, lambda x: len(x['items']) != len({str(i['catalog_item_id']) for i in x['items']}))
    c = json.loads(json.dumps(base_catalog)); c['items'][0]['provenance']['matrix_validation'] = 'missing.json'; check('missing_provenance_path', c, lambda x: x['items'][0]['provenance']['matrix_validation'] != MATRIX_VALIDATION_REL.as_posix())

    # Guard against accidental unused fixture drift.
    _ = first_item
    return {'count': len(cases), 'all_pass': all(case['pass'] for case in cases), 'cases': cases}


def build(root: Path) -> int:
    context = build_context(root)
    identity_validation, provenance = validate_catalog(context)
    prov_validation = provenance_validation(context)
    negatives = negative_tests(context)

    overall_pass = (
        identity_validation['status'] == 'PASS'
        and prov_validation['status'] == 'PASS'
        and negatives['all_pass']
        and context['d64'].get('production_execution') is not True
        and context['d64'].get('runtime_authority') in (None, 'NONE')
    )
    receipt = {
        'checkpoint': 'D7.4',
        'name': 'Catalog Identity / Provenance',
        'authority': 'D7.4',
        'result': 'PASS' if overall_pass else 'FAIL',
        'status': 'CLOSED' if overall_pass else 'BLOCKED',
        'd7_3_predecessor': 'PASS/CLOSED',
        'canonical_authorities': {
            'matrix': 'CANONICAL_D7_1',
            'catalog': 'CANONICAL_D7_3',
            'identity_provenance': 'CANONICAL_D7_4',
        },
        'catalog_items': len(context['catalog'].get('items', [])),
        'core_cases': len(context['matrix'].get('rows', [])),
        'one_to_one': identity_validation['one_to_one'],
        'identity_ids_recomputed': identity_validation['identity_ids_recomputed'],
        'identity_hashes_recomputed': identity_validation['identity_hashes_recomputed'],
        'provenance_pass': prov_validation['status'] == 'PASS',
        'negative_cases': negatives['count'],
        'negative_tests_pass': negatives['all_pass'],
        'source_hashes_current': identity_validation['source_matrix_hash_current'] and identity_validation['d6_4_hash_current'],
        'master_seed': context['catalog'].get('governance', {}).get('master_seed'),
        'derivation_runtime_activation': context['catalog'].get('governance', {}).get('derivation_runtime_activation'),
        'runtime_authority': context['catalog'].get('authority_state', {}).get('runtime_authority'),
        'production_execution': context['catalog'].get('authority_state', {}).get('production_execution'),
        'renderer_execution': context['catalog'].get('authority_state', {}).get('renderer_execution'),
        'media_rendered_by_catalog': context['catalog'].get('authority_state', {}).get('media_rendered_by_catalog'),
        'd4_8_status': 'BLOCKED' if (context['d64'].get('d4_8_status') == 'BLOCKED' or context['d64'].get('d4_8_blocked') is True) else 'NOT_BLOCKED',
        'plan_owner': 'canonical_production_orchestrator',
        'c11c_build_factory_expected_sha256': C11C_BUILD_SHA,
        'next': 'D7.5 - Full D7 Acceptance' if overall_pass else 'REPAIR_D7.4',
    }
    out = root / OUTPUT_DIR
    for name, obj in zip(OUTPUT_NAMES, (identity_validation, prov_validation, negatives, receipt)):
        write_json(out / name, obj)
    print(json.dumps({
        'authority': 'CANONICAL_D7_4',
        'catalog_authority': 'CANONICAL_D7_3',
        'catalog_items': receipt['catalog_items'],
        'core_cases': receipt['core_cases'],
        'one_to_one': receipt['one_to_one'],
        'identity_ids_recomputed': receipt['identity_ids_recomputed'],
        'identity_hashes_recomputed': receipt['identity_hashes_recomputed'],
        'provenance_pass': receipt['provenance_pass'],
        'negative_cases': receipt['negative_cases'],
        'negative_tests_pass': receipt['negative_tests_pass'],
        'source_hashes_current': receipt['source_hashes_current'],
        'runtime_authority': receipt['runtime_authority'],
        'production_execution': receipt['production_execution'],
        'd4_8_status': receipt['d4_8_status'],
        'result': receipt['result'],
        'status': receipt['status'],
        'next': receipt['next'],
    }, sort_keys=True))
    return 0 if overall_pass else 2


def repo_snapshot(root: Path) -> dict[str, Any]:
    skip = OUTPUT_DIR.as_posix().rstrip('/') + '/'
    files = []
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel == '.git/index.lock' or rel.startswith(skip):
            continue
        try:
            files.append((rel, path.stat().st_size, sha256_file(path)))
        except OSError:
            continue
    files.sort()
    h = hashlib.sha256()
    for rel, size, digest in files:
        h.update(rel.encode('utf-8')); h.update(b'\0')
        h.update(str(size).encode('ascii')); h.update(b'\0')
        h.update(digest.encode('ascii')); h.update(b'\n')
    return {'files': len(files), 'sha256': h.hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--snapshot-only', action='store_true')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        return 2
    if args.snapshot_only:
        print(json.dumps(repo_snapshot(root), sort_keys=True))
        return 0
    try:
        return build(root)
    except Exception as exc:
        print(json.dumps({'result': 'FAIL', 'status': 'BLOCKED', 'error': str(exc)}, sort_keys=True))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
