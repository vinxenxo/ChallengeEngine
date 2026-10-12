"""Read-only dynamic selector catalog for the future shared D9 GUI.

Options are projected from the canonical D9.8 model/Producer schema. The module
never duplicates family/subtype/variant inventories, never writes artifacts, and
never invokes rendering. Model-only content remains REVIEW-selectable but cannot
be promoted to PRODUCTION mode while request_plan_compatible is false.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from universal_editorial_model import EditorialModelError, build_catalog, resolve_selection as resolve_canonical_selection
from universal_producer import REQUEST_SCHEMA_REL

CONTRACT_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_CATALOG_CONTRACT_V1.json')
CONTRACT_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_CATALOG_CONTRACT_SCHEMA_V1.json')
CATALOG_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_CATALOG_SCHEMA_V1.json')
SELECTION_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_DYNAMIC_SELECTION_SCHEMA_V1.json')
GUI_STATE_CONTRACT_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_CONTRACT_V1.json')
GUI_STATE_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_STATE_SCHEMA_V1.json')
CATALOG_SCHEMA_ID = 'C11-D-D9-SHARED-PRODUCTION-GUI-DYNAMIC-CATALOG-V1'
SELECTION_SCHEMA_ID = 'C11-D-D9-SHARED-PRODUCTION-GUI-DYNAMIC-SELECTION-V1'

class SharedProductionGUICatalogError(ValueError):
    """Raised when catalog integrity or selector compatibility fails."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT

def _read_json(root: Path, rel: Path) -> Any:
    try:
        return json.loads((root / rel).read_text(encoding='utf-8-sig'))
    except Exception as exc:
        raise SharedProductionGUICatalogError(f'Cannot read {rel.as_posix()}: {exc}') from exc

def _sha_file(root: Path, rel: str) -> str:
    try:
        return hashlib.sha256((root / rel).read_bytes()).hexdigest()
    except Exception as exc:
        raise SharedProductionGUICatalogError(f'Cannot hash pinned source {rel}: {exc}') from exc

def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value

def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(_canonical(value), ensure_ascii=True, allow_nan=False, separators=(',', ':')).encode('ascii')

