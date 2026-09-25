# START PROMPT — ChallengeEngineV01_STATELESS / C11-C 2.12.0

Continue from validated C11-C 2.12.0 overlay on baseline C11-C 2.11.1.

## Current state
- Visual Drills: Tracking, Saccade, Pursuit, Peripheral Scan.
- Visual Loops: geometric/Geometric Waves, fractal/Fractal Bloom, kaleidoscope/Sacred Symmetry, particle_flow/Living Particles, vector_field/Invisible Forces.
- Invisible Forces currently exposes seven presentation grammars including scalar_potential.
- Coverage corpus: 27 unique visual grammars.
- FAMILY_MUSIC_V4 generator revision: 4.1.1. Visual Loops pass technical grammar_id explicitly into their launchers and music generation.
- Social copy is emoji-free and UTF-8 without BOM. Fixed hashtags: #GenerativeArt #GodotEngine #LoopArt #OddlySatisfying.
- Weekly production batch: 27 products. Monthly batch: same 27-slot pattern repeated with globally unique seeds.

## Canonical production commands
`tools/prototypes/c11c_bulk/run_c11c_visual_loops_subtype_music_coverage.ps1 -ResetReviewAssets`
`tools/prototypes/c11c_bulk/run_c11c_weekly_production_batch.ps1`
`tools/prototypes/c11c_bulk/run_c11c_monthly_production_batch.ps1`

## Frozen boundaries
Do not modify C11-B simulation truth, structural RNG, SimulationResult, winning_frame, close_calls, WinningFrameDetector, RenderedFrameStream, C7 ownership/contracts, or C9 authoring contracts.

## Validation gate
Focused tests -> aggregate `python tests/run_all.py` -> physical coverage/production review. Do not declare closure from a focused test alone.
