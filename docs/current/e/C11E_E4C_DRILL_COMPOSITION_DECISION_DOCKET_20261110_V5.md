# C11-E E4C Drill composition and timebase decision docket — V4 (2026-11-10)

**State:** `BOTH_NEW_DRILL_DECISIONS_APPROVED_AS_PROPOSED_FOR_D_OWNED_DESIGN_AND_CONTRACT_IMPLEMENTATION_ONLY`.

## Prior exact-hash decisions retained

The operator policy record `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04` already approves A.1, A.3, E4B Loop composition, B.1 and D.1 within their recorded limits. B.1 preserves cadence/frame order/duration without resampling but did not itself decide the Drill phase offset. D.1 is only a technical delivery envelope; it does not authorize audio selection, generation, mixing, mastering or loudness behavior.

## New operator record

The explicit operator decision message `APPROVED AS PROPOSAL` is recorded in:

- `docs/current/e/C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json`
- SHA-256: `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`

The record binds each decision to its exact proposal and schema hashes. Both proposal files remain byte-identical and continue to carry `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`; approval is represented only in the separate decision record.

## Decision 1 — Drill outer-band geometry — APPROVED_AS_PROPOSED

- Proposal: `definitions/c11d/production/C11E_E4C_DRILL_EDITORIAL_COMPOSITION_PROPOSAL_V1.json`
- SHA-256: `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09`
- Schema SHA-256: `3684316e98ab2054bd913df17c6e398d8040d047027de36332690cfd2be517bc`
- Geometry: 720×1280 REVIEW_720; 192px top/bottom bands; 504×896 uniformly-contained original C11-C viewport at x=108,y=192; no crop/stretch/resampling.
- Visibility: D editorial visible only during GAME; suppressed during PRE_ROLL and END_CTA. Native `VisualDrillEndCTA` and C11-C source frame ownership remain intact.

## Decision 2 — GAME payload to final-presentation timebase — APPROVED_AS_PROPOSED

- Proposal: `definitions/c11d/production/C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_V1.json`
- SHA-256: `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8`
- Schema SHA-256: `c5cedcd749a6702dc47b1de0bd67c57721bb9a06cee5cb3709cdc1b17d8a6806`
- Mapping: `final_presentation_frame_index = pre_roll_frames + game_payload_frame_index`.
- At 30fps / 630 GAME frames: PRE_ROLL `[0,90)`, GAME `[90,720)`, END_CTA `[720,810)`.
- No frame-rate resampling, frame reordering or C11-C source mutation. D editorial remains GAME-only; native END_CTA is preserved.

## Authorization boundary and next gate

The two approvals authorize D-owned design/contract implementation and focused isolated visual/pixel tests only. They do **not** authorize renderer-native input, renderer activation, production dispatch, media creation, audio selection/generation/materialization, C11-C source/mechanics modification, release promotion or cutover. `release_authority=NONE`; D4.8 remains BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION.

Next: install the V4 reconciliation overlay successfully, verify receipt and postimages, then implement the single D-owned Drill visual consumer at the existing boundary and prove phase visibility, font shaping/coverage, clipping/overflow/contrast and deterministic pixel/source identity across all 20 selectors. Native A/V remains a later separate gate using silent protected C11-C capture and existing `FAMILY_MUSIC_V4`; these approvals do not grant audio-generation authority.


Installer recovery note: V3 passed AST, inventory, pins, destination-state and short-stage-root checks, then failed closed in staged validation under StrictMode because a mode-based filter traversed the three non-payload manifest metadata rows. V4 scopes these filters to `$operationEntries` (29 payload operations). Both earlier attempts stopped pre-transaction; V4 is the next active-checkout test gate.
