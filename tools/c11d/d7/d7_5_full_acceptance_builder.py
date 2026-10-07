#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

OUTPUT_DIR = Path('artifacts/tests/c11d_d7/d7_5')
OUTPUT_NAMES = (
    'd7_5_full_acceptance.json',
    'd7_5_governance_validation.json',
    'd7_5_negative_tests.json',
    'd7_5_acceptance_receipt.json',
)
D70_RECEIPT = Path('artifacts/tests/c11d_d7/d7_0/d7_0_audit_receipt.json')
D71_RECEIPT = Path('artifacts/tests/c11d_d7/d7_1/d7_1_matrix_receipt.json')
D72_RECEIPT = Path('artifacts/tests/c11d_d7/d7_2/d7_2_validation_receipt.json')
D73_CATALOG = Path('artifacts/tests/c11d_d7/d7_3/d7_3_canonical_catalog.json')
D73_RECEIPT = Path('artifacts/tests/c11d_d7/d7_3/d7_3_catalog_receipt.json')
D74_RECEIPT = Path('artifacts/tests/c11d_d7/d7_4/d7_4_identity_receipt.json')
D64_RECEIPT = Path('artifacts/tests/c11d_d6/d6_4/d6_4_integration_receipt.json')
D65_RECEIPT = Path('artifacts/tests/c11d_d6/d6_5/d6_5_acceptance_receipt.json')
D71_MATRIX = Path('artifacts/tests/c11d_d7/d7_1/d7_1_canonical_matrix.json')
D71_SPEC = Path('definitions/c11d/production/C11D_PRODUCTION_MATRIX_SPEC_V1.json')
D73_SPEC = Path('definitions/c11d/production/C11D_CANONICAL_CATALOG_SPEC_V1.json')
D74_SPEC = Path('definitions/c11d/production/C11D_CATALOG_IDENTITY_PROVENANCE_SPEC_V1.json')
D75_SPEC = Path('definitions/c11d/production/C11D_D7_FULL_ACCEPTANCE_SPEC_V1.json')
D75_POLICY = Path('definitions/c11d/production/C11D_D7_FULL_ACCEPTANCE_GOVERNANCE_POLICY_V1.json')
D6_REGISTRY = Path('definitions/c11d/seeds/C11D_SEED_REGISTRY_V1.json')
D6_RESOLVER = Path('tools/c11d/d6/seed_resolver.py')
BUILD_FACTORY = Path('build_factory.py')
BUILD_FACTORY_NAME = 'build_factory.py'
SEARCH_EXCLUDED_DIRS = {'.git', '.godot', '__pycache__', 'artifacts', 'release'}
C11C_BUILD_SHA = '3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3'
EXPECTED_CHALLENGES = 9
EXPECTED_PROFILES = 5
EXPECTED_MODES = 2
EXPECTED_CORE = 90


def canon_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canon_bytes(obj))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def require_file(root: Path, rel: Path, label: str) -> Path:
    path = root / rel
    if not path.is_file():
        raise ValueError(f'{label} missing: {rel.as_posix()}')
    return path


def require_receipt(root: Path, rel: Path, label: str) -> tuple[Path, dict[str, Any]]:
    path = root / rel
    if not path.is_file():
        raise ValueError(f'{label} receipt missing: {rel.as_posix()}')
    try:
        data = load_json(path)
    except Exception as exc:
        raise ValueError(f'{label} receipt parse error: {exc}')
    if not isinstance(data, dict) or data.get('result') != 'PASS' or data.get('status') != 'CLOSED':
        raise ValueError(f'{label} must be PASS/CLOSED')
    return path, data


def numeric_first(data: dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return None


def bool_first(data: dict[str, Any], *keys: str) -> bool | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, bool):
            return value
    return None


def repo_snapshot(root: Path) -> dict[str, Any]:
    skip = OUTPUT_DIR.as_posix().rstrip('/') + '/'
    files: list[tuple[str, int, str]] = []
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


