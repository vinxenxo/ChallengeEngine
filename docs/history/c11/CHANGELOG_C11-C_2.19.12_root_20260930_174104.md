# CHANGELOG — C11-C 2.19.12

## V36 — Maintenance StrictMode Count hardening

- Fixed `tools/maintenance/verify_repository_layout.ps1` so singleton pipeline results cannot break `.Count` checks under PowerShell StrictMode.
- Fixed `tools/maintenance/create_c11c_freeze_zip.ps1` with the same zero/one/many collection normalization.
- No product/runtime/mechanics changes.
- Freeze gate remains unchanged in meaning: this is tooling robustness only.
