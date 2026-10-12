"""C11-D shared backend facade for future GUI and CLI callers.

Pure preparation only: canonical D9.9 -> D9.10 bridge -> D-only adapter ->
shared editorial/presentation context binding. No render dispatch, production,
media creation, or result persistence occurs here.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from universal_producer import evaluate_universal_request
from editorial_render_bridge import build_bridge_planning_record, sha256 as bridge_sha256
from d_render_adapter import prepare_d_only_adapter_envelope, validate_d_only_adapter_envelope
from d_renderer_shared_editorial_presentation_context_binding import (
    build_context_binding_from_result, validate_binding_record,
    SharedContextBindingError, canonical_json as shared_canonical_json,
)

CONTRACT_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_V1.json')
CONTRACT_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_CONTRACT_SCHEMA_V1.json')
OUTPUT_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_FACADE_SCHEMA_V1.json')
MANIFEST_SHA256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
SERVICE_SCHEMA = 'C11-D-D9-SHARED-PRODUCTION-CONTEXT-FACADE-V1'
CONTRACT_SCHEMA = 'C11-D-D9-SHARED-PRODUCTION-CONTEXT-FACADE-CONTRACT-V1'
SUPPORTED = ('challenges', 'visual_loops', 'visual_drills')

class SharedProductionContextError(ValueError):
    """Raised when the canonical shared backend context cannot be safely prepared."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT

def _read_json(root: Path, rel: Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding='utf-8-sig'))
    except Exception as exc:
        raise SharedProductionContextError(f'Cannot read {rel.as_posix()}: {exc}') from exc
    if not isinstance(value, dict):
        raise SharedProductionContextError(f'Expected JSON object: {rel.as_posix()}')
    return value

def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [_canonical(v) for v in value]
    return value

def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(',', ':'), allow_nan=False)

def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode('utf-8')).hexdigest()

def _file_sha(root: Path, rel: str) -> str:
    try:
        return hashlib.sha256((root / rel).read_bytes()).hexdigest()
    except Exception as exc:
        raise SharedProductionContextError(f'Cannot hash source pin {rel}: {exc}') from exc

def _validate_schema(instance: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(instance), key=lambda e: (list(map(str, e.path)), e.message))
    except ImportError as exc:
        raise SharedProductionContextError('jsonschema is required for strict shared backend validation') from exc
    except Exception as exc:
        raise SharedProductionContextError(f'Invalid {label} schema: {exc}') from exc
    if errors:
        raise SharedProductionContextError(f'{label} schema violation: {errors[0].message}')

