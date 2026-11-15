# C11E_E4C_PURSUIT_BATCH_RECOVERY_RUNBOOK_20261115_V3 — authoritative update

1. Preserve the V2 failed evidence root and the 19 V2 ADD_ONLY destinations. Do not rerun V2 or manually repair the files.
2. Place `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115.zip` and its `.sha256` sidecar in Downloads. Place the V3 recovery ZIP and its sidecar in Downloads.
3. Extract V3 into a new version-specific Downloads directory. Run only `INSTALL_C11E_E4C_PURSUIT_BATCH_OVERLAY_V3_RECOVERY.ps1` under Windows PowerShell 5.1 with `-PackageZip`, `-PriorPackageZip`, `-ProjectRoot` and `-PythonExe`.
4. The recovery installer first audits the original V2 run ID, exact V2 ZIP/manifest, 19 journal destinations, 34 source pins and frozen C11-C manifest. It stops before mutation if anything differs.
5. Only after the prior transaction audit passes does it install two SHA-pinned replacements with 2 real backups and 15 ADD_ONLY docs; then it checks all postimages/pins and runs the existing pursuit runner in PREPARE_ONLY.
6. If any V3 failure occurs after `TRANSACTION_STARTED=TRUE`, preserve the V3 evidence and do not rerun automatically. If it succeeds, independently audit the new transaction journal, backups, postimages, source pins and BatchId. Do not add `-Execute`.

This process makes no Git calls, does not use pip, does not modify C11-C or E1 service, and does not start Godot, FFmpeg or media rendering. Commits remain operator-managed.

## Pursuit recovery V4 — authoritative installer correction (2026-11-15)

The V3 recovery package was not executed: Windows PowerShell 5.1 rejected its script at parse time because the audit-receipt hashtable declared `source_pins_post` twice (the summary key and detailed array). The parser error occurred before installer execution, so V3 made no checkout mutations. Do not run V3.

V4 is the only recovery candidate. It retains the 19/19 ADD_ONLY destinations committed by V2, audits the exact V2 run `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417`, corrects the duplicate key to `source_pin_results_post`, and adds an operator-side `Parser.ParseFile` gate before invoking the installer. Its transaction is bounded to two SHA-pinned replacements (pursuit runner and runner-contract test) plus 15 ADD_ONLY documentation/prompt destinations. It must pass 34/34 source pins, frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` / 796318 bytes, Windows PowerShell 5.1 AST, Python 3.13 tests and atomic I/O 6/6 before mutation.

V4's default embedded pursuit action is PREPARE_ONLY. Do not pass `-Execute`. Independently audit the V4 receipt, journal, two backups, 17 postimages, 34 source pins and the resulting five-selector BatchId before authorizing a later execution. Preserve all failed evidence. C11-C/E1/dispatch boundaries remain unchanged.

## V5 — Pursuit native timeline recovery

V5.1 is the only package to use for the Pursuit batch after the V4 mismatch. Do not run V1–V4 installers again and do not reuse `E4C-PURSUIT-T1-5-20261115T140852Z-b3abbe94`. V4's first child generated T1; the wrapper then rejected it because it expected Tracking's 810/27 timeline. V5 uses Pursuit's canonical 510 gameplay frames at 30 fps plus 90-frame PRE_ROLL and END_CTA = 690/23.

1. Extract the V5 ZIP and sidecar to Downloads; verify the ZIP hash.
2. In Windows PowerShell 5.1, `Parser.ParseFile` the V5.1 installer in the parent process; do not invoke it if there are parse errors.
3. Run the V5.1 installer with `-PackageZip`, `-ProjectRoot`, and `-PythonExe`. No PriorPackageZip argument is required. It checks four exact V4 preimages, 35 source pins, C11-C frozen manifest, staged Python tests, PowerShell AST, atomic I/O 6/6, and runs the installed Pursuit runner in PREPARE_ONLY.
4. The installer must report 4/4 replacements, all add-only docs, 35/35 pins, frozen manifest PASS, and `PASS_PREPARE_ONLY_NO_RENDER`. Confirm that `renderer_invoked`, `godot_invoked`, `ffmpeg_invoked`, `production_media_created`, and `production_dispatch` are all false.
5. The prepare-only run must report T1 as `PASS_EXISTING_T1_REUSED_NO_RERENDER` and show only T2–T5 as executable. It must not create a new batch lock or authorization marker.
6. Independently inspect the install receipt, transaction journal, real backups, postimages, and `T1_RECOVERY_AUDIT` before deciding whether to authorize execution. A new BatchId is generated per execution; any started execution attempt is one-shot and a failed attempt is never retried with the same ID.
7. After T2–T5 technical qualification, review final A/C videos and A/B/C music independently. No family is accepted by installer status alone.

Governance remains `GIT_CHECKS=SKIPPED`, `COMMITS=OPERATOR_MANAGED`, E1 `PREPARE_ONLY`, family adapter `NOT_CONNECTED_E1`, `PRODUCTION_DISPATCH=FALSE`, `RELEASE_AUTHORITY=NONE`.

## V5.3 installer deep-hardening addendum — 2026-11-15

The first complete static review found that V5.3 still set `transaction_started=true` before making its four replacement backups. This was corrected: backup preparation/journaling now runs with `transaction_started=false`; every backup is hash/byte verified and persisted; all 20 targets are rechecked immediately before the transaction boundary; and each individual target is rechecked just before its atomic operation. The installer also scans ZIP member names and duplicate paths before extraction. The staged canonical fixture is copied to both `tests/fixtures` and `definitions`, matching the test imports and canonical path consumers. The staged suite now contains 37 Python tests. The receipt and failure record carry backup records.

Status is **BUILT, NOT INSTALLED**. The Linux build environment cannot execute Windows PowerShell 5.1, so native AST/atomic-I/O checks remain mandatory operator gates. No renderer or media generation is part of installation. V5/V5.1 remain invalid.

V5.3 refuerza además el límite transaccional: exige que existan previamente todos los directorios padre; comprueba el binding exacto de cada destino REPLACE con su payload; usa creación atómica exclusiva para ADD (no sobrescribe un destino concurrente); y limita el rollback a operaciones confirmadas o a la operación REPLACE en vuelo. Los temporales en vuelo se limpian en fallo. La suite Python se exige exactamente en 37/37 y la prueba atómica amplía a 7/7 con colisión ADD.
