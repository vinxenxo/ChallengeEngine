#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ALLOWED_OUTPUT_REL = Path('artifacts/tests/c11d_d7/d7_0')
D6_RECEIPT_REL = Path('artifacts/tests/c11d_d6/d6_5/d6_5_acceptance_receipt.json')
C11C_ZIP_SHA = 'D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32'
C11C_TREE_SHA = '2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256'
BUILD_FACTORY_SHA = '3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3'
OUTPUT_NAMES = (
    'd7_0_production_inventory.json',
    'd7_0_matrix_usage_audit.json',
    'd7_0_catalog_findings.json',
    'd7_0_audit_receipt.json',
)


def canon_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canon_bytes(obj))


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
    files.sort(key=lambda x: x[0])
    h = hashlib.sha256()
    for rel, size, digest in files:
        h.update(rel.encode('utf-8'))
        h.update(b'\0')
        h.update(str(size).encode('ascii'))
        h.update(b'\0')
        h.update(digest.encode('ascii'))
        h.update(b'\n')
    return {'files': len(files), 'sha256': h.hexdigest()}


def load_json(path: Path) -> dict[str, Any] | list[Any]:
    return json.loads(path.read_text(encoding='utf-8-sig'))


def find_first(root: Path, candidates: list[str]) -> Path | None:
    for rel in candidates:
        p = root / rel
        if p.is_file():
            return p
    return None


