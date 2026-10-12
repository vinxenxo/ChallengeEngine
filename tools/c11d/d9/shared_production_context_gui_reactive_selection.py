"""Fail-closed reactive selection state for the future D9 GUI.

This module only handles cascading selection state. Options come from the
canonical D9.8 catalog, semantic selector validation delegates to its existing
resolver, and no request is created or persisted here.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from shared_production_context_gui_catalog import (
    SharedProductionGUICatalogError,
    build_dynamic_gui_catalog,
    resolve_gui_catalog_selection,
)

CONTRACT_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_REACTIVE_SELECTION_STATE_CONTRACT_V1.json')
CONTRACT_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_REACTIVE_SELECTION_STATE_CONTRACT_SCHEMA_V1.json')
STATE_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_REACTIVE_SELECTION_STATE_SCHEMA_V1.json')
SNAPSHOT_SCHEMA_REL = Path('definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_REACTIVE_SELECTION_SNAPSHOT_SCHEMA_V1.json')
CONTRACT_ID = 'C11-D-D9-SHARED-PRODUCTION-GUI-REACTIVE-SELECTION-STATE-CONTRACT-V1'
STATE_ID = 'C11-D-SHARED-GUI-REACTIVE-SELECTION-STATE-V1'
SNAPSHOT_ID = 'C11-D-SHARED-GUI-REACTIVE-SELECTION-SNAPSHOT-V1'
MANIFEST_SHA256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
STATE_KEYS = {'schema','schema_version','mode','catalog_sha256','selection'}
SELECTION_KEYS = {'content_type','family_id','selector_field','selector_id'}

class SharedProductionGUIReactiveSelectionError(ValueError):
    """Raised when a GUI selection transition is invalid or stale."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT

def _read_json(root: Path, rel: Path) -> Any:
    try:
        return json.loads((root / rel).read_text(encoding='utf-8-sig'))
    except Exception as exc:
        raise SharedProductionGUIReactiveSelectionError(f'Cannot read {rel.as_posix()}: {exc}') from exc

def _sha_file(root: Path, rel: str) -> str:
    try:
        return hashlib.sha256((root / rel).read_bytes()).hexdigest()
    except Exception as exc:
        raise SharedProductionGUIReactiveSelectionError(f'Cannot hash source {rel}: {exc}') from exc

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

def _validate_instance(root: Path, rel: Path, value: dict[str, Any]) -> None:
    try:
        import jsonschema
        schema = _read_json(root, rel)
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(value), key=lambda e: (list(map(str,e.path)),e.message))
    except Exception as exc:
        raise SharedProductionGUIReactiveSelectionError(f'Schema validation failed for {rel.as_posix()}: {exc}') from exc
    if errors:
        err = errors[0]
        raise SharedProductionGUIReactiveSelectionError(f'{rel.as_posix()} instance violation at {list(err.path)}: {err.message}')

