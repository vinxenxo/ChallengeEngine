# C11-D Full Context Continuity Checkpoint — V17 (2026-10-21)

## Authority and immutable baseline

Active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` remains the source of truth. Apply only verified, minimal ADD_ONLY overlays from the repo root; never extract a context ZIP wholesale over the checkout. Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. C11-C is immutable and remains authoritative until the D branch independently passes acceptance, approval and freeze/promotion gates.

## Latest V2-B evidence — accepted on Windows

- Design contract: 90/90; 11/11 files; 81/81 source pins; 9/9 authority-input pins.
- Runtime implementation static suite: 198/198; receipt SHA-256 `e64cfd259914c471d03e8578b955140ad487b04694c5f682834517d823fcbfc4`.
- Source-frame runtime: 45/45 planner invocations, 45/45 independent Godot Mono processes, 9/9 selectors; report SHA-256 `f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446`.
- Sanitized evidence audit: 9/9 selectors; 45/45 planner/runtime; 6/6 typed candidates; no raw candidate values; audit SHA-256 `8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00`.
- Semantic-review request: 75/75; request SHA-256 `b576612dd0913ce8f706a5272a5b9ca5ceb6c7a1f39d832323d9db98578b5d01`.
- Semantic decision record: 146/146 Windows checks; receipt SHA-256 `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`; record SHA-256 `cc3550cd4d13f228ec9b3d51eeaa199505c5975b42882fb06ba3e83c4a000e90`.
- Field-region/visibility proposal: **551/551 Windows checks**, candidates 4/4, source pins 81/81, authority inputs 9/9 and semantic inputs 6/6. Stdout SHA `dc6ecb960fc59852c4b3251a1146ef6425675c44be4cf03304d3fc0026942d27`, stderr SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, receipt SHA `87c8ab97db18a7531dc2df610b51fe819c8bf746b2b66475b544220c37c95cbb`.

## Operator decision recorded for field-region/visibility

Separate record: `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_V1.json`. The four accepted proposals are:

- `CHALLENGE_003.target_x`: future coordinate-policy specification only; scalar X in `PILOT_0X100`, without inferred Y or normalization.
- `CHALLENGE_005.target_position`: future coordinate-policy specification only; per-run constant `Vector2` repeated per source frame.
- `CHALLENGE_006.target_position`: future coordinate-policy specification only; per-frame `Vector2` target track separate from catcher.
- `CHALLENGE_007.target_position`: future coordinate-policy specification only; per-frame `Vector2` target track separate from scanner.

`CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked. The accepted decisions allow only a separate coordinate-policy proposal. They do not authorize actual projection, bindings, payload materialization/consumer, renderer activation, render test, media or release. The prior field-region proposal itself remains immutable and `PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED`.

## Immediate next engineering gate

Prepare a separate **coordinate-policy proposal** covering only the four accepted candidates. It must explicitly specify or keep blocked:

1. source coordinate space, origin, axis direction, units/range and boundary semantics;
2. mapping from each source space to logical 540x960 and the delivery profile, with scale/offset and out-of-bounds policy;
3. `CHALLENGE_003.target_x` missing-Y treatment, without inventing a second coordinate;
4. asset intrinsic-size and anchor responsibilities separate from simulation scale/rotation/opacity;
5. exact source-frame indexing/cardinality, temporal ownership, and fail-closed behavior;
6. candidate-level exclusions and proof that no `FrameSnapshot.custom_data` map, score telemetry or `close_calls` enters a consumer.

The policy proposal must stay `PROPOSED_NOT_APPROVED`. Once that proposal is tested, the next separate decision can approve only those coordinate rules that are explicit and source-grounded. Do not jump directly to a payload consumer or real render.

## Project objective and route to the first D render test

The objective is to reach a controlled real-render test on a formally approved D baseline, then work toward replacing C11-C only after D gates, approval and freeze are complete. To reach it safely, the remaining chain is: coordinate policy -> explicit binding/consumer contract and allowlist -> candidate payload consumer tests -> integrated renderer contract/baseline candidate -> separately authorized render test -> evidence-backed D baseline approval/freeze/promotion. Do not claim a render is authorized until the relevant gate permits it. Routine progression through established steps does not require redundant confirmation, but gate artifacts, evidence and governance restrictions remain mandatory.

## Hard governance locks

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

Never modify C11-C or its freeze manifest, challenge JSONs, or the `CHALLENGE_004` V1 harness/fixture. Never serialize whole `FrameSnapshot.custom_data`. `winning_frame` remains the sole Challenge temporal anchor; `close_calls` remains episode-count metadata only. Do not rerun the 45/45 Godot matrix for static-only decision-record work.

## Evidence-integrity correction — field-region decision overlay V2

A Windows test attempt for the first decision-record overlay failed only at `CHECK_644` because the overlay itself carried a malformed empty-stderr digest (the constant omitted `bf`). The attempt rolled back the eight ADD_ONLY files. V2 corrects the digest in the decision record, regression test and manifest, preserving the original Windows 551/551 receipt pin and every governance lock. Re-run APPLY and TEST for overlay V2; do not infer success from the earlier 652/653 run.


## Coordinate policy proposal gate — 2026-10-21 V17

The field-region/visibility decision record is accepted for coordinate-policy specification only. Windows evidence: 653/653; stdout SHA-256 `a7e3b9dd98b317df5bb19e02c1751ae2b79ed4c297440eada8493c452bb44bba`; stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; receipt SHA-256 `4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a`.

The new coordinate policy artifact `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_V1.json` remains `PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED`. It proposes `CANVAS_1080X1920 -> LOGICAL_SOCIAL_CANVAS_540X960` scale 0.5, zero offset, and logical-to-`REVIEW_720` reference spatial scale 4/3, zero offset. Combined reference canvas-to-delivery spatial scale is 2/3. These are proposed coordinate equations only, not approval of binding/projection or renderer activation.

For `CHALLENGE_003.target_x`, the scalar still supplies no Y. A logical centerline Y=480 is proposed explicitly as a presentation-only default, not inferred simulation data, and remains unapproved. Source scalars outside [0,100] fail closed; they are never clamped. The `100x100` intrinsic size interpretation for `waypoint.svg` and `target.svg`, center anchor, and canvas-edge clipping are also proposals pending review.

The three vector candidates preserve finite, in-bounds source positions by scale 0.5 with no translation, Y inversion, clamping or intermediate rounding. `REVIEW_720` is a spatial reference only; no delivery frame resampling or frame-index mapping is added. Source frame order and cardinality are preserved; `winning_frame` remains the sole Challenge temporal anchor; `close_calls` remains episode-count metadata only.

`CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked. No challenge JSON, CoordinateMapper, C11-C source, CHALLENGE_004 V1 harness, consumer, renderer or media was changed or authorized. Locks remain renderer OFF, payload/media false, candidate input inadmissible, D4.8 blocked, D10 blocked for promotion, no baseline approval and release authority NONE.
