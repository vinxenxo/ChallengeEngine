> **Historical snapshot — final functional baseline: C11-C 2.19.1.** This file preserves the state, proposal or repair of its named release. Later integration through 2.19.1 (plus absorbed 2.19.2 test-only contract maintenance) is recorded in `docs/history/c11c/releases/C11-C_2.12_to_2.19.1_CUMULATIVE_HISTORY.md`. Historical text is preserved rather than rewritten.

C11-C 2.12.0 OVERLAY

Baseline: C11-C 2.11.1

Copy the overlay contents into the repository root, preserving paths. This overlay is not a full project ZIP.

New production commands:
- .\tools\prototypes\c11c_bulk\run_c11c_weekly_production_batch.ps1
- .\tools\prototypes\c11c_bulk\run_c11c_monthly_production_batch.ps1

Review command:
- .\tools\prototypes\c11c_bulk\run_c11c_visual_loops_subtype_music_coverage.ps1 -ResetReviewAssets

Weekly output: artifacts\batch\week\XXXX\<day>\...
Monthly output: artifacts\batch\month\YYYY-MM\week1..weekN\...

The batch uses the protected canonical production launcher and passes family + seed + technical grammar explicitly.
