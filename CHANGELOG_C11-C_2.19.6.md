# C11-C 2.19.6 — Consolidated Final Repair Candidate

Date: 2026-09-28
Status: **FINAL REPAIR CANDIDATE — NOT FROZEN**

## Consolidated 2.19 lineage

2.19.0–2.19.5 are historical implementation steps absorbed into this candidate. The 2.19.3-v2 mutex experiment is explicitly rejected.

## Runtime repair retained

Fresh worker roots exclude source `.godot`, then perform a one-time headless Godot editor bootstrap to generate and verify `global_script_class_cache.cfg` with `PresentationProfile`. Movie Maker captures remain genuinely concurrent across up to 7 workers.

## Final acceptance repair

The remaining failure was a test false negative. The worker contract test compared the pool creation marker with the `Start-LoopReviewJob` function declaration. It now compares the actual `Start-LoopReviewJob -FamilyId` invocation.

## Suite launcher consolidation

`c11c-suite/` is the sole active Suite surface. Active BAT/CMD launchers are normalized to UTF-8 without BOM and retain their previous command semantics. `c11c-studio/` remains retired and untouched.

## Explicit non-changes

No simulation truth, RNG ownership/algorithm, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts or logical 540×960 geometry were changed.

## Acceptance status

Windows/Godot runtime acceptance is still required. Final freeze remains prohibited until the focused test, genuine 7-worker review, full logical corpus, retrocompatibility, physical gates, full acceptance and formal freeze seal pass.
