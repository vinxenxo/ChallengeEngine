# C11-E Installer Incident Register — V51 (2026-11-16)

## Peripheral Scan combined overlay — final disposition

**Accepted installer run:** `C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2_20261116_20261116T115533Z_df4b90b9` using package SHA `4a21188d104d95e2c23842cd08be345cd82eecaa0ab5da11be8469a1f3d88b7d`.

- Windows PowerShell 5.1 AST: 4/4 PASS.
- Atomic helper dot-source and atomic JSON writer preflight: PASS.
- Python staged tests: 51/51 PASS; `py_compile` 3/3 PASS.
- Atomic I/O: 7/7 PASS.
- Source pins: 38/38 pre, pretransaction and post; frozen C11-C manifest PASS.
- Install transaction: exactly 21 unique ADD operations, 21/21 ADDED; zero replacements; committed.
- Staged and installed PREPARE_ONLY: PASS_NO_RENDER.
- Installed runner launched the one-shot five-tier batch; all five child exits 0 and technical PASS.

The accepted FIX2 helper change addresses a Windows classic path-length failure during atomic JSON temporary-file creation. It uses short same-directory GUID temporary/backup names. The run above demonstrates successful native Windows execution of the helper and transaction.

## Failed attempts — preserve as historical evidence

- Post-install continuation V1/V2/V3 did not start the family batch. V3 stopped at `INSTALLED_21_POSTIMAGE_AUDIT` because all 21 expected files were absent in the pre-install snapshot. Those tools were based on a false installed-state assumption and are retired.
- Original combined V2 stopped at PowerShell AST because of a trailing comma in the guide-hash hashtable; no transaction began.
- PS51 FIX1 passed AST but failed in atomic JSON temporary-file creation before transaction. The generated temp path exceeded the classic Windows path limit.
- PS51 FIX2 corrected temp/backup naming and completed the installation, PREPARE_ONLY, and one-shot batch in the same invocation. It is the accepted installation path. Do not rerun it.

All prior failure receipts, temporary stages and logs remain evidence-only. Do not delete or reinterpret them as successful installations. No automatic retry or rollback was performed after the accepted install commit.

## Permanent controls

C11-C frozen manifest remains `e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953` / 796,318 bytes. E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; production dispatch false; release authority none. No Git bookkeeping; commits operator-managed; source SHA pins enforced.
