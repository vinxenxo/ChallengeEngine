# START PROMPT — ChallengeEngineV01_STATELESS / C11-C NEXT WINDOW

You are continuing `ChallengeEngineV01_STATELESS` from **C11-C 2.9.1**.

Read and obey this order:
1. `AGENTS.md`.
2. `MASTER_HANDOVER_C11-C_2.9.1.md`.
3. `docs/c11/C11-C_PHASE_STATUS_2.9.1.md`.
4. Existing C11-C changelogs through 2.9.1.

## Authoritative state
C11-B is CLOSED / CERTIFIED / FROZEN.
Do not modify simulation truth, structural RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio contracts, or C9 authoring contracts.

## C11-C Visual Drills
The four families exist:
- `tracking`
- `saccade`
- `pursuit`
- `peripheral_scan`

Tracking and Saccade are mechanically closed.
Pursuit and Peripheral Scan are implemented and need normal visual/runtime review after 2.9.1 validation.

## Common presentation contract
- Logical frame: 540x960.
- Physical output: 720x1280, 9:16, 30 FPS.
- Countdown: 3 seconds.
- Gameplay: canonical family duration.
- Terminal CTA: 3 seconds in **Header**, reusing `CTAComponent`.
- CTA text:
  `¿LO CONSEGUISTE?`
  `¿HASTA DÓNDE LLEGASTE?`
- Visual Drill social sidecar `.txt` must be generated for every family.
- Comic Sans is not allowed for new Visual Drill editorial text.

## Known 2.9.0 issue and 2.9.1 fix
`PeripheralScanRenderer.gd` referenced `_environment` without declaring it. This caused a parser error which cascaded into renderer-dependent playback suites.
2.9.1 declares and owns `_environment` as a presentation-only `Node2D`.

Do not compensate by weakening tests. The correct state is clean compilation + clean playback + green aggregate runner.

## Visual direction
Tracking: dynamic seeded motion, premium target, history trail, no Tron road.
Saccade: sparse high-contrast target, discrete jumps, jump number inside target.
Pursuit: `El Monolito en el Vacío`; spline-driven orbital motion, arc-length traversal, foveal isolation, sizygia events.
Peripheral Scan: `El Eclipse y la Tormenta Solar`; rigid central anchor, orbital radar rings, deterministic flares, threat/distractor counting.

## Gameplay-depth backlog
Tracking: occlusion + morphing.
Saccade: N-back + flash recognition.
Pursuit: depth/scale illusion + flanker distractors.
Peripheral Scan: quadrant accounting + rhythmic asynchrony.

## Working rule
Do not start a new major family until 2.9.1 is fully green and the four existing families have passed both automated validation and physical video review.

First task in the new window: verify the 2.9.1 hotfix with focused suites and `python tests/run_all.py`.
