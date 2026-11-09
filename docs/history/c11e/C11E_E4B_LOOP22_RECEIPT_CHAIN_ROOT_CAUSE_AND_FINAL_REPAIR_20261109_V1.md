# C11-E E4B Loop22 — Receipt Chain Root Cause and Final Repair V1

**Date:** 2026-11-09  
**Disposition:** Installer-debug subtask root cause established; no Loop22 media qualification is claimed yet.

## 1. What failed

The operator installed `C11E_E4B_LOOP22_AV_RECEIPT_PIN_FIX_V2_20261109.zip` successfully:

- `INSTALL_STATUS=PASS_ADD_ONLY_INSTALL`
- source pins: 37/37
- prior postimages: 13/13
- payload: 11/11
- added: 11/11
- package manifest SHA-256: `aa7cdb169dcddf469c16b02d6e70b2e09e8c2ea4059bebca20c51d7d25ef02ba`
- install receipt SHA-256: `7de2dd2ccbc1eaf6c48e2997d21d3d2474cbd8c268bc8b51ca2a4ce03263f28e`

The subsequent exact-pinned repair script stopped during its preflight at `frozen_c11c_manifest_sha256`. It did not change the V4 wrapper and did not invoke the media runner.

## 2. Actual root cause: receipt producer, not receipt consumer

In `INSTALL_C11E_E4B_LOOP22_AV_RECEIPT_PIN_FIX_V2.ps1`, the frozen-manifest pin used during package validation is correct (64 hex characters). The actual C11-C manifest on disk is also correct:

`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`

However, the install receipt constructor near line 130 writes this malformed value:

`e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953`

It is 63 characters: one `5` is missing after `...959535`.

The installer then checks only that the serialized receipt bytes match the generated receipt digest and that its sidecar matches those bytes. It does not deserialize the newly written receipt and validate the semantic field values. Therefore the installer can print `PASS_ADD_ONLY_INSTALL` while its own receipt contains invalid governance metadata. The payload copy itself can still be byte-correct; the receipt's semantic assertion is not.

This explains the latest operator error exactly. The downstream audit correctly rejected the malformed value. The earlier hotfix failed before any mutation because it correctly checked the receipt before patching V4.

## 3. Independent V4 defect

The installed V4 wrapper declares `$BaseV2ReceiptSha256` but one assertion uses `$BaseV2ReceiptSha` (missing the `256` suffix). That evaluates to an empty string and causes the previous V4 receipt-field mismatch. The previous hotfix had an exact single-reference patch for this defect, but it was never applied because the malformed Receipt Pin V2 receipt failed first.

The audited V4 source identities are:

- exact preimage SHA-256: `c6adf58e2ecb22dc0400c139626034755ca13716a9bbebae276805e01f732dab`
- exact one-reference postimage SHA-256: `92e9ee5e922ee55b2eee25b17e0d7aa0462c2d78fa24dc7e2c1af7cce57ebb63`

The transformation is limited to the single assertion referencing `$BaseV2ReceiptSha`.

## 4. Final repair strategy

Do not reinstall V1, V2, shared-directory V1, or Receipt Pin V2. Do not create another package installer.

Use the one-shot repair script `FIX_C11E_E4B_LOOP22_RECEIPT_AND_V4_ONESHOT_V1.ps1`. It:

1. checks the active checkout and canonical frozen manifest;
2. verifies predecessor install receipts, hashes, sidecars, counts and the exact known malformed Receipt Pin V2 receipt preimage;
3. verifies the exact V4 preimage and one unbound variable reference;
4. stages the corrected receipt/sidecar and exact V4 postimage before any replacement;
5. preserves both original preimages in a timestamped evidence folder;
6. performs only two scoped repairs: the generated install receipt field/sidecar and the single V4 assertion;
7. records a correction receipt and rollback information;
8. invokes the existing V4 wrapper immediately. V4 remains the only authority to run its bridge test, AST checks, 25 focused tests and fail-closed media preflight before any capture.

This is a surgical repair, not an installer: it adds no package payload and does not rerun any installation.

## 5. Loop22 status and acceptance boundary

The shared-directory runner fix is independently covered by the 25-test focused contract suite in the isolated fixture: 44 logical A/B jobs map to 40 unique output directories; each is created once, with `exist_ok=False` retained. That fixture result is not a Windows active-checkout media qualification.

No 44-slot media run is established by any of the V1/V2/V3/V4/hotfix failures described above. In particular:

- completed Loop22 captures: 0
- completed Loop22 A/V outputs: 0
- accepted A/B pairs: 0
- Loop22 human review: not started

The actual next task is to pass the existing V4 preflight and execute 22 selectors × A/B = 44 qualifications. Technical acceptance requires 44/44 and 22/22 A/B pairs. Operator visual/editorial/layout and audio review of all 44 outputs is still mandatory.

## 6. Phase order and governance

E4C Drill must not be declared started or accepted until Loop22 technical and human closeout is complete. E4C remains the next roadmap phase after that gate; E5 → E6 Smoke18 → E7 Matrix101 → E8 follow in order. CH_008/CH_009 remain held for the declared 11-second versus 12-second phase-sum conflict.

C11-C 2.19.12 remains immutable. Frozen manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No Git checks; commits are operator-managed. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.
