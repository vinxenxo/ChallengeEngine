> **SUPERSEDED by C11-C 2.2.1 / Contract v1.3.** Visual Drill Matrix is now ON and the common header/footer layout has moved to the 2.2.1 presentation overlay.

# C11-C Visual Drill Social Presentation Contract v1.2

**Release:** C11-C 2.2.0 — VISUAL DRILL SOCIAL PRESENTATION FOUNDATION

## Closed common layer

Visual Drills consume the same social/editorial presentation boundary as Visual Loops.

- Logical canvas: 540x960.
- Header: logical y=0..144.
- Body: logical y=144..816.
- Footer: logical y=816..960.
- Physical social output: 720x1280, 9:16, 30 FPS.
- Physical scaling: exactly 4/3, applied once to the complete presentation root.
- Individual drill renderers and mechanics do not compensate for physical scaling.
- Shared Header/Footer refinements from C11-C are applied.
- Matrix/split-flap transition is OFF for Visual Drills.
- Social sidecar metadata is generated per render.
- Audio is ON by default.
- A single deterministic global ambient master is reused across every Visual Drill family and seed.
- `-NoSound` and `-Silent` disable audio.

## Scope boundary

This release does not define or modify drill mechanics, simulation mathematics, RNG ownership, `SimulationResult`, timing truth, `winning_frame`, C7, C9, or C11-B geometry.

The next phase is limited to family-specific mechanic refinement and art direction: Tracking, Saccade, Pursuit and Peripheral Scan.
