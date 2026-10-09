# D Renderer Delivery Timebase Projection — V1 checkpoint

**Status:** preparation-only proposal; not approved, not frozen, not renderer input.

## Purpose

This increment explicitly projects canonical source timeline boundaries into a requested delivery profile timebase. It addresses the known `CHALLENGE_004` 60 FPS source versus `REVIEW_720` 30 FPS delivery profile mismatch without mutating C11-C and without pretending to define simulation frame sampling.

## Policy proposal

`CUMULATIVE_SOURCE_BOUNDARY_NEAREST_DELIVERY_TICK`: for every zero-based half-open source boundary `b`, project it to `floor(b * delivery_fps / source_fps + 0.5)`. The implementation uses exact integer arithmetic. Each target segment's frame count is the difference between projected cumulative boundaries; it does not independently round each segment duration. A projected zero-length segment remains zero length and is marked disabled; no minimum frame is invented.

Expected representative result for the source-pinned `CHALLENGE_004` preview and `REVIEW_720` delivery profile:

- Source: 900 frames at 60 FPS, with `HOOK → GAME → REVEAL → CTA` spans 180/420/180/120.
- Delivery projection: 450 frames at 30 FPS, with corresponding spans 90/210/90/60.
- Source and projected timeline durations are both exactly 15 seconds for this fixture.
- Visual Loop and Visual Drill examples already use 30 FPS and preserve their current continuous frame spans.

## Explicitly unresolved

This does **not** choose simulation source frames, define interpolation, map `winning_frame` or `close_calls`, bind generated loop/drill payload instances, define audio resampling, or assign per-field editorial visibility windows. Therefore it does not make a video render-ready. Those are independent contracts and must not be inferred from this projection.

## Governance

The contract is in-memory and source-pinned. It emits no renderer-native input, performs no dispatch, invokes no Godot/FFmpeg process, writes no output artifact, and creates no media. It does not approve the projection policy, regions, temporal topology or baseline. D4.8 remains BLOCKED; release authority NONE; D9 OPEN; D10 BLOCKED. C11-C 2.19.12 and its manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` remain immutable.

## Validation

Run `python -m py_compile .\tools\c11d\d9\d_renderer_delivery_timebase_projection.py .\tools\c11d\d9\test_d_renderer_delivery_timebase_projection.py` and then `python .\tools\c11d\d9\test_d_renderer_delivery_timebase_projection.py`. The test expects 3/3 content types, deterministic outputs, pinned source lineage, 42 negative cases, and Draft 2020-12 validation if `jsonschema` is installed.
