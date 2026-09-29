# C11-C 2.19.5 — Consolidated Repair Candidate

**Status: NOT FROZEN**

This release candidate consolidates the remaining 2.19.x workstation/toolchain defects into one repair set. It is not another micro-patch overlay.

## Included repairs

### 1. Parallel Art Direction worker isolation

The previous 720x1280 -> 540x960 regression was traced to concurrent workers mutating the same project-root `override.cfg`.

The repaired ownership model is:

- parent batch creates the single 720x1280 Movie Maker override;
- parent arms `C11C_SHARED_MOVIE_OVERRIDE=1`;
- all `Start-Job` workers inherit that flag;
- worker-side Movie Capture helper treats the override as externally managed and does not touch the root file;
- parent restores the override only after all selected stages finish.

`-Workers 7` therefore remains true parallel execution.

### 2. Non-blocking review contract tests

`C11CParallelReviewWorkerIsolationContractTest.gd` and `C11CVisualDrillReviewEnvelopePathContractTest.gd` are source-only tests. They inspect orchestration sources and must not spawn a render process tree.

### 3. Bounded direct test launcher

`c11c-suite/c11c-test/run_suite.bat` delegates to `run_suite.py`, which gives each direct Godot test a 120-second deadline and terminates Godot on timeout.

### 4. Suite launcher normalization

The canonical launchers under `c11c-suite` now resolve the project root consistently and propagate child exit codes. The historical typo launcher `c11c-maintenace` delegates to canonical `c11c-maintenance`.

The launcher verifier scans the active `c11c-suite` launcher surface and rejects any `c11c-studio` dependency.

### 5. 2.19 documentation consolidation

A single current-state document, acceptance gate, documentation index, workstation command sheet, consolidated changelog, master handover and start prompt are provided for the branch.

Historical 2.19.2/2.19.3 notes are preserved as history rather than rewritten. An idempotent maintenance script is included for moving the old active-looking 2.19 notes into the historical releases area.

## Explicit non-changes

No C11-B simulation truth, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio contract, C9 semantics or logical 540x960 social geometry is changed.

`c11c-studio` is not updated and is not part of the active toolchain.

## Acceptance prerequisite

Do not freeze from static self-test alone. Require focused contract PASS, launcher-verifier PASS, representative game tests PASS, full logical suite PASS, parallel Art Direction review PASS at `Workers=7`, and the remaining physical/export acceptance gates PASS.
