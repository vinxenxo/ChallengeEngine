# Current authority — Pursuit V5.3 (2026-11-15)

V5, V5.1 and V5.2 are invalidated. Use only the V5.3 archive and its SHA-256 sidecar. V5.3 retains the 4 exact pinned replacements and 16 add-only docs/prompts, but hardens installer integration, package inventory, and transaction rollback. It verifies the package-relative atomic helper and dot-sources it; stages the canonical fixture in both test and definition folders; requires exactly 37 staged Python tests and atomic I/O 7/7; validates existing destination parents and exact replacement payload bindings; uses exclusive atomic create for ADD; journals four verified backups before setting transaction_started; and bounds rollback to committed/in-flight operations only. It remains BUILT, NOT INSTALLED until native Windows PowerShell 5.1 AST, atomic I/O, actual T1 physical recovery and PREPARE_ONLY gates pass.

# C11E_E4C_PURSUIT_V5_INSTALL_AND_RECOVERY_NOTES_20261115_V3 — authoritative update

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

## V5 recovery disposition

V5 does not attempt to repair or overwrite the previous evidence trees. It accepts the user-reported V4 installed state as its preimage authority and requires exact SHA-256 matches for the four replaced files. It does not require or reinstall V2. The old V4 batch attempt remains consumed and T1 is read-only recovered from its exact receipt/media. If T1 evidence is missing, malformed, source pins differ, or physical media hashes fail, the V5 install stops before any checkout payload mutation.

V5 transaction scope: four pinned replacements (coordinator, coordinator tests, runner, runner contract tests) plus add-only versioned docs/prompts. No operation targets the canonical Pursuit definition, D consumer, D executor, CLI/GUI, music engine or frozen C11-C files. The frozen C11-C manifest is pre/post pinned. Source pin count for the V5 coordinator is 35 (the previous V4 34-file set plus the canonical Pursuit definition pin). T1's three in-receipt source snapshots remain a separate 91-entry per-run integrity contract.


## V5.1 installer parser correction (2026-11-15)

The original V5 installer was not executable under Windows PowerShell 5.1: two interpolated error strings used `$Phase:` and were rejected by the parser because the colon followed an unbraced variable reference. V5.1 changes both references to `${Phase}:`, rebuilds the installer self-hash and package manifest, and retains the same four pinned replacements, sixteen add-only documents, source pins, and PREPARE_ONLY governance. The earlier failed V5 invocation did not start the installer script: the first attempt referenced an unextracted path; the second was rejected by the parent parser. Therefore no V5 transaction or rollback occurred from those attempts. Use only the V5.1 archive, extract it to the fresh folder shown in its README, and require a successful AST parse before invocation.

## V5.3 installer deep-hardening addendum — 2026-11-15

The first complete static review found that V5.3 still set `transaction_started=true` before making its four replacement backups. This was corrected: backup preparation/journaling now runs with `transaction_started=false`; every backup is hash/byte verified and persisted; all 20 targets are rechecked immediately before the transaction boundary; and each individual target is rechecked just before its atomic operation. The installer also scans ZIP member names and duplicate paths before extraction. The staged canonical fixture is copied to both `tests/fixtures` and `definitions`, matching the test imports and canonical path consumers. The staged suite now contains 37 Python tests. The receipt and failure record carry backup records.

Status is **BUILT, NOT INSTALLED**. The Linux build environment cannot execute Windows PowerShell 5.1, so native AST/atomic-I/O checks remain mandatory operator gates. No renderer or media generation is part of installation. V5/V5.1 remain invalid.

V5.3 refuerza además el límite transaccional: exige que existan previamente todos los directorios padre; comprueba el binding exacto de cada destino REPLACE con su payload; usa creación atómica exclusiva para ADD (no sobrescribe un destino concurrente); y limita el rollback a operaciones confirmadas o a la operación REPLACE en vuelo. Los temporales en vuelo se limpian en fallo. La suite Python se exige exactamente en 37/37 y la prueba atómica amplía a 7/7 con colisión ADD.
