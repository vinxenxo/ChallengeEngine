# C11-C Visual Duration Policy v1.0

Historical documents containing the old 18-second baseline remain immutable. This is the active policy for current production/review.

## Standard range
All production/review visual videos use a policy-driven duration between 20 and 30 seconds. At 30 FPS the frame count is derived from the resolved duration.

## Visual Loops
A Visual Loop must finish a complete authored temporal cycle. Current policy:

| Cycles | Duration | Frames |
|---:|---:|---:|
| 1 | 24 s | 720 |
| 2 | 27 s | 810 |
| 3 | 30 s | 900 |

Audio receives the same duration/cycle information so the musical period closes on the same temporal boundary.

## Visual Drills
Existing 3-second countdown and 3-second terminal CTA remain. Current total presentation duration is:

| Family | Gameplay | Total |
|---|---:|---:|
| Tracking | 24 s | 30 s |
| Saccade | 21 s | 27 s |
| Pursuit | 24 s | 30 s |
| Peripheral Scan | 21 s | 27 s |

Legacy authoring fixtures remain at historical values for regression compatibility.

## Acceptance conditions
A duration change is accepted only when visual endpoint, audio endpoint, frame count and social metadata all derive from the same resolved duration.

## Frozen boundary
This is a presentation/delivery policy. It does not change simulation truth, structural RNG, `SimulationResult`, `winning_frame`, `close_calls`, `RenderedFrameStream`, C7 ownership or C9 authoring semantics.
