[CmdletBinding()]
param(
    [switch]$SkipHeavyPhysical,
    [switch]$SkipReviews
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$ProjectRoot = (Resolve-Path $PSScriptRoot).Path
Set-Location $ProjectRoot
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$A1Root = "artifacts\qa\c11a1_challenge\full_acceptance_$stamp"

function Invoke-Step([string]$Label, [scriptblock]$Action) {
    Write-Host "`n=============================================="
    Write-Host $Label
    Write-Host "=============================================="
    & $Action
    if ($LASTEXITCODE -ne 0) { throw "$Label failed with exit code $LASTEXITCODE" }
}

Invoke-Step 'C11C workspace preparation' {
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\tools\maintenance\prepare_c11c_acceptance_workspace.ps1' -RotateAcceptanceRoots
}

Invoke-Step 'C11-C suite self-test' { python '.\c11c-suite\self_test.py' }
Invoke-Step 'Producer self-test' { python '.\c11c-suite\c11c-producer\self_test.py' }
Invoke-Step 'Producer GUI contract' { python '.\c11c-suite\c11c-producer\test_producer_gui_contract.py' }
Invoke-Step 'Retro reference contract' { python '.\c11c-suite\test_retro_reference_contract.py' }
Invoke-Step 'Full logical corpus' { python '.\tests\run_all.py' }
Invoke-Step 'C11-A.1 — 54 fresh runs' {
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1' -OutputRoot $A1Root
}
Invoke-Step 'Retrocompatibility — 54 telemetry/A-B checks' {
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\tools\c11freeze\run_retrocompatibility.ps1'
}
if (-not $SkipHeavyPhysical) {
    Invoke-Step 'C10-C physical smoke' {
        powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\tools\qa\c10\run_C10C_physical_export.ps1'
    }
    Invoke-Step 'Physical export suite' {
        powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\tools\c11freeze\run_physical_export_suite.ps1'
    }
}
if (-not $SkipReviews) {
    Invoke-Step 'C11-C Art Direction corpus' {
        powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1' -Workers 7 -All -Reset
    }
    Invoke-Step 'C11-C Visual Drill review smoke' {
        powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1' -Seeds 314159 -Families tracking,saccade,pursuit,peripheral_scan -Smoke -ResetReviewAssets
    }
}

Write-Host "`n=============================================="
Write-Host 'C11-C 2.19.3 — FULL ACCEPTANCE PASS'
Write-Host "=============================================="
