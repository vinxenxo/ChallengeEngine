[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $ProjectRoot

function Invoke-Step([string]$Label,[scriptblock]$Action){
    Write-Host "`n============================================================"
    Write-Host "[C11C-FOCUSED] $Label"
    Write-Host "============================================================"
    & $Action
    if($LASTEXITCODE -ne 0){ throw "$Label failed with exit code $LASTEXITCODE" }
}

Invoke-Step 'Suite self-test' { python .\c11c-suite\self_test.py }
Invoke-Step 'Producer self-test' { python .\c11c-suite\c11c-producer\self_test.py }
Invoke-Step 'Producer GUI contract' { python .\c11c-suite\c11c-producer\test_producer_gui_contract.py }
Invoke-Step 'Suite launcher audit' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\verify_c11c_suite_launchers.ps1 }
Invoke-Step 'Visual Drill envelope-path lifecycle contract' { & .\c11c-suite\c11c-test\run_suite.bat C11CVisualDrillReviewEnvelopePathContractTest.gd }
Invoke-Step 'Parallel review worker isolation contract' { & .\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd }
Invoke-Step 'One video each type smoke' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\run_c11c_one_video_each_type.ps1 }
Write-Host '[C11C-FOCUSED] COMPLETE PASS - focused contracts + 3-video smoke'
