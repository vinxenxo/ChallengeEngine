"""Map future GUI control state to the one canonical D9.9 request vocabulary.

This is a D-owned state adapter, not a GUI implementation. It performs only
structural/state mapping and then delegates semantic validation and context
resolution to the shared GUI adapter / production-context facade.
"""
from __future__ import annotations
from collections.abc import Mapping
from pathlib import Path
import hashlib, json, re, sys
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from universal_producer import REQUEST_SCHEMA_ID
from shared_production_context_gui_adapter import (
    SharedProductionContextGUIAdapterError,
    audit_gui_adapter,
    prepare_gui_shared_context,
)

STATE_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_SCHEMA_V1.json')
STATE_CONTRACT_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_CONTRACT_V1.json')
STATE_CONTRACT_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_CONTRACT_SCHEMA_V1.json')
MANIFEST_SHA256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
STATE_SCHEMA_ID = 'C11-D-SHARED-GUI-PRODUCTION-STATE-V1'
STATE_CONTRACT_ID = 'C11-D-D9-SHARED-PRODUCTION-CONTEXT-GUI-STATE-CONTRACT-V1'
SHARED_EDITORIAL_FIELDS = frozenset({'title', 'subtitle', 'call_to_action', 'language'})
CHALLENGE_ONLY_FIELDS = frozenset({'player_name', 'challenge_label'})
ALL_EDITORIAL_FIELDS = SHARED_EDITORIAL_FIELDS | CHALLENGE_ONLY_FIELDS

