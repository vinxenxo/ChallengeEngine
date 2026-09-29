# C11-C 2.19.12 — Exclusive tooling bugfix

## Fixed

- `c11c-suite/c11c-producer/test_gui_contract.bat` now points to the existing canonical `test_producer_gui_contract.py`.
- `tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1` now exposes canonical `WorkerRoot` values for private worker sandboxes. `Root` remains a compatibility alias, and `run_c11c_art_direction_batch_v4.ps1` consumes `WorkerRoot`.

## Preserved

- Genuine `Workers=7` parallel execution via `Start-Job`.
- Private temporary Godot project roots.
- No global mutex and no serial fallback.
- `c11c-suite` as the only active Suite surface.
- `c11c-studio` untouched and non-operational.
- C11-B/C7/C9 and logical 540x960 frozen boundaries.

## Status

Candidate only; not frozen.

## Late workstation QA closure — 2026-09-29

- Normalized absent Challenge `reveal_duration` to a zero-second optional phase across active C11-C production/smoke QA.
- Added `run_c11c_challenge_family_smoke.ps1/.bat`, defaulting to `CHALLENGE_003` and `MIN_540`.
- Registered the diagnostic in Suite Test, Producer and Maintenance; aligned Producer's current Challenge review manifest with C11-C QA.
- Added the consolidated failure-prevention rulebook for Windows PowerShell 5.1, encoding, StrictMode, ffprobe, paths, Challenge discovery/timing and worker isolation.

C11-C remains **CANDIDATE / NOT FROZEN** until workstation closure evidence is complete.
