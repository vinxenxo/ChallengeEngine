# C11-D Editorial Field → Region → Visibility Reconciliation — Checkpoint V1

**State:** `PREPARATION_ONLY_RECONCILIATION_NOT_RENDERER_INPUT`  
**Date:** 2026-10-11  
**Scope:** fixed D9.9 editorial-field contracts for Challenges, Visual Loops and Visual Drills.  
**Approval:** proposal reconciliation only; no layout, field-window, renderer-baseline, production or release approval.

## Decision

Existing contracts already declare parts of the mapping, but in separate namespaces. This increment joins them into a single fail-closed 14-instance matrix without treating the join itself as approval or renderer input.

- Challenge D9.9 universal fields: `title`, `subtitle`, `call_to_action`, `player_name`, `challenge_label`; `language` is metadata only. Semantic region IDs are carried as proposals; Challenge D9.9 field-window mapping is not declared.
- Visual Loop and Visual Drill: `title` / `subtitle` route to semantic `HEADER`; `call_to_action` routes to semantic `FOOTER`; `language` remains metadata. The existing proposed rule gives non-empty visual fields a full continuous span based on the actual materialized payload's `frame_count`, but evaluated windows remain `null` because raw editorial values are not exposed by the current runtime summary.
- Challenge phase-field window policy remains its own namespace: `hook`, `reveal`, `cta`. It must not be implicitly aliased to D9.9 universal fields `title`, `subtitle`, or `call_to_action`. Similar names do not prove semantic identity.
- `CHALLENGE_OVERLAY` is a semantic role only. Its exploratory normalized bounds are not consumed; geometry remains `UNRESOLVED_NO_COORDINATES` and must resolve through the existing D1.5/profile/family hierarchy.

## Counts from the reconciled fixed review chain

| Measure | Result |
|---|---:|
| Content types | 3/3 |
| Canonical field instances | 14/14 |
| D9.9-to-review-chain parity | 14/14 |
| Visual field instances | 11 |
| Metadata-only `language` instances | 3 |
| Loop/Drill visibility rules declared but not evaluated | 6 |
| D9.9 universal Challenge fields with no window policy | 5 |
| Current visual payload consumption | 0/14 |
| Evaluated visibility windows | 0 |

## Artifacts

- `definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_ROUTING_VISIBILITY_RECONCILIATION_V1.json`
- `definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_ROUTING_VISIBILITY_RECONCILIATION_SCHEMA_V1.json`
- `tools/c11d/d9/d_renderer_editorial_field_routing_visibility_reconciliation.py`
- `tools/c11d/d9/test_d_renderer_editorial_field_routing_visibility_reconciliation.py`

The contract binds 27 source artifacts (24 upstream sources plus the schema, implementation and focused test) by SHA-256. The runner only builds and validates an in-memory reconciliation and writes no receipt. The strict contract schema is Draft 2020-12. Focused test: 13/13 PASS in the preparation environment.

## Next gate

Run the focused test on the operator's Windows checkout, then run the unified review, D9.13 lifecycle and candidate preflight. Do not register this test into the aggregate Suite until Windows acceptance. A later visual-field consumer must remain blocked until the routing/window policies are formally approved and an in-memory payload source exposes the exact raw editorial values. No inferred coordinates, durations, field aliases, simulation changes, renderer-native input, dispatch, media or release are permitted here.

## Governance locks

C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; media false; D4.8 BLOCKED; release authority NONE; D9.14/D9.16 blocked; D9.17 NO-GO; D10 BLOCKED; renderer and D baseline approvals remain absent.