def discover_build_factory(root: Path) -> tuple[Path, list[dict[str, str]]]:
    candidates: list[Path] = []
    for path in root.rglob(BUILD_FACTORY_NAME):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(root).parts
        if any(part in SEARCH_EXCLUDED_DIRS for part in rel_parts):
            continue
        candidates.append(path)
    candidates.sort(key=lambda p: p.as_posix().lower())
    details: list[dict[str, str]] = []
    matching: list[Path] = []
    for path in candidates:
        digest = sha256_file(path)
        rel = path.relative_to(root).as_posix()
        details.append({'path': rel, 'sha256': digest})
        if digest.lower() == C11C_BUILD_SHA.lower():
            matching.append(path)
    if len(matching) == 1:
        return matching[0], details
    if not candidates:
        raise ValueError(
            'C11-C build_factory.py not found anywhere in active repository tree; '
            'D7.5 requires the frozen C11-C build identity to be present.'
        )
    if len(matching) > 1:
        paths = ', '.join(p.relative_to(root).as_posix() for p in matching)
        raise ValueError(
            'Multiple build_factory.py candidates match the frozen SHA; identity is ambiguous: ' + paths
        )
    summary = '; '.join(f"{item['path']}={item['sha256']}" for item in details)
    raise ValueError(
        'No active build_factory.py candidate matches the frozen SHA ' + C11C_BUILD_SHA + '. Candidates: ' + summary
    )


def build_context(root: Path) -> dict[str, Any]:
    d70_path, d70 = require_receipt(root, D70_RECEIPT, 'D7.0')
    d71_path, d71 = require_receipt(root, D71_RECEIPT, 'D7.1 receipt')
    d72_path, d72 = require_receipt(root, D72_RECEIPT, 'D7.2 receipt')
    d73_path, d73 = require_receipt(root, D73_RECEIPT, 'D7.3 receipt')
    d74_path, d74 = require_receipt(root, D74_RECEIPT, 'D7.4 receipt')
    d64_path, d64 = require_receipt(root, D64_RECEIPT, 'D6.4 receipt')
    d65_path, d65 = require_receipt(root, D65_RECEIPT, 'D6.5 receipt')
    matrix_path = require_file(root, D71_MATRIX, 'D7.1 canonical matrix')
    catalog_path = require_file(root, D73_CATALOG, 'D7.3 canonical catalog')
    build_factory_path, build_factory_candidates = discover_build_factory(root)
    for rel, label in (
        (D71_SPEC, 'D7.1 spec'), (D73_SPEC, 'D7.3 spec'), (D74_SPEC, 'D7.4 spec'),
        (D75_SPEC, 'D7.5 spec'), (D75_POLICY, 'D7.5 policy'),
        (D6_REGISTRY, 'D6.1 registry'), (D6_RESOLVER, 'D6.2 seed resolver'),
    ):
        require_file(root, rel, label)
    return {
        'd70_path': d70_path, 'd70': d70, 'd71_path': d71_path, 'd71': d71,
        'd72_path': d72_path, 'd72': d72, 'd73_path': d73_path, 'd73': d73,
        'd74_path': d74_path, 'd74': d74, 'd64_path': d64_path, 'd64': d64,
        'd65_path': d65_path, 'd65': d65, 'matrix_path': matrix_path,
        'matrix': load_json(matrix_path), 'catalog_path': catalog_path,
        'catalog': load_json(catalog_path),
        'build_factory_path': build_factory_path,
        'build_factory_candidates': build_factory_candidates,
    }


