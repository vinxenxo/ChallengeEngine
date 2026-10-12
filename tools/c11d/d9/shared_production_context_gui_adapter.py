"""D-owned GUI integration seam for the shared D9 production-context backend.

Accepts a canonical D9.9 raw request already assembled from GUI controls and
routes it through the single shared production-context facade. It deliberately
does not duplicate selection/editorial resolution and never dispatches rendering.
The frozen C11-C Producer GUI is not patched by this module; a future D GUI can
call this stable adapter directly.
"""
from __future__ import annotations
from collections.abc import Mapping
from pathlib import Path
import json, re, sys
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from shared_production_context_service import (
    SharedProductionContextError,
    canonical_json,
    prepare_shared_production_context,
    validate_shared_production_context,
    validate_service_contract,
)

GUI_CONTRACT_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_ADAPTER_CONTRACT_V1.json')
GUI_CONTRACT_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_ADAPTER_CONTRACT_SCHEMA_V1.json')
MANIFEST_SHA256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
GUI_CONTRACT_SCHEMA = 'C11-D-D9-SHARED-PRODUCTION-CONTEXT-GUI-ADAPTER-CONTRACT-V1'

class SharedProductionContextGUIAdapterError(ValueError):
    """Raised when a GUI request cannot be safely bound to the shared backend."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT

def _read_json(root: Path, relative: Path) -> dict[str, Any]:
    try:
        value = json.loads((root / relative).read_text(encoding='utf-8-sig'))
    except Exception as exc:
        raise SharedProductionContextGUIAdapterError(f'Cannot read {relative.as_posix()}: {exc}') from exc
    if not isinstance(value, dict):
        raise SharedProductionContextGUIAdapterError(f'Expected JSON object: {relative.as_posix()}')
    return value

def _sha(root: Path, relative: str) -> str:
    try:
        return __import__('hashlib').sha256((root / relative).read_bytes()).hexdigest()
    except Exception as exc:
        raise SharedProductionContextGUIAdapterError(f'Cannot hash GUI adapter source pin {relative}: {exc}') from exc

def audit_gui_adapter(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    try:
        parent_state = validate_service_contract(root)
    except Exception as exc:
        raise SharedProductionContextGUIAdapterError(f'Parent shared backend contract failed: {exc}') from exc
    contract = _read_json(root, GUI_CONTRACT_REL)
    schema = _read_json(root, GUI_CONTRACT_SCHEMA_REL)
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(contract), key=lambda e: (list(map(str, e.path)), e.message))
    except Exception as exc:
        raise SharedProductionContextGUIAdapterError(f'Invalid GUI adapter contract schema: {exc}') from exc
    if errors:
        raise SharedProductionContextGUIAdapterError(f'GUI adapter contract schema violation: {errors[0].message}')
    if contract.get('schema') != GUI_CONTRACT_SCHEMA or contract.get('schema_version') != '1.0':
        raise SharedProductionContextGUIAdapterError('GUI adapter contract identity mismatch')
    if contract.get('status') != 'PREPARE_ONLY_FUTURE_GUI_ADAPTER_EXISTING_GUI_SOURCE_UNMODIFIED_BY_OVERLAY':
        raise SharedProductionContextGUIAdapterError('GUI adapter must remain D-owned and prepare-only')
    pins = contract.get('source_lineage')
    if not isinstance(pins, list) or len(pins) != 8 or pins[0].get('path') != 'release/C11C_FREEZE_PACKAGE_MANIFEST.json' or pins[0].get('sha256') != MANIFEST_SHA256:
        raise SharedProductionContextGUIAdapterError('Frozen C11-C manifest must lead GUI adapter lineage')
    seen: set[str] = set()
    for row in pins:
        if not isinstance(row, Mapping) or set(row) != {'path','role','sha256'}:
            raise SharedProductionContextGUIAdapterError('Malformed GUI adapter source-lineage row')
        rel, digest = str(row['path']), str(row['sha256'])
        path = Path(rel)
        if path.is_absolute() or '..' in path.parts or '\\' in rel or rel in seen:
            raise SharedProductionContextGUIAdapterError(f'Unsafe or duplicate GUI source pin: {rel}')
        if not re.fullmatch(r'[a-f0-9]{64}', digest):
            raise SharedProductionContextGUIAdapterError(f'Invalid GUI source SHA-256: {rel}')
        if _sha(root, rel) != digest:
            raise SharedProductionContextGUIAdapterError(f'Pinned GUI source drift: {rel}')
        seen.add(rel)
    expected_adapter_hash = contract.get('adapter_sha256')
    if _sha(root, 'tools/c11d/d9/shared_production_context_gui_adapter.py') != expected_adapter_hash:
        raise SharedProductionContextGUIAdapterError('GUI adapter implementation hash drift')
    source_pin = next((x for x in pins if x['path'] == 'c11c-suite/c11c-producer/main.py'), None)
    if source_pin is None:
        raise SharedProductionContextGUIAdapterError('Active Producer GUI source pin missing')
    return {
        'source_pins': len(pins),
        'parent_source_pins': parent_state['lineage_count'],
        'supported_content_types': 3,
        'existing_gui_source_modified_by_overlay': False,
        'renderer': False,
        'media_created': False,
        'release_authority': 'NONE',
    }

def prepare_gui_shared_context(raw_request: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    """Prepare GUI-submitted D9.9 request through the canonical shared facade.

    GUI controls must submit the canonical raw-request vocabulary. This adapter
    only enforces GUI origin and delegates; it does not resolve editorial fields,
    presentation profiles, family selectors, seeds, or production plans itself.
    The return value is exactly the shared facade record, enabling strict CLI parity.
    """
    if not isinstance(raw_request, Mapping):
        raise SharedProductionContextGUIAdapterError('GUI request must be a JSON object/mapping')
    provenance = raw_request.get('provenance')
    if not isinstance(provenance, Mapping) or provenance.get('request_origin') != 'GUI':
        raise SharedProductionContextGUIAdapterError("GUI request provenance.request_origin must equal 'GUI'")
    root = _root(project_root)
    audit_gui_adapter(root)
    before = canonical_json(raw_request)
    try:
        record = prepare_shared_production_context(raw_request, root)
        validate_shared_production_context(record, raw_request, root)
    except Exception as exc:
        raise SharedProductionContextGUIAdapterError(f'Shared GUI context preparation failed: {exc}') from exc
    if canonical_json(raw_request) != before:
        raise SharedProductionContextGUIAdapterError('GUI raw request was mutated by the adapter')
    canonical = record.get('canonical_result', {}).get('canonical_request', {})
    if canonical.get('request_id') != raw_request.get('request_id'):
        raise SharedProductionContextGUIAdapterError('Canonical request identity diverges from GUI request')
    if record.get('execution_boundary', {}).get('renderer_native_input_emitted') is not False or record.get('execution_boundary', {}).get('renderer_activation') is not False or record.get('execution_boundary', {}).get('media_created') is not False or record.get('execution_boundary', {}).get('release_authority') != 'NONE':
        raise SharedProductionContextGUIAdapterError('GUI adapter detected execution-boundary escalation')
    return record

def validate_gui_shared_context(record: Mapping[str, Any], raw_request: Mapping[str, Any], project_root: Path | str | None = None) -> bool:
    expected = prepare_gui_shared_context(raw_request, project_root)
    if not isinstance(record, Mapping) or dict(record) != expected:
        raise SharedProductionContextGUIAdapterError('GUI shared-context record differs from canonical recomputation')
    return True