def audit_reactive_selection_contract(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract = _read_json(root, CONTRACT_REL)
    contract_schema = _read_json(root, CONTRACT_SCHEMA_REL)
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(contract_schema)
        jsonschema.Draft202012Validator.check_schema(_read_json(root, STATE_SCHEMA_REL))
        jsonschema.Draft202012Validator.check_schema(_read_json(root, SNAPSHOT_SCHEMA_REL))
        errors = sorted(jsonschema.Draft202012Validator(contract_schema).iter_errors(contract), key=lambda e: (list(map(str,e.path)),e.message))
    except Exception as exc:
        raise SharedProductionGUIReactiveSelectionError(f'Invalid reactive selection contract/schema: {exc}') from exc
    if errors:
        raise SharedProductionGUIReactiveSelectionError(f'Contract schema violation: {errors[0].message}')
    if contract.get('schema') != CONTRACT_ID or contract.get('status') != 'PREPARE_ONLY_REACTIVE_CASCADING_STATE_NO_GUI_WIDGET_MODIFICATION':
        raise SharedProductionGUIReactiveSelectionError('Reactive selection contract identity/status mismatch')
    expected = {
        'implementation_sha256': _sha_file(root, 'tools/c11d/d9/shared_production_context_gui_reactive_selection.py'),
        'contract_schema_sha256': _sha_file(root, CONTRACT_SCHEMA_REL.as_posix()),
        'state_schema_sha256': _sha_file(root, STATE_SCHEMA_REL.as_posix()),
        'snapshot_schema_sha256': _sha_file(root, SNAPSHOT_SCHEMA_REL.as_posix()),
    }
    for key, digest in expected.items():
        if contract.get(key) != digest:
            raise SharedProductionGUIReactiveSelectionError(f'Pinned {key} mismatch')
    lineage = contract.get('source_lineage')
    if not isinstance(lineage, list) or len(lineage) != 9:
        raise SharedProductionGUIReactiveSelectionError('Expected nine canonical source pins')
    seen: set[str] = set()
    for row in lineage:
        if not isinstance(row, dict) or set(row) != {'path','role','sha256'}:
            raise SharedProductionGUIReactiveSelectionError('Malformed source lineage row')
        rel, digest = row['path'], row['sha256']
        if not isinstance(rel,str) or not rel or rel.startswith('/') or '\\' in rel or any(part in ('','.','..') for part in rel.split('/')):
            raise SharedProductionGUIReactiveSelectionError(f'Unsafe source path: {rel!r}')
        if rel in seen:
            raise SharedProductionGUIReactiveSelectionError(f'Duplicate source pin: {rel}')
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
            raise SharedProductionGUIReactiveSelectionError(f'Invalid SHA-256: {rel}')
        if _sha_file(root,rel) != digest:
            raise SharedProductionGUIReactiveSelectionError(f'Pinned source drift: {rel}')
        seen.add(rel)
    if lineage[0]['path'] != 'release/C11C_FREEZE_PACKAGE_MANIFEST.json' or lineage[0]['sha256'] != MANIFEST_SHA256:
        raise SharedProductionGUIReactiveSelectionError('Frozen C11-C manifest must lead the source lineage')
    # Delegate integrity of the underlying catalog and canonical state mapper to their own auditors.
    try:
        from shared_production_context_gui_catalog import audit_dynamic_gui_catalog
        from shared_production_context_gui_state import audit_gui_state_contract
        catalog_audit = audit_dynamic_gui_catalog(root)
        state_audit = audit_gui_state_contract(root)
    except Exception as exc:
        raise SharedProductionGUIReactiveSelectionError(f'Parent catalog/state contract failed: {exc}') from exc
    return {
        'source_pins': len(lineage),
        'parent_catalog_source_pins': catalog_audit['source_pins'],
        'parent_state_source_pins': state_audit['source_pins'],
        'implementation_sha256': expected['implementation_sha256'],
        'renderer': 'OFF', 'media_created': False, 'D4.8': 'BLOCKED', 'release_authority': 'NONE',
    }

def _empty_selection() -> dict[str, Any]:
    return {'content_type': None, 'family_id': None, 'selector_field': None, 'selector_id': None}

def _validate_state_shape(state: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(state, Mapping) or set(state) != STATE_KEYS:
        raise SharedProductionGUIReactiveSelectionError('State must contain exactly schema, schema_version, mode, catalog_sha256 and selection')
    if state.get('schema') != STATE_ID or state.get('schema_version') != '1.0':
        raise SharedProductionGUIReactiveSelectionError('Reactive GUI state schema identity mismatch')
    if state.get('mode') not in {'REVIEW','PRODUCTION'}:
        raise SharedProductionGUIReactiveSelectionError('Unsupported mode')
    selection = state.get('selection')
    if not isinstance(selection, Mapping) or set(selection) != SELECTION_KEYS:
        raise SharedProductionGUIReactiveSelectionError('Selection must contain exactly content_type, family_id, selector_field and selector_id')
    ct, fam, field, selector = (selection[k] for k in ('content_type','family_id','selector_field','selector_id'))
    for key, val in [('content_type',ct),('family_id',fam),('selector_field',field),('selector_id',selector)]:
        if val is not None and not isinstance(val,str):
            raise SharedProductionGUIReactiveSelectionError(f'{key} must be a string or null')
    if ct is None and (fam is not None or field is not None or selector is not None):
        raise SharedProductionGUIReactiveSelectionError('Descendant selections require a content_type')
    if fam is None and (field is not None or selector is not None):
        raise SharedProductionGUIReactiveSelectionError('Selector fields require a family_id')
    if selector is None and field is not None:
        raise SharedProductionGUIReactiveSelectionError('selector_field must be null until a selector_id is chosen')
    if selector is not None and (field is None or fam is None or ct is None):
        raise SharedProductionGUIReactiveSelectionError('A selector requires a complete content_type/family_id/selector_field path')
    digest = state.get('catalog_sha256')
    if not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
        raise SharedProductionGUIReactiveSelectionError('Invalid catalog_sha256')
    return copy.deepcopy(dict(state))

def _find_content(catalog: Mapping[str, Any], content_type: str | None) -> dict[str, Any] | None:
    if content_type is None: return None
    return next((r for r in catalog['content_types'] if r.get('id')==content_type),None)

def _mode_allowed(row: Mapping[str, Any] | None, mode: str) -> bool:
    return bool(row and row.get('selection_enabled') is True and mode in row.get('allowed_modes',[]))

def _find_family(content_row: Mapping[str, Any] | None, family_id: str | None) -> dict[str, Any] | None:
    if content_row is None or family_id is None: return None
    return next((r for r in content_row.get('families',[]) if r.get('id')==family_id),None)

def _find_selector(family_row: Mapping[str, Any] | None, selector_id: str | None) -> dict[str, Any] | None:
    if family_row is None or selector_id is None: return None
    return next((r for r in family_row.get('selectors',[]) if r.get('id')==selector_id),None)

def _clear_selector(state: dict[str, Any], invalidated: list[str]) -> None:
    sel=state['selection']
    for key in ('selector_field','selector_id'):
        if sel[key] is not None and key not in invalidated: invalidated.append(key)
        sel[key]=None

def _clear_family(state: dict[str, Any], invalidated: list[str]) -> None:
    sel=state['selection']
    _clear_selector(state,invalidated)
    if sel['family_id'] is not None and 'family_id' not in invalidated: invalidated.append('family_id')
    sel['family_id']=None

def _reconcile(state: dict[str, Any], catalog: Mapping[str, Any], invalidated: list[str]) -> str | None:
    sel=state['selection']; ctrow=_find_content(catalog,sel['content_type'])
    if sel['content_type'] is not None and ctrow is None:
        _clear_family(state, invalidated)
        if 'content_type' not in invalidated: invalidated.append('content_type')
        sel['content_type']=None
        return 'CONTENT_TYPE_NO_LONGER_REGISTERED'
    if sel['content_type'] is None: return None
    if not _mode_allowed(ctrow,state['mode']):
        _clear_family(state,invalidated); return 'CONTENT_TYPE_NOT_ALLOWED_IN_MODE'
    famrow=_find_family(ctrow,sel['family_id'])
    if sel['family_id'] is not None and (famrow is None or not _mode_allowed(famrow,state['mode'])):
        _clear_family(state,invalidated); return 'FAMILY_NO_LONGER_VALID'
    if sel['family_id'] is None: return None
    selector=_find_selector(famrow,sel['selector_id'])
    if sel['selector_id'] is not None and (selector is None or selector.get('selector_field') != sel['selector_field']):
        _clear_selector(state,invalidated); return 'SELECTOR_NO_LONGER_VALID'
    return None

def _validate_transition_event(event: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(event, Mapping) or 'action' not in event:
        raise SharedProductionGUIReactiveSelectionError('Transition event must be an object with action')
    action=event.get('action')
    fields={
      'set_mode': {'action','mode'},
      'select_content_type': {'action','content_type'},
      'select_family': {'action','family_id'},
      'select_selector': {'action','selector_id'},
      'clear_selection': {'action'},
      'refresh_catalog': {'action'},
    }
    if action not in fields:
        raise SharedProductionGUIReactiveSelectionError(f'Unknown transition action: {action!r}')
    if set(event) != fields[action]:
        raise SharedProductionGUIReactiveSelectionError(f'Unexpected or missing event field(s) for {action}')
    return dict(event)

def _compose(snapshot: Mapping[str, Any], state: dict[str, Any], action: str, invalidated: list[str], reason: str | None, refreshed: bool, root: Path) -> dict[str, Any]:
    catalog_row=_find_content(snapshot,state['selection']['content_type'])
    content_types=[]
    for row in snapshot['content_types']:
        copyrow=copy.deepcopy(row); copyrow['selectable_in_mode']=_mode_allowed(row,state['mode']); content_types.append(copyrow)
    families=[]; selectors=[]
    if _mode_allowed(catalog_row,state['mode']):
        families=[copy.deepcopy(f) for f in catalog_row.get('families',[]) if _mode_allowed(f,state['mode'])]
    family_row=_find_family(catalog_row,state['selection']['family_id'])
    if _mode_allowed(catalog_row,state['mode']) and _mode_allowed(family_row,state['mode']):
        selectors=[copy.deepcopy(s) for s in family_row.get('selectors',[]) if s.get('selector_field')==family_row.get('selector_field')]
    selection=state['selection']
    complete=bool(selection['content_type'] and selection['family_id'] and selection['selector_field'] and selection['selector_id'])
    resolved=None; exact=None; canonical_ok=False; blockers=[]
    if not selection['content_type']:
        blockers.append('CONTENT_TYPE_NOT_SELECTED')
    else:
        ctrow=_find_content(snapshot,selection['content_type'])
        if not _mode_allowed(ctrow,state['mode']): blockers.append('CONTENT_TYPE_NOT_ALLOWED_IN_MODE')
        if not selection['family_id']: blockers.append('FAMILY_NOT_SELECTED')
        if not selection['selector_id']: blockers.append('SELECTOR_NOT_SELECTED')
    if complete and not blockers:
        try:
            resolved_record=resolve_gui_catalog_selection(selection['content_type'],selection['family_id'],selection['selector_id'],state['mode'],root)
            if resolved_record['selector_field'] != selection['selector_field']:
                raise SharedProductionGUIReactiveSelectionError('Canonical selector field drift')
            resolved=resolved_record['selection']; exact=resolved_record.get('exact_concrete_grammar')
            canonical_ok=True
        except Exception as exc:
            blockers.append('CANONICAL_SELECTION_REJECTED')
            if reason is None: reason=f'Canonical selection not resolved: {exc}'
    output={
      'schema':SNAPSHOT_ID,'schema_version':'1.0','state':state,
      'available':{'modes':['REVIEW','PRODUCTION'],'content_types':content_types,'families':families,'selectors':selectors},
      'transition':{'action':action.upper(),'invalidated_fields':sorted(set(invalidated)),'catalog_refreshed':bool(refreshed),'reason':reason},
      'readiness':{'selection_path_complete':complete,'canonical_selection_resolved':canonical_ok,'canonical_selection':resolved,'exact_concrete_selector':exact,'blockers':blockers},
      'identity':{'catalog_sha256':snapshot['identity']['catalog_sha256']},
      'execution_boundary':{'request_created':False,'renderer_input_emitted':False,'renderer_dispatch_invoked':False,'media_created':False,'persisted':False,'release_authority':'NONE'}
    }
    output['identity']['snapshot_sha256']=_sha_value(output)
    _validate_instance(root,SNAPSHOT_SCHEMA_REL,output)
    return output

def initialize_gui_reactive_selection_state(mode: str = 'REVIEW', project_root: Path | str | None = None) -> dict[str, Any]:
    root=_root(project_root)
    if mode not in {'REVIEW','PRODUCTION'}: raise SharedProductionGUIReactiveSelectionError(f'Unsupported mode: {mode!r}')
    audit_reactive_selection_contract(root)
    snapshot=build_dynamic_gui_catalog(root)
    state={'schema':STATE_ID,'schema_version':'1.0','mode':mode,'catalog_sha256':snapshot['identity']['catalog_sha256'],'selection':_empty_selection()}
    _validate_instance(root,STATE_SCHEMA_REL,state)
    return _compose(snapshot,state,'INITIALIZE',[],None,False,root)

def transition_gui_reactive_selection_state(current_state: Mapping[str, Any], event: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    root=_root(project_root)
    audit_reactive_selection_contract(root)
    state=_validate_state_shape(current_state)
    _validate_instance(root,STATE_SCHEMA_REL,state)
    event=_validate_transition_event(event)
    snapshot=build_dynamic_gui_catalog(root)
    catalog_hash=snapshot['identity']['catalog_sha256']
    action=event['action']
    refreshed=False; invalidated: list[str]=[]; reason=None
    if state['catalog_sha256'] != catalog_hash and action != 'refresh_catalog':
        raise SharedProductionGUIReactiveSelectionError('Stale GUI selection state: canonical catalog identity changed; use refresh_catalog')
    state['catalog_sha256']=catalog_hash
    sel=state['selection']
    if action=='set_mode':
        new_mode=event['mode']
        if new_mode not in {'REVIEW','PRODUCTION'}: raise SharedProductionGUIReactiveSelectionError(f'Unsupported mode: {new_mode!r}')
        changed=new_mode != state['mode']; state['mode']=new_mode
        if changed: reason=_reconcile(state,snapshot,invalidated)
    elif action=='select_content_type':
        content_type=event['content_type']; row=_find_content(snapshot,content_type)
        if row is None: raise SharedProductionGUIReactiveSelectionError(f'Unknown content type: {content_type!r}')
        if not _mode_allowed(row,state['mode']): raise SharedProductionGUIReactiveSelectionError(f'Content type is not selectable in {state["mode"]}: {content_type}')
        if sel['content_type'] != content_type:
            if sel['content_type'] is not None: invalidated.append('content_type')
            _clear_family(state,invalidated); sel['content_type']=content_type
    elif action=='select_family':
        ctrow=_find_content(snapshot,sel['content_type'])
        if not _mode_allowed(ctrow,state['mode']): raise SharedProductionGUIReactiveSelectionError('Select an available content type before selecting a family')
        family_id=event['family_id']; family=_find_family(ctrow,family_id)
        if not _mode_allowed(family,state['mode']): raise SharedProductionGUIReactiveSelectionError(f'Unknown or unavailable family: {family_id!r}')
        if sel['family_id'] != family_id:
            _clear_selector(state,invalidated); sel['family_id']=family_id
            sel['selector_field']=None; sel['selector_id']=None
    elif action=='select_selector':
        ctrow=_find_content(snapshot,sel['content_type']); family=_find_family(ctrow,sel['family_id'])
        if not _mode_allowed(ctrow,state['mode']) or not _mode_allowed(family,state['mode']):
            raise SharedProductionGUIReactiveSelectionError('Select an available content type and family before selecting a subtype/variant')
        selector_id=event['selector_id']; selector=_find_selector(family,selector_id)
        if selector is None: raise SharedProductionGUIReactiveSelectionError(f'Unknown selector: {selector_id!r}')
        if selector.get('selector_field') != family.get('selector_field'):
            raise SharedProductionGUIReactiveSelectionError('Selector field is incompatible with selected family')
        sel['selector_field']=selector['selector_field']; sel['selector_id']=selector_id
        try:
            canonical=resolve_gui_catalog_selection(sel['content_type'],sel['family_id'],selector_id,state['mode'],root)
            if canonical['selector_field'] != sel['selector_field']:
                raise SharedProductionGUIReactiveSelectionError('Canonical selector-field mismatch')
        except Exception as exc:
            _clear_selector(state,invalidated)
            raise SharedProductionGUIReactiveSelectionError(f'Canonical selector rejected selection: {exc}') from exc
    elif action=='clear_selection':
        for key,val in sel.items():
            if val is not None: invalidated.append(key)
        state['selection']=_empty_selection()
    elif action=='refresh_catalog':
        reason=_reconcile(state,snapshot,invalidated); refreshed=True
    return _compose(snapshot,state,action,invalidated,reason,refreshed,root)

def _json_out(value: Any) -> None:
    sys.stdout.write(json.dumps(_canonical(value),ensure_ascii=True,allow_nan=False,separators=(',',':'),sort_keys=True)+'\n')

def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description='Read-only cascading state machine for future D9 GUI controls')
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--audit-only',action='store_true')
    group.add_argument('--initialize',action='store_true')
    group.add_argument('--transition',action='store_true')
    parser.add_argument('--mode',choices=('REVIEW','PRODUCTION'),default='REVIEW')
    parser.add_argument('--state-json')
    parser.add_argument('--event-json')
    parser.add_argument('--project-root',type=Path,default=None)
    args=parser.parse_args(argv)
    try:
        if args.audit_only: result={'result':'PASS','audit':audit_reactive_selection_contract(args.project_root)}
        elif args.initialize: result=initialize_gui_reactive_selection_state(args.mode,args.project_root)
        else:
            if not args.state_json or not args.event_json: raise SharedProductionGUIReactiveSelectionError('--transition requires --state-json and --event-json')
            state=json.loads(args.state_json); event=json.loads(args.event_json)
            result=transition_gui_reactive_selection_state(state,event,args.project_root)
        _json_out(result); return 0
    except Exception as exc:
        _json_out({'result':'FAIL','error_type':type(exc).__name__,'error':str(exc),'renderer':'OFF','media_created':False,'release_authority':'NONE'})
        return 2

if __name__=='__main__':
    raise SystemExit(main())
