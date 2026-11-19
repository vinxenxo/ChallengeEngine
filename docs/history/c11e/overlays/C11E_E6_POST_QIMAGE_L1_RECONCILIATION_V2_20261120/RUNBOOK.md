# Runbook — post-QImage L1 reconciliation V2

## Preconditions

V2 installer must report `INSTALL_STATUS=PASS_ADD_ONLY`, `INSTALL_FILES=18/18 VERIFIED` and `DOCS_FILES=15/15 VERIFIED`. Run the 21 V2 unit tests. Do not rerun V2.7 or the V1 audit.

## Read-only audit

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\RUN_C11E_E6_POST_QIMAGE_L1_RECONCILIATION_V2.ps1'
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw 'PHASE_RECONCILIATION_V2_RUNNER_MISSING' }
& (Join-Path $PSHOME 'powershell.exe') -NoProfile -ExecutionPolicy Bypass -File $Runner -ProjectRoot $ProjectRoot -PythonExe $PythonExe
$AuditExit = $LASTEXITCODE
if ($AuditExit -ne 0) { throw "PHASE_RECONCILIATION_V2_BLOCKED:$AuditExit; preserve receipt and logs" }
```

## Required result

`READ_ONLY_EVIDENCE_CHECKS=18/18 PASS` and `PHASE_RECONCILIATION_V2_STATUS=PASS_READ_ONLY_E6_PHASE_RECONCILIATION_V2_WITH_VISUAL_REVIEW_PENDING`.

This is read-only reconciliation, not E6 acceptance or execution authority. Preserve the V1 blocked receipt as incident evidence.
