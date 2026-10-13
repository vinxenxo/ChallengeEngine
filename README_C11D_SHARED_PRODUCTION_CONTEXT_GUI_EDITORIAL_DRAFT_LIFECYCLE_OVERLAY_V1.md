# C11-D Shared Production GUI Editorial Draft Lifecycle Overlay V1

Additive D-owned data lifecycle for the future GUI. The overlay adds the draft state/contract schemas, a Python state service and focused tests, and a checkpoint. The current Master Handover and Start Prompt must be updated additively with the supplied in-chat PowerShell block so that pre-existing operator edits are preserved.

## Included files

- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_DRAFT_LIFECYCLE_CONTRACT_V1.json`
- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_DRAFT_LIFECYCLE_CONTRACT_SCHEMA_V1.json`
- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_DRAFT_STATE_SCHEMA_V1.json`
- `tools/c11d/d9/shared_production_context_gui_editorial_draft.py`
- `tools/c11d/d9/test_shared_production_context_gui_editorial_draft.py`
- `docs/current/d/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_DRAFT_LIFECYCLE_CHECKPOINT_V1.md`
- this README

## Field lifecycle semantics

Common overrides (`title`, `subtitle`, `call_to_action`, `language`) survive content-type/family/selector changes. Challenge-only overrides (`player_name`, `challenge_label`) are accepted only while the selected type is Challenges and are deleted when leaving Challenges. No dormant stash is retained. Clearing an override deletes it to allow D9.8 profile inheritance; explicitly writing an empty string means D9.8 normalization to `UNKNOWN`.

## API

See the checkpoint. Effective values are resolved only via the canonical D9.8 editorial model. Field lengths use the stricter maximum from D9.8 and the canonical GUI-state request schema. Draft state is in-memory, schema-validated and hash-sealed. This does not create a D9.9 production request.

## Governance

No current GUI widget changes; no state persistence; no renderer input or dispatch; no media. C11-C is immutable. `renderer=OFF`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.17 remains NO-GO, and D10 remains blocked.
