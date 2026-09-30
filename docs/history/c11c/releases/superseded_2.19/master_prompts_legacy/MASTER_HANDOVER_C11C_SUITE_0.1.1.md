> **Historical cross-context prompt.** Current repository authority is C11-C 2.19.2 under `docs/current/c11c/`.
>
# MASTER HANDOVER — C11-C Suite 0.1.1

## Current state

C11-C audiovisual manufacturing remains on the established frozen backend contract. The operator-facing phase has introduced `c11c-suite/` with TEST, CATALOG, MAINTENANCE, CONFIG and the relocated PRODUCER.

## Hotfix included

`tools/prototypes/c11c_bulk/run_c11c_production.ps1` now guards the `REVIEW_720` native-review path against a same-path `Copy-Item`. This is an orchestration/package safety correction only.

## Regression protection

`tests/C11CProductionReviewCopySafetyTest.gd` is registered in `tests/run_all.py`. The current registry contains 134 suites.

## Next phase

Keep the engine and audiovisual manufacturing contracts closed while iterating on Suite usability. New GUIs must call or inspect existing canonical surfaces rather than implement replacement logic.
