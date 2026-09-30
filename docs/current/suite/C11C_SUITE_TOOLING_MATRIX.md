# C11-C Suite — Tooling Matrix at 2.19.12 Freeze

**Suite runtime:** 0.1.4  
**Producer:** 0.9.7  
**C11-C:** 2.19.12  
**Status:** final acceptance PASS; freeze packaging pending.

## Operator rule

The Suite is an operator shell, not a second backend. GUI actions must invoke the same canonical PowerShell, Python, BAT or Godot entrypoints used from the repository root. The GUI must not duplicate production, validation, media-cleanup or packaging logic.

## Active surfaces

| Surface | Purpose | Canonical authority | State |
|---|---|---|---|
| `c11c-test` | logical regression, focused QA, C11-C acceptance/review | `tests/run_all.py`, `tools/qa/c11/*`, `FULL_ACCEPTANCE_C11C_2.19.12.ps1` | active |
| `c11c-producer` | audiovisual orchestration | Producer 0.9.7 + canonical C11-C production/review tools | active |
| `c11c-maintenance` | cleanup, repository organization, docs consolidation, freeze | `tools/maintenance/*` + C11-C cleanup script | active |
| `c11c-catalog` | catalog inspection | catalog entrypoint | active |
| `c11c-config` | declarative configuration inspection/editing | config entrypoint | active |

## Current C11-C routes

| Capability | GUI surface | Canonical CLI/PowerShell/BAT | Notes |
|---|---|---|---|
| Full logical regression | Test | `python .\tests\run_all.py` | registered suite authority |
| Focused C11-C validation | Test | `tools/qa/c11/run_c11c_focused_validation.ps1` | no full 52-video rerender |
| One-video smoke | Test | `tools/qa/c11/run_c11c_one_video_each_type.ps1` | Loop + Drill + Longform |
| Complete 52-video review | Test | `tools/qa/c11/run_c11c_complete_video_review.ps1 -Workers 7` | normal mode preserves a COMPLETE corpus |
| C11-C acceptance | Test | `FULL_ACCEPTANCE_C11C_2.19.12.ps1` | final C11-C gate |
| Documentation consolidation | Maintenance | `tools/maintenance/consolidate_c11c_2_19_documentation.ps1` | dry-run first |
| Root organization | Maintenance | `c11c-suite/c11c-maintenance/organize_repository_root.ps1` | dry-run first; archive, do not delete evidence |
| C11-C media cleanup | Maintenance | `tools/prototypes/c11c_bulk/clean_c11c_artifacts.ps1` | allowlist only; dry-run by default |
| Cleanup safety contract | Test/Maintenance | `c11c-suite/c11c-maintenance/test_cleanup_contract.py` | static contract |
| Freeze dry-run | Test/Maintenance | `tools/maintenance/create_c11c_freeze_zip.ps1 -DryRun` | validates gates/exclusions, no ZIP |
| Freeze package | Maintenance | `c11c-suite/c11c-maintenance/run_freeze_package.bat` | sole C11-C freeze package path |

## Historical routes kept deliberately

`run_c11a1_challenge_bulk_qa.ps1`, `run_c11a_visual_bulk_qa.ps1` and `tools/c11freeze/run_all.ps1` remain exposed only as explicitly labelled historical/regression routes. They are not alternative C11-C acceptance authorities.

The old `c11c-studio` surface and misspelled `c11c-maintenace` directory are retired. The latter is quarantined intact during root organization when the canonical maintenance tree exists.

## D invariant

GUI and CLI are co-equal surfaces for every D milestone. A new capability is not considered complete until:

1. its canonical command works directly;
2. the Suite can invoke that same command without duplicating logic;
3. inputs, provenance and reproducibility are equivalent; and
4. a focused parity test covers the route.

This invariant applies from D0 onward; it is not deferred to D9.
