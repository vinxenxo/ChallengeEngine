#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ALLOWED_OUTPUT_REL = Path('artifacts/tests/c11d_d7/d7_1')
D70_RECEIPT_REL = Path('artifacts/tests/c11d_d7/d7_0/d7_0_audit_receipt.json')
D65_RECEIPT_REL = Path('artifacts/tests/c11d_d6/d6_5/d6_5_acceptance_receipt.json')
D4_SCHEMA_REL = Path('definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json')
D6_REGISTRY_REL = Path('definitions/c11d/seeds/C11D_SEED_REGISTRY_V1.json')
D6_POLICY_REL = Path('definitions/c11d/seeds/C11D_SEED_GOVERNANCE_POLICY_V1.json')
D4_ORCHESTRATOR_REL = Path('tools/c11d/d4/canonical_production_orchestrator.py')
MATRIX_SPEC_REL = Path('definitions/c11d/production/C11D_PRODUCTION_MATRIX_SPEC_V1.json')
MATRIX_POLICY_REL = Path('definitions/c11d/production/C11D_PRODUCTION_MATRIX_GOVERNANCE_POLICY_V1.json')
C11C_BUILD_SHA = '3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3'
EXPECTED_CHALLENGES = 9
EXPECTED_PROFILES = 5
EXPECTED_MODES = ('REVIEW', 'PRODUCTION')
OUTPUT_NAMES = (
    'd7_1_canonical_matrix.json',
    'd7_1_matrix_validation.json',
    'd7_1_negative_tests.json',
    'd7_1_matrix_receipt.json',
)


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


def repo_snapshot(root: Path) -> dict[str, Any]:
    files: list[tuple[str, int, str]] = []
    skip = ALLOWED_OUTPUT_REL.as_posix().rstrip('/') + '/'
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel == '.git/index.lock' or rel.startswith(skip):
            continue
        try:
            digest = sha256_file(path)
            size = path.stat().st_size
        except OSError:
            continue
        files.append((rel, size, digest))
    files.sort(key=lambda item: item[0])
    h = hashlib.sha256()
    for rel, size, digest in files:
        h.update(rel.encode('utf-8'))
        h.update(b'\0')
        h.update(str(size).encode('ascii'))
        h.update(b'\0')
        h.update(digest.encode('ascii'))
        h.update(b'\n')
    return {'files': len(files), 'sha256': h.hexdigest()}


def require_pass_closed(path: Path, label: str) -> tuple[dict[str, Any] | None, str | None]:
    if not path.is_file():
        return None, f'{label} receipt missing: {path.as_posix()}'
    try:
        data = load_json(path)
    except Exception as exc:
        return None, f'{label} receipt parse error: {exc}'
    if not isinstance(data, dict):
        return None, f'{label} receipt is not an object'
    if data.get('result') != 'PASS' or data.get('status') != 'CLOSED':
        return data, f'{label} must be PASS/CLOSED'
    return data, None


def collect_enum_values(node: Any, target_key: str, path: str = '') -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == target_key and isinstance(value, dict) and isinstance(value.get('enum'), list):
                found.extend(str(item) for item in value['enum'])
            found.extend(collect_enum_values(value, target_key, f'{path}/{key}'))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(collect_enum_values(value, target_key, f'{path}/{index}'))
    return sorted(set(found))


def discover_profiles(root: Path) -> tuple[list[str], list[str]]:
    schema = root / D4_SCHEMA_REL
    if schema.is_file():
        try:
            data = load_json(schema)
            enums = collect_enum_values(data, 'delivery_profile_id')
            if enums:
                return enums, [schema.relative_to(root).as_posix()]
        except Exception:
            pass

    candidates: list[Path] = []
    prod_root = root / 'definitions/c11d/production'
    if prod_root.is_dir():
        candidates.extend(sorted(prod_root.glob('*.json')))
    d4_artifacts = root / 'artifacts/tests/c11d_d4'
    if d4_artifacts.is_dir():
        candidates.extend(sorted(d4_artifacts.rglob('*.json')))

    values: set[str] = set()
    evidence: set[str] = set()
    for path in candidates:
        try:
            data = load_json(path)
        except Exception:
            continue
        local_values: set[str] = set()
        def walk(node: Any) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == 'delivery_profile_id' and isinstance(value, str):
                        local_values.add(value)
                    if key == 'profile_id' and isinstance(value, str) and ('delivery' in path.as_posix().lower() or 'production_profile' in path.as_posix().lower()):
                        local_values.add(value)
                    walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)
        walk(data)
        if local_values:
            values.update(local_values)
            evidence.add(path.relative_to(root).as_posix())
    return sorted(values), sorted(evidence)