def extract_challenges(root: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for p in sorted((root / 'challenges').glob('CHALLENGE_*.json')):
        try:
            data = load_json(p)
        except Exception as exc:
            out.append({'path': p.relative_to(root).as_posix(), 'parse_error': str(exc)})
            continue
        if not isinstance(data, dict):
            out.append({'path': p.relative_to(root).as_posix(), 'type': type(data).__name__})
            continue
        cid = data.get('challenge_id') or p.stem
        out.append({
            'challenge_id': cid,
            'version': data.get('version'),
            'mechanic': data.get('mechanic') or data.get('mechanics') or data.get('type'),
            'family': data.get('family'),
            'path': p.relative_to(root).as_posix(),
            'has_seed_field': any(k in data for k in ('seed', 'gameplay_seed', 'music_seed')),
            'top_level_keys': sorted(str(k) for k in data.keys()),
        })
    return out


def discover_by_tokens(root: Path, tokens: tuple[str, ...], suffixes: tuple[str, ...] = ('.json', '.md', '.py', '.ps1')) -> list[str]:
    hits: list[str] = []
    for p in root.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in suffixes:
            continue
        rel = p.relative_to(root).as_posix()
        if rel == ALLOWED_OUTPUT_REL.as_posix() or rel.startswith(ALLOWED_OUTPUT_REL.as_posix().rstrip('/') + '/'):
            continue
        lower = rel.lower()
        if any(tok in lower for tok in tokens):
            hits.append(rel)
    return sorted(set(hits))


def read_d6_receipt(root: Path) -> tuple[dict[str, Any] | None, str | None]:
    p = root / D6_RECEIPT_REL
    if not p.is_file():
        return None, 'D6.5 acceptance receipt missing'
    try:
        data = load_json(p)
    except Exception as exc:
        return None, f'D6.5 acceptance receipt parse error: {exc}'
    if not isinstance(data, dict):
        return None, 'D6.5 acceptance receipt is not an object'
    if data.get('result') != 'PASS' or data.get('status') != 'CLOSED':
        return data, 'D6.5 must be PASS/CLOSED before D7.0'
    return data, None


def inspect_c11c_markers(root: Path) -> dict[str, Any]:
    build = find_first(root, ['tools/build_factory.py', 'build_factory.py'])
    build_sha = sha256_file(build) if build else None
    return {
        'expected_zip_sha256': C11C_ZIP_SHA,
        'expected_tree_sha256': C11C_TREE_SHA,
        'expected_build_factory_sha256': BUILD_FACTORY_SHA,
        'build_factory_present': build is not None,
        'build_factory_sha256': build_sha,
        'build_factory_matches_expected': build_sha == BUILD_FACTORY_SHA if build_sha else False,
        'frozen_identity_authoritative_from_d6_5': True,
    }


def classify_matrix_sources(paths: list[str]) -> dict[str, int]:
    counts = {'CANONICAL_CANDIDATE': 0, 'HISTORICAL': 0, 'AUDIT_EVIDENCE': 0, 'UNKNOWN': 0}
    for rel in paths:
        low = rel.lower()
        if 'artifacts/tests' in low:
            counts['AUDIT_EVIDENCE'] += 1
        elif any(x in low for x in ('old', 'legacy', 'historical', 'archive')):
            counts['HISTORICAL'] += 1
        elif any(x in low for x in ('production_matrix', 'production-matrix', 'catalog', 'matrix')):
            counts['CANONICAL_CANDIDATE'] += 1
        else:
            counts['UNKNOWN'] += 1
    return counts


def run_audit(root: Path) -> int:
    d6_receipt, d6_error = read_d6_receipt(root)
    if d6_error:
        print(json.dumps({'result': 'FAIL', 'status': 'BLOCKED', 'error': d6_error}, ensure_ascii=False, sort_keys=True))
        return 2

    challenges = extract_challenges(root)
    malformed_challenges = sum(1 for x in challenges if 'parse_error' in x)

    production_tokens = discover_by_tokens(root, ('production', 'matrix', 'catalog', 'content_matrix', 'release_matrix'))
    catalog_tokens = discover_by_tokens(root, ('catalog', 'content_catalog', 'production_catalog'))
    profile_candidates = discover_by_tokens(root, ('delivery_profile', 'profile_registry', 'production_profile', 'delivery'))
    request_candidates = discover_by_tokens(root, ('production_request', 'canonical_production_orchestrator', 'production_cli', 'gui_production_adapter'))
    provenance_candidates = discover_by_tokens(root, ('provenance', 'lineage', 'artifact_manifest'))

    d4_schema = find_first(root, ['definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json'])
    d6_registry = find_first(root, ['definitions/c11d/seeds/C11D_SEED_REGISTRY_V1.json'])
    d6_policy = find_first(root, ['definitions/c11d/seeds/C11D_SEED_GOVERNANCE_POLICY_V1.json'])
    d4_orchestrator = find_first(root, ['tools/c11d/d4/canonical_production_orchestrator.py'])

    governance_findings = []
    if malformed_challenges:
        governance_findings.append({'severity': 'BLOCKING', 'code': 'CHALLENGE_PARSE_FAILURE', 'count': malformed_challenges})
    if not d4_schema:
        governance_findings.append({'severity': 'BLOCKING', 'code': 'D4_REQUEST_SCHEMA_MISSING'})
    if not d6_registry or not d6_policy:
        governance_findings.append({'severity': 'BLOCKING', 'code': 'D6_SEED_GOVERNANCE_MISSING'})
    if not d4_orchestrator:
        governance_findings.append({'severity': 'WARNING', 'code': 'D4_ORCHESTRATOR_NOT_FOUND_IN_EXPECTED_PATH'})
    if production_tokens:
        governance_findings.append({'severity': 'INFO', 'code': 'EXISTING_PRODUCTION_ARTIFACTS_DISCOVERED', 'count': len(production_tokens)})
    if catalog_tokens:
        governance_findings.append({'severity': 'INFO', 'code': 'EXISTING_CATALOG_ARTIFACTS_DISCOVERED', 'count': len(catalog_tokens)})

    matrix_candidates = [p for p in production_tokens if any(x in p.lower() for x in ('matrix', 'catalog'))]
    matrix_classification = classify_matrix_sources(matrix_candidates)

    challenge_families: dict[str, int] = {}
    mechanics: dict[str, int] = {}
    versions: dict[str, int] = {}
    for item in challenges:
        fam = str(item.get('family') or 'UNKNOWN')
        challenge_families[fam] = challenge_families.get(fam, 0) + 1
        mech = str(item.get('mechanic') or 'UNKNOWN')
        mechanics[mech] = mechanics.get(mech, 0) + 1
        ver = str(item.get('version') or 'UNKNOWN')
        versions[ver] = versions.get(ver, 0) + 1

    source_inventory = {
        'challenges': challenges,
        'challenge_count': len(challenges),
        'challenge_family_counts': dict(sorted(challenge_families.items())),
        'mechanic_counts': dict(sorted(mechanics.items())),
        'version_counts': dict(sorted(versions.items())),
        'production_related_paths': production_tokens,
        'catalog_related_paths': catalog_tokens,
        'delivery_profile_related_paths': profile_candidates,
        'request_orchestrator_related_paths': request_candidates,
        'provenance_related_paths': provenance_candidates,
        'canonical_request_schema_present': d4_schema is not None,
        'canonical_seed_registry_present': d6_registry is not None,
        'canonical_seed_policy_present': d6_policy is not None,
        'd4_orchestrator_present': d4_orchestrator is not None,
    }

    usage_matrix = {
        'matrix_authority': 'NOT_ESTABLISHED_IN_D7_0',
        'catalog_authority': 'NOT_ESTABLISHED_IN_D7_0',
        'existing_matrix_source_classification': matrix_classification,
        'challenge_inventory_count': len(challenges),
        'production_profile_inventory_paths': len(profile_candidates),
        'request_orchestrator_paths': len(request_candidates),
        'provenance_paths': len(provenance_candidates),
        'd6_5_result': d6_receipt.get('result'),
        'd6_5_status': d6_receipt.get('status'),
        'runtime_authority': 'NONE',
        'production_execution': False,
        'renderer_execution': False,
    }

    c11c = inspect_c11c_markers(root)
    findings = {
        'findings': governance_findings,
        'blocking_findings': sum(1 for x in governance_findings if x.get('severity') == 'BLOCKING'),
        'warning_findings': sum(1 for x in governance_findings if x.get('severity') == 'WARNING'),
        'info_findings': sum(1 for x in governance_findings if x.get('severity') == 'INFO'),
        'orchestration_activation': 'DISABLED',
        'catalog_promotion': 'DISABLED',
        'matrix_promotion': 'DISABLED',
        'unknowns_must_be_preserved': True,
    }

    receipt = {
        'checkpoint': 'D7.0',
        'name': 'Production Matrix & Catalog Audit',
        'result': 'PASS' if findings['blocking_findings'] == 0 else 'FAIL',
        'status': 'CLOSED' if findings['blocking_findings'] == 0 else 'BLOCKED',
        'd6_5_predecessor': 'PASS/CLOSED',
        'challenge_count': len(challenges),
        'production_related_paths': len(production_tokens),
        'catalog_related_paths': len(catalog_tokens),
        'matrix_authority': 'NOT_ESTABLISHED_IN_D7_0',
        'catalog_authority': 'NOT_ESTABLISHED_IN_D7_0',
        'runtime_authority': 'NONE',
        'production_execution': False,
        'renderer_execution': False,
        'godot_production_execution': False,
        'ffmpeg_production_execution': False,
        'c11c_frozen_identity': c11c,
        'mutation_guard': 'RUNNER_ENFORCED',
        'deterministic': True,
        'idempotent': True,
        'next': 'D7.1 - Canonical Production Matrix' if findings['blocking_findings'] == 0 else 'REPAIR_D7.0',
    }

    out = root / ALLOWED_OUTPUT_REL
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / OUTPUT_NAMES[0], source_inventory)
    write_json(out / OUTPUT_NAMES[1], usage_matrix)
    write_json(out / OUTPUT_NAMES[2], findings)
    write_json(out / OUTPUT_NAMES[3], receipt)

    print(json.dumps({
        'challenge_count': len(challenges),
        'production_paths': len(production_tokens),
        'catalog_paths': len(catalog_tokens),
        'blocking_findings': findings['blocking_findings'],
        'matrix_authority': 'NOT_ESTABLISHED_IN_D7_0',
        'catalog_authority': 'NOT_ESTABLISHED_IN_D7_0',
        'frozen': True,
        'result': receipt['result'],
        'status': receipt['status'],
    }, ensure_ascii=False, sort_keys=True))
    return 0 if receipt['result'] == 'PASS' else 2


def snapshot_only(root: Path) -> int:
    print(json.dumps(repo_snapshot(root), sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--snapshot-only', action='store_true')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print('Repository root does not exist.', file=sys.stderr)
        return 2
    return snapshot_only(root) if args.snapshot_only else run_audit(root)


if __name__ == '__main__':
    raise SystemExit(main())
