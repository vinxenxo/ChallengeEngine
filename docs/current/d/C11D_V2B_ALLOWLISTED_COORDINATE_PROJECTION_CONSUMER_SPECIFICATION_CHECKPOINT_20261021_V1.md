# C11-D V2-B Allowlisted Coordinate Consumer Specification — Checkpoint V1

Date: 2026-10-21
Status: `SPECIFICATION_ONLY_NOT_IMPLEMENTED`

## Accepted predecessor evidence

The coordinate-policy decision suite passed `2756/2756` on the active Windows checkout. Its stdout SHA-256 is `e233f0f85abfa4249873f14056c8ed6d089026e2e9093b8c60773d7d5282ca94`; stderr SHA-256 is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; receipt SHA-256 is `b61fb3403e0ad5725937be05f8a7153c3cf35ccde167306f45151ece0f1cc4cb`. The prior coordinate proposal suite passed `961/961`, stdout `44c1ec6507988023b7cd20cdcc8e0e722c99af610d9be02a6d658ce9b07e9f57`; Windows receipt SHA-256 `1518168dd6b50fc869dbd18b05dcdef13397ea8023ff6fa1f896f55dee5b9f96`. The field-region decision receipt SHA-256 is `4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a`.

## New artifact

`definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_V1.json` defines a renderer-neutral input/output contract for a future allowlisted target-marker projection consumer. Its allowlist is exactly `CHALLENGE_003.target_x`, `CHALLENGE_005.target_position`, `CHALLENGE_006.target_position`, and `CHALLENGE_007.target_position`. `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked.

The source frame index is the zero-based ordinal of `SimulationResult.frames`; `FrameSnapshot` has no authoritative frame-index field. The contract reads one allowlisted property per frame from `FrameSnapshot.custom_data`, never serializes/copies the complete dictionary, rejects the entire candidate track if any sample is invalid, and emits only logical target-marker coordinates plus an explicitly allowlisted marker descriptor. No raw custom_data values, score, `close_calls`, or fallback from `FrameSnapshot.position` are permitted.

## Non-interference and unresolved implementation

No production consumer code is included. `REVIEW_720` remains a spatial reference only and is not applied by the logical projection contract. Renderer pixel rounding, raster crop, antialiasing, and subpixel semantics remain blocked for the renderer implementation gate. Runtime coordinate transform, binding approval, renderer projection, payload materialization, media creation, render test, release and promotion remain unauthorized.

Locks remain unchanged: `renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, approved bindings `0`, `D4.8=BLOCKED`, `D10=BLOCKED_FOR_PROMOTION`, `release_authority=NONE`. The frozen C11-C manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Next gate

Run the static contract suite on the active Windows checkout with the exact prior coordinate-policy decision receipt path. If green, proceed to the next distinct engineering gate: design the actual allowlisted consumer implementation with exhaustive negative tests, still without renderer activation or media creation.
