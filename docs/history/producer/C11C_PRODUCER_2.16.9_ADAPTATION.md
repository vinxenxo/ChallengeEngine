# C11-C Producer — 2.16.9 Adaptation

## UI rule

The approved Producer 0.4.0 two-column light interface is preserved. The adaptation extends it rather than replacing it.

## Current supported actions

### Single content

- Visual Loop: any of the five families and all 27 grammars.
- Visual Drill: Tracking, Saccade, Pursuit, Peripheral Scan.
- Challenge: CHALLENGE_001 … CHALLENGE_009.

### Review/batch

- 27 Loops
- 20 Drills
- 5 Longforms
- Loops + Drills
- Loops + Longforms
- Drills + Longforms
- Complete 27 + 20 + 5 corpus

### Utility

- Full regression.
- 7 review workers.
- Resume / Reset.
- Optional GIF.
- Optional AVI retention.

## Accessibility/usability priorities

- Same two-column layout.
- Explicit labels.
- Large controls with visible focus states.
- Irrelevant controls disabled instead of silently ignored.
- Queue remains visible while a process runs.
- Logs remain visible and readable.
- Backend hash is displayed and gated.

## Backend boundary

The GUI invokes PowerShell/Godot/Python launchers. Python does not reimplement mechanics, rendering or seed-variation algorithms.


## Current amendment

The 2.18.0 stabilization overlay supersedes the temporary 0.8.0 GUI surface while preserving its approved two-column information architecture. See `C11C_PRODUCER_0.9.0_CURRENT_STATE.md`.
