# E6 Composition Readiness — Source Pin Adjudication V1

**Disposition:** `AUDIT_PACKAGE_PIN_LITERAL_ERROR_RECONCILED_NOT_LIVE_SOURCE_REGRESSION`.

## Finding

The V1 composition-readiness source-pin manifest carried an incorrect expected SHA-256 for `tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd`. The user's active-checkout V1 audit receipt reported the actual file at 26,367 bytes with SHA-256 `eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203`; V1 incorrectly expected `eba81fff3d0f7c4b5d6b5eeb55c5e14a4d25b44c040c4cc6d2d59b6c9a631203`.

This is not a source update or a file to be overwritten. The corrected actual SHA was already included as a PASS in the earlier active-checkout E6 D9 dependency-pin reconciliation, report `E6D9PINREC_20261118T090219Z_97FFB0DD`, SHA-256 `fa54b47826f58acc823d45a8771a2dc12827d34d46d9586a34b8f6813a9e0603`, among 33/33 accepted source-pin checks. The user's V1 composition-readiness receipt, SHA-256 `d57a4b90d89adc94c0471719f619d45e4289be3b3e10a2ba1b88e1804f0aa3a6`, independently records the same actual path/hash/byte count and the single mismatch.

The comparison nightly ZIP also contains this exact byte sequence, but it remains comparison evidence only. The active checkout remains the authority. V2 verifies both immutable active-checkout receipts and requires the exact consumer path/hash pair to appear in the prior 33-pin PASS report before adjudication can pass.

## Technical interpretation

The difference between the earlier E4A.6 consumer postimage and the current file is consistent with the reserved-band black-state hardening: the consumer mounts the existing header/footer regions while enabled, forces both backgrounds opaque black, and suppresses inactive text/rules. That matches the already accepted reserved-band requirement. V2 does not modify this source; it only records the previously accepted current hash.

## Correction boundary

- New versioned pin manifest V2 only; V1 remains immutable.
- All other 16 pins are byte-identical to the V1 declarations.
- Active `C11EChallengeLiveEditorialConsumer.gd` is read-only and must remain at its current SHA.
- Frozen C11-C manifest and D4.8 R1V V2 remain unchanged.
- V2 audit must verify all 17 pins, 36 Challenge PREPARE_ONLY evidence files, the prior 33-pin report, and the V1 blocked audit receipt.
- Passing this reconciliation closes only the false source-pin blocker. It does not implement Loop D composition, populate Challenge editorial fields, accept reuse candidates, finalize D4.8 successor policy, authorize TEST_ONLY execution, or activate production.

## Next gate

Run the V2 audit once. Expected: `SOURCE_PINS=17/17 PASS` and `V1_PIN_ADJUDICATION=PASS_AUDIT_PACKAGE_PIN_ENTRY_ERROR_RECONCILED`. Continue only with the separately recorded outstanding gates; do not rerun E4/E5 or accepted A/V batches.
