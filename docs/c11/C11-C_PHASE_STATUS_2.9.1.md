# C11-C Phase Status — 2.9.1

## Current phase
**C11-C Visual Drills — four-family implementation complete; 2.9.1 runtime hotfix pending validation.**

## Frozen / do not reopen
- C11-B certified/frozen baseline.
- Challenge simulation truth and mechanics.
- Structural RNG ownership.
- `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`.
- `RenderedFrameStream` as presentation input.
- C7 audio contract ownership.
- C9 authoring contracts.
- 540x960 logical social frame and 720x1280 physical delivery.

## Visual Drill families
### Tracking
Seeded authoring now changes movement characteristics as well as cosmetic presentation. The renderer remains passive. The target is the visual hero; history-only trail uses time fade. Decorative Tron road was deliberately removed.

### Saccade
Discrete A→B relocation with no spatial interpolation. Polar/golden-angle placement, bounded jump distance, APPEAR/IDLE/VANISH phases and an in-target jump counter sourced from authored mechanic state.

### Pursuit
"El Monolito en el Vacío": uniform cubic B-spline, arc-length LUT, authored per-frame traversal, subtle speed modulation, foveal target geometry, sizygia answer sheet and camouflage zones.

### Peripheral Scan
"El Eclipse y la Tormenta Solar": rigid central anchor, three orbital rings, deterministic polar schedule, exact threat/distractor timing and answer sheet, central cognitive marker and peripheral flare treatment.

## Common usability layer
- 3-second challenge-derived countdown.
- Terminal 3-second self-evaluation CTA in **Header**.
- CTA message: "¿LO CONSEGUISTE? / ¿HASTA DÓNDE LLEGASTE?"
- Visual Drill durations remain within the 20–30 second delivery envelope.
- Shared social sidecar `.txt` output is expected for every drill family.

## Current 2.9.1 hotfix
`PeripheralScanRenderer.gd` had an undeclared `_environment` identifier. This caused renderer compilation failure and cascaded aggregate failures. The hotfix only restores the missing presentation dependency declaration.

## Next window
Treat 2.9.1 as the stable handoff point. Do not reopen Tracking/Saccade mechanics unless a regression is demonstrated. Continue with visual/audio refinement or new gameplay depth only after the complete corpus is green.
