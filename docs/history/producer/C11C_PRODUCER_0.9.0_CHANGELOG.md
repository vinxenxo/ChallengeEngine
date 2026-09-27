# C11-C Producer 0.9.0 — Changelog

## Based on

Producer 0.8.0 / 2.17.9 stabilization state.

## Changes

- Removed visible banner/header to recover vertical workspace.
- Removed temporary help/advice copy from the working area.
- Replaced variation numeric editors with compact slider controls plus explicit `ALEATORIO` checkboxes.
- Added strong queue selection styling.
- Completed queue rows are retained and dimmed.
- Existing manually-seeded products are detected and shown as `YA PRODUCIDO` instead of being queued accidentally.
- Kept failed recipes retryable.
- Centralized alias-safe delivery profile consumption.
- Fixed the Visual Loop wrapper assumption that every profile exposes an `fps` field.
- Added explicit current delivery FPS and encoder metadata to the central profile catalog.
- Changed Drill source audio mux to 48 kHz stereo AAC target.
- Added detailed current/runtime acceptance documentation.

## Boundaries preserved

No changes to Challenge mechanics, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 contracts, C9 challenge semantics or C11-B logical 540×960 social geometry.