def _sha_value(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()

def _display_label(identifier: str, row: Mapping[str, Any]) -> str:
    label = row.get('label')
    if isinstance(label, str) and label.strip():
        return label.strip()
    # Display-only fallback; never used for identity or request selection.
    return identifier.replace('_', ' ').replace('-', ' ').title()

def audit_dynamic_gui_catalog(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract = _read_json(root, CONTRACT_REL)
    contract_schema = _read_json(root, CONTRACT_SCHEMA_REL)
    catalog_schema = _read_json(root, CATALOG_SCHEMA_REL)
    selection_schema = _read_json(root, SELECTION_SCHEMA_REL)
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(contract_schema)
        errors = list(jsonschema.Draft202012Validator(contract_schema).iter_errors(contract))
        if errors:
            raise SharedProductionGUICatalogError(f'Contract schema violation: {errors[0].message}')
        jsonschema.Draft202012Validator.check_schema(catalog_schema)
        jsonschema.Draft202012Validator.check_schema(selection_schema)
    except SharedProductionGUICatalogError:
        raise
    except Exception as exc:
        raise SharedProductionGUICatalogError(f'JSON Schema validation failed: {exc}') from exc

    if contract.get('schema') != 'C11-D-D9-SHARED-PRODUCTION-GUI-DYNAMIC-CATALOG-CONTRACT-V1':
        raise SharedProductionGUICatalogError('Dynamic GUI catalog contract identity mismatch')
    if contract.get('status') != 'PREPARE_ONLY_READ_ONLY_DYNAMIC_OPTIONS_NO_GUI_SOURCE_MODIFICATION':
        raise SharedProductionGUICatalogError('Dynamic GUI catalog contract status mismatch')
    expected_hashes = {
        'implementation_sha256': module_rel_hash(root),
        'contract_schema_sha256': _sha_file(root, CONTRACT_SCHEMA_REL.as_posix()),
        'catalog_schema_sha256': _sha_file(root, CATALOG_SCHEMA_REL.as_posix()),
        'selection_schema_sha256': _sha_file(root, SELECTION_SCHEMA_REL.as_posix()),
    }
    for key, actual in expected_hashes.items():
        if contract.get(key) != actual:
            raise SharedProductionGUICatalogError(f'Pinned {key} mismatch')

    lineage = contract.get('source_lineage')
    if not isinstance(lineage, list) or len(lineage) != 8:
        raise SharedProductionGUICatalogError('Expected exactly eight canonical source pins')
    seen: set[str] = set()
    for row in lineage:
        if not isinstance(row, dict):
            raise SharedProductionGUICatalogError('Source lineage item must be an object')
        rel = row.get('path')
        digest = row.get('sha256')
        if not isinstance(rel, str) or not rel or '\\' in rel or rel.startswith('/') or any(part in ('.', '..') for part in rel.split('/')):
            raise SharedProductionGUICatalogError(f'Unsafe source path: {rel!r}')
        if rel in seen:
            raise SharedProductionGUICatalogError(f'Duplicate source pin: {rel}')
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise SharedProductionGUICatalogError(f'Invalid source SHA-256: {rel}')
        if _sha_file(root, rel) != digest:
            raise SharedProductionGUICatalogError(f'Pinned source drift: {rel}')
        seen.add(rel)
    if lineage[0].get('path') != 'release/C11C_FREEZE_PACKAGE_MANIFEST.json':
        raise SharedProductionGUICatalogError('Frozen C11-C manifest must be the first source pin')

    request_contract = _read_json(root, REQUEST_SCHEMA_REL)
    gui_contract = _read_json(root, GUI_STATE_CONTRACT_REL)
    gui_schema = _read_json(root, GUI_STATE_SCHEMA_REL)
    gui_mapping = gui_contract.get('control_mapping', {}) if isinstance(gui_contract, dict) else {}
    if gui_contract.get('schema') != 'C11-D-D9-SHARED-PRODUCTION-CONTEXT-GUI-STATE-CONTRACT-V1':
        raise SharedProductionGUICatalogError('Canonical GUI state contract identity mismatch')
    if gui_mapping.get('visual_loop_selector') != 'subtype_id' or gui_mapping.get('challenge_and_drill_selector') != 'variant_id':
        raise SharedProductionGUICatalogError('GUI state selector fields differ from the canonical dynamic catalog contract')
    if gui_mapping.get('unknown_selectors') != 'REJECT':
        raise SharedProductionGUICatalogError('Canonical GUI state contract must reject unknown selectors')
    request_types = request_contract.get('supported_content_types')
    gui_types = gui_schema.get('properties', {}).get('selection', {}).get('properties', {}).get('content_type', {}).get('enum')
    if not isinstance(request_types, list) or not isinstance(gui_types, list):
        raise SharedProductionGUICatalogError('Canonical request/GUI state content-type declarations are missing')
    expected_active_types = {'challenges', 'visual_loops', 'visual_drills'}
    if not expected_active_types.issubset(set(request_types)) or not expected_active_types.issubset(set(gui_types)):
        raise SharedProductionGUICatalogError('Canonical request and GUI state schemas must both declare all three active content types')

    try:
        raw = build_catalog(root)
    except Exception as exc:
        raise SharedProductionGUICatalogError(f'Canonical selector catalog failed: {exc}') from exc
    rows = raw.get('content_types') if isinstance(raw, dict) else None
    if not isinstance(rows, dict):
        raise SharedProductionGUICatalogError('Canonical D9.8 catalog content_types is missing')
    required = {'challenges', 'visual_loops', 'visual_drills'}
    if not required.issubset(rows):
        raise SharedProductionGUICatalogError('Canonical D9.8 selector catalog lost an active content type')
    if 'longform' not in rows:
        raise SharedProductionGUICatalogError('Longform must remain represented explicitly as disabled')
    return {
        'source_pins': len(lineage),
        'active_type_contract_parity': len(required),
        'longform_present_disabled': rows['longform'].get('enabled_for_selection') is False,
        'implementation_sha256': expected_hashes['implementation_sha256'],
        'catalog_sha256': _sha_value(raw),
        'renderer': 'OFF',
        'media_created': False,
        'D4.8': 'BLOCKED',
        'release_authority': 'NONE',
    }

def module_rel_hash(root: Path) -> str:
    try:
        return _sha_file(root, 'tools/c11d/d9/shared_production_context_gui_catalog.py')
    except Exception as exc:
        raise SharedProductionGUICatalogError(f'Cannot hash dynamic catalog implementation: {exc}') from exc

def _selector_rows(content_type: str, family: Mapping[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    if content_type == 'visual_loops':
        rows = family.get('subtypes')
        key = 'subtype_id'
    else:
        rows = family.get('variants')
        key = 'variant_id'
    if not isinstance(rows, list):
        raise SharedProductionGUICatalogError(f'Family selector inventory is missing for {content_type}/{family.get("id")}')
    selectors = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id']:
            raise SharedProductionGUICatalogError(f'Malformed selector row in {content_type}/{family.get("id")}')
        if row['id'] in seen:
            raise SharedProductionGUICatalogError(f'Duplicate selector in {content_type}/{family.get("id")}: {row["id"]}')
        seen.add(row['id'])
        selectors.append({
            'id': row['id'],
            'label': _display_label(row['id'], row),
            'selector_field': key,
            'selection_mode': bool(row.get('selection_mode', False)),
            'concrete_variant': bool(row.get('concrete_variant', True)),
            'metadata': {k: v for k, v in row.items() if k not in {'id', 'label'}},
        })
    return key, selectors

def build_dynamic_gui_catalog(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    audit = audit_dynamic_gui_catalog(root)
    contract = _read_json(root, CONTRACT_REL)
    request_contract = _read_json(root, REQUEST_SCHEMA_REL)
    gui_state_schema = _read_json(root, GUI_STATE_SCHEMA_REL)
    request_types = set(request_contract['supported_content_types'])
    gui_types = set(gui_state_schema['properties']['selection']['properties']['content_type']['enum'])
    raw = build_catalog(root)
    content_types: list[dict[str, Any]] = []
    family_total = selector_total = active_count = disabled_count = 0

    for content_type, info in raw['content_types'].items():
        state = str(info.get('state', 'UNKNOWN'))
        enabled_in_model = info.get('enabled_for_selection') is not False and state != 'VISIBLE_BUT_DISABLED'
        canonical_supported = content_type in request_types and content_type in gui_types
        selectable = bool(enabled_in_model and canonical_supported)
        request_compatible = info.get('request_plan_compatible') is True
        review_enabled = selectable
        production_enabled = bool(selectable and request_compatible and state == 'ACTIVE')
        if not canonical_supported:
            reason = 'NOT_SUPPORTED_BY_CANONICAL_REQUEST_AND_GUI_STATE_CONTRACTS'
        elif not enabled_in_model:
            reason = str(info.get('reason') or 'DISABLED_BY_CANONICAL_MODEL')
        elif not production_enabled:
            reason = str(info.get('compatibility_reason') or info.get('request_plan_compatibility') or 'REQUEST_PLAN_COMPATIBILITY_NOT_APPROVED')
        else:
            reason = None
        family_rows = info.get('families', []) if isinstance(info.get('families', []), list) else []
        families: list[dict[str, Any]] = []
        for family in family_rows:
            if not isinstance(family, dict) or not isinstance(family.get('id'), str):
                raise SharedProductionGUICatalogError(f'Malformed family in canonical catalog: {content_type}')
            selector_field, selectors = _selector_rows(content_type, family)
            family_total += 1
            selector_total += len(selectors)
            families.append({
                'id': family['id'],
                'label': _display_label(family['id'], family),
                'selector_field': selector_field,
                'selectors': selectors,
                'selection_enabled': selectable,
                'allowed_modes': ['REVIEW', 'PRODUCTION'] if production_enabled else (['REVIEW'] if review_enabled else []),
                'source_metadata': {k: v for k, v in family.items() if k not in {'id', 'label', 'subtypes', 'variants'}},
            })
        if selectable:
            active_count += 1
        else:
            disabled_count += 1
        content_types.append({
            'id': content_type,
            'label': _display_label(content_type, info),
            'state': state,
            'canonical_request_supported': content_type in request_types,
            'gui_state_supported': content_type in gui_types,
            'selection_enabled': selectable,
            'request_plan_compatible': request_compatible,
            'allowed_modes': ['REVIEW', 'PRODUCTION'] if production_enabled else (['REVIEW'] if review_enabled else []),
            'selector_field': 'subtype_id' if content_type == 'visual_loops' else 'variant_id',
            'editable_fields': list(info.get('editable_fields', [])),
            'families': families,
            'family_count': len(families),
            'selector_count': sum(len(row['selectors']) for row in families),
            'reason_if_restricted': reason,
        })

    snapshot = {
        'schema': CATALOG_SCHEMA_ID,
        'schema_version': '1.0',
        'status': 'READ_ONLY_DYNAMIC_OPTIONS_PREPARE_ONLY',
        'identity': {'catalog_sha256': audit['catalog_sha256'], 'implementation_sha256': audit['implementation_sha256']},
        'content_types': content_types,
        'inventory_summary': {
            'content_type_count': len(content_types),
            'selection_enabled_content_type_count': active_count,
            'disabled_content_type_count': disabled_count,
            'family_count': family_total,
            'selector_count': selector_total,
            'longform_enabled': False,
        },
        'execution_boundary': {
            'catalog_source': 'D9.8_BUILD_CATALOG_FROM_CANONICAL_PRODUCER_SCHEMA',
            'GUI_SOURCE_MODIFIED': False,
            'request_created': False,
            'renderer_input_emitted': False,
            'renderer_dispatch_invoked': False,
            'media_created': False,
            'persisted': False,
            'release_authority': 'NONE',
        },
        'audit': {'source_pins': audit['source_pins'], 'active_type_contract_parity': audit['active_type_contract_parity'], 'longform_present_disabled': audit['longform_present_disabled']},
    }
    _validate_instance(root, CATALOG_SCHEMA_REL, snapshot)
    return snapshot

def _validate_instance(root: Path, rel: Path, instance: dict[str, Any]) -> None:
    try:
        import jsonschema
        schema = _read_json(root, rel)
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(instance), key=lambda e: (list(map(str, e.path)), e.message))
    except Exception as exc:
        raise SharedProductionGUICatalogError(f'Cannot validate {rel.as_posix()}: {exc}') from exc
    if errors:
        raise SharedProductionGUICatalogError(f'{rel.as_posix()} instance violation at {list(errors[0].path)}: {errors[0].message}')

def _content_row(snapshot: Mapping[str, Any], content_type: str) -> Mapping[str, Any]:
    for row in snapshot['content_types']:
        if row['id'] == content_type:
            return row
    raise SharedProductionGUICatalogError(f'Unknown content_type: {content_type}')

def get_family_options(content_type: str, mode: str = 'REVIEW', project_root: Path | str | None = None) -> list[dict[str, Any]]:
    if mode not in {'REVIEW', 'PRODUCTION'}:
        raise SharedProductionGUICatalogError(f'Unsupported mode: {mode}')
    snapshot = build_dynamic_gui_catalog(project_root)
    row = _content_row(snapshot, content_type)
    if mode not in row['allowed_modes']:
        raise SharedProductionGUICatalogError(f'Content type {content_type} is not selectable in mode {mode}: {row.get("reason_if_restricted")}')
    return row['families']

def get_selector_options(content_type: str, family_id: str, mode: str = 'REVIEW', project_root: Path | str | None = None) -> list[dict[str, Any]]:
    families = get_family_options(content_type, mode, project_root)
    match = [family for family in families if family['id'] == family_id]
    if len(match) != 1:
        raise SharedProductionGUICatalogError(f'Unknown family_id {family_id!r} for content_type {content_type!r}')
    if not match[0]['selection_enabled']:
        raise SharedProductionGUICatalogError(f'Family is disabled: {content_type}/{family_id}')
    return match[0]['selectors']

def resolve_gui_catalog_selection(content_type: str, family_id: str, selector_id: str, mode: str = 'REVIEW', project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    selectors = get_selector_options(content_type, family_id, mode, root)
    match = [item for item in selectors if item['id'] == selector_id]
    if len(match) != 1:
        raise SharedProductionGUICatalogError(f'Unknown selector_id {selector_id!r} for {content_type}/{family_id}')
    selector = match[0]
    selection: dict[str, Any] = {'content_type': content_type, 'family_id': family_id, selector['selector_field']: selector_id}
    try:
        canonical_selection = resolve_canonical_selection(selection, root)
    except Exception as exc:
        raise SharedProductionGUICatalogError(f'Canonical selector resolution rejected selection: {exc}') from exc
    result = {
        'schema': SELECTION_SCHEMA_ID,
        'schema_version': '1.0',
        'mode': mode,
        'content_type': content_type,
        'family_id': canonical_selection['family_id'],
        'selector_field': selector['selector_field'],
        'selector_id': selector_id,
        'selector_metadata': selector['metadata'],
        'selection': {
            'content_type': canonical_selection['content_type'],
            'family_id': canonical_selection['family_id'],
            'subtype_id': canonical_selection.get('subtype_id'),
            'variant_id': canonical_selection.get('variant_id'),
        },
        'request_plan_compatible': canonical_selection['request_plan_compatible'],
        'exact_concrete_grammar': bool(selector.get('concrete_variant', True)) if content_type == 'visual_loops' else None,
        'renderer_input_emitted': False,
        'media_created': False,
        'release_authority': 'NONE',
    }
    result['identity_sha256'] = _sha_value(result)
    _validate_instance(root, SELECTION_SCHEMA_REL, result)
    return result

def _json_out(value: Any) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n')

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Read-only D9 dynamic catalog for future GUI cascading controls')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--audit-only', action='store_true')
    group.add_argument('--catalog', action='store_true')
    group.add_argument('--families-for', metavar='CONTENT_TYPE')
    group.add_argument('--selectors-for', nargs=2, metavar=('CONTENT_TYPE','FAMILY_ID'))
    group.add_argument('--resolve-selection', nargs=3, metavar=('CONTENT_TYPE','FAMILY_ID','SELECTOR_ID'))
    parser.add_argument('--mode', choices=('REVIEW','PRODUCTION'), default='REVIEW')
    parser.add_argument('--project-root', type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        if args.audit_only:
            _json_out({'result':'PASS','audit':audit_dynamic_gui_catalog(args.project_root)})
        elif args.catalog:
            _json_out(build_dynamic_gui_catalog(args.project_root))
        elif args.families_for:
            _json_out({'content_type':args.families_for,'mode':args.mode,'families':get_family_options(args.families_for,args.mode,args.project_root)})
        elif args.selectors_for:
            content_type,family_id=args.selectors_for
            _json_out({'content_type':content_type,'family_id':family_id,'mode':args.mode,'selectors':get_selector_options(content_type,family_id,args.mode,args.project_root)})
        else:
            content_type,family_id,selector_id=args.resolve_selection
            _json_out(resolve_gui_catalog_selection(content_type,family_id,selector_id,args.mode,args.project_root))
        return 0
    except Exception as exc:
        _json_out({'result':'FAIL','error_type':type(exc).__name__,'error':str(exc),'renderer':'OFF','media_created':False,'release_authority':'NONE'})
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