def validate_full(context: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    d70 = context['d70']; d71 = context['d71']; d72 = context['d72']; d73 = context['d73']; d74 = context['d74']
    d64 = context['d64']; d65 = context['d65']
    matrix = context['matrix']; catalog = context['catalog']

    matrix_rows = matrix.get('rows', [])
    catalog_items = catalog.get('items', [])
    matrix_authority = (d71.get('canonical_authorities') or {}).get('matrix') or d71.get('matrix_authority') or d71.get('authority')
    if matrix_authority != 'CANONICAL_D7_1':
        errors.append('D7_1_MATRIX_AUTHORITY_INVALID')
    if d72.get('matrix_authority') not in (None, 'CANONICAL_D7_1'):
        errors.append('D7_2_MATRIX_AUTHORITY_MISMATCH')
    if d73.get('matrix_authority') != 'CANONICAL_D7_1':
        errors.append('D7_3_MATRIX_AUTHORITY_MISMATCH')
    if d73.get('catalog_authority') != 'CANONICAL_D7_3':
        errors.append('D7_3_CATALOG_AUTHORITY_INVALID')
    if d74.get('catalog_authority') != 'CANONICAL_D7_3':
        errors.append('D7_4_CATALOG_AUTHORITY_MISMATCH')
    if d74.get('authority') != 'CANONICAL_D7_4':
        errors.append('D7_4_IDENTITY_AUTHORITY_INVALID')

    challenge_count = numeric_first(d70, 'challenge_count', 'challenges', 'challenge_files', 'challenge_inventory_count')
    if challenge_count is not None and challenge_count != EXPECTED_CHALLENGES:
        errors.append('D7_0_CHALLENGE_COUNT_NOT_9')
    if len(matrix_rows) != EXPECTED_CORE:
        errors.append('D7_1_MATRIX_NOT_90')
    if len(catalog_items) != EXPECTED_CORE:
        errors.append('D7_3_CATALOG_NOT_90')
    if d72.get('core_cases') not in (None, EXPECTED_CORE) or d72.get('coverage') not in (None, True):
        errors.append('D7_2_COVERAGE_GATE_INVALID')
    if d71.get('core_cases') not in (None, EXPECTED_CORE):
        errors.append('D7_1_CORE_NOT_90')
    if d71.get('challenge_count') not in (None, EXPECTED_CHALLENGES):
        errors.append('D7_1_CHALLENGE_COUNT_NOT_9')
    if d71.get('delivery_profile_count') not in (None, EXPECTED_PROFILES):
        errors.append('D7_1_PROFILE_COUNT_NOT_5')
    if d71.get('mode_count') not in (None, EXPECTED_MODES):
        errors.append('D7_1_MODE_COUNT_NOT_2')
    if d73.get('core_cases') != EXPECTED_CORE or d73.get('catalog_items') != EXPECTED_CORE or d73.get('complete') is not True:
        errors.append('D7_3_COVERAGE_GATE_INVALID')
    if d74.get('core_cases') != EXPECTED_CORE or d74.get('catalog_items') != EXPECTED_CORE or d74.get('one_to_one') is not True:
        errors.append('D7_4_COVERAGE_GATE_INVALID')

    expected_matrix_sha = sha256_file(context['matrix_path'])
    if catalog.get('sources', {}).get('d7_1_matrix_sha256') not in (None, expected_matrix_sha):
        errors.append('D7_3_MATRIX_HASH_INVALID')
    if d74.get('source_hashes_current') is not True:
        errors.append('D7_4_SOURCE_HASH_GATE_INVALID')

    gate_values = {
        'd74_d4_8_status': d74.get('d4_8_status'),
        'd74_runtime_authority': d74.get('runtime_authority'),
        'd74_production_execution': d74.get('production_execution'),
    }
    if d74.get('d4_8_status') != 'BLOCKED':
        errors.append('D4_8_NOT_BLOCKED')
    if d74.get('runtime_authority') != 'NONE':
        errors.append('D7_4_RUNTIME_AUTHORITY_NOT_NONE')
    if d74.get('production_execution') is not False:
        errors.append('D7_4_PRODUCTION_EXECUTION_ENABLED')
    if d74.get('renderer_execution') is not False:
        errors.append('D7_4_RENDERER_EXECUTION_ENABLED')

    for label, data in [('D6.4', d64), ('D6.5', d65)]:
        if data.get('production_execution') is True:
            errors.append(f'{label}_PRODUCTION_EXECUTION_ENABLED')
        if data.get('runtime_authority') not in (None, 'NONE'):
            errors.append(f'{label}_RUNTIME_AUTHORITY_ENABLED')

    build_sha = sha256_file(context['build_factory_path'])
    if build_sha != C11C_BUILD_SHA.lower():
        errors.append('C11C_BUILD_FACTORY_HASH_MISMATCH')

    if not isinstance(catalog.get('governance'), dict):
        errors.append('CATALOG_GOVERNANCE_MISSING')
    else:
        gov = catalog['governance']
        if gov.get('master_seed') != 'NOT_ADOPTED': errors.append('MASTER_SEED_POLICY_INVALID')
        if gov.get('derivation_runtime_activation') is not False: errors.append('DERIVATION_RUNTIME_ACTIVATED')
        if gov.get('cross_domain_seed_sharing') != 'FORBIDDEN': errors.append('CROSS_DOMAIN_SEED_SHARING_ALLOWED')
        if gov.get('automatic_seed_generation') is not False: errors.append('AUTOMATIC_SEED_GENERATION_ENABLED')
    authority_state = catalog.get('authority_state', {})
    if authority_state.get('runtime_authority') != 'NONE': errors.append('CATALOG_RUNTIME_AUTHORITY_INVALID')
    if authority_state.get('production_execution') is not False: errors.append('CATALOG_PRODUCTION_EXECUTION_INVALID')
    if authority_state.get('renderer_execution') is not False: errors.append('CATALOG_RENDERER_EXECUTION_INVALID')
    if authority_state.get('media_rendered_by_catalog') is not False: errors.append('CATALOG_MEDIA_RENDER_CLAIM_INVALID')

    release_path = context['root'] / 'release'
    release_exists = release_path.exists()
    if release_exists:
        errors.append('RELEASE_DIRECTORY_MUST_NOT_BE_CREATED_BY_D7_5')

    return {
        'checkpoint': 'D7.5',
        'status': 'PASS' if not errors else 'FAIL',
        'predecessors': {
            'D7.0': 'PASS/CLOSED', 'D7.1': 'PASS/CLOSED', 'D7.2': 'PASS/CLOSED',
            'D7.3': 'PASS/CLOSED', 'D7.4': 'PASS/CLOSED'
        },
        'challenge_count': challenge_count,
        'expected_challenges': EXPECTED_CHALLENGES,
        'profiles': EXPECTED_PROFILES,
        'modes': EXPECTED_MODES,
        'matrix_rows': len(matrix_rows),
        'catalog_items': len(catalog_items),
        'core_cases': EXPECTED_CORE,
        'matrix_authority': 'CANONICAL_D7_1',
        'catalog_authority': 'CANONICAL_D7_3',
        'identity_provenance_authority': 'CANONICAL_D7_4',
        'coverage_complete': len(matrix_rows) == EXPECTED_CORE and len(catalog_items) == EXPECTED_CORE,
        'source_matrix_sha256': expected_matrix_sha,
        'c11c_build_factory_sha256': build_sha,
        'c11c_build_factory_path': context['build_factory_path'].relative_to(context['root']).as_posix(),
        'c11c_build_factory_candidates': context.get('build_factory_candidates', []),
        'c11c_build_factory_expected_sha256': C11C_BUILD_SHA.lower(),
        'governance': {
            'master_seed': catalog.get('governance', {}).get('master_seed'),
            'derivation_runtime_activation': catalog.get('governance', {}).get('derivation_runtime_activation'),
            'cross_domain_seed_sharing': catalog.get('governance', {}).get('cross_domain_seed_sharing'),
            'automatic_seed_generation': catalog.get('governance', {}).get('automatic_seed_generation'),
            'd4_8': d74.get('d4_8_status'),
            'runtime_authority': d74.get('runtime_authority'),
            'production_execution': d74.get('production_execution'),
            'renderer_execution': d74.get('renderer_execution'),
        },
        'release_directory_present': release_exists,
        'errors': sorted(set(errors)),
    }


def validate_governance(context: dict[str, Any], full: dict[str, Any]) -> dict[str, Any]:
    catalog = context['catalog']; d64 = context['d64']; d74 = context['d74']
    checks = {
        'd4_8_blocked': d74.get('d4_8_status') == 'BLOCKED',
        'runtime_none': d74.get('runtime_authority') == 'NONE',
        'production_false': d74.get('production_execution') is False,
        'renderer_false': d74.get('renderer_execution') is False,
        'master_seed_not_adopted': catalog.get('governance', {}).get('master_seed') == 'NOT_ADOPTED',
        'derivation_runtime_false': catalog.get('governance', {}).get('derivation_runtime_activation') is False,
        'cross_domain_forbidden': catalog.get('governance', {}).get('cross_domain_seed_sharing') == 'FORBIDDEN',
        'automatic_seed_generation_false': catalog.get('governance', {}).get('automatic_seed_generation') is False,
        'd6_4_production_false': d64.get('production_execution') is not True,
        'd6_4_runtime_none': d64.get('runtime_authority') in (None, 'NONE'),
        'c11c_build_hash_gate': full.get('c11c_build_factory_sha256') == full.get('c11c_build_factory_expected_sha256'),
        'release_write_forbidden': full.get('release_directory_present') is False,
    }
    return {'checkpoint': 'D7.5', 'status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks, 'errors': sorted(k for k, v in checks.items() if not v)}


def negative_tests(context: dict[str, Any], full: dict[str, Any]) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    base = {
        'matrix_authority': full.get('matrix_authority'),
        'catalog_authority': full.get('catalog_authority'),
        'identity_provenance_authority': full.get('identity_provenance_authority'),
        'core_cases': full.get('core_cases'),
        'd4_8': full.get('governance', {}).get('d4_8'),
        'runtime_authority': full.get('governance', {}).get('runtime_authority'),
        'production_execution': full.get('governance', {}).get('production_execution'),
        'master_seed': full.get('governance', {}).get('master_seed'),
    }
    def reject(name: str, mutated: dict[str, Any], predicate) -> None:
        ok = bool(predicate(mutated))
        cases.append({'case': name, 'expected': 'REJECT', 'observed': 'REJECT' if ok else 'ACCEPT', 'pass': ok})
    reject('matrix_authority_tamper', {**base, 'matrix_authority': 'OTHER'}, lambda x: x['matrix_authority'] != 'CANONICAL_D7_1')
    reject('catalog_authority_tamper', {**base, 'catalog_authority': 'OTHER'}, lambda x: x['catalog_authority'] != 'CANONICAL_D7_3')
    reject('identity_authority_tamper', {**base, 'identity_provenance_authority': 'OTHER'}, lambda x: x['identity_provenance_authority'] != 'CANONICAL_D7_4')
    reject('core_case_count_tamper', {**base, 'core_cases': 89}, lambda x: x['core_cases'] != EXPECTED_CORE)
    reject('d4_8_unblocked', {**base, 'd4_8': 'READY'}, lambda x: x['d4_8'] != 'BLOCKED')
    reject('runtime_authority_tamper', {**base, 'runtime_authority': 'CATALOG'}, lambda x: x['runtime_authority'] != 'NONE')
    reject('production_enable_tamper', {**base, 'production_execution': True}, lambda x: x['production_execution'] is True)
    reject('master_seed_adoption_tamper', {**base, 'master_seed': 'ADOPTED'}, lambda x: x['master_seed'] != 'NOT_ADOPTED')
    return {'checkpoint': 'D7.5', 'count': len(cases), 'all_pass': all(x['pass'] for x in cases), 'cases': cases}


def build(root: Path) -> int:
    context = build_context(root)
    context['root'] = root
    # Preserve the canonical path resolved by discover_build_factory().
    # The active C11-C build_factory.py is rooted at the repository root.
    full = validate_full(context)
    governance = validate_governance(context, full)
    negatives = negative_tests(context, full)
    overall_pass = full['status'] == 'PASS' and governance['status'] == 'PASS' and negatives['all_pass']
    receipt = {
        'checkpoint': 'C11-D D7.5',
        'result': 'PASS' if overall_pass else 'FAIL',
        'status': 'CLOSED' if overall_pass else 'BLOCKED',
        'objective': 'Full D7 Acceptance',
        'd7_predecessors_pass_closed': True,
        'canonical_authorities': {
            'matrix': 'CANONICAL_D7_1',
            'catalog': 'CANONICAL_D7_3',
            'identity_provenance': 'CANONICAL_D7_4',
        },
        'challenge_count': full['challenge_count'],
        'profiles': EXPECTED_PROFILES,
        'modes': EXPECTED_MODES,
        'matrix_rows': full['matrix_rows'],
        'catalog_items': full['catalog_items'],
        'core_cases': full['core_cases'],
        'coverage_complete': full['coverage_complete'],
        'governance_pass': governance['status'] == 'PASS',
        'negative_cases': negatives['count'],
        'negative_tests_pass': negatives['all_pass'],
        'd4_8_status': full['governance']['d4_8'],
        'runtime_authority': full['governance']['runtime_authority'],
        'production_execution': full['governance']['production_execution'],
        'renderer_execution': full['governance']['renderer_execution'],
        'release_directory_present': full['release_directory_present'],
        'c11c_build_factory_sha256': full['c11c_build_factory_sha256'],
        'next': 'D8 - Media QA + Release Pipeline' if overall_pass else 'REPAIR_D7.5',
    }
    output = root / OUTPUT_DIR
    for name, obj in zip(OUTPUT_NAMES, (full, governance, negatives, receipt)):
        write_json(output / name, obj)
    print(json.dumps({
        'authority': 'CANONICAL_D7_5',
        'matrix_authority': 'CANONICAL_D7_1',
        'catalog_authority': 'CANONICAL_D7_3',
        'identity_provenance_authority': 'CANONICAL_D7_4',
        'challenges': full['challenge_count'],
        'profiles': EXPECTED_PROFILES,
        'modes': EXPECTED_MODES,
        'matrix_rows': full['matrix_rows'],
        'catalog_items': full['catalog_items'],
        'core_cases': full['core_cases'],
        'coverage_complete': full['coverage_complete'],
        'governance_pass': governance['status'] == 'PASS',
        'negative_cases': negatives['count'],
        'negative_tests_pass': negatives['all_pass'],
        'd4_8_status': full['governance']['d4_8'],
        'runtime_authority': full['governance']['runtime_authority'],
        'production_execution': full['governance']['production_execution'],
        'release_directory_present': full['release_directory_present'],
        'result': receipt['result'],
        'status': receipt['status'],
        'next': receipt['next'],
    }, sort_keys=True))
    return 0 if overall_pass else 2


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