def validate_service_contract(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract = _read_json(root, CONTRACT_REL)
    contract_schema = _read_json(root, CONTRACT_SCHEMA_REL)
    output_schema = _read_json(root, OUTPUT_SCHEMA_REL)
    if contract.get('schema') != CONTRACT_SCHEMA or contract.get('schema_version') != '1.0':
        raise SharedProductionContextError('Shared backend facade contract identity mismatch')
    if contract.get('status') != 'PREPARE_ONLY_COMMON_BACKEND_FACADE_NOT_RENDERER_INPUT':
        raise SharedProductionContextError('Shared backend facade must remain preparation-only')
    gates = contract.get('governance', {})
    expected_gates = {'renderer_activation': False, 'production_execution': False, 'media_created': False, 'c11c_source_mutation': False, 'd4_8': 'BLOCKED', 'release_authority': 'NONE', 'd9_17': 'BLOCKED_NO_GO', 'd10': 'BLOCKED'}
    if gates != expected_gates:
        raise SharedProductionContextError('Shared backend facade governance locks drift')
    lineage = contract.get('source_lineage')
    if not isinstance(lineage, list) or len(lineage) < 22 or not lineage or lineage[0].get('path') != 'release/C11C_FREEZE_PACKAGE_MANIFEST.json' or lineage[0].get('sha256') != MANIFEST_SHA256:
        raise SharedProductionContextError('Frozen C11-C manifest must lead shared backend source lineage')
    seen: set[str] = set()
    for row in lineage:
        if not isinstance(row, Mapping) or set(row) != {'path','role','sha256'}:
            raise SharedProductionContextError('Malformed shared backend source lineage row')
        rel, digest = str(row['path']), str(row['sha256'])
        posix = PurePosixPath(rel)
        if posix.is_absolute() or '..' in posix.parts or '\\' in rel or rel in seen:
            raise SharedProductionContextError(f'Unsafe or duplicate source pin: {rel}')
        if not re.fullmatch(r'[a-f0-9]{64}', digest):
            raise SharedProductionContextError(f'Invalid source SHA-256: {rel}')
        if _file_sha(root, rel) != digest:
            raise SharedProductionContextError(f'Pinned source drift: {rel}')
        seen.add(rel)
    _validate_schema(contract, contract_schema, 'Shared backend facade contract')
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(output_schema)
    except Exception as exc:
        raise SharedProductionContextError(f'Invalid shared backend output schema: {exc}') from exc
    return {'root':root,'contract':contract,'contract_schema':contract_schema,'output_schema':output_schema,'lineage_count':len(lineage)}

def _assert_component_identity(result: Mapping[str, Any], bridge: Mapping[str, Any], adapter: Mapping[str, Any], context: Mapping[str, Any]) -> None:
    request = result.get('canonical_request', {})
    plan = result.get('plan', {})
    if result.get('status') != 'PLANNED':
        raise SharedProductionContextError('Canonical D9.9 result must be PLANNED')
    if request.get('selection') != plan.get('selection') or request.get('presentation_profile_id') != plan.get('presentation_profile_id'):
        raise SharedProductionContextError('Canonical request/plan identity divergence')
    expected = {
        'request_hash': result.get('request_hash'),
        'editorial_hash': result.get('editorial_hash'),
        'plan_hash': result.get('plan_hash'),
    }
    for field, value in expected.items():
        if bridge.get('identity', {}).get(field) != value:
            raise SharedProductionContextError(f'D9.10 bridge identity mismatch: {field}')
    if adapter.get('source_identity', {}).get('request_hash') != expected['request_hash'] or adapter.get('source_identity', {}).get('editorial_hash') != expected['editorial_hash'] or adapter.get('source_identity', {}).get('plan_hash') != expected['plan_hash']:
        raise SharedProductionContextError('D-only adapter identity differs from canonical D9.9 result')
    ci = context.get('identity', {})
    if ci.get('request_sha256') != expected['request_hash'] or ci.get('editorial_sha256') != expected['editorial_hash'] or ci.get('plan_sha256') != expected['plan_hash']:
        raise SharedProductionContextError('Shared editorial/presentation binding identity differs from canonical D9.9 result')
    pid = request.get('presentation_profile_id')
    if not pid or plan.get('presentation_profile_id') != pid or bridge.get('presentation_profile_id') != pid or adapter.get('binding_preview', {}).get('presentation_profile_id') != pid or context.get('presentation_binding', {}).get('profile_id') != pid:
        raise SharedProductionContextError('Presentation profile reference diverges across shared context components')
    editorial = plan.get('editorial')
    if adapter.get('binding_preview', {}).get('editorial_bindings') != editorial or context.get('editorial_binding', {}).get('resolved_values') != editorial:
        raise SharedProductionContextError('Editorial payload differs across canonical D9 context components')
    if adapter.get('envelope_hash') != sha256({k:v for k,v in adapter.items() if k != 'envelope_hash'}):
        raise SharedProductionContextError('D-only adapter envelope self-hash mismatch')
    if bridge.get('record_hash') != sha256({k:v for k,v in bridge.items() if k != 'record_hash'}):
        raise SharedProductionContextError('D9.10 bridge record self-hash mismatch')
    boundaries = [
        result.get('renderer') is False, result.get('execution') is False,
        plan.get('renderer_activation') is False, plan.get('production_execution') is False,
        result.get('release_authority') == 'NONE', plan.get('release_authority') == 'NONE', plan.get('d4_8') == 'BLOCKED',
        adapter.get('renderer_dispatch_invoked') is False, adapter.get('renderer_activation') is False,
        adapter.get('renderer_input_emitted') is False, adapter.get('production_execution') is False,
        adapter.get('media_output_created') is False, adapter.get('d4_8') == 'BLOCKED', adapter.get('release_authority') == 'NONE',
        context.get('execution_boundary', {}).get('renderer_native_input_emitted') is False,
        context.get('execution_boundary', {}).get('renderer_activation') is False,
        context.get('execution_boundary', {}).get('media_created') is False,
        context.get('execution_boundary', {}).get('d4_8') == 'BLOCKED',
        context.get('execution_boundary', {}).get('release_authority') == 'NONE',
    ]
    if not all(boundaries):
        raise SharedProductionContextError('Renderer/production/governance boundary escalation detected')

def prepare_shared_production_context(raw_request: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    """Shared API for GUI and CLI; returns a deterministic in-memory context record."""
    state = validate_service_contract(project_root)
    root = state['root']
    if not isinstance(raw_request, Mapping):
        raise SharedProductionContextError('Request must be a JSON object/mapping')
    try:
        result = evaluate_universal_request(raw_request, root)
        if result.get('status') != 'PLANNED':
            raise SharedProductionContextError('Canonical D9.9 request was not planned')
        bridge = build_bridge_planning_record(result, root)
        adapter = prepare_d_only_adapter_envelope(result, bridge, root)
        validate_d_only_adapter_envelope(adapter, root)
        context = build_context_binding_from_result(result, root)
        validate_binding_record(context, result, root)
    except SharedProductionContextError:
        raise
    except Exception as exc:
        raise SharedProductionContextError(f'Canonical shared-context preparation failed: {exc}') from exc
    _assert_component_identity(result, bridge, adapter, context)
    identity = {
        'request_id': result['canonical_request']['request_id'],
        'content_type': result['plan']['selection']['content_type'],
        'selection': _canonical(result['plan']['selection']),
        'request_sha256': result['request_hash'],
        'editorial_sha256': result['editorial_hash'],
        'plan_sha256': result['plan_hash'],
        'canonical_result_sha256': sha256(result),
        'bridge_record_sha256': bridge['record_hash'],
        'adapter_envelope_sha256': adapter['envelope_hash'],
        'shared_context_binding_sha256': context['record_sha256'],
    }
    record = {
        'schema': SERVICE_SCHEMA,
        'schema_version': '1.0',
        'status': 'PREPARED_COMMON_BACKEND_CONTEXT_NOT_RENDERER_INPUT',
        'identity': identity,
        'canonical_result': _canonical(result),
        'bridge_planning_record': _canonical(bridge),
        'd_only_adapter_envelope': _canonical(adapter),
        'shared_context_binding': _canonical(context),
        'source_contracts': {
            'service_contract_sha256': sha256(state['contract']),
            'canonical_request_contract_sha256': _file_sha(root, 'definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json'),
            'bridge_contract_sha256': _file_sha(root, 'definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json'),
            'adapter_contract_sha256': _file_sha(root, 'definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json'),
            'shared_context_contract_sha256': _file_sha(root, 'definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_CONTEXT_BINDING_CONTRACT_V1.json'),
        },
        'execution_boundary': {
            'mode': 'IN_MEMORY_SHARED_BACKEND_FACADE_ONLY', 'record_persisted': False,
            'renderer_native_input_emitted': False, 'renderer_dispatch_invoked': False,
            'renderer_activation': False, 'production_execution': False, 'media_created': False,
            'c11c_source_mutation': False, 'candidate_input_admissible': False,
            'd4_8': 'BLOCKED', 'release_authority': 'NONE', 'd9_17': 'BLOCKED_NO_GO', 'd10': 'BLOCKED',
        },
    }
    context_hash = sha256(record)
    record['context_sha256'] = context_hash
    record['record_sha256'] = sha256(record)
    _validate_schema(record, state['output_schema'], 'Shared production context facade record')
    return record

def validate_shared_production_context(record: Mapping[str, Any], raw_request: Mapping[str, Any], project_root: Path | str | None = None) -> bool:
    if not isinstance(record, Mapping):
        raise SharedProductionContextError('Shared production context facade record must be an object')
    expected = prepare_shared_production_context(raw_request, project_root)
    if dict(record) != expected:
        raise SharedProductionContextError('Shared backend record differs from canonical recomputation')
    return True

def audit(project_root: Path | str | None = None) -> dict[str, Any]:
    state = validate_service_contract(project_root)
    return {'source_pins':state['lineage_count'],'supported_content_types':len(state['contract']['supported_content_types']),'composition_stages':len(state['contract']['composition_order']),'cli_gui_backend':'ONE_SHARED_API','result_persistence':'NONE'}

def _write_stdout(text: str) -> None:
    data = text.encode('ascii')
    binary = getattr(sys.stdout, 'buffer', None)
    if binary is not None:
        binary.write(data); binary.flush()
    else:
        sys.stdout.write(text); sys.stdout.flush()

def main() -> int:
    parser = argparse.ArgumentParser(description='C11-D shared GUI/CLI backend facade; no render dispatch or result persistence')
    parser.add_argument('--project-root', type=Path, default=None)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--request', type=Path, help='Read-only canonical D9.9 request JSON')
    group.add_argument('--audit-only', action='store_true', help='Audit pinned sources and governance only')
    args = parser.parse_args()
    try:
        if args.audit_only:
            counts = audit(args.project_root)
            line = ('C11-D SHARED BACKEND FACADE AUDIT PASS | '
                    f"source_pins={counts['source_pins']}/{counts['source_pins']} | supported_content_types={counts['supported_content_types']}/3 | "
                    f"composition_stages={counts['composition_stages']}/6 | cli_gui_backend={counts['cli_gui_backend']} | "
                    f"result_persistence={counts['result_persistence']} | renderer_input=NOT_EMITTED | renderer=OFF | "
                    'media_created=false | D4.8=BLOCKED | release_authority=NONE\n')
            _write_stdout(line.encode('ascii').decode('ascii'))
            return 0
        raw = json.loads(args.request.read_text(encoding='utf-8-sig'))
        record = prepare_shared_production_context(raw, args.project_root)
        # ASCII-safe JSON keeps the stdout protocol independent of Windows code pages.
        payload = json.dumps(record, ensure_ascii=True, indent=2, sort_keys=True) + '\n'
        _write_stdout(payload)
        return 0
    except Exception as exc:
        message = f'C11-D SHARED BACKEND FACADE FAIL | {exc} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE\n'
        _write_stdout(message.encode('ascii', errors='backslashreplace').decode('ascii'))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
