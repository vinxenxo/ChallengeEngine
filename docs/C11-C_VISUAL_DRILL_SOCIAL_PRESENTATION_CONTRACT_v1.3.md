# C11-C Visual Drill Social Presentation Contract v1.3

**Release:** C11-C 2.2.2 — COMMON PRESENTATION OVERLAY

## Common presentation

Visual Drills consume the same presentation layer as Visual Loops.

- Logical canvas: `540x960`.
- Header region: `y=0..144`.
- Body region: `y=144..816`.
- Footer region: `y=816..960`.
- Physical social output: `720x1280`, 9:16, 30 FPS.
- Physical scaling: exactly `4/3`, applied once at the complete presentation boundary.

## Header

The former first header text is not rendered. Its occupied upper space remains as intentional margin. The existing double-line header block remains in its prior vertical position. The separator moves immediately below it.

The double-line header block is the sole header text block. Matrix/airport-board animation is enabled for Visual Drills. The deterministic sequence is:

1. Existing double-line header text.
2. Former first header text.
3. Former second footer text.
4. Former third footer text.

The sequence is distributed over the complete render duration and preserves multiline structure while scrambling characters during transitions.

## Footer

Only the first footer text remains visible. The former second and third footer texts are consumed by the header Matrix sequence. The footer separator remains the leading separator.

Header typography is `21` logical px with deterministic fit-down. Footer typography is `14` logical px with deterministic fit-down.

## Audio/social

The previously closed shared social sidecar and one global deterministic ambient master remain unchanged. `-NoSound` and `-Silent` still disable audio.

## Scope boundary

No drill mechanic, simulation mathematics, RNG ownership, `SimulationResult`, timing truth, `winning_frame`, C7, C9 or frozen C11-B geometry is modified by this contract.
