# C11-D V2-B Coordinate Policy Decision — Checkpoint V1

Date: 2026-10-21
Status: `COORDINATE_POLICY_ACCEPTED_FOR_FUTURE_CONSUMER_SPECIFICATION_ONLY`

## Prior verified gates

- Candidate semantic decision: 146/146; receipt SHA-256 `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`.
- Field-region decision: 653/653; stdout SHA-256 `a7e3b9dd98b317df5bb19e02c1751ae2b79ed4c297440eada8493c452bb44bba`; stderr empty `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; receipt SHA-256 `4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a`.
- Coordinate-policy proposal: 961/961; stdout SHA-256 `439e68e15c72975ccc3ac26d42e5e8e8dc5019bcc4e9f1f3051fd061701b07f3`; stderr empty `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; receipt SHA-256 `1518168dd6b50fc869dbd18b05dcdef13397ea8023ff6fa1f896f55dee5b9f96`.
- Frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Decisions recorded

Five policy choices are accepted for future consumer specification only: uniform 0.5 source-to-logical mapping; uniform 4/3 mapping to `REVIEW_720` as spatial reference only; presentation-only centerline `Y=480` for `CHALLENGE_003.target_x`; interpretation of the pinned 100x100 SVG intrinsic sizes as source-canvas units; and center anchoring with asset-bound clipping at the logical canvas boundary.

Renderer pixel rounding, antialiasing and final crop raster semantics remain blocked for the renderer implementation gate. No runtime coordinate transform, binding, consumer, renderer projection, render test, payload materialization or media creation is authorized. `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked.

## Policy invariants

Source canvas `1080x1920` maps to logical `540x960` with scale 0.5 on both axes, zero offset, no intermediate rounding, top-left origin, X right and Y down. `REVIEW_720` `720x1280` is a spatial reference at scale 4/3 from the logical canvas, not the final delivery profile. `CHALLENGE_003.target_x` maps to X by `(target_x/100)*540` and to presentation-only Y=480. Vector candidates use source point `(x,y)*0.5`; invalid, nonfinite or out-of-domain values fail closed as a whole track, with no clamp, no interpolation or extrapolation, and source frame count/order preserved.

Asset marker dimensions 100x100 source units imply 50x50 logical units and 200/3 by 200/3 reference units; asset center anchor and logical-edge clipping do not move source positions. Renderer-dependent pixel rounding and crop details remain blocked.

## Governance locks

`renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, approved bindings/projection bindings all zero, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14=BLOCKED`, `D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, baseline approval missing, freeze ineligible, release authority none. C11-C remains immutable.

## Next gate

Prepare an explicit renderer-neutral allowlisted coordinate projection/consumer specification plus negative contract tests. Keep this as specification work; no payload-consumer implementation or renderer execution until the corresponding authorization gates close.
