# QImage and L1 receipt shape correction

V1 mistakenly assumed QImage test count could be read as a scalar from `qimage_tests`. In the V2.7 receipt, `qimage_tests` is an object with `run`, `tests`, `failures`, `errors` and `status`. V2 validates all five, plus runtime and benchmark fields.

V1 also read `e6_accepted` from the top-level L1 receipt. The V2 L1 schema places it in both `phase_state` and `governance`. V2 requires both to equal zero. It also validates all 18 check rows, zero blocked checks, the exact PASS_WITH_VISUAL_REVIEW_PENDING status and `no_execution_authority_created=true`.

Regression tests cover valid shape, wrong test count, test failures/errors, performance over-budget, governance drift, missing nested E6 values and inconsistent L1 check totals.
