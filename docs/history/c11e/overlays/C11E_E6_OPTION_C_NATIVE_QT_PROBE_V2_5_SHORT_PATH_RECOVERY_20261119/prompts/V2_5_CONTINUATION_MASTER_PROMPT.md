# C11-E continuation master prompt — V2.5 (2026-11-19)

Continue only from the operator's active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The active checkout is the sole source authority; ZIPs are references and must never be extracted over the checkout.

## What happened in V2.4

V2.4 ZIP SHA: `cd79f09cf4d9304cad1b555a7772b0f031c3f07d8c9c02d65d7f2da12e82f860`. Operator verified the sidecar, but `Expand-Archive` failed before installer invocation. The deepest V2.4 member is 175 characters; the selected Downloads extraction root produced a 276-character absolute path. The later `-File` call failed because the installer had not been extracted. No V2.4 install receipt exists and no V2.4 test or QImage runner executed. Do not classify this as a failed V2.4 install transaction.

Source review found two more V2.4 path hazards: a long prefix in the internal `%TEMP%` staging directory, and `.partial.<GUID>` appended to the full destination filename. V2.5 shortens outer extraction, stage root and same-directory write temporary paths; every relevant absolute path is checked before destination writes. The transactional Add-only logic, no-overwrite move, exact postimage verification, receipt/sidecar verification and rollback-of-owned-files are retained.

## V2.5 payload / what is unchanged

V2.5 installs the V2.4 A3 V4 adjudicator, pinned original diagnostic producer, runner and 17 focused tests using their original byte-identical payloads and destinations. It reuses the already-installed V2 QImage implementation and 37-test target suite by exact path; it does not replace them. It adds V2.5 incident/runbook/ledger and two continuation prompts. Do not rerun V2.1/V2.2/V2.3 tests or runners.

## Immediate task

1. Install V2.5 using the runbook's `%TEMP%\c11e25` extraction root and absolute-path preflight. Do not use the original long Downloads extraction folder.
2. Require PowerShell 5.1 AST PASS, frozen C11-C/D4.8 pins unchanged, all package member hashes PASS, outer/stage/write path budgets PASS, and all 18 destinations verified.
3. Execute V2.4's 17 focused regressions once.
4. Execute `RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_4.py` once under Python 3.13.14 / PySide6 6.11.2 with exactly seven iterations. Preserve receipt and sidecar.
5. Require A3 source/lineage PASS, all pins PASS, QImage 37/37, and native P95 <=33.333 ms. Any failure blocks; preserve the exact receipt and do not blindly rerun.
6. Inspect three synthetic previews and explicitly decide resampler quality. Approved geometry is 720x1280 canvas, body 504x896 at (108,192), black reserved bands and side gutters; this does not decide filtering quality.

## Next technical phase (not yet authorized to execute)

After a true QImage-stage PASS and accepted visual resampler review, perform read-only source closure of the real Loop input and D9.9/D9.10/R1P metadata. Pin the actual frame source, sequence/order, RGB24 byte count, dimensions, stride, color semantics and selector identity. No guessed decoder/path. Then prepare a separate bounded successor D4.8 policy and exact E6 TEST_ONLY execution manifest. D4.8 V2 remains unchanged and BLOCKED. Only after separate approval may L2 copy one real frame into the existing D seam; L3 covers negative controls and human review; L4 widens the same consumer to six Loop selectors. Do not start Smoke18 media or dispatch from this synthetic probe.

## Immutable governance

C11-C freeze manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes). D4.8 V2 SHA `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` (12,996 bytes), unchanged and BLOCKED. Renderer OFF; E1 PREPARE_ONLY; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; E6 accepted 0; no BatchId; `release_authority=NONE`. No Godot, FFmpeg, FFprobe, audio, mux, dispatch or media. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`.
