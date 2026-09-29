# C11-C 2.19.12 — Exclusive tooling bugfix

## Fixed

- `c11c-suite/c11c-producer/test_gui_contract.bat` now points to the existing canonical `test_producer_gui_contract.py`.
- `tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1` now exposes canonical `WorkerRoot` values for private worker sandboxes. `Root` remains a compatibility alias, and `run_c11c_art_direction_batch_v4.ps1` consumes `WorkerRoot`.
- `tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1` now resolves the authoritative `build_factory.py` manifest path from factory stdout, the historical canonical path, or a unique valid manifest inside the current run. Ambiguous or missing manifests fail closed.
- C11-A.1 factory artifact paths are now resolved relative to the resolved manifest directory, preserving absolute paths when explicitly declared.

## Preserved

- Genuine `Workers=7` parallel execution via `Start-Job`.
- Private temporary Godot project roots.
- No global mutex and no serial fallback.
- `c11c-suite` as the only active Suite surface.
- `c11c-studio` untouched and non-operational.
- C11-B/C7/C9 and logical 540x960 frozen boundaries.

## Status

Candidate only; not frozen.
