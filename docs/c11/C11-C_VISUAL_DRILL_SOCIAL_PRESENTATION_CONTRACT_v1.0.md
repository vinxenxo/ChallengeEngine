# C11-C — Visual Drill Social / Editorial Presentation Contract v1.0

## Status

**ACTIVE** — presentation-only contract for Visual Drills.

## Scope

This contract brings Visual Drills onto the same social/editorial presentation system used by the C11-C Visual Loop delivery layer.

It does **not** modify:

- simulation mathematics;
- `SimulationResult`;
- simulation or mechanic RNG ownership;
- `WinningFrameDetector`;
- `WinningFrameVisibilityGate`;
- `RenderedFrameStream` semantics;
- C7 audio contracts;
- C9 authoring contracts;
- `UnifiedSocialFrame` logical geometry.

## Shared layout

All visual content uses the same logical social frame:

- canvas: `540×960`;
- Header: `y=0..144`;
- Body: `y=144..816`;
- Footer: `y=816..960`.

Physical social delivery is captured at:

- `720×1280`;
- `9:16`;
- `30 FPS`.

The 720×1280 value is a capture/delivery concern. The logical C11-B/C11-C composition remains 540×960.

## Shared editorial grammar

### Header

Two centered editorial blocks with:

- strong typography;
- word-safe fitting;
- automatic horizontal fitting;
- bold treatment;
- decorative separator;
- palette-bound colors where the active visual system supplies them.

The Matrix / split-flap transition is **optional** and is disabled for Visual Drills by default.

### Footer

Three centered lines:

1. factual/render telemetry;
2. generation/audio/social metadata;
3. family signature.

The footer must not grow into a fourth-line legacy stack.

## Visual Drill-specific content

Only the semantic content changes by family:

- Tracking: trajectory / smooth pursuit;
- Saccade: discrete relocation / spatial precision;
- Pursuit: continuous following;
- Peripheral Scan: fixation / eccentric stimulus.

The shared layout component must not know or calculate the mechanics of those exercises.

## Audio

Visual Drills are rendered with audio enabled by default. The audio layer is presentation infrastructure and uses one deterministic shared master across all Visual Drill families and seeds at this stage. Family-specific sound grammar is intentionally deferred until mechanics are refined.

## Architectural rule

No second Visual Drill Header/Footer implementation is permitted when the shared `C11CVisualEditorialLayer` can satisfy the requirement.

The family binder supplies semantic editorial data; the shared layer owns visual placement, fitting, typography, rules and section treatment.
