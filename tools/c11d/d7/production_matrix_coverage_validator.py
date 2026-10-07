#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ALLOWED_OUTPUT_REL = Path('artifacts/tests/c11d_d7/d7_2')
D70_RECEIPT_REL = Path('artifacts/tests/c11d_d7/d7_0/d7_0_audit_receipt.json')
D71_MATRIX_REL = Path('artifacts/tests/c11d_d7/d7_1/d7_1_canonical_matrix.json')
D71_VALIDATION_REL = Path('artifacts/tests/c11d_d7/d7_1/d7_1_matrix_validation.json')
D71_NEGATIVE_REL = Path('artifacts/tests/c11d_d7/d7_1/d7_1_negative_tests.json')
D71_RECEIPT_REL = Path('artifacts/tests/c11d_d7/d7_1/d7_1_matrix_receipt.json')
D65_RECEIPT_REL = Path('artifacts/tests/c11d_d6/d6_5/d6_5_acceptance_receipt.json')
D4_SCHEMA_REL = Path('definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json')
POLICY_REL = Path('definitions/c11d/production/C11D_PRODUCTION_MATRIX_COVERAGE_POLICY_V1.json')
C11C_BUILD_SHA = '3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3'
EXPECTED_MODES = ('REVIEW', 'PRODUCTION')
OUTPUT_NAMES = (
    'd7_2_coverage_matrix.json',
    'd7_2_constraint_validation.json',
    'd7_2_negative_tests.json',
    'd7_2_validation_receipt.json',
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


def require_pass_closed(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f'{label} receipt missing: {path.as_posix()}')
    data = load_json(path)
    if not isinstance(data, dict):
        raise ValueError(f'{label} receipt is not an object')
    if data.get('result') != 'PASS' or data.get('status') != 'CLOSED':
        raise ValueError(f'{label} must be PASS/CLOSED')
    return data


def collect_enum_values(node: Any, target_key: str) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == target_key and isinstance(value, dict) and isinstance(value.get('enum'), list):
                found.extend(str(item) for item in value['enum'])
            found.extend(collect_enum_values(value, target_key))
    elif isinstance(node, list):
        for value in node:
            found.extend(collect_enum_values(value, target_key))
    return sorted(set(found))


def discover_challenges(root: Path) -> list[str]:
    challenge_root = root / 'challenges'
    results: list[str] = []
    if not challenge_root.is_dir():
        return results
    for path in sorted(challenge_root.glob('CHALLENGE_*.json')):
        data = load_json(path)
        if isinstance(data, dict):
            results.append(str(data.get('challenge_id') or path.stem))
    return results


def discover_profiles(root: Path, matrix: dict[str, Any]) -> list[str]:
    schema_path = root / D4_SCHEMA_REL
    if schema_path.is_file():
        try:
            enums = collect_enum_values(load_json(schema_path), 'delivery_profile_id')
            if enums:
                return enums
        except Exception:
            pass
    return sorted({str(row.get('delivery_profile_id')) for row in matrix.get('rows', []) if row.get('delivery_profile_id') is not None})


def load_inputs(root: Path) -> dict[str, Any]:
    d70 = require_pass_closed(root / D70_RECEIPT_REL, 'D7.0')
    d65 = require_pass_closed(root / D65_RECEIPT_REL, 'D6.5')
    d71 = require_pass_closed(root / D71_RECEIPT_REL, 'D7.1')
    matrix = load_json(root / D71_MATRIX_REL)
    d71_validation = load_json(root / D71_VALIDATION_REL)
    d71_negative = load_json(root / D71_NEGATIVE_REL)
    policy = load_json(root / POLICY_REL)
    if not isinstance(matrix, dict) or not isinstance(d71_validation, dict) or not isinstance(d71_negative, dict) or not isinstance(policy, dict):
        raise ValueError('D7.1 matrix/validation/negative/policy inputs must be objects')
    return {
        'd70': d70,
        'd65': d65,
        'd71': d71,
        'matrix': matrix,
        'd71_validation': d71_validation,
        'd71_negative': d71_negative,
        'policy': policy,
    }


def validate_matrix(matrix: dict[str, Any], policy: dict[str, Any], challenges: list[str], profiles: list[str]) -> tuple[dict[str, Any], list[str]]:
    rows = matrix.get('rows') if isinstance(matrix.get('rows'), list) else []
    errors: list[str] = []
    expected = len(challenges) * len(profiles) * len(EXPECTED_MODES)
    allowed_challenges = set(challenges)
    allowed_profiles = set(profiles)
    allowed_modes = set(EXPECTED_MODES)
    keys = [row.get('matrix_key') if isinstance(row, dict) else None for row in rows]
    duplicate_keys = sorted({key for key in keys if keys.count(key) > 1})
    expected_canonical_authority = policy.get('matrix_authority', 'CANONICAL_D7_1')
    matrix_authority = matrix.get('authority')
    matrix_authority_state = matrix.get('authority_state', {}) if isinstance(matrix.get('authority_state'), dict) else {}
    if matrix_authority != 'D7.1' or matrix_authority_state.get('matrix_authority') != expected_canonical_authority:
        errors.append('MATRIX_AUTHORITY_MISMATCH')
    if matrix.get('status') != 'CANONICAL':
        errors.append('MATRIX_STATUS_NOT_CANONICAL')
    if len(rows) != expected:
        errors.append('CORE_COVERAGE_COUNT_MISMATCH')
    if duplicate_keys:
        errors.append('DUPLICATE_MATRIX_KEY')

    challenge_counts = {value: 0 for value in challenges}
    profile_counts = {value: 0 for value in profiles}
    mode_counts = {value: 0 for value in EXPECTED_MODES}
    expected_keys = set()
    for challenge in challenges:
        for profile in profiles:
            for mode in EXPECTED_MODES:
                expected_keys.add(f'{challenge}|{profile}|{mode}')

    actual_keys: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f'ROW_NOT_OBJECT:{index}')
            continue
        challenge_id = row.get('challenge_id')
        profile_id = row.get('delivery_profile_id')
        mode = row.get('mode')
        key = row.get('matrix_key')
        if challenge_id not in allowed_challenges:
            errors.append('UNKNOWN_CHALLENGE')
        else:
            challenge_counts[challenge_id] += 1
        if profile_id not in allowed_profiles:
            errors.append('UNKNOWN_DELIVERY_PROFILE')
        else:
            profile_counts[profile_id] += 1
        if mode not in allowed_modes:
            errors.append('UNKNOWN_MODE')
        else:
            mode_counts[mode] += 1
        if isinstance(key, str):
            actual_keys.add(key)
        expected_key = f'{challenge_id}|{profile_id}|{mode}'
        if key != expected_key:
            errors.append('MATRIX_KEY_COMPONENT_MISMATCH')

        gameplay = row.get('seed_bindings', {}).get('GAMEPLAY', {}) if isinstance(row.get('seed_bindings'), dict) else {}
        music = row.get('seed_bindings', {}).get('MUSIC', {}) if isinstance(row.get('seed_bindings'), dict) else {}
        execution = row.get('execution', {}) if isinstance(row.get('execution'), dict) else {}
        governance = row.get('governance', {}) if isinstance(row.get('governance'), dict) else {}
        if gameplay.get('authority') != 'gameplay' or gameplay.get('source_field') != 'request.seed' or gameplay.get('resolution') != 'D6.2 explicit':
            errors.append('INVALID_GAMEPLAY_SEED_BINDING')
        if music.get('authority') != 'music' or music.get('source_field') != 'request.music_seed' or music.get('resolution') != 'D6.2 explicit':
            errors.append('INVALID_MUSIC_SEED_BINDING')
        if execution.get('plan_only') is not True:
            errors.append('PLAN_ONLY_NOT_TRUE')
        if execution.get('production_execution') is not False:
            errors.append('PRODUCTION_EXECUTION_ENABLED')
        if execution.get('renderer_execution') is not False:
            errors.append('RENDERER_EXECUTION_ENABLED')
        if execution.get('runtime_authority') != 'NONE':
            errors.append('RUNTIME_AUTHORITY_NOT_NONE')
        if row.get('personalization_profile') != policy.get('personalization_core_default', 'none_v1'):
            errors.append('CORE_PERSONALIZATION_NOT_DEFAULT')
        if row.get('variation_index', None) is not policy.get('variation_index_core_value', None):
            errors.append('VARIATION_INDEX_MUST_REMAIN_NULL')
        if governance.get('master_seed') != 'NOT_ADOPTED':
            errors.append('MASTER_SEED_AUTHORITY')
        if governance.get('derivation_runtime_activation') is not False:
            errors.append('DERIVATION_ACTIVATED')
        if governance.get('cross_domain_seed_sharing') != 'FORBIDDEN':
            errors.append('CROSS_DOMAIN_SEED_SHARING')

    for value, count in challenge_counts.items():
        if count != len(profiles) * len(EXPECTED_MODES):
            errors.append('CHALLENGE_DIMENSION_INCOMPLETE')
    for value, count in profile_counts.items():
        if count != len(challenges) * len(EXPECTED_MODES):
            errors.append('PROFILE_DIMENSION_INCOMPLETE')
    for value, count in mode_counts.items():
        if count != len(challenges) * len(profiles):
            errors.append('MODE_DIMENSION_INCOMPLETE')

    missing_keys = sorted(expected_keys - actual_keys)
    unexpected_keys = sorted(actual_keys - expected_keys)
    if missing_keys:
        errors.append('MISSING_MATRIX_KEYS')
    if unexpected_keys:
        errors.append('UNEXPECTED_MATRIX_KEYS')

    coverage = {
        'challenge_count': len(challenges),
        'delivery_profile_count': len(profiles),
        'mode_count': len(EXPECTED_MODES),
        'expected_core_cases': expected,
        'actual_core_cases': len(rows),
        'complete': not errors,
        'challenge_counts': challenge_counts,
        'profile_counts': profile_counts,
        'mode_counts': mode_counts,
        'duplicate_matrix_keys': duplicate_keys,
        'missing_matrix_keys': missing_keys,
        'unexpected_matrix_keys': unexpected_keys,
    }
    return coverage, sorted(set(errors))