class SharedProductionGUIStateError(ValueError):
    """Invalid future-GUI state or failed canonical binding."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT

def _read_json(root: Path, rel: Path) -> dict[str, Any]:
    try:
        result = json.loads((root / rel).read_text(encoding='utf-8-sig'))
    except Exception as exc:
        raise SharedProductionGUIStateError(f'Cannot read {rel.as_posix()}: {exc}') from exc
    if not isinstance(result, dict):
        raise SharedProductionGUIStateError(f'Expected JSON object: {rel.as_posix()}')
    return result

def _sha(root: Path, rel: str) -> str:
    try:
        return hashlib.sha256((root / rel).read_bytes()).hexdigest()
    except Exception as exc:
        raise SharedProductionGUIStateError(f'Cannot hash pinned source {rel}: {exc}') from exc

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

def audit_gui_state_contract(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    try:
        parent = audit_gui_adapter(root)
    except Exception as exc:
        raise SharedProductionGUIStateError(f'Parent GUI adapter contract failed: {exc}') from exc
    contract = _read_json(root, STATE_CONTRACT_REL)
    contract_schema = _read_json(root, STATE_CONTRACT_SCHEMA_REL)
    state_schema = _read_json(root, STATE_SCHEMA_REL)
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(contract_schema)
        jsonschema.Draft202012Validator.check_schema(state_schema)
        errors = sorted(jsonschema.Draft202012Validator(contract_schema).iter_errors(contract), key=lambda e: (list(map(str,e.path)),e.message))
    except Exception as exc:
        raise SharedProductionGUIStateError(f'GUI state schema/contract invalid: {exc}') from exc
    if errors:
        raise SharedProductionGUIStateError(f'GUI state contract schema violation: {errors[0].message}')
    if contract.get('schema') != STATE_CONTRACT_ID or contract.get('schema_version') != '1.0':
        raise SharedProductionGUIStateError('GUI state contract identity mismatch')
    if contract.get('status') != 'PREPARE_ONLY_CANONICAL_UI_STATE_MAPPING_NO_GUI_SOURCE_MODIFICATION':
        raise SharedProductionGUIStateError('GUI state contract must remain prepare-only')
    if _sha(root, STATE_SCHEMA_REL.as_posix()) != contract.get('state_schema_sha256'):
        raise SharedProductionGUIStateError('GUI state schema hash drift')
    if _sha(root, 'tools/c11d/d9/shared_production_context_gui_state.py') != contract.get('implementation_sha256'):
        raise SharedProductionGUIStateError('GUI state implementation hash drift')
    lineage = contract.get('source_lineage')
    if not isinstance(lineage, list) or len(lineage) != 14:
        raise SharedProductionGUIStateError('GUI state lineage must contain exactly fourteen source pins')
    if lineage[0].get('path') != 'release/C11C_FREEZE_PACKAGE_MANIFEST.json' or lineage[0].get('sha256') != MANIFEST_SHA256:
        raise SharedProductionGUIStateError('Frozen C11-C manifest must lead GUI state lineage')
    seen: set[str] = set()
    for row in lineage:
        if not isinstance(row, Mapping) or set(row) != {'path','role','sha256'}:
            raise SharedProductionGUIStateError('Malformed GUI state source lineage row')
        rel, digest = str(row['path']), str(row['sha256'])
        p = Path(rel)
        if p.is_absolute() or '..' in p.parts or '\\' in rel or rel in seen:
            raise SharedProductionGUIStateError(f'Unsafe or duplicate GUI state source pin: {rel}')
        if not re.fullmatch(r'[a-f0-9]{64}',digest):
            raise SharedProductionGUIStateError(f'Invalid source SHA-256: {rel}')
        if _sha(root,rel) != digest:
            raise SharedProductionGUIStateError(f'Pinned GUI state source drift: {rel}')
        seen.add(rel)
    return {'source_pins':len(lineage),'parent_source_pins':parent['source_pins'],'state_schema_sha256':contract['state_schema_sha256'],'renderer':False,'media_created':False,'release_authority':'NONE'}

def validate_gui_state(state: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    if not isinstance(state, Mapping):
        raise SharedProductionGUIStateError('GUI state must be an object/mapping')
    root = _root(project_root)
    audit_gui_state_contract(root)
    schema = _read_json(root, STATE_SCHEMA_REL)
    try:
        import jsonschema
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(dict(state)), key=lambda e: (list(map(str,e.path)),e.message))
    except Exception as exc:
        raise SharedProductionGUIStateError(f'Cannot validate GUI state: {exc}') from exc
    if errors:
        raise SharedProductionGUIStateError(f'GUI state schema violation at {list(errors[0].path)}: {errors[0].message}')
    selection = state['selection']
    content_type = selection['content_type']
    selector_count = int('subtype_id' in selection) + int('variant_id' in selection)
    if selector_count != 1:
        raise SharedProductionGUIStateError('GUI state must select exactly one subtype_id or variant_id')
    if content_type == 'visual_loops' and 'subtype_id' not in selection:
        raise SharedProductionGUIStateError('Visual Loops require an explicit subtype_id/grammar selector')
    if content_type != 'visual_loops' and 'variant_id' not in selection:
        raise SharedProductionGUIStateError(f'{content_type} requires an explicit variant_id selector')
    editorial = state['editorial']
    profile = editorial['profile']
    overrides = editorial['overrides']
    if not isinstance(profile, Mapping) or not isinstance(overrides, Mapping):
        raise SharedProductionGUIStateError('editorial.profile and editorial.overrides must be objects')
    unknown = set(overrides) - ALL_EDITORIAL_FIELDS
    if unknown:
        raise SharedProductionGUIStateError('Unsupported GUI editorial override field(s): ' + ', '.join(sorted(unknown)))
    challenge_fields = set(overrides) & CHALLENGE_ONLY_FIELDS
    if content_type != 'challenges' and challenge_fields:
        raise SharedProductionGUIStateError('Challenge-only editorial fields are not valid for this content type: ' + ', '.join(sorted(challenge_fields)))
    for key, value in overrides.items():
        if not isinstance(value, str):
            raise SharedProductionGUIStateError(f'Editorial override {key} must be a string')
    production = state['production']
    if not production['personalization_enabled'] and (profile or overrides):
        raise SharedProductionGUIStateError('Disabled personalization cannot carry editorial profile or override values')
    # Ensure the UI state remains immutable as it crosses the adapter boundary.
    before = canonical_json(state)
    raw = {
        'schema': REQUEST_SCHEMA_ID,
        'schema_version': '1.0',
        'request_id': state['request_id'],
        'mode': state['mode'],
        'selection': dict(selection),
        'seed': production['seed'],
        'music_seed': production['music_seed'],
        'delivery_profile_id': production['delivery_profile_id'],
        'presentation_profile_id': production['presentation_profile_id'],
        'variation_index': production['variation_index'],
        'audio_enabled': production['audio_enabled'],
        'personalization_enabled': production['personalization_enabled'],
        'editorial_profile': dict(profile),
        'production_override': dict(overrides),
        'provenance': {'source_revision':'C11D-GUI-STATE-ADAPTER-V1','request_origin':'GUI'},
    }
    if canonical_json(state) != before:
        raise SharedProductionGUIStateError('GUI state was mutated while mapping to canonical request')
    # Canonical request is audited by the canonical backend; this light schema mapping must not resolve catalog/business rules.
    return raw

def build_canonical_request_from_gui_state(state: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    return validate_gui_state(state, project_root)

def prepare_gui_state_context(state: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    raw = build_canonical_request_from_gui_state(state, root)
    try:
        return prepare_gui_shared_context(raw, root)
    except Exception as exc:
        raise SharedProductionGUIStateError(f'Canonical shared context rejected GUI state: {exc}') from exc
