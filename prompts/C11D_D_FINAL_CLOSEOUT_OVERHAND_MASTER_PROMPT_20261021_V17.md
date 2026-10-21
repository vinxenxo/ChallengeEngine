# C11-D Final Closeout Overhand Master Prompt — V17 (2026-10-21)

## Objective

Drive C11-D to a deterministic, renderer-agnostic production system and the earliest safely authorized real-render test on a formal D baseline. The long-term goal is to replace frozen C11-C only after D acceptance, baseline approval, freeze and controlled promotion. Do not mistake a test PASS or a proposal decision for release authority.

## Repository and immutable baseline

Authoritative Windows checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Apply only minimal verified ADD_ONLY overlays from the root. Require ZIP/manifest/hash/precondition checks, exact destination absence, post-copy verification, pin reconciliation and rollback on partial failure. Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Never modify it or bulk-extract a context ZIP over the checkout.

## Current V2-B verified milestones

- Design: 90/90 static tests.
- Runtime implementation: 198/198 static tests; receipt `e64cfd259914c471d03e8578b955140ad487b04694c5f682834517d823fcbfc4`.
- Runtime seed-sensitivity matrix: 45/45 planner invocations, 45/45 independent Godot 4.7.1 Mono processes, 9/9 selectors; report `f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446`.
- Candidate audit: 9/9 selectors, 45/45 runtime, six typed candidates, no raw candidate values; audit `8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00`.
- Semantic request: 75/75; request `b576612dd0913ce8f706a5272a5b9ca5ceb6c7a1f39d832323d9db98578b5d01`.
- Semantic decision record: 146/146 Windows tests; record `cc3550cd4d13f228ec9b3d51eeaa199505c5975b42882fb06ba3e83c4a000e90`; receipt `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`.
- Field-region/visibility proposal: 551/551 Windows tests; receipt `87c8ab97db18a7531dc2df610b51fe819c8bf746b2b66475b544220c37c95cbb`; stdout `dc6ecb960fc59852c4b3251a1146ef6425675c44be4cf03304d3fc0026942d27`; stderr `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; pins 81/81, 9/9, 6/6.

## Decision in this overlay

The operator accepted the region/visibility proposal only for authoring a separate future coordinate-policy specification. The immutable source proposal stays `PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED`. Decisions include four candidate entries and retain the two inherited blocks:

- Accept for future coordinate-policy specification only: `CHALLENGE_003.target_x`, `CHALLENGE_005.target_position`, `CHALLENGE_006.target_position`, `CHALLENGE_007.target_position`.
- Remain blocked: `CHALLENGE_008.active_selection`, `CHALLENGE_009.displayed_count` (11s total vs 12s phase sum and presentation policy unresolved).

No source field binding, destination mapping, pixel placement, payload consumer, render test, media, release, freeze or promotion is authorized by the decision record.

## Next planned gate: coordinate-policy proposal

Create a new JSON contract + strict schema + static tests + checkpoint/prompt update. It should explicitly propose (and label `PROPOSED_NOT_APPROVED`) coordinate policies per candidate, including source coordinate space, origin, axis direction, units, boundaries, source-to-logical 540x960 transform, logical-to-delivery transform, anchor/intrinsic asset scale, out-of-bounds behavior, source-frame sequence/cardinality, and fail-closed conditions. The 1080x1920-to-540x960 mapping must be explicitly declared as a proposal rather than silently inferred from dimensions. The subsequent delivery transform must distinguish profile scaling from frame-timebase resampling. For `CHALLENGE_003.target_x`, do not invent Y: make placement unavailable until a source-grounded axis-only visualization is explicitly decided. Reuse existing `winning_frame` as the sole Challenge temporal anchor; `close_calls` remains episode-count metadata only.

Do not implement the consumer during the policy-specification stage. After proposal tests pass, a separate operator decision record can authorize only the explicit mapping details it names. Then proceed to a request-scoped, allowlisted candidate payload consumer contract, input and negative tests, and an isolated in-memory renderer/baseline test harness. Before any actual renderer/video execution, resolve D4.8 and D baseline governance gates explicitly. Use a no-media dry run or in-memory preview where that is the highest currently authorized level; never claim video output when no render occurred.

## Governance locks

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

Never serialize all of `FrameSnapshot.custom_data`, emit unapproved native renderer input, change simulation calculation/input/pause/result semantics, alter challenge JSONs, modify the frozen C11-C package or the `CHALLENGE_004` V1 harness/fixture, create media while the lock is active, or promote D ahead of formal acceptance. Re-run Godot only when a change actually impacts runtime; decision-only changes rely on pinned evidence and static tests.

## Operator workflow preference

The operator has standing approval to continue through predictable planned gates without redundant confirmation. This does not override the mandatory evidence, explicit scope of each formal decision record, or the governance locks above. Present clear apply/test blocks separately and claim PASS only from actual exit code, marker, hashes and source-pin reconciliation.

V2 evidence correction: the unaccepted V1 field-region decision overlay encoded the empty stderr SHA-256 as a 62-character string, omitting `bf`. The 551/551 source evidence remains pinned and unchanged. V2 changes only the erroneous digest references and related checksum/test/docs, not any approvals or governance locks.


## Coordinate policy proposal gate — 2026-10-21 V17

The field-region/visibility decision record is accepted for coordinate-policy specification only. Windows evidence: 653/653; stdout SHA-256 `a7e3b9dd98b317df5bb19e02c1751ae2b79ed4c297440eada8493c452bb44bba`; stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; receipt SHA-256 `4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a`.

The new coordinate policy artifact `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_V1.json` remains `PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED`. It proposes `CANVAS_1080X1920 -> LOGICAL_SOCIAL_CANVAS_540X960` scale 0.5, zero offset, and logical-to-`REVIEW_720` reference spatial scale 4/3, zero offset. Combined reference canvas-to-delivery spatial scale is 2/3. These are proposed coordinate equations only, not approval of binding/projection or renderer activation.

For `CHALLENGE_003.target_x`, the scalar still supplies no Y. A logical centerline Y=480 is proposed explicitly as a presentation-only default, not inferred simulation data, and remains unapproved. Source scalars outside [0,100] fail closed; they are never clamped. The `100x100` intrinsic size interpretation for `waypoint.svg` and `target.svg`, center anchor, and canvas-edge clipping are also proposals pending review.

The three vector candidates preserve finite, in-bounds source positions by scale 0.5 with no translation, Y inversion, clamping or intermediate rounding. `REVIEW_720` is a spatial reference only; no delivery frame resampling or frame-index mapping is added. Source frame order and cardinality are preserved; `winning_frame` remains the sole Challenge temporal anchor; `close_calls` remains episode-count metadata only.

`CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked. No challenge JSON, CoordinateMapper, C11-C source, CHALLENGE_004 V1 harness, consumer, renderer or media was changed or authorized. Locks remain renderer OFF, payload/media false, candidate input inadmissible, D4.8 blocked, D10 blocked for promotion, no baseline approval and release authority NONE.
