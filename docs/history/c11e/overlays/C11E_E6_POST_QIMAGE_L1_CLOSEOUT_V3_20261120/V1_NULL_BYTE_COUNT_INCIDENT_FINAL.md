# V1 null byte-count incident — final disposition

## Finding

V1 reported `v2_7_qt_receipt.source_pins=false`. Four rows were affected:

- `smoke18_reuse_requalification`
- `option_c_v4_install_receipt`
- `loop_policy_v2_receipt`
- `a3_diagnostic_v1`

For each row, the recorded expected SHA-256 exactly equaled the active file SHA-256. `expected_bytes` was `null`; actual sizes were 11024, 1270, 7430 and 5595 bytes. V1 incorrectly performed an unconditional byte-count comparison.

## Corrective rule in V2

1. Source existence and the exact SHA-256 remain mandatory.
2. If `expected_bytes` is a valid non-negative integer, actual bytes must equal it exactly.
3. If `expected_bytes` is `null`, record `NOT_DECLARED_SHA256_ONLY`; do not infer or fabricate a size.
4. A malformed non-null byte-count value blocks.

V2 tests 18–21 specifically cover these semantics. The operator result was 21/21 tests and 18/18 read-only checks PASS.

## Disposition

`CLOSED_BY_V2_READ_ONLY_RECONCILIATION`. The V1 blocked receipt remains immutable historical evidence. No historical receipt was edited and no missing byte-count value was filled in after the fact.
