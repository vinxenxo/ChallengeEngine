# C6-F0.3.4 — CTA Regression Root Cause & Surgical Recovery

## Finding
The temporal extraction is not the root cause of the missing CTA visual.

`CHALLENGE_001.mp4` in the supplied baseline is 540 frames / 9.0 s, matching the manifest telemetry:
- `hook_frames=0`
- `game_frames=420`
- `reveal_frames=0`
- `cta_frames=120`
- `total_frames=540`

The last frame therefore lies in the CTA interval. The temporal authority is reaching the CTA.

## Root cause
The regression was introduced in the E2 presentation render-model revision (`437db61 -> 69e6a3b`), not by the later temporal extraction.

The prior certified binder supplied these fallback render-model values:
- `cta_main = "LINK IN BIO"`
- `cta_sub = "¡Juega ahora!"`

The later revision changed both defaults to empty strings. `PresentationUI.apply_render_model()` still made the CTA component visible when `cta_visible=true`, but it configured both labels with empty text. The result was a visually blank CTA section.

The pre-regression E2 artifact at `437db61` contains the expected final CTA visual, including `LINK IN BIO` and `¡Juega ahora!`; the supplied current artifact does not.

## Surgical patch
Only `core/presentation/ChallengePresentationBinder.gd` is changed:
- restore `cta_main` fallback to `LINK IN BIO`;
- restore `cta_sub` fallback to `¡Juega ahora!`;
- restore the historical `badge_text` and `success_text` defaults as part of the same render-model compatibility block.

No timeline, simulation, RNG, mechanic, factory, or export math is changed.

## Regression guard
Added `tests/C6F0_3_4CTARenderRegressionTest.gd`, registered in `tests/run_all.py`.
It verifies:
1. the terminal ChallengeTimeline frame resolves to `CTA`;
2. the CTA render model contains the historical texts;
3. `PresentationUI` makes the CTA visible and renders both labels.

## Validation status
Static inspection and artifact comparison completed from the supplied baseline.
Godot execution of the patch could not be performed in this Linux analysis environment because the supplied runtime is Windows-side (`godot` executable is not available here).
Local Windows execution is therefore required before certification.
