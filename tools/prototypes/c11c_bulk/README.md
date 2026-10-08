# C11-C Bulk Review Tooling — 2.19.4

## Canonical Art Direction runner

`run_c11c_art_direction_batch_v4.ps1` is the active 27-loop / 20-drill / 5-longform review orchestrator.

`-Workers 7` is a real concurrency contract. Loop captures are assigned to separate temporary Godot project roots, each with private Movie Maker `override.cfg` and `.godot` state. A project-global mutex is deliberately not used.

The worker pool excludes generated `artifacts/`, `.godot/`, `.git/`, caches and retired `c11c-studio/` from its project copies. Each worker reports its slot and root, and the batch records maximum observed worker concurrency.

Historical runner variants remain evidence. New operational changes should target the canonical `run_c11c_art_direction_batch_v4.ps1` and related Suite surfaces.

## Current D7/D8 state

C11-C 2.19.12 is frozen. C11-D D7 is PASS/CLOSED and FROZEN; D8.0 is the next phase. The active C11-D baseline is `ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip` (SHA-256 `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`).

## Directory contents

### Subdirectories
- None.

### Representative files
- `C11CProductionBatchCommon.ps1`
- `C11CReviewWorkerIsolation.ps1`
- `C11CVisualDrillReviewEnvelopeGenerator.gd`
- `C11C_PRODUCTION_25_HOTFIX_README.md`
- `C11C_PRODUCTION_POLICY.md`
- `C11C_PRODUCTION_SEED_BANK_v1.json`
- `C11C_TOOLCHAIN_CANONICAL.md`
- `SEED_MATRIX_C11C_V1.json`
- `clean_c11c_artifacts.ps1`
- `export_all_review_assets.ps1`
- `export_review_gifs.ps1`
- `export_review_keyframes.ps1`
- `reset_c11c_artifacts.ps1`
- `retire_legacy_c11c_tool_versions.ps1`
- … 29 additional files.
