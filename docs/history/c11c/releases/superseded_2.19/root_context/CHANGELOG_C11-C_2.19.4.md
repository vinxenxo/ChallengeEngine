# C11-C 2.19.4 — Consolidated Repair Candidate Changelog

## Why 2.19.4 exists

The 2.19.2 freeze claim was invalidated for final-freeze purposes after workstation acceptance exposed multiple independent issues. The 2.19.3 repair line consolidated those issues, but its v2 mutex workaround solved the Movie Maker resolution race by serializing the supposedly parallel review workers.

2.19.4 is the consolidated replacement: one worker, one temporary Godot project root, one temporary `override.cfg` and one private `.godot` state. No global capture mutex is used.

## Functional/tooling scope

- preserves the proven temporary AVI capture route;
- preserves canonical social-hook sourcing;
- preserves 17 s default Drill gameplay and 21 s Tracking gameplay;
- preserves C10-C `--qa-mode` handling for the deliberate short physical smoke;
- preserves C11-A.1 factory isolation and unique acceptance roots;
- restores known-good Art Direction batch source and keeps it PowerShell-5.1-friendly with UTF-8 BOM encoding;
- introduces a real per-worker project sandbox for Art Direction loop captures;
- adds runtime maximum-observed worker-concurrency evidence;
- adds `C11CParallelReviewWorkerIsolationContractTest.gd` and registers it in `tests/run_all.py`;
- advances the active Suite to 0.1.4 and audits operational launcher sources for any `c11c-studio` dependency;
- replaces the maintenance GUI's obsolete 2.16.9 documentation reorganizer with the canonical 2.19.x consolidation utility;
- creates a single current 2.19 consolidated history and new C11-C master/start prompts.

## Explicit non-goals

No changes are made to C11-B/C simulation truth, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 semantics or logical 540×960 social geometry.

## Status

**REPAIR CANDIDATE — NOT FROZEN.** Final freeze requires the workstation acceptance gate to pass and the Art Direction batch to prove observed concurrency greater than one.
