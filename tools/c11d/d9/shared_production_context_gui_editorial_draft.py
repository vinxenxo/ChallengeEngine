"""Request-scoped editorial draft lifecycle for the future shared D9 GUI.

This D-owned service preserves common text overrides across selector changes,
removes Challenge-only overrides when the selected content type is not
Challenges, and delegates effective-value resolution to the canonical D9.8
editorial model. It does not modify GUI widgets, persist drafts, create D9.9
production requests, emit renderer input, dispatch rendering, or create media.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from universal_editorial_model import (
    EditorialModelError,
    build_catalog,
    load_model,
    resolve_editorial_values,
)
from shared_production_context_gui_catalog import (
    SharedProductionGUICatalogError,
    audit_dynamic_gui_catalog,
    _sha_value as _catalog_sha_value,
)
from shared_production_context_gui_reactive_selection import (
    SharedProductionGUIReactiveSelectionError,
    SNAPSHOT_ID as REACTIVE_SNAPSHOT_ID,
    SNAPSHOT_SCHEMA_REL as REACTIVE_SNAPSHOT_SCHEMA_REL,
    audit_reactive_selection_contract,
    _sha_value as _reactive_sha_value,
)

MANIFEST_SHA256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
GUI_STATE_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_SCHEMA_V1.json')
CONTRACT_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_DRAFT_LIFECYCLE_CONTRACT_V1.json')
CONTRACT_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_DRAFT_LIFECYCLE_CONTRACT_SCHEMA_V1.json')
STATE_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_DRAFT_STATE_SCHEMA_V1.json')
CONTRACT_ID = 'C11-D-D9-SHARED-PRODUCTION-CONTEXT-GUI-EDITORIAL-DRAFT-LIFECYCLE-CONTRACT-V1'
STATE_ID = 'C11-D-SHARED-PRODUCTION-GUI-EDITORIAL-DRAFT-STATE-V1'
SHARED_FIELDS = ('title', 'subtitle', 'call_to_action', 'language')
CHALLENGE_FIELDS = ('player_name', 'challenge_label')
EDITABLE_FIELDS = frozenset((*SHARED_FIELDS, *CHALLENGE_FIELDS))


class SharedProductionGUIEditorialDraftError(ValueError):
    """Invalid editorial draft state or failed canonical resolution."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT


def _read_json(root: Path, rel: Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding='utf-8-sig'))
    except Exception as exc:
        raise SharedProductionGUIEditorialDraftError(f'Cannot read {rel.as_posix()}: {exc}') from exc
    if not isinstance(value, dict):
        raise SharedProductionGUIEditorialDraftError(f'Expected JSON object: {rel.as_posix()}')
    return value


def _sha_file(root: Path, rel: str) -> str:
    try:
        return hashlib.sha256((root / rel).read_bytes()).hexdigest()
    except Exception as exc:
        raise SharedProductionGUIEditorialDraftError(f'Cannot hash pinned source {rel}: {exc}') from exc


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=True, allow_nan=False, separators=(',', ':'), sort_keys=True)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode('ascii')).hexdigest()


def _schema_validate(root: Path, schema_rel: Path, instance: Any, label: str) -> None:
    try:
        import jsonschema
        schema = _read_json(root, schema_rel)
        jsonschema.Draft202012Validator.check_schema(schema)
        errors = sorted(
            jsonschema.Draft202012Validator(schema).iter_errors(instance),
            key=lambda e: (list(map(str, e.path)), e.message),
        )
    except Exception as exc:
        raise SharedProductionGUIEditorialDraftError(f'{label} schema validation failed: {exc}') from exc
    if errors:
        err = errors[0]
        raise SharedProductionGUIEditorialDraftError(f'{label} schema violation at {list(err.path)}: {err.message}')


