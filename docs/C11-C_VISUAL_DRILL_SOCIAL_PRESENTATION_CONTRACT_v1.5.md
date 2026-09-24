# C11-C Visual Drill Social Presentation Contract v1.5

## Terminal CTA placement

Visual Drills use the shared Challenge-derived `CTAComponent`. The terminal self-evaluation CTA is a presentation-only phase appended after the canonical gameplay stream.

`PRE_ROLL (3s) → GAME (canonical gameplay) → END_CTA (3s)`

During `END_CTA`, the last emitted gameplay frame remains the visual substrate while telemetry/footer content is suppressed. The CTA itself is mounted in the **HEADER**, replacing the editorial header copy for the final phase. This is a placement change only; the temporal contract and wording remain:

- `¿LO CONSEGUISTE?`
- `¿HASTA DÓNDE LLEGASTE?`

No Visual Drill runtime or `RenderedFrameStream` owns this phase. The same `CTAComponent` implementation used by Challenge is reused; no second CTA implementation is introduced.

## Timing

- Tracking: 21s gameplay + 3s countdown + 3s CTA = 27s / 810 frames.
- Saccade: 17s gameplay + 3s countdown + 3s CTA = 23s / 690 frames.
- Pursuit: 17s gameplay + 3s countdown + 3s CTA = 23s / 690 frames.
- Peripheral Scan: 17s gameplay + 3s countdown + 3s CTA = 23s / 690 frames.

## Geometry

The frozen 540x960 logical frame and Header/Body/Footer structural rectangles remain unchanged. The CTA is simply a presentation child of the Header content root during the terminal phase.
