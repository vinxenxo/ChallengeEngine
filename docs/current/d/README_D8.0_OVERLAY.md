# C11-D D8.0 overlay

This overlay adds only the D8.0 governance/inventory contract, handover/entry documents, and a read-only inventory runner.

It does not modify C11-C, D7 authorities, media, release products, production executors, renderer settings, seeds, or existing tests.

Apply from repository root. Then run in Windows PowerShell 5.1:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11d\d8\run_d8_0_inventory.ps1 -VerifyBaselineZip -BaselineZip "$env:USERPROFILE\Downloads\ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip"
```

D8.0 evidence is written only to:

`artifacts/tests/c11d_d8/d8_0/`

No FFmpeg/FFprobe media operation is executed by this runner.
