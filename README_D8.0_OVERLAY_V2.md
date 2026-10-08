# C11-D D8.0 overlay V2

Repairs the D8.0 inventory runner path-resolution bug found during the first execution.

Fixes:
- repository root is resolved in the script body, not in the `param()` default;
- `-BaselineZip` is accepted without requiring `-VerifyBaselineZip`;
- when a baseline path is supplied, its path and SHA-256 are recorded in D8.0 evidence;
- `-VerifyBaselineZip` remains available as an optional strict assertion, but is not required for the normal D8.0 inventory run.

No C11-C, D7, media, release product, seed, renderer, or production changes.

Apply from repository root:

```powershell
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_D8.0_CANONICAL_INVENTORY_OVERLAY_V2.zip" `
  -DestinationPath "." `
  -Force
```

Recommended D8.0 run using the known baseline location:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File ".\tools\c11d\d8\run_d8_0_inventory.ps1" `
  -BaselineZip ".\artifacts\releases\ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip"
```
