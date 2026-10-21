# C11-D V2-B Candidate Coordinate Policy Proposal — Checkpoint V1

Date: 2026-10-21
Status: `PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED`

## Completed prior gate

Windows field-region decision regression returned `653/653`; stdout SHA-256 `a7e3b9dd98b317df5bb19e02c1751ae2b79ed4c297440eada8493c452bb44bba`; stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; test receipt SHA-256 `4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a`. Four field-region proposals were accepted for coordinate-policy specification only; CHALLENGE_008 and CHALLENGE_009 remain blocked. The immutable prior decision record SHA-256 is `1ec59d7a9257cfc2477fc37efe8cb2f04d9807a7f9986d96afc2f2ddd9b4f7af`.

## Current artifact

`definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_V1.json` specifies a renderer-neutral spatial transform proposal for exactly the four candidates. The proposal pins 81 source artifacts, 9 authority inputs, 6 semantic inputs, 6 field-region decision artifacts, and 3 coordinate-reference artifacts.

## Proposed transform equations

- Source canvas `1080x1920` to logical social canvas `540x960`: uniform 0.5 scale on X/Y, zero offset, no rounding.
- Logical `540x960` to reference delivery `REVIEW_720` `720x1280`: uniform 4/3 scale, zero offset. This is a spatial reference only; no final delivery profile is selected.
- Combined reference canvas-to-delivery scale: 2/3 on both axes. No temporal resampling, frame conversion or `winning_frame` remap.
- `CHALLENGE_003.target_x`: validate finite `[0,100]`; propose `x_logical=(target_x/100)*540`; explicitly propose presentation-only `y_logical=480`, not source semantics. Out-of-range fails closed, no clamping.
- `CHALLENGE_005/006/007.target_position`: validate finite `Vector2` with inclusive source bounds `[0,1080] x [0,1920]`, then `x/y * 0.5`; no offset, Y inversion, clamping or intermediate rounding.
- Propose treating the pinned `waypoint.svg`/`target.svg` intrinsic `100x100` as source canvas units, centering the asset at the mapped point and clipping asset bounds at the canvas edge. Asset pixel rounding remains unresolved.

## Still not approved

No coordinate policy, point placement, asset sizing, binding, payload consumer, renderer projection, renderer execution, payload materialization, media creation, release or baseline promotion is authorized by this proposal. `renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, approved bindings remain zero, D4.8 stays BLOCKED, D10 stays BLOCKED_FOR_PROMOTION, release authority NONE. C11-C is immutable.

## Next gate

Run the static suite on the active Windows checkout using the exact prior field-region decision receipt from `%TEMP%`. If green, record an independent operator decision on these explicit spatial formulas and their presentation-only Y/asset-size assumptions. Do not implement a consumer or enable renderer as part of the proposal gate.
