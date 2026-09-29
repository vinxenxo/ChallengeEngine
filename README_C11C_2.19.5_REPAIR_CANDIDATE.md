# C11-C 2.19.5 — Consolidated Repair Candidate

Status: **NOT FROZEN**.

This package is a consolidated repair candidate for the 2.19.x acceptance cycle. It is intentionally not a new micro-patch chain.

## What this package repairs

1. **Parallel Art Direction worker race**
   - `-Workers 7` remains real parallel execution.
   - The parent batch creates the single 720x1280 Movie Maker override.
   - Workers inherit `C11C_SHARED_MOVIE_OVERRIDE=1` and therefore never mutate or remove the project-root `override.cfg`.
   - Artifact naming remains worker-specific.

2. **Review contract tests that could block the console**
   - `C11CParallelReviewWorkerIsolationContractTest.gd` is static/source-only.
   - `C11CVisualDrillReviewEnvelopePathContractTest.gd` is static/source-only.
   - Neither launches PowerShell, FFmpeg or Movie Maker.

3. **Direct suite launcher hardening**
   - `c11c-suite/c11c-test/run_suite.bat` delegates to `run_suite.py`.
   - `run_suite.py` uses a 120-second timeout and terminates Godot if the test does not exit.

4. **Launcher normalization**
   - Canonical `c11c-suite` launchers use project-root resolution and explicit exit-code propagation.
   - `c11c-maintenace` remains compatibility-only and delegates to canonical `c11c-maintenance`.
   - Active `c11c-suite` launchers are checked for any `c11c-studio` dependency.

5. **Documentation consolidation**
   - Current state, acceptance gate, 2.19 history, handover, start prompt and next prompt are synchronized around 2.19.5.

## What this package does not change

No C11-B simulation truth, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `RenderedFrameStream`, C7 audio contract, C9 authoring semantics or logical 540x960 social geometry is modified by this repair.

`c11c-studio` is not updated.

## Required acceptance principle

Do not solve a 720x1280 regression by reducing workers to one. A valid acceptance result must demonstrate more than one concurrent worker and no 540x960 fallback.

Do not declare `FROZEN` until the full workstation acceptance gate is green.
