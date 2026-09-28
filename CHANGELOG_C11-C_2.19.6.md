# C11-C 2.19.6 — Consolidated Repair Candidate

Date: 2026-09-28
Status: **FINAL REPAIR CANDIDATE — NOT FROZEN**

## Fixed

### 1. Fresh-worker `PresentationProfile` parse regression
The 2.19.4/2.19.5 worker architecture correctly isolated each concurrent capture in its own temporary Godot project, but the source `.godot` directory was intentionally excluded. Fresh worker projects therefore lacked Godot's generated `global_script_class_cache.cfg`. `UnifiedSocialFrame.gd` could not resolve the `class_name PresentationProfile`, producing parse errors and gray/empty Movie Maker frames.

2.19.6 adds a one-time per-worker headless Godot editor bootstrap before capture and verifies the generated class cache contains `PresentationProfile`.

### 2. Concurrency preserved
The bootstrap is only project preparation. Movie Maker captures remain genuinely concurrent across up to 7 workers. No global mutex or one-at-a-time fallback is introduced.

### 3. Suite launcher consolidation
`c11c-suite/` is the sole active Suite surface. Canonical BAT launchers now consistently set `C11C_PROJECT_ROOT`, `cd /d` to the repository root and propagate child exit codes. The `c11c-maintenace` path remains a compatibility delegate. `c11c-studio` remains retired and untouched.

### 4. Documentation consolidation
All active 2.19 authority is consolidated under 2.19.6. Prior 2.19.0–2.19.5 current snapshots are retained as historical evidence under `docs/history/c11c/releases/superseded_2.19/`.

## Explicit non-changes

No changes were made to C11-B simulation truth, RNG ownership/algorithm, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio contracts, C9 semantics or logical 540×960 social geometry.

## Acceptance

Windows/Godot runtime proof is still required. Final freeze remains prohibited until focused worker test, 7-worker Art Direction, full logical/retro/physical acceptance and the formal 2.19.6 freeze seal all pass.
