# Runbook — E6 post-QImage L1 phase reconciliation V1

## Preconditions

1. V2.7 installer PASS and V2.7 runner PASS already exist. Do not repeat either run.
2. Preserve their exact receipts and sidecars.
3. Confirm Python 3.13.14 exists at `%LOCALAPPDATA%\Programs\Python\Python313\python.exe`. No dependency changes.

## Execute once

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\RUN_C11E_E6_POST_QIMAGE_L1_RECONCILIATION_V1.ps1'
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw 'PHASE_RECONCILIATION_RUNNER_MISSING' }
& (Join-Path $PSHOME 'powershell.exe') -NoProfile -ExecutionPolicy Bypass -File $Runner -ProjectRoot $ProjectRoot -PythonExe $PythonExe
$Exit = $LASTEXITCODE
if ($Exit -ne 0) { throw "PHASE_RECONCILIATION_BLOCKED:$Exit; preserve its receipt" }
```

## Required result

`PHASE_RECONCILIATION_STATUS=PASS_READ_ONLY_E6_PHASE_RECONCILIATION_WITH_VISUAL_REVIEW_PENDING`. The runner produces its own immutable JSON receipt and SHA-256 sidecar under `artifacts/tests/c11e/e6_post_qimage_l1_reconciliation/<RUN_ID>/`.

## Failure discipline

A missing/mismatched receipt, sidecar, source pin or preview blocks. Do not rerun predecessor suites. Preserve the failed output and correct only the exact missing/mismatched evidence with a new versioned overlay. `NO_PASS_EMITTED=TRUE` is mandatory on failure.
