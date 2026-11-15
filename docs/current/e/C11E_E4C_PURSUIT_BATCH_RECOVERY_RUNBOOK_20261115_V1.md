# Pursuit V3 recovery runbook — operator procedure

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
