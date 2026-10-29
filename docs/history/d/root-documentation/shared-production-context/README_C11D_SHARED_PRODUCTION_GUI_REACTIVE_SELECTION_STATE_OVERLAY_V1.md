# C11-D Shared Production GUI Reactive Selection State Overlay V1

Additive, D-owned state-machine contract for cascading controls in the future GUI. This overlay does not modify current GUI widgets and is not connected to the current GUI source.

## Included files

- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_REACTIVE_SELECTION_STATE_CONTRACT_V1.json`
- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_REACTIVE_SELECTION_STATE_CONTRACT_SCHEMA_V1.json`
- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_REACTIVE_SELECTION_STATE_SCHEMA_V1.json`
- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_REACTIVE_SELECTION_SNAPSHOT_SCHEMA_V1.json`
- `tools/c11d/d9/shared_production_context_gui_reactive_selection.py`
- `tools/c11d/d9/test_shared_production_context_gui_reactive_selection.py`
- `docs/current/d/D_RENDERER_SHARED_PRODUCTION_GUI_REACTIVE_SELECTION_STATE_CHECKPOINT_V1.md`
- this README

## API

- `initialize_gui_reactive_selection_state(mode='REVIEW', project_root=None)`
- `transition_gui_reactive_selection_state(current_state, event, project_root=None)`
- CLI: `--audit-only`, `--initialize --mode REVIEW|PRODUCTION`, or `--transition --state-json JSON --event-json JSON`

Supported events: `set_mode`, `select_content_type`, `select_family`, `select_selector`, `clear_selection`, `refresh_catalog`.

## Semantics

- No type, family or selector is auto-selected.
- Changing content type clears family and selector descendants; changing family clears the selector.
- A mode change retains selections only while each remains valid. When the selected content type is not available in the new mode, the type stays visible but descendants are cleared with a reason.
- Unknown choices are rejected, not substituted.
- Stale catalog state is rejected until explicit `refresh_catalog`, which reconciles and clears invalid paths.
- API/CLI snapshots are deterministic and hash-bound; state is transient and no files are written.
- The final selector path delegates to the canonical D9.8 resolver. This does not create a D9.9 production request.

Governance stays locked: `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`; D9.17 remains NO-GO and D10 blocked.
