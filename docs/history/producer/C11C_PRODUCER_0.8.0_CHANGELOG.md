# C11-C Producer 0.8.0 — Change Log

## Basis

Built as an additive overlay over the C11-C 2.16.9 frozen baseline plus the 2.17 Challenge delivery work.

## 0.8.0 closure changes

- GUI keeps the approved 0.4.0 two-column light layout.
- Producer schema now uses the central delivery profile catalogue.
- MASTER_1080 is the standard A LA CARTA delivery profile.
- Challenges are read from the actual `challenges/*.json` corpus rather than duplicated timing metadata.
- Challenge 008 and 009 timing is derived from phase sums, producing 12 s / 720 frames.
- Challenge multi-seed jobs use a seed-specific OutputRoot to prevent product collisions.
- Visual Loop and Visual Drill producer routes receive the selected delivery profile.
- Loop and Drill delivery wrappers resolve dimensions/audio settings from `profiles/delivery/c11c_video_delivery_profiles.json` rather than maintaining a second profile table.
- Review Drill Tracking duration is normalized to 21 s gameplay / 27 s total / 810 frames.
- GUI operation changes refresh the visible form again when returning to A LA CARTA.
- RESUME and RESET are treated as mutually exclusive.
- Launcher errors stop the current recipe cleanly and preserve a visible ERROR state.

## Frozen boundaries

This release does not modify C11-B simulation truth, Challenge mechanics, RNG ownership, SimulationResult, winning_frame, close_calls, WinningFrameDetector, RenderedFrameStream, C7 contracts or C9 authoring semantics.

## Acceptance

Static Producer self-test and seed-probe preflight pass. Windows/PySide6 GUI runtime acceptance remains a user-side step.
