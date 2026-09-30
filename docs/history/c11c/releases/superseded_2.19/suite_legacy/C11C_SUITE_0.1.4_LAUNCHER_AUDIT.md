# C11-C Suite 0.1.4 — Active Launcher Map

| Surface | GUI operation | Canonical CLI/backend | Status |
|---|---|---|---|
| Test | acceptance | `FULL_ACCEPTANCE_C11C_2.19.12.ps1` | ACTIVE |
| Test | A1 single qualification | `FULL_ACCEPTANCE_C11C_2.19.12_A1_SINGLE.ps1` | ACTIVE |
| Test | C11-C Challenge review | `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` | ACTIVE |
| Test | complete video review | `tools/qa/c11/run_c11c_complete_video_review.ps1` | ACTIVE |
| Producer | Challenge review | `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` | ACTIVE |
| Producer | Loop/Drill/Longform production | `tools/prototypes/c11c_bulk/*` | ACTIVE |
| Maintenance | safe cleanup | `tools/prototypes/c11c_bulk/clean_c11c_artifacts.ps1` | ACTIVE |
| Maintenance | docs consolidation | `tools/maintenance/consolidate_c11c_2_19_documentation.ps1` | ACTIVE |
| Maintenance | layout | `tools/maintenance/verify_repository_layout.ps1` | ACTIVE |
| Maintenance | frozen package | `tools/maintenance/create_c11c_freeze_zip.ps1` | ACTIVE |

Every new D tool should follow this same model: one canonical backend operation, exposed in CLI and the appropriate Suite surface.