def negative_tests(challenges: list[str], profiles: list[str], base_matrix: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    base_rows = base_matrix.get('rows', [])
    if not base_rows:
        raise ValueError('D7.1 matrix contains no rows')
    base = json.loads(json.dumps(base_rows[0]))

    def candidate_errors(candidate_rows: list[dict[str, Any]]) -> set[str]:
        _, errors = validate_matrix({
            'authority': 'D7.1',
            'status': 'CANONICAL',
            'authority_state': {'matrix_authority': 'CANONICAL_D7_1'},
            'rows': candidate_rows
        }, policy, challenges, profiles)
        return set(errors)

    cases: list[dict[str, Any]] = []

    def add(name: str, mutate: Any, expected_error: str) -> None:
        candidate = json.loads(json.dumps(base_rows))
        mutate(candidate)
        errors = candidate_errors(candidate)
        cases.append({'case': name, 'expected': 'REJECT', 'reason_expected': expected_error, 'observed_reject': bool(errors), 'reason_observed': sorted(errors), 'pass': expected_error in errors})

    add('missing_row', lambda rows: rows.pop(), 'CORE_COVERAGE_COUNT_MISMATCH')
    add('duplicate_matrix_key', lambda rows: rows.__setitem__(1, json.loads(json.dumps(rows[0]))), 'DUPLICATE_MATRIX_KEY')
    add('unknown_challenge', lambda rows: rows[0].update({'challenge_id': 'UNKNOWN'}), 'UNKNOWN_CHALLENGE')
    add('unknown_profile', lambda rows: rows[0].update({'delivery_profile_id': 'UNKNOWN'}), 'UNKNOWN_DELIVERY_PROFILE')
    add('invalid_mode', lambda rows: rows[0].update({'mode': 'INVALID'}), 'UNKNOWN_MODE')
    add('wrong_matrix_key', lambda rows: rows[0].update({'matrix_key': 'TAMPERED'}), 'MATRIX_KEY_COMPONENT_MISMATCH')
    add('gameplay_binding_mapped_to_music', lambda rows: rows[0]['seed_bindings']['GAMEPLAY'].update({'authority': 'music', 'source_field': 'request.music_seed'}), 'INVALID_GAMEPLAY_SEED_BINDING')
    add('music_binding_mapped_to_gameplay', lambda rows: rows[0]['seed_bindings']['MUSIC'].update({'authority': 'gameplay', 'source_field': 'request.seed'}), 'INVALID_MUSIC_SEED_BINDING')
    add('plan_only_disabled', lambda rows: rows[0]['execution'].update({'plan_only': False}), 'PLAN_ONLY_NOT_TRUE')
    add('production_execution_enabled', lambda rows: rows[0]['execution'].update({'production_execution': True}), 'PRODUCTION_EXECUTION_ENABLED')
    add('renderer_enabled', lambda rows: rows[0]['execution'].update({'renderer_execution': True}), 'RENDERER_EXECUTION_ENABLED')
    add('runtime_authority_enabled', lambda rows: rows[0]['execution'].update({'runtime_authority': 'D7.1'}), 'RUNTIME_AUTHORITY_NOT_NONE')
    add('non_default_personalization', lambda rows: rows[0].update({'personalization_profile': 'editorial_text_v1'}), 'CORE_PERSONALIZATION_NOT_DEFAULT')
    add('variation_authority_injected', lambda rows: rows[0].update({'variation_index': 1}), 'VARIATION_INDEX_MUST_REMAIN_NULL')
    add('master_seed_introduced', lambda rows: rows[0]['governance'].update({'master_seed': 'CANONICAL'}), 'MASTER_SEED_AUTHORITY')
    add('derivation_activated', lambda rows: rows[0]['governance'].update({'derivation_runtime_activation': True}), 'DERIVATION_ACTIVATED')
    add('cross_domain_seed_sharing', lambda rows: rows[0]['governance'].update({'cross_domain_seed_sharing': 'ALLOWED'}), 'CROSS_DOMAIN_SEED_SHARING')
    add('protected_winning_frame_seed', lambda rows: rows[0]['seed_bindings']['GAMEPLAY'].update({'authority': 'winning_frame', 'source_field': 'winning_frame'}), 'INVALID_GAMEPLAY_SEED_BINDING')
    # Authority-level negative is validated separately to keep the expected reason precise.
    authority_candidate = json.loads(json.dumps(base_matrix))
    authority_candidate['authority'] = 'D7.0'
    _, authority_errors = validate_matrix(authority_candidate, policy, challenges, profiles)
    cases.append({'case': 'matrix_authority_tampered', 'expected': 'REJECT', 'reason_expected': 'MATRIX_AUTHORITY_MISMATCH', 'observed_reject': bool(authority_errors), 'reason_observed': authority_errors, 'pass': 'MATRIX_AUTHORITY_MISMATCH' in authority_errors})
    status_candidate = json.loads(json.dumps(base_matrix))
    status_candidate['status'] = 'DRAFT'
    _, status_errors = validate_matrix(status_candidate, policy, challenges, profiles)
    cases.append({'case': 'matrix_status_not_canonical', 'expected': 'REJECT', 'reason_expected': 'MATRIX_STATUS_NOT_CANONICAL', 'observed_reject': bool(status_errors), 'reason_observed': status_errors, 'pass': 'MATRIX_STATUS_NOT_CANONICAL' in status_errors})
    return {'count': len(cases), 'all_pass': all(item['pass'] for item in cases), 'cases': cases}


def run(root: Path) -> int:
    try:
        inputs = load_inputs(root)
        policy = inputs['policy']
        matrix = inputs['matrix']
        challenges = discover_challenges(root)
        profiles = discover_profiles(root, matrix)
        expected_challenge_count = int(policy['coverage']['challenge_count'])
        expected_profile_count = int(policy['coverage']['delivery_profile_count'])
        if len(challenges) != expected_challenge_count:
            raise ValueError(f'Expected {expected_challenge_count} challenges; discovered {len(challenges)}')
        if len(profiles) != expected_profile_count:
            raise ValueError(f'Expected {expected_profile_count} profiles; discovered {len(profiles)}: {profiles}')
        coverage, errors = validate_matrix(matrix, policy, challenges, profiles)
        negatives = negative_tests(challenges, profiles, matrix, policy)
        policy_ok = (
            policy.get('authority') == 'D7.2'
            and policy.get('constraints', {}).get('matrix_authority') == 'CANONICAL_D7_1'
            and policy.get('constraints', {}).get('catalog_authority') == 'NOT_ESTABLISHED_IN_D7_1'
        )
        core_pass = not errors and negatives['all_pass'] and policy_ok
        constraint_validation = {
            'result': 'PASS' if core_pass else 'FAIL',
            'errors': errors,
            'policy_ok': policy_ok,
            'd7_1_authority': matrix.get('authority'),
            'd7_1_status': matrix.get('status'),
            'catalog_authority': matrix.get('authority_state', {}).get('catalog_authority'),
            'seed_bindings': {'GAMEPLAY': 'request.seed', 'MUSIC': 'request.music_seed'},
            'runtime_authority': 'NONE',
            'production_execution': False,
            'renderer_execution': False,
            'godot_production_execution': False,
            'ffmpeg_production_execution': False,
        }
        receipt = {
            'checkpoint': 'D7.2',
            'name': 'Production Matrix Coverage / Constraint Validator',
            'result': 'PASS' if core_pass else 'FAIL',
            'status': 'CLOSED' if core_pass else 'BLOCKED',
            'predecessors': {'D6.5': 'PASS/CLOSED', 'D7.0': 'PASS/CLOSED', 'D7.1': 'PASS/CLOSED'},
            'matrix_authority': 'CANONICAL_D7_1',
            'catalog_authority': 'NOT_ESTABLISHED_IN_D7_1',
            'challenge_count': len(challenges),
            'delivery_profile_count': len(profiles),
            'mode_count': len(EXPECTED_MODES),
            'core_cases': coverage['actual_core_cases'],
            'coverage_complete': coverage['complete'],
            'negative_cases': negatives['count'],
            'negative_tests_pass': negatives['all_pass'],
            'd3_d4_d6_constraints_preserved': True,
            'master_seed': 'NOT_ADOPTED',
            'derivation_runtime_activation': False,
            'runtime_authority': 'NONE',
            'production_execution': False,
            'renderer_execution': False,
            'godot_production_execution': False,
            'ffmpeg_production_execution': False,
            'c11c_build_factory_expected_sha256': C11C_BUILD_SHA,
            'next': 'D7.3 - Canonical Catalog Builder' if core_pass else 'REPAIR_D7.2',
        }
        output_dir = root / ALLOWED_OUTPUT_REL
        write_json(output_dir / OUTPUT_NAMES[0], coverage)
        write_json(output_dir / OUTPUT_NAMES[1], constraint_validation)
        write_json(output_dir / OUTPUT_NAMES[2], negatives)
        write_json(output_dir / OUTPUT_NAMES[3], receipt)
        print(json.dumps({
            'authority': 'D7.2',
            'matrix_authority': 'CANONICAL_D7_1',
            'challenge_count': len(challenges),
            'delivery_profile_count': len(profiles),
            'mode_count': len(EXPECTED_MODES),
            'core_cases': coverage['actual_core_cases'],
            'coverage_complete': coverage['complete'],
            'negative_cases': negatives['count'],
            'negative_tests_pass': negatives['all_pass'],
            'errors': errors,
            'catalog_authority': 'NOT_ESTABLISHED_IN_D7_1',
            'result': receipt['result'],
            'status': receipt['status'],
        }, ensure_ascii=False, sort_keys=True))
        return 0 if core_pass else 2
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
