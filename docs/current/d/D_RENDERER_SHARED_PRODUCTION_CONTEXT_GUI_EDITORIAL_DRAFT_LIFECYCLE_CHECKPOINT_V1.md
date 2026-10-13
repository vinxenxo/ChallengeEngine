# D9 — Shared Production GUI Editorial Draft Lifecycle V1

**Status:** `PREPARE_ONLY_EDITORIAL_DRAFT_NO_GUI_WIDGET_MODIFICATION`  
**Windows acceptance:** pending operator execution of the focused test and regressions  
**Renderer/media authority:** none

## Purpose

Provide a D-owned, request-scoped editorial draft lifecycle for the future GUI. The lifecycle consumes snapshots from the canonical reactive GUI selection state, stores editable text overrides separately from the configured D9.8 editorial profile, and delegates effective-value resolution to `universal_editorial_model.resolve_editorial_values`.

## Canonical field policy

- Shared fields are `title`, `subtitle`, `call_to_action`, and `language` for Challenges, Visual Loops, and Visual Drills.
- Challenge-only fields are `player_name` and `challenge_label`. They are exposed only while the active content type is `challenges`.
- A type/family/selector transition preserves shared draft overrides.
- A transition away from Challenges deletes Challenge-only request overrides; they are not hidden in a stash and are not restored if the user later returns to Challenges.
- Changing family or selector within Challenges preserves Challenge-only overrides because the content type still allows them.
- `clear_gui_editorial_draft_override` removes a key so D9.8 can inherit the selected profile value. An explicit empty-string override is not the same action: D9.8 normalizes it to `UNKNOWN` and therefore it overrides a higher-layer profile value.
- Text edit length is checked against the stricter maximum declared by the D9.8 model and canonical GUI-state request schema, so the draft cannot accept a value that the eventual canonical request mapper must reject.
- Reserved editorial fields and telemetry/provenance fields are rejected.

## API

- `initialize_gui_editorial_draft_state(selection_snapshot, profile=None, project_root=None)`
- `transition_gui_editorial_draft_state(current_state, selection_snapshot, project_root=None)`
- `set_gui_editorial_draft_override(current_state, field, value, project_root=None)`
- `clear_gui_editorial_draft_override(current_state, field, project_root=None)`
- `preview_gui_editorial_draft(current_state, project_root=None)`
- CLI: `--audit-only`, `--initialize-from-snapshot-json`, `--transition`, `--set-field`, `--clear-field`, `--preview`

The draft state is hash-sealed and strict-schema validated. The reactive snapshot's catalog identity and snapshot digest must validate against the current canonical catalog. A catalog identity change is rejected unless the incoming snapshot came from an explicit `refresh_catalog` transition. Incomplete selection paths return `SELECTION_INCOMPLETE` without resolving values. Complete paths use D9.8 for all effective value resolution.

## Tests

The focused test covers source pins and schemas, incomplete states, common-field persistence across family/selector transitions, Challenge-only field visibility and deletion, profile inheritance after clearing an override, explicit-empty semantics, reserved/unknown/overlong rejection, draft and snapshot hash drift, explicit catalog refresh requirements, ASCII-safe CLI audit, and byte-exact source restoration after a negative drift test.

## Execution boundary and governance

This is a data/state preparation service only. It does not modify GUI widgets, create canonical production requests, persist state, emit renderer-native input, dispatch rendering, execute shaders, or create media. C11-C remains immutable; renderer OFF; `media_created=false`; D4.8 BLOCKED; `release_authority=NONE`; D9.17 NO-GO; D10 blocked.

## Required Windows validation

Run `test_shared_production_context_gui_editorial_draft.py`, then `shared_production_context_gui_editorial_draft.py --audit-only`, then the parent GUI reactive-selection/catalog/state/facade and D9.8–D9.10 regression tests and the baseline candidate preflight. Do not mark Windows acceptance PASS before the operator supplies the actual results.
