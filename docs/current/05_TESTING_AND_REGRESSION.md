# Testing and Regression — Current

## Mandatory gate

```powershell
python .\tests\run_all.py
```

Every discovered `*Test.gd` requires an explicit entry in `KNOWN_SUITES` and an explicit PASS marker. Missing registration is a fatal error.

When a suite fails, `run_all.py` re-runs that suite with `--verbose` and stores the diagnostic log in `artifacts/tests/logs/verbose/`.

## C11-C focused contracts

Run focused C11-C tests when changing visual tooling, then run the full suite. Physical production success does not replace logical regression.

## Producer / Suite tooling

`c11c-suite/c11c-producer/self_test.py` validates Producer syntax/schema/backend-profile alignment and launchers. `c11c-producer/` at the repository root is now compatibility-only.

The Suite `c11c-test` GUI reads `tests/run_all.py` rather than maintaining a duplicated test registry.

## New focused production-wrapper regression

`tests/C11CProductionReviewCopySafetyTest.gd` protects the REVIEW_720 same-path orchestration case: the canonical loop production wrapper must not call `Copy-Item` with identical source and destination paths.
