# C11-D D7.0 Overlay

This root-relative overlay opens D7 with an audit-only checkpoint.

Apply from the repository root with:

```powershell
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_D7.0_PRODUCTION_MATRIX_CATALOG_AUDIT_V1.zip" `
  -DestinationPath "." `
  -Force
```

Run the PowerShell 5.1 parser audit, then execute:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11d\d7\run_d7_0_production_matrix_catalog_audit.ps1
```

Run it twice.

D7.0 writes only under `artifacts/tests/c11d_d7/d7_0/` and does not create a `release/` output.

D7.0 does not create the canonical matrix. That begins in D7.1.
