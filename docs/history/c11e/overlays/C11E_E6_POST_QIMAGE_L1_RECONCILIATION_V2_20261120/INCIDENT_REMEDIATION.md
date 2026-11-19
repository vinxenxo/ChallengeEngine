# Incident remediation — V1 source byte-count null handling

| Item | Finding |
|---|---|
| Blocked gate | `v2_7_qt_receipt` |
| V1 check | `source_pins=false` |
| Affected rows | `smoke18_reuse_requalification`, `option_c_v4_install_receipt`, `loop_policy_v2_receipt`, `a3_diagnostic_v1` |
| Expected vs actual SHA-256 | Identical for all four rows |
| Expected bytes | `null` for all four rows |
| Actual sizes | 11024, 1270, 7430 and 5595 bytes |
| Defect | Null optional byte count treated as mandatory exact zero/null equality |
| Correction | SHA-256 remains mandatory; byte count exact only when declared as a valid non-negative integer |

The evidence does not show a source-content mismatch. V2 does not replace the historical receipts or fill missing byte-count fields in them.
