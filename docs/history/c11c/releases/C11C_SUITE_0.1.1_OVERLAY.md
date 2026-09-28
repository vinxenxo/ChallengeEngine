# C11-C Suite 0.1.1 + Longform Review Packaging Fix

## Included

1. Fix the `REVIEW_720` same-path `Copy-Item` failure in `run_c11c_production.ps1`.
2. Add `C11CProductionReviewCopySafetyTest.gd` and register it in `tests/run_all.py`.
3. Add `c11c-suite/` with TEST, CATALOG, MAINTENANCE, CONFIG and PRODUCER.
4. Move the live Producer under `c11c-suite/c11c-producer/` and retain the original root entry points as compatibility shims.
5. Keep the requested `c11c-maintenace` spelling as a compatibility alias to canonical `c11c-maintenance`.
6. Add architecture, GUI contract, operator and handover documentation.
7. Remove Python Windows-path escape warnings from the new GUI source paths without changing runtime behavior.

## Safety boundary

No Challenge mechanics, RNG, simulation semantics, presentation truth, audiovisual ownership or renderer mathematics have been changed.

## Validation

Python compilation with warnings treated as errors passes for all Suite Python sources, and `c11c-suite/self_test.py` passes in the build environment. Windows/PySide6/Godot runtime acceptance remains the final local gate.
