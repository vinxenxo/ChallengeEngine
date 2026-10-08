# CHANGELOG — C11-C 2.19.12

## V36 — Maintenance StrictMode Count hardening

- Fixed `tools/maintenance/verify_repository_layout.ps1` so singleton pipeline results cannot break `.Count` checks under PowerShell StrictMode.
- Fixed `tools/maintenance/create_c11c_freeze_zip.ps1` with the same zero/one/many collection normalization.
- No product/runtime/mechanics changes.
- Freeze gate remains unchanged in meaning: this is tooling robustness only.

## V39 — Freeze ZIP quarantine exclusion

- Fixed `tools/maintenance/create_c11c_freeze_zip.ps1` so `docs/history/root_conflicts/` remains preserved in the repository but is excluded from the frozen source ZIP.
- This prevents quarantined legacy conflict files such as `c11c-maintenace/main.py` and `run.bat` from triggering the ZIP forbidden-entry gate.
- The freeze gate itself remains strict: the forbidden-entry validation is unchanged; only the source-package exclusion set is corrected.
- No product/runtime/mechanics changes.
