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
