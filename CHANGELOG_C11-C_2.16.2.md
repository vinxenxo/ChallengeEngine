# C11-C 2.16.2 — Post-Review Runner + Editorial Spacing Refinement

## Scope
- Keeps C11-C 2.15.1 frozen and continues the 2.16.x post-freeze art-direction branch.
- Fixes the Visual Art Direction Review V3 PowerShell `Seeds` parameter binding bug by passing one typed `[int[]]` array.
- Keeps the review runner at 7 workers by default and resumable via `-Resume`.
- Restores a larger visual gap between the Header/Footer text boxes and their separator rules.
- Increases shared Header typography from 25px to 27px while retaining Bold.
- Keeps Header at three lines and Footer at up to three lines.

## Editorial geometry
- Header text box height: 128 logical px; separator at Y=140.
- Footer text box starts at Y=28 logical px; separator at Y=14.
- Separator rules remain visible.

## No engine truth changes
Simulation truth, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, C11-B frozen contracts, C7 ownership and C9 authoring contracts are untouched.
