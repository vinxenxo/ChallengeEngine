# C11E Pursuit V2 install recovery — 2026-11-15

## Evidence identity

Failed run: `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417`. V2 package ZIP SHA-256 `b1ea9ad9f18f3078628d7dfc0fe0c58077dc387b93f467a35fedabd46fc47481`; package manifest SHA-256 `7c00decac39d89bf39fe662a6364bf3e3470f82fef7d7cbc4669dfb11324891a`. Evidence root: `artifacts/tests/c11e/e4c_pursuit_batch_overlay_install/C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417`.

## Confirmed transaction state

The failure archive records `transaction_started=true`, `committed_count=19`, `operation_count=19`, and stage `POSTINSTALL_SOURCE_PIN_RECHECK`. Its journal contains exactly 19 `ADD_COMMITTED` rows and remains `TRANSACTION_IN_PROGRESS`. No `INSTALL_RECEIPT.json` was created. The preflight passed: Python 3.13.14, PySide6 6.11.2, py_compile 3/3, pursuit tests 10/10, runner contract tests 8/8, PowerShell AST 4/4 and atomic I/O 6/6. No runner output or batch ID exists because the failure occurs before the embedded PREPARE_ONLY call.

## Defects

1. Installer line 338 redundantly re-hashes `release/C11C_FREEZE_PACKAGE_MANIFEST.json` after the preceding 34-pin post-check loop has already hashed that exact path. The V2 failure receipt did not capture the digest from the second read. This recovery treats the single current post-pin result as authoritative, records it, checks SHA and byte count, and refuses any mismatch.
2. The V2 runner declared driver SHA `dcb2c035ff5aee83a673e30347617aed67c8b382bf85af68441153611964566b`, but the driver payload SHA in the V2 manifest and package is `7164a83c882116081cda720b37c47107e9145ad2b918b759470b06c5eb3d5522`. The V2 runner contract test repeated the wrong value and did not compute the driver bytes.

## Recovery scope

V3 does not rerun V2 and does not overwrite any of its 19 ADD_ONLY destinations. It independently checks those 19 files against the original V2 package manifest and journal, validates all 34 protected source pins and the 796,318-byte frozen manifest, then replaces exactly two files whose V2 preimages are SHA pinned: the runner (`e31cd6...`) and its test (`f7948339...`). Both real backups are written and verified. The coordinator and business logic remain unchanged. Fifteen new versioned documents/prompts are added.

After installation, the fixed runner is launched once in default `PREPARE_ONLY`, with stdout/stderr separated and no `-Execute`. A new BatchId is produced only if all gates pass. This stage creates no media, no execution lock and no production dispatch. Independent audit is required before any separate execution authorization.

## Pursuit recovery V4 — authoritative installer correction (2026-11-15)

The V3 recovery package was not executed: Windows PowerShell 5.1 rejected its script at parse time because the audit-receipt hashtable declared `source_pins_post` twice (the summary key and detailed array). The parser error occurred before installer execution, so V3 made no checkout mutations. Do not run V3.

V4 is the only recovery candidate. It retains the 19/19 ADD_ONLY destinations committed by V2, audits the exact V2 run `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417`, corrects the duplicate key to `source_pin_results_post`, and adds an operator-side `Parser.ParseFile` gate before invoking the installer. Its transaction is bounded to two SHA-pinned replacements (pursuit runner and runner-contract test) plus 15 ADD_ONLY documentation/prompt destinations. It must pass 34/34 source pins, frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` / 796318 bytes, Windows PowerShell 5.1 AST, Python 3.13 tests and atomic I/O 6/6 before mutation.

V4's default embedded pursuit action is PREPARE_ONLY. Do not pass `-Execute`. Independently audit the V4 receipt, journal, two backups, 17 postimages, 34 source pins and the resulting five-selector BatchId before authorizing a later execution. Preserve all failed evidence. C11-C/E1/dispatch boundaries remain unchanged.