def audit_gui_editorial_draft_contract(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    try:
        parent = audit_reactive_selection_contract(root)
    except Exception as exc:
        raise SharedProductionGUIEditorialDraftError(f'Parent catalog/reactive-selection contract failed: {exc}') from exc

    contract = _read_json(root, CONTRACT_REL)
    contract_schema = _read_json(root, CONTRACT_SCHEMA_REL)
    state_schema = _read_json(root, STATE_SCHEMA_REL)
    _schema_validate(root, CONTRACT_SCHEMA_REL, contract, 'Editorial draft contract')

    if contract.get('schema') != CONTRACT_ID or contract.get('schema_version') != '1.0':
        raise SharedProductionGUIEditorialDraftError('Editorial draft contract identity mismatch')
    if contract.get('status') != 'PREPARE_ONLY_EDITORIAL_DRAFT_NO_GUI_WIDGET_MODIFICATION':
        raise SharedProductionGUIEditorialDraftError('Editorial draft contract must remain prepare-only')

    expected_contract_schema_hash = _sha_file(root, CONTRACT_SCHEMA_REL.as_posix())
    expected_state_schema_hash = _sha_file(root, STATE_SCHEMA_REL.as_posix())
    expected_impl_hash = _sha_file(root, 'tools/c11d/d9/shared_production_context_gui_editorial_draft.py')
    for key, expected in (
        ('contract_schema_sha256', expected_contract_schema_hash),
        ('state_schema_sha256', expected_state_schema_hash),
        ('implementation_sha256', expected_impl_hash),
    ):
        if contract.get(key) != expected:
            raise SharedProductionGUIEditorialDraftError(f'Pinned {key} mismatch')

    lineage = contract.get('source_lineage')
    if not isinstance(lineage, list) or len(lineage) != 10:
        raise SharedProductionGUIEditorialDraftError('Expected exactly ten canonical source pins')
    seen: set[str] = set()
    for row in lineage:
        if not isinstance(row, Mapping) or set(row) != {'path', 'role', 'sha256'}:
            raise SharedProductionGUIEditorialDraftError('Malformed editorial draft source-lineage row')
        rel, digest = row['path'], row['sha256']
        if not isinstance(rel, str) or not rel or rel.startswith('/') or '\\' in rel or any(part in ('', '.', '..') for part in rel.split('/')):
            raise SharedProductionGUIEditorialDraftError(f'Unsafe source path: {rel!r}')
        if rel in seen:
            raise SharedProductionGUIEditorialDraftError(f'Duplicate source pin: {rel}')
        if not isinstance(digest, str) or not re.fullmatch(r'[a-f0-9]{64}', digest):
            raise SharedProductionGUIEditorialDraftError(f'Invalid source SHA-256: {rel}')
        if _sha_file(root, rel) != digest:
            raise SharedProductionGUIEditorialDraftError(f'Pinned editorial-draft source drift: {rel}')
        seen.add(rel)

    if lineage[0]['path'] != 'release/C11C_FREEZE_PACKAGE_MANIFEST.json' or lineage[0]['sha256'] != MANIFEST_SHA256:
        raise SharedProductionGUIEditorialDraftError('Frozen C11-C manifest must be the first source pin')

    try:
        jsonschema = __import__('jsonschema')
        jsonschema.Draft202012Validator.check_schema(state_schema)
        jsonschema.Draft202012Validator.check_schema(contract_schema)
    except Exception as exc:
        raise SharedProductionGUIEditorialDraftError(f'Editorial draft schema definition invalid: {exc}') from exc

    return {
        'source_pins': len(lineage),
        'parent_reactive_selection_source_pins': parent['source_pins'],
        'parent_catalog_source_pins': parent.get('parent_catalog_source_pins'),
        'state_schema_sha256': expected_state_schema_hash,
        'renderer': 'OFF',
        'media_created': False,
        'D4.8': 'BLOCKED',
        'release_authority': 'NONE',
    }


def _visible_fields(content_type: str | None, root: Path) -> list[str]:
    if content_type is None:
        return []
    model = load_model(root)
    declaration = model.get('content_types', {}).get(content_type)
    if not isinstance(declaration, Mapping):
        raise SharedProductionGUIEditorialDraftError(f'Unknown active content type: {content_type}')
    result = []
    for field in declaration.get('editable_fields', []):
        field_spec = model.get('editorial_fields', {}).get(field, {})
        if field_spec.get('enabled') is True and content_type in field_spec.get('content_types', []):
            result.append(field)
    return result


def _max_override_length(field: str, root: Path) -> int:
    """Use the stricter limit of canonical D9.8 and the GUI request-state schema."""
    model = load_model(root)
    model_max = int(model['editorial_fields'][field].get('max_length', 160))
    gui_schema = _read_json(root, GUI_STATE_SCHEMA_REL)
    gui_overrides = (gui_schema.get('properties', {}).get('editorial', {})
                     .get('properties', {}).get('overrides', {})
                     .get('properties', {}))
    gui_spec = gui_overrides.get(field)
    if not isinstance(gui_spec, Mapping) or not isinstance(gui_spec.get('maxLength'), int):
        raise SharedProductionGUIEditorialDraftError(f'GUI request-state schema has no text limit for editable field: {field}')
    return min(model_max, int(gui_spec['maxLength']))


def _validate_profile(profile: Any, root: Path) -> dict[str, Any]:
    if not isinstance(profile, Mapping):
        raise SharedProductionGUIEditorialDraftError('Editorial profile must be an object')
    # D9.8 validates all declared scopes, including non-selected scopes, when
    # resolving a valid selector. Use an actual Challenge from the live catalog
    # solely as a validation anchor; its returned values are discarded.
    catalog = build_catalog(root)
    families = catalog.get('content_types', {}).get('challenges', {}).get('families', [])
    anchor = next((
        (family['id'], variant['id'])
        for family in families
        for variant in family.get('variants', [])
    ), None)
    if anchor is None:
        raise SharedProductionGUIEditorialDraftError('No canonical Challenge anchor is available to validate editorial profile scopes')
    family_id, variant_id = anchor
    try:
        resolve_editorial_values(
            {'content_type': 'challenges', 'family_id': family_id, 'variant_id': variant_id},
            profile=dict(profile),
            production_override={},
            project_root=root,
        )
    except Exception as exc:
        raise SharedProductionGUIEditorialDraftError(f'Canonical D9.8 editorial profile rejected: {exc}') from exc
    return copy.deepcopy(dict(profile))


def _validate_snapshot(snapshot: Mapping[str, Any], root: Path) -> dict[str, Any]:
    if not isinstance(snapshot, Mapping):
        raise SharedProductionGUIEditorialDraftError('Reactive selection snapshot must be an object')
    _schema_validate(root, REACTIVE_SNAPSHOT_SCHEMA_REL, dict(snapshot), 'Reactive selection snapshot')
    if snapshot.get('schema') != REACTIVE_SNAPSHOT_ID or snapshot.get('schema_version') != '1.0':
        raise SharedProductionGUIEditorialDraftError('Reactive selection snapshot identity mismatch')

    snapshot_copy = copy.deepcopy(dict(snapshot))
    identity = snapshot_copy.get('identity')
    if not isinstance(identity, dict):
        raise SharedProductionGUIEditorialDraftError('Reactive snapshot identity is missing')
    observed_snapshot_hash = identity.pop('snapshot_sha256', None)
    if not isinstance(observed_snapshot_hash, str) or not re.fullmatch(r'[a-f0-9]{64}', observed_snapshot_hash):
        raise SharedProductionGUIEditorialDraftError('Invalid reactive snapshot SHA-256')
    if canonical_sha256(snapshot_copy) != observed_snapshot_hash:
        raise SharedProductionGUIEditorialDraftError('Reactive snapshot content/hash mismatch')

    state = snapshot.get('state')
    if not isinstance(state, Mapping) or state.get('schema') != 'C11-D-SHARED-GUI-REACTIVE-SELECTION-STATE-V1':
        raise SharedProductionGUIEditorialDraftError('Reactive selection state identity mismatch')
    selection = state.get('selection')
    if not isinstance(selection, Mapping) or set(selection) != {'content_type', 'family_id', 'selector_field', 'selector_id'}:
        raise SharedProductionGUIEditorialDraftError('Reactive selection shape mismatch')
    if identity.get('catalog_sha256') != state.get('catalog_sha256'):
        raise SharedProductionGUIEditorialDraftError('Reactive selection/catalog identity mismatch')

    try:
        current_catalog = build_catalog(root)
        fresh_catalog_hash = _catalog_sha_value(current_catalog)
    except Exception as exc:
        raise SharedProductionGUIEditorialDraftError(f'Cannot refresh canonical catalog identity: {exc}') from exc
    if state.get('catalog_sha256') != fresh_catalog_hash:
        raise SharedProductionGUIEditorialDraftError('Stale reactive selection snapshot; explicit catalog refresh is required')

    readiness = snapshot.get('readiness')
    if not isinstance(readiness, Mapping):
        raise SharedProductionGUIEditorialDraftError('Reactive snapshot readiness is missing')
    complete = readiness.get('selection_path_complete') is True
    resolved = readiness.get('canonical_selection_resolved') is True
    if complete and not resolved:
        raise SharedProductionGUIEditorialDraftError('Reactive snapshot claims a complete but unresolved selection path')

    binding = {
        'mode': state.get('mode'),
        'catalog_sha256': state.get('catalog_sha256'),
        'selection_snapshot_sha256': observed_snapshot_hash,
        'content_type': selection.get('content_type'),
        'family_id': selection.get('family_id'),
        'selector_field': selection.get('selector_field'),
        'selector_id': selection.get('selector_id'),
        'selection_path_complete': complete,
        'canonical_selection_resolved': resolved,
        'blockers': list(readiness.get('blockers', [])),
    }
    _validate_selection_binding(binding)
    return binding


def _validate_selection_binding(binding: Mapping[str, Any]) -> None:
    if binding.get('mode') not in {'REVIEW', 'PRODUCTION'}:
        raise SharedProductionGUIEditorialDraftError('Unsupported GUI mode in editorial draft binding')
    for key in ('catalog_sha256', 'selection_snapshot_sha256'):
        value = binding.get(key)
        if not isinstance(value, str) or not re.fullmatch(r'[a-f0-9]{64}', value):
            raise SharedProductionGUIEditorialDraftError(f'Invalid selection binding hash: {key}')
    content_type = binding.get('content_type')
    if content_type not in {None, 'challenges', 'visual_loops', 'visual_drills'}:
        raise SharedProductionGUIEditorialDraftError(f'Unsupported content type in editorial draft: {content_type!r}')
    family, field, selector = (binding.get(k) for k in ('family_id', 'selector_field', 'selector_id'))
    for key, value in (('family_id', family), ('selector_field', field), ('selector_id', selector)):
        if value is not None and not isinstance(value, str):
            raise SharedProductionGUIEditorialDraftError(f'{key} must be a string or null')
    if content_type is None and (family is not None or field is not None or selector is not None):
        raise SharedProductionGUIEditorialDraftError('Descendant selection requires a content type')
    if family is None and (field is not None or selector is not None):
        raise SharedProductionGUIEditorialDraftError('Selector requires a family')
    if selector is None and field is not None:
        raise SharedProductionGUIEditorialDraftError('selector_field must be null before selector_id')
    if selector is not None and (field not in {'subtype_id', 'variant_id'} or family is None or content_type is None):
        raise SharedProductionGUIEditorialDraftError('Selector binding is incomplete or invalid')
    complete = binding.get('selection_path_complete')
    resolved = binding.get('canonical_selection_resolved')
    if not isinstance(complete, bool) or not isinstance(resolved, bool):
        raise SharedProductionGUIEditorialDraftError('Selection readiness fields must be booleans')
    if complete and not resolved:
        raise SharedProductionGUIEditorialDraftError('Complete selection must have a canonical resolution')
    if selector is not None and not complete:
        raise SharedProductionGUIEditorialDraftError('Selector present but selection is not marked complete')
    blockers = binding.get('blockers')
    if not isinstance(blockers, list) or any(not isinstance(item, str) for item in blockers):
        raise SharedProductionGUIEditorialDraftError('Selection blockers must be a list of strings')


def _seal_state(state_without_hash: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(state_without_hash))
    value.pop('state_sha256', None)
    value['state_sha256'] = canonical_sha256(value)
    return value


def _validate_state(state: Mapping[str, Any], root: Path, *, validate_profile: bool = True) -> dict[str, Any]:
    if not isinstance(state, Mapping):
        raise SharedProductionGUIEditorialDraftError('Editorial draft state must be an object')
    value = copy.deepcopy(dict(state))
    observed_hash = value.pop('state_sha256', None)
    if not isinstance(observed_hash, str) or not re.fullmatch(r'[a-f0-9]{64}', observed_hash):
        raise SharedProductionGUIEditorialDraftError('Missing or malformed editorial draft state hash')
    if canonical_sha256(value) != observed_hash:
        raise SharedProductionGUIEditorialDraftError('Editorial draft state hash mismatch')
    value['state_sha256'] = observed_hash
    _schema_validate(root, STATE_SCHEMA_REL, value, 'Editorial draft state')
    if value.get('schema') != STATE_ID or value.get('schema_version') != '1.0':
        raise SharedProductionGUIEditorialDraftError('Editorial draft state identity mismatch')

    binding = value.get('selection_binding')
    if not isinstance(binding, Mapping):
        raise SharedProductionGUIEditorialDraftError('Editorial draft selection binding is missing')
    _validate_selection_binding(binding)
    content_type = binding.get('content_type')
    overrides = value.get('overrides')
    if not isinstance(overrides, Mapping):
        raise SharedProductionGUIEditorialDraftError('Editorial overrides must be an object')
    allowed = set(_visible_fields(content_type, root))
    unknown = set(overrides) - allowed
    if unknown:
        raise SharedProductionGUIEditorialDraftError('Inactive/unknown override fields in draft state: ' + ', '.join(sorted(unknown)))
    model = load_model(root)
    for field, field_value in overrides.items():
        if not isinstance(field_value, str):
            raise SharedProductionGUIEditorialDraftError(f'Editorial override {field} must be a string')
        max_length = _max_override_length(field, root)
        if len(field_value) > max_length:
            raise SharedProductionGUIEditorialDraftError(f'Editorial override {field} exceeds canonical maximum length {max_length}')
    if validate_profile:
        _validate_profile(value.get('profile'), root)
    return value


def _new_state(binding: Mapping[str, Any], profile: Mapping[str, Any], overrides: Mapping[str, str], root: Path) -> dict[str, Any]:
    content_type = binding.get('content_type')
    valid_overrides = dict(overrides)
    if content_type != 'challenges':
        for field in CHALLENGE_FIELDS:
            valid_overrides.pop(field, None)
    allowed = set(_visible_fields(content_type, root))
    invalid = set(valid_overrides) - allowed
    if invalid:
        raise SharedProductionGUIEditorialDraftError('Overrides invalid for selected content type: ' + ', '.join(sorted(invalid)))
    candidate = {
        'schema': STATE_ID,
        'schema_version': '1.0',
        'selection_binding': copy.deepcopy(dict(binding)),
        'profile': copy.deepcopy(dict(profile)),
        'overrides': valid_overrides,
    }
    sealed = _seal_state(candidate)
    return _validate_state(sealed, root)


def initialize_gui_editorial_draft_state(
    selection_snapshot: Mapping[str, Any],
    profile: Mapping[str, Any] | None = None,
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    root = _root(project_root)
    audit_gui_editorial_draft_contract(root)
    binding = _validate_snapshot(selection_snapshot, root)
    valid_profile = _validate_profile({} if profile is None else profile, root)
    return _new_state(binding, valid_profile, {}, root)


def transition_gui_editorial_draft_state(
    current_state: Mapping[str, Any],
    selection_snapshot: Mapping[str, Any],
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    root = _root(project_root)
    audit_gui_editorial_draft_contract(root)
    current = _validate_state(current_state, root)
    binding = _validate_snapshot(selection_snapshot, root)
    previous_binding = current['selection_binding']
    if previous_binding['catalog_sha256'] != binding['catalog_sha256'] and selection_snapshot.get('transition', {}).get('catalog_refreshed') is not True:
        raise SharedProductionGUIEditorialDraftError('Catalog identity changed without explicit refresh_catalog transition')
    # Universal fields survive all type/family/selector changes. Challenge-only
    # request overrides are dropped when Challenges is no longer active, not stashed.
    return _new_state(binding, current['profile'], current['overrides'], root)


def set_gui_editorial_draft_override(
    current_state: Mapping[str, Any], field: str, value: str,
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    root = _root(project_root)
    audit_gui_editorial_draft_contract(root)
    current = _validate_state(current_state, root)
    if not isinstance(field, str) or field not in EDITABLE_FIELDS:
        raise SharedProductionGUIEditorialDraftError(f'Unknown or disabled editorial field: {field!r}')
    if not isinstance(value, str):
        raise SharedProductionGUIEditorialDraftError(f'Editorial override {field} must be a string')
    active = set(_visible_fields(current['selection_binding'].get('content_type'), root))
    if field not in active:
        raise SharedProductionGUIEditorialDraftError(f'Editorial field is not active for current content type: {field}')
    max_length = _max_override_length(field, root)
    if len(value) > max_length:
        raise SharedProductionGUIEditorialDraftError(f'Editorial override {field} exceeds canonical maximum length {max_length}')
    overrides = dict(current['overrides'])
    overrides[field] = value
    return _new_state(current['selection_binding'], current['profile'], overrides, root)


def clear_gui_editorial_draft_override(
    current_state: Mapping[str, Any], field: str,
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    root = _root(project_root)
    audit_gui_editorial_draft_contract(root)
    current = _validate_state(current_state, root)
    if not isinstance(field, str) or field not in EDITABLE_FIELDS:
        raise SharedProductionGUIEditorialDraftError(f'Unknown or disabled editorial field: {field!r}')
    active = set(_visible_fields(current['selection_binding'].get('content_type'), root))
    if field not in active:
        raise SharedProductionGUIEditorialDraftError(f'Editorial field is not active for current content type: {field}')
    overrides = dict(current['overrides'])
    overrides.pop(field, None)
    return _new_state(current['selection_binding'], current['profile'], overrides, root)


def _canonical_selection(binding: Mapping[str, Any]) -> dict[str, Any]:
    content_type = binding.get('content_type')
    family_id = binding.get('family_id')
    selector_field = binding.get('selector_field')
    selector_id = binding.get('selector_id')
    if not binding.get('selection_path_complete') or not binding.get('canonical_selection_resolved'):
        raise SharedProductionGUIEditorialDraftError('Selection path is incomplete; editorial values cannot be resolved yet')
    selection: dict[str, Any] = {'content_type': content_type, 'family_id': family_id}
    if selector_field == 'subtype_id':
        selection['subtype_id'] = selector_id
    elif selector_field == 'variant_id':
        selection['variant_id'] = selector_id
    else:
        raise SharedProductionGUIEditorialDraftError('Unsupported canonical selector field')
    return selection


def preview_gui_editorial_draft(
    current_state: Mapping[str, Any], project_root: Path | str | None = None,
) -> dict[str, Any]:
    root = _root(project_root)
    audit_gui_editorial_draft_contract(root)
    state = _validate_state(current_state, root)
    binding = state['selection_binding']
    visible = _visible_fields(binding.get('content_type'), root)
    preview: dict[str, Any] = {
        'schema': 'C11-D-SHARED-PRODUCTION-GUI-EDITORIAL-DRAFT-PREVIEW-V1',
        'schema_version': '1.0',
        'state_sha256': state['state_sha256'],
        'selection_binding': copy.deepcopy(binding),
        'active_fields': visible,
        'draft_overrides': copy.deepcopy(state['overrides']),
        'effective_values': None,
        'applied_layers': [],
        'status': 'SELECTION_INCOMPLETE',
        'execution_boundary': {
            'canonical_production_request_created': False,
            'renderer_input_emitted': False,
            'renderer_dispatch_invoked': False,
            'media_created': False,
            'persisted': False,
            'release_authority': 'NONE',
        },
    }
    if binding['selection_path_complete'] and binding['canonical_selection_resolved']:
        try:
            result = resolve_editorial_values(
                _canonical_selection(binding),
                profile=state['profile'],
                production_override=state['overrides'],
                project_root=root,
            )
        except Exception as exc:
            raise SharedProductionGUIEditorialDraftError(f'Canonical D9.8 editorial resolution failed: {exc}') from exc
        values = result.get('values')
        expected_fields = set(visible)
        if not isinstance(values, Mapping) or set(values) != expected_fields:
            raise SharedProductionGUIEditorialDraftError('Canonical D9.8 returned an unexpected active editorial field set')
        if binding.get('content_type') != 'challenges' and set(values) & set(CHALLENGE_FIELDS):
            raise SharedProductionGUIEditorialDraftError('Challenge-only fields leaked into a non-Challenge preview')
        preview['effective_values'] = dict(values)
        preview['applied_layers'] = list(result.get('applied_layers', []))
        preview['status'] = 'READY_FOR_EDITORIAL_REVIEW_ONLY'
    preview['preview_sha256'] = canonical_sha256(preview)
    return preview


def _json_out(value: Any) -> None:
    sys.stdout.write(canonical_json(value) + '\n')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Prepare-only shared editorial draft lifecycle for the future D9 GUI')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--audit-only', action='store_true')
    group.add_argument('--initialize-from-snapshot-json')
    group.add_argument('--transition', action='store_true')
    group.add_argument('--set-field', action='store_true')
    group.add_argument('--clear-field', action='store_true')
    group.add_argument('--preview', action='store_true')
    parser.add_argument('--state-json')
    parser.add_argument('--snapshot-json')
    parser.add_argument('--profile-json')
    parser.add_argument('--field')
    parser.add_argument('--value')
    parser.add_argument('--project-root', type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        if args.audit_only:
            result = {'result': 'PASS', 'audit': audit_gui_editorial_draft_contract(args.project_root)}
        elif args.initialize_from_snapshot_json:
            snapshot = json.loads(args.initialize_from_snapshot_json)
            profile = json.loads(args.profile_json) if args.profile_json else {}
            result = initialize_gui_editorial_draft_state(snapshot, profile, args.project_root)
        elif args.transition:
            if not args.state_json or not args.snapshot_json:
                raise SharedProductionGUIEditorialDraftError('--transition requires --state-json and --snapshot-json')
            result = transition_gui_editorial_draft_state(json.loads(args.state_json), json.loads(args.snapshot_json), args.project_root)
        elif args.set_field:
            if not args.state_json or args.field is None or args.value is None:
                raise SharedProductionGUIEditorialDraftError('--set-field requires --state-json, --field, and --value')
            result = set_gui_editorial_draft_override(json.loads(args.state_json), args.field, args.value, args.project_root)
        elif args.clear_field:
            if not args.state_json or args.field is None:
                raise SharedProductionGUIEditorialDraftError('--clear-field requires --state-json and --field')
            result = clear_gui_editorial_draft_override(json.loads(args.state_json), args.field, args.project_root)
        else:
            if not args.state_json:
                raise SharedProductionGUIEditorialDraftError('--preview requires --state-json')
            result = preview_gui_editorial_draft(json.loads(args.state_json), args.project_root)
        _json_out(result)
        return 0
    except Exception as exc:
        _json_out({
            'result': 'FAIL',
            'error_type': type(exc).__name__,
            'error': str(exc),
            'renderer': 'OFF', 'media_created': False,
            'D4.8': 'BLOCKED', 'release_authority': 'NONE',
        })
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
