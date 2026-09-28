# C11-C 2.19.5 — Final Consolidated Repair Changelog

## Purpose

2.19.5 is the consolidation point for the complete 2.19 branch. It absorbs the verified 2.19.0–2.19.4 implementation lineage and repairs the remaining workstation defects without reopening engine truth.

## Final repair changes

- Restored `tools/prototypes/c11c_common/C11CMovieCapture.ps1` to a non-serialized helper. Parallel safety is provided by one temporary Godot project root per worker.
- Fixed the PowerShell worker-helper parser bug by changing `$i:` to `${i}:` in `C11CReviewWorkerIsolation.ps1`.
- Strengthened `C11CParallelReviewWorkerIsolationContractTest.gd` to reject a global mutex and invalid `$i:` interpolation.
- Strengthened `c11c-suite/self_test.py` to audit the worker helper interpolation and all canonical Suite launchers.
- Updated `FULL_ACCEPTANCE_C11C_2.19.5.ps1` to run the focused worker contract and validate the completed Art Direction concurrency manifest.
- Consolidated 2.19 documentation so 2.19.5 is the only active current authority; previous current snapshots remain historical evidence.
- Confirmed that `c11c-suite/` is the only active Suite implementation surface and `c11c-studio/` is retired.

## Historical lineage absorbed

- 2.19.0 — temporary AVI capture route.
- 2.19.1 — canonical social-hook lookup.
- 2.19.2 — test-contract alignment; final freeze claim later invalidated.
- 2.19.3 — repair consolidation.
- 2.19.3-v2 — global-mutex experiment; rejected and must not return.
- 2.19.4 — genuine worker-local concurrency architecture.

## Scope boundary

No C11-B simulation mathematics, RNG algorithm/ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 ownership/contracts, C9 semantics or logical 540×960 geometry was changed by this final repair.

## Status

**FINAL REPAIR CANDIDATE — NOT FROZEN UNTIL WINDOWS/GODOT ACCEPTANCE AND C11-C FREEZE SEAL PASS.**
