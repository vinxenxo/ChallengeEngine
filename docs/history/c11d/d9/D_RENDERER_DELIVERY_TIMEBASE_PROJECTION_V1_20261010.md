# D Renderer Delivery Timebase Projection V1 — history record

Date: 2026-10-10

## Change

Added `D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1` as an in-memory proposal to address source/delivery FPS differences. It consumes only the pinned temporal-bound preview and delivery profile registry; it projects cumulative source frame boundaries with exact integer-ratio nearest-tick rounding.

## Representative source-grounded result

For `CHALLENGE_004`, 900 frames at 60 FPS project to 450 frames at the `REVIEW_720` profile's 30 FPS, preserving the existing four phase order and boundaries as 90, 210, 90, 60 frames. Geometric loop and tracking drill reference spans remain unchanged at their existing matching 30 FPS.

## Limits

Projection policy is PROPOSED_NOT_APPROVED. Source-frame sampling for simulation, event-anchor mapping, interpolation, audio resampling, selected loop/drill instance identity and per-field visibility windows remain unresolved. No renderer input, dispatch or media is produced. `D4.8=BLOCKED`; `release_authority=NONE`; baseline remains unapproved and not frozen. The frozen C11-C manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
