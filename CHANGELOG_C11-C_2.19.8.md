# C11-C 2.19.8 - Changelog

## Purpose

2.19.8 consolidates the 2.19 tooling/documentation branch after the 2.19.4 workstation validation reported all focused tests green but the canonical complete-video-review launcher failed in Windows PowerShell 5.1 parsing.

## Changes

- Replaced the complete-review script's Unicode PASS-line text with ASCII-safe output.
- Added `c11c-suite/c11c-test/run_c11c_complete_review.bat` and `run_c11c_acceptance.bat`.
- Added `verify_c11c_suite_launchers.ps1`.
- Updated the C11-C test GUI to expose the consolidated acceptance, launcher audit and complete-review commands.
- Extended Suite static self-test coverage for those surfaces.
- Consolidated current 2.19 documentation and moved superseded 2.19.x docs into historical evidence via the maintenance utility.
- Created current master handover, start prompt, context index, command sheet, acceptance gate, review runbook and freeze command files.

## Explicit non-goals

No changes to simulation truth, RNG ownership, C11-B mechanics, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio ownership/contracts, C9 semantics, logical 540x960 geometry or the proven per-worker capture architecture.

## Status

**FINAL TOOLING/DOCUMENTATION CONSOLIDATION CANDIDATE - NOT FROZEN.**
