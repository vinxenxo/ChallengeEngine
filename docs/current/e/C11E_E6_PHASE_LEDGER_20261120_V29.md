# C11-E E6 phase ledger — V29

## Accepted
- V2.7 synthetic QImage: 37/37; seven iterations; P50 4.7681 ms; P95 5.5743 ms; `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`.
- L1 reconciliation V2: 18/18; receipt SHA `24c2a4f09901a3d1c888d972aabf2a7016496f48e5011b512a1e261338d72474`.
- L1 closeout docs V3: 16/16 ADD_ONLY; receipt SHA `08321c5988aecca20cc668ab69b95e0ab854006b524dda0d4df205a79defeed6`.
- Loop Source Closure V1: installer 22/22 ADD_ONLY, focused tests 27/27 PASS, six selected MP4 sources successfully rehashed. Its audit receipt is retained with 118 checks: 113 PASS, 2 PENDING, 3 BLOCKED.

## V1 false-negative analysis

All three BLOCKED rows were auditor semantic defects confirmed by operator-supplied JSON:
1. `d4_8_v2_immutable`: expected SHA typo; actual D4.8 bytes/hash match the correct frozen pin.
2. `qimage_l1_semantics`: nested `qimage_tests` object compared to scalar rather than validating `run/tests/failures/errors/status`.
3. `l1_reconciliation_semantics`: top-level `e6_accepted` read as null although authoritative `phase_state` and `governance` contain zero.

No historical file or receipt should be rewritten. V2 contains code-only semantic fixes and additional tests; operator execution remains pending.

## Current true pending gates

- Source color matrix/primaries/transfer remain undeclared.
- Operator visual review of the three synthetic QImage preview PNGs remains pending.
- No real RGB24 buffer is materialized; the historic decoded stream is YUV420P. No color conversion is authorized.
- L2 remains not ready; successor policy and execution manifest remain unarmed drafts.
- Challenge and Drill runtime readback are separate open gates. Smoke18 remains a draft; E6 accepted 0.

D4.8 V2 remains BLOCKED/unchanged; renderer/media/dispatch OFF; release authority NONE.
