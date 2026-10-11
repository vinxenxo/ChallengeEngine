# Loop/Drill Editorial Field-Window Proposal — Unified Review Integration Checkpoint

**Date:** 2026-10-11  
**State:** INTEGRATED FOR REVIEW / NOT APPROVED  
**Scope:** C11-D D9 unified in-memory review; no renderer or media execution.

## Integration result

The unified review now validates the proposal contract at `definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json`, binds its declared fixtures to the materialized Visual Loop and Visual Drill payload identities and timings, and includes a dedicated cross-artifact check: `loop_drill_editorial_field_window_proposal_parity`.

- Unified content types: 3/3.
- Runtime harnesses: unchanged at 7/7; no new Godot harness was introduced.
- Cross-artifact checks: 13/13.
- Contract source lineage: 16/16.
- Frozen C11-C manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Unified status remains `REVIEW_CHAIN_CONSISTENT_NOT_VIDEO_READY`.

## Joined policy metadata

The review records the following proposal rules for both continuous content types:

- `title` and `subtitle` target `HEADER`; `call_to_action` targets `FOOTER`.
- A visual field is eligible only when its value is a non-empty string; its proposed interval is `[0, frame_count)` (zero-based, start-inclusive, end-exclusive).
- Empty values are suppressed with no window. `language` is metadata only. Unknown fields are rejected until explicitly mapped.
- No loop cycles or drill exercise subphases are inferred.

The current seven-harness runtime summary does not expose the raw editorial values for Loop/Drill. Therefore the unified manifest records the declared rules and payload frame count but leaves `visibility_windows` as `null`, explicitly marks `RAW_EDITORIAL_VALUES_NOT_EXPOSED_IN_RUNTIME_SUMMARY`, and does not claim that per-field evaluated windows have been computed. It neither rewrites editorial text nor emits renderer-native input.

## Gates and governance

The previous `...FIELD_MAPPING_UNDECLARED` labels are now `VISUAL_LOOP_EDITORIAL_FIELD_MAPPING_NOT_APPROVED` and `VISUAL_DRILL_EDITORIAL_FIELD_MAPPING_NOT_APPROVED`. The number of unresolved gates remains eight: the proposal is joined and verifiable, but not approved. The broader `EDITORIAL_FIELD_WINDOW_POLICY_NOT_APPROVED` gate remains open as well.

- `loop_editorial_field_mapping_approved=false`
- `drill_editorial_field_mapping_approved=false`
- `loop_drill_editorial_field_window_policy_approved=false`
- `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`
- No persistent report, payload files, production execution, or changes to frozen C11-C simulation truth.

## Validation performed in the preparation workspace

- Loop/Drill proposal tests: 22/22 PASS.
- Coordinate/sample composition proposal tests: 18/18 PASS.
- Challenge sample-selection proposal negatives: 22/22 PASS.
- Coordinate-projection contract: 18 unit tests PASS; source pins 13/13.
- Delivery timebase projection: 42 negative controls PASS; challenge 900@60 FPS to 450@30 FPS.
- Challenge delivery timeline: 55 negative controls PASS.
- Unified review contract: 20 unit tests PASS; schema and JSON Schema PASS; lineage 16/16; cross-checks 13/13.

The new seven-harness Godot orchestration has **not** been executed in the preparation environment after this integration. It must be run in the operator's Windows checkout before marking the integrated runtime review green. The focused Python tests do not substitute for that run.

## Next action

Apply `C11D_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_UNIFIED_REVIEW_INTEGRATION_OVERLAY_V1.zip`, run the proposal, unified review, lifecycle, baseline-candidate preflight and aggregate suite in Windows, and preserve the eight unresolved gates. Do not approve the policy or enable the renderer merely because contracts pass.

## Joined field-routing/visibility matrix — 2026-10-11

`D_RENDERER_EDITORIAL_FIELD_ROUTING_VISIBILITY_RECONCILIATION_CHECKPOINT_V1.md` now cross-checks the Loop/Drill mapping alongside semantic region routing for all three content types. The six full-span Loop/Drill rules remain proposed, are not evaluated to concrete per-field windows, and are not approved. Current runtime summary does not expose the raw editorial values, so `visibility_windows` continues to be `null`. This matrix does not modify this integration's contracts or add a harness.
