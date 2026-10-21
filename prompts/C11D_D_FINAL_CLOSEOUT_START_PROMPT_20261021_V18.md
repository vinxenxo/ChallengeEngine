# C11-D Final Closeout Start Prompt — V18 (2026-10-21)

Continue in the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The live checkout is authoritative. Never extract a whole context archive over it. Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; never modify it during D work.

## Latest verified evidence

- Semantic decision record: 146/146; receipt `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`.
- Field-region decision record: 653/653; receipt `4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a`; stdout `a7e3b9dd98b317df5bb19e02c1751ae2b79ed4c297440eada8493c452bb44bba`; stderr empty.
- Coordinate-policy proposal: 961/961; receipt `1518168dd6b50fc869dbd18b05dcdef13397ea8023ff6fa1f896f55dee5b9f96`; stdout `439e68e15c72975ccc3ac26d42e5e8e8dc5019bcc4e9f1f3051fd061701b07f3`; stderr empty.
- Coordinate-policy decision record V1 is the next ADD_ONLY artifact. It records five policy choices accepted for future consumer specification only and keeps renderer pixel rounding/crop blocked.

## Accepted coordinate policy for future specification only

Source `1080x1920` to logical `540x960`: uniform scale 0.5, zero offset, no intermediate rounding. Logical to `REVIEW_720` `720x1280`: uniform 4/3 spatial reference only, not final delivery selection. `CHALLENGE_003.target_x`: X=`(target_x/100)*540`, presentation-only Y=480, never a recovered source Y. SVG `100x100` intrinsic dimensions are treated as source-canvas units for future specification; mapped size `50x50` logical; center anchor and clip asset bounds at edges without moving the point. Pixel rounding/crop raster semantics remain blocked for the renderer implementation gate.

No runtime coordinate transform, bindings, consumer implementation, renderer projection, render test, payload materialization or media creation is authorized. `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` stay blocked. Preserve exact frame count/order, no interpolation/extrapolation/resampling; `winning_frame` is the sole Challenge temporal anchor and `close_calls` episode count only.

## Mandatory locks

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; seed domains incomplete; automatic seed generation false; master seed not adopted; approved binding counts zero; D4.8 blocked; D9.10 prepare-only; D9.14/D9.16 blocked; D9.17 blocked no-go; D10 blocked for promotion; baseline approval missing; freeze ineligible; release authority none.

## Next gate

Use the coordinate-policy decision receipt after the static suite passes, then design a renderer-neutral allowlisted coordinate projection/consumer contract with negative tests. Do not modify CoordinateMapper, challenge JSON, C11-C, or CHALLENGE_004 V1 harness. Don't rerun the earlier 45-process Godot matrix for static-only changes.
