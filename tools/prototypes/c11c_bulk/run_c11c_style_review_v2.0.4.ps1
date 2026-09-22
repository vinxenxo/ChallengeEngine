param(
    [int[]]$Seeds = @(314159, 271828, 161803, 112358, 577215, 8675309, 424242, 990001),
    [switch]$KeepExistingReviewAssets
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$ReviewRoot = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_review_assets'

Write-Host '[C11-C-STYLE-REVIEW] STEP 1/4 - cleanup regenerable prototype media'
& (Join-Path $PSScriptRoot 'clean_c11c_artifacts.ps1') -Apply
if ($LASTEXITCODE -ne 0) { throw "Artifact cleanup failed: exit=$LASTEXITCODE" }

if (-not $KeepExistingReviewAssets) {
    Write-Host '[C11-C-STYLE-REVIEW] STEP 2/4 - reset previous review assets'
    if (Test-Path -LiteralPath $ReviewRoot) {
        Remove-Item -LiteralPath $ReviewRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null
} else {
    Write-Host '[C11-C-STYLE-REVIEW] STEP 2/4 - keeping existing review assets'
}

Write-Host '[C11-C-STYLE-REVIEW] STEP 3/4 - multiseed render across all five families'
$bulk = Join-Path $PSScriptRoot 'run_c11c_multiseed_bulk.ps1'
& powershell -NoProfile -ExecutionPolicy Bypass -File $bulk -Seeds $Seeds
if ($LASTEXITCODE -ne 0) { throw "Multiseed bulk failed: exit=$LASTEXITCODE" }

Write-Host '[C11-C-STYLE-REVIEW] STEP 4/4 - regenerate GIFs and keyframes'
$reviews = Join-Path $PSScriptRoot 'export_all_review_assets.ps1'
& powershell -NoProfile -ExecutionPolicy Bypass -File $reviews -InputRoot (Join-Path $ProjectRoot 'artifacts\prototypes') -OutputRoot $ReviewRoot
if ($LASTEXITCODE -ne 0) { throw "Review export failed: exit=$LASTEXITCODE" }

Write-Host '[C11-C-STYLE-REVIEW] COMPLETE - review corpus rebuilt'
Write-Host ("[C11-C-STYLE-REVIEW] Seeds: " + ($Seeds -join ', '))
Write-Host ("[C11-C-STYLE-REVIEW] Renders: " + ($Seeds.Count * 5))
Write-Host ("[C11-C-STYLE-REVIEW] Review root: " + $ReviewRoot)