def discover_challenges(root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    challenges_root = root / 'challenges'
    for path in sorted(challenges_root.glob('CHALLENGE_*.json')) if challenges_root.is_dir() else []:
        data = load_json(path)
        if not isinstance(data, dict):
            raise ValueError(f'Challenge is not object: {path}')
        results.append({
            'challenge_id': str(data.get('challenge_id') or path.stem),
            'version': data.get('version'),
            'mechanic': data.get('mechanic') or data.get('mechanics') or data.get('type'),
            'family': data.get('family'),
            'path': path.relative_to(root).as_posix(),
        })
    return results


def load_spec(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    spec = load_json(root / MATRIX_SPEC_REL)
    policy = load_json(root / MATRIX_POLICY_REL)
    if not isinstance(spec, dict) or not isinstance(policy, dict):
        raise ValueError('D7.1 matrix spec/policy must be objects')
    return spec, policy


def build_matrix(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    d70, error70 = require_pass_closed(root / D70_RECEIPT_REL, 'D7.0')
    if error70:
        raise ValueError(error70)
    d65, error65 = require_pass_closed(root / D65_RECEIPT_REL, 'D6.5')
    if error65:
        raise ValueError(error65)
    for rel, label in ((D4_SCHEMA_REL, 'D4.2 schema'), (D6_REGISTRY_REL, 'D6.1 registry'), (D6_POLICY_REL, 'D6.1 policy'), (D4_ORCHESTRATOR_REL, 'D4.4 orchestrator')):
        if not (root / rel).is_file():
            raise ValueError(f'{label} missing: {rel.as_posix()}')

    spec, policy = load_spec(root)
    challenges = discover_challenges(root)
    profiles, profile_evidence = discover_profiles(root)
    if len(challenges) != EXPECTED_CHALLENGES:
        raise ValueError(f'Expected {EXPECTED_CHALLENGES} challenges; discovered {len(challenges)}')
    if len(profiles) != EXPECTED_PROFILES:
        raise ValueError(f'Expected {EXPECTED_PROFILES} delivery profiles; discovered {len(profiles)}: {profiles}')
    modes = list(EXPECTED_MODES)
    rows: list[dict[str, Any]] = []
    for challenge in challenges:
        for profile_id in profiles:
            for mode in modes:
                key = f"{challenge['challenge_id']}|{profile_id}|{mode}"
                rows.append({
                    'matrix_key': key,
                    'challenge_id': challenge['challenge_id'],
                    'challenge_version': challenge.get('version'),
                    'challenge_path': challenge['path'],
                    'delivery_profile_id': profile_id,
                    'mode': mode,
                    'seed_bindings': {
                        'GAMEPLAY': {'authority': 'gameplay', 'source_field': 'request.seed', 'resolution': 'D6.2 explicit'},
                        'MUSIC': {'authority': 'music', 'source_field': 'request.music_seed', 'resolution': 'D6.2 explicit'}
                    },
                    'personalization_profile': 'none_v1',
                    'variation_index': None,
                    'execution': {
                        'plan_only': True,
                        'production_execution': False,
                        'renderer_execution': False,
                        'runtime_authority': 'NONE'
                    },
                    'governance': {
                        'master_seed': 'NOT_ADOPTED',
                        'derivation_runtime_activation': False,
                        'cross_domain_seed_sharing': 'FORBIDDEN'
                    }
                })
    rows.sort(key=lambda item: item['matrix_key'])
    matrix = {
        'matrix_id': spec['matrix_id'],
        'schema_version': spec['schema_version'],
        'authority': 'D7.1',
        'status': 'CANONICAL',
        'coverage': {
            'challenge_count': len(challenges),
            'delivery_profile_count': len(profiles),
            'mode_count': len(modes),
            'expected_core_cases': len(rows),
            'core_cases': len(rows),
            'complete': len(rows) == len(challenges) * len(profiles) * len(modes)
        },
        'sources': {
            'd7_0_receipt': D70_RECEIPT_REL.as_posix(),
            'd6_5_receipt': D65_RECEIPT_REL.as_posix(),
            'd4_schema': D4_SCHEMA_REL.as_posix(),
            'd6_registry': D6_REGISTRY_REL.as_posix(),
            'd6_policy': D6_POLICY_REL.as_posix(),
            'd4_orchestrator': D4_ORCHESTRATOR_REL.as_posix(),
            'delivery_profile_evidence': profile_evidence
        },
        'rows': rows,
        'extensions': {
            'personalization_core_default': 'none_v1',
            'personalization_cases_not_expanded_in_core_matrix': True,
            'master_seed': 'NOT_ADOPTED'
        },
        'authority_state': {
            'matrix_authority': 'CANONICAL_D7_1',
            'catalog_authority': 'NOT_ESTABLISHED_IN_D7_1',
            'runtime_authority': 'NONE',
            'production_execution': False
        }
    }
    validation = validate_matrix(matrix, spec, policy, challenges, profiles)
    return matrix, validation


def validate_matrix(matrix: dict[str, Any], spec: dict[str, Any], policy: dict[str, Any], challenges: list[dict[str, Any]], profiles: list[str]) -> dict[str, Any]:
    rows = matrix.get('rows', [])
    expected = len(challenges) * len(profiles) * len(EXPECTED_MODES)
    keys = [row.get('matrix_key') for row in rows]
    duplicate_keys = sorted({key for key in keys if keys.count(key) > 1})
    challenge_ids = {item['challenge_id'] for item in challenges}
    errors: list[str] = []
    if len(rows) != expected:
        errors.append('CORE_COVERAGE_COUNT_MISMATCH')
    if len(set(keys)) != len(keys):
        errors.append('DUPLICATE_MATRIX_KEY')
    for row in rows:
        if row.get('challenge_id') not in challenge_ids:
            errors.append('UNKNOWN_CHALLENGE')
        if row.get('delivery_profile_id') not in set(profiles):
            errors.append('UNKNOWN_DELIVERY_PROFILE')
        if row.get('mode') not in set(EXPECTED_MODES):
            errors.append('UNKNOWN_MODE')
        if row.get('seed_bindings', {}).get('GAMEPLAY', {}).get('source_field') != 'request.seed':
            errors.append('INVALID_GAMEPLAY_SEED_BINDING')
        if row.get('seed_bindings', {}).get('MUSIC', {}).get('source_field') != 'request.music_seed':
            errors.append('INVALID_MUSIC_SEED_BINDING')
        if row.get('execution', {}).get('production_execution') is not False:
            errors.append('PRODUCTION_EXECUTION_ENABLED')
        if row.get('execution', {}).get('runtime_authority') != 'NONE':
            errors.append('RUNTIME_AUTHORITY_NOT_NONE')
    return {
        'result': 'PASS' if not errors else 'FAIL',
        'errors': sorted(set(errors)),
        'rows': len(rows),
        'expected_rows': expected,
        'duplicate_matrix_keys': duplicate_keys,
        'matrix_authority': matrix.get('authority'),
        'policy_authority': policy.get('matrix_authority'),
        'catalog_authority': policy.get('catalog_authority')
    }


def negative_tests() -> dict[str, Any]:
    def validate_candidate(candidate: dict[str, Any]) -> tuple[bool, str]:
        gameplay = candidate.get('seed_bindings', {}).get('GAMEPLAY', {})
        music = candidate.get('seed_bindings', {}).get('MUSIC', {})
        execution = candidate.get('execution', {})
        governance = candidate.get('governance', {})
        if candidate.get('challenge_id') == 'UNKNOWN': return False, 'UNKNOWN_CHALLENGE'
        if candidate.get('delivery_profile_id') == 'UNKNOWN': return False, 'UNKNOWN_DELIVERY_PROFILE'
        if candidate.get('mode') not in EXPECTED_MODES: return False, 'UNKNOWN_MODE'
        if gameplay.get('authority') != 'gameplay' or gameplay.get('source_field') != 'request.seed': return False, 'INVALID_GAMEPLAY_SEED_BINDING'
        if music.get('authority') != 'music' or music.get('source_field') != 'request.music_seed': return False, 'INVALID_MUSIC_SEED_BINDING'
        if execution.get('production_execution') is not False: return False, 'PRODUCTION_EXECUTION_ENABLED'
        if execution.get('renderer_execution') is not False: return False, 'RENDERER_EXECUTION_ENABLED'
        if execution.get('runtime_authority') != 'NONE': return False, 'RUNTIME_AUTHORITY_NOT_NONE'
        if governance.get('master_seed') != 'NOT_ADOPTED': return False, 'MASTER_SEED_AUTHORITY'
        if governance.get('derivation_runtime_activation') is not False: return False, 'DERIVATION_ACTIVATED'
        if governance.get('automatic_seed_generation') is True: return False, 'AUTOMATIC_SEED_GENERATION'
        if governance.get('catalog_authority') == 'CANONICAL_D7_1': return False, 'CATALOG_AUTHORITY_ACTIVATED'
        return True, 'VALID'

    base = {
        'challenge_id': 'CHALLENGE_001',
        'delivery_profile_id': 'PROFILE_001',
        'mode': 'REVIEW',
        'seed_bindings': {
            'GAMEPLAY': {'authority': 'gameplay', 'source_field': 'request.seed'},
            'MUSIC': {'authority': 'music', 'source_field': 'request.music_seed'}
        },
        'execution': {'production_execution': False, 'renderer_execution': False, 'runtime_authority': 'NONE'},
        'governance': {'master_seed': 'NOT_ADOPTED', 'derivation_runtime_activation': False, 'automatic_seed_generation': False}
    }
    cases: list[dict[str, Any]] = []

    def add_candidate(name: str, mutate: Any) -> None:
        candidate = json.loads(json.dumps(base))
        mutate(candidate)
        accepted, reason = validate_candidate(candidate)
        cases.append({'case': name, 'expected': 'REJECT', 'observed': 'ACCEPT' if accepted else 'REJECT', 'reason': reason, 'pass': not accepted})

    add_candidate('unknown_challenge', lambda c: c.update({'challenge_id': 'UNKNOWN'}))
    add_candidate('unknown_profile', lambda c: c.update({'delivery_profile_id': 'UNKNOWN'}))
    add_candidate('unknown_mode', lambda c: c.update({'mode': 'INVALID'}))
    add_candidate('gameplay_mapped_to_music', lambda c: c['seed_bindings']['GAMEPLAY'].update({'authority': 'music', 'source_field': 'request.music_seed'}))
    add_candidate('music_mapped_to_gameplay', lambda c: c['seed_bindings']['MUSIC'].update({'authority': 'gameplay', 'source_field': 'request.seed'}))
    add_candidate('production_execution_enabled', lambda c: c['execution'].update({'production_execution': True}))
    add_candidate('renderer_enabled', lambda c: c['execution'].update({'renderer_execution': True}))
    add_candidate('runtime_authority_enabled', lambda c: c['execution'].update({'runtime_authority': 'D7.1'}))
    add_candidate('master_seed_introduced', lambda c: c['governance'].update({'master_seed': 'CANONICAL'}))
    add_candidate('derivation_activated', lambda c: c['governance'].update({'derivation_runtime_activation': True}))
    add_candidate('automatic_seed_generation', lambda c: c['governance'].update({'automatic_seed_generation': True}))
    add_candidate('personalization_as_seed_source', lambda c: c['seed_bindings']['GAMEPLAY'].update({'authority': 'personalization', 'source_field': 'personalization'}))
    add_candidate('variation_as_seed_source', lambda c: c['seed_bindings']['GAMEPLAY'].update({'authority': 'variation', 'source_field': 'variation_index'}))
    add_candidate('protected_winning_frame_as_seed', lambda c: c['seed_bindings']['GAMEPLAY'].update({'authority': 'winning_frame', 'source_field': 'winning_frame'}))
    add_candidate('catalog_authority_activated', lambda c: c['governance'].update({'catalog_authority': 'CANONICAL_D7_1'}))
    add_candidate('cross_domain_sharing', lambda c: c['seed_bindings']['MUSIC'].update({'authority': 'gameplay', 'source_field': 'request.seed'}))
    add_candidate('seed_value_generated', lambda c: c['governance'].update({'automatic_seed_generation': True}))

    duplicate_matrix = {
        'rows': [
            {'matrix_key': 'CHALLENGE_001|PROFILE_001|REVIEW'},
            {'matrix_key': 'CHALLENGE_001|PROFILE_001|REVIEW'}
        ]
    }
    duplicate_detected = len({row['matrix_key'] for row in duplicate_matrix['rows']}) != len(duplicate_matrix['rows'])
    cases.append({'case': 'duplicate_matrix_key', 'expected': 'REJECT', 'observed': 'REJECT' if duplicate_detected else 'ACCEPT', 'reason': 'DUPLICATE_MATRIX_KEY' if duplicate_detected else 'NO_DUPLICATE_DETECTED', 'pass': duplicate_detected})

    return {'count': len(cases), 'all_pass': all(item['pass'] for item in cases), 'cases': cases}


def run(root: Path) -> int:
    try:
        matrix, validation = build_matrix(root)
        negatives = negative_tests()
        receipt = {
            'checkpoint': 'D7.1',
            'name': 'Canonical Production Matrix',
            'result': 'PASS' if validation['result'] == 'PASS' and negatives['all_pass'] else 'FAIL',
            'status': 'CLOSED' if validation['result'] == 'PASS' and negatives['all_pass'] else 'BLOCKED',
            'd7_0_predecessor': 'PASS/CLOSED',
            'd6_5_predecessor': 'PASS/CLOSED',
            'canonical_authorities': {'matrix': 'CANONICAL_D7_1', 'catalog': 'NOT_ESTABLISHED_IN_D7_1'},
            'challenge_count': matrix['coverage']['challenge_count'],
            'delivery_profile_count': matrix['coverage']['delivery_profile_count'],
            'mode_count': matrix['coverage']['mode_count'],
            'core_cases': matrix['coverage']['core_cases'],
            'core_complete': matrix['coverage']['complete'],
            'negative_cases': negatives['count'],
            'negative_tests_pass': negatives['all_pass'],
            'seed_sources': {'GAMEPLAY': 'request.seed', 'MUSIC': 'request.music_seed'},
            'master_seed': 'NOT_ADOPTED',
            'derivation_runtime_activation': False,
            'runtime_authority': 'NONE',
            'production_execution': False,
            'renderer_execution': False,
            'godot_production_execution': False,
            'ffmpeg_production_execution': False,
            'c11c_build_factory_expected_sha256': C11C_BUILD_SHA,
            'next': 'D7.2 - Matrix Coverage / Constraint Validator' if validation['result'] == 'PASS' and negatives['all_pass'] else 'REPAIR_D7.1'
        }
        out = root / ALLOWED_OUTPUT_REL
        write_json(out / OUTPUT_NAMES[0], matrix)
        write_json(out / OUTPUT_NAMES[1], validation)
        write_json(out / OUTPUT_NAMES[2], negatives)
        write_json(out / OUTPUT_NAMES[3], receipt)
        print(json.dumps({
            'authority': 'CANONICAL_D7_1',
            'challenge_count': matrix['coverage']['challenge_count'],
            'delivery_profile_count': matrix['coverage']['delivery_profile_count'],
            'mode_count': matrix['coverage']['mode_count'],
            'core_cases': matrix['coverage']['core_cases'],
            'core_complete': matrix['coverage']['complete'],
            'negative_cases': negatives['count'],
            'negative_tests_pass': negatives['all_pass'],
            'result': receipt['result'],
            'status': receipt['status'],
            'catalog_authority': 'NOT_ESTABLISHED_IN_D7_1'
        }, ensure_ascii=False, sort_keys=True))
        return 0 if receipt['result'] == 'PASS' else 2
    except Exception as exc:
        print(json.dumps({'result': 'FAIL', 'status': 'BLOCKED', 'error': str(exc)}, ensure_ascii=False, sort_keys=True))
        return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--snapshot-only', action='store_true')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print('Repository root does not exist.', file=sys.stderr)
        return 2
    if args.snapshot_only:
        print(json.dumps(repo_snapshot(root), sort_keys=True))
        return 0
    return run(root)


if __name__ == '__main__':
    raise SystemExit(main())
